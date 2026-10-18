"""The failure lab: break Ultron on purpose, and measure where it breaks.

Each experiment turns one dial (how big the law is, how noisy the data, how many
irrelevant things are measured, how much of the data is wrong, ...) until Ultron
fails, and reports the breakpoint. Nothing here teaches the saved brain anything:
experiments use copies or fresh brains.

Run: python -m ultron stress      (writes reports/failure_lab.md and .json)
"""

import copy
import random
import time

from ..brain import dsl
from ..brain.brain import Brain
from ..brain.dsl import INT, safe_evaluate, show
from ..brain.invariants import search_invariant
from ..brain.memory import Spec
from ..brain.synth import synthesize


def _row(level, outcome, ok, **extra):
    return {"level": level, "outcome": outcome, "ok": bool(ok), **extra}


def _breakpoint(rows):
    for r in rows:
        if not r["ok"]:
            return r["level"]
    return None


def experiment(name, question, dial, rows, note=""):
    return {"name": name, "question": question, "dial": dial, "rows": rows,
            "breakpoint": _breakpoint(rows), "note": note}


# ------------------------------------------------------------------ programs
TARGETS = [
    ("a+b", lambda a, b: a + b),
    ("a·b", lambda a, b: a * b),
    ("a·b+a", lambda a, b: a * b + a),
    ("a·b+a+b", lambda a, b: a * b + a + b),
    ("a²+b", lambda a, b: a * a + b),
    ("(a+b)²", lambda a, b: (a + b) ** 2),
    ("a·b²+a", lambda a, b: a * b * b + a),
    ("a³+b²", lambda a, b: a ** 3 + b * b),
    ("(a+1)(b+2)(a+b)", lambda a, b: (a + 1) * (b + 2) * (a + b)),
]


def _pairs(rng, n, hi=9):
    return [{"a": rng.randint(0, hi), "b": rng.randint(0, hi)} for _ in range(n)]


def _check(expr, f, library, rng):
    if expr is None:
        return False
    test = _pairs(rng, 40, 30)
    return all(safe_evaluate(expr, x, library) == f(x["a"], x["b"]) for x in test)


def program_size(brain):
    """How big a law can its program search find (with everything it already knows)?"""
    rng = random.Random(1)
    lib = copy.deepcopy(brain.library)
    rows = []
    for label, f in TARGETS:
        xs = _pairs(rng, 20)
        t = time.time()
        res = synthesize(xs, [f(x["a"], x["b"]) for x in xs], {"a": INT, "b": INT}, INT, lib)
        ok = _check(res.expr, f, lib, rng)
        rows.append(_row(label, show(res.expr) if res.expr else "nothing found", ok,
                         steps=res.steps, seconds=round(time.time() - t, 2)))
    return experiment("program size", "How big a law can it find by search?",
                      "the law's size", rows,
                      "Search is size-ordered and exhaustive: cost grows exponentially "
                      "with the size of the law.")


def _unfold(expr, library):
    """A program with every learned piece written out in full: its size in the pieces
    Ultron already had."""
    from ..brain.dsl import Law  # noqa: F401
    tag = expr[0]
    if tag in ("call", "call1") and library.get(expr[1]) is not None and \
            library.get(expr[1]).provenance.get("abstraction"):
        law = library.get(expr[1])
        args = [_unfold(a, library) for a in expr[2:]]
        return _subst(law.expr, dict(zip(law.params, args)), library)
    if tag in ("var", "const"):
        return expr
    if tag == "iter":
        return expr[:2] + tuple(_unfold(e, library) for e in expr[2:])
    if tag in ("call", "call1"):
        return expr[:2] + tuple(_unfold(e, library) for e in expr[2:])
    return (tag,) + tuple(_unfold(e, library) if isinstance(e, tuple) else e for e in expr[1:])


def _subst(expr, env, library):
    if expr[0] == "var":
        return env.get(expr[1], expr)
    if expr[0] == "const":
        return expr
    if expr[0] in ("call", "call1", "iter"):
        return _unfold(expr[:2] + tuple(_subst(e, env, library) for e in expr[2:]), library)
    return (expr[0],) + tuple(_subst(e, env, library) if isinstance(e, tuple) else e
                              for e in expr[1:])


