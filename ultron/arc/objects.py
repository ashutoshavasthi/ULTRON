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
# the empty set first: "every thing does the same"
FEATURE_SETS = [()] + [(q,) for q in QUANTITIES] + list(itertools.combinations(QUANTITIES, 2))


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
    RAYS.clear()
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


RAYS = {}                   # rays already traced while learning one law

DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]


def _ray(g, th, dr, dc, stop, bg):
    """The background cells a ray reaches, sent from every cell of a thing in one
    direction until the edge (or, if stop, until it meets something)."""
    own = set(th.cells)
    out = set()
    h, w = g.shape
    for r, c in th.cells:
        r, c = r + dr, c + dc
        while 0 <= r < h and 0 <= c < w:
            if (r, c) not in own:
                if g[r, c] != bg:
                    if stop:
                        break
                else:
                    out.add((r, c))
            r, c = r + dr, c + dc
    return out


def _mark_cells(g, th, mark, bg):
    if mark[0] == "ray":
        _, dr, dc, col, stop = mark
        return {(r, c, col) for r, c in _ray(g, th, dr, dc, stop, bg)}
    dr, dc, col = mark
    r, c = th.r0 + dr, th.c0 + dc
    if 0 <= r < g.shape[0] and 0 <= c < g.shape[1] and g[r, c] == bg:
        return {(r, c, col)}
    return set()


def _marks(setting, fs, seen):
    bgs = [background(g) for g, _, _, _ in seen]
    inst = {}                   # kind -> [(grid index, thing)]
    for gi, (g, t, ts, qs) in enumerate(seen):
        for th, q in zip(ts, qs):
            inst.setdefault(tuple(q[f] for f in fs), []).append((gi, th))
    colours = sorted({int(v) for g, t, _, _ in seen for v in t[g != t].tolist()})
    stamps = {}
    for kind, places in inst.items():
        if len(places) < 2:
            stamps[kind] = frozenset()      # seen once: no evidence of what it does
            continue
        keep = set()
        # rays: lines a thing sends out until the edge (or until they meet something)
        for dr, dc in DIRS:
            for stop in (True, False):
                for col in colours:
                    ok, shown = True, 0
                    for gi, th in places:
                        g, t = seen[gi][0], seen[gi][1]
                        rk = (id(th), dr, dc, stop)
                        if rk not in RAYS:
                            RAYS[rk] = _ray(g, th, dr, dc, stop, bgs[gi])
                        cells = RAYS[rk]
                        if any(t[r, c] != col for r, c in cells):
                            ok = False
                            break
                        shown += bool(cells)
                    if ok and shown >= 2:
                        keep.add(("ray", dr, dc, col, stop))
                        break
        if any(m[0] == "ray" and m[4] for m in keep):      # a stopping ray says it all
            keep = {m for m in keep if m[4] or ("ray",) + m[1:4] + (True,) not in keep}
        covered = {}
        for gi, th in places:
            covered[id(th)] = {(r, c) for m in keep
                               for r, c, _ in _mark_cells(seen[gi][0], th, m, bgs[gi])}
        # marks at fixed places around the thing
        cand = set()
        for gi, th in places:
            g, t = seen[gi][0], seen[gi][1]
            rr, cc = np.nonzero(g != t)
            cand |= {(int(r) - th.r0, int(c) - th.c0, int(t[r, c])) for r, c in zip(rr, cc)
                     if (int(r), int(c)) not in covered[id(th)]}
        for dr, dc, col in cand:
            ok, shown = True, 0
            for gi, th in places:
                g, t = seen[gi][0], seen[gi][1]
                r, c = th.r0 + dr, th.c0 + dc
                # marks go only on background: an occupied cell says nothing
                if 0 <= r < g.shape[0] and 0 <= c < g.shape[1] and g[r, c] == bgs[gi]:
                    if t[r, c] != col:
                        ok = False
                        break
                    shown += 1
            if ok and shown >= 2:           # a mark at least two things actually show
                keep.add((dr, dc, col))
        stamps[kind] = frozenset(keep)
    # the marks must explain every painted cell
    for gi, (g, t, ts, qs) in enumerate(seen):
        painted = np.zeros(g.shape, bool)
        for th, q in zip(ts, qs):
            for m in stamps[tuple(q[f] for f in fs)]:
                for r, c, _ in _mark_cells(g, th, m, bgs[gi]):
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
        for m in stamps[k]:
            for r, c, col in _mark_cells(g, th, m, bg):
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
    if any(t.size >= g.size for g, t in zip(grids, targets)):
        return None
    best = _learn_colour_box(grids, targets)
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
        for mode in ("box", "patch", "inside"):
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


