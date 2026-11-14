"""Teaching the interpreter.

teach(): it imitates hand-written words on dreams, where every step has an exact answer.
Rediscovery (below) then gives meaning to free words from puzzles no hand-written program
explains: the puzzle no longer has to be solved before it can teach anything.
"""

import copy
import math
import random
import time

import numpy as np
import torch
from torch.nn import functional as F

from . import curriculum
from .state import VOCAB, encode


def tensors(samples, vocab, size, device="cpu"):
    """[(picture, word, result)] -> tokens in, operation ids, argument ids, tokens out."""
    x = torch.as_tensor(np.stack([encode(g, size).ravel() for g, _, _ in samples]), device=device)
    y = torch.as_tensor(np.stack([encode(o, size).ravel() for _, _, o in samples]), device=device)
    op, arg = torch.as_tensor([vocab.ids(w) for _, w, _ in samples], device=device).T
    return x, op, arg, y


def dream(grids, vocab, rng, side, n):
    """n exact steps of hand-written words, the words drawn evenly."""
    out = []
    while len(out) < n:
        w = rng.choice(vocab.known)
        s = curriculum.step(grids, vocab.known, w, rng, side)
        if s is not None:
            out.append((s[0], w, s[1]))
    return out


def device_of(model):
    return next(model.parameters()).device


def loss_of(model, batch):
    x, op, arg, y = batch
    return F.cross_entropy(model(x, op, arg).reshape(-1, VOCAB), y.reshape(-1))


class Ema:
    """A slow copy of the weights (what gets tested and saved)."""

    def __init__(self, model, decay=0.999):
        self.model, self.decay = copy.deepcopy(model).eval(), decay
        for p in self.model.parameters():
            p.requires_grad_(False)

    @torch.no_grad()
    def update(self, model):
        for a, b in zip(self.model.parameters(), model.parameters()):
            a.lerp_(b, 1 - self.decay)


def teach(model, vocab, grids, steps, side, batch=64, lr=1e-3, warmup=500, seed=0,
          every=2000, check=None, log=print):
    """Imitate the hand-written words on dreams. Returns the slow copy of the model."""
    rng = random.Random(seed)
    torch.manual_seed(seed)
    opt = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=0.01, betas=(0.9, 0.95))
    ema = Ema(model)
    t0, run = time.time(), 0.0
    for step in range(1, steps + 1):
        for g in opt.param_groups:
            g["lr"] = lr * min(step / warmup, 0.1 + 0.9 * 0.5 * (1 + math.cos(math.pi * step / steps)))
        model.train()
        loss = loss_of(model, tensors(dream(grids, vocab, rng, side, batch), vocab, model.size,
                                      device_of(model)))
        opt.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        opt.step()
        ema.update(model)
        run = loss.item() if step == 1 else 0.98 * run + 0.02 * loss.item()
        if step % every == 0 or step == steps:
            note = f" {check(ema.model)}" if check else ""
            log(f"step {step}/{steps} loss {run:.4f} {time.time() - t0:.0f}s{note}")
    return ema.model


# ------------------------------------------------------------------ free words
# A free word gets its meaning from puzzles no hand-written program explains. Each puzzle
# keeps one of its examples back as a check: the word is trained only on the others, and
# the puzzle counts as explained by the word only when the check example also comes out
# exactly right. A word that fits what it trained on but not the check has memorised the
# puzzle, and the puzzle is turned away.

GROWTH = (1, 2, 3, 5, 8, 12, 18, 27, 40, 60, 90, 135)   # unconfirmed members allowed, by round
NEAR = 3.0      # ... and only puzzles whose loss is within this factor of its third best


def options(vocab, slot, puzzle):
    """The ways free word `slot` could be the puzzle's rule: bare, or taking one of the
    colours in the puzzle's answers."""
    op, takes_colour = slot
    if not takes_colour:
        return [vocab.free(op)]
    cols = sorted({int(c) for _, o in puzzle["train"] for c in np.unique(o)})
    return [vocab.free(op, c) for c in cols]


@torch.no_grad()
def fits(model, vocab, puzzles, slots, idx):
    """For each puzzle in idx and each free word in `slots`: its best option as
    (loss on the training examples, training examples exact, check example exact, word)."""
    model.eval()
    rows = [(i, s, w) for i in idx for s in slots for w in options(vocab, s, puzzles[i])]
    best = {}
    for a in range(0, len(rows), 256):
        part = rows[a:a + 256]
        samples = [(g, w, o) for i, _, w in part for g, o in puzzles[i]["train"]]
        x, op, arg, y = tensors(samples, vocab, model.size, device_of(model))
        logits = model(x, op, arg)
        ce = F.cross_entropy(logits.reshape(-1, VOCAB), y.reshape(-1), reduction="none")
        ce = ce.view(len(samples), -1).mean(1)
        ok = (logits.argmax(-1) == y).all(1)
        k = 0
        for i, s, w in part:
            n = len(puzzles[i]["train"])
            loss = ce[k:k + n - 1].mean().item()
            got = (loss, bool(ok[k:k + n - 1].all()), bool(ok[k + n - 1]), w)
            k += n
            if (i, s) not in best or (not got[1], got[0]) < (not best[i, s][1], best[i, s][0]):
                best[i, s] = got
    return best


def optimiser(model, lr=3e-4, word_lr=3e-3):
    """Word vectors learn fast; the rest of the interpreter moves slowly."""
    words = [p for n, p in model.named_parameters() if n.startswith(("op.", "arg."))]
    rest = [p for n, p in model.named_parameters() if not n.startswith(("op.", "arg."))]
    return torch.optim.AdamW([{"params": rest, "lr": lr}, {"params": words, "lr": word_lr}],
                             weight_decay=0.0, betas=(0.9, 0.95))


