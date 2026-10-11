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


def test_predicts_powers_before_meeting_them(trained):
    brain, results = trained
    assert results[13]["passed"]
    invent = next(e for e in brain.log if e["kind"] == "invent" and "repeated_groups" in e["text"])
    assert invent["lesson"] == 3                       # ten lessons before the growing world
    assert not brain.library.get("repeated_groups").provenance.get("predicted")
    assert reasoner.arithmetic(brain, "3 power 4").text == "81"


def test_knows_where_the_pattern_stops(trained):
    brain, _ = trained
    assert brain.inventions["ladder"]["stops_at"] == "repeated_groups"
    assert brain.inventions["ladder"]["predicted"] == ["repeated_groups"]


def test_one_shape_discovery_for_three_kinds_of_number(trained):
    brain, _ = trained
    shapes = {inv["shape"] for inv in brain.inventions.values()}
    assert {"line", "cycle", "finer line"} <= shapes
    finer = brain.inventions["finer:cake_balance"]
    # it worked out which input is which by testing, and re-cuts with its own times law
    assert finer["roles"] == {"count": "pieces", "kind": "cut", "whole": "wholes"}
    assert finer["scale"] == "groups"


def test_energy_with_three_parts(trained):
    brain, results = trained
    assert results[14]["passed"]
    law = brain.qlaws["bounce"]
    assert [p for p, _ in law.terms] == [{"y": 1}, {"v": 2}, {"c": 2}]
    assert abs(law.terms[2][1] - 400 / (2 * 2 * 9.81)) < 1e-6    # k / 2mg, found not given


def test_invents_irrational_numbers_and_the_world_agrees(trained):
    brain, results = trained
    assert results[15]["passed"]
    first = next(e for e in brain.log if e["kind"] == "invent" and "GAPS" in e["text"])
    assert first["lesson"] < 15                      # by reasoning, before any tiles
    ans = reasoner.arithmetic(brain, "what power 2 equals 2")
    kind, lo, hi = ans.value
    assert kind == "between" and lo[0] / lo[1] < 2 ** 0.5 < hi[0] / hi[1]
    assert brain.predict("ruler", {"marks": 1000}) == 1414   # predicted, never measured


def test_invents_column_arithmetic(trained):
    brain, _ = trained
    col = next(e for e in brain.log if e["kind"] == "invent" and "column arithmetic" in e["text"])
    assert col["lesson"] == 4
    # each fast path was earned by agreeing with a law on 60 examples
    assert brain.library.fast["groups"][0] == "times"
    assert brain.library.fast["pay"] == ("take away", "yx")
    ans = reasoner.arithmetic(brain, "123456789 times 987654321")
    assert ans.text == "121932631112635269"
    assert reasoner.arithmetic(brain, "2 power 100").text == str(2 ** 100)


def _inside(ans, truth):
    kind, lo, hi = ans.value
    return kind == "between" and lo[0] / lo[1] <= truth <= hi[0] / hi[1]


def test_fractional_repeats(trained):
    brain, _ = trained
    assert "fractional repeats" in brain.inventions
    assert reasoner.arithmetic(brain, "4 power what equals 8").text == "3/2"
    assert reasoner.arithmetic(brain, "8 power 2/3").text == "4"
    assert reasoner.arithmetic(brain, "27 power 1/3").text == "3"
    assert _inside(reasoner.arithmetic(brain, "2 power what equals 3"), 1.5849625)
    assert _inside(reasoner.arithmetic(brain, "5 power what equals 1/3"), -0.6826062)
    assert reasoner.arithmetic(brain, "3 power what equals -1").value is None
