from ultron.brain import reasoner


def test_final_exam_and_noisy_lab_pass(trained):
    _, results = trained
    assert results[7]["passed"] and results[8]["passed"]


def test_division_without_being_taught(trained):
    brain, _ = trained
    assert brain.vocab.get("divided") is None
    assert reasoner.arithmetic(brain, "what times 7 equals 84").value == 12


def test_refuses_what_it_has_never_experienced(trained):
    brain, _ = trained
    assert reasoner.arithmetic(brain, "5 minus 8").value is None
    assert reasoner.arithmetic(brain, "what times 4 equals 21").value is None
    assert brain.predict("orbit", {"r": 1.2e9, "system": "Saturn"}) is None
    assert reasoner.physics(brain, "a", {"x": 0.3, "m": 2.0}, {"spring": "S99"}).value is None


def test_noisy_lab_estimate_is_refined(trained):
    brain, _ = trained
    assert abs(brain.qlaws["lab_push"].constant - 1) < 0.005
    assert brain.qlaws["lab_stretch"].kind == "grouped"


def test_runs_laws_backwards(trained):
    brain, _ = trained
    ans = reasoner.physics(brain, "m", {"F": 30.0, "a": 6.0})
    assert abs(ans.value - 5.0) < 1e-6