def _colour_box(g, colour, mode):
    """Where a colour is: the box around all its cells (or what that box holds inside)."""
    ys, xs = np.nonzero(g == colour)
    if len(ys) == 0:
        return None
    r0, r1, c0, c1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    if mode == "inside":
        if r1 - r0 < 3 or c1 - c0 < 3:
            return None
        return g[r0 + 1:r1 - 1, c0 + 1:c1 - 1]
    return g[r0:r1, c0:c1]


def colour_traits(g):
    """For each colour in the picture: how its cells lie (a rectangle's outline, a solid
    block) and how common it is compared with the others."""
    bg = background(g)
    vals, counts = np.unique(g, return_counts=True)
    present = [(int(v), int(n)) for v, n in zip(vals, counts) if v != bg]
    if not present:
        return {}
    ns = sorted({n for _, n in present})
    out = {}
    for c, n in present:
        ys, xs = np.nonzero(g == c)
        r0, r1, c0, c1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
        box = np.zeros((r1 - r0, c1 - c0), bool)
        box[ys - r0, xs - c0] = True
        ring = np.ones_like(box)
        if box.shape[0] > 2 and box.shape[1] > 2:
            ring[1:-1, 1:-1] = False
        out[c] = {"outline": bool(box.shape[0] > 2 and box.shape[1] > 2 and
                                  np.array_equal(box, ring)),
                  "solid": bool(box.all()),
                  "count_rank": "most" if n == ns[-1] else "least" if n == ns[0] else "middle"}
    return out


def _learn_colour_box(grids, targets):
    """The answer is the box where some colour is: a colour named outright, or chosen by a
    trait (the one drawn as an outline, the rarest...), learned from the examples."""
    colours = sorted(set.intersection(*[set(np.unique(g).tolist()) for g in grids]))
    for mode in ("box", "inside"):
        for c in colours:
            if all((lambda cut: cut is not None and np.array_equal(cut, t))(_colour_box(g, c, mode))
                   for g, t in zip(grids, targets)):
                return ("where colour", mode, ("colour",), (c,))
    traits = [colour_traits(g) for g in grids]
    for mode in ("box", "inside"):
        for trait, value in (("outline", True), ("solid", True), ("count_rank", "least"),
                             ("count_rank", "most")):
            ok = True
            for g, t, tr in zip(grids, targets, traits):
                chosen = [c for c, f in tr.items() if f[trait] == value]
                if len(chosen) != 1:
                    ok = False
                    break
                cut = _colour_box(g, chosen[0], mode)
                if cut is None or not np.array_equal(cut, t):
                    ok = False
                    break
            if ok:
                return ("where colour", mode, (trait,), (value,))
    return None


def _cut(g, th, mode):
    if mode == "inside":            # what a frame holds: its box without its border
        if th.r1 - th.r0 < 3 or th.c1 - th.c0 < 3:
            return np.zeros((0, 0), dtype=g.dtype)
        return g[th.r0 + 1:th.r1 - 1, th.c0 + 1:th.c1 - 1]
    return g[th.r0:th.r1, th.c0:th.c1] if mode == "box" else th.patch


