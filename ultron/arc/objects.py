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
    # "the most" and "the least": every count compared with the other things'
    for q in RANKED:
        vals = sorted({d[q] for d in out})
        for d in out:
            d[q + "_rank"] = "most" if d[q] == vals[-1] else \
                             "least" if d[q] == vals[0] else "middle"
    return ts, out


RANKED = ["shape_count", "colour_count", "holes", "height", "width", "n_colours"]


QUANTITIES = ["colour", "size", "size_rank", "shape", "shape_count", "colour_count",
              "height", "width", "holes", "border", "n_colours", "symmetric", "filled"] + \
             [q + "_rank" for q in RANKED]
FEATURE_SETS = [(q,) for q in QUANTITIES] + list(itertools.combinations(QUANTITIES, 2))


def learn(grids, targets):
    """The shortest law (perception setting, quantities, table, default) agreeing with
    every example, or None. A thing's outcome is "keep" (it stays as it was) or a colour.
    A law may name a default outcome and list only the exceptions to it, when that is
    the shorter description; the default then also covers kinds of thing the examples
    never showed (the law says what happens to them)."""
    laws = rivals(grids, targets)
    return laws[0] if laws else None


def rivals(grids, targets, n=2):
    """The n shortest laws: when the examples can't tell two laws apart (say, "things with
    a hole" and "things of size 8"), both are kept, as Ultron does with any confounder."""
    if any(g.shape != t.shape for g, t in zip(grids, targets)):
        return []
    found = []
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
                found.append(rule)
    order = sorted(range(len(found)), key=lambda i: (_size(found[i]), i))
    out, tables = [], []
    for i in order:
        if (found[i][2], found[i][3]) in tables and found[i][1] == out[-1][1]:
            continue
        out.append(found[i])
        tables.append((found[i][2], found[i][3]))
        if len(out) == n:
            break
    return out


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


# ------------------------------------------------- what things do to their surroundings

def learn_marks(grids, targets):
    """Pictures where paint appears around things: for each kind of thing, the marks it
    leaves around itself (cells at fixed places relative to it, with their colours). The
    shortest law that explains every painted cell, and nothing else, wins."""
    if any(g.shape != t.shape for g, t in zip(grids, targets)):
        return None
    bgs = [background(g) for g in grids]
    if any(((g != t) & (g != bg)).any() for g, t, bg in zip(grids, targets, bgs)):
        return None             # something other than background changed
    if all((g == t).all() for g, t in zip(grids, targets)):
        return None
    best = None
    for setting in SETTINGS:
        seen = []
        for g, t in zip(grids, targets):
            ts, qs = describe_things(g, setting)
            if not qs or len(ts) > 30:
                seen = None
                break
            seen.append((g, t, ts, qs))
        if seen is None:
            continue
        for fs in FEATURE_SETS:
            rule = _marks(setting, fs, seen)
            if rule is not None and (best is None or _marks_size(rule) < _marks_size(best)):
                best = rule
    return best


def _marks(setting, fs, seen):
    bgs = [background(g) for g, _, _, _ in seen]
    inst = {}                   # kind -> [(grid index, anchor)]
    for gi, (g, t, ts, qs) in enumerate(seen):
        for th, q in zip(ts, qs):
            inst.setdefault(tuple(q[f] for f in fs), []).append((gi, th.r0, th.c0))
    stamps = {}
    for kind, places in inst.items():
        if len(places) < 2:
            stamps[kind] = frozenset()      # seen once: no evidence of what it does
            continue
        cand = set()
        for gi, r0, c0 in places:
            g, t = seen[gi][0], seen[gi][1]
            rr, cc = np.nonzero(g != t)
            cand |= {(int(r) - r0, int(c) - c0, int(t[r, c])) for r, c in zip(rr, cc)}
        keep = set()
        for dr, dc, col in cand:
            ok, shown = True, 0
            for gi, r0, c0 in places:
                g, t = seen[gi][0], seen[gi][1]
                r, c = r0 + dr, c0 + dc
                # marks go only on background: an occupied cell says nothing
                if 0 <= r < g.shape[0] and 0 <= c < g.shape[1] and \
                        g[r, c] == bgs[gi] and t[r, c] != col:
                    ok = False
                    break
                if 0 <= r < g.shape[0] and 0 <= c < g.shape[1] and g[r, c] == bgs[gi]:
                    shown += 1
            if ok and shown >= 2:           # a mark at least two things actually show
                keep.add((dr, dc, col))
        stamps[kind] = frozenset(keep)
    # the marks must explain every painted cell
    for gi, (g, t, ts, qs) in enumerate(seen):
        painted = np.zeros(g.shape, bool)
        for th, q in zip(ts, qs):
            for dr, dc, col in stamps[tuple(q[f] for f in fs)]:
                r, c = th.r0 + dr, th.c0 + dc
                if 0 <= r < g.shape[0] and 0 <= c < g.shape[1]:
                    painted[r, c] = True
        if (painted != (g != t)).any():
            return None
    if not any(stamps.values()):
        return None
    # a law must compress: the marks, written once, explain at least twice as many
    # painted cells
    painted = sum(int((g != t).sum()) for g, t, _, _ in seen)
    if 2 * sum(len(s) for s in set(stamps.values())) > painted:
        return None
    return (setting, fs, stamps)


