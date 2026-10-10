"""Small steps that compose: a typed language for pictures, things, numbers and colours.

The 38 frozen operations are big, finished ideas: a task is solved by one or two of them
or not at all, so Ultron's solutions share almost nothing it could learn from (measured:
2 blocks per half, 0 tasks gained on unseen ones). Here the building blocks are small.
A program is a tree of steps over four kinds of value:

    G  a picture          T  some things in it (a list; one thing is a list of one)
    N  a number           C  a colour
    plus names used as arguments: K (a measure of a thing) and D (a direction)

A step that acts on things acts on each of them ("for each"), and keeping some of them is
a filter ("where"), so a law like "small things turn green" is a short program:

    paint(x, recolour(with(things(x), size, 1), 3))

Programs are found the way Ultron finds any law: smallest first, bottom up, with two
programs that do the same thing to every example kept once (observational equivalence),
within a fixed budget of steps, so a run is the same on any machine. The first program
that turns every training input into its output is a shortest one.

The steps are hand-written, counted (STEPS) and frozen, like the 38 operations; they are
smaller and more generic, so what Ultron builds from them can be its own.
"""

import numpy as np

from .grid import background, key

G, T, N, C, K, D, L = "G", "T", "N", "C", "K", "D", "L"
MAX_SIDE = 30
BUDGET = 40_000         # steps per task when the solver falls back on these


# ------------------------------------------------------------------ things as values
class P:
    """One thing: where its box starts and what it looks like (-1 where it is empty)."""
    __slots__ = ("r0", "c0", "patch", "_k", "_m", "_size", "_colour", "_colours")

    def __init__(self, r0, c0, patch):
        self.r0, self.c0, self.patch = int(r0), int(c0), patch
        self._k = self._m = self._size = self._colour = self._colours = None

    def key(self):
        if self._k is None:
            self._k = (self.r0, self.c0, self.patch.shape, self.patch.tobytes())
        return self._k

    @property
    def mask(self):
        if self._m is None:
            self._m = self.patch >= 0
        return self._m

    def size(self):
        if self._size is None:
            self._size = int(self.mask.sum())
        return self._size

    def colours(self):
        if self._colours is None:
            self._colours = np.unique(self.patch[self.mask])
        return self._colours

    def colour(self):
        if self._colour is None:
            vals, ns = np.unique(self.patch[self.mask], return_counts=True)
            self._colour = int(vals[np.argmax(ns)]) if len(vals) else -1
        return self._colour


_PIECES = {}


