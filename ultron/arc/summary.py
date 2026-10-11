"""Summary laws: the answer says something ABOUT the picture.

Some answers are not a changed picture but a summary of it:

  a colour      a 1x1 answer: which colour is a law (the colour of the thing that stands
                out, or a class of the picture: "symmetric pictures get 1, others 7")
  a count       a row, a column or a diagonal as long as how many there are of something
                (things, things of a kind, coloured cells)
  blocks        a picture made of uniform blocks, answered with one cell per block

As everywhere, the shortest law that explains every example wins, and a kind of picture
never seen in the examples gets no answer rather than a guess.
"""

import numpy as np

from .grid import background, things
from . import objects as O


# ------------------------------------------------------------------- picture traits
def _sym(g):
    bg = background(g)
    ys, xs = np.nonzero(g != bg)
    if len(ys) == 0:
        return "empty"
    b = g[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    return ("h" if np.array_equal(b, b[:, ::-1]) else "") + \
        ("v" if np.array_equal(b, b[::-1]) else "") or "none"


def picture_traits(g):
    """A few plain quantities of the whole picture."""
    bg = background(g)
    ts = things(g, bg, False, True)
    colours = sorted(set(np.unique(g).tolist()) - {bg})
    shapes = sorted({(t.patch != bg).tobytes() + bytes(t.patch.shape) for t in ts})
    return {"symmetry": _sym(g), "things": len(ts), "colours": len(colours),
            "shape": shapes[0] if len(shapes) == 1 else None,
            "colour set": tuple(colours)}


TRAITS = ["symmetry", "things", "colours", "shape", "colour set"]


# ----------------------------------------------------------------------- 1x1 answers
def _learn_colour(grids, targets):
    if not all(t.shape == (1, 1) for t in targets):
        return None
    want = [int(t[0, 0]) for t in targets]
    # the colour of the thing a law singles out
    for setting in O.SETTINGS:
        described = [O.describe_things(g, setting) for g in grids]
        if any(not qs for _, qs in described):
            continue
        for fs in O.FEATURE_SETS[1:]:
            values = None
            for (ts, qs), w in zip(described, want):
                fit = {tuple(q[f] for f in fs) for q in qs if q["colour"] == w}
                fit = {v for v in fit if all(q["colour"] == w for q in qs
                                             if tuple(q[f] for f in fs) == v)}
                values = fit if values is None else values & fit
                if not values:
                    break
            if values:
                return ("thing colour", setting, fs, sorted(values, key=str)[0])
    # a class of the picture: a table from one trait to the colour
    for trait in TRAITS:
        table, ok = {}, True
        for g, w in zip(grids, want):
            k = picture_traits(g)[trait]
            if k is None or table.setdefault(k, w) != w:
                ok = False
                break
        if ok and len(table) < len(grids):      # a law must say more than its examples
            return ("picture class", trait, table)
    return None


def _apply_colour(rule, g):
    if rule[0] == "thing colour":
        _, setting, fs, value = rule
        ts, qs = O.describe_things(g, setting)
        cs = {q["colour"] for q in qs if tuple(q[f] for f in fs) == value}
        return np.array([[cs.pop()]], dtype=g.dtype) if len(cs) == 1 else None
    _, trait, table = rule
    k = picture_traits(g)[trait]
    return np.array([[table[k]]], dtype=g.dtype) if k in table else None


# --------------------------------------------------------------------------- counts
def _counts(g):
    """Things worth counting, by name: {name: (count, colour of what was counted)}."""
    bg = background(g)
    out = {}
    for setting in ((False, False), (True, False), (False, True)):
        ts = things(g, bg, *setting)
        out[f"things{setting}"] = (len(ts), ts[0].colour if ts and
                                   len({t.colour for t in ts}) == 1 else None)
    vals, ns = np.unique(g, return_counts=True)
    present = [(int(v), int(n)) for v, n in zip(vals, ns) if v != bg]
    out["cells"] = (sum(n for _, n in present), present[0][0] if len(present) == 1 else None)
    out["colours"] = (len(present), None)
    for v, n in present:
        out[f"cells of {v}"] = (n, v)
    return out


LAYOUTS = ["row", "column", "diagonal", "square"]


def _draw(layout, k, colour, bg, width=None):
    if k <= 0 or k > 30:
        return None
    if layout == "row":
        if width is None:
            return np.full((1, k), colour)
        if k > width:
            return None
        out = np.full((1, width), bg)
        out[0, :k] = colour
        return out
    if layout == "column":
        return np.full((k, 1), colour)
    if layout == "square":
        return np.full((k, k), colour)
    out = np.full((k, k), bg)
    np.fill_diagonal(out, colour)
    return out


def _learn_count(grids, targets):
    counts = [_counts(g) for g in grids]
    names = sorted(set.intersection(*[set(c) for c in counts]))
    widths = {t.shape[1] for t in targets}
    width = widths.pop() if len(widths) == 1 and all(t.shape[0] == 1 for t in targets) else None
    for name in names:
        for layout in LAYOUTS:
            for fixed in ((None, width) if layout == "row" and width else (None,)):
                for colour_rule in ("counted", "constant"):
                    const = None
                    ok = True
                    for g, t, c in zip(grids, targets, counts):
                        k, counted = c[name]
                        if colour_rule == "counted":
                            colour = counted
                        else:
                            vals = set(np.unique(t).tolist()) - {background(g)}
                            colour = vals.pop() if len(vals) == 1 else None
                            if const is None:
                                const = colour
                            colour = const if colour == const else None
                        if colour is None:
                            ok = False
                            break
                        out = _draw(layout, k, colour, background(g), fixed)
                        if out is None or out.shape != t.shape or \
                                not np.array_equal(out.astype(t.dtype), t):
                            ok = False
                            break
                    if ok:
                        return ("count", name, layout, fixed, colour_rule, const)
    return None


def _apply_count(rule, g):
    _, name, layout, fixed, colour_rule, const = rule
    c = _counts(g)
    if name not in c:
        return None
    k, counted = c[name]
    colour = counted if colour_rule == "counted" else const
    if colour is None:
        return None
    out = _draw(layout, k, colour, background(g), fixed)
    return None if out is None else out.astype(g.dtype)


# --------------------------------------------------------------------------- blocks
def _runs(g, axis):
    keep = [0]
    for k in range(1, g.shape[axis]):
        a, b = (g[k], g[k - 1]) if axis == 0 else (g[:, k], g[:, k - 1])
        if not np.array_equal(a, b):
            keep.append(k)
    return g[keep] if axis == 0 else g[:, keep]


def blocks(g, crop):
    """One cell per uniform block (after cutting to what is drawn, if crop)."""
    if crop:
        bg = background(g)
        ys, xs = np.nonzero(g != bg)
        if len(ys) == 0:
            return None
        g = g[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    return _runs(_runs(g, 0), 1)


def _learn_blocks(grids, targets):
    for crop in (False, True):
        if all((lambda b: b is not None and np.array_equal(b, t))(blocks(g, crop))
               for g, t in zip(grids, targets)):
            return ("blocks", crop)
    return None


# ------------------------------------------------------------------------ the family
def learn(grids, targets):
    if any(t.size >= g.size for g, t in zip(grids, targets)):
        return None
    for f in (_learn_colour, _learn_count, _learn_blocks):
        rule = f(grids, targets)
        if rule is not None:
            return rule
    return None


def apply(rule, g):
    if rule[0] in ("thing colour", "picture class"):
        return _apply_colour(rule, g)
    if rule[0] == "count":
        return _apply_count(rule, g)
    return blocks(g, rule[1])


def length(rule):
    if rule[0] == "picture class":
        return 1 + 0.5 * len(rule[2])
    return 2


def describe(rule):
    kind = rule[0]
    if kind == "thing colour":
        v = ", ".join(f"{f}={'…' if f == 'shape' else x}" for f, x in zip(rule[2], rule[3]))
        return f"the colour of the thing with {v}"
    if kind == "picture class":
        return f"a colour for each kind of picture, by its {rule[1]} ({len(rule[2])} kinds)"
    if kind == "count":
        _, name, layout, fixed, colour_rule, const = rule
        return (f"a {layout} as long as the number of {name}" +
                (f" (in a row of {fixed})" if fixed else "") +
                (", in their colour" if colour_rule == "counted" else f", in colour {const}"))
    return "one cell per uniform block" + (" of what is drawn" if rule[1] else "")
