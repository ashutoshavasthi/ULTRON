"""Operations on grids. Each is generic (it means the same thing in every task) and is
listed, with why it is generic, in PRIMITIVES.md. An operation takes a grid and one
parameter, and gives a grid, or None when it doesn't apply.

Parameters come from the task itself (the colours that appear in its outputs, the size
ratios between its inputs and outputs), never from a list of known answers.
"""

import numpy as np

from .grid import background, bbox, parts, things

BG = None   # the background is worked out per grid unless an op says otherwise


# --------------------------------------------------------------- geometry
def rot90(g, p=None):
    return np.rot90(g, 1)


def rot180(g, p=None):
    return np.rot90(g, 2)


def rot270(g, p=None):
    return np.rot90(g, 3)


def flip_v(g, p=None):
    return g[::-1]


def flip_h(g, p=None):
    return g[:, ::-1]


def transpose(g, p=None):
    return g.T


def antitranspose(g, p=None):
    return np.rot90(g, 2).T


# --------------------------------------------------------------- cropping
def crop_content(g, p=None):
    """The smallest box holding everything that isn't background."""
    bx = bbox(g != background(g))
    if bx is None:
        return None
    r0, r1, c0, c1 = bx
    out = g[r0:r1, c0:c1]
    return None if out.shape == g.shape else out


SELECT = ("largest", "smallest", "rarest_colour", "commonest_colour", "top", "bottom",
          "left", "right", "most_colours", "biggest_box")


def _select(ts, how):
    if not ts:
        return None
    if how == "largest":
        best = max(ts, key=lambda t: t.size)
        return best if sum(t.size == best.size for t in ts) == 1 else None
    if how == "smallest":
        best = min(ts, key=lambda t: t.size)
        return best if sum(t.size == best.size for t in ts) == 1 else None
    if how == "biggest_box":
        best = max(ts, key=lambda t: t.box_area)
        return best if sum(t.box_area == best.box_area for t in ts) == 1 else None
    if how in ("rarest_colour", "commonest_colour"):
        counts = {}
        for t in ts:
            counts[t.colour] = counts.get(t.colour, 0) + 1
        target = (min if how == "rarest_colour" else max)(counts.values())
        pick = [t for t in ts if counts[t.colour] == target]
        return pick[0] if len(pick) == 1 else None
    if how == "most_colours":
        best = max(ts, key=lambda t: t.n_colours)
        return best if sum(t.n_colours == best.n_colours for t in ts) == 1 else None
    pos = {"top": lambda t: t.r0, "bottom": lambda t: -t.r1, "left": lambda t: t.c0,
           "right": lambda t: -t.c1}[how]
    best = min(ts, key=pos)
    return best if sum(pos(t) == pos(best) for t in ts) == 1 else None


def crop_thing(g, p):
    """Cut out one thing, chosen by how it stands out (p = (how, multicolour))."""
    how, multi = p
    t = _select(things(g, multicolour=multi, diagonal=multi), how)
    return None if t is None else t.patch


def keep_thing(g, p):
    """Keep only one thing (chosen as in crop_thing); everything else becomes background."""
    how, multi = p
    bg = background(g)
    t = _select(things(g, bg, multicolour=multi, diagonal=multi), how)
    if t is None:
        return None
    out = np.full_like(g, bg)
    for r, c in t.cells:
        out[r, c] = g[r, c]
    return out


def remove_specks(g, p):
    """Things of at most p cells are noise: remove them."""
    bg = background(g)
    out = g.copy()
    changed = False
    for t in things(g, bg, diagonal=True, multicolour=True):
        if t.size <= p:
            for r, c in t.cells:
                out[r, c] = bg
            changed = True
    return out if changed else None


# --------------------------------------------------------------- size
def upscale(g, k):
    return np.kron(g, np.ones((k, k), dtype=g.dtype))