def library_learning(brain):
    """S1: practise a family of laws that share a piece never taught on its own; sleep on
    them (find the pieces worth having); then laws far beyond the search's reach."""
    from ..brain import abstraction
    from ..brain.dsl import size
    rng = random.Random(15)
    S = lambda x, y: (x + 1) * (y + 1)
    T = lambda x, y: (x + 1) * (y + 2)
    practice = [lambda a, b: S(a, b) + a, lambda a, b: S(a, b) - b,
                lambda a, b: S(a + 1, b), lambda a, b: S(a, b) * a,
                lambda a, b: S(a, b) + b]
    held_out = [("S(S(a,b),a)+S(a,b)", lambda a, b: S(S(a, b), a) + S(a, b)),
                ("S(S(a,b),S(a,a))", lambda a, b: S(S(a, b), S(a, a))),
                ("S(S(a,b),S(b,b))", lambda a, b: S(S(a, b), S(b, b))),
                ("S(S(a,b),S(a,b))+a", lambda a, b: S(S(a, b), S(a, b)) + a),
                # asymmetric, so no shortcut through "square": 12+ pieces written out
                ("S(T(a,b),T(b,a))", lambda a, b: S(T(a, b), T(b, a))),
                ("T(T(a,b),T(b,a))", lambda a, b: T(T(a, b), T(b, a)))]
    lib = copy.deepcopy(brain.library)
    solved = []
    for f in practice:
        xs = _pairs(rng, 20)
        res = synthesize(xs, [f(x["a"], x["b"]) for x in xs], {"a": INT, "b": INT}, INT, lib)
        if res.expr is not None:
            solved.append(res.expr)
    pieces, _ = abstraction.sleep(solved, lib)
    rows = [_row(f"practice: {len(solved)} of {len(practice)} laws found; sleep",
                 "; ".join(f"{n} = {show(e)} (saves {sv})" for n, e, sv in pieces) or
                 "no piece worth having", bool(pieces))]
    plain = copy.deepcopy(brain.library)
    for label, f in held_out:
        xs = _pairs(rng, 20)
        ys = [f(x["a"], x["b"]) for x in xs]
        t = time.time()
        res = synthesize(xs, ys, {"a": INT, "b": INT}, INT, lib)
        sec = time.time() - t
        ok = res.expr is not None and _check(res.expr, f, lib, rng) and sec < 60
        full = size(_unfold(res.expr, lib)) if res.expr is not None else None
        base = synthesize(xs, ys, {"a": INT, "b": INT}, INT, plain).expr
        rows.append(_row(label, (show(res.expr) if res.expr else "nothing found") +
                         (f" — {full} pieces written out" if full else ""), ok,
                         seconds=round(sec, 1), size_written_out=full,
                         without_pieces=show(base) if base else "nothing found"))
    return experiment("library learning", "After sleeping on laws that share a piece nobody "
                      "taught it, does it find laws bigger than its search can reach?",
                      "held-out law", rows, "Its search alone stops at 7 pieces. The held-out "
                      "laws are compositions of the family's pieces (S = (x+1)(y+1), T = "
                      "(x+1)(y+2)); S1 asks for laws of 12 pieces written out, within 60 s.")


def intuition_prior(brain):
    """S2, intuition alone: description length in bits given what its intuition expects
    (a law it expects is cheap to name). Does that cut search, without losing laws or
    choosing worse ones? Held-out: the lab's laws and dreams from an unseen seed."""
    from ..brain import intuition
    from ..brain.dsl import size
    model = intuition.learn(brain.library, seed=0)
    rng = random.Random(7)
    tasks = []
    for label, f in TARGETS[:-1]:
        xs = _pairs(rng, 20)
        tasks.append((label, xs, [f(x["a"], x["b"]) for x in xs]))
    drng = random.Random(12345)
    while len(tasks) < len(TARGETS) - 1 + 30:
        d = intuition.dream(brain.library, drng)
        if d is not None:
            tasks.append(("dream", d[1], d[2]))
    plain_steps = prior_steps = lost = worse = 0
    for label, xs, ys in tasks:
        p = synthesize(xs, ys, {"a": INT, "b": INT}, INT, brain.library)
        c = intuition.costs(model, xs, ys, ["a", "b"], brain.library)
        q = synthesize(xs, ys, {"a": INT, "b": INT}, INT, brain.library, costs=c)
        plain_steps += p.steps
        prior_steps += q.steps
        lost += p.expr is not None and q.expr is None
        worse += p.expr is not None and q.expr is not None and size(q.expr) > size(p.expr)
    ratio = plain_steps / max(1, prior_steps)
    rows = [_row(f"{len(tasks)} held-out laws (lab laws and unseen dreams)",
                 f"search {ratio:.1f}x less with the prior; {lost} lost, {worse} longer",
                 ratio >= 10 and lost == 0, plain=plain_steps, prior=prior_steps)]
    return experiment("intuition", "Does measuring description length against what its "
                      "intuition expects cut search (S2, intuition alone)?", "held-out set",
                      rows, "Kept out of the brain until it pays: a wrong guess pushes a "
                      "needed law to a dearer level, and search grows exponentially per level.")


def wrong_labels(brain):
    """Some experiences recorded wrongly: does it still find the law (with Ultron's own
    policy: a law plus a list of exceptions, if that is the shorter description)?"""
    from ..brain.brain import allowed_exceptions, worth_listing
    from ..brain.dsl import size
    rng = random.Random(2)
    lib = copy.deepcopy(brain.library)
    rows = []
    for frac in (0.0, 0.05, 0.1, 0.2):
        xs = _pairs(rng, 40)
        ys = [x["a"] * x["b"] for x in xs]
        for i in rng.sample(range(len(ys)), int(frac * len(ys))):
            ys[i] += rng.choice((-1, 1))
        res = synthesize(xs, ys, {"a": INT, "b": INT}, INT, lib,
                         exceptions=allowed_exceptions(len(xs)))
        if res.expr is not None and not worth_listing(size(res.expr), len(res.exceptions),
                                                      len(xs)):
            res.expr = None
        ok = _check(res.expr, lambda a, b: a * b, lib, rng)
        rows.append(_row(f"{frac:.0%} wrong", show(res.expr) if res.expr else "nothing found",
                         ok))
    return experiment("wrong labels (programs)", "If some experiences are recorded wrongly, "
                      "does it still find multiplication?", "share of wrong records", rows)


