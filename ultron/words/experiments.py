"""Gate G0 of docs/MECHANISM.md, on small pictures and a CPU.

G0-a, carrying out: the interpreter is taught 48 hand-written words on dreams. Does it
carry out single words, and programs of six words, exactly on pictures kept aside?

G0-b, rediscovery: five families of hand-written words are never shown to it. For each
family in turn, Ultron gets only puzzles whose hidden rule is a word of that family. Does
a free word come to mean the hidden word, on pictures and (for colour words) colours it
never trained on? Three checks keep the answer honest: the hand-written words alone must
not explain those puzzles; a vector fitted to each puzzle separately is the comparison;
and each learned word is tested for being a mere abbreviation.

    python -m ultron words teach      # G0-a's training (about two hours on four cores)
    python -m ultron words g0         # both gates, writes reports/words_g0.md
"""

import json
import os
import random
import time

import torch
from torch.nn import functional as F

from . import crystallise, curriculum, learn, measure, search
from .interpreter import Interpreter, load, save
from .state import VOCAB
from .vocab import ARGS, HIDDEN_G0, KNOWN_G0, Vocab, Word

HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASE = os.path.join(HERE, "brain", "words_base.pt")
REPORT = os.path.join(HERE, "reports", "words_g0.md")
UNSEEN_COLOURS = (4, 7)       # never used in a colour family's training puzzles
FULL = dict(side=8, hidden=96, steps=30000, n_free=8, puzzles=120, held=40, rounds=12,
            round_steps=150, per_word=20, chains=200)
QUICK = dict(side=6, hidden=48, steps=300, n_free=4, puzzles=24, held=8, rounds=3,
             round_steps=30, per_word=5, chains=30)