def practise(model, vocab, puzzles, members, grids, side, opt, rng, steps=150, batch=32,
             settled=()):
    """Train on the members' training examples (never their check example). Mixed in, so
    nothing already learned is lost: as many dreams of the hand-written words, and half
    as many examples from puzzles that earlier learned words already explain (`settled`).
    members, settled = [(puzzle index, the word it is taken to be), ...]."""
    model.train()
    for _ in range(steps):
        mine = []
        for group, n in ((members, batch), (settled, batch // 2)):
            for _ in range(n if group else 0):
                i, w = rng.choice(group)
                g, o = rng.choice(puzzles[i]["train"][:-1])
                mine.append((g, w, o))
        both = mine + dream(grids, vocab, rng, side, batch)
        loss = loss_of(model, tensors(both, vocab, model.size, device_of(model)))
        opt.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        opt.step()


def rediscover(model, vocab, puzzles, grids, side, rounds=12, steps=150, batch=32,
               lr=3e-4, word_lr=3e-3, polish=2, seed=0, log=print):
    """Give meaning to free words from unexplained puzzles (the last training example of
    each puzzle is its check and is never trained on).

    One word at a time: a new word starts from a single unexplained puzzle, tried both
    bare and taking a colour. Each round it trains with the puzzles it fits best, chosen
    afresh, a few more each round (GROWTH), and only puzzles it fits about as well as its
    best few (NEAR). It trains on its members' training examples, with dreams of the
    hand-written words and the puzzles of words already kept mixed in, so nothing is
    forgotten. Puzzles it has memorised are turned away. The bare or colour form that
    ends up explaining more puzzles is kept, and practised a little longer on the puzzles
    it explains. Returns
    {puzzle index: word} for every explained puzzle, and the slots kept."""
    rng = random.Random(seed)
    torch.manual_seed(seed)
    opt = optimiser(model, lr, word_lr)
    explained, kept, banned = {}, [], set()
    free_ops = list(range(vocab.n_free))

    def train(members):
        settled = [(i, w) for i, w in explained.items() if w is not None]
        practise(model, vocab, puzzles, members, grids, side, opt, rng, steps, batch, settled)

    while len(free_ops) >= 2:
        todo = [i for i in range(len(puzzles)) if i not in explained]
        if len(todo) < 3:
            break
        start = todo[0]
        pair = [(free_ops[0], False), (free_ops[1], True)]      # bare, taking a colour
        with torch.no_grad():                                   # fresh meanings
            for op, _ in pair:
                model.op.weight[vocab.op_id[f"new{op}"]].normal_(std=1 / math.sqrt(model.hidden))
        members = {s: {start: None} for s in pair}
        waited = {s: {} for s in pair}
        for r in range(rounds):
            found = fits(model, vocab, puzzles, pair, todo)
            for s in pair:
                sure = {i for i in todo if found[i, s][1] and found[i, s][2]}
                for i in members[s]:              # fits what it trained on but keeps
                    if found[i, s][1] and not found[i, s][2] and i != start:   # failing its
                        waited[s][i] = waited[s].get(i, 0) + 1                 # check:
                        if waited[s][i] > 2:                                   # memorised
                            banned.add((i, s))
                # Who trains with the word this round: the starting puzzle, every puzzle
                # it has confirmed, and the unconfirmed puzzles it fits best, up to
                # GROWTH[r] of them. They are chosen afresh each round, and only from
                # puzzles it fits about as well as its best few (within NEAR times their
                # typical loss): a puzzle of some other word fits far worse and stays out.
                # (Measured on gravity, reports/words_g0.md: after training on one puzzle
                # the 8 best-fitting others were almost all of the same word, but a word
                # needs many more than 8 puzzles before any pass their check, so growth
                # cannot wait for confirmations.)
                n = GROWTH[min(r, len(GROWTH) - 1)]
                ranked = sorted((i for i in todo if i != start and i not in sure
                                 and (i, s) not in banned), key=lambda i: found[i, s][0])
                if len(ranked) > 5:
                    near = NEAR * found[ranked[2], s][0]
                    ranked = [i for i in ranked if found[i, s][0] <= near]
                keep = {i: found[i, s][3] for i in [start] + sorted(sure) + ranked[:n - 1]}
                members[s] = keep
            log(f"  word new{pair[0][0]}/new{pair[1][0]} round {r + 1}: members "
                f"{len(members[pair[0]])}/{len(members[pair[1]])}")
            train([(i, w) for s in pair for i, w in members[s].items()])
        found = fits(model, vocab, puzzles, pair, todo)
        sure = {s: {i: found[i, s][3] for i in todo if found[i, s][1] and found[i, s][2]}
                for s in pair}
        best = max(pair, key=lambda s: (len(sure[s]), not s[1]))     # ties: the bare word
        log(f"  kept new{best[0]}{' (takes a colour)' if best[1] else ''}: explains "
            f"{len(sure[best])} puzzles (other form: {len(sure[pair[1 - pair.index(best)]])})")
        if len(sure[best]) < 3:          # a word must earn its place: at least 3 puzzles
            banned.update((start, s) for s in pair)
            explained[start] = None      # set this puzzle aside and try another start
            if sum(v is None for v in explained.values()) >= 3:
                break
            continue
        for _ in range(polish):          # the word has earned its place: practise it on
            train(list(sure[best].items()))             # the puzzles it explains
        if polish:
            found = fits(model, vocab, puzzles, [best], todo)
            sure[best] = {i: found[i, best][3] for i in todo
                          if found[i, best][1] and found[i, best][2]}
            log(f"  after practice it explains {len(sure[best])} puzzles")
        explained.update(sure[best])
        kept.append(best)
        free_ops.remove(best[0])
    return {i: w for i, w in explained.items() if w is not None}, kept
