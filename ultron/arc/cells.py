"""Local laws: a cell's new colour depends on what it sees around it.

Many pictures change by a local rule ("a background cell between two red cells turns
blue", "cells of small things turn grey"). Ultron finds such a rule the way it finds any
law: it tries the smallest set of things a cell could be looking at (its own colour,
its neighbours, the size of the thing it belongs to, ...), and keeps the first set for
which one table, cell situation → new colour, agrees with every example. A rule that
meets a situation in the test it never saw in the examples gives no answer rather than
a guess.
"""

import itertools

import numpy as np

from .grid import background, things


def _neigh(g, r, c, steps):
    h, w = g.shape
    return tuple(int(g[r + dr, c + dc]) if 0 <= r + dr < h and 0 <= c + dc < w else -1
                 for dr, dc in steps)


N4 = ((-1, 0), (1, 0), (0, -1), (0, 1))
N8 = N4 + ((-1, -1), (-1, 1), (1, -1), (1, 1))


def features(g):
    """For every cell, the situations it could be in: {feature name: grid of values}."""
    h, w = g.shape
    bg = background(g)
    size = np.zeros(g.shape, dtype=int)
    rank = np.zeros(g.shape, dtype=int)
    ts = things(g, bg)
    if ts:
        sizes = sorted({t.size for t in ts})
        for t in ts:
            for r, c in t.cells:
                size[r, c] = t.size
                rank[r, c] = 1 if t.size == sizes[-1] else (-1 if t.size == sizes[0] else 0)
    f = {"colour": [[int(g[r, c]) for c in range(w)] for r in range(h)],
         "n4": [[_neigh(g, r, c, N4) for c in range(w)] for r in range(h)],
         "n8": [[_neigh(g, r, c, N8) for c in range(w)] for r in range(h)],
         "count8": [[sum(v not in (bg, -1) for v in _neigh(g, r, c, N8)) for c in range(w)]
                    for r in range(h)],
         "size": size.tolist(),
         "rank": rank.tolist(),
         "row": [[tuple(sorted(set(g[r].tolist()) - {bg})) for c in range(w)] for r in range(h)],
         "col": [[tuple(sorted(set(g[:, c].tolist()) - {bg})) for c in range(w)]
                 for r in range(h)],
         "parity": [[(r % 2, c % 2) for c in range(w)] for r in range(h)],
         "line": [[(bool(set(g[r, :c].tolist()) - {bg}) and bool(set(g[r, c + 1:].tolist()) - {bg}),
                    bool(set(g[:r, c].tolist()) - {bg}) and bool(set(g[r + 1:, c].tolist()) - {bg}))
                   for c in range(w)] for r in range(h)]}
    return f


# the sets of features tried, smallest description first (always with the cell's colour)
FEATURE_SETS = [("colour",)] + [("colour", x) for x in
                                ("count8", "size", "rank", "parity", "line", "row", "col", "n4")] \
               + [("colour", "n8")] + [("colour",) + p for p in
                                       itertools.combinations(("count8", "rank", "line", "parity"), 2)]


def learn(grids, targets):
    """The smallest feature set whose table agrees with every example, and the table."""
    if any(g.shape != t.shape for g, t in zip(grids, targets)):
        return None
    feats = [features(g) for g in grids]
    for fs in FEATURE_SETS:
        table, ok = {}, True
        for f, t in zip(feats, targets):
            h, w = t.shape
            for r in range(h):
                for c in range(w):
                    k = tuple(f[n][r][c] for n in fs)
                    v = int(t[r, c])
                    if table.setdefault(k, v) != v:
                        ok = False
                        break
                if not ok:
                    break
            if not ok:
                break
        if ok and any(k[0] != v for k, v in table.items()):
            return fs, table
    return None


def apply(rule, g):
    fs, table = rule
    f = features(g)
    h, w = g.shape
    out = np.empty_like(g)
    for r in range(h):
        for c in range(w):
            k = tuple(f[n][r][c] for n in fs)
            if k not in table:
                return None         # a situation never seen in the examples: no guess
            out[r, c] = table[k]
    return out


def describe(rule):
    fs, table = rule
    changes = sum(1 for k, v in table.items() if k[0] != v)
    return f"local law on ({', '.join(fs)}): {changes} situations change colour"