def hidden_cause(brain):
    """The outcome depends on something it can't see: it must NOT claim a law."""
    rng = random.Random(3)
    lib = copy.deepcopy(brain.library)
    xs = _pairs(rng, 30)
    ys = [x["a"] * x["b"] + rng.randint(0, 3) for x in xs]
    res = synthesize(xs, ys, {"a": INT, "b": INT}, INT, lib)
    rnd = [rng.randint(0, 20) for _ in xs]
    res2 = synthesize(xs, rnd, {"a": INT, "b": INT}, INT, lib)
    rows = [_row("hidden cause", show(res.expr) if res.expr else "no law (right)",
                 res.expr is None),
            _row("pure noise", show(res2.expr) if res2.expr else "no law (right)",
                 res2.expr is None)]
    return experiment("hidden causes and noise", "When the outcome depends on something "
                      "unseen, or on nothing, does it refuse to claim a law?", "case", rows)


def few_examples(brain):
    """How few experiences are enough?"""
    rng = random.Random(4)
    lib = copy.deepcopy(brain.library)
    rows = []
    for n in (1, 2, 3, 4, 6, 8):
        xs = _pairs(rng, n)
        f = lambda a, b: a * b + a
        res = synthesize(xs, [f(x["a"], x["b"]) for x in xs], {"a": INT, "b": INT}, INT, lib)
        ok = _check(res.expr, f, lib, rng)
        rows.append(_row(f"{n} examples", show(res.expr) if res.expr else "nothing", ok))
    return experiment("few examples", "How few examples does it need to find a·b+a?",
                      "examples", rows,
                      "Failing with very few examples is expected: many laws fit. The point "
                      "is how fast it converges.")


def program_compute(brain):
    rng = random.Random(5)
    lib = copy.deepcopy(brain.library)
    rows = []
    for n in (20, 100, 400):
        xs = _pairs(rng, n)
        f = lambda a, b: a * b + a + b
        t = time.time()
        res = synthesize(xs, [f(x["a"], x["b"]) for x in xs], {"a": INT, "b": INT}, INT, lib)
        sec = time.time() - t
        rows.append(_row(f"{n} examples", f"{sec:.1f} s", sec < 30 and res.expr is not None,
                         seconds=round(sec, 2)))
    return experiment("compute vs data", "How does search time grow with more examples?",
                      "examples", rows)


# ------------------------------------------------------------------ measurements
def _push_rows(rng, n, noise=0.0, extra=0, outliers=0.0, scale=1.0):
    rows = []
    for _ in range(n):
        m, F = rng.uniform(1, 10) * scale, rng.uniform(1, 50) * scale
        a = F / m
        r = {"F": F * (1 + rng.gauss(0, noise)), "m": m * (1 + rng.gauss(0, noise)),
             "a": a * (1 + rng.gauss(0, noise))}
        for k in range(extra):
            r[f"d{k}"] = rng.uniform(1, 10)
        rows.append(r)
    for i in rng.sample(range(n), int(outliers * n)):
        rows[i]["a"] *= rng.choice((0.3, 3.0))
    return rows


def _is_fma(law):
    return law is not None and law.powers in ({"F": 1, "a": -1, "m": -1},
                                              {"F": -1, "a": 1, "m": 1})


def noise_ramp(brain):
    rng = random.Random(6)
    rows = []
    for noise in (0.005, 0.01, 0.02, 0.05, 0.1, 0.2):
        eps = _push_rows(rng, 40, noise)
        res = search_invariant("push", eps, ["F", "m", "a"], 1e-9, precision=noise)
        rows.append(_row(f"±{noise:.1%}", res.law.formula() if res.law else "nothing",
                         _is_fma(res.law)))
    return experiment("noise", "How noisy can measurements be before F = m·a is lost?",
                      "noise per reading (known to it)", rows)


def _push_trials(rng, settings, repeats, noise, hidden=0.0):
    """Each setting (a mass and a force) measured `repeats` times; a hidden cause, if any,
    changes from setting to setting but not between repeats of one setting."""
    rows = []
    for t in range(settings):
        m, F = rng.uniform(1, 10), rng.uniform(1, 50)
        a = F / m * (1 + rng.uniform(-hidden, hidden))
        for _ in range(repeats):
            rows.append({"trial": t, "F": F * (1 + rng.gauss(0, noise)),
                         "m": m * (1 + rng.gauss(0, noise)), "a": a * (1 + rng.gauss(0, noise))})
    return rows


def noise_unknown(brain):
    """It isn't told how noisy its readings are. With repeated trials it measures the
    noise; without, it accepts only a law that explains nearly all the variation."""
    rng = random.Random(16)
    rows = []
    for noise in (0.01, 0.02, 0.05, 0.1, 0.2):
        res = search_invariant("push", _push_trials(rng, 20, 2, noise), ["F", "m", "a"],
                               1e-9, precision=None)
        est = max(res.noise["per_quantity"].values()) if res.noise and \
            "per_quantity" in res.noise else None
        rows.append(_row(f"±{noise:.0%}, repeated trials",
                         (res.law.formula() if res.law else "nothing") +
                         (f" (noise measured ±{est:.1%})" if est else ""),
                         _is_fma(res.law) and est is not None and 0.5 < est / noise < 2))
    for noise in (0.01, 0.02, 0.05, 0.1):
        res = search_invariant("push", _push_rows(rng, 40, noise), ["F", "m", "a"], 1e-9,
                               precision=None)
        rows.append(_row(f"±{noise:.0%}, no repeats", res.law.formula() if res.law else
                         "nothing", _is_fma(res.law)))
    return experiment("noise unknown", "Not told how noisy its readings are, does it work "
                      "the noise out and still find F = m·a?", "noise per reading (unknown "
                      "to it)", rows)


