from ultron.brain import reasoner


def test_final_exam_and_noisy_lab_pass(trained):
    _, results = trained
    assert results[7]["passed"] and results[9]["passed"]


def test_division_without_being_taught(trained):
    brain, _ = trained
    assert brain.vocab.get("divided") is None
    assert reasoner.arithmetic(brain, "what times 7 equals 84").value == 12


def test_refuses_what_it_has_never_experienced(trained):
    brain, _ = trained
    assert reasoner.arithmetic(brain, "what times 4 equals 21").value is None
    assert reasoner.arithmetic(brain, "5 plus -3").value is None     # never paid a negative wage
    assert reasoner.arithmetic(brain, "-2 times 3").value is None    # never made -2 groups
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


def test_invents_numbers_below_zero(trained):
    brain, results = trained
    assert results[8]["passed"]
    inv = brain.inventions["line:earn/spend"]
    assert inv["primitives"] == ["down"] and inv["up"] == "earn"
    # the invention came before any word for it
    kinds = [(e["kind"], e["text"]) for e in brain.log if e["lesson"] == 8]
    first_invent = next(i for i, (k, _) in enumerate(kinds) if k == "invent")
    first_word = next(i for i, (k, t) in enumerate(kinds) if k == "word" and "below zero" in t)
    assert first_invent < first_word


def test_arithmetic_below_zero(trained):
    brain, _ = trained
    assert reasoner.arithmetic(brain, "5 minus 8").text == "-3"
    assert reasoner.arithmetic(brain, "negative four minus three").text == "-7"
    assert reasoner.arithmetic(brain, "what plus 9 equals 2").text == "-7"


def test_laws_carry_trust(trained):
    brain, _ = trained
    assert brain.status("push") == "established"
    assert all(l.provenance["support"] >= 3 for l in brain.claws["collide"])


def test_blind_harness(trained, tmp_path, capsys):
    from ultron.__main__ import main
    brain, _ = trained
    bpath = tmp_path / "b.json"
    brain.save(bpath)
    main(["--brain", str(bpath), "blind", "blind/example_not_blind.txt"])
    out = capsys.readouterr().out
    assert "Score: 10/10" in out
