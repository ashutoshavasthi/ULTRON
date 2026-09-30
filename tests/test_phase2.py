from ultron.brain import reasoner


def test_same_code_finds_a_line_and_a_cycle(trained):
    brain, results = trained
    assert results[11]["passed"]
    assert brain.inventions["line:earn/spend"]["shape"] == "line"
    assert brain.inventions["cycle:tick"]["shape"] == "cycle"
    assert brain.inventions["cycle:tick"]["size"] == 6
    assert brain.library.cycles == {"tick": 6}


def test_clock_arithmetic(trained):
    brain, _ = trained
    assert reasoner.arithmetic(brain, "100 after 3").text == "1"
    assert reasoner.arithmetic(brain, "-2 after 3").text == "1"
    assert reasoner.arithmetic(brain, "what after 4 equals 1").text == "3"


def test_no_such_position(trained):
    brain, _ = trained
    ans = reasoner.arithmetic(brain, "2 after 9")
    assert ans.value is None and "no position 9" in ans.text
    ans = reasoner.arithmetic(brain, "what after 9 equals 1")
    assert ans.value is None and "no position 9" in ans.text


def test_invents_energy(trained):
    from ultron.brain.invariants import SumLaw
    brain, results = trained
    assert results[12]["passed"]
    law = brain.qlaws["roll"]
    assert isinstance(law, SumLaw) and law.a == {"y": 1} and law.b == {"v": 2}
    assert abs(law.coef - 1 / (2 * 9.81)) < 1e-6      # it found gravity's 1/2g itself
    assert "m" not in law.variables()                    # mass plays no part


def test_energy_answers_new_kinds_of_question(trained):
    brain, results = trained
    names = [i["name"] for i in results[12]["items"]]
    assert any("thrown straight up" in n for n in names)
    assert all(i["scores"]["ultron"][0] == i["scores"]["ultron"][1] for i in results[12]["items"])
