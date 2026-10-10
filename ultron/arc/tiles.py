"""Arrangement laws: the answer is copies of the picture laid out in a grid.

Each place in the grid holds the picture turned or mirrored in its own way, or nothing.
Which way, for each place, is learned from the examples (they must all agree). Or a copy
appears exactly where the picture's own cell has a certain colour (the picture drawn
with itself). The shortest law that explains every example wins.
"""

import numpy as np

from .grid import background

TURNS = [("as it is", lambda g: g), ("mirrored left-right", lambda g: g[:, ::-1]),
         ("mirrored top-bottom", lambda g: g[::-1]), ("half turn", lambda g: g[::-1, ::-1]),
         ("quarter turn", lambda g: np.rot90(g, 1)), ("three quarter turn", lambda g: np.rot90(g, 3)),
         ("transposed", lambda g: g.T), ("anti-transposed", lambda g: np.rot90(g, 2).T)]
BLANK = "blank"


def _ratio(grids, targets):
    rs = set()
    for g, t in zip(grids, targets):
        if t.shape[0] % g.shape[0] or t.shape[1] % g.shape[1]:
            return None
        rs.add((t.shape[0] // g.shape[0], t.shape[1] // g.shape[1]))
    return rs.pop() if len(rs) == 1 and rs != {(1, 1)} else None


def _layout(grids, targets, a, b):
    """For each place, the first turn (or blank) every example agrees on."""
    layout = []
    for p in range(a):
        row = []
        for q in range(b):
            choice = None
            for name, f in [(BLANK, None)] + TURNS:
                ok = True
                for g, t in zip(grids, targets):
                    h, w = g.shape
                    blk = t[p * h:(p + 1) * h, q * w:(q + 1) * w]
                    want = np.full_like(g, background(g)) if f is None else f(g)
                    if want.shape != blk.shape or not np.array_equal(want, blk):
                        ok = False
                        break
                if ok:
                    choice = name
                    break
            if choice is None:
                return None
            row.append(choice)
        layout.append(row)
    if all(c == BLANK for r in layout for c in r):
        return None
    return layout


def _by_cells(grids, targets, a, b):
    """A copy where the picture's cell has the chosen colour (named, or the commonest
    colour that isn't background), blank elsewhere."""
    if any(g.shape != (a, b) for g in grids):
        return None
    for which in ("commonest", "not background") + tuple(range(10)):
        ok = True
        for g, t in zip(grids, targets):
            out = _draw_by_cells(g, which)
            if out is None or not np.array_equal(out, t):
                ok = False
                break
        if ok:
            return which
    return None


def _draw_by_cells(g, which):
    bg = background(g)
    h, w = g.shape
    if which == "commonest":
        vals, ns = np.unique(g[g != bg], return_counts=True)
        if len(vals) == 0 or (ns == ns.max()).sum() > 1:
            return None
        colour = int(vals[np.argmax(ns)])
        on = g == colour
    elif which == "not background":
        on = g != bg
    else:
        on = g == which
    out = np.full((h * h, w * w), bg, dtype=g.dtype)
    for r in range(h):
        for c in range(w):
            if on[r, c]:
                out[r * h:(r + 1) * h, c * w:(c + 1) * w] = g
    return out


def learn(grids, targets):
    ab = _ratio(grids, targets)
    if ab is None:
        return None
    a, b = ab
    layout = _layout(grids, targets, a, b)
    if layout is not None:
        return ("layout", layout)
    which = _by_cells(grids, targets, a, b)
    if which is not None:
        return ("by cells", which)
    return None


def apply(rule, g):
    if rule[0] == "by cells":
        return _draw_by_cells(g, rule[1])
    layout = rule[1]
    h, w = g.shape
    turns = dict(TURNS)
    out = np.full((h * len(layout), w * len(layout[0])), background(g), dtype=g.dtype)
    for p, row in enumerate(layout):
        for q, name in enumerate(row):
            if name != BLANK:
                blk = turns[name](g)
                if blk.shape != (h, w):
                    return None
                out[p * h:(p + 1) * h, q * w:(q + 1) * w] = blk
    return out


def length(rule):
    if rule[0] == "by cells":
        return 2
    return 1 + 0.25 * sum(1 for r in rule[1] for c in r if c != "as it is")


def describe(rule):
    if rule[0] == "by cells":
        return f"the picture drawn with itself: a copy where its cell is {rule[1]}"
    layout = rule[1]
    return f"copies in a {len(layout)}x{len(layout[0])} grid: " + \
        " | ".join(", ".join(r) for r in layout)
