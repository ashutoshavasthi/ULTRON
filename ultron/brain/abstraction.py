"""Abstraction sleep: finding the pieces its laws keep sharing.

A confirmed law becomes a building block whole. But laws also share *pieces* that
were never taught as laws of their own: "(x+1)·(y+1)" inside several different laws.
While it sleeps, Ultron lines its laws up against each other (anti-unification: keep
what two programs have in common, put a hole where they differ) to find such pieces.
A piece becomes a new building block only if writing it once and using it everywhere
makes the total description of everything it knows **shorter**: the same minimum
description length rule as everywhere else. Then a law too big to find by search
becomes small enough.

This is the "abstraction sleep" of DreamCoder, done with Ultron's own rule.
"""

from .dsl import INT, Law, size

HOLE = "hole"


def _children(e):
    """(index, child) pairs of a program node that are programs themselves."""
    tag = e[0]
    if tag in ("var", "const", HOLE):
        return []
    if tag == "iter":
        out = [(2, e[2]), (3, e[3])]
        if e[1][0] == "call":
            out.append((("F", 2), e[1][2]))
        return out
    if tag in ("call", "fold", "zip"):
        return [(i, e[i]) for i in range(2, len(e))]
    if tag in ("call1", "map", "len"):
        return [(i, e[i]) for i in range(1 if tag == "len" else 2, len(e))]
    if tag == "filter":
        return [(2, e[2]), (3, e[3])]
    return [(i, e[i]) for i in range(1, len(e))]


def _rebuild(e, kids):
    e = list(e)
    for idx, k in kids.items():
        if isinstance(idx, tuple):
            F = list(e[1])
            F[idx[1]] = k
            e[1] = tuple(F)
        else:
            e[idx] = k
    return tuple(e)


def _head(e):
    """A node without its children: what must agree for two nodes to be 'the same'."""
    kids = dict(_children(e))
    return _rebuild(e, {i: None for i in kids})


def subtrees(e):
    yield e
    for _, c in _children(e):
        yield from subtrees(c)


def anti_unify(a, b, holes):
    """The most specific pattern both programs fit: shared structure kept, a hole wherever
    they differ (the same pair of differing pieces gets the same hole)."""
    if a == b and a[0] != "var" and not any(s[0] == "var" for s in subtrees(a)):
        return a
    if _head(a) == _head(b) and a[0] not in ("var", "const"):
        ka, kb = dict(_children(a)), dict(_children(b))
        return _rebuild(a, {i: anti_unify(ka[i], kb[i], holes) for i in ka})
    key = (a, b)
    if key not in holes:
        holes[key] = (HOLE, len(holes))
    return holes[key]


def _n_holes(p):
    return len({s for s in subtrees(p) if s[0] == HOLE})


def match(pattern, e, binding=None):
    """Does program e fit the pattern? Returns {hole: piece} or None."""
    binding = {} if binding is None else binding
    if pattern[0] == HOLE:
        if pattern in binding:
            return binding if binding[pattern] == e else None
        binding[pattern] = e
        return binding
    if _head(pattern) != _head(e):
        return None
    kp, ke = dict(_children(pattern)), dict(_children(e))
    for i in kp:
        if match(kp[i], ke[i], binding) is None:
            return None
    return binding


def _pattern_size(p):
    """Writing the piece down: its nodes (a hole costs nothing; it is filled at each use)."""
    return sum(1 for s in subtrees(p) if s[0] != HOLE)


def rewrite(e, name, pattern):
    """Use the piece wherever the program fits it (largest first)."""
    b = match(pattern, e)
    if b is not None:
        holes = sorted(b, key=lambda h: h[1])
        args = [rewrite(b[h], name, pattern) for h in holes]
        return ("call", name, *args) if len(args) == 2 else ("call1", name, args[0])
    kids = dict(_children(e))
    if not kids:
        return e
    return _rebuild(e, {i: rewrite(k, name, pattern) for i, k in kids.items()})


def candidates(programs, min_size=3):
    """Patterns shared by pieces of two different programs, with one or two holes."""
    pieces = []
    for i, p in enumerate(programs):
        for s in subtrees(p):
            if size(s) >= min_size:
                pieces.append((i, s))
    found = set()
    for x in range(len(pieces)):
        for y in range(x + 1, len(pieces)):
            (i, a), (j, b) = pieces[x], pieces[y]
            if i == j:
                continue
            pat = anti_unify(a, b, {})
            if pat[0] != HOLE and 1 <= _n_holes(pat) <= 2 and _pattern_size(pat) >= 2:
                found.add(pat)
    return sorted(found, key=repr)


def saving(pattern, programs):
    """How much shorter everything becomes with this piece, minus writing it down."""
    name = "__piece__"
    before = sum(size(p) for p in programs)
    after = sum(size(rewrite(p, name, pattern)) for p in programs)
    return before - after - _pattern_size(pattern)


def sleep(programs, library, max_pieces=3, prefix="piece"):
    """Find pieces worth having; add each to the library as a building block. Returns the
    pieces found [(name, pattern, saving)], best first. The programs are rewritten to use
    them (later pieces may be built from earlier ones)."""
    progs = list(programs)
    found = []
    for k in range(max_pieces):
        best = None
        for pat in candidates(progs):
            sv = saving(pat, progs)
            if sv > 0 and (best is None or sv > best[1]):
                best = (pat, sv)
        if best is None:
            break
        pat, sv = best
        name = f"{prefix}{len([n for n in library.laws if n.startswith(prefix)]) + 1}"
        holes = sorted({s for s in subtrees(pat) if s[0] == HOLE}, key=lambda h: h[1])
        params = [f"x{i + 1}" for i in range(len(holes))]
        expr = _fill(pat, {h: ("var", p) for h, p in zip(holes, params)})
        library.add(Law(name, params, expr, INT, {"abstraction": True, "saving": sv}))
        progs = [rewrite(p, name, pat) for p in progs]
        found.append((name, expr, sv))
    return found, progs


def _fill(p, binding):
    if p[0] == HOLE:
        return binding[p]
    kids = dict(_children(p))
    if not kids:
        return p
    return _rebuild(p, {i: _fill(k, binding) for i, k in kids.items()})
