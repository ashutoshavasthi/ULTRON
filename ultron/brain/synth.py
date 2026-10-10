"""The hypothesis engine for discrete laws.

Given every experience of one kind (inputs -> outcome), find the *smallest*
program that reproduces all of them. Programs are written smallest first, and
two programs that behave identically on everything seen so far count as one,
so the first match is guaranteed to be a shortest explanation (Occam's razor /
minimum description length). Nothing here is random.

It can also return *rivals*: other programs, as short or one size longer, that
explain the same experiences but might disagree about situations not yet seen.
Rivals are what make designing an experiment possible.
"""

from . import dsl
from .dsl import BOOL, INT, LIST, Overflow, apply_step


class SearchResult:
    def __init__(self, expr, steps, exhausted, rivals=(), exceptions=()):
        self.expr = expr            # the law, or None
        self.steps = steps          # how many candidate programs were considered
        self.exhausted = exhausted  # True if the search hit its size/effort limit
        self.rivals = list(rivals)  # other explanations of the same experiences
        self.exceptions = list(exceptions)  # experiences the law does NOT fit (indices)


class _Done(Exception):
    pass


MAX_SAME_SIZE = 40
EXCEPTION_COST = 3      # describing one exception (which experience, what it was) costs
                        # about as much as three steps of program


def borrowed(expr):
    """How many laws from the library an explanation borrows."""
    if not isinstance(expr, tuple):
        return 0
    own = 1 if expr[0] in ("call", "call1") else 0
    if expr[0] == "iter" and expr[1][0] in ("call", "call1"):
        own += 1
    return own + sum(borrowed(e) for e in expr[1:] if isinstance(e, tuple))


def _vec_iter(F, nvec, xvec, tvec, library):
    out = []
    for i, (n, acc) in enumerate(zip(nvec, xvec)):
        if F[0] == "call1" and F[1] in library.cycles:
            n = n % library.cycles[F[1]]
        if n < 0 or n > dsl.MAX_ITER:
            return None
        t = tvec[i] if tvec is not None else None
        try:
            for _ in range(n):
                acc = apply_step(F, acc, t, library)
        except Overflow:
            return None
        out.append(acc)
    return tuple(out)


def _vec_call1(name, avec, library):
    out = []
    try:
        for a in avec:
            v = library.call1(name, a)
            if v > dsl.MAX_VALUE:
                return None
            out.append(v)
    except Overflow:
        return None
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


def _each(f, *vecs):
    """f on each example; None if any example can't be worked out."""
    out = []
    try:
        for args in zip(*vecs):
            out.append(f(*args))
    except dsl.Overflow:
        return None
    return tuple(out)


def _lists(s, at, consider, steps, ulibs, libs, library, cost=lambda law: 1):
    from .dsl import RELS, apply_step, keep
    for L, lv in list(at(LIST, s - 1)):
        consider(("len", L), INT, tuple(len(x) for x in lv), s)
    for F, fc in [(F, 1) for F in steps] + [(("call1", l.name), cost(l)) for l in ulibs]:
        for L, lv in list(at(LIST, s - 1 - fc)):
            consider(("map", F, L), LIST,
                     _each(lambda l: tuple(apply_step(F, x, None, library) for x in l), lv), s)
    for law in libs:
        for ts in range(1, s - 1 - cost(law)):
            for t, tv in list(at(INT, ts)):
                F = ("call", law.name, t)
                for L, lv in list(at(LIST, s - 1 - cost(law) - ts)):
                    consider(("map", F, L), LIST, _each(
                        lambda l, tt: tuple(apply_step(F, x, tt, library) for x in l), lv, tv), s)
    for i in range(1, s - 2):
        j = s - 2 - i
        for t, tv in list(at(INT, i)):
            for L, lv in list(at(LIST, j)):
                for rel in RELS:
                    consider(("filter", rel, t, L), LIST, _each(
                        lambda l, tt: tuple(x for x in l if keep(rel, x, tt)), lv, tv), s)
        for law in libs:
            if cost(law) != 1:
                continue
            for L, lv in list(at(LIST, i)):
                for x, xv in list(at(INT, j)):
                    def fold(l, acc, name=law.name):
                        for v in l:
                            acc = dsl.check(library.call(name, acc, v))
                        return acc
                    consider(("fold", law.name, L, x), INT, _each(fold, lv, xv), s)
            for A, av in list(at(LIST, i)):
                for B, bv in list(at(LIST, j)):
                    consider(("zip", law.name, A, B), LIST, _each(
                        lambda a, b, name=law.name: tuple(dsl.check(library.call(name, p, q))
                                                          for p, q in zip(a, b)), av, bv), s)