def _pick_size(rule):
    return 1 + 0.5 * len(rule[2])


def apply_pick(rule, g):
    setting, mode, fs, value = rule
    if setting == "where colour":
        if fs == ("colour",):
            cut = _colour_box(g, value[0], mode)
        else:
            chosen = [c for c, f in colour_traits(g).items() if f[fs[0]] == value[0]]
            if len(chosen) != 1:
                return None     # no single colour has the trait: no guess
            cut = _colour_box(g, chosen[0], mode)
        return None if cut is None else cut.copy()
    ts, qs = describe_things(g, setting)
    cuts = [_cut(g, th, mode) for th, q in zip(ts, qs) if tuple(q[f] for f in fs) == value]
    if not cuts or cuts[0].size == 0 or any(not np.array_equal(c, cuts[0]) for c in cuts):
        return None             # nothing, or things that disagree, fit the law: no guess
    return cuts[0].copy()


def pick_length(rule):
    return _pick_size(rule)


def describe_pick(rule):
    setting, mode, fs, value = rule
    if setting == "where colour":
        which = f"colour {value[0]}" if fs == ("colour",) else \
            {"outline": "the colour drawn as an outline", "solid": "the colour drawn as a block",
             "count_rank": f"the {value[0]} common colour"}[fs[0]]
        return f"{'inside ' if mode == 'inside' else ''}the box where {which} is"
    v = ", ".join(f"{f}={'…' if f == 'shape' else x}" for f, x in zip(fs, value))
    return f"the thing with {v}"


# ------------------------------------------------------------------ how things move

def _move_cost(m):
    """How much a way of moving takes to say: "toward the other thing" names nothing,
    a slide names a direction, a step names a distance too."""
    if m[0] == "toward":
        return 0
    if m[0] == "slide":
        return 1
    if m[0] == "own":
        return 1.5
    return 1 + (abs(m[1]) + abs(m[2]) > 1)


def _displace(g, th, rule, bg, static):
    """Where a thing goes: a fixed step, a slide until it meets something (or the edge),
    or a step as long as its own height or width."""
    kind = rule[0]
    if kind == "step":
        return rule[1], rule[2]
    if kind == "own":
        _, sign, dr, dc = rule
        return sign * dr * (th.r1 - th.r0), sign * dc * (th.c1 - th.c0)
    if kind == "toward":
        dr, dc = _toward(g, th, static)
        if (dr, dc) == (0, 0):
            return 0, 0
    else:
        _, dr, dc = rule
    h, w = g.shape
    k = 0
    while True:
        nxt = [(r + (k + 1) * dr, c + (k + 1) * dc) for r, c in th.cells]
        if any(not (0 <= r < h and 0 <= c < w) or static[r, c] for r, c in nxt):
            return k * dr, k * dc
        k += 1
        if k > 30:
            return k * dr, k * dc


def _toward(g, th, static):
    """The one direction in which the thing, going straight, would meet something that
    stays put (or none, if there isn't exactly one)."""
    h, w = g.shape
    found = []
    for dr, dc in DIRS[:4]:
        for r, c in th.cells:
            r, c = r + dr, c + dc
            hit = False
            while 0 <= r < h and 0 <= c < w:
                if static[r, c]:
                    hit = True
                    break
                r, c = r + dr, c + dc
            if hit:
                found.append((dr, dc))
                break
    return found[0] if len(found) == 1 else (0, 0)


def _move_all(g, ts, rules, bg):
    static = np.zeros(g.shape, bool)
    for th, rule in zip(ts, rules):
        if rule is None:
            for r, c in th.cells:
                static[r, c] = True
    out = g.copy()
    moves = []
    for th, rule in zip(ts, rules):
        if rule is not None:
            moves.append((th, _displace(g, th, rule, bg, static)))
            for r, c in th.cells:
                out[r, c] = bg
    h, w = g.shape
    for th, (dr, dc) in moves:
        for r, c in th.cells:
            if 0 <= r + dr < h and 0 <= c + dc < w:
                out[r + dr, c + dc] = g[r, c]
    return out


