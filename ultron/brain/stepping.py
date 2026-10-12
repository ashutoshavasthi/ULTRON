"""Explaining a law by stepping: when no short program explains f(x, y) directly, look
at how the outcome changes when x goes up by one.

    f(x + 1, y) = step(f(x, y), y)        f(0, y) = start(y)

so f is "start at start(y) and take the step x times": ("iter", ("call", step, y), x,
start). The step is found by the ordinary law search. If no short step fits every case,
Ultron looks for the rule that holds most of the time, then for when it doesn't hold,
then for what happens instead: ite(when, instead, rule). Each part is a shortest
program; the whole is checked on every experience. Nothing here knows any particular
law: it is how Ultron found "MODULO" in Engc (lesson 100), as it found clock numbers
by watching a wheel tick.

Afterwards it reflects on the step: if, for every setting t it can imagine, t steps
always come back to where they started, the step is a cycle whose length is its own
setting, so only the steps after whole turns matter (dsl.iterate).
"""

from .dsl import BOOL, INT, Law, safe_evaluate, show, size
from .synth import synthesize

SETTINGS = (3, 5, 7, 8)      # settings of y it sweeps (spread out), each once round
MAJORITY = 4                 # the usual rule may be wrong on at most 1 in 4 cases


def _rename(expr, old, new):
    if not isinstance(expr, tuple):
        return expr
    if expr == ("var", old):
        return ("var", new)
    return tuple(_rename(e, old, new) for e in expr)


def _search(xs, ys, var_types, out_type, library, consts, extra, **kw):
    return synthesize(xs, ys, var_types, out_type, library, consts, extra=extra, **kw)


def find_step(pairs, library, consts, extra):
    """pairs: [((acc, t), next)]. The shortest step law, or one built from a usual rule
    and its exceptions. Returns (expr, how, steps)."""
    xs = [{"acc": a, "t": t} for (a, t), _ in pairs]
    ys = [n for _, n in pairs]
    types = {"acc": INT, "t": INT}
    direct = _search(xs, ys, types, INT, library, consts, extra)
    steps = direct.steps
    if direct.expr is not None:
        return direct.expr, "direct", steps
    usual = _search(xs, ys, types, INT, library, consts, extra,
                    exceptions=len(xs) // MAJORITY, max_size=4)
    steps += usual.steps
    if usual.expr is None or not usual.exceptions:
        return None, "none", steps
    odd = set(usual.exceptions)
    when = _search(xs, [i in odd for i in range(len(xs))], types, BOOL, library, consts, extra)
    steps += when.steps
    if when.expr is None:
        return None, "none", steps
    instead = _search([xs[i] for i in sorted(odd)], [ys[i] for i in sorted(odd)], types,
                      INT, library, consts, extra)
    steps += instead.steps
    if instead.expr is None:
        return None, "none", steps
    expr = ("ite", when.expr, instead.expr, usual.expr)
    if all(safe_evaluate(expr, x, library) == y for x, y in zip(xs, ys)):
        return expr, "rule and exceptions", steps
    return None, "none", steps


def by_stepping(name, outcome, library, consts, extra=(), known=None):
    """outcome(x, y) -> the world's answer (an experiment Ultron runs) or None if it
    fails. known: {(x, y): answer} already seen. Returns (expr, step_law, story, runs)."""
    seen = dict(known or {})
    runs = 0

    def ask(x, y):
        nonlocal runs
        if (x, y) not in seen:
            seen[(x, y)] = outcome(x, y)
            runs += 1
        return seen[(x, y)]

    pairs, starts = [], []
    for t in SETTINGS:
        prev = ask(0, t)
        if not isinstance(prev, int) or isinstance(prev, bool):
            return None, None, None, runs
        starts.append(({"y": t}, prev))
        for x in range(1, t + 2):
            nxt = ask(x, t)
            if not isinstance(nxt, int) or isinstance(nxt, bool):
                return None, None, None, runs
            if ((prev, t), nxt) not in pairs:
                pairs.append(((prev, t), nxt))
            prev = nxt
    step, how, _ = find_step(pairs, library, consts, extra)
    if step is None:
        return None, None, None, runs
    start = synthesize([s for s, _ in starts], [v for _, v in starts], {"y": INT}, INT,
                       library, consts, extra=extra)
    if start.expr is None:
        return None, None, None, runs
    step_law = Law(f"step:{name}", ["acc", "t"], step, INT,
                   {"found_by": "stepping", "how": how, "size": size(step)})
    library.add(step_law)
    expr = ("iter", ("call", step_law.name, ("var", "y")), ("var", "x"), start.expr)
    ok = all(safe_evaluate(expr, {"x": x, "y": y}, library) == v
             for (x, y), v in seen.items() if isinstance(v, int) and not isinstance(v, bool))
    if not ok:
        del library.laws[step_law.name]
        return None, None, None, runs
    # a law about the step: does doing it t times always come back to the start?
    if all(_back_after(step_law.name, t, library) for t in range(1, 13)):
        library.cycles[step_law.name] = "param"
    story = (f"no short law explained '{name}' directly, so I watched it step: raising the "
             f"first number by one does {show(step)} (found as {how}), starting from "
             f"{show(start.expr)}; so '{name}' is: start there and step x times"
             + ("; and t steps always come back to the start, so only the steps after "
                "whole turns matter" if library.cycles.get(step_law.name) == "param" else ""))
    return expr, step_law, story, runs


def _back_after(name, t, library):
    for s in range(t):
        acc = s
        for _ in range(t):
            try:
                acc = library.call(name, acc, t)
            except Exception:  # noqa: BLE001 - imagining failed: not a cycle
                return False
            if acc is None:
                return False
        if acc != s:
            return False
    return True
