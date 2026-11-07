"""Dreams and a learned guide: Ultron practises on puzzles it makes from its own language.

Dreams. A dream is a puzzle whose answer Ultron knows because it made it: it writes a
random program in its own language (the given small steps of compose.py and the words
it grew), weighted toward the steps it uses most, and runs it on real input pictures
from its practice half (never from the held-out half). A dream is kept only when every
picture gives an answer, the answers aren't all the same, and at least one differs from
its input. Each dream is a puzzle plus the program that made it.

The guide. From dreams and from its real solutions, Ultron learns which steps a puzzle
needs from what the puzzle looks like (same size or not, colours added or removed, how
many things, ...): one small logistic model per step, P(step used | puzzle). The search
then tries steps in that order (compose.ORDER), so it reaches the programs a puzzle
probably needs within the same budget. It only changes the order: every answer is still
checked against every example, so the guide can make the search find more, never make
an answer wrong.
"""

import numpy as np

from . import compose, grid

G, T, N, C, K, D, L = compose.G, compose.T, compose.N, compose.C, compose.K, compose.D, \
    compose.L
LEAF = (K, D, N, C, L)


# ------------------------------------------------------------------ making dreams

def _producers(words):
    """{type: [(name, arg types)]} for the given steps and its own words."""
    out = {}
    for name, argt, outt, _ in compose.STEPS:
        out.setdefault(outt, []).append((name, tuple(argt)))
    for w in words or []:
        out.setdefault(w["type"], []).append((w["name"], tuple(w["args"])))
    return out


def _sample(rng, want, depth, producers, consts, weights):
    if want == G and (depth <= 0 or rng.random() < 0.25):
        return ("x",)
    if want in LEAF and (rng.random() < 0.85 or want not in producers or depth <= 0):
        vals = consts[want]
        return ("k", vals[int(rng.integers(len(vals)))]) if vals else None
    options = producers.get(want, [])
    if depth <= 0 or not options:
        return None
    w = np.array([1.0 + weights.get(name, 0) for name, _ in options])
    name, argt = options[int(rng.choice(len(options), p=w / w.sum()))]
    args = []
    for t in argt:
        a = _sample(rng, t, depth - 1, producers, consts, weights)
        if a is None:
            return None
        args.append(a)
    return (name,) + tuple(args)


def make(tasks, practice, words=(), n=2000, seed=0, weights=None, depth=4):
    """n dreams: [{"train": [(input, output)], "test": [(input, output)], "program": expr}].
    Inputs come only from the practice tasks."""
    rng = np.random.default_rng(seed)
    producers = _producers(words)
    weights = weights or {}
    old = compose.LIBRARY[0]
    compose.LIBRARY[0] = list(words) or None
    dreams, seen, tries = [], set(), 0
    try:
        while len(dreams) < n and tries < 40 * n:
            tries += 1
            t = tasks[practice[int(rng.integers(len(practice)))]]
            inputs = [i for i, _ in t["train"]] + [i for i, _ in t["test"]]
            consts = compose.constants(t["train"])
            prog = _sample(rng, G, depth, producers, consts, weights)
            if prog is None or prog == ("x",):
                continue
            outs = []
            for x in inputs:
                try:
                    y = compose.run(prog, x)
                except Exception:
                    y = None
                if not isinstance(y, np.ndarray) or y.ndim != 2:
                    break
                outs.append(y.astype(np.int8))
            else:
                if all(np.array_equal(o, x) for o, x in zip(outs, inputs)):
                    continue
                if all(np.array_equal(outs[0], o) for o in outs[1:]):
                    continue
                k = tuple(compose.key(o) for o in outs)
                if k in seen:
                    continue
                seen.add(k)
                pairs = list(zip(inputs, outs))
                dreams.append({"train": pairs[:-1], "test": pairs[-1:], "program": prog})
    finally:
        compose.LIBRARY[0] = old
    return dreams


# ------------------------------------------------------------------ what a puzzle looks like

def features(train):
    """What a puzzle looks like, from its examples: a fixed list of numbers in [0, 1]."""
    f = []
    ins = [i for i, _ in train]
    outs = [o for _, o in train]
    same = all(i.shape == o.shape for i, o in zip(ins, outs))
    smaller = all(o.size < i.size for i, o in zip(ins, outs))
    larger = all(o.size > i.size for i, o in zip(ins, outs))
    ratio = np.mean([o.size / max(1, i.size) for i, o in zip(ins, outs)])
    f += [same, smaller, larger, min(ratio, 4) / 4, ratio in (4.0, 9.0)]
    ci = [set(np.unique(i).tolist()) for i in ins]
    co = [set(np.unique(o).tolist()) for o in outs]
    f += [all(b - a for a, b in zip(ci, co)), all(a - b for a, b in zip(ci, co)),
          all(a == b for a, b in zip(ci, co)), np.mean([len(b) for b in co]) / 10]
    if same:
        changed = np.mean([(i != o).mean() for i, o in zip(ins, outs)])
        bg = [grid.background(i) for i in ins]
        only_bg = all(((i != o) <= (i == b)).all() for i, o, b in zip(ins, outs, bg))
        f += [changed, changed < 0.1, only_bg]
    else:
        f += [0.0, 0.0, 0.0]
    for g in (outs[0], ins[0]):
        f += [np.array_equal(g, g[:, ::-1]), np.array_equal(g, g[::-1]),
              g.shape[0] == g.shape[1] and np.array_equal(g, g.T)]
    nin = np.mean([len(grid.things(i)) for i in ins])
    nout = np.mean([len(grid.things(o)) for o in outs])
    f += [min(nin, 20) / 20, min(nout, 20) / 20, nout < nin, nout > nin, nout == 1]
    f += [any(np.array_equal(o, np.rot90(i, k)) for k in (1, 2, 3)) for i, o in
          zip(ins[:1], outs[:1])]
    f += [1.0]                                                    # bias
    return np.array([float(v) for v in f])


def _names(expr, out):
    if isinstance(expr, tuple) and expr and isinstance(expr[0], str) and \
            expr[0] not in ("x", "k", "hole"):
        out.add(expr[0])
        for a in expr[1:]:
            _names(a, out)
    return out


# ------------------------------------------------------------------ the guide

class Guide:
    """P(step used | what the puzzle looks like), one logistic model per step."""

    def __init__(self, names, weights):
        self.names = list(names)
        self.w = np.asarray(weights, dtype=float)       # (steps, features)

    @classmethod
    def fit(cls, examples, names, epochs=300, lr=0.5, l2=1e-3):
        """examples: [(train pairs, program)]."""
        X = np.stack([features(tr) for tr, _ in examples])
        Y = np.zeros((len(examples), len(names)))
        index = {n: j for j, n in enumerate(names)}
        for k, (_, prog) in enumerate(examples):
            for n in _names(prog, set()):
                if n in index:
                    Y[k, index[n]] = 1.0
        W = np.zeros((len(names), X.shape[1]))
        for _ in range(epochs):
            P = 1 / (1 + np.exp(-(X @ W.T)))
            W -= lr * ((P - Y).T @ X / len(X) + l2 * W)
        return cls(names, W)

    def order(self, train):
        """{step: probability} for this puzzle (the search tries the most likely first)."""
        p = 1 / (1 + np.exp(-(self.w @ features(train))))
        return {n: float(v) for n, v in zip(self.names, p)}

    __call__ = order

    def to_json(self):
        return {"names": self.names, "weights": self.w.round(6).tolist()}

    @classmethod
    def from_json(cls, d):
        return cls(d["names"], d["weights"]) if d else None
