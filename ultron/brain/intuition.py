"""Intuition: which building blocks a law will need, guessed from the examples alone.

Ultron's program search is exhaustive: every law in its library is tried in every
place. Intuition makes a guess first. Looking only at the examples (how fast the
outcome grows with each input, whether it ever falls, its parity...), a small network
predicts which of its laws the explanation will use. The search then tries those
first; if they aren't enough, it searches everything as before. So intuition can make
a search faster, never wrong: every law is still checked against every example.

Where the network learns from: **dreams**. Ultron makes up programs from its own
library, runs them on made-up numbers, and remembers which laws each one used. No
outside data, no teacher. It is numpy, single-threaded, with a fixed seed, so it
learns the same way every time.
"""

import random

import numpy as np

from . import dsl
from .dsl import INT

N_FEATURES = 16


def features(inputs, outputs, names):
    """What the examples look like, as numbers (no law is assumed)."""
    a = np.array([[float(x[n]) for n in names] for x in inputs])
    y = np.array([float(v) for v in outputs])
    f = []
    ly = np.log1p(np.abs(y))
    for j in range(min(2, a.shape[1])):
        la = np.log1p(np.abs(a[:, j]))
        if la.std() > 1e-9:
            slope = np.cov(la, ly, bias=True)[0, 1] / la.var()
            corr = np.corrcoef(la, ly)[0, 1] if ly.std() > 1e-9 else 0.0
        else:
            slope = corr = 0.0
        f += [slope, corr]
    while len(f) < 4:
        f.append(0.0)
    s = a.sum(axis=1)
    p = a.prod(axis=1) if a.shape[1] else np.zeros(len(y))
    f += [
        float(np.mean(y >= s)),             # never less than the inputs together
        float(np.mean(y >= p)),             # never less than their product
        float(np.mean(y == s)),
        float(np.mean(y == p)),
        float(np.mean(y % 2 == 0)),
        float(np.mean(y < np.max(a, axis=1))) if a.shape[1] else 0.0,
        float(np.log1p(np.max(np.abs(y))) / 10),
        float(np.mean(y == 0)),
        float(np.mean(np.abs(y - s) <= 2)),     # a sum, give or take a step
        float(np.mean(np.abs(y - p) <= 2 * s + 2)),
        float(len(set(y.tolist())) / max(1, len(y))),
        1.0,
    ]
    out = np.array(f[:N_FEATURES], dtype=float)
    return np.nan_to_num(out)


def laws_in(expr):
    """The library laws a program uses."""
    found = set()

    def walk(e):
        if not isinstance(e, tuple) or not e:
            return
        if e[0] in ("call", "call1"):
            found.add(e[1])
        if e[0] == "iter" and e[1][0] in ("call", "call1"):
            found.add(e[1][1])
        for x in e[1:]:
            if isinstance(x, tuple):
                walk(x)
    walk(expr)
    return found


def dream(library, rng, max_laws=3):
    """A made-up program from its own laws and steps, and the made-up examples it makes."""
    binary, unary = library.search_laws()
    leaves = [("var", "a"), ("var", "b"), ("const", 1)]

    def grow(depth):
        r = rng.random()
        if depth <= 0 or r < 0.3:
            return rng.choice(leaves)
        if r < 0.45:
            return (rng.choice(["succ", "pred"]), grow(depth - 1))
        if r < 0.55 and unary:
            return ("call1", rng.choice(unary).name, grow(depth - 1))
        law = rng.choice(binary)
        return ("call", law.name, grow(depth - 1), grow(depth - 1))
    for _ in range(50):
        expr = grow(rng.randint(1, 3))
        used = laws_in(expr)
        if not used or len(used) > max_laws or dsl.size(expr) > 7:
            continue
        xs = [{"a": rng.randint(0, 9), "b": rng.randint(0, 9)} for _ in range(20)]
        ys = []
        with dsl.limits(20000, 10 ** 7):
            try:
                for x in xs:
                    ys.append(dsl.evaluate(expr, x, library))
            except (dsl.Overflow, KeyError):
                continue
        if len(set(ys)) < 3:
            continue        # a dream that says nothing
        return expr, xs, ys
    return None


