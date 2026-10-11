"""Compression: noticing a pattern in its own laws, and predicting from it.

Ultron looks at the *shape* of the laws in its library. One of them has the form

    L2(a, n) = repeat n times [ L1(·, a) ] starting from e

where e is L1's "nothing" (L1(e, a) = a). For example, groups ("times") is merge
("plus") repeated, starting from 0. Ultron abstracts that as a law-maker, REPEAT:
from any law it can build "that law, repeated". Applying REPEAT to its most
repeated law predicts a law it has never experienced (for groups: repeated
groups, starting from 1). It keeps that as a *prediction*, not a building
block, until the world confirms it.

The pattern also tells it when to stop. If a law isn't symmetric (L(2,3) ≠
L(3,2)), "repeat it" can mean two different things, and nothing it knows says
which. Then it says so instead of guessing.
"""

from .dsl import INT, Law, Overflow, show

SAMPLES = range(0, 5)


def _ladder_step(law):
    """(lower law, amount param, count param, start) if law = REPEAT(lower), else None."""
    e = law.expr
    if (len(law.params) == 2 and e[0] == "iter" and e[1][0] == "call"
            and e[1][2][0] == "var" and e[2][0] == "var" and e[3][0] == "const"
            and {e[1][2][1], e[2][1]} == set(law.params)):
        return e[1][1], e[1][2][1], e[2][1], e[3][1]
    return None


def _nothing(brain, law_name):
    """The value e with law(e, a) = a for every a tried: the law's 'nothing'."""
    for e in range(0, 11):
        try:
            if all(brain.library.call(law_name, e, a) == a for a in SAMPLES):
                return e
        except Overflow:
            continue
    return None


def _symmetric(brain, law_name):
    try:
        return all(brain.library.call(law_name, x, y) == brain.library.call(law_name, y, x)
                   for x in SAMPLES for y in SAMPLES)
    except Overflow:
        return False


def look_for_ladders(brain):
    """Find REPEAT in the library; predict the next law; note where it must stop."""
    if not brain.compress:
        return None
    lib = brain.library
    steps = {}
    for law in lib.binary_int_laws():
        found = _ladder_step(law)
        if found and brain.trusts(law.name) and found[0] in lib and \
                _nothing(brain, found[0]) == found[3]:
            steps[law.name] = found
    if not steps:
        return None
    record = brain.inventions.setdefault("ladder", {
        "shape": "law-maker", "primitives": [], "lesson": brain.lesson, "rungs": [],
        "predicted": [], "stops_at": None, "story": ""})
    record["evidence"] = len(steps)
    for upper, (lower, a, n, e) in sorted(steps.items()):
        if upper not in record["rungs"]:
            record["rungs"].append(upper)
            brain.note("reflect", f"'{upper}' is '{lower}' repeated: {upper}({a}, {n}) = repeat "
                                  f"{n} times [{lower}(·, {a})] starting from {e}, which is "
                                  f"'{lower}''s nothing ({lower}({e}, x) = x)")
    # climb: the highest trusted law that isn't below another one
    lows = {lower for lower, *_ in steps.values()}
    tops = [name for name in steps if name not in lows]
    # a confirmed prediction is itself a rung
    for name in list(record["predicted"]):
        law = lib.get(name)
        if law is not None and not law.provenance.get("predicted") and name not in tops:
            tops.append(name)
    for top in sorted(tops):
        if any(lib.get(p) and lib.get(p).expr[1][1] == top for p in record["predicted"]):
            continue
        if record["stops_at"] == top:
            continue
        if not _symmetric(brain, top):
            record["stops_at"] = top
            story = (f"Repeating '{top}' could mean two different things: {top}(2, 3) is not "
                     f"{top}(3, 2), so I can't tell which input to feed back in. The REPEAT "
                     f"pattern stops telling me what comes next here, so I won't guess.")
            brain.note("reflect", story)
            record["story"] += " " + story
            continue
        e = _nothing(brain, top)
        if e is None:
            continue
        name = f"repeated_{top}"
        if name in lib:
            continue
        law = Law(name, ["amount", "times"],
                  ("iter", ("call", top, ("var", "amount")), ("var", "times"), ("const", e)),
                  INT, {"lesson": brain.lesson, "predicted": True, "size": 5})
        lib.add(law)
        record["predicted"].append(name)
        lower = steps[top][0] if top in steps else None
        seen = len(steps)
        story = (f"'{top}' is " + (f"'{lower}' repeated" if lower else "a law made by repeating")
                 + f" (I have seen this shape {seen} time{'s' if seen > 1 else ''}). If REPEAT "
                 f"is a general way of making laws, then applied to '{top}' it predicts a law I "
                 f"have never met: {name}(amount, times) = {show(law.expr)}. That is only a "
                 f"guess from a pattern, so I'll keep it as a prediction until the world agrees.")
        brain.note("invent", story)
        record["story"] = (record["story"] + " " + story).strip()
    return record


