"""Phase 3: learned eyes, laws from video, invented kinds of explanation, acting."""

from ultron.brain import kinds, reasoner
from ultron.brain.invariants import SumLaw


def test_eyes_learned_from_touch(trained):
    brain, results = trained
    assert results[19]["passed"]
    assert brain.eyes is not None and brain.eyes.trained_on == 400
    items = {i["name"][:20]: i["scores"]["ultron"] for i in results[19]["items"]}
    assert all(c >= 0.95 * n for c, n in items.values())


def test_laws_rediscovered_from_video(trained):
    brain, results = trained
    assert results[21]["passed"]
    assert brain.qlaws["see_push"].powers == {"F": 1, "a": -1, "m": -1}
    assert abs(brain.qlaws["see_push"].constant - 1) < 0.02
    roll = brain.qlaws["see_roll"]
    assert isinstance(roll, SumLaw) and roll.b == {"v": 2}
    assert abs(roll.coef * 2 * 9.81 - 1) < 0.03          # 1/2g, from pixels


def test_noise_check_rejects_wrong_forms():
    """With measured uncertainties, only the form that leaves noise-sized leftovers fits."""
    import random
    from ultron.brain.invariants import search_sum_invariant
    rng = random.Random(3)
    eps = []
    for run in range(5):
        top = rng.uniform(1, 4)
        for _ in range(8):
            y = rng.uniform(0, top)
            v = (2 * 9.81 * (top - y)) ** 0.5
            eps.append({"y": y + rng.gauss(0, 0.01), "v": v + rng.gauss(0, 0.05),
                        "±y": 0.01, "±v": 0.05, "run": run})
    law = search_sum_invariant("r", eps, ["y", "v"], 0.05, "run",
                               errors={"y": "±y", "v": "±v"}).law
    assert law is not None and law.b == {"v": 2}


def test_invents_a_new_kind(trained):
    brain, results = trained
    assert results[22]["passed"]
    kind = brain.kinds["kind 1"]
    assert kind["template"] == {"y_ops": ["Δ", "ρ"], "x_op": None}
    assert kind["found_in"] == "cool"
    assert brain.kind_steps["cool"]["invent"] > 0


def test_reuses_kinds_and_invents_a_second(trained):
    brain, results = trained
    assert results[23]["passed"]
    assert {"bounces", "charge"} <= set(brain.kinds["kind 1"]["uses"])
    second = brain.kinds["kind 2"]
    assert second["found_in"] == "hang" and "burn" in second["uses"]
    assert "wander" not in brain.slaws                        # noise stays unexplained


def test_ablation_cannot_explain():
    from ultron.brain.brain import Brain
    from ultron.brain.memory import Spec
    from ultron.env.sequences import CoolingCups
    b = Brain()
    b.inventing = False
    b.meet(Spec("cool", "sequence", {"t": None}, "T", group_by="cup", order_by="t", tol=0.01,
                surprise=0.005))
    cups = CoolingCups(1)
    for _ in range(6):
        cup = cups.new_cup()
        for t in range(10):
            b.experience("cool", {"t": t, "cup": cup}, cups.read(cup, t))
    assert "cool" not in b.slaws and not b.kinds


def test_sequence_questions(trained):
    brain, _ = trained
    ask = lambda q: reasoner.physics(brain, *reasoner.parse_physics(q)[:2])
    rest = ask("find rest given T@0=80 T@1=70 T@2=62")
    assert abs(rest.value - 30) < 1e-6          # steps 10, 8: settles at 62 - 8·0.8/0.2
    assert abs(ask("find L given F=20 L@2=0.31 L@10=0.39").value - 0.49) < 1e-9
    assert ask("find x given t=5 x@0=1 x@1=3 x@2=2").value is None


def test_acting_corrects_its_misses(trained):
    brain, results = trained
    assert results[24]["passed"] and results[25]["passed"]
    trace = results[24]["traces"][-1]
    assert "never done this on carpet" in trace[0]


def test_kind_templates_are_data():
    t = {"y_ops": ["Δ", "ρ"], "x_op": None}
    assert [round(z, 9) for z in kinds.transform(t, [0, 1, 2, 3], [80, 70, 62, 55.6])] == [0.8, 0.8]
    law = kinds.SequenceLaw("x", "T", "t", "cup", t, "per group")
    assert abs(law.predict(([0, 1, 2], [80, 70, 62]), 3) - 55.6) < 1e-9


def test_blind_3_failures_stay_fixed(trained):
    """Questions from the third independent examiner that Ultron once got wrong."""
    brain, _ = trained
    ask = lambda q: reasoner.physics(brain, *reasoner.parse_physics(q)[:2]).value
    assert abs(ask("find T given t=0 T@3=45.312 T@4=39.414 T@5=34.813") - 75) < 0.75
    assert abs(ask("find T given t=5 T@0=88 T@2=66.378 T@4=51.84") - 46.4688) < 0.5
    assert abs(ask("find h given k=4 h@0=3.2 h@1=2.72") - 1.67042) < 0.02   # all balls settle at 0
    assert ask("find T given t=5 T@0=80 T@1=70") is None                      # cups don't


def test_independent_3_passes(trained):
    import pathlib
    from ultron.__main__ import score_blind
    path = pathlib.Path(__file__).parent.parent / "blind" / "independent_3.txt"
    right, total, _ = score_blind(trained[0], path.read_text())
    assert right == total
