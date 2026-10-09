"""Seeing a grid: background, things (objects), their boxes, how a grid splits into parts.

These are perception, not answers: the same few ideas a child uses on any picture.
"""

from collections import Counter, deque

import numpy as np


def key(g):
    """A hashable fingerprint of a grid."""
    return (g.shape, g.tobytes())


def background(g):
    """The most common colour."""
    vals, counts = np.unique(g, return_counts=True)
    return int(vals[np.argmax(counts)])


def colours(g):
    return sorted(int(c) for c in np.unique(g))


def bbox(mask):
    rows = np.flatnonzero(mask.any(axis=1))
    cols = np.flatnonzero(mask.any(axis=0))
    if not len(rows):
        return None
    return rows[0], rows[-1] + 1, cols[0], cols[-1] + 1


class Thing:
    """A connected piece of the grid that isn't background."""

    def __init__(self, cells, grid, bg):
        self.cells = cells
        rs = [r for r, _ in cells]
        cs = [c for _, c in cells]
        self.r0, self.r1, self.c0, self.c1 = min(rs), max(rs) + 1, min(cs), max(cs) + 1
        self.size = len(cells)
        vals = Counter(int(grid[r, c]) for r, c in cells)
        self.colour = vals.most_common(1)[0][0]
        self.n_colours = len(vals)
        self.patch = np.full((self.r1 - self.r0, self.c1 - self.c0), bg, dtype=grid.dtype)
        for r, c in cells:
            self.patch[r - self.r0, c - self.c0] = grid[r, c]

    @property
    def box_area(self):
        return (self.r1 - self.r0) * (self.c1 - self.c0)


_SEEN = {}


def things(g, bg=None, diagonal=False, multicolour=False):
    """Connected pieces of non-background cells. multicolour: neighbours of any
    non-background colour join; otherwise only the same colour. (A grid looked at
    before is remembered, not looked at again.)"""
    bg = background(g) if bg is None else bg
    k = (key(g), bg, diagonal, multicolour)
    if k not in _SEEN:
        if len(_SEEN) > 20000:
            _SEEN.clear()
        _SEEN[k] = _things(g, bg, diagonal, multicolour)
    return _SEEN[k]


def _things(g, bg, diagonal, multicolour):
    h, w = g.shape
    seen = np.zeros(g.shape, dtype=bool)
    steps = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    if diagonal:
        steps += [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    out = []
    for r in range(h):
        for c in range(w):
            if seen[r, c] or g[r, c] == bg:
                continue
            col = g[r, c]
            cells, queue = [], deque([(r, c)])
            seen[r, c] = True
            while queue:
                y, x = queue.popleft()
                cells.append((y, x))
                for dy, dx in steps:
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < h and 0 <= nx < w and not seen[ny, nx] and g[ny, nx] != bg \
                            and (multicolour or g[ny, nx] == col):
                        seen[ny, nx] = True
                        queue.append((ny, nx))
            out.append(Thing(cells, g, bg))
    return out


def separator_lines(g):
    """Full rows and columns of one colour that cut the grid into parts: a colour is a
    separator only if every cell of that colour lies on such a line."""
    h, w = g.shape
    best = ([], [])
    for c in colours(g):
        rows = [r for r in range(h) if (g[r] == c).all()]
        cols = [x for x in range(w) if (g[:, x] == c).all()]
        if not rows and not cols:
            continue
        on_lines = np.zeros(g.shape, dtype=bool)
        on_lines[rows, :] = True
        on_lines[:, cols] = True
        if ((g == c) & ~on_lines).any():
            continue
        if len(rows) + len(cols) > len(best[0]) + len(best[1]):
            best = (rows, cols)
    return best


def parts(g):
    """The grid's parts: split by separator lines, if there are any (and they don't
    cover everything), else None."""
    h, w = g.shape
    rows, cols = separator_lines(g)
    if len(rows) + len(cols) == 0 or len(rows) == h or len(cols) == w:
        return None
    rcuts = _spans(rows, h)
    ccuts = _spans(cols, w)
    out = [g[a:b, c:d] for a, b in rcuts for c, d in ccuts]
    if len(out) < 2 or any(p.size == 0 for p in out):
        return None
    return out


def _spans(lines, n):
    spans, start = [], 0
    for x in sorted(lines) + [n]:
        if x > start:
            spans.append((start, x))
        start = x + 1
    return spans


def halves(g):
    """Two equal halves (side by side, or one above the other), if the grid is even."""
    h, w = g.shape
    out = []
    if w % 2 == 0:
        out.append((g[:, :w // 2], g[:, w // 2:]))
    if h % 2 == 0:
        out.append((g[:h // 2], g[h // 2:]))
    return out
