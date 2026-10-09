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


def wrong_labels(brain):
    """A few experiences recorded wrongly: does exact program search survive?"""
    rng = random.Random(2)
    lib = copy.deepcopy(brain.library)
    rows = []
    for frac in (0.0, 0.05, 0.1, 0.2):
        xs = _pairs(rng, 40)
        ys = [x["a"] * x["b"] for x in xs]
        for i in rng.sample(range(len(ys)), int(frac * len(ys))):
            ys[i] += rng.choice((-1, 1))
        res = synthesize(xs, ys, {"a": INT, "b": INT}, INT, lib)
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
    for k in (0, 1, 2, 4, 6):
        eps = _push_rows(rng, 40, 0.0, extra=k)
        names = ["F", "m", "a"] + [f"d{i}" for i in range(k)]
        t = time.time()
        res = search_invariant("push", eps, names, 1e-9)
        sec = time.time() - t
        rows.append(_row(f"{k} irrelevant", res.law.formula() if res.law else "nothing",
                         _is_fma(res.law), steps=res.steps, seconds=round(sec, 2)))
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
    res = search_invariant("push", eps, ["F", "m", "a", "c"], 1e-9)
    picked = res.law.formula() if res.law else "nothing"
    noticed = False                     # nothing in the engine reports ties
    rows = [_row("mass and a label always equal", f"picked {picked}; ambiguity noticed: "
                 f"{noticed}", noticed)]
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
    now = law.properties.get("S") if law else None
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
        rows.append(_row(label, law.formula() if law else "no explanation", law is not None))
    return experiment("kinds of law", "Which shapes of law can it explain at all?", "law",
                      rows, "Anything outside its grammar (Δ, ρ, composed) is out of reach.")


# ------------------------------------------------------------------ perception
def eyes_stress(brain):
    import numpy as np
    from ..senses.camera import scatter, shoot
    if brain.eyes is None:
        return experiment("eyes", "", "", [_row("no eyes", "untrained", False)])
    rows = []
    cases = [("normal (8% noise)", dict(noise=0.08), {}),
             ("16% noise", dict(noise=0.16), {}),
             ("32% noise", dict(noise=0.32), {}),
             ("big things (r 4-6)", dict(noise=0.08), dict(gap=12.0, radius=(4, 6))),
             ("faint things", dict(noise=0.08), dict(dim=True)),
             ("crowded (gap 3 px)", dict(noise=0.08), dict(gap=3.0))]
    for label, cam, place in cases:
        rng = np.random.default_rng(13)
        right = 0
        for _ in range(25):
            n = int(rng.integers(1, 25))
            try:
                blobs = scatter(n, rng, gap=place.get("gap", 5.0),
                                radius=place.get("radius", (1.4, 2.6)))
            except ValueError:
                continue
            if place.get("dim"):
                blobs = [(x, y, r, b * 0.3) for x, y, r, b in blobs]
            right += brain.eyes.count(lambda: shoot(blobs, rng, noise=cam["noise"])[0])[0] == n
        rows.append(_row(label, f"{right}/25 trays counted right", right >= 23))
    return experiment("eyes", "How robust is its learned vision?", "condition", rows)


EXPERIMENTS = [program_size, wrong_labels, hidden_cause, few_examples, program_compute,
               noise_ramp, outliers, distractors, confounder, magnitudes, changing_world,
               law_forms, eyes_stress]


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
