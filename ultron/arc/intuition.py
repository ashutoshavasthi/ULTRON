"""Intuition for ARC: which half-built programs look promising.

MEASURED (training split, learned on one half, tested on the other; it is not used by
default: solve.INTUITION[0] = None):
  * it ranks the step that leads to an explanation at median position 1 of ~200 (the
    default order: 29); on Ultron's real multi-step solutions, 3.5 (default: 35);
  * search effort to the first explanation falls 3.9x in total (median 5.3x per task;
    46x and 42x on two real tasks) on 76 held-out tasks;
  * but the score does not rise (cross-validated: +1 and -3 tasks): most unsolved tasks
    have no explanation within two or three of the 38 frozen operations at all. What
    limits Ultron on ARC is what it can express, not how it searches.


The search tries programs breadth first within a fixed budget of operations; on most
tasks the budget runs out part-way through two-step programs. Which half-built programs
it expands first then decides what it can find at all.

After a step, Ultron can look at what it has made and compare it with what it wants:
the right shape? how many cells already right? the right colours, the right number of
things? closer than before the step? A small model (numpy logistic regression, fixed
seed) learns from its own experience how such looks predict that a step lies on the way
to an explanation:

  * from its own searches: a step is "on the way" if it begins a program that turned
    out to explain every example;
  * from dreams: chains of its own operations applied to real pictures make tasks
    whose way is known, including the longer ones its search can't yet reach.

The search then expands the most promising half-built programs first. Every answer is
still checked against every example, so intuition can make search find more within its
budget, never make it wrong.
"""

import json
import os
import random

import numpy as np

from .grid import background, colours, things

HERE = os.path.dirname(__file__)
PATH = os.path.join(HERE, "intuition.json")


def _look(grids, targets):
    """How close these pictures are to the targets, as a few numbers."""
    shape = cells = cols = hist = area = ncol = nthings = 0.0
    for g, t in zip(grids, targets):
        same = g.shape == t.shape
        shape += same
        if same:
            cells += float((g == t).mean())
        cg, ct = set(colours(g)), set(colours(t))
        cols += len(cg & ct) / max(1, len(cg | ct))
        hg = np.bincount(g.ravel(), minlength=10) / g.size
        ht = np.bincount(t.ravel(), minlength=10) / t.size
        hist += 1 - np.abs(hg - ht).sum() / 2
        area += min(g.size, t.size) / max(g.size, t.size)
        ncol += len(cg) == len(ct)
        bg = background(g)
        nthings += len(things(g, bg)) == len(things(t, background(t)))
    n = len(targets)
    return np.array([shape, cells, cols, hist, area, ncol, nthings]) / n


N_LOOK = 7


def features(outs, targets, parent_look, depth, name):
    """What a half-built program's result looks like, against the targets and its parent."""
    now = _look(outs, targets)
    changed = 1.0
    return np.concatenate([now, now - parent_look, [depth / 3, changed, 1.0]]), now


class Model:
    def __init__(self, w=None, mu=None, sd=None):
        self.w, self.mu, self.sd = w, mu, sd

    def train(self, X, y, epochs=500, lr=0.5, l2=1e-3):
        X = np.asarray(X, float)
        y = np.asarray(y, float)
        self.mu, self.sd = X.mean(axis=0), X.std(axis=0) + 1e-9
        Xn = (X - self.mu) / self.sd
        Xn[:, -1] = 1.0
        # positives are rare: weigh them up so the model doesn't learn "never"
        wpos = (len(y) - y.sum()) / max(1.0, y.sum())
        sw = np.where(y > 0, wpos, 1.0)
        self.w = np.zeros(X.shape[1])
        for _ in range(epochs):
            p = 1 / (1 + np.exp(-Xn @ self.w))
            self.w -= lr * (Xn.T @ ((p - y) * sw)) / sw.sum() + l2 * self.w
        return self

    def score(self, f):
        x = (f - self.mu) / self.sd
        x[-1] = 1.0
        return float(x @ self.w)

    def to_json(self):
        return {"w": self.w.tolist(), "mu": self.mu.tolist(), "sd": self.sd.tolist()}

    @classmethod
    def from_json(cls, d):
        return cls(np.array(d["w"]), np.array(d["mu"]), np.array(d["sd"]))


def save(model, path=PATH):
    with open(path, "w") as f:
        json.dump(model.to_json(), f)
        f.write("\n")


def load(path=PATH):
    if not os.path.exists(path):
        return None
    with open(path) as f:
        return Model.from_json(json.load(f))


# ------------------------------------------------------------------ experience
def experience_from_search(train, budget=40000):
    """Run its own search once, recording every one-step program; label a step as on the
    way if a program that explains every example begins with it."""
    from . import solve
    solve.RECORD[0] = []
    try:
        found, _ = solve.solve(train, budget=budget)
    finally:
        rec, solve.RECORD[0] = solve.RECORD[0], None
    firsts = {repr(p[0]) for p in found if p and p[0][0] not in solve.LEARNED}
    X, y = [], []
    for prog, f in rec:
        X.append(f)
        y.append(1.0 if repr(prog[0]) in firsts else 0.0)
    return X, y


def dream(train, rng, budget=4000):
    """A made-up task from real pictures: a chain of two of its own operations applied
    to them. Returns (pictures, made-up targets, the chain) or None."""
    from . import ops as O
    from . import solve
    from .grid import key
    ins = [i for i, _ in train]
    reg = O.registry(solve.context(train))
    for _ in range(20):
        chain = [rng.choice(reg), rng.choice(reg)]
        outs = []
        for g in ins:
            for name, f, p in chain:
                try:
                    g = f(g, p) if g is not None else None
                except (ValueError, IndexError):
                    g = None
            if g is None or g.size == 0 or g.shape[0] > 30 or g.shape[1] > 30:
                outs = None
                break
            outs.append(g)
        if outs is None:
            continue
        if len({key(o) for o in outs}) < len(outs) or \
                any(key(o) == key(i) for o, i in zip(outs, ins)):
            continue
        return list(zip(ins, outs)), [(n, p) for n, _, p in chain]
    return None


def learn(tasks, n_dreams=300, seed=0):
    """Learn from its own searches on these tasks and from dreams made of their
    pictures."""
    rng = random.Random(seed)
    X, y = [], []
    ids = sorted(tasks)
    for tid in ids:
        a, b = experience_from_search(tasks[tid]["train"])
        X += a
        y += b
    for k in range(n_dreams):
        d = dream(tasks[ids[k % len(ids)]]["train"], rng)
        if d is None:
            continue
        pairs, chain = d
        from . import solve
        solve.RECORD[0] = []
        try:
            solve.solve(pairs, budget=4000, max_depth=1)
        finally:
            rec, solve.RECORD[0] = solve.RECORD[0], None
        first = repr(chain[0])
        for prog, f in rec:
            X.append(f)
            y.append(1.0 if repr(prog[0]) == first else 0.0)
    return Model().train(X, y)