def _move_options(g, t, th, bg, static):
    """The rules that would move this thing where the example shows it (if it moved)."""
    h, w = g.shape
    out = []
    for dr in range(-h + 1, h):
        for dc in range(-w + 1, w):
            if all(0 <= r + dr < h and 0 <= c + dc < w and t[r + dr, c + dc] == g[r, c]
                   for r, c in th.cells):
                out.append((dr, dc))
    rules = set()
    for d in out:
        if d == (0, 0):
            rules.add(None)
            continue
        rules.add(("step",) + d)
        if _displace(g, th, ("toward",), bg, static) == d:
            rules.add(("toward",))
        for dr, dc in DIRS[:4]:
            if _displace(g, th, ("slide", dr, dc), bg, static) == d:
                rules.add(("slide", dr, dc))
            for sign in (1, -1):
                if _displace(g, th, ("own", sign, dr, dc), bg, static) == d:
                    rules.add(("own", sign, dr, dc))
    return rules


def learn_moves(grids, targets):
    """Pictures where things move as wholes: for each kind of thing, how it moves (the
    shortest law that puts every thing where every example shows it)."""
    if any(g.shape != t.shape for g, t in zip(grids, targets)):
        return None
    if all((g == t).all() for g, t in zip(grids, targets)):
        return None
    best = None
    for setting in SETTINGS:
        seen = []
        for g, t in zip(grids, targets):
            ts, qs = describe_things(g, setting)
            if not qs or len(ts) > 20:
                seen = None
                break
            seen.append((g, t, ts, qs))
        if seen is None:
            continue
        for fs in FEATURE_SETS:
            if best is not None and 1 + 0.5 * len(fs) >= _moves_size(best):
                break
            rule = _moves(setting, fs, seen)
            if rule is not None and (best is None or _moves_size(rule) < _moves_size(best)):
                best = rule
    return best


def _moves(setting, fs, seen):
    # first, which things stay put: kinds whose every instance is unmoved in the example
    kinds = {}
    for g, t, ts, qs in seen:
        bg = background(g)
        for th, q in zip(ts, qs):
            k = tuple(q[f] for f in fs)
            stays = all(t[r, c] == g[r, c] for r, c in th.cells)
            kinds.setdefault(k, []).append(stays)
    moving = {k for k, v in kinds.items() if not all(v)}
    if not moving or any(len(kinds[k]) < 2 for k in moving):
        return None             # a kind seen moving once: no evidence of how it moves
    options = {}
    for g, t, ts, qs in seen:
        bg = background(g)
        static = np.zeros(g.shape, bool)
        for th, q in zip(ts, qs):
            if tuple(q[f] for f in fs) not in moving:
                for r, c in th.cells:
                    static[r, c] = True
        for th, q in zip(ts, qs):
            k = tuple(q[f] for f in fs)
            if k in moving:
                o = _move_options(g, t, th, bg, static) - {None}
                options[k] = o if k not in options else options[k] & o
                if not options[k]:
                    return None
    table = {k: min(v, key=lambda m: (_move_cost(m), str(m))) for k, v in options.items()}
    for g, t, ts, qs in seen:
        rules = [table.get(tuple(q[f] for f in fs)) for q in qs]
        if not np.array_equal(_move_all(g, ts, rules, background(g)), t):
            return None
    return (setting, fs, table)


def _moves_size(rule):
    return 1 + 0.5 * max(1, len(rule[1])) * sum(1 + _move_cost(m) for m in rule[2].values())


def apply_moves(rule, g):
    setting, fs, table = rule
    ts, qs = describe_things(g, setting)
    if not qs:
        return None
    rules = [table.get(tuple(q[f] for f in fs)) for q in qs]
    if all(r is None for r in rules):
        return None
    return _move_all(g, ts, rules, background(g))


