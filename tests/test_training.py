import json

from ultron.brain import reasoner
from ultron.brain.brain import Brain
from ultron.trainer.trainer import Trainer


def test_every_lesson_passes_its_held_out_exam(trained):
    _, results = trained
    for n, r in results.items():
        assert r["passed"], f"lesson {n} failed"


def test_memorisers_fail_where_ultron_succeeds(trained):
    _, results = trained
    for n in (1, 2, 3, 5):
        for item in results[n]["items"]:
            s = item["scores"]
            if s["lookup"][1]:
                assert s["lookup"][0] / s["lookup"][1] < 0.1


def test_noisy_tv_is_abandoned(trained):
    tv = trained[1][2]["noisy_tv"]
    assert not tv["lamps_law"]
    assert tv["lamp_choices"] <= 16


def test_blank_brain_cannot_multiply(trained):
    assert trained[1][3]["blank_brain"]["score"][0] == 0


def test_one_shot_transfer_to_jupiters_moons(trained):
    r = trained[1][6]
    assert r["items"][1]["scores"]["ultron"] == [3, 3]
    assert r["blank_one_shot"]["scores"]["ultron"][0] == 0
    assert 1000 < r["sun_vs_jupiter"] < 1100


def test_answers_questions_with_reasons(trained):
    brain, _ = trained
    ans = reasoner.arithmetic(brain, "what is 347 plus 1289?")
    assert ans.text == "1636" and len(ans.steps) >= 3
    assert reasoner.arithmetic(brain, "3 divided 4").value is None


def test_chains_laws_it_learned_separately(trained):
    brain, _ = trained
    law = brain.qlaws["stretch"]
    spring = sorted(law.properties)[0]
    ans = reasoner.physics(brain, "a", {"x": 0.5, "m": 2.0}, {"spring": spring})
    assert abs(ans.value - law.properties[spring] * 0.5 / 2.0) < 1e-6


def test_training_is_deterministic():
    runs = []
    for _ in range(2):
        b = Brain()
        t = Trainer(b)
        for n in range(4):
            t.run(n)
        runs.append(json.dumps(b.to_json(), sort_keys=True))
    assert runs[0] == runs[1]


def test_save_and_load_round_trip(trained, tmp_path):
    brain, _ = trained
    path = tmp_path / "b.json"
    brain.save(path)
    again = Brain.load(path)
    assert reasoner.arithmetic(again, "12 times 11").text == "132"
    assert again.predict("push", {"F": 10.0, "m": 2.0}) == brain.predict("push", {"F": 10.0, "m": 2.0})
