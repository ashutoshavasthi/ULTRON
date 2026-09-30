"""The hypothesis engine for discrete laws.

Given every experience of one kind (inputs -> outcome), find the *smallest*
program that reproduces all of them. Programs are written smallest first, and
two programs that behave identically on everything seen so far count as one,
so the first match is guaranteed to be a shortest explanation (Occam's razor /
minimum description length). Nothing here is random.
"""

from . import dsl
from .dsl import BOOL, INT, Overflow, apply_step


class SearchResult:
    def __init__(self, expr, steps, exhausted):
        self.expr = expr          # the law, or None
        self.steps = steps        # how many candidate programs were considered
        self.exhausted = exhausted  # True if the search hit its size/effort limit


def _vec_iter(F, nvec, xvec, tvec, library):
    out = []
    for i, (n, acc) in enumerate(zip(nvec, xvec)):
        if n > dsl.MAX_ITER:
            return None
        t = tvec[i] if tvec is not None else None
        try:
            for _ in range(n):
                acc = apply_step(F, acc, t, library)
        except Overflow:
            return None
        out.append(acc)
    return tuple(out)


def _vec_call(name, avec, bvec, library):
    out = []
    try:
        for a, b in zip(avec, bvec):
            v = library.call(name, a, b)
            if v > dsl.MAX_VALUE:
                return None
            out.append(v)
    except Overflow:
        return None
    return tuple(out)


def synthesize(inputs, targets, var_types, out_type, library, consts=(0, 1),
               max_size=7, max_bank=60000):
    """Search for the smallest program mapping each inputs[i] to targets[i]."""
    with dsl.limits(20000, 10 ** 7):
        return _synthesize(inputs, targets, var_types, out_type, library, consts,
                           max_size, max_bank)


def _synthesize(inputs, targets, var_types, out_type, library, consts, max_size, max_bank):
    target = tuple(targets)
    names = sorted(var_types)
    bank = {INT: {}, BOOL: {}}          # type -> size -> [(expr, vec)]
    seen = {INT: set(), BOOL: set()}
    state = {"steps": 0, "total": 0}

    def consider(expr, typ, vec, s):
        state["steps"] += 1
        if vec is None or vec in seen[typ]:
            return False
        seen[typ].add(vec)
        bank[typ].setdefault(s, []).append((expr, vec))
        state["total"] += 1
        return typ == out_type and vec == target

    def at(typ, s):
        return bank[typ].get(s, [])

    libs = library.binary_int_laws()

    # size 1: what it perceives, and the constants it knows
    for n in names:
        typ = var_types[n]
        expr = ("var", n)
        if consider(expr, typ, tuple(inp[n] for inp in inputs), 1):
            return SearchResult(expr, state["steps"], False)
    for c in consts:
        typ = BOOL if isinstance(c, bool) else INT
        expr = ("const", c)
        if consider(expr, typ, tuple(c for _ in inputs), 1):
            return SearchResult(expr, state["steps"], False)
    for c in (True, False):
        if out_type == BOOL and consider(("const", c), BOOL, tuple(c for _ in inputs), 1):
            return SearchResult(("const", c), state["steps"], False)

    for s in range(2, max_size + 1):
        # one-argument building blocks
        for e, v in list(at(INT, s - 1)):
            if consider(("succ", e), INT, tuple(x + 1 for x in v), s):
                return SearchResult(("succ", e), state["steps"], False)
            if consider(("pred", e), INT, tuple(x - 1 if x > 0 else 0 for x in v), s):
                return SearchResult(("pred", e), state["steps"], False)
        for e, v in list(at(BOOL, s - 1)):
            if consider(("not", e), BOOL, tuple(not x for x in v), s):
                return SearchResult(("not", e), state["steps"], False)

        # two-argument building blocks
        for i in range(1, s - 1):
            j = s - 1 - i
            for a, av in list(at(INT, i)):
                for b, bv in list(at(INT, j)):
                    if consider(("eq", a, b), BOOL, tuple(x == y for x, y in zip(av, bv)), s):
                        return SearchResult(("eq", a, b), state["steps"], False)
                    if consider(("lt", a, b), BOOL, tuple(x < y for x, y in zip(av, bv)), s):
                        return SearchResult(("lt", a, b), state["steps"], False)
                    for law in libs:
                        expr = ("call", law.name, a, b)
                        if consider(expr, INT, _vec_call(law.name, av, bv, library), s):
                            return SearchResult(expr, state["steps"], False)
            for a, av in list(at(BOOL, i)):
                for b, bv in list(at(BOOL, j)):
                    if consider(("and", a, b), BOOL, tuple(x and y for x, y in zip(av, bv)), s):
                        return SearchResult(("and", a, b), state["steps"], False)

        # repetition: "start at x and do F, n times"
        step_options = [(("succ",), 1, None), (("pred",), 1, None)]
        for law in libs:
            for ts in range(1, s - 3):
                for t, tv in list(at(INT, ts)):
                    step_options.append((("call", law.name, t), 1 + ts, tv))
        for F, f_cost, tv in step_options:
            rest = s - 1 - f_cost
            for ns in range(1, rest):
                xs = rest - ns
                for n, nv in list(at(INT, ns)):
                    for x, xv in list(at(INT, xs)):
                        expr = ("iter", F, n, x)
                        if consider(expr, INT, _vec_iter(F, nv, xv, tv, library), s):
                            return SearchResult(expr, state["steps"], False)
        if state["total"] > max_bank:
            return SearchResult(None, state["steps"], True)
    return SearchResult(None, state["steps"], True)
