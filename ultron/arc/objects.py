"""Laws about things: a thing's new colour depends on what kind of thing it is.

Many pictures change thing by thing ("the biggest piece turns blue", "pieces with a hole
turn red", "pieces whose shape appears twice disappear"). This is Ultron's oldest skill,
finding a law among quantities, applied to the things it sees. Each thing is described
by plain quantities (its colour, size, shape, holes, ...). Ultron looks for the smallest
set of quantities for which one table, kind of thing → new colour, agrees with every
example; the shortest description wins.

As with local laws, a test thing of a kind never seen in the examples gets no answer
rather than a guess.
"""

import itertools

import numpy as np

from .grid import background, things

SETTINGS = [(False, False), (True, False), (False, True), (True, True)]  # (diagonal, multicolour)


def _holes(t, bg):
    """Background cells inside a thing's box that can't reach the box edge."""
    m = t.patch == bg
    h, w = m.shape
    seen = np.zeros_like(m)
    stack = [(r, c) for r in range(h) for c in range(w)
             if m[r, c] and (r in (0, h - 1) or c in (0, w - 1))]
    for r, c in stack:
        seen[r, c] = True
    while stack:
        r, c = stack.pop()
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            a, b = r + dr, c + dc
            if 0 <= a < h and 0 <= b < w and m[a, b] and not seen[a, b]:
                seen[a, b] = True
                stack.append((a, b))
    return int((m & ~seen).sum())


def describe_things(g, setting):
    """The things in g and, for each, its quantities."""
    bg = background(g)
    ts = things(g, bg, *setting)
    if not ts or len(ts) > 60:
        return ts, []
    shapes = [(t.patch != bg).tobytes() + bytes(t.patch.shape) for t in ts]
    sizes = sorted({t.size for t in ts})
    h, w = g.shape
    out = []
    for t, s in zip(ts, shapes):
        mask = t.patch != bg
        out.append({
            "colour": t.colour,
            "size": t.size,
            "size_rank": "largest" if t.size == sizes[-1] else
                         "smallest" if t.size == sizes[0] else "middle",
            "shape": s,
            "shape_count": shapes.count(s),
            "colour_count": sum(1 for u in ts if u.colour == t.colour),
            "height": t.r1 - t.r0,
            "width": t.c1 - t.c0,
            "holes": _holes(t, bg),
            "border": t.r0 == 0 or t.c0 == 0 or t.r1 == h or t.c1 == w,
            "n_colours": t.n_colours,
            "symmetric": bool((mask == mask[:, ::-1]).all() or (mask == mask[::-1]).all()),
            "filled": bool(mask.all()),
        })
    return ts, out


QUANTITIES = ["colour", "size", "size_rank", "shape", "shape_count", "colour_count",
              "height", "width", "holes", "border", "n_colours", "symmetric", "filled"]
FEATURE_SETS = [(q,) for q in QUANTITIES] + list(itertools.combinations(QUANTITIES, 2))


def learn(grids, targets):
    """The shortest law (perception setting, quantities, table, default) agreeing with
    every example, or None. A thing's outcome is "keep" (it stays as it was) or a colour.
    A law may name a default outcome and list only the exceptions to it, when that is
    the shorter description; the default then also covers kinds of thing the examples
    never showed (the law says what happens to them)."""
    if any(g.shape != t.shape for g, t in zip(grids, targets)):
        return None
    best = None
    for setting in SETTINGS:
        seen = []
        ok = True
        for g, t in zip(grids, targets):
            ts, qs = describe_things(g, setting)
            if not qs:
                ok = False
                break
            covered = np.zeros(g.shape, bool)
            new = []
            for th in ts:
                rr, cc = zip(*th.cells)
                covered[rr, cc] = True
                if (t[rr, cc] == g[rr, cc]).all():
                    new.append(KEEP)
                    continue
                vals = set(t[rr, cc].tolist())
                if len(vals) != 1:
                    ok = False
                    break
                new.append(vals.pop())
            if not ok or (g[~covered] != t[~covered]).any():
                ok = False
                break
            seen.append((qs, new))
        if not ok or all(v == KEEP for _, new in seen for v in new):
            continue
        for fs in FEATURE_SETS:
            table, counts, good = {}, {}, True
            for qs, new in seen:
                for q, v in zip(qs, new):
                    k = tuple(q[f] for f in fs)
                    counts[k] = counts.get(k, 0) + 1
                    if table.setdefault(k, v) != v:
                        good = False
                        break
                if not good:
                    break
            if not good:
                continue
            for rule in _forms(setting, fs, table, counts):
                if best is None or _size(rule) < _size(best):
                    best = rule
    return best


KEEP = "keep"


def _forms(setting, fs, table, counts):
    """The law as a full table, and as a default outcome plus its exceptions. A default is
    a claim about kinds of thing never seen, so it is allowed only when it really is the
    rule: it covers more of the kinds seen than all its exceptions together, and the law
    with its exceptions is shorter than the observations it explains."""
    yield (setting, fs, table, None)
    n = sum(counts.values())
    kinds = {}
    for v in table.values():
        kinds[v] = kinds.get(v, 0) + 1
    default = max(sorted(kinds, key=str), key=lambda v: kinds[v])
    exceptions = {k: v for k, v in table.items() if v != default}
    rule = (setting, fs, exceptions, default)
    if exceptions and kinds[default] > len(exceptions) and _size(rule) < 0.5 * n:
        yield rule


def _size(rule):
    _, fs, table, default = rule
    return 1 + 0.5 * len(fs) * len(table) + (0.5 if default is not None else 0)


def apply(rule, g):
    setting, fs, table, default = rule
    ts, qs = describe_things(g, setting)
    if not qs:
        return None
    out = g.copy()
    for th, q in zip(ts, qs):
        k = tuple(q[f] for f in fs)
        v = table.get(k, default)
        if v is None:
            return None         # a kind of thing the law says nothing about: no guess
        if v != KEEP:
            rr, cc = zip(*th.cells)
            out[rr, cc] = v
    return out


def length(rule):
    return _size(rule)


def describe(rule):
    setting, fs, table, default = rule
    if default is None:
        return f"thing law on ({', '.join(fs)}): {len(table)} kinds of thing"
    return (f"thing law on ({', '.join(fs)}): {default} except {len(table)} kind"
            f"{'s' if len(table) != 1 else ''}")