def outliers(brain):
    rng = random.Random(7)
    rows = []
    for frac in (0.0, 0.025, 0.05, 0.1, 0.2):
        eps = _push_rows(rng, 40, 0.01, outliers=frac)
        res = search_invariant("push", eps, ["F", "m", "a"], 1e-9, precision=0.01)
        rows.append(_row(f"{frac:.1%} bad readings", res.law.formula() if res.law else
                         "nothing", _is_fma(res.law)))
    return experiment("outliers", "If some readings are badly wrong (a slipped ruler), is "
                      "F = m·a still found?", "share of bad readings", rows)


def distractors(brain):
    rng = random.Random(8)
    rows = []
    for k in (0, 2, 4, 6, 10):
        eps = _push_rows(rng, 40, 0.0, extra=k)
        names = ["F", "m", "a"] + [f"d{i}" for i in range(k)]
        t = time.time()
        res = search_invariant("push", eps, names, 1e-9, require="a")
        sec = time.time() - t
        rows.append(_row(f"{k} irrelevant", res.law.formula() if res.law else "nothing",
                         _is_fma(res.law) and sec < 10, steps=res.steps, seconds=round(sec, 2)))
    return experiment("irrelevant measurements", "If it also measures things that don't "
                      "matter (colour, time of day...), does it still find F = m·a?",
                      "irrelevant quantities", rows)


def confounder(brain):
    """Two quantities always move together in what it saw: it can't know which matters.
    Does it notice?"""
    rng = random.Random(9)
    eps = _push_rows(rng, 40)
    for e in eps:
        e["c"] = e["m"]                 # a 'label' that happens to equal the mass
    res = search_invariant("push", eps, ["F", "m", "a", "c"], 1e-9, require="a")
    picked = res.law.formula() if res.law else "nothing"
    noticed = bool(res.rivals)
    about = res.law is not None and "a" in res.law.powers
    rows = [_row("mass and a label always equal", f"picked {picked}; ambiguity noticed: "
                 f"{noticed}", noticed and about)]
    # now it may act: offered experiments where the label and the mass can differ, does
    # it choose one that separates its rival laws, and end with the right one?
    b = Brain("lab")
    b.meet(Spec("push", "quantity", {"F": (1, 1, -2), "m": (1, 0, 0), "c": (1, 0, 0)}, "a",
                units={"F": (1, 1, -2), "m": (1, 0, 0), "c": (1, 0, 0), "a": (0, 1, -2)}))
    for e in eps[:20]:
        b.experience("push", {"F": e["F"], "m": e["m"], "c": e["c"]}, e["a"])
    first = b.qlaws.get("push")
    designed = 0
    for _ in range(6):
        options = [{"F": rng.uniform(1, 50), "m": rng.uniform(1, 10), "c": rng.uniform(1, 10)}
                   for _ in range(8)]
        x = b.propose("push", options)
        designed += x is not None
        x = x or options[0]
        b.experience("push", x, x["F"] / x["m"])
    law = b.qlaws.get("push")
    right = law is not None and law.powers in ({"F": 1, "a": -1, "m": -1},
                                               {"F": -1, "a": 1, "m": 1})
    rows.append(_row("…and it may choose its experiments",
                     f"{first.formula() if first else 'nothing'} → "
                     f"{law.formula() if law else 'nothing'}; {designed} designed",
                     right and designed > 0))
    return experiment("confounders", "When two things always move together, does it notice "
                      "it can't tell which one matters (and design an experiment)?", "case", rows)


def magnitudes(brain):
    rng = random.Random(10)
    rows = []
    for scale in (1e-12, 1e-6, 1.0, 1e6, 1e12):
        eps = _push_rows(rng, 30, scale=scale)
        res = search_invariant("push", eps, ["F", "m", "a"], 1e-9)
        rows.append(_row(f"×{scale:g}", res.law.formula() if res.law else "nothing",
                         _is_fma(res.law)))
    return experiment("magnitudes", "Does it work with tiny and huge numbers?", "scale", rows)


# ------------------------------------------------------------------ change and kinds
def changing_world(brain):
    """The world changes: a spring is replaced by a stiffer one with the same name."""
    b = Brain("lab")
    b.meet(Spec("stretch", "quantity", {"x": (0, 1, 0)}, "F", group_by="spring",
                units={"F": (1, 1, -2), "x": (0, 1, 0)}))
    rng = random.Random(11)
    for k in (50.0, 80.0):
        for _ in range(15):
            x = rng.uniform(0.1, 1)
            b.experience("stretch", {"x": x, "spring": "S"}, k * x)
    law = b.qlaws.get("stretch")
    now = None
    if law is not None:
        now = law.constant if law.kind == "global" else law.properties.get("S")
    noticed = any(e["kind"] == "doubt" for e in b.log)
    rows = [_row("stiffness 50 → 80", f"believes {now:.4g}" if now else "no law",
                 now is not None and abs(now - 80) < 1, noticed_change=noticed)]
    return experiment("a changing world", "When the world changes under the same name, does "
                      "it notice and update?", "case", rows)