def seed_predictions(brain, spec):
    """Meeting a new kind of experience with two amounts: keep the predicted laws in
    mind as candidate explanations. They aren't assumed, and experiments aren't designed
    around them; they are checked against the real experiences before any search, and
    only mentioned if they fit."""
    if spec.kind != "program" or spec.out_type != INT or len(spec.inputs) != 2:
        return
    preds = [n for n in brain.inventions.get("ladder", {}).get("predicted", [])
             if brain.library.get(n) and brain.library.get(n).provenance.get("predicted")]
    if not preds:
        return
    x, y = sorted(spec.inputs)
    ideas = []
    for name in preds:
        ideas += [("call", name, ("var", x), ("var", y)), ("call", name, ("var", y), ("var", x))]
    brain.candidates[spec.name] = ideas


def confirm_predictions(brain, expr):
    """A confirmed law built on a predicted one: the prediction was right."""
    if expr[0] == "call":
        law = brain.library.get(expr[1])
        if law is not None and law.provenance.get("predicted"):
            law.provenance["predicted"] = False
            law.provenance["confirmed_in"] = brain.lesson
            brain.note("confirm", f"my predicted law '{expr[1]}' was right: the world does "
                                  f"exactly what REPEAT said it would")
            record = brain.inventions.get("ladder")
            if record is not None:
                record["confirmed"] = record.get("confirmed", 0) + 1


# ------------------------------------------------------------ fractional repeats
FRACTIONAL = "fractional repeats"


def ladder_view(brain, law_name, depth=0):
    """(core ladder law, which input of `law_name` is the amount, which is the count).
    Unfolds laws defined as another law (grow(days, split) = repeated_groups(split, days))."""
    law = brain.library.get(law_name)
    if law is None or depth > 3 or len(law.params) != 2:
        return None
    step = _ladder_step(law)
    if step is not None:
        return law_name, step[1], step[2]
    e = law.expr
    if e[0] == "call" and e[2][0] == "var" and e[3][0] == "var":
        inner = ladder_view(brain, e[1], depth + 1)
        if inner is None:
            return None
        core, amount, count = inner
        inner_law = brain.library.get(e[1])
        mapping = {inner_law.params[0]: e[2][1], inner_law.params[1]: e[3][1]}
        return core, mapping[amount], mapping[count]
    return None


def power(brain, core, base, n):
    """The core ladder law with (amount=base, count=n), whole n, by Ultron's own law."""
    law = brain.library.get(core)
    args = {law.params[0]: None, law.params[1]: None}
    step = _ladder_step(law)
    args[step[1]], args[step[2]] = base, n
    return brain.library.call(core, args[law.params[0]], args[law.params[1]])