def moves_length(rule):
    return _moves_size(rule)


def describe_moves(rule):
    setting, fs, table = rule
    words = {"step": "steps", "slide": "slides", "own": "moves by its own size",
             "toward": "goes toward what stays put"}
    how = sorted({words[m[0]] for m in table.values()})
    return f"things move by ({', '.join(fs)}): {len(table)} kinds ({', '.join(how)})"


# ------------------------------------------------------------- copies of a template

def _place(out, g, th, r, c, bg, recolour=None):
    """Paint the template's cells with its top-left at (r, c); background cells of the
    picture only, and only inside it."""
    h, w = out.shape
    for (tr, tc) in th.cells:
        rr, cc = r + tr - th.r0, c + tc - th.c0
        if 0 <= rr < h and 0 <= cc < w and out[rr, cc] == bg:
            out[rr, cc] = g[tr, tc] if recolour is None else recolour


def _copies(g, setting, pick_fs, pick_value, anchor, recolour):
    """Copy the template (the thing with that value) onto every other thing (a marker)."""
    bg = background(g)
    ts, qs = describe_things(g, setting)
    if not qs:
        return None
    tmpl = [th for th, q in zip(ts, qs) if tuple(q[f] for f in pick_fs) == pick_value]
    if len(tmpl) != 1:
        return None
    t = tmpl[0]
    markers = [th for th in ts if th is not t]
    if not markers:
        return None
    out = g.copy()
    for m in markers:                   # a marker is replaced by its copy
        for r, c in m.cells:
            out[r, c] = bg
    for m in markers:
        if anchor == "centre":
            r = (m.r0 + m.r1 - 1) // 2 - (t.r1 - t.r0 - 1) // 2
            c = (m.c0 + m.c1 - 1) // 2 - (t.c1 - t.c0 - 1) // 2
        else:                       # the template's cell of the marker's colour goes there
            same = [(tr, tc) for tr, tc in t.cells if g[tr, tc] == m.colour]
            if len(same) != 1 or m.size != 1:
                return None
            (tr, tc), (mr, mc) = same[0], m.cells[0]
            r, c = t.r0 + mr - tr, t.c0 + mc - tc
        _place(out, g, t, r, c, bg, m.colour if recolour else None)
    return out


def learn_copies(grids, targets):
    """Pictures where copies of one thing (the template) appear at the other things (the
    markers): which thing is the template, how a copy sits on its marker, and whether it
    takes the marker's colour, learned from the examples (shortest first)."""
    if any(g.shape != t.shape for g, t in zip(grids, targets)):
        return None
    if all((g == t).all() for g, t in zip(grids, targets)):
        return None
    for setting in [(False, True), (True, True), (False, False), (True, False)]:
        described = [describe_things(g, setting) for g in grids]
        if any(not qs or len(ts) > 12 for ts, qs in described):
            continue
        for fs in FEATURE_SETS[1:1 + len(QUANTITIES)]:      # one quantity says which
            values = None
            for ts, qs in described:
                vs = {tuple(q[f] for f in fs) for q in qs}
                once = {v for v in vs if sum(1 for q in qs if tuple(q[f] for f in fs) == v) == 1}
                values = once if values is None else values & once
            for value in sorted(values or [], key=str):
                for anchor in ("centre", "colour"):
                    for recolour in (False, True):
                        if all((lambda o: o is not None and np.array_equal(o, t))(
                                _copies(g, setting, fs, value, anchor, recolour))
                               for g, t in zip(grids, targets)):
                            return (setting, fs, value, anchor, recolour)
    return None


def apply_copies(rule, g):
    setting, fs, value, anchor, recolour = rule
    return _copies(g, setting, fs, value, anchor, recolour)


def copies_length(rule):
    return 2 + 0.5 * len(rule[1]) + (0.5 if rule[4] else 0)