def law_forms(brain):
    """Laws that aren't products, sums or its invented kinds."""
    import math
    forms = [
        ("settling (known kind)", lambda t, p: p[0] + (p[1] - p[0]) * p[2] ** t),
        ("straight line (known kind)", lambda t, p: p[0] + p[1] * t),
        ("quadratic", lambda t, p: p[0] + p[1] * t + p[2] * t * t),
        ("oscillation", lambda t, p: p[0] * math.sin(p[1] * t + p[2])),
        ("damped oscillation", lambda t, p: p[0] * p[2] ** t * math.cos(p[1] * t)),
        ("logistic growth", lambda t, p: p[0] / (1 + 9 * math.exp(-p[1] * t))),
        ("power law t^1.5", lambda t, p: p[0] * (t + 1) ** 1.5),
    ]
    rows = []
    for label, f in forms:
        b = Brain("lab")
        b.kinds = copy.deepcopy(brain.kinds)
        b.meet(Spec("w", "sequence", {"t": None}, "y", group_by="obj", order_by="t",
                    tol=0.01, surprise=0.005))
        rng = random.Random(12)
        for o in range(6):
            p = (rng.uniform(1, 5), rng.uniform(0.3, 0.9), rng.uniform(0.7, 0.95))
            for t in range(10):
                b.experience("w", {"t": t, "obj": f"O{o}"}, round(f(t, p), 6))
        law = b.slaws.get("w")
        # the test that counts: a new object, 6 readings seen, the next 4 predicted
        p = (rng.uniform(1, 5), rng.uniform(0.3, 0.9), rng.uniform(0.7, 0.95))
        xs = list(range(6))
        ys = [round(f(t, p), 6) for t in xs]
        right = law is not None
        for t in range(6, 10):
            guess = law.predict((xs, ys), t, "new") if law is not None else None
            true = f(t, p)
            right = right and guess is not None and abs(guess - true) <= 0.02 * max(1, abs(true))
        rows.append(_row(label, law.formula() if law else "no explanation", right))
    return experiment("kinds of law", "Which shapes of law can it explain, and then predict "
                      "for a new object?", "law", rows,
                      "Its grammar: Δ, ρ, composed; applied to a power of the reading; and "
                      "recurrences (the next reading a fixed mix of the last few).")


# ------------------------------------------------------------------ perception
def eyes_stress(brain):
    import numpy as np
    from ..senses.camera import scatter, shoot
    if brain.eyes is None:
        return experiment("eyes", "", "", [_row("no eyes", "untrained", False)])
    rows = []
    # (label, camera noise, gap, radius, brightness factor, how many things, gates?)
    cases = [("normal (8% noise)", 0.08, 5.0, (1.4, 2.6), 1.0, (1, 25), True),
             ("16% noise", 0.16, 5.0, (1.4, 2.6), 1.0, (1, 25), True),
             ("32% noise", 0.32, 5.0, (1.4, 2.6), 1.0, (1, 25), True),
             ("big things (r 4-6)", 0.08, 13.0, (4, 6), 1.0, (1, 7), True),
             ("faint things (30% brightness)", 0.08, 5.0, (1.4, 2.6), 0.3, (1, 25), True),
             ("touching (gap = diameter)", 0.08, 3.0, (1.2, 1.5), 1.0, (1, 25), True),
             ("overlapping (gap < diameter)", 0.08, 3.0, (1.4, 2.6), 1.0, (1, 25), False)]
    for label, noise, gap, radius, dim, (lo, hi), gates in cases:
        # the trays come from their own generator and the camera from another, so the
        # same trays are shown whatever the eyes do (looking longer takes more pictures)
        rng, camera = np.random.default_rng(13), np.random.default_rng(10_013)
        right = tried = 0
        while tried < 25:
            n = int(rng.integers(lo, hi))
            try:
                blobs = scatter(n, rng, gap=gap, radius=radius)
            except ValueError:
                continue                # a tray that can't be built isn't a test
            tried += 1
            blobs = [(x, y, r, b * dim) for x, y, r, b in blobs]
            right += brain.eyes.count(lambda: shoot(blobs, camera, noise=noise)[0])[0] == n
        rows.append(_row(label, f"{right}/25 trays counted right"
                         + ("" if gates else " (merged blobs: a physical limit, reported only)"),
                         right >= 23 or not gates))
    return experiment("eyes", "How robust is its learned vision?", "condition", rows)


