"""How well the interpreter carries out words, measured on pictures kept aside."""

import random


from . import curriculum
from .vocab import changes


def same(a, b):
    return a is not None and b is not None and a.shape == b.shape and bool((a == b).all())


def steps_exact(model, vocab, grids, side, per_word=20, seed=1, words=None, ids=None):
    """For each word, the share of kept-aside pictures (that the word changes) whose
    result comes out exactly right. `ids` lets a free word stand in for a hidden one."""
    rng = random.Random(seed)
    words = vocab.known if words is None else words
    cases = []
    for w in words:
        got = 0
        for _ in range(per_word * 30):
            g = curriculum.state(grids, vocab.known, rng, side)
            out = changes(w, g)
            if out is not None and max(out.shape) <= side:
                cases.append((w, g, out))
                got += 1
                if got == per_word:
                    break
    preds = model.run([g for _, g, _ in cases],
                      [ids[w] if ids else vocab.ids(w) for w, _, _ in cases])
    score = {}
    for (w, _, out), p in zip(cases, preds):
        a, b = score.get(w, (0, 0))
        score[w] = (a + same(p, out), b + 1)
    return score


def chains_exact(model, vocab, grids, side, length=6, n=200, seed=2):
    """The share of programs of `length` hand-written words that the interpreter carries
    out exactly from start to end, each step starting from its own snapped picture."""
    rng = random.Random(seed)
    cases = [c for c in (curriculum.chain(grids, vocab.known, rng, side, length)
                         for _ in range(n)) if c]
    cur = [g for g, _, _ in cases]
    alive = [True] * len(cases)
    for k in range(length):
        idx = [i for i, a in enumerate(alive) if a]
        preds = model.run([cur[i] for i in idx], [vocab.ids(cases[i][1][k]) for i in idx])
        for i, p in zip(idx, preds):
            alive[i] = same(p, cases[i][2][k])
            cur[i] = p
    return sum(alive), len(cases)


def share(score):
    right = sum(a for a, _ in score.values())
    total = sum(b for _, b in score.values())
    return right / max(total, 1)