def describe_copies(rule):
    setting, fs, value, anchor, recolour = rule
    v = ", ".join(f"{f}={'…' if f == 'shape' else x}" for f, x in zip(fs, value))
    how = "centred on" if anchor == "centre" else "matching colours with"
    return (f"copies of the thing with {v} {how} every other thing" +
            (", in that thing's colour" if recolour else ""))


# -------------------------------------------------------------- lines between things

def _gaps(g, bg):
    """Every run of background between two coloured cells on a row or a column:
    (direction, end colour a, end colour b, cells)."""
    h, w = g.shape
    out = []
    for r in range(h):
        idx = [c for c in range(w) if g[r, c] != bg]
        for a, b in zip(idx, idx[1:]):
            if b > a + 1:
                out.append(("row", int(g[r, a]), int(g[r, b]), [(r, c) for c in range(a + 1, b)]))
    for c in range(w):
        idx = [r for r in range(h) if g[r, c] != bg]
        for a, b in zip(idx, idx[1:]):
            if b > a + 1:
                out.append(("col", int(g[a, c]), int(g[b, c]), [(r, c) for r in range(a + 1, b)]))
    return out


GAP_KEYS = [
    ("whether the ends match", lambda d, a, b: (a == b,)),
    ("whether the ends match and which way", lambda d, a, b: (d, a == b)),
    ("same colour", lambda d, a, b: (a == b, a if a == b else None)),
    ("the two colours", lambda d, a, b: (min(a, b), max(a, b))),
    ("direction, same colour", lambda d, a, b: (d, a == b, a if a == b else None)),
    ("direction, the two colours", lambda d, a, b: (d, min(a, b), max(a, b))),
]
ENDS = "the ends' colour"      # a gap filled with the colour its two (matching) ends share


def learn_gaps(grids, targets):
    """Pictures where lines are drawn between things: what fills a gap between two
    coloured cells on a row or column (a colour, or nothing) is a law of the two ends."""
    if any(g.shape != t.shape for g, t in zip(grids, targets)):
        return None
    bgs = [background(g) for g in grids]
    if any(((g != t) & (g != bg)).any() for g, t, bg in zip(grids, targets, bgs)):
        return None
    if all((g == t).all() for g, t in zip(grids, targets)):
        return None
    for kname, key in GAP_KEYS:
        table, ok = {}, True
        for g, t, bg in zip(grids, targets, bgs):
            for d, a, b, cells in _gaps(g, bg):
                vals = {int(t[r, c]) for r, c in cells}
                if len(vals) != 1:
                    vals = {bg} if all(t[r, c] == bg for r, c in cells) else vals
                if len(vals) != 1:
                    ok = False
                    break
                v = vals.pop()
                if a == b and v == a:
                    v = ENDS
                if table.setdefault(key(d, a, b), v) != v:
                    ok = False
                    break
            if not ok:
                break
        if not ok or all(v == bgs[0] for v in table.values()):
            continue
        rule = (kname, table)
        if all((lambda o: o is not None and np.array_equal(o, t))(apply_gaps(rule, g))
               for g, t in zip(grids, targets)):
            return rule
    return None


def apply_gaps(rule, g):
    kname, table = rule
    key = dict(GAP_KEYS)[kname]
    bg = background(g)
    out = g.copy()
    for d, a, b, cells in _gaps(g, bg):
        k = key(d, a, b)
        if k not in table:
            return None             # a kind of gap never seen in the examples: no guess
        v = a if table[k] == ENDS else table[k]
        if v != bg:
            for r, c in cells:
                out[r, c] = v
    return out


def gaps_length(rule):
    return 1 + 0.5 * sum(1 for v in rule[1].values())


def describe_gaps(rule):
    kname, table = rule
    n = sum(1 for v in table.values())
    return f"lines between things: what fills a gap depends on {kname} ({n} kinds of gap)"
