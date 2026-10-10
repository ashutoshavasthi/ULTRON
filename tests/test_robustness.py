"""Breakpoints found by the failure lab, pushed outward. They must never move back."""

import random

from ultron.brain.brain import Brain
from ultron.brain.dsl import INT, safe_evaluate
from ultron.brain.memory import Spec
from ultron.brain.synth import synthesize
from ultron.judge import failures


def _ok(exp):
    r = exp(Brain("lab"))
    return [row["level"] for row in r["rows"] if not row["ok"]]


def test_measurement_laws_survive_real_noise():
    assert _ok(failures.noise_ramp) == []          # bell-curve noise up to ±20%


def test_measurement_laws_survive_outliers():
    assert _ok(failures.outliers) == []            # up to 20% badly wrong readings


def test_tiny_and_huge_numbers():
    assert _ok(failures.magnitudes) == []


def test_program_with_wrong_records(trained):
    brain, _ = trained
    rng = random.Random(2)
    xs = [{"a": rng.randint(0, 9), "b": rng.randint(0, 9)} for _ in range(40)]
    ys = [x["a"] * x["b"] for x in xs]
    for i in rng.sample(range(40), 4):
        ys[i] += 1
    r = synthesize(xs, ys, {"a": INT, "b": INT}, INT, brain.library, exceptions=10)
    assert r.expr is not None and len(r.exceptions) == 4
    assert all(safe_evaluate(r.expr, {"a": a, "b": b}, brain.library) == a * b
               for a in range(10) for b in range(10))


def test_no_false_law_from_noise(trained):
    brain, _ = trained
    rng = random.Random(3)
    xs = [{"a": rng.randint(0, 9), "b": rng.randint(0, 9)} for _ in range(30)]
    r = synthesize(xs, [rng.randint(0, 20) for _ in xs], {"a": INT, "b": INT}, INT,
                   brain.library, exceptions=7)
    assert r.expr is None


def test_learning_keeps_a_law_through_mis_recorded_experiences():
    b = Brain("lab")
    b.meet(Spec("add", "program", {"a": INT, "b": INT}, "out", out_type=INT))
    rng = random.Random(9)
    bad = 0
    for i in range(40):
        a, c = rng.randint(0, 9), rng.randint(0, 9)
        wrong = i in (15, 27)
        bad += wrong
        b.experience("add", {"a": a, "b": c}, a + c + (1 if wrong else 0))
    law = b.hypotheses.get("add")
    assert law is not None
    assert all(safe_evaluate(law, {"a": a, "b": c}, b.library) == a + c
               for a in range(10) for c in range(10))
    assert len(b.exceptions.get("add", [])) == bad
