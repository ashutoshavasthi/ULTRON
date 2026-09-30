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