def _components(g, diagonal, multicolour, ground=False):
    """Connected pieces of non-background cells, in reading order of their first cell
    (the same pieces, in the same order, as grid.things). Each cell takes the smallest
    label among its connected neighbours until nothing changes."""
    bg = background(g)
    k = (key(g), bg, diagonal, multicolour, ground)
    if k in _PIECES:
        return _PIECES[k]
    if len(_PIECES) > 50000:
        _PIECES.clear()
    h, w = g.shape
    on = (g == bg) if ground else (g != bg)
    if not on.any():
        _PIECES[k] = None
        return None
    big = h * w
    lab = np.where(on, np.arange(big).reshape(h, w), big).astype(np.int64)
    pad = np.full((h + 2, w + 2), big)
    gp = np.full((h + 2, w + 2), -1, dtype=np.int16)
    gp[1:-1, 1:-1] = np.where(on, g, -1)
    shifts = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    if diagonal:
        shifts += [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    joins = []
    for dy, dx in shifts:
        nb = gp[1 + dy:h + 1 + dy, 1 + dx:w + 1 + dx]
        ok = on & (nb >= 0) & (True if multicolour else nb == g)
        joins.append((dy, dx, ok))
    while True:
        pad[1:-1, 1:-1] = lab
        new = lab
        for dy, dx, ok in joins:
            nb = pad[1 + dy:h + 1 + dy, 1 + dx:w + 1 + dx]
            new = np.where(ok & (nb < new), nb, new)
        # pointer jumping: a cell also takes its label's own label (labels are cells of
        # the same piece, so this only ever shortens the way to the piece's first cell)
        flat = np.append(new.ravel(), big)
        while True:
            jumped = flat[flat]
            if (jumped == flat).all():
                break
            flat = jumped
        new = flat[:-1].reshape(h, w)
        if (new == lab).all():
            break
        lab = new
    cells = np.flatnonzero(on.ravel())
    labs = lab.ravel()[cells]
    order = np.argsort(labs, kind="stable")
    cells, labs = cells[order], labs[order]
    starts = np.flatnonzero(np.r_[True, labs[1:] != labs[:-1]])
    rs, cs = cells // w, cells % w
    r0s, r1s = np.minimum.reduceat(rs, starts), np.maximum.reduceat(rs, starts) + 1
    c0s, c1s = np.minimum.reduceat(cs, starts), np.maximum.reduceat(cs, starts) + 1
    out = []
    for v, r0, r1, c0, c1 in zip(labs[starts], r0s, r1s, c0s, c1s):
        m = lab[r0:r1, c0:c1] == v
        out.append(P(r0, c0, np.where(m, g[r0:r1, c0:c1], -1).astype(np.int8)))
    _PIECES[k] = tuple(out) or None
    return _PIECES[k]


def _tkey(ts):
    return tuple(p.key() for p in ts)


# ------------------------------------------------------------------ the steps
def s_things(g):
    return _components(g, False, False)


def s_pieces(g):
    """Things whose cells may have several colours and touch at corners."""
    return _components(g, True, True)


MEASURES = {
    "size": lambda p: p.size(),
    "height": lambda p: p.patch.shape[0],
    "width": lambda p: p.patch.shape[1],
    "top": lambda p: p.r0,
    "left": lambda p: p.c0,
    "colour": lambda p: p.colour(),
    "colours": lambda p: len(p.colours()),
}


def _extreme(ts, k, pick):
    if not ts:
        return None
    vals = [MEASURES[k](p) for p in ts]
    best = pick(vals)
    out = tuple(p for p, v in zip(ts, vals) if v == best)
    return out if len(out) < len(ts) else None


def s_most(ts, k):
    return _extreme(ts, k, max)


def s_least(ts, k):
    return _extreme(ts, k, min)


def s_with(ts, k, n):
    out = tuple(p for p in ts if MEASURES[k](p) == n)
    return out if out and len(out) < len(ts) else None


def s_without(ts, k, n):
    out = tuple(p for p in ts if MEASURES[k](p) != n)
    return out if out and len(out) < len(ts) else None


def s_recolour(ts, c):
    out = []
    for p in ts:
        q = p.patch.copy()
        q[q >= 0] = c
        out.append(P(p.r0, p.c0, q))
    return tuple(out)


STEP = {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)}


def s_shift(ts, d):
    dr, dc = STEP[d]
    return tuple(P(p.r0 + dr, p.c0 + dc, p.patch) for p in ts)


def s_fill_box(ts):
    out = []
    for p in ts:
        q = p.patch.copy()
        q[q < 0] = p.colour()
        out.append(P(p.r0, p.c0, q))
    return tuple(out)


def s_flip_each(ts, d):
    """Each thing mirrored in place (left-right for left/right, top-bottom for up/down)."""
    f = (lambda a: a[:, ::-1]) if d in ("left", "right") else (lambda a: a[::-1])
    return tuple(P(p.r0, p.c0, f(p.patch).copy()) for p in ts)


def _clip(g, p):
    """The part of the picture under a thing, and the part of the thing on the picture."""
    h, w = g.shape
    ph, pw = p.patch.shape
    y0, x0 = max(p.r0, 0), max(p.c0, 0)
    y1, x1 = min(p.r0 + ph, h), min(p.c0 + pw, w)
    if y0 >= y1 or x0 >= x1:
        return None, None
    return (slice(y0, y1), slice(x0, x1)), \
        (slice(y0 - p.r0, y1 - p.r0), slice(x0 - p.c0, x1 - p.c0))


def s_paint(g, ts):
    out = g.copy()
    for p in ts:
        at, part = _clip(g, p)
        if at is not None:
            pm = p.patch[part]
            sub = out[at]
            m = pm >= 0
            sub[m] = pm[m]
    return out


def s_erase(g, ts):
    out = g.copy()
    bg = background(g)
    for p in ts:
        at, part = _clip(g, p)
        if at is not None:
            out[at][p.mask[part]] = bg
    return out


def _box(ts):
    r0 = min(p.r0 for p in ts)
    c0 = min(p.c0 for p in ts)
    r1 = max(p.r0 + p.patch.shape[0] for p in ts)
    c1 = max(p.c0 + p.patch.shape[1] for p in ts)
    return r0, c0, r1, c1