def false_laws(brain):
    """The audit: 100 datasets with nothing to find (pure noise, or a hidden cause). How
    many times does it claim a law anyway? It should be zero."""
    from ..brain.brain import allowed_exceptions, worth_listing
    from ..brain.dsl import size
    rng = random.Random(14)
    lib = copy.deepcopy(brain.library)
    false_programs = 0
    for i in range(50):
        xs = _pairs(rng, 24)
        ys = ([rng.randint(0, 20) for _ in xs] if i % 2 else
              [x["a"] + x["b"] + rng.randint(0, 5) for x in xs])
        res = synthesize(xs, ys, {"a": INT, "b": INT}, INT, lib, max_size=5,
                         exceptions=allowed_exceptions(len(xs)))
        if res.expr is not None and worth_listing(size(res.expr), len(res.exceptions), len(xs)):
            false_programs += 1
    false_quantities = 0
    for i in range(50):
        eps = [{"x": rng.uniform(1, 10), "y": rng.uniform(1, 10), "z": rng.uniform(1, 10)}
               for _ in range(30)]
        res = search_invariant("noise", eps, ["x", "y", "z"], 1e-9, precision=0.02,
                               require="z")
        false_quantities += res.law is not None
    # not told its noise: pure noise without repeats, and a small hidden cause (±5%)
    # that only repeated trials can tell from noise
    unknown_noise = hidden = 0
    for i in range(25):
        eps = [{"x": rng.uniform(1, 10), "y": rng.uniform(1, 10), "z": rng.uniform(1, 10)}
               for _ in range(30)]
        unknown_noise += search_invariant("noise", eps, ["x", "y", "z"], 1e-9, precision=None,
                                          require="z").law is not None
        eps = _push_trials(rng, 20, 2, 0.005, hidden=0.05)
        hidden += search_invariant("push", eps, ["F", "m", "a"], 1e-9,
                                   precision=None).law is not None
    # sequences with nothing to find: random walks and pure noise, in sequence worlds
    false_kinds = 0
    for i in range(25):
        b = Brain("audit")
        b.kinds = copy.deepcopy(brain.kinds)
        b.meet(Spec("w", "sequence", {"t": None}, "y", group_by="obj", order_by="t",
                    tol=0.01, surprise=0.005))
        for o in range(6):
            y = rng.uniform(1, 5)
            for t in range(10):
                y = y + rng.uniform(-1, 1) if i % 2 else rng.uniform(1, 5)
                b.experience("w", {"t": t, "obj": f"O{o}"}, round(y, 6))
        false_kinds += b.slaws.get("w") is not None
    rows = [_row("50 program datasets with nothing to find", f"{false_programs} false laws",
                 false_programs == 0),
            _row("25 sequence worlds with nothing to find", f"{false_kinds} false laws",
                 false_kinds == 0),
            _row("50 measurement datasets with nothing to find",
                 f"{false_quantities} false laws", false_quantities == 0),
            _row("25 datasets of pure noise, noise not told", f"{unknown_noise} false laws",
                 unknown_noise == 0),
            _row("25 hidden causes (±5%) with repeated trials, noise not told",
                 f"{hidden} false laws", hidden == 0)]
    return experiment("false laws", "On data with nothing to find, does it ever claim a law?",
                      "audit", rows)


def words_stress(brain):
    """Words by pointing (stage 3, L1) under a Trainer who sometimes says the wrong word,
    and with fewer sentences heard. Each row relearns the words from scratch (Ultron's
    own kinds of thing kept) and is scored on 60 sentences about new tables, in word
    combinations never heard."""
    from ..brain.categories import kinds_of
    from ..brain.language import fits, learn_lexicon
    from ..senses.tabletop import COLOURS, SHAPES, SIZES
    from ..senses.things import look_at_table
    from ..trainer.language_lessons import WordsByPointing
    from .exams import _meant
    if brain.eyes is None or not brain.categories:
        return experiment("words by pointing", "", "", [_row("no words", "untrained", False)])
    cats = brain.categories
    kinds = lambda seen: [kinds_of(cats, t) for t in seen]
    teach = WordsByPointing(7029)
    heard = [(said.split(), kinds(look_at_table(brain.eyes, look)))
             for said, look, _, _ in teach.talks(120)]
    test = []
    for said, look, things, target in WordsByPointing(8029).talks(60, held_out=True):
        seen = look_at_table(brain.eyes, look)
        test.append((said.split(), kinds(seen), _meant(seen, things, target)))
    families = [sorted(COLOURS), sorted(SIZES), sorted(SHAPES)]

    def score(learned):
        lexicon, rivals = learned
        right = gave = 0
        for words, ks, truth in test:
            if any(w not in lexicon for w in words):
                continue
            pick = lambda lex: [i for i, k in enumerate(ks)
                                if all(fits(lex[w], k) for w in words)]
            hits = pick(lexicon)
            if any(pick(r) != hits for r in rivals):
                continue                        # not sure yet what a word means
            if len(hits) == 1:
                gave += 1
                right += hits[0] == truth
        return right, gave

    rows = []
    rng = random.Random(29)
    for frac in (0.0, 0.05, 0.1, 0.2, 0.3):
        spoilt = []
        for words, ks in heard:
            words = list(words)
            if rng.random() < frac:
                i = rng.randrange(1, len(words))
                fam = next(f for f in families if words[i] in f)
                words[i] = rng.choice([w for w in fam if w != words[i]])
            spoilt.append((words, ks))
        right, gave = score(learn_lexicon(spoilt, cats, rivals=True))
        rows.append(_row(f"{frac:.0%} of sentences name the wrong thing",
                         f"{right}/60 right ({right}/{gave} of its answers)", right >= 57,
                         right=right, gave=gave))
    for n in (120, 60, 40, 20, 10):
        right, gave = score(learn_lexicon(heard[:n], cats, rivals=True))
        rows.append(_row(f"{n} sentences heard", f"{right}/60 right ({right}/{gave} of its "
                         f"answers)", right >= 57, right=right, gave=gave))
    return experiment("words by pointing", "Does it still learn what words mean when the "
                      "Trainer sometimes says the wrong word, or says less?",
                      "wrong words; sentences heard", rows,
                      note="A row passes at 57/60 (95%). The two dials are separate: "
                           "the first breakpoint is the first row that fails.")