def downscale(g, k):
    h, w = g.shape
    if h % k or w % k:
        return None
    blocks = g.reshape(h // k, k, w // k, k)
    first = blocks[:, :1, :, :1]
    if not (blocks == first).all():
        return None
    return blocks[:, 0, :, 0]


def tile(g, p):
    a, b = p
    return np.tile(g, (a, b))


def mirror_tile(g, p):
    """The grid and its mirror images side by side (p: 'h', 'v' or 'both')."""
    if p == "h":
        return np.hstack([g, g[:, ::-1]])
    if p == "v":
        return np.vstack([g, g[::-1]])
    top = np.hstack([g, g[:, ::-1]])
    return np.vstack([top, top[::-1]])


# --------------------------------------------------------------- colour
def recolour_all(g, c):
    """Every non-background cell becomes colour c."""
    bg = background(g)
    out = g.copy()
    out[g != bg] = c
    return None if (out == g).all() else out


def keep_colour(g, c):
    bg = background(g)
    if c == bg or not (g == c).any():
        return None
    out = np.full_like(g, bg)
    out[g == c] = c
    return out


def remove_colour(g, c):
    bg = background(g)
    if c == bg or not (g == c).any():
        return None
    out = g.copy()
    out[g == c] = bg
    return out


# --------------------------------------------------------------- filling and drawing
def fill_enclosed(g, c):
    """Background cells that can't reach the edge without crossing something are
    enclosed: paint them c."""
    bg = background(g)
    h, w = g.shape
    outside = np.zeros(g.shape, dtype=bool)
    stack = [(r, c0) for r in range(h) for c0 in (0, w - 1) if g[r, c0] == bg]
    stack += [(r0, x) for x in range(w) for r0 in (0, h - 1) if g[r0, x] == bg]
    while stack:
        y, x = stack.pop()
        if outside[y, x]:
            continue
        outside[y, x] = True
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ny, nx = y + dy, x + dx
            if 0 <= ny < h and 0 <= nx < w and not outside[ny, nx] and g[ny, nx] == bg:
                stack.append((ny, nx))
    inside = (g == bg) & ~outside
    if not inside.any():
        return None
    out = g.copy()
    out[inside] = c
    return out


def gravity(g, d):
    """Everything falls toward one side (d: 'down', 'up', 'left', 'right')."""
    bg = background(g)
    k = {"down": 0, "right": 1, "up": 2, "left": 3}[d]
    a = np.rot90(g, k)          # make the chosen side "down"
    out = np.full_like(a, bg)
    for col in range(a.shape[1]):
        cells = [v for v in a[:, col] if v != bg]
        if cells:
            out[-len(cells):, col] = cells
    out = np.rot90(out, -k)
    return None if (out == g).all() else out


def outline(g, c):
    """Draw a border of colour c around the grid's edge."""
    out = g.copy()
    out[0, :] = out[-1, :] = c
    out[:, 0] = out[:, -1] = c
    return None if (out == g).all() else out


def symmetrize(g, p):
    """Complete a picture that should be symmetric: where a cell is background but its
    mirror image isn't, copy the mirror (p: 'h', 'v', 'both', 'rot')."""
    bg = background(g)
    out = g.copy()
    views = {"h": [lambda a: a[:, ::-1]], "v": [lambda a: a[::-1]],
             "both": [lambda a: a[:, ::-1], lambda a: a[::-1], lambda a: a[::-1, ::-1]],
             "rot": [lambda a: np.rot90(a, 2)]}[p]
    for f in views:
        m = f(out)
        if m.shape != out.shape:
            return None
        hole = (out == bg) & (m != bg)
        out[hole] = m[hole]
    return None if (out == g).all() else out


def complete_pattern(g, hole):
    """A picture made of a repeating tile, with some cells covered (colour `hole`): find
    the smallest repeat that agrees everywhere it can be seen, and fill the holes."""
    h, w = g.shape
    known = g != hole
    if known.all() or not known.any():
        return None
    for py in range(1, h + 1):
        for px in range(1, w + 1):
            if py * px >= h * w / 2 + 1:
                continue
            tile = -np.ones((py, px), dtype=int)
            ok = True
            for r in range(h):
                for c in range(w):
                    if known[r, c]:
                        t = tile[r % py, c % px]
                        if t == -1:
                            tile[r % py, c % px] = g[r, c]
                        elif t != g[r, c]:
                            ok = False
                            break
                if not ok:
                    break
            if ok and (tile >= 0).all():
                out = g.copy()
                for r in range(h):
                    for c in range(w):
                        if not known[r, c]:
                            out[r, c] = tile[r % py, c % px]
                return out
    return None


def extend_rays(g, p):
    """Every cell of colour c sends a ray in direction d until it meets something or the
    edge (p = (c, d); d is one of up, down, left, right, all)."""
    c, d = p
    bg = background(g)
    if c == bg or not (g == c).any():
        return None
    dirs = {"up": [(-1, 0)], "down": [(1, 0)], "left": [(0, -1)], "right": [(0, 1)],
            "all": [(-1, 0), (1, 0), (0, -1), (0, 1)]}[d]
    out = g.copy()
    h, w = g.shape
    for r, x in zip(*np.nonzero(g == c)):
        for dr, dc in dirs:
            y, z = r + dr, x + dc
            while 0 <= y < h and 0 <= z < w and g[y, z] == bg:
                out[y, z] = c
                y, z = y + dr, z + dc
    return None if (out == g).all() else out


def fractal(g, p=None):
    """A picture made of copies of itself: each coloured cell becomes a copy of the whole,
    each background cell an empty block."""
    h, w = g.shape
    if h * h > 30 or w * w > 30:
        return None
    bg = background(g)
    mask = (g != bg).astype(g.dtype)
    out = np.kron(mask, g)
    out[np.kron(mask, np.ones_like(g)) == 0] = bg
    return out


def connect(g, p):
    """Join cells of the same colour that lie on one straight line (p: 'rows', 'cols',
    'diagonals', 'all') by painting the cells between them."""
    bg = background(g)
    out = g.copy()
    h, w = g.shape
    dirs = {"rows": [(0, 1)], "cols": [(1, 0)], "diagonals": [(1, 1), (1, -1)],
            "all": [(0, 1), (1, 0), (1, 1), (1, -1)]}[p]
    for c in set(np.unique(g).tolist()) - {bg}:
        cells = list(zip(*np.nonzero(g == c)))
        cellset = set(cells)
        for r, x in cells:
            for dr, dc in dirs:
                y, z = r + dr, x + dc
                path = []
                while 0 <= y < h and 0 <= z < w and (y, z) not in cellset:
                    path.append((y, z))
                    y, z = y + dr, z + dc
                if 0 <= y < h and 0 <= z < w and path:
                    for a, b in path:
                        if out[a, b] == bg:
                            out[a, b] = c
    return None if (out == g).all() else out


def lines_through(g, p):
    """Every cell of colour c draws a full line through the picture (p = (c, axis);
    axis: 'h', 'v' or 'both')."""
    c, axis = p
    bg = background(g)
    if c == bg or not (g == c).any():
        return None
    out = g.copy()
    for r, x in zip(*np.nonzero(g == c)):
        if axis in ("h", "both"):
            row = out[r]
            row[row == bg] = c
        if axis in ("v", "both"):
            col = out[:, x]
            col[col == bg] = c
    return None if (out == g).all() else out


def complete_diagonal(g, hole):
    """Stripes along diagonals: a colour for each value of (row + col) or (row - col)
    modulo some k, seen where not covered; fill the covered cells."""
    h, w = g.shape
    known = g != hole
    if known.all() or not known.any():
        return None
    for sign in (1, -1):
        for k in range(2, max(h, w) + 1):
            tab, ok = {}, True
            for r, c in zip(*np.nonzero(known)):
                key_ = (r + sign * c) % k
                if tab.setdefault(key_, g[r, c]) != g[r, c]:
                    ok = False
                    break
            if ok and len(tab) == k:
                out = g.copy()
                for r, c in zip(*np.nonzero(~known)):
                    out[r, c] = tab[(r + sign * c) % k]
                return out
    return None


def continue_pattern(g, p):
    """Continue a picture that repeats (rows, or columns) to a new size (p = (H, W)
    ratio as a fraction (a, b) of the old height and width)."""
    (ha, hb), (wa, wb) = p
    h, w = g.shape
    if (h * ha) % hb or (w * wa) % wb:
        return None
    H, W = h * ha // hb, w * wa // wb
    def period(n, same):
        for q in range(1, n + 1):
            if all(same(i, i % q) for i in range(n)):
                return q
        return n
    pr = period(h, lambda i, j: (g[i] == g[j]).all())
    pc = period(w, lambda i, j: (g[:, i] == g[:, j]).all())
    out = np.empty((H, W), dtype=g.dtype)
    for r in range(H):
        for c in range(W):
            out[r, c] = g[r % pr, c % pc]
    return None if out.shape == g.shape else out


def count_parts(g, p=None):
    """A grid with one cell per panel (panels laid out as in the picture), each the
    panel's background."""
    from .grid import separator_lines, _spans
    rows, cols = separator_lines(g)
    if not rows and not cols:
        return None
    h, w = g.shape
    nr, nc = len(_spans(rows, h)), len(_spans(cols, w))
    ps = parts(g)
    if ps is None:
        return None
    return np.full((nr, nc), background(ps[0]), dtype=g.dtype)


def count_things(g, c):
    """A row with one cell of colour c for each thing of colour c."""
    n = sum(1 for t in things(g) if t.colour == c)
    if n == 0 or n > 30:
        return None
    return np.full((1, n), c, dtype=g.dtype)


# --------------------------------------------------------------- each thing
def each_thing(g, p):
    """Every thing is turned in place (p = (how, multicolour); how: flip_h, flip_v,
    rot180, transpose) inside its own box."""
    how, multi = p
    bg = background(g)
    out = np.full_like(g, bg)
    ts = things(g, bg, multicolour=multi, diagonal=multi)
    if not ts:
        return None
    covered = np.zeros(g.shape, dtype=bool)
    for t in ts:
        patch = {"flip_h": t.patch[:, ::-1], "flip_v": t.patch[::-1],
                 "rot180": t.patch[::-1, ::-1], "transpose": t.patch.T}[how]
        if patch.shape != t.patch.shape:
            return None
        region = out[t.r0:t.r1, t.c0:t.c1]
        m = patch != bg
        region[m] = patch[m]
        covered[t.r0:t.r1, t.c0:t.c1] |= m
    return None if (out == g).all() else out


def slide_things(g, d):
    """Every thing slides (keeping its shape) toward one side until it meets the edge or
    another thing (d: 'down', 'up', 'left', 'right')."""
    bg = background(g)
    k = {"down": 0, "right": 1, "up": 2, "left": 3}[d]
    a = np.rot90(g, k).copy()
    ts = sorted(things(a, bg, diagonal=True, multicolour=True), key=lambda t: -t.r1)
    out = np.full_like(a, bg)
    h = a.shape[0]
    for t in ts:
        cells = [(r, c, a[r, c]) for r, c in t.cells]
        step = 0
        while all(r + step + 1 < h and out[r + step + 1, c] == bg for r, c, _ in cells):
            step += 1
        for r, c, v in cells:
            out[r + step, c] = v
    out = np.rot90(out, -k)
    return None if (out == g).all() else out


def frame_things(g, c):
    """Draw a frame of colour c around every thing (just outside its box)."""
    bg = background(g)
    out = g.copy()
    h, w = g.shape
    ts = things(g, bg, diagonal=True, multicolour=True)
    if not ts:
        return None
    for t in ts:
        for r in range(t.r0 - 1, t.r1 + 1):
            for x in range(t.c0 - 1, t.c1 + 1):
                if 0 <= r < h and 0 <= x < w and out[r, x] == bg and not (
                        t.r0 <= r < t.r1 and t.c0 <= x < t.c1):
                    out[r, x] = c
    return None if (out == g).all() else out


def hollow_things(g, p=None):
    """Keep only each thing's outline: cells with all four neighbours in the same thing
    become background."""
    bg = background(g)
    out = g.copy()
    h, w = g.shape
    for r in range(1, h - 1):
        for x in range(1, w - 1):
            v = g[r, x]
            if v != bg and g[r - 1, x] == v and g[r + 1, x] == v and g[r, x - 1] == v \
                    and g[r, x + 1] == v:
                out[r, x] = bg
    return None if (out == g).all() else out


# --------------------------------------------------------------- parts and logic
def _pair(g, how):
    """Two equal parts of the grid: split by separator lines, or as halves."""
    if how == "lines":
        ps = parts(g)
        if ps is None or len(ps) != 2 or ps[0].shape != ps[1].shape:
            return None
        return ps
    h, w = g.shape
    if how == "halves_lr":
        return (g[:, :w // 2], g[:, w // 2:]) if w % 2 == 0 else None
    return (g[:h // 2], g[h // 2:]) if h % 2 == 0 else None


def combine(g, p):
    """Lay two parts of the grid over each other and keep the cells where (and / or /
    xor / only-left / neither) is true, painted colour c. p = (how split, rule, c)."""
    how, rule, c = p
    pr = _pair(g, how)
    if pr is None:
        return None
    a, b = pr
    bg = background(g)
    x, y = a != bg, b != bg
    m = {"and": x & y, "or": x | y, "xor": x ^ y, "left": x & ~y, "nor": ~x & ~y}[rule]
    out = np.zeros(a.shape, dtype=g.dtype)
    out[m] = c
    return out


def pick_part(g, p):
    """One of the parts the grid is divided into (p: which, e.g. 'odd one out')."""
    ps = parts(g)
    if ps is None:
        return None
    if p == "first":
        return ps[0]
    if p == "last":
        return ps[-1]
    keys = [(q.shape, q.tobytes()) for q in ps]
    if p == "odd_one":
        uniq = [q for q, k in zip(ps, keys) if keys.count(k) == 1]
        return uniq[0] if len(uniq) == 1 and len(ps) > 2 else None
    if p == "most_colour":
        counts = [int((q != background(q)).sum()) for q in ps]
        best = max(counts)
        return ps[counts.index(best)] if counts.count(best) == 1 else None
    if p == "least_colour":
        counts = [int((q != background(q)).sum()) for q in ps]
        best = min(counts)
        return ps[counts.index(best)] if counts.count(best) == 1 else None
    return None


def overlay_parts(g, p=None):
    """Lay all parts over each other; later parts' colours show through the background."""
    ps = parts(g)
    if ps is None or len({q.shape for q in ps}) != 1:
        return None
    bg = background(g)
    out = ps[0].copy()
    for q in ps[1:]:
        m = q != bg
        out[m] = q[m]
    return out


# --------------------------------------------------------------- the registry
# (name, function, parameter space from the task's context)
def registry(ctx):
    cols = ctx["out_colours"]
    ops = [("rot90", rot90, [None]), ("rot180", rot180, [None]), ("rot270", rot270, [None]),
           ("flip_v", flip_v, [None]), ("flip_h", flip_h, [None]),
           ("transpose", transpose, [None]), ("antitranspose", antitranspose, [None]),
           ("crop_content", crop_content, [None]),
           ("crop_thing", crop_thing, [(s, m) for m in (False, True) for s in SELECT]),
           ("keep_thing", keep_thing, [(s, m) for m in (False, True) for s in SELECT]),
           ("remove_specks", remove_specks, [1, 2]),
           ("upscale", upscale, ctx["scales_up"]),
           ("downscale", downscale, ctx["scales_down"]),
           ("tile", tile, ctx["tiles"]),
           ("mirror_tile", mirror_tile, ["h", "v", "both"]),
           ("recolour_all", recolour_all, cols),
           ("keep_colour", keep_colour, ctx["in_colours"]),
           ("remove_colour", remove_colour, ctx["in_colours"]),
           ("fill_enclosed", fill_enclosed, cols),
           ("gravity", gravity, ["down", "up", "left", "right"]),
           ("outline", outline, cols),
           ("symmetrize", symmetrize, ["h", "v", "both", "rot"]),
           ("combine", combine, [(h, r, c) for h in ("lines", "halves_lr", "halves_tb")
                                 for r in ("and", "or", "xor", "left", "nor") for c in cols
                                 if c != 0]),
           ("pick_part", pick_part, ["first", "last", "odd_one", "most_colour", "least_colour"]),
           ("overlay_parts", overlay_parts, [None]),
           ("complete_pattern", complete_pattern, ctx["in_colours"]),
           ("complete_diagonal", complete_diagonal, ctx["in_colours"]),
           ("fractal", fractal, [None]),
           ("connect", connect, ["rows", "cols", "diagonals", "all"]),
           ("lines_through", lines_through, [(c, a) for c in ctx["in_colours"]
                                             for a in ("h", "v", "both")]),
           ("continue_pattern", continue_pattern, ctx["ratios"]),
           ("count_parts", count_parts, [None]),
           ("count_things", count_things, cols),
           ("each_thing", each_thing, [(h, m) for m in (False, True)
                                       for h in ("flip_h", "flip_v", "rot180", "transpose")]),
           ("slide_things", slide_things, ["down", "up", "left", "right"]),
           ("frame_things", frame_things, cols),
           ("hollow_things", hollow_things, [None]),
           ("extend_rays", extend_rays, [(c, d) for c in ctx["in_colours"]
                                         for d in ("up", "down", "left", "right", "all")])]
    return [(n, f, p) for n, f, ps in ops for p in ps]