def s_crop(g, ts):
    """The part of the picture in the box around these things."""
    if not ts:
        return None
    r0, c0, r1, c1 = _box(ts)
    r0, c0 = max(r0, 0), max(c0, 0)
    out = g[r0:r1, c0:c1]
    return out if out.size and out.shape != g.shape else None


def s_alone(ts):
    """These things on their own, on the background, cut to their box."""
    if not ts:
        return None
    from .grid import TASK_BACKGROUND
    r0, c0, r1, c1 = _box(ts)
    if r1 - r0 > MAX_SIDE or c1 - c0 > MAX_SIDE:
        return None
    bg = TASK_BACKGROUND[0] if TASK_BACKGROUND[0] is not None else 0
    out = np.full((r1 - r0, c1 - c0), bg, dtype=np.int8)
    for p in ts:
        ph, pw = p.patch.shape
        sub = out[p.r0 - r0:p.r0 - r0 + ph, p.c0 - c0:p.c0 - c0 + pw]
        sub[p.mask] = p.patch[p.mask]
    return out


def s_blank(g):
    return np.full_like(g, background(g))


def s_upscale(g, n):
    if not 2 <= n <= 5 or g.shape[0] * n > MAX_SIDE or g.shape[1] * n > MAX_SIDE:
        return None
    return np.kron(g, np.ones((n, n), dtype=g.dtype))


def s_beside(a, b):
    if a.shape[0] != b.shape[0] or a.shape[1] + b.shape[1] > MAX_SIDE:
        return None
    return np.hstack([a, b])


def s_above(a, b):
    if a.shape[1] != b.shape[1] or a.shape[0] + b.shape[0] > MAX_SIDE:
        return None
    return np.vstack([a, b])


def s_swap(g, a, b):
    """Colour a becomes b."""
    if a == b or not (g == a).any():
        return None
    out = g.copy()
    out[g == a] = b
    return out


def s_count(ts):
    return len(ts)


def s_size(ts):
    return sum(p.size() for p in ts)


def s_colour(ts):
    vals = np.concatenate([p.patch[p.mask] for p in ts]) if ts else np.array([])
    if not len(vals):
        return None
    v, n = np.unique(vals, return_counts=True)
    return int(v[np.argmax(n)])


# --- repetition: a step repeated until something stops it
def s_slide(g, ts, d):
    """Each thing moves toward d, one cell at a time, until the next cell is taken or
    off the picture (the things nearest that side move first)."""
    dr, dc = STEP[d]
    bg = background(g)
    h, w = g.shape
    canvas = s_erase(g, ts)

    def lead(p):
        ph, pw = p.patch.shape
        return (p.r0 + (ph - 1 if dr > 0 else 0)) * dr + (p.c0 + (pw - 1 if dc > 0 else 0)) * dc
    for p in sorted(ts, key=lambda p: -lead(p)):
        rs, cs = np.nonzero(p.mask)
        rs, cs = rs + p.r0, cs + p.c0
        if rs.min() < 0 or cs.min() < 0 or rs.max() >= h or cs.max() >= w:
            return None
        step = 0
        while True:
            ny, nx = rs + (step + 1) * dr, cs + (step + 1) * dc
            if ny.min() < 0 or nx.min() < 0 or ny.max() >= h or nx.max() >= w or \
                    (canvas[ny, nx] != bg).any():
                break
            step += 1
        canvas = s_paint(canvas, (P(p.r0 + step * dr, p.c0 + step * dc, p.patch),))
    return canvas


def s_ray(g, ts, d):
    """From every cell of these things, a line of its colour toward d, until it meets
    something or the edge."""
    dr, dc = STEP[d]
    bg = background(g)
    h, w = g.shape
    out = g.copy()
    for p in ts:
        for r, c in zip(*np.nonzero(p.mask)):
            v = p.patch[r, c]
            y, x = p.r0 + r + dr, p.c0 + c + dc
            while 0 <= y < h and 0 <= x < w and g[y, x] == bg:
                out[y, x] = v
                y, x = y + dr, x + dc
    return out


def s_dots(g):
    """Every coloured cell as a thing of its own."""
    bg = background(g)
    rs, cs = np.nonzero(g != bg)
    return tuple(P(r, c, g[r:r + 1, c:c + 1].copy()) for r, c in zip(rs, cs)) or None