def events_stress(brain):
    """Words for what happens (stage 3, L2) under a Trainer who sometimes says the wrong
    word, with fewer sentences heard, and through a noisier camera. Each row relearns the
    event words (or the comparing words) from scratch, with the words for looks it already
    has, and is scored on 60 new films about things never seen doing that."""
    from ..brain import events
    from ..brain.language import (comparing, learn_lexicon, learn_relations, name_with,
                                  picked, relate_with, runs)
    from ..senses.tabletop import NOISE
    from ..trainer.language_lessons import VERBS, WordsForWhatHappens, truth
    from .exams import _film_thing
    if brain.eyes is None or not brain.event_words:
        return experiment("words for what happens", "", "", [_row("no words", "untrained",
                                                                  False)])
    found = dict(brain.categories)
    found.update(events.categories(brain))
    known = {w: m[1] for w, m in brain.vocab.items()
             if m[0] == "look" and w not in brain.event_words}
    kinds = lambda film: [events.kinds_of_thing(brain, t) for t in film["things"]]

    def films(noise):
        teach = WordsForWhatHappens(7030, noise=noise)
        heard = []
        for said, watch, _, _ in teach.event_talks():
            f = events.watch(brain, watch())
            heard.append((said.split(), kinds(f)))
        test = []
        for said, watch, things, target in WordsForWhatHappens(8030, noise=noise) \
                .event_talks(60, held_out=True):
            f = events.watch(brain, watch())
            test.append((said.split(), f, _film_thing(f, things, target)))
        return heard, test

    def score(heard, test):
        lexicon, rivals = learn_lexicon(heard, found, rivals=True, known=known)
        words = {w: m for w, m in lexicon.items() if w not in known}
        seen = [k for _, ks in heard for k in ks]
        right = gave = 0
        for said, f, meant in test:
            mine = picked(brain, f, said[:-1])
            if len(mine) != 1:
                continue
            got, _ = name_with(words, rivals, kinds(f)[mine[0]], seen)
            gave += got is not None
            right += got == said[-1]
        return right, gave

    rows = []
    heard, test = films(None)
    rng = random.Random(30)
    for frac in (0.0, 0.1, 0.2, 0.3):
        spoilt = []
        for words, ks in heard:
            words = list(words)
            if rng.random() < frac:
                words[-1] = rng.choice([v for v in VERBS if v != words[-1]])
            spoilt.append((words, ks))
        right, gave = score(spoilt, test)
        rows.append(_row(f"{frac:.0%} of event sentences say the wrong word",
                         f"{right}/60 right ({right}/{gave} of its answers)", right >= 54,
                         right=right, gave=gave))
    for n in (50, 25, 12):
        right, gave = score(heard[:n], test)
        rows.append(_row(f"{n} event sentences heard", f"{right}/60 right ({right}/{gave} "
                         f"of its answers)", right >= 54, right=right, gave=gave))
    for times in (2, 3):
        right, gave = score(*films(NOISE * times))
        rows.append(_row(f"camera {times} times as noisy", f"{right}/60 right ({right}/{gave} "
                         f"of its answers)", right >= 54, right=right, gave=gave))
    # comparing words
    teach = WordsForWhatHappens(7130)
    compared = []
    for said, watch, _, word, _, _ in teach.relation_talks():
        f = events.watch(brain, watch())
        got = comparing(brain, said, f)
        if got is not None:
            compared.append((got[0], f, got[1], got[2], word))
    test = []
    for said, watch, things, word, first, second in WordsForWhatHappens(8130) \
            .relation_talks(60, held_out=True):
        f = events.watch(brain, watch())
        rs, _ = runs(brain, ["___" if w == word else w for w in said.split()])
        if len(rs) == 2:
            test.append((f, picked(brain, f, rs[0]), picked(brain, f, rs[1]), word, first,
                         second))
    for frac in (0.0, 0.1, 0.2):
        spoilt = []
        for others, f, a, b, word in compared:
            if rng.random() < frac:
                wrong = rng.choice([w for w in ("faster", "heavier", "before", "after",
                                                "more", "fewer") if w != word])
                others = [wrong if w == word else w for w in others]
            spoilt.append((others, f, a, b))
        best, rivals = learn_relations(spoilt, rivals=True)
        right = gave = 0
        for f, a, b, word, first, second in test:
            says = relate_with(best, rivals, f, a, b)
            gave += bool(says)
            right += word in says and all(truth(w, first, second) for w in says)
        rows.append(_row(f"{frac:.0%} of comparing sentences say the wrong word",
                         f"{right}/{len(test)} right ({right}/{gave} of its answers)",
                         right >= 54, right=right, gave=gave))
    return experiment("words for what happens", "Does it still learn words for events and "
                      "for comparing when the Trainer sometimes says the wrong word, says "
                      "less, or the camera is noisier?",
                      "wrong words; sentences heard; camera noise", rows,
                      note="A row passes at 54/60 (90%). Event words were taught with 100 "
                           "sentences and comparing words with 120 in the first rows.")