def look_for_exponent_laws(brain):
    """Check the laws of repeating, and give 'repeat p/q times' its only consistent meaning."""
    if FRACTIONAL in brain.inventions:
        return None
    record = brain.inventions.get("ladder", {})
    cores = [n for n in record.get("predicted", [])
             if brain.library.get(n) and not brain.library.get(n).provenance.get("predicted")]
    for core in cores:
        times = next((l.name for l in brain.library.binary_int_laws()
                      if brain.library.fast.get(l.name, ("",))[0] == "times"), "groups")
        plus = next((l.name for l in brain.library.binary_int_laws()
                     if brain.library.fast.get(l.name, ("",))[0] == "add"), "merge")
        try:
            ok = all(
                power(brain, core, power(brain, core, a, p), q)
                == power(brain, core, a, brain.library.call(times, p, q))
                and brain.library.call(times, power(brain, core, a, p), power(brain, core, a, q))
                == power(brain, core, a, brain.library.call(plus, p, q))
                for a in range(1, 6) for p in range(0, 4) for q in range(0, 4))
        except Overflow:
            ok = False
        if not ok:
            continue
        story = (f"Two things are always true of my '{core}' law (checked on 80 examples): "
                 f"repeating p times and then that q times is repeating p·q times, and "
                 f"repeating p times and then q more is repeating p+q times. So if 'repeating "
                 f"half a time' means anything, doing it twice must be repeating once. The only "
                 f"meaning that keeps both laws true: repeating p/q times gives the amount whose "
                 f"q-fold repeat equals the p-fold repeat. It may be a pile of pieces, or a "
                 f"number in a gap.")
        inv = {"shape": "extended meaning", "law": core, "primitives": [],
               "lesson": brain.lesson, "story": story}
        brain.inventions[FRACTIONAL] = inv
        brain.note("invent", story)
        brain.library.squaring = True
        brain.note("reflect", "the same law lets me repeat faster: to repeat 2k times, repeat "
                              "k times and then do that twice (squaring)")
        return inv
    return None


def fractional_side(brain, law_name, base, count, goal):
    """Is repeating `count` (= c/d) times too little (-1), exact (0) or too much (1),
    compared with `goal`? By the laws of repeating: base^(c/d) vs goal  <=>  base^c vs
    goal^d (for amounts above zero and a law that grows with the count)."""
    from . import amounts
    view = ladder_view(brain, law_name)
    if view is None or FRACTIONAL not in brain.inventions:
        return None
    core = view[0]
    c, d = count            # no need to simplify: base^c vs goal^d works for any c/d
    if base[0] <= 0 or goal[0] <= 0 or d <= 0:
        return None
    def rep(x, n):
        # repeating times on k/n multiplies the counts and the kinds of piece separately
        # (that is how its times law works on amounts), so work on each as whole numbers,
        # which its column method does quickly and remembers
        return (power(brain, core, x[0], n), power(brain, core, x[1], n))

    if c >= 0:
        left = rep(base, c)
    else:
        # repeating below zero times is undoing: one over the repeat (k/n -> n/k)
        up = rep(base, -c)
        left = None if up[0] == 0 else ((up[1], up[0]) if up[0] > 0 else (-up[1], -up[0]))
    right = rep(goal, d)
    if left is None or right is None:
        return None
    c1, c2, _ = amounts.common(brain, left, right)
    return c1 - c2


def unknown_is_count(brain, law_name, order, unknown_first):
    """In 'law(?, known)' / 'law(known, ?)', is the unknown the number of repeats of the
    law whose fractional repeats Ultron had to give a meaning to? (For times, a fraction
    of a group already means pieces of cake, so this doesn't apply there.)"""
    view = ladder_view(brain, law_name)
    inv = brain.inventions.get(FRACTIONAL)
    if view is None or inv is None or view[0] != inv["law"]:
        return False
    law = brain.library.get(law_name)
    first = law.params[0] if order == "xy" else law.params[1]
    second = law.params[1] if order == "xy" else law.params[0]
    return (first if unknown_first else second) == view[2]


def fractional_power(brain, law_name, base, count):
    """law(amount=base, count=p/q) by its only consistent meaning: the amount whose
    q-fold repeat equals the p-fold repeat. Returns ("exact", amount), ("gap", Gap)
    or None."""
    from . import amounts, gaps
    view = ladder_view(brain, law_name)
    inv = brain.inventions.get(FRACTIONAL)
    if view is None or inv is None or view[0] != inv["law"] or base[0] < 0:
        return None
    core = view[0]
    p, q = amounts.simplest(brain, count)
    target = amounts.apply_law(brain, core, base, (p, 1))
    if target is None:
        return None
    core_law = brain.library.get(core)
    amount_first = _ladder_step(core_law)[1] == core_law.params[0]
    exact = amounts.solve(brain, core, "xy", (q, 1), target, amount_first)
    if exact is not None and exact[0] >= 0:
        return ("exact", exact)
    return ("gap", gaps.Gap(core, "xy", (q, 1), target, amount_first))
