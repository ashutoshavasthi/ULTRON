"""Symmetry laws: a picture that is symmetric except where something is missing.

Many pictures are mirror- or rotation-symmetric about some centre (not always the
middle of the grid), with parts missing: blank, or hidden under a patch of one colour.
Ultron finds the symmetry the picture already has: the group (a mirror, two mirrors,
quarter turns, a diagonal) and the centre where the cells it can see agree with their
images. It then fills each missing cell from its images. The kind of symmetry, what
counts as missing (blank, or a hiding colour), and whether the answer is only the
repaired patch are learned from the task's own examples, shortest first. Unless the
images agree, there is no answer.
"""

import numpy as np

from .grid import background

GROUPS = [("h", ["h"]), ("v", ["v"]), ("rot180", ["rot180"]), ("diag", ["diag"]),
          ("anti", ["anti"]), ("h+v", ["h", "v", "rot180"]),
          ("quarter turns", ["rot90", "rot180", "rot270"]),
          ("all", ["h", "v", "rot180", "rot90", "rot270", "diag", "anti"])]


def _image(op, r, c, R, C):  # one cell (see _images)
    # R, C: the centre in doubled coordinates
    if op == "h":
        return r, C - c
    if op == "v":
        return R - r, c
    if op == "rot180":
        return R - r, C - c
    dr2, dc2 = 2 * r - R, 2 * c - C          # offset from the centre, doubled
    if op == "rot90":
        nr2, nc2 = dc2, -dr2
    elif op == "rot270":
        nr2, nc2 = -dc2, dr2
    elif op == "diag":
        nr2, nc2 = dc2, dr2
    else:
        nr2, nc2 = -dc2, -dr2
    if (R + nr2) % 2 or (C + nc2) % 2:
        return None
    return (R + nr2) // 2, (C + nc2) // 2


def _images(op, rs, cs, R, C):
    """Images of many cells at once (numpy); cells whose image falls between cells are
    marked invalid."""
    if op == "h":
        return rs, C - cs, np.ones(len(rs), bool)
    if op == "v":
        return R - rs, cs, np.ones(len(rs), bool)
    if op == "rot180":
        return R - rs, C - cs, np.ones(len(rs), bool)
    dr2, dc2 = 2 * rs - R, 2 * cs - C
    nr2, nc2 = {"rot90": (dc2, -dr2), "rot270": (-dc2, dr2), "diag": (dc2, dr2),
                "anti": (-dc2, -dr2)}[op]
    ok = ((R + nr2) % 2 == 0) & ((C + nc2) % 2 == 0)
    return (R + nr2) // 2, (C + nc2) // 2, ok


_CENTRES = {}


def centre(g, known, ops):
    """The centre (doubled coordinates) where everything it can see agrees with its
    images, with the most agreeing pairs; None if there is none."""
    key = (g.tobytes(), g.shape, known.tobytes(), tuple(ops))
    if key in _CENTRES:
        return _CENTRES[key]
    h, w = g.shape
    rs, cs = np.nonzero(known)
    vals = g[rs, cs]
    best, best_n = None, 0
    for R in range(0, 2 * h - 1):
        for C in range(0, 2 * w - 1):
            n, bad = 0, False
            for op in ops:
                a, b, ok = _images(op, rs, cs, R, C)
                if not ok.all():
                    bad = True
                    break
                inside = (a >= 0) & (a < h) & (b >= 0) & (b < w)
                a, b = a[inside], b[inside]
                seen = known[a, b]
                if (g[a[seen], b[seen]] != vals[inside][seen]).any():
                    bad = True
                    break
                n += int(seen.sum())
            if not bad and n > best_n:
                best, best_n = (R, C), n
    # it must be real symmetry, not a coincidence of a few cells
    if best is None or best_n < max(4, int(known.sum()) // 2):
        best = None
    if len(_CENTRES) > 5000:
        _CENTRES.clear()
    _CENTRES[key] = best
    return best


def complete(g, ops, hiding=None, crop=False):
    """Fill what is missing (blank, or under the hiding colour) from its images."""
    bg = background(g)
    missing = (g == hiding) if hiding is not None else (g == bg)
    known = ~missing if hiding is not None else (g != bg)
    if not missing.any() or not known.any():
        return None
    c = centre(g, known, ops)
    if c is None:
        return None
    R, C = c
    out = g.copy()
    h, w = g.shape
    rs, cs = np.nonzero(missing)
    for r, cc in zip(rs.tolist(), cs.tolist()):
        vals = set()
        for op in ops:
            im = _image(op, r, cc, R, C)
            if im is None:
                continue
            a, b = im
            if 0 <= a < h and 0 <= b < w and known[a, b]:
                vals.add(int(g[a, b]))
        if len(vals) > 1:
            return None             # its images disagree: no answer
        if vals:
            out[r, cc] = vals.pop()
        elif hiding is not None:
            return None             # something hidden it has no way to see
    if crop:
        if hiding is None:
            return None
        ys, xs = np.nonzero(missing)
        return out[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    return out


def learn(grids, targets, colours):
    laws = rivals(grids, targets, colours, n=1)
    return laws[0] if laws else None


def rivals(grids, targets, colours, n=2):
    """The shortest symmetry laws that turn every example into its answer (when the
    examples can't tell two apart, both are kept: the two attempts)."""
    found = []
    for name, ops in GROUPS:
        for hiding in [None] + list(colours):
            for crop in (False, True):
                if crop and hiding is None:
                    continue
                ok = True
                for g, t in zip(grids, targets):
                    out = complete(g, ops, hiding, crop)
                    if out is None or out.shape != t.shape or not np.array_equal(out, t):
                        ok = False
                        break
                if ok:
                    found.append((name, hiding, crop))
                    if len(found) == n:
                        return found
    return found


def apply(rule, g):
    name, hiding, crop = rule
    return complete(g, dict(GROUPS)[name], hiding, crop)


def length(rule):
    name, hiding, crop = rule
    return 1 + 0.5 * len(dict(GROUPS)[name]) + (0.5 if hiding is not None else 0) + \
        (0.5 if crop else 0)


def describe(rule):
    name, hiding, crop = rule
    what = "blank cells" if hiding is None else f"what colour {hiding} hides"
    return f"symmetry ({name}) about its own centre fills {what}" + \
        (", answer is the repaired patch" if crop else "")