def synthesize(inputs, targets, var_types, out_type, library, consts=(0, 1),
               max_size=7, max_bank=60000, rivals=0, extra=(), exceptions=0, costs=None):
    """Search for the smallest program mapping each inputs[i] to targets[i].

    extra: invented primitives the brain may use (e.g. "down": one step lower,
    with no floor at zero).
    exceptions: how many experiences may disagree with the law. A law with exceptions
    is described by the program plus a list of the exceptions (EXCEPTION_COST each);
    the shortest whole description wins, so an exact law is preferred unless it is
    much longer. This is how a few wrongly recorded experiences stop being fatal.
    """
    if costs:
        # the budget is measured in the same currency as the description: an unexpected
        # law may cost up to 3 more to name, so the budget grows by that much
        max_size += 3
    with dsl.limits(20000, 10 ** 7):
        if exceptions or len(inputs) <= SAMPLE:
            return _synthesize(inputs, targets, var_types, out_type, library, consts,
                               max_size, max_bank, rivals, tuple(extra), exceptions,
                               costs=costs)
        # imagine candidates on a few examples first; check every example only for the
        # candidates that get those right (a law is still checked on everything)
        n = len(inputs)
        pick = sorted({round(i * (n - 1) / (SAMPLE - 1)) for i in range(SAMPLE)})

        def full(expr):
            for x, y in zip(inputs, targets):
                try:
                    v = dsl.evaluate(expr, x, library)
                except (dsl.Overflow, KeyError, TypeError):
                    return False
                if (tuple(v) if isinstance(v, (list, tuple)) else v) != \
                        (tuple(y) if isinstance(y, (list, tuple)) else y):
                    return False
            return True
        res = _synthesize([inputs[i] for i in pick], [targets[i] for i in pick], var_types,
                          out_type, library, consts, max_size, max_bank, rivals,
                          tuple(extra), 0, verify=full, costs=costs)
        return res


SAMPLE = 8      # examples a candidate is first imagined on


