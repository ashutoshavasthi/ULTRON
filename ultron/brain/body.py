"""Acting to reach a goal: plan with a learned law, act, watch, correct.

A minimal body (Phase 3's stand-in for Phase 4): Ultron can choose an action (how
fast to kick a puck), see the result, and see the goal. To reach a goal it runs its
own law backwards to choose the action. If it misses, it doesn't try at random: the
miss itself is a measurement, so it works out what its law's constant must be HERE
(this floor might not be the floor it learned on) and plans again.
"""

from .invariants import QuantityLaw


def _monomial(values, powers):
    v = 1.0
    for var, p in powers.items():
        v *= values[var] ** p
    return v


def reach(brain, spec_name, action, result, want, act, place=None, tries=2, close=0.1):
    """Choose `action` so that `result` comes out as `want`, using the law for spec_name.
    act(action_value) -> observed result (None if it couldn't be seen). Returns
    {"hit": bool, "tries": n, "trace": [...]}"""
    law = brain.qlaws.get(spec_name)
    if law is None:
        return {"hit": False, "tries": 0, "trace": ["I have no law for this"]}
    if law.kind == "grouped" and place in law.properties:
        c = law.properties[place]
        why = f"my law for {place}: {law.formula()} = {c:.4g}"
    elif law.kind == "global" and brain.law_applies(spec_name, place):
        c = law.constant
        why = f"my law: {law.formula()} = {c:.4g}"
    else:
        known = list(law.properties.values()) if law.kind == "grouped" else [law.constant]
        c = sorted(known)[len(known) // 2]
        why = (f"I've never done this on {place}: my law's form should hold, but maybe not "
               f"its number. A cautious first try, aimed at HALF the distance with the number "
               f"I know ({law.formula()} = {c:.4g}), so that even a slippery floor won't send "
               f"it off the end; what I see will tell me this floor's number")
    cautious = not (law.kind == "grouped" and place in law.properties) and not (
        law.kind == "global" and brain.law_applies(spec_name, place))
    trace = [why]
    for i in range(1, tries + 1):
        aim = want / 2 if cautious and i == 1 else want
        plan = QuantityLaw(law.etype, law.powers, "global", constant=c).solve(
            action, {result: aim})
        if plan is None:
            return {"hit": False, "tries": i, "trace": trace + ["my law can't be run backwards"]}
        got = act(plan)
        if got is None:
            trace.append(f"try {i}: {action} = {plan:.3g}: I lost sight of it")
            return {"hit": False, "tries": i, "trace": trace}
        miss = got - want
        trace.append(f"try {i}: {action} = {plan:.3g}, so {result} should be {aim:.3g}; "
                     f"it was {got:.3g}")
        if abs(miss) <= close:
            return {"hit": True, "tries": i, "trace": trace}
        # the miss is a measurement: what must the law's constant be here?
        c = _monomial({action: plan, result: got}, law.powers)
        if aim != want:
            trace.append(f"so here {law.formula()} = {c:.4g}; now for the mark itself")
        else:
            trace.append(f"missed by {miss:+.3g}; here {law.formula()} must be {c:.4g}, not "
                         f"what I thought; planning again")
    return {"hit": False, "tries": tries, "trace": trace}