def teach(quick=False, path=None, steps=None, start=None, lr=1e-3, log=print):
    """G0-a's training: imitate the hand-written words on dreams, and save the result.

    The interpreter is saved every twelfth of the run. `start` continues from a saved one
    (after an interruption), with a fresh optimiser; use a lower `lr` then."""
    cfg = QUICK if quick else FULL
    grids, aside = curriculum.pool(side=cfg["side"])
    vocab = Vocab(KNOWN_G0, n_free=cfg["n_free"])
    path = path or BASE
    done = 0
    if start:
        model, ck = load(start)
        done = ck.get("steps", 0)
    else:
        model = Interpreter(len(vocab.ops), len(ARGS), cfg["side"] + 1, hidden=cfg["hidden"])
    steps = steps or cfg["steps"]
    every = max(steps // 12, 1)
    seen = [0]

    def check(m):
        seen[0] = min(seen[0] + every, steps)
        save(m, path, side=cfg["side"], steps=done + seen[0], resumed_at=done or None)
        s = measure.steps_exact(m, vocab, aside, cfg["side"], per_word=5)
        return f"single words exact {measure.share(s):.3f}"

    model = learn.teach(model, vocab, grids, steps, cfg["side"], lr=lr, check=check,
                        every=every, seed=done, log=log)
    save(model, path, side=cfg["side"], steps=done + steps, resumed_at=done or None)
    return model


def carrying_out(model, vocab, aside, cfg):
    """G0-a: single words (by family) and six-word programs, on pictures kept aside."""
    score = measure.steps_exact(model, vocab, aside, cfg["side"], per_word=cfg["per_word"])
    fam = {}
    for w, (a, b) in score.items():
        x = fam.setdefault(w.op, [0, 0])
        x[0] += a
        x[1] += b
    right, total = measure.chains_exact(model, vocab, aside, cfg["side"], n=cfg["chains"])
    return {"single": measure.share(score), "by_family": fam,
            "chains_right": right, "chains": total}


def _puzzles(programs, grids, rng, side, n, examples):
    out = []
    for k in range(n * 20):
        p = curriculum.puzzle(programs[k % len(programs)](rng), grids, rng, side, examples)
        if p:
            out.append(p)
            if len(out) == n:
                break
    return out


def fitted_vector(model, vocab, puzzle, steps=80, lr=0.05):
    """The comparison: no shared word. One vector is fitted to this puzzle's examples by
    gradient descent (the interpreter itself is left alone), then answers the test."""
    from .learn import tensors
    for p in model.parameters():
        p.requires_grad_(False)
    n_known = len(vocab.ops) - vocab.n_free
    w = model.op.weight[:n_known].mean(0, keepdim=True).clone().requires_grad_(True)
    x, _, _, y = tensors([(g, vocab.known[0], o) for g, o in puzzle["train"]], vocab, model.size)
    opt = torch.optim.Adam([w], lr=lr)
    model.eval()
    for _ in range(steps):
        loss = F.cross_entropy(model(x, word=w.expand(len(x), -1)).reshape(-1, VOCAB), y.reshape(-1))
        opt.zero_grad()
        loss.backward()
        opt.step()
    with torch.no_grad():
        fit = bool((model(x, word=w.expand(len(x), -1)).argmax(-1) == y).all())
        tx, _, _, ty = tensors([(puzzle["test"][0], vocab.known[0], puzzle["test"][1])],
                               vocab, model.size)
        right = bool((model(tx, word=w).argmax(-1) == ty).all())
    for p in model.parameters():
        p.requires_grad_(True)
    return fit, right


def rediscovery(family, base_path=None, quick=False, seed=0, log=print):
    """G0-b for one hidden family, starting from the taught interpreter."""
    cfg = QUICK if quick else FULL
    side = cfg["side"]
    model, _ = load(base_path or BASE)
    grids, aside = curriculum.pool(side=side)
    vocab = Vocab(KNOWN_G0, n_free=cfg["n_free"])
    rng = random.Random(seed)
    hidden = HIDDEN_G0[family]
    takes_colour = hidden[0].param in range(10)
    shown = [w for w in hidden if not (takes_colour and w.param in UNSEEN_COLOURS)]
    t0 = time.time()

    # puzzles whose hidden rule is one word of the family (4 examples: 3 to learn from,
    # 1 as the check), and held-out puzzles on kept-aside pictures: the word alone, and
    # the word with a hand-written word before or after it
    # a family of several separate words (gravity: four sides) gets half the usual number
    # of puzzles for each word, since each word has to be learned from its own puzzles
    n_train = cfg["puzzles"] if takes_colour or len(shown) == 1 else cfg["puzzles"] // 2 * len(shown)
    train = _puzzles([lambda r, w=w: [w] for w in shown], grids, rng, side, n_train, 4)
    direct = _puzzles([lambda r, w=w: [w] for w in shown], aside, rng, side, cfg["held"], 3)
    mixed = _puzzles([lambda r, w=w: [r.choice(KNOWN_G0), w] for w in shown]
                     + [lambda r, w=w: [w, r.choice(KNOWN_G0)] for w in shown],
                     aside, rng, side, cfg["held"], 3)

    # check 1: what the hand-written words alone explain (those puzzles need no new word)
    alone = [bool(search.explain(p, vocab, depth=2, side=side, want=1)) for p in train]
    todo = [p for p, a in zip(train, alone) if not a]
    without = {"direct": sum(search.solve(p, vocab, depth=2, side=side)[0] for p in direct),
               "mixed": sum(search.solve(p, vocab, depth=2, side=side)[0] for p in mixed)}
    log(f"{family}: {len(train)} puzzles, {sum(alone)} explained by hand-written words alone")

    # check 2: one vector fitted per puzzle, no shared word
    vec = [fitted_vector(model, vocab, p) for p in direct]

    explained, kept = learn.rediscover(model, vocab, todo, grids, side,
                                       rounds=cfg["rounds"], steps=cfg["round_steps"],
                                       seed=seed, log=log)

    # which free word came to stand for each hidden word (the one most of its puzzles chose)
    votes = {}
    for i, w in explained.items():
        h = todo[i]["program"][0]
        key = h.op if takes_colour else h
        votes.setdefault(key, {}).setdefault(w.op, 0)
        votes[key][w.op] += 1
    stands = {}
    for h in hidden:
        key = h.op if takes_colour else h
        if key in votes:
            op = max(votes[key], key=votes[key].get)
            stands[h] = Word(op, h.param if takes_colour else None)
    ids = {h: vocab.ids(w) for h, w in stands.items()}
    exact = measure.steps_exact(model, vocab, aside, side, per_word=cfg["per_word"],
                                words=list(ids), ids=ids) if ids else {}
    seen = {h: v for h, v in exact.items() if h in shown}
    unseen = {h: v for h, v in exact.items() if h not in shown}

    with_words = {"direct": sum(search.solve(p, vocab, model, kept, 2, side)[0] for p in direct),
                  "mixed": sum(search.solve(p, vocab, model, kept, 2, side)[0] for p in mixed)}
    new = []
    for h, w in stands.items():
        if h in shown and w.op not in [n[0] for n in new]:
            prog, changed = crystallise.imitate(model, vocab, w, aside, side)
            new.append((w.op, None if prog is None else " > ".join(map(str, prog)), changed))
    still = measure.steps_exact(model, vocab, aside, side, per_word=5)
    out = {
        "family": family, "puzzles": len(train), "explained_by_hand_written": sum(alone),
        "explained_by_learned_words": len(explained), "to_explain": len(todo),
        "words_kept": [f"new{op}" + (" (takes a colour)" if c else "") for op, c in kept],
        "stands_for": {str(h): str(w) for h, w in stands.items()},
        "match_seen": measure.share(seen) if seen else 0.0,
        "match_unseen_colours": measure.share(unseen) if unseen else None,
        "match_by_word": {str(h): f"{a}/{b}" for h, (a, b) in exact.items()},
        "held_direct": len(direct), "held_mixed": len(mixed),
        "without_words": without, "with_words": with_words,
        "fitted_vector": {"fits_examples": sum(f for f, _ in vec),
                          "test_right": sum(r for _, r in vec)},
        "abbreviation_of": {op: prog for op, prog, _ in new},
        "old_words_still_exact": measure.share(still),
        "seconds": round(time.time() - t0),
    }
    log(json.dumps(out, indent=1))
    return out


def diagnose(family, base_path=None, quick=False, seed=0, log=print):
    """Why is a family of several words (gravity: down, up, left, right) hard to relearn?

    Ranking: a new word trains on one puzzle alone. Of the 8 other puzzles it then fits
    best, how many have the same hidden word as that puzzle? (By chance: that word's
    share of the puzzles.) A poor ranking means the wrong puzzles train together.

    Amount: a new word is handed a clean group of 4, 8, 16 puzzles of one hidden word.
    How many of them pass their check, and how well does the word match the hidden word
    on kept-aside pictures? Poor results here mean it simply needs more to learn from."""
    cfg = QUICK if quick else FULL
    side = cfg["side"]
    grids, aside = curriculum.pool(side=side)
    vocab = Vocab(KNOWN_G0, n_free=cfg["n_free"])
    rng = random.Random(seed)
    hidden = HIDDEN_G0[family]
    puzzles = _puzzles([lambda r, w=w: [w] for w in hidden], grids, rng, side, cfg["puzzles"], 4)
    of = {}
    for i, p in enumerate(puzzles):
        of.setdefault(p["program"][0], []).append(i)
    slot, word = (0, False), vocab.free(0)
    out = {"family": family, "ranking": [], "amount": []}
    for h in hidden[:4]:
        model, _ = load(base_path or BASE)
        start = of[h][0]
        learn.practise(model, vocab, puzzles, [(start, word)], grids, side,
                       learn.optimiser(model), random.Random(seed), cfg["round_steps"])
        found = learn.fits(model, vocab, puzzles, [slot], range(len(puzzles)))
        ranked = sorted((i for i in range(len(puzzles)) if i != start),
                        key=lambda i: found[i, slot][0])[:8]
        row = {"start": str(h), "same_word_in_best_8": sum(i in of[h] for i in ranked),
               "by_chance": round(8 * (len(of[h]) - 1) / (len(puzzles) - 1), 1)}
        out["ranking"].append(row)
        log(f"ranking {row}")
    h = hidden[0]
    for n in (4, 8, 16):
        if len(of[h]) < n:
            break
        model, _ = load(base_path or BASE)
        members = [(i, word) for i in of[h][:n]]
        opt, r = learn.optimiser(model), random.Random(seed)
        for _ in range(cfg["rounds"] // 2):
            learn.practise(model, vocab, puzzles, members, grids, side, opt, r, cfg["round_steps"])
        found = learn.fits(model, vocab, puzzles, [slot], of[h][:n])
        match = measure.steps_exact(model, vocab, aside, side, per_word=cfg["per_word"],
                                    words=[h], ids={h: vocab.ids(word)})
        row = {"word": str(h), "puzzles_given": n,
               "pass_their_check": sum(found[i, slot][1] and found[i, slot][2] for i in of[h][:n]),
               "match_on_kept_aside": measure.share(match)}
        out["amount"].append(row)
        log(f"amount {row}")
    return out


def write(result, path=REPORT):
    a, b = result["carrying_out"], result["rediscovery"]
    passed = sum(r["match_seen"] >= 0.95 for r in b)
    chains = a["chains_right"] / max(a["chains"], 1)
    lines = [
        "# Learned words, gate G0 (small pictures, CPU)\n",
        "Produced by `python -m ultron words g0`. The gate and its targets were fixed in "
        "advance in [docs/MECHANISM.md](../docs/MECHANISM.md).\n",
        f"Setting: pictures up to {result['cfg']['side']} x {result['cfg']['side']}, taken only "
        f"from the practice half; an interpreter of width {result['cfg']['hidden']} "
        f"({result['parameters']:,} numbers), taught for {result['cfg']['steps']:,} steps.\n",
        "## G0-a: carrying out hand-written words\n",
        f"- Single words exact on kept-aside pictures: **{a['single']:.1%}** (target 99%).",
        f"- Programs of six words exact from start to end: **{a['chains_right']}/{a['chains']}"
        f" = {chains:.1%}** (target 90%).",
        f"- **{'Met' if a['single'] >= 0.99 and chains >= 0.9 else 'Not met'}.**\n",
        "| Family | Exact |", "|---|---|"]
    lines += [f"| {k} | {x}/{y} |" for k, (x, y) in sorted(a["by_family"].items())]
    lines += [""] + [f"{note}\n" for note in result.get("notes_a", [])]
    lines += [
        "\n## G0-b: rediscovering words it was never shown\n",
        f"Target: a free word matches the hidden word on at least 95% of kept-aside pictures "
        f"for at least 3 of the {len(HIDDEN_G0)} families. **Met for {passed} of "
        f"{len(HIDDEN_G0)}"
        + (f" ({len(b)} run so far)" if len(b) < len(HIDDEN_G0) else "") + ".**\n",
        "| Hidden family | Puzzles (explained by hand-written words alone) | Explained by "
        "learned words | Words kept | Match on kept-aside pictures | Match on colours never "
        "trained | Held-out puzzles right: without -> with learned words | One vector per "
        "puzzle: test right | New primitive? |", "|---|---|---|---|---|---|---|---|---|"]
    for r in b:
        held = r["held_direct"] + r["held_mixed"]
        wo = r["without_words"]["direct"] + r["without_words"]["mixed"]
        wi = r["with_words"]["direct"] + r["with_words"]["mixed"]
        new = "; ".join(f"{op}: {'new' if p is None else 'abbreviates ' + p}"
                        for op, p in r["abbreviation_of"].items()) or "-"
        unseen = "-" if r["match_unseen_colours"] is None else f"{r['match_unseen_colours']:.0%}"
        lines.append(
            f"| {r['family']} | {r['puzzles']} ({r['explained_by_hand_written']}) | "
            f"{r['explained_by_learned_words']}/{r['to_explain']} | "
            f"{', '.join(r['words_kept']) or 'none'} | {r['match_seen']:.0%} | {unseen} | "
            f"{wo}/{held} -> {wi}/{held} | {r['fitted_vector']['test_right']}/{r['held_direct']} "
            f"| {new} |")
    lines += ["", "Held-out puzzles are made from kept-aside pictures: half use the hidden "
              "word alone, half put a hand-written word before or after it. \"New\" means no "
              "program of up to three hand-written words imitates the learned word.", ""]
    lines += [f"{note}\n" for note in result.get("notes_b", [])]
    for d in result.get("diagnosis", []):
        lines += [f"## Why {d['family']} is hard: a diagnosis\n", d.get("note", ""), "",
                  "A new word trains on one puzzle alone. Of the 8 other puzzles it then fits "
                  "best, how many have the same hidden word?\n",
                  "| Starting puzzle | Same word among the best 8 | Expected by chance |",
                  "|---|---|---|"]
        lines += [f"| {r['start']} | {r['same_word_in_best_8']} | {r['by_chance']} |"
                  for r in d["ranking"]]
        lines += ["", "A new word is handed a clean group of puzzles of one hidden word.\n",
                  "| Hidden word | Puzzles given | Pass their check | Match on kept-aside "
                  "pictures |", "|---|---|---|---|"]
        lines += [f"| {r['word']} | {r['puzzles_given']} | {r['pass_their_check']} | "
                  f"{r['match_on_kept_aside']:.0%} |" for r in d["amount"]]
        lines += [""]
    with open(path, "w") as f:
        f.write("\n".join(lines))
    with open(path[:-3] + ".json", "w") as f:
        json.dump(result, f, indent=1, default=str)


def board(result=None, path=REPORT):
    """One cell for the scoreboard: what the last G0 run showed (or that there is none)."""
    if result is None:
        if not os.path.exists(path[:-3] + ".json"):
            return "not run"
        with open(path[:-3] + ".json") as f:
            result = json.load(f)
    rows = result["rediscovery"]
    met = sum(r["match_seen"] >= 0.95 for r in rows)
    new = sum(p is None for r in rows for p in r["abbreviation_of"].values())
    return (f"G0: {met} of {len(HIDDEN_G0)} hidden families relearned, {new} new primitives "
            f"(single words exact {result['carrying_out']['single']:.0%})")


def g0(quick=False, base_path=None, families=None, log=print):
    cfg = QUICK if quick else FULL
    base_path = base_path or BASE
    if not os.path.exists(base_path):
        teach(quick, base_path, log=log)
    model, ck = load(base_path)
    _, aside = curriculum.pool(side=cfg["side"])
    vocab = Vocab(KNOWN_G0, n_free=cfg["n_free"])
    result = {"cfg": {**cfg, "steps": ck.get("steps", cfg["steps"])},
              "parameters": sum(p.numel() for p in model.parameters()),
              "carrying_out": carrying_out(model, vocab, aside, cfg), "rediscovery": []}
    log(json.dumps(result["carrying_out"], default=str))
    for family in families or HIDDEN_G0:
        result["rediscovery"].append(rediscovery(family, base_path, quick, log=log))
    return result