def _synthesize(inputs, targets, var_types, out_type, library, consts, max_size, max_bank,
                n_rivals, extra, n_exceptions=0, verify=None, costs=None):
    target = tuple(targets)
    names = sorted(var_types)
    bank = {INT: {}, BOOL: {}, LIST: {}}    # type -> size -> [(expr, vec)]
    seen = {INT: set(), BOOL: set(), LIST: set()}
    if out_type == LIST:
        target = tuple(tuple(t) for t in target)
    state = {"steps": 0, "total": 0, "matches": [], "first_size": None, "near": None}

    def consider(expr, typ, vec, s):
        state["steps"] += 1
        if vec is None:
            return
        if n_exceptions and typ == out_type and vec != target:
            wrong = [i for i, (x, y) in enumerate(zip(vec, target)) if x != y]
            if len(wrong) <= n_exceptions:
                dl = s + EXCEPTION_COST * len(wrong)
                if state["near"] is None or dl < state["near"][0]:
                    state["near"] = (dl, expr, wrong)
        if typ == out_type and vec == target and (verify is None or verify(expr)):
            state["matches"].append((s, expr))
            if state["first_size"] is None:
                state["first_size"] = s
            # finish the size where the first explanation appeared (to compare all the
            # equally short ones), then only collect enough rivals
            state["least_borrowed"] = min(state.get("least_borrowed", 99), borrowed(expr)) \
                if s == state["first_size"] else state.get("least_borrowed", 99)
            if len(state["matches"]) > n_rivals and (
                    s > state["first_size"] or state["least_borrowed"] == 0):
                raise _Done()   # nothing equally short can borrow fewer laws than none
            if len(state["matches"]) >= MAX_SAME_SIZE:
                raise _Done()
        if vec in seen[typ]:
            return
        seen[typ].add(vec)
        bank[typ].setdefault(s, []).append((expr, vec))
        state["total"] += 1

    def at(typ, s):
        return bank[typ].get(s, [])

    libs, ulibs = library.search_laws()     # laws that behave the same, once
    # what naming each law costs: 1 for all (counting nodes), or less for a law its
    # intuition expects here than for one it doesn't (description length in bits)
    cost = (lambda law: 1) if not costs else (lambda law: costs.get(law.name, 1))
    dear = sorted({cost(l) for l in libs + ulibs} - {1})
    libs1 = [l for l in libs if cost(l) == 1]
    ulibs1 = [l for l in ulibs if cost(l) == 1]
    unary = [("succ", lambda x: x + 1), ("pred", lambda x: x - 1 if x > 0 else 0)]
    steps = [("succ",), ("pred",)]
    if "down" in extra:
        unary.append(("down", lambda x: x - 1))
        steps.append(("down",))

    def result(exhausted):
        m = state["matches"]
        near = state["near"]
        if near is not None and (not m or near[0] < state["first_size"]):
            return SearchResult(near[1], state["steps"], False, [], near[2])
        if not m:
            return SearchResult(None, state["steps"], exhausted)
        shortest = [e for sz, e in m if sz == state["first_size"]]
        # equally short: borrowing a law from the library costs more description (it is
        # one choice among many laws) than a basic step, so prefer fewer borrowed laws
        best = min(shortest, key=lambda e: (borrowed(e), shortest.index(e)))
        rest = [e for _, e in m if e is not best]
        return SearchResult(best, state["steps"], False, rest)

    try:
        # size 1: what it perceives, and the constants it knows
        for n in names:
            if var_types[n] == LIST:
                consider(("var", n), LIST, tuple(tuple(inp[n]) for inp in inputs), 1)
            else:
                consider(("var", n), var_types[n], tuple(inp[n] for inp in inputs), 1)
        for c in consts:
            typ = BOOL if isinstance(c, bool) else INT
            consider(("const", c), typ, tuple(c for _ in inputs), 1)
        if out_type == BOOL:
            for c in (True, False):
                consider(("const", c), BOOL, tuple(c for _ in inputs), 1)

        for s in range(2, max_size + 1):
            if state["near"] is not None and s >= state["near"][0]:
                break       # nothing this long can beat the law-with-exceptions found
            if state["first_size"] is not None and (
                    s > state["first_size"] + 1 or len(state["matches"]) > n_rivals):
                return result(False)
            # one-argument building blocks
            for e, v in list(at(INT, s - 1)):
                for name, f in unary:
                    consider((name, e), INT, tuple(f(x) for x in v), s)
                for law in ulibs1:
                    consider(("call1", law.name, e), INT, _vec_call1(law.name, v, library), s)
            for k in dear:                  # laws it didn't expect cost more to name
                for e, v in list(at(INT, s - k)):
                    for law in ulibs:
                        if cost(law) == k:
                            consider(("call1", law.name, e), INT,
                                     _vec_call1(law.name, v, library), s)
            for e, v in list(at(BOOL, s - 1)):
                consider(("not", e), BOOL, tuple(not x for x in v), s)

            # two-argument building blocks
            for i in range(1, s - 1):
                j = s - 1 - i
                for a, av in list(at(INT, i)):
                    for b, bv in list(at(INT, j)):
                        consider(("eq", a, b), BOOL, tuple(x == y for x, y in zip(av, bv)), s)
                        consider(("lt", a, b), BOOL, tuple(x < y for x, y in zip(av, bv)), s)
                        for law in libs1:
                            consider(("call", law.name, a, b), INT,
                                     _vec_call(law.name, av, bv, library), s)
                for a, av in list(at(BOOL, i)):
                    for b, bv in list(at(BOOL, j)):
                        consider(("and", a, b), BOOL, tuple(x and y for x, y in zip(av, bv)), s)
            for k in dear:
                for i in range(1, s - k):
                    j = s - k - i
                    for a, av in list(at(INT, i)):
                        for b, bv in list(at(INT, j)):
                            for law in libs:
                                if cost(law) == k:
                                    consider(("call", law.name, a, b), INT,
                                             _vec_call(law.name, av, bv, library), s)

            # "if c then a else b" (simple conditions only: size 3 or less)
            for i in range(1, min(3, s - 3) + 1):
                for j in range(1, s - 1 - i):
                    k = s - 1 - i - j
                    for c, cv in list(at(BOOL, i)):
                        for a, av in list(at(INT, j)):
                            for b, bv in list(at(INT, k)):
                                consider(("ite", c, a, b), INT,
                                         tuple(x if q else y for q, x, y in zip(cv, av, bv)), s)

            # rows of things: how many, each one stepped, those below/above/equal to
            # something, everything combined with a law, two rows paired by a law
            if bank[LIST]:
                _lists(s, at, consider, steps, ulibs, libs, library, cost)
                if dear:
                    _lists_dear(s, at, consider, libs, library, cost)

            # repetition: "start at x and do F, n times"
            options = [(F, 1, None) for F in steps] + \
                [(("call1", l.name), cost(l), None) for l in ulibs]
            for law in libs:
                for ts in range(1, s - 2 - cost(law)):
                    for t, tv in list(at(INT, ts)):
                        options.append((("call", law.name, t), cost(law) + ts, tv))
            for F, f_cost, tv in options:
                rest = s - 1 - f_cost
                for ns in range(1, rest):
                    xs = rest - ns
                    for n, nv in list(at(INT, ns)):
                        for x, xv in list(at(INT, xs)):
                            consider(("iter", F, n, x), INT,
                                     _vec_iter(F, nv, xv, tv, library), s)
            if state["total"] > max_bank:
                return result(True)
    except _Done:
        return result(False)
    return result(True)


def _lists_dear(s, at, consider, libs, library, cost):
    """fold and zip with laws that cost more than 1 to name."""
    for law in libs:
        k = cost(law)
        if k == 1:
            continue
        for i in range(1, s - 1 - k):
            j = s - 1 - k - i
            for L, lv in list(at(LIST, i)):
                for x, xv in list(at(INT, j)):
                    def fold(l, acc, name=law.name):
                        for v in l:
                            acc = dsl.check(library.call(name, acc, v))
                        return acc
                    consider(("fold", law.name, L, x), INT, _each(fold, lv, xv), s)
            for A, av in list(at(LIST, i)):
                for B, bv in list(at(LIST, j)):
                    consider(("zip", law.name, A, B), LIST, _each(
                        lambda a, b, name=law.name: tuple(dsl.check(library.call(name, p, q))
                                                          for p, q in zip(a, b)), av, bv), s)