def _marks_size(rule):
    _, fs, stamps = rule
    distinct = {s for s in stamps.values()}
    return 1 + 0.5 * len(fs) * len(stamps) + 0.25 * sum(len(s) for s in distinct)


def marks_length(rule):
    return _marks_size(rule)


def apply_marks(rule, g):
    setting, fs, stamps = rule
    ts, qs = describe_things(g, setting)
    if not qs:
        return None
    out = g.copy()
    bg = background(g)
    for th, q in zip(ts, qs):
        k = tuple(q[f] for f in fs)
        if k not in stamps:
            return None         # a kind of thing never seen in the examples: no guess
        for dr, dc, col in stamps[k]:
            r, c = th.r0 + dr, th.c0 + dc
            if 0 <= r < g.shape[0] and 0 <= c < g.shape[1] and g[r, c] == bg:
                out[r, c] = col
    return out


def describe_marks(rule):
    setting, fs, stamps = rule
    n = sum(1 for s in stamps.values() if s)
    return f"marks around things by ({', '.join(fs)}): {n} kinds leave marks"


# ------------------------------------------------------------- which thing is the answer

def learn_pick(grids, targets):
    """Pictures whose answer is one of their things: the shortest description of which
    one, as a value of its quantities (say, "the one whose shape appears once"); every
    thing with that value must give the same answer. Returns (setting, mode, quantities,
    value)."""
    best = None
    for setting in SETTINGS:
        seen = []
        for g, t in zip(grids, targets):
            ts, qs = describe_things(g, setting)
            if not qs:
                seen = None
                break
            seen.append((g, t, ts, qs))
        if seen is None:
            continue
        for mode in ("box", "patch"):
            right = []
            for g, t, ts, qs in seen:
                right.append({i for i, th in enumerate(ts) if np.array_equal(_cut(g, th, mode), t)})
            if not all(right):
                continue
            for fs in FEATURE_SETS:
                if best is not None and 1 + 0.5 * len(fs) >= _pick_size(best):
                    break
                values = None
                for (g, t, ts, qs), ok in zip(seen, right):
                    keys = [tuple(q[f] for f in fs) for q in qs]
                    # a value every thing with it gives the right answer
                    fit = {keys[i] for i in ok
                           if all(j in ok for j, k in enumerate(keys) if k == keys[i])}
                    values = fit if values is None else values & fit
                    if not values:
                        break
                if values:
                    best = (setting, mode, fs, sorted(values, key=str)[0])
                    break
    return best


def _cut(g, th, mode):
    return g[th.r0:th.r1, th.c0:th.c1] if mode == "box" else th.patch


def _pick_size(rule):
    return 1 + 0.5 * len(rule[2])


def apply_pick(rule, g):
    setting, mode, fs, value = rule
    ts, qs = describe_things(g, setting)
    cuts = [_cut(g, th, mode) for th, q in zip(ts, qs) if tuple(q[f] for f in fs) == value]
    if not cuts or any(not np.array_equal(c, cuts[0]) for c in cuts):
        return None             # nothing, or things that disagree, fit the law: no guess
    return cuts[0].copy()


def pick_length(rule):
    return _pick_size(rule)


def describe_pick(rule):
    setting, mode, fs, value = rule
    v = ", ".join(f"{f}={'…' if f == 'shape' else x}" for f, x in zip(fs, value))
    return f"the thing with {v}"
