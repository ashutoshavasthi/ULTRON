"""Rules about cells: an ordered list of short "if ... then ..." rules, learned from a
task's own examples, that says what colour every cell of the answer takes.

The local law (cells.py) is one table over a few features: it cannot say anything about a
situation it has not seen. Here Ultron describes a cell by many generic things it can
see from where it stands (its colour and its neighbours'; the first colour it meets
looking in each of eight directions; the cell mirrored across the picture; the thing it
belongs to, its size and whether it is the biggest; whether it is shut in; its row and
column), and looks for the shortest list of rules

    if <one or two of these facts hold> then <a colour, or the colour of something it sees>
    otherwise <a default>

that gives every cell of every example exactly its colour. A rule may say "become the
colour you see to the left", so a law found with red and blue also works for green.

Shortest first, and kept honest the way the rest of Ultron is:
- every rule must be right on every cell it fires on (no exceptions);
- the list is grown greedily, the rule that explains most of what is still unexplained
  first, the simplest one when two explain as much;
- a list is believed only if it predicts each example when learned without it
  (leave-one-out), so a list that merely memorises the examples gives no answer.
"""

import numpy as np

from .grid import background, things

DIRS = ((-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
DNAMES = ("up", "down", "left", "right", "ul", "ur", "dl", "dr")
MAX_RULES = 8


def _rays(g, bg):
    """For each direction: the colour of the first non-ground cell seen looking that way
    (-1 if none)."""
    h, w = g.shape
    out = []
    for dr, dc in DIRS:
        ray = np.full((h, w), -1, dtype=np.int16)
        rows = range(h - 1, -1, -1) if dr > 0 else range(h)
        cols = range(w - 1, -1, -1) if dc > 0 else range(w)
        for r in rows:
            for c in cols:
                y, x = r + dr, c + dc
                if 0 <= y < h and 0 <= x < w:
                    ray[r, c] = g[y, x] if g[y, x] != bg else ray[y, x]
        out.append(ray)
    return out


def _shifted(g, dr, dc):
    h, w = g.shape
    out = np.full((h, w), -1, dtype=np.int16)
    ys, ye = max(0, -dr), min(h, h - dr)
    xs, xe = max(0, -dc), min(w, w - dc)
    out[ys:ye, xs:xe] = g[ys + dr:ye + dr, xs + dc:xe + dc]
    return out


def _enclosed(g, bg):
    """Ground cells that cannot reach the edge through ground (4-connected)."""
    h, w = g.shape
    free = g == bg
    reach = np.zeros((h, w), dtype=bool)
    stack = [(r, c) for r in range(h) for c in (0, w - 1) if free[r, c]] + \
            [(r, c) for c in range(w) for r in (0, h - 1) if free[r, c]]
    for r, c in stack:
        reach[r, c] = True
    while stack:
        r, c = stack.pop()
        for dr, dc in DIRS[:4]:
            y, x = r + dr, c + dc
            if 0 <= y < h and 0 <= x < w and free[y, x] and not reach[y, x]:
                reach[y, x] = True
                stack.append((y, x))
    return free & ~reach


def features(g):
    """Two dictionaries of per-cell grids: colours a cell sees (which a rule may also
    copy), and other facts about it."""
    g = np.asarray(g)
    h, w = g.shape
    bg = background(g)
    gi = g.astype(np.int16)
    col = {"colour": gi}
    for name, (dr, dc) in zip(DNAMES, DIRS):
        col["n_" + name] = _shifted(gi, dr, dc)
    for name, ray in zip(DNAMES, _rays(g, bg)):
        col["ray_" + name] = ray
    col["mirror_h"] = gi[:, ::-1]
    col["mirror_v"] = gi[::-1, :]
    col["mirror_hv"] = gi[::-1, ::-1]
    if h == w:
        col["mirror_d"] = gi.T.copy()
    fact = {}
    nb = g != bg
    fact["ground"] = (~nb).astype(np.int16)
    fact["enclosed"] = _enclosed(g, bg).astype(np.int16)
    busy = [(col["n_" + d] != bg) & (col["n_" + d] != -1) for d in DNAMES]
    n4 = sum(b.astype(np.int16) for b in busy[:4])
    n8 = n4 + sum(b.astype(np.int16) for b in busy[4:])
    same8 = sum((col["n_" + d] == gi).astype(np.int16) for d in DNAMES)
    fact["count4"] = n4.astype(np.int16)
    fact["count8"] = n8.astype(np.int16)
    fact["same8"] = same8.astype(np.int16)
    rr, cc = np.indices((h, w))
    fact["row_parity"] = (rr % 2).astype(np.int16)
    fact["col_parity"] = (cc % 2).astype(np.int16)
    fact["row_mod3"] = (rr % 3).astype(np.int16)
    fact["col_mod3"] = (cc % 3).astype(np.int16)
    fact["edge"] = ((rr == 0) | (rr == h - 1) | (cc == 0) | (cc == w - 1)).astype(np.int16)
    fact["row_busy"] = np.repeat(nb.sum(axis=1, keepdims=True) > 0, w, axis=1).astype(np.int16)
    fact["col_busy"] = np.repeat(nb.sum(axis=0, keepdims=True) > 0, h, axis=0).astype(np.int16)
    # the thing (one colour, touching at corners too) a cell belongs to
    size = np.zeros((h, w), dtype=np.int16)
    biggest = np.zeros((h, w), dtype=np.int16)
    border = np.zeros((h, w), dtype=np.int16)
    same_shape = np.zeros((h, w), dtype=np.int16)
    on_box = np.zeros((h, w), dtype=np.int16)
    ts = things(g, bg, diagonal=True)
    if ts:
        sizes = sorted({t.size for t in ts})
        shapes = {}
        for t in ts:
            shapes[(t.patch != bg).tobytes() + bytes(t.patch.shape)] = \
                shapes.get((t.patch != bg).tobytes() + bytes(t.patch.shape), 0) + 1
        for t in ts:
            s = 1 if t.size == sizes[-1] else (-1 if t.size == sizes[0] else 0)
            touches = int(t.r0 == 0 or t.c0 == 0 or t.r1 == h or t.c1 == w)
            k = shapes[(t.patch != bg).tobytes() + bytes(t.patch.shape)]
            for r, c in t.cells:
                size[r, c] = min(t.size, 9)
                biggest[r, c] = s
                border[r, c] = touches
                same_shape[r, c] = min(k, 3)
                on_box[r, c] = int(r in (t.r0, t.r1 - 1) or c in (t.c0, t.c1 - 1))
    fact["size"] = size
    fact["size_rank"] = biggest
    fact["thing_at_edge"] = border
    fact["same_shape"] = same_shape
    fact["on_box_edge"] = on_box
    # the multicolour thing a cell belongs to: its main colour and its other colour
    main = np.full((h, w), -1, dtype=np.int16)
    other = np.full((h, w), -1, dtype=np.int16)
    for t in things(g, bg, diagonal=True, multicolour=True):
        vals, counts = np.unique([g[r, c] for r, c in t.cells], return_counts=True)
        order = sorted(zip(-counts, vals))
        for r, c in t.cells:
            main[r, c] = order[0][1]
            other[r, c] = order[1][1] if len(order) > 1 else -1
    col["thing_main"] = main
    col["thing_other"] = other
    return col, fact


def _cells(grids):
    """Every cell of every grid as one long vector per feature."""
    cols, facts = {}, {}
    for g in grids:
        c, f = features(g)
        for k, v in c.items():
            cols.setdefault(k, []).append(v.ravel())
        for k, v in f.items():
            facts.setdefault(k, []).append(v.ravel())
    n = len(grids)
    cols = {k: np.concatenate(v) for k, v in cols.items() if len(v) == n}
    facts = {k: np.concatenate(v) for k, v in facts.items() if len(v) == n}
    return cols, facts


def _bits(mask):
    """A boolean vector as a Python integer (bit i = cell i): fast and and/or/count."""
    if not mask.size:
        return 0
    v = int.from_bytes(np.packbits(mask[::-1].astype(np.uint8)).tobytes(), "big")
    return v >> (-mask.size % 8)


def _atoms(cols, facts):
    """Every simple fact a rule may test: a feature has a value, or two colours a cell
    sees are the same."""
    atoms = []
    for k in sorted(facts):
        for v in np.unique(facts[k]).tolist():
            atoms.append((("is", k, v), facts[k] == v))
    for k in sorted(cols):
        for v in np.unique(cols[k]).tolist():
            atoms.append((("is", k, v), cols[k] == v))
    names = sorted(cols)
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            m = (cols[a] == cols[b]) & (cols[a] != -1)
            if m.any() and not m.all():
                atoms.append((("same", a, b), m))
    return atoms


def _test(atom, cols, facts):
    kind, a, b = atom
    if kind == "same":
        return (cols[a] == cols[b]) & (cols[a] != -1)
    src = facts if a in facts else cols
    return src[a] == b


def learn_list(grids, targets):
    """The shortest rule list that gives every cell of every target, or None."""
    if any(g.shape != t.shape for g, t in zip(grids, targets)):
        return None
    cols, facts = _cells(grids)
    out = np.concatenate([t.ravel() for t in targets]).astype(np.int16)
    n = out.size
    allbits = (1 << n) - 1
    # what each action gets right: become colour v, or take the colour one sees
    actions = []
    for v in sorted(set(out.tolist())):
        actions.append((("paint", v), _bits(out == v)))
    for k in sorted(cols):
        actions.append((("copy", k), _bits(cols[k] == out)))
    good = dict(actions)
    keep = good[("copy", "colour")]
    if keep == allbits:
        return None
    # the default: the action right on most cells (keeping one's colour wins ties)
    default = max(actions, key=lambda a: (a[1].bit_count(), a[0] == ("copy", "colour")))[0]
    atoms = [(a, _bits(m)) for a, m in _atoms(cols, facts)]
    rules = []
    left = allbits                       # cells no rule has spoken for yet
    while True:
        bad = left & ~good[default]
        if not bad:
            break
        if len(rules) >= MAX_RULES:
            return None
        best = None
        # one fact, then two facts together, for each action that would help
        useful = [(a, gbits) for a, gbits in actions if gbits & bad]
        singles = [(a, m & left) for a, m in atoms if m & bad]
        for act, gbits in useful:
            for atom, m in singles:
                if m & ~gbits:
                    continue
                gain = (m & bad).bit_count()
                cand = (gain, -1, (atom,), act)
                if best is None or cand[:2] > best[:2]:
                    best = cand
        if best is None or best[0] * 4 < bad.bit_count():
            top = sorted(singles, key=lambda x: -(x[1] & bad).bit_count())[:40]
            for act, gbits in useful:
                for i, (a1, m1) in enumerate(top):
                    if not m1 & gbits & bad:
                        continue
                    for a2, m2 in atoms:
                        m = m1 & m2
                        if not m & bad or m & ~gbits:
                            continue
                        gain = (m & bad).bit_count()
                        cand = (gain, -2, (a1, a2), act)
                        if best is None or cand[:2] > best[:2]:
                            best = cand
        if best is None:
            return None
        gain, _, test, act = best
        m = left
        for a in test:
            m &= dict(atoms)[a]
        rules.append((test, act))
        left &= ~m
    return rules, default


def _act(act, cols):
    kind, x = act
    if kind == "paint":
        return np.full(cols["colour"].shape, x, dtype=np.int16)
    return cols[x]


def apply_list(law, g):
    rules, default = law
    cols, facts = _cells([g])
    for kind, a, b in (atom for test, _ in rules for atom in test):
        if (a not in cols and a not in facts) or (kind == "same" and b not in cols):
            return None
    for kind, x in [act for _, act in rules] + [default]:
        if kind == "copy" and x not in cols:
            return None
    n = cols["colour"].size
    out = _act(default, cols).copy()
    done = np.zeros(n, dtype=bool)
    for test, act in rules:
        m = ~done
        for atom in test:
            m &= _test(atom, cols, facts)
        out[m] = _act(act, cols)[m]
        done |= m
    if (out < 0).any():
        return None
    return out.reshape(g.shape).astype(np.int8)


def learn(grids, targets):
    """A rule list, believed only if, learned without each example in turn, it predicts
    that example exactly."""
    law = learn_list(grids, targets)
    if law is None or len(grids) < 2:
        return None
    for i in range(len(grids)):
        rest = [j for j in range(len(grids)) if j != i]
        sub = learn_list([grids[j] for j in rest], [targets[j] for j in rest])
        if sub is None:
            return None
        p = apply_list(sub, grids[i])
        if p is None or not np.array_equal(p, targets[i]):
            return None
    return law


def apply(law, g):
    return apply_list(law, g)


def length(law):
    rules, _ = law
    return 1 + sum(len(test) + 1 for test, _ in rules)


def _say(atom):
    kind, a, b = atom
    return f"{a} is {b}" if kind == "is" else f"{a} = {b}"


def describe(law):
    rules, default = law
    parts = [f"if {' and '.join(_say(a) for a in test)}: {act[0]} {act[1]}"
             for test, act in rules]
    return "cell rules: " + "; ".join(parts) + f"; else {default[0]} {default[1]}"