# --- regions and cells of things
def s_holes(g):
    """Pieces of background that don't reach the edge (enclosed), as things."""
    h, w = g.shape
    ps = _components(g, False, False, ground=True) or ()
    out = tuple(p for p in ps if p.r0 > 0 and p.c0 > 0 and p.r0 + p.patch.shape[0] < h
                and p.c0 + p.patch.shape[1] < w)
    return out or None


def s_inside(ts):
    """Each thing's inner cells: those whose four neighbours are the thing too."""
    out = []
    for p in ts:
        m = np.pad(p.mask, 1)
        inner = m[1:-1, 1:-1] & m[:-2, 1:-1] & m[2:, 1:-1] & m[1:-1, :-2] & m[1:-1, 2:]
        if inner.any():
            out.append(P(p.r0, p.c0, np.where(inner, p.patch, -1).astype(np.int8)))
    return tuple(out) or None


def s_ring(ts):
    """The cells just around each thing's box, in the thing's colour."""
    out = []
    for p in ts:
        ph, pw = p.patch.shape
        q = np.full((ph + 2, pw + 2), p.colour(), dtype=np.int8)
        q[1:-1, 1:-1] = -1
        out.append(P(p.r0 - 1, p.c0 - 1, q))
    return tuple(out)


# --- two pictures, cell by cell
def s_overlay(a, b):
    """b's coloured cells fill a's background (same size)."""
    if a.shape != b.shape:
        return None
    bg = background(a)
    out = a.copy()
    m = (a == bg) & (b != background(b))
    out[m] = b[m]
    return out


LOGIC = {"both": lambda x, y: x & y, "either": lambda x, y: x | y,
         "one": lambda x, y: x ^ y, "first": lambda x, y: x & ~y,
         "neither": lambda x, y: ~x & ~y}


def s_logic(a, b, rule, c):
    """Lay two pictures over each other; colour c where the rule holds of their
    coloured cells, background elsewhere."""
    if a.shape != b.shape:
        return None
    m = LOGIC[rule](a != background(a), b != background(b))
    out = np.full_like(a, background(a))
    out[m] = c
    return out


