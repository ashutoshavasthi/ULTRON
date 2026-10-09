"""Solving an ARC task the way Ultron finds any law: the shortest program that explains
every example. Programs are chains of grid operations, tried shortest first; programs
that do exactly the same thing to every example are kept once (observational
equivalence). The last step may be a colour mapping learned from the examples
themselves, when one consistent mapping turns the program's output into every target.

The search has a fixed budget of operations per task (not a time limit), so a run gives
the same answer on any machine.
"""

import numpy as np

from . import cells, objects, summary, symmetry, tiles
from . import ops as O
from .grid import colours, key

BUDGET = 40_000         # grid operations per task
MAX_DEPTH = 3


def context(train):
    ins = [i for i, _ in train]
    outs = [o for _, o in train]
    out_colours = sorted({c for o in outs for c in colours(o)})
    in_colours = sorted({c for i in ins for c in colours(i)})
    ups, downs, tiles, ratios = {2, 3}, {2, 3}, set(), set()
    from fractions import Fraction
    for i, o in train:
        (h, w), (H, W) = i.shape, o.shape
        fh, fw = Fraction(H, h), Fraction(W, w)
        if (fh, fw) != (1, 1):
            ratios.add(((fh.numerator, fh.denominator), (fw.numerator, fw.denominator)))
        if H % h == 0 and W % w == 0:
            a, b = H // h, W // w
            if a == b and a > 1:
                ups.add(a)
            if (a, b) != (1, 1):
                tiles.add((a, b))
        if h % H == 0 and w % W == 0 and h // H == w // W and h // H > 1:
            downs.add(h // H)
    return {"out_colours": out_colours, "in_colours": in_colours,
            "scales_up": sorted(ups), "scales_down": sorted(downs), "tiles": sorted(tiles),
            "ratios": sorted(ratios)}


def _colour_map(grids, targets):
    """One consistent recolouring that turns every grid into its target, or None."""
    m = {}
    for g, t in zip(grids, targets):
        if g.shape != t.shape:
            return None
        for a, b in zip(g.ravel().tolist(), t.ravel().tolist()):
            if m.setdefault(a, b) != b:
                return None
    if all(a == b for a, b in m.items()):
        return None
    return m


def run(program, g):
    for name, p in program:
        if g is None:
            return None
        if name == "cells":
            g = cells.apply(p, g)
            continue
        if name == "things":
            g = objects.apply(p, g)
            continue
        if name == "marks":
            g = objects.apply_marks(p, g)
            continue
        if name == "pick":
            g = objects.apply_pick(p, g)
            continue
        if name == "moves":
            g = objects.apply_moves(p, g)
            continue
        if name == "symmetry":
            g = symmetry.apply(p, g)
            continue
        if name == "copies":
            g = objects.apply_copies(p, g)
            continue
        if name == "gaps":
            g = objects.apply_gaps(p, g)
            continue
        if name == "summary":
            g = summary.apply(p, g)
            continue
        if name == "tiles":
            g = tiles.apply(p, g)
            continue
        if name == "colourmap":
            g = np.vectorize(lambda v: p.get(int(v), int(v)), otypes=[np.int8])(g)
            continue
        f = _OPS[name]
        try:
            g = f(g, p)
        except (ValueError, IndexError):
            return None
        if g is None or g.size == 0 or g.shape[0] > 30 or g.shape[1] > 30:
            return None
    return g


_OPS = {}


def show(program):
    out = []
    for name, p in program:
        if name == "colourmap":
            out.append("recolour " + ", ".join(f"{a}→{b}" for a, b in sorted(p.items()) if a != b))
        elif name == "cells":
            out.append(cells.describe(p))
        elif name == "things":
            out.append(objects.describe(p))
        elif name == "marks":
            out.append(objects.describe_marks(p))
        elif name == "pick":
            out.append(objects.describe_pick(p))
        elif name == "moves":
            out.append(objects.describe_moves(p))
        elif name == "symmetry":
            out.append(symmetry.describe(p))
        elif name == "copies":
            out.append(objects.describe_copies(p))
        elif name == "gaps":
            out.append(objects.describe_gaps(p))
        elif name == "summary":
            out.append(summary.describe(p))
        elif name == "tiles":
            out.append(tiles.describe(p))
        elif name.startswith("block") and LIBRARY[0]:
            from . import library
            out.append(library.show_use(LIBRARY[0][int(name[5:]) - 1], p))
        else:
            out.append(name if p is None else f"{name}({p})")
    return " ▸ ".join(out) if out else "identity"


def length(program):
    """Description length: one per operation, plus what a learned table or recolouring
    must spell out (the shortest description wins, as everywhere in Ultron)."""
    total = 0.0
    for name, p in program:
        if name == "colourmap":
            total += 0.5 * sum(1 for a, b in p.items() if a != b)
        elif name == "cells":
            fs, table = p
            total += 1 + 0.5 * len(fs) * sum(1 for k, v in table.items() if k[0] != v)
        elif name == "things":
            total += objects.length(p)
        elif name == "marks":
            total += objects.marks_length(p)
        elif name == "pick":
            total += objects.pick_length(p)
        elif name == "moves":
            total += objects.moves_length(p)
        elif name == "symmetry":
            total += symmetry.length(p)
        elif name == "copies":
            total += objects.copies_length(p)
        elif name == "gaps":
            total += objects.gaps_length(p)
        elif name == "summary":
            total += summary.length(p)
        elif name == "tiles":
            total += tiles.length(p)
        else:
            total += 1
    return total


def task_background(train):
    vals = np.concatenate([g.ravel() for pair in train for g in pair])
    counts = np.bincount(vals.astype(np.int64), minlength=10)
    return int(np.argmax(counts))


def solve(train, budget=BUDGET, max_depth=MAX_DEPTH, want=2):
    """Programs that explain every training pair, shortest description first."""
    from . import grid
    grid.TASK_BACKGROUND[0] = task_background(train)
    grid._SEEN.clear()
    found, spent = _search(train, budget, max_depth, want)
    order = sorted(range(len(found)), key=lambda i: (length(found[i]), i))
    return [found[i] for i in order], spent


GUIDE = [None]          # intuition (guide.py), when one has been learned and switched on
INTUITION = [None]      # intuition.py: which half-built programs to expand first
RECORD = [None]         # when a list: every one-step program and how it looked (to learn)
FIRST = [None]          # operations spent when the first searched program was found
LEARNED = {"colourmap", "cells", "things", "marks", "pick", "moves", "symmetry", "copies",
           "gaps", "summary", "tiles"}
LIBRARY = [None]        # building blocks Ultron learned itself (library.py), when switched on


def _search(train, budget, max_depth, want):
    ctx = context(train)
    reg = O.registry(ctx)
    if GUIDE[0] is not None:
        from . import guide
        reg = guide.order(GUIDE[0], train, reg)
    if LIBRARY[0]:
        from . import library
        reg = library.operations(LIBRARY[0], ctx) + reg     # its own blocks first
    for name, f, _ in reg:
        _OPS[name] = f
    ins = [i for i, _ in train]
    targets = [o for _, o in train]
    goal = tuple(key(o) for o in targets)
    found, spent = [], 0
    m = _colour_map(ins, targets)
    if m is not None:
        found.append((("colourmap", m),))
    rule = cells.learn(ins, targets)
    if rule is not None:
        found.append((("cells", rule),))
    for law in objects.rivals(ins, targets):
        found.append((("things", law),))
    marks = objects.learn_marks(ins, targets)
    if marks is not None:
        found.append((("marks", marks),))
    pick = objects.learn_pick(ins, targets)
    if pick is not None:
        found.append((("pick", pick),))
    moves = objects.learn_moves(ins, targets)
    if moves is not None:
        found.append((("moves", moves),))
    for law in symmetry.rivals(ins, targets, ctx["in_colours"]):
        found.append((("symmetry", law),))
    copies = objects.learn_copies(ins, targets)
    if copies is not None:
        found.append((("copies", copies),))
    gaps = objects.learn_gaps(ins, targets)
    if gaps is not None:
        found.append((("gaps", gaps),))
    summ = summary.learn(ins, targets)
    if summ is not None:
        found.append((("summary", summ),))
    arrangement = tiles.learn(ins, targets)
    if arrangement is not None:
        found.append((("tiles", arrangement),))
    frontier = [((), ins)]
    seen = {tuple(key(g) for g in ins)}
    cache = {}
    looks = {(): None}
    if INTUITION[0] is not None or RECORD[0] is not None:
        from . import intuition as I
        looks[()] = I._look(ins, targets)
    for depth in range(1, max_depth + 1):
        best = sorted(length(f) for f in found)
        if len(best) >= want and best[want - 1] <= depth:
            return found, spent     # nothing this long can be shorter than what's found
        nxt = []
        for prog, grids in frontier:
            for name, f, p in reg:
                spent += len(grids)
                if spent > budget:
                    return found, spent
                outs = []
                for g in grids:
                    ck = (name, repr(p), key(g))
                    if ck in cache:
                        r = cache[ck]
                    else:
                        try:
                            r = f(g, p)
                        except (ValueError, IndexError):
                            r = None
                        cache[ck] = r
                    if r is None or r.size == 0 or r.shape[0] > 30 or r.shape[1] > 30:
                        outs = None
                        break
                    outs.append(r)
                if outs is None:
                    continue
                k = tuple(key(g) for g in outs)
                if k in seen:
                    continue
                seen.add(k)
                p2 = prog + ((name, p),)
                if k == goal:
                    found.append(p2)
                    if FIRST[0] is None:
                        FIRST[0] = spent
                else:
                    cm = _colour_map(outs, targets)
                    if cm is not None:
                        found.append(p2 + (("colourmap", cm),))
                    elif depth == 1:
                        rule = cells.learn(outs, targets)
                        if rule is not None:
                            found.append(p2 + (("cells", rule),))
                        for law in objects.rivals(outs, targets):
                            found.append(p2 + (("things", law),))
                        marks = objects.learn_marks(outs, targets)
                        if marks is not None:
                            found.append(p2 + (("marks", marks),))
                        pick = objects.learn_pick(outs, targets)
                        if pick is not None:
                            found.append(p2 + (("pick", pick),))
                if depth < max_depth or RECORD[0] is not None:
                    if looks[()] is not None:
                        f, now = I.features(outs, targets, looks[prog], depth, name)
                        looks[p2] = now
                        if RECORD[0] is not None and depth == 1:
                            RECORD[0].append((p2, f))
                        score = I.Model.score(INTUITION[0], f) if INTUITION[0] else 0.0
                    else:
                        score = 0.0
                    if depth < max_depth:
                        nxt.append((p2, outs, score))
        # intuition: the most promising half-built programs are expanded first (a stable
        # sort, so without intuition the order is unchanged)
        if INTUITION[0] is not None:
            nxt.sort(key=lambda n: -n[2])
        frontier = [(p, o) for p, o, _ in nxt]
    return found, spent


def predict(train, tests, **kw):
    """Up to two different answers for each test input, from the shortest programs."""
    programs, spent = solve(train, **kw)      # (sets the task's background for run())
    attempts = [[] for _ in tests]
    used = []
    for prog in programs:
        preds = [run(prog, t) for t in tests]
        if any(p is None for p in preds):
            continue
        if any(len(a) >= 2 for a in attempts):
            break
        new = False
        for a, p in zip(attempts, preds):
            if all(not np.array_equal(p, q) for q in a):
                a.append(p)
                new = True
        if new:
            used.append(prog)
    return attempts, used, spent