def hunches(inputs, outputs, names, library, laws):
    """For each law: how closely the outcome follows that law tried on the inputs (either
    way round, or on one input twice). A quick look, not a search."""
    y = np.log1p(np.abs(np.array([float(v) for v in outputs])))
    out = []
    names = list(names)
    pairs = [(names[0], names[1]), (names[1], names[0]), (names[0], names[0]),
             (names[1], names[1])] if len(names) > 1 else [(names[0], names[0])]
    for law in laws:
        best = 0.0
        combos = pairs if len(law.params) == 2 else [(n,) for n in names]
        for args in combos:
            vals = []
            with dsl.limits(20000, 10 ** 7):
                try:
                    for x in inputs:
                        v = (library.call(law.name, x[args[0]], x[args[1]]) if len(args) == 2
                             else library.call1(law.name, x[args[0]]))
                        vals.append(float(v))
                except (dsl.Overflow, KeyError, TypeError, RecursionError):
                    continue
            lv = np.log1p(np.abs(np.array(vals)))
            if lv.std() > 1e-9 and y.std() > 1e-9:
                best = max(best, float(np.corrcoef(lv, y)[0, 1]))
        out.append(best)
    return np.array(out)


class Intuition:
    """One small logistic model per law: does a task that looks like this need it? It
    sees the examples' shape and its quick hunches about every law."""

    def __init__(self, names):
        self.names = list(names)
        self.w = np.zeros((len(self.names), N_FEATURES))
        self.mu = np.zeros(N_FEATURES)
        self.sd = np.ones(N_FEATURES)

    def train(self, tasks, epochs=400, lr=0.5):
        """tasks: [(features, set of laws used)]"""
        X = np.array([f for f, _ in tasks])
        self.w = np.zeros((len(self.names), X.shape[1]))
        Y = np.array([[1.0 if n in used else 0.0 for n in self.names] for _, used in tasks])
        self.mu, self.sd = X.mean(axis=0), X.std(axis=0) + 1e-9
        Xn = (X - self.mu) / self.sd
        Xn[:, N_FEATURES - 1] = 1.0
        for _ in range(epochs):
            p = 1 / (1 + np.exp(-Xn @ self.w.T))
            self.w -= lr * ((p - Y).T @ Xn) / len(X) + 1e-3 * self.w
        return self

    def guess(self, f):
        x = (f - self.mu) / self.sd
        x[N_FEATURES - 1] = 1.0
        p = 1 / (1 + np.exp(-self.w @ x))
        return dict(zip(self.names, p.tolist()))


def learn(library, n_dreams=600, seed=0):
    """Dream, then learn from the dreams."""
    rng = random.Random(seed)
    binary, unary = library.search_laws()
    names = sorted(l.name for l in binary + unary)
    tasks = []
    while len(tasks) < n_dreams:
        d = dream(library, rng)
        if d is None:
            continue
        expr, xs, ys = d
        tasks.append((look(xs, ys, ["a", "b"], library, names), laws_in(expr)))
    model = Intuition(names).train(tasks)
    model.library_size = len(library.laws)
    return model


def look(inputs, outputs, names, library, law_names):
    laws = [library.get(n) for n in law_names]
    return np.concatenate([features(inputs, outputs, names),
                           hunches(inputs, outputs, names, library, laws)])


def first_guess(intuition, inputs, outputs, names, k=3, library=None):
    """The k laws it would try first."""
    p = intuition.guess(look(inputs, outputs, names, library, intuition.names))
    return sorted(p, key=lambda n: (-p[n], n))[:k]


MAX_EXTRA = 3       # an unexpected law costs at most this much more to name


def costs(model, inputs, outputs, names, library):
    """What naming each law costs for this task, in whole units: description length in
    bits given what intuition expects. The law it expects most costs 1 (as before); a law
    it thinks 2^k times less likely costs 1 + k (at most 1 + MAX_EXTRA, so nothing is
    ever out of reach)."""
    import math as _m
    if model is None:
        return None
    p = model.guess(look(inputs, outputs, names, library, model.names))
    total = sum(p.values()) or 1.0
    q = {n: max(v / total, 1e-9) for n, v in p.items()}
    best = max(q.values())
    return {n: 1 + min(MAX_EXTRA, int(_m.floor(_m.log2(best / v)))) for n, v in q.items()}