def s_left(g):
    w = g.shape[1]
    return g[:, :w // 2] if w >= 2 else None


def s_right(g):
    w = g.shape[1]
    return g[:, w - w // 2:] if w >= 2 else None


def s_top(g):
    h = g.shape[0]
    return g[:h // 2] if h >= 2 else None


def s_bottom(g):
    h = g.shape[0]
    return g[h - h // 2:] if h >= 2 else None


def s_part(g, n):
    """The n-th part between the picture's separator lines."""
    from .grid import parts
    ps = parts(g)
    return ps[n - 1] if ps is not None and 1 <= n <= len(ps) else None


# (name, argument types, result type, function) -- the counted, frozen steps
STEPS = [
    ("rot90", (G,), G, lambda g: np.rot90(g, -1)),
    ("rot180", (G,), G, lambda g: g[::-1, ::-1]),
    ("flip", (G,), G, lambda g: g[:, ::-1]),
    ("flip_v", (G,), G, lambda g: g[::-1]),
    ("transpose", (G,), G, lambda g: g.T),
    ("things", (G,), T, s_things),
    ("pieces", (G,), T, s_pieces),
    ("most", (T, K), T, s_most),
    ("least", (T, K), T, s_least),
    ("with", (T, K, N), T, s_with),
    ("without", (T, K, N), T, s_without),
    ("recolour", (T, C), T, s_recolour),
    ("shift", (T, D), T, s_shift),
    ("fill_box", (T,), T, s_fill_box),
    ("flip_each", (T, D), T, s_flip_each),
    ("paint", (G, T), G, s_paint),
    ("erase", (G, T), G, s_erase),
    ("crop", (G, T), G, s_crop),
    ("alone", (T,), G, s_alone),
    ("blank", (G,), G, s_blank),
    ("upscale", (G, N), G, s_upscale),
    ("beside", (G, G), G, s_beside),
    ("above", (G, G), G, s_above),
    ("swap", (G, C, C), G, s_swap),
    ("count", (T,), N, s_count),
    ("size", (T,), N, s_size),
    ("colour", (T,), C, s_colour),
    # repetition and cells (lever 1)
    ("slide", (G, T, D), G, s_slide),
    ("ray", (G, T, D), G, s_ray),
    ("holes", (G,), T, s_holes),
    ("dots", (G,), T, s_dots),
    ("inside", (T,), T, s_inside),
    ("ring", (T,), T, s_ring),
    ("overlay", (G, G), G, s_overlay),
    ("logic", (G, G, L, C), G, s_logic),
    ("left", (G,), G, s_left),
    ("right", (G,), G, s_right),
    ("top", (G,), G, s_top),
    ("bottom", (G,), G, s_bottom),
    ("part", (G, N), G, s_part),
]
FUNCS = {name: f for name, _, _, f in STEPS}
# the first 27 steps, without repetition, cell-by-cell steps or per-cell laws: what the
# solver falls back on (measured: the full language finds more on its own, 57 vs 34
# training tasks, but within the same budget as a fallback it loses two and adds wrong
# answers, so the fallback keeps the smaller set)
BASIC = STEPS[:27]


# ------------------------------------------------------------------ running a program
LIBRARY = [None]        # steps Ultron built itself from these (learn_library), when on
FINISH = [True]         # check each new set of things / picture as a finished answer
OWN_LAST = [False]      # try its own steps after the given ones at each size
CELLS_UP_TO = 4         # a local law per cell is tried on pictures made in this many steps


def run(expr, x, holes=()):
    """A program's value on one input picture (None if a step can't apply)."""
    tag = expr[0]
    if tag == "x":
        return x
    if tag == "k":
        return expr[1]
    if tag == "hole":
        return holes[expr[1]]
    args = []
    for a in expr[1:]:
        v = run(a, x, holes)
        if v is None:
            return None
        args.append(v)
    return _apply(tag, args, x)


def _colour_map(grids, targets):
    from .solve import _colour_map
    return _colour_map(grids, targets)


def s_map(g, m):
    """A recolouring learned from the task's own examples."""
    m = dict(m)
    return np.vectorize(lambda v: m.get(int(v), int(v)), otypes=[np.int8])(g)


def _apply(tag, args, x):
    if tag == "map":
        return s_map(*args)
    if tag == "cells":
        from . import cells
        g, (fs, items) = args
        return cells.apply((tuple(fs), {_tup(k): v for k, v in items}), g)
    lib = _lib()
    if tag in lib:
        return run(lib[tag]["pattern"], x, args)
    try:
        return _check(FUNCS[tag](*args))
    except (ValueError, IndexError):
        return None


def _lib():
    return {e["name"]: e for e in (LIBRARY[0] or [])}


def _tup(v):
    return tuple(_tup(x) for x in v) if isinstance(v, (list, tuple)) else v


def _check(v):
    if isinstance(v, np.ndarray):
        if v.size == 0 or v.shape[0] > MAX_SIDE or v.shape[1] > MAX_SIDE:
            return None
    return v


def _vkey(v):
    if isinstance(v, np.ndarray):
        return key(v)
    if isinstance(v, tuple):
        return _tkey(v)
    return v


def size(expr):
    """Description length in steps: one per node; a learned recolouring costs half a step
    per colour it changes."""
    if expr[0] == "k":
        return 1
    if expr[0] == "map":
        return size(expr[1]) + 0.5 * sum(1 for a, b in expr[2][1] if a != b)
    if expr[0] == "cells":
        fs, items = expr[2][1]
        return size(expr[1]) + 1 + 0.5 * len(fs) * sum(1 for k, v in items if k[0] != v)
    return 1 + sum(size(a) for a in expr[1:])


def show(expr):
    tag = expr[0]
    if tag == "x":
        return "x"
    if tag == "k":
        return str(expr[1])
    if tag == "hole":
        return "_" + "abc"[expr[1]]
    if tag == "cells":
        fs, items = expr[2][1]
        changes = sum(1 for k, v in items if k[0] != v)
        return show(expr[1]) + f" ▸ local law on ({', '.join(fs)}): {changes} situations"
    if tag == "map":
        return show(expr[1]) + " ▸ recolour " + ", ".join(
            f"{a}→{b}" for a, b in expr[2][1] if a != b)
    return f"{tag}(" + ", ".join(show(a) for a in expr[1:]) + ")"


def parse(text):
    """A program from how show() writes it."""
    import re
    toks = re.findall(r"[A-Za-z_][A-Za-z_0-9]*|-?\d+|[(),]", text)
    pos = [0]

    def one():
        t = toks[pos[0]]
        pos[0] += 1
        if t == "x":
            return ("x",)
        if re.fullmatch(r"-?\d+", t):
            return ("k", int(t))
        if pos[0] < len(toks) and toks[pos[0]] == "(":
            pos[0] += 1
            args = [one()]
            while toks[pos[0]] == ",":
                pos[0] += 1
                args.append(one())
            pos[0] += 1
            return (t,) + tuple(args)
        return ("k", t)
    return one()


# ------------------------------------------------------------------ the search
class _Budget(Exception):
    pass


def constants(train):
    ins = [i for i, _ in train]
    outs = [o for _, o in train]
    cols = sorted({int(c) for g in ins + outs for c in np.unique(g)})
    return {K: list(MEASURES), D: list(STEP), N: [1, 2, 3], C: cols, L: list(LOGIC)}


def search(train, budget=40_000, max_size=9, want=2, stats=None, steps=None, cells_up_to=None):
    """Programs (smallest first) that turn every training input into its output."""
    cells_up_to = CELLS_UP_TO if cells_up_to is None else cells_up_to
    ins = [i for i, _ in train]
    targets = [o for _, o in train]
    goal = tuple(key(o) for o in targets)
    consts = constants(train)
    # bank[type][size] = [(expr, values)]; seen[type] = value keys already had
    bank = {t: {} for t in (G, T, N, C, K, D, L)}
    seen = {t: set() for t in bank}
    found = []
    spent = [0]

    def add(t, s, expr, vals):
        k = tuple(_vkey(v) for v in vals)
        if k in seen[t]:
            return
        seen[t].add(k)
        bank[t].setdefault(s, []).append((expr, vals))
        if t == G:
            if k == goal:
                found.append(expr)
            elif FINISH[0]:
                m = _colour_map(vals, targets)
                if m is not None:
                    found.append(("map", expr, ("k", tuple(sorted(m.items())))))
                elif s <= cells_up_to and all(v.shape == o.shape for v, o in zip(vals, targets)):
                    # a law for each cell, from what is around it (cells.py)
                    from . import cells
                    spent[0] += len(ins)
                    rule = cells.learn(list(vals), targets)
                    if rule is not None:
                        found.append(("cells", expr, ("k", (rule[0], tuple(sorted(
                            rule[1].items(), key=repr))))))
        elif t == T and FINISH[0]:
            # the ways a set of things can finish a program, checked against the goal
            # (not kept: only a match matters)
            for name, args in (("paint", (("x",), expr)), ("erase", (("x",), expr)),
                               ("crop", (("x",), expr)), ("alone", (expr,))):
                spent[0] += len(ins)
                outs = []
                for i, x in enumerate(ins):
                    a = [x if e == ("x",) else vals[i] for e in args]
                    try:
                        r = _check(FUNCS[name](*a))
                    except (ValueError, IndexError):
                        r = None
                    if r is None:
                        break
                    outs.append(r)
                else:
                    if tuple(key(o) for o in outs) == goal:
                        found.append((name,) + args)

    add(G, 1, ("x",), tuple(ins))
    for t in (K, D, N, C, L):
        for v in consts[t]:
            add(t, 1, ("k", v), tuple(v for _ in ins))
    # its own steps first: a step built from others is tried before the others
    own = [(e["name"], tuple(e["args"]), e["type"], None) for e in (LIBRARY[0] or [])]
    base_steps = STEPS if steps is None else steps
    steps = base_steps + own if OWN_LAST[0] else own + base_steps
    try:
        for s in range(1, max_size + 1):
            for name, argt, outt, f in steps:
                if not argt and s != 1 or argt and s < 2:
                    continue
                for args in _args(bank, argt, s - 1):
                    spent[0] += len(ins)
                    if spent[0] > budget:
                        raise _Budget
                    vals = []
                    for i, x in enumerate(ins):
                        a = [v[i] for _, v in args]
                        if f is None:
                            r = _apply(name, a, x)
                        else:
                            try:
                                r = _check(f(*a))
                            except (ValueError, IndexError):
                                r = None
                        if r is None:
                            break
                        vals.append(r)
                    else:
                        add(outt, s, (name,) + tuple(e for e, _ in args), tuple(vals))
            if s == 1:
                continue
            if stats is not None:
                stats.append((s, spent[0], {t: len(bank[t].get(s, [])) for t in bank}))
            # stop only when nothing longer could be shorter than what's found: a law
            # that spells out a long table is a long description, however soon it appears
            best = sorted(size(e) for e in found)
            if len(best) >= want and best[want - 1] <= s:
                break
    except _Budget:
        pass
    return found, spent[0]


def _args(bank, types, total):
    """Every way to fill these argument types with programs whose sizes add to total."""
    if not types:
        if total == 0:
            yield ()
        return
    first, rest = types[0], types[1:]
    for s in sorted(bank[first]):
        if s > total - len(rest):
            break
        for e in bank[first][s]:
            for tail in _args(bank, rest, total - s):
                yield (e,) + tail


def _answers(train, tests, max_size, **kw):
    found, spent = search(train, max_size=max_size, **kw)
    found = sorted(found, key=lambda e: (size(e), show(e)))
    attempts = [[] for _ in tests]
    used = []
    for expr in found:
        preds = [run(expr, t) for t in tests]
        if any(p is None or not isinstance(p, np.ndarray) for p in preds):
            continue
        new = False
        for a, p in zip(attempts, preds):
            if len(a) < 2 and all(not np.array_equal(p, q) for q in a):
                a.append(p)
                new = True
        if new:
            used.append(expr)
    return attempts, used, spent


def earns(train, max_size=12, **kw):
    """Leave one out: learning from every example but one, does Ultron predict the one
    left out, for each example in turn? A true rule survives this; a program that fits
    every example by coincidence usually doesn't. (The same rule its per-puzzle network
    had to meet.) Returns (passed, steps spent)."""
    from . import grid
    from .solve import task_background
    if len(train) < 2:
        return False, 0
    spent = 0
    saved = grid.TASK_BACKGROUND[0]
    try:
        for k in range(len(train)):
            rest = train[:k] + train[k + 1:]
            grid.TASK_BACKGROUND[0] = task_background(rest)
            attempts, _, sp = _answers(rest, [train[k][0]], max_size, **kw)
            spent += sp
            if not any(np.array_equal(p, train[k][1]) for p in attempts[0]):
                return False, spent
    finally:
        grid.TASK_BACKGROUND[0] = saved
    return True, spent


def predict(train, tests, max_size=12, loo=False, **kw):
    """Up to two different answers for each test input. With loo, only when the task
    earns them (earns): otherwise no answer, never a guess."""
    from . import grid
    from .solve import task_background
    grid.TASK_BACKGROUND[0] = task_background(train)
    attempts, used, spent = _answers(train, tests, max_size, **kw)
    if loo and used:
        ok, extra = earns(train, max_size=max_size, **kw)
        grid.TASK_BACKGROUND[0] = task_background(train)
        spent += extra
        if not ok:
            return [[] for _ in tests], [], spent
    return attempts, used, spent


# ------------------------------------------------------------------ growing its own steps
# Library learning on these trees (the abstraction sleep of brain/abstraction.py, on
# pictures): line up pieces of the programs that explained different tasks, keep what
# they share and leave a typed hole where they differ. A piece becomes a step of its own
# only if writing it once and using it everywhere makes the total description of every
# explained task SHORTER (MDL). A step can be built from steps it built before.
SIGS = {name: (argt, outt) for name, argt, outt, _ in STEPS}
MAX_HOLES = 3
MAX_STEPS = 24


def _sig(name, lib):
    if name in lib:
        return tuple(lib[name]["args"]), lib[name]["type"]
    return SIGS[name]


def _typed_subtrees(expr, want, lib, out):
    """(subtree, its type) for every subtree that is a step (not x, not a constant)."""
    if expr[0] in ("x", "k", "hole"):
        return
    if expr[0] in ("map", "cells"):    # a law learned per task is not a piece to share
        _typed_subtrees(expr[1], G, lib, out)
        return
    argt, outt = _sig(expr[0], lib)
    out.append((expr, outt))
    for a, t in zip(expr[1:], argt):
        _typed_subtrees(a, t, lib, out)


def anti_unify(a, b, t, lib, holes):
    """What a and b (both of type t) share; a typed hole where they differ."""
    if a == b:
        return a
    if a[0] == b[0] and a[0] not in ("x", "k", "hole", "map", "cells") and len(a) == len(b):
        argt, _ = _sig(a[0], lib)
        return (a[0],) + tuple(anti_unify(x, y, tt, lib, holes)
                               for x, y, tt in zip(a[1:], b[1:], argt))
    pair = (a, b)
    if pair not in holes:
        holes[pair] = (len(holes), t)
    return ("hole", holes[pair][0])


def match(pattern, expr, binding):
    """Does expr fit the pattern? (fills binding with what each hole stands for)"""
    if pattern[0] == "hole":
        j = pattern[1]
        if j in binding:
            return binding[j] == expr
        binding[j] = expr
        return True
    if pattern[0] != expr[0] or len(pattern) != len(expr):
        return False
    if pattern[0] == "k":
        return pattern == expr
    return all(match(p, e, binding) for p, e in zip(pattern[1:], expr[1:]))


def _fixed(pattern):
    """Nodes of a pattern that are written out (holes are filled per use)."""
    if pattern[0] == "hole":
        return 0
    if pattern[0] in ("x", "k"):
        return 1
    return 1 + sum(_fixed(a) for a in pattern[1:])


def _rewrite(expr, name, pattern, n_holes):
    b = {}
    if expr[0] not in ("x", "k", "hole") and match(pattern, expr, b):
        return (name,) + tuple(_rewrite(b[j], name, pattern, n_holes) for j in range(n_holes))
    if expr[0] in ("x", "k", "hole"):
        return expr
    return (expr[0],) + tuple(_rewrite(a, name, pattern, n_holes) for a in expr[1:])


def _uses(pattern, programs):
    tasks = set()
    for task, prog in programs.items():
        stack = [prog]
        while stack:
            e = stack.pop()
            if e[0] in ("x", "k", "hole"):
                continue
            if match(pattern, e, {}):
                tasks.add(task)
                break
            stack.extend(e[1:])
    return tasks


def learn_library(programs, library=()):
    """New steps worth having, given {task: program} of explained tasks.
    Returns the library: its earlier steps followed by the new ones, best first."""
    library = list(library)
    programs = dict(programs)
    while len(library) < MAX_STEPS:
        lib = {e["name"]: e for e in library}
        subs = {}
        for task, prog in sorted(programs.items()):
            out = []
            _typed_subtrees(prog, None, lib, out)
            for e, t in out:
                subs.setdefault((e, t), set()).add(task)
        items = sorted(subs.items(), key=lambda kv: repr(kv[0]))
        cands = {}
        for i, ((a, ta), ka) in enumerate(items):
            for (b, tb), kb in items[i:]:
                if ta != tb or a[0] != b[0] or (a == b and len(ka) < 2) or \
                        (a != b and not (ka - kb or kb - ka)):
                    continue
                holes = {}
                p = anti_unify(a, b, ta, lib, holes)
                if len(holes) > MAX_HOLES or _fixed(p) < 2:
                    continue
                cands[p] = (ta, [t for _, (j, t) in sorted(holes.items(),
                                                           key=lambda kv: kv[1][0])])
        best = None
        for p, (t, args) in sorted(cands.items(), key=lambda kv: repr(kv[0])):
            uses = _uses(p, programs)
            n = _fixed(p)
            saving = len(uses) * (n - 1) - n
            if len(uses) >= 2 and saving > 0 and (best is None or saving > best[0]):
                best = (saving, p, t, args, sorted(uses))
        if best is None:
            break
        saving, p, t, args, uses = best
        name = f"own{len(library) + 1}"
        library.append({"name": name, "pattern": p, "args": args, "type": t,
                        "uses": len(uses), "saving": saving, "tasks": uses})
        programs = {k: _rewrite(v, name, p, len(args)) for k, v in programs.items()}
    return library


def inline(expr, library):
    """A program with its own steps spelled out as the small steps they stand for."""
    if expr[0] in ("x", "k", "hole"):
        return expr
    args = tuple(inline(a, library) for a in expr[1:])
    lib = {e["name"]: e for e in library}
    if expr[0] in lib:
        return inline(_fill(lib[expr[0]]["pattern"], args), library)
    return (expr[0],) + args


def _fill(pattern, args):
    if pattern[0] == "hole":
        return args[pattern[1]]
    if pattern[0] in ("x", "k"):
        return pattern
    return (pattern[0],) + tuple(_fill(a, args) for a in pattern[1:])


def describe_step(e):
    return f"{e['name']}({', '.join(e['args'])}) = {show(e['pattern'])}"
