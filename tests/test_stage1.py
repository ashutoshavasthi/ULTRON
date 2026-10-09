"""Stage 1 criteria R2 (it works out its own noise), R5 (it designs the experiment that
separates rival measurement laws) and E1 (laws of change)."""

import random

from ultron.brain.brain import Brain
from ultron.brain.invariants import search_invariant
from ultron.brain.kinds import SequenceLaw, grammar, search, sequences
from ultron.brain.memory import Spec
from ultron.judge.failures import _push_rows, _push_trials

FMA = ({"F": 1, "a": -1, "m": -1}, {"F": -1, "a": 1, "m": 1})


def test_noise_measured_from_repeated_trials():
    rng = random.Random(1)
    res = search_invariant("push", _push_trials(rng, 20, 2, 0.1), ["F", "m", "a"], 1e-9,
                           precision=None)
    assert res.law is not None and res.law.powers in FMA
    est = max(res.noise["per_quantity"].values())
    assert 0.05 < est < 0.2


def test_hidden_cause_is_not_taken_for_noise_when_trials_repeat():
    rng = random.Random(2)
    for _ in range(5):
        eps = _push_trials(rng, 20, 2, 0.005, hidden=0.05)
        assert search_invariant("push", eps, ["F", "m", "a"], 1e-9, precision=None).law is None


def test_without_repeats_only_a_law_explaining_nearly_everything():
    rng = random.Random(3)
    assert search_invariant("push", _push_rows(rng, 40, 0.01), ["F", "m", "a"], 1e-9,
                            precision=None).law.powers in FMA
    eps = [{"x": rng.uniform(1, 10), "y": rng.uniform(1, 10), "z": rng.uniform(1, 10)}
           for _ in range(30)]
    assert search_invariant("n", eps, ["x", "y", "z"], 1e-9, precision=None,
                            require="z").law is None


def test_designs_the_experiment_that_separates_rival_laws():
    rng = random.Random(9)
    b = Brain("t")
    b.meet(Spec("push", "quantity", {"F": (1, 1, -2), "m": (1, 0, 0), "c": (1, 0, 0)}, "a",
                units={"F": (1, 1, -2), "m": (1, 0, 0), "c": (1, 0, 0), "a": (0, 1, -2)}))
    for _ in range(20):
        m, F = rng.uniform(1, 10), rng.uniform(1, 50)
        b.experience("push", {"F": F, "m": m, "c": m}, F / m)   # c always equals m
    assert b.quantity_rivals.get("push")
    for _ in range(4):
        options = [{"F": rng.uniform(1, 50), "m": rng.uniform(1, 10), "c": rng.uniform(1, 10)}
                   for _ in range(8)]
        x = b.propose("push", options) or options[0]
        b.experience("push", x, x["F"] / x["m"])
    assert b.qlaws["push"].powers in FMA


def _explain(f, objects=5, n=10):
    import math  # noqa: F401
    rng = random.Random(4)
    eps = []
    params = []
    for o in range(objects):
        p = (rng.uniform(1, 5), rng.uniform(0.3, 0.9), rng.uniform(0.7, 0.95))
        params.append(p)
        eps += [{"t": t, "obj": o, "y": round(f(t, p), 6)} for t in range(n)]
    seqs = sequences(eps, "y", "t", "obj")
    found, _ = search(seqs, 0.01, grammar())
    assert found is not None
    return SequenceLaw("w", "y", "t", "obj", found.template, found.scope, found.constant,
                       found.properties, found.spread)


def test_oscillation_its_period_and_damping():
    import math
    law = _explain(lambda t, p: p[0] * p[2] ** t * math.cos(p[1] * t))
    assert law.template.get("rec") == 2
    amp, step, keep = 3.0, 0.5, 0.9
    xs = list(range(6))
    ys = [amp * keep ** t * math.cos(step * t) for t in xs]
    assert abs(law.predict((xs, ys), 9, "new") - amp * keep ** 9 * math.cos(step * 9)) < 1e-6
    assert abs(law.period((xs, ys), "new") - 2 * math.pi / step) < 1e-6
    assert abs(law.shrink((xs, ys), "new") - keep) < 1e-6


def test_logistic_capacity_and_draining_never_measured():
    import math
    law = _explain(lambda t, p: 900 * p[0] / (1 + 9 * math.exp(-p[1] * t)))
    xs = list(range(6))
    ys = [1500 / (1 + 30 * math.exp(-0.6 * t)) for t in xs]
    assert abs(law.resting_value((xs, ys), "new") - 1500) < 1
    law = _explain(lambda t, p: (8 * p[0] - p[1] * t) ** 2, n=8)
    ys = [(6 - 0.5 * t) ** 2 for t in xs]
    assert abs(law.reaches_zero((xs, ys), "new") - 12) < 0.05


def test_lists_built_from_laws_it_already_has():
    from ultron.brain.dsl import INT, LIST, Law, Library, evaluate, show
    from ultron.brain.synth import synthesize
    lib = Library()
    # addition, as Ultron invented it in lesson 2: start at a and step up b times
    lib.add(Law("merge", ["a", "b"], ("iter", ("succ",), ("var", "b"), ("var", "a")), INT))
    rng = random.Random(5)
    xs = [{"L": [rng.randint(0, 9) for _ in range(rng.randint(1, 4))], "t": rng.randint(0, 9)}
          for _ in range(10)]
    total = synthesize(xs, [sum(x["L"]) for x in xs], {"L": LIST, "t": INT}, INT, lib).expr
    above = synthesize(xs, [sum(v > x["t"] for v in x["L"]) for x in xs],
                       {"L": LIST, "t": INT}, INT, lib).expr
    assert total == ("fold", "merge", ("var", "L"), ("const", 0)), show(total)
    long = list(range(20))
    assert evaluate(total, {"L": long, "t": 0}, lib) == sum(long)
    assert evaluate(above, {"L": long, "t": 12}, lib) == 7


def test_sleep_finds_a_shared_piece_only_when_it_pays():
    from ultron.brain import abstraction
    from ultron.brain.dsl import INT, Law, Library, evaluate
    lib = Library()
    lib.add(Law("groups", ["a", "b"], ("iter", ("succ",), ("const", 0), ("var", "a")), INT))
    v = lambda n: ("var", n)
    S = lambda x, y: ("call", "groups", ("succ", x), ("succ", y))
    progs = [("pred", S(v("a"), ("succ", v("b")))), ("succ", S(v("b"), v("a"))),
             ("call", "groups", v("a"), S(v("a"), v("b"))), ("pred", S(v("b"), v("b")))]
    pieces, rewritten = abstraction.sleep(progs, lib)
    assert pieces and pieces[0][1] == S(v("x1"), v("x2"))
    assert all("piece1" in repr(p) for p in rewritten)
    # pieces with nothing in common: no piece is worth writing down
    lone = Library()
    assert abstraction.sleep([("succ", v("a")), ("pred", v("b"))], lone)[0] == []