def grammar_stress(brain):
    """How words combine (stage 3, L3) when it mishears words, when the Trainer sometimes
    talks about another table, when one word has two meanings, and with fewer sentences
    heard. Each row finds the grammar again from scratch (the words for kinds of thing
    kept) and is scored on 60 sentences about new tables: 20 nested deeper, 20 with more
    phrases joined, 20 with words in new places."""
    from ..brain import grammar
    from ..trainer.grammar_lessons import EXAM, HowWordsCombine
    from .exams import _table_things
    if brain.eyes is None or not brain.grammar:
        return experiment("how words combine", "", "", [_row("no grammar", "untrained", False)])
    heard = []
    for said, look, things, meant, kind in HowWordsCombine(7031).talks():
        heard.append(grammar.heard_as(brain, said, grammar.see_table(brain, look)))
    test = []
    for said, look, things, meant, kind in HowWordsCombine(8031).talks(
            kinds=[(k, 20) for k, _ in EXAM]):
        seen = grammar.see_table(brain, look)
        test.append((grammar.heard_as(brain, said, seen), _table_things(seen, things),
                     sorted(meant)))
    known = grammar.known_kinds(brain)
    vocabulary = sorted({w for ws, _, _ in heard for w in ws})

    def score(said):
        lexicon, rivals = grammar.learn_grammar(said, brain.categories, known=known,
                                                rivals=True)
        doubts = set(grammar.doubtful_words(said, lexicon)) | set(
            grammar.unsteady_words(said, brain.categories, known=known))
        right = gave = 0
        for (ws, table, kinds), which, truth in test:
            got, _ = grammar.understand(lexicon, rivals, ws, table, kinds, doubts)
            if got is not None:
                gave += 1
                right += sorted(which[i] for i in got) == truth
        return right, gave

    def row(level, said):
        right, gave = score(said)
        return _row(level, f"{right}/60 right ({right}/{gave} of its answers)", right >= 57,
                    right=right, gave=gave)

    rows = []
    rng = random.Random(31)
    for frac in (0.0, 0.2, 0.4):
        spoilt = []
        for ws, table, kinds in heard:
            ws = list(ws)
            if rng.random() < frac:
                i = rng.randrange(len(ws))
                ws[i] = rng.choice([w for w in vocabulary if w != ws[i]])
            spoilt.append((ws, table, kinds))
        rows.append(row(f"{frac:.0%} of sentences have a word misheard", spoilt))
    for frac in (0.2, 0.4):
        spoilt = []
        for k, (ws, table, kinds) in enumerate(heard):
            if rng.random() < frac:
                _, table, kinds = heard[(k + 1) % len(heard)]
            spoilt.append((ws, table, kinds))
        rows.append(row(f"{frac:.0%} of sentences are about another table", spoilt))
    # 'left' also said for 'above' in half the sentences that say 'above'
    twice = [([("left" if w == "above" and rng.random() < 0.5 else w) for w in ws], t, k)
             for ws, t, k in heard]
    rows.append(row("'left' has two meanings (also 'above', half the time)", twice))
    for n in (75, 30):
        rows.append(row(f"{n} sentences heard", heard[:n]))
    return experiment("how words combine", "Does it still find how words combine when it "
                      "mishears words, when the Trainer talks about another table, when a "
                      "word has two meanings, or when it hears less?",
                      "misheard words; wrong tables; two meanings; sentences heard", rows,
                      note="A row passes at 57/60 (95%). The grammar was found from 300 "
                           "sentences in the first rows.")


EXPERIMENTS = [program_size, library_learning, intuition_prior, wrong_labels, hidden_cause, few_examples, program_compute,
               noise_ramp, noise_unknown, outliers, distractors, confounder, magnitudes, changing_world,
               law_forms, eyes_stress, false_laws, words_stress, events_stress,
               grammar_stress]


def _level0():
    from .room_lab import EXPERIMENTS as LEVEL0         # Level 0: the room (WP3)
    return LEVEL0


EXPERIMENTS += _level0()


def run_all(brain):
    out = []
    for exp in EXPERIMENTS:
        t = time.time()
        with dsl.limits(20000, 10 ** 7):
            r = exp(brain)
        r["seconds"] = round(time.time() - t, 1)
        out.append(r)
    return out


def report(results):
    lines = ["# The failure lab", "",
             "Every experiment turns one dial until Ultron breaks. ✅ = still right, "
             "❌ = broken. Regenerate with `python -m ultron stress`.", ""]
    for r in results:
        bp = r["breakpoint"]
        lines += [f"## {r['name']}", "", f"_{r['question']}_ "
                  f"Breaks at: **{bp if bp is not None else 'did not break'}**", "",
                  f"| {r['dial']} | what it did | |", "|---|---|---|"]
        for row in r["rows"]:
            lines.append(f"| {row['level']} | `{row['outcome']}` | {'✅' if row['ok'] else '❌'} |")
        if r.get("note"):
            lines += ["", r["note"]]
        lines.append("")
    return "\n".join(lines)
