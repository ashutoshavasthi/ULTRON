from fractions import Fraction

from ultron.brain import dsl, reasoner


def _between(ans):
    lo, hi = ans.text.replace("between ", "").split(" and ")
    return Fraction(lo), Fraction(hi)


def test_invents_column_arithmetic(trained):
    brain, results = trained
    assert results[18]["passed"]
    assert brain.inventions["columns"]["shape"] == "algorithm"
    labels = {label for label, _ in brain.library.fast.values()}
    assert {"add", "times", "repeated times"} <= labels


def test_huge_numbers_exact_and_cheap(trained):
    brain, _ = trained
    before = dsl.STEPS[0]
    a = reasoner.arithmetic(brain, "123456789123 times 987654321987")
    assert a.text == str(123456789123 * 987654321987)
    assert reasoner.arithmetic(brain, "3 power 40").text == str(3 ** 40)
    assert dsl.STEPS[0] - before < 1_000_000          # counting it out would take ~10^23 steps


def test_fractional_repeats_have_meaning(trained):
    brain, _ = trained
    assert "fractional repeats" in brain.inventions
    assert reasoner.arithmetic(brain, "8 power 2/3").text == "4"
    lo, hi = _between(reasoner.arithmetic(brain, "5 power 2/3"))
    assert lo ** 3 < 25 < hi ** 3                     # 5^(2/3) cubed is 25
    assert hi - lo <= Fraction(1, 50)


def test_logarithms_pinned(trained):
    brain, _ = trained
    lo, hi = _between(reasoner.arithmetic(brain, "2 power what equals 3"))
    assert lo < Fraction(158496, 100000) < hi and hi - lo <= Fraction(1, 50)


def test_law_about_a_law(trained):
    brain, results = trained
    assert results[17]["passed"]
    meta = brain.qlaws["coil_stretch~why"]
    assert abs(meta.constant - 600) < 1e-6
    assert brain.inventions["why:coil_stretch"]["shape"] == "law about a law"


def test_spring_never_stretched_and_backward_chain(trained):
    brain, results = trained
    items = {i["name"]: i for i in results[17]["items"]}
    for name, item in items.items():
        assert item["scores"]["ultron"][0] == item["scores"]["ultron"][1], name


def test_energy_between_two_moments(trained):
    brain, _ = trained
    v = reasoner.physics(brain, "v", {"y0": 5, "v0": 0, "y": 0}).value
    assert abs(v - (2 * 9.81 * 5) ** 0.5) < 1e-3
    v0 = reasoner.physics(brain, "v0", {"y0": 0, "y": 3, "v": 2}).value
    assert abs(v0 - (4 + 2 * 9.81 * 3) ** 0.5) < 1e-3              # a start value, backwards
    c = reasoner.physics(brain, "c", {"y0": 1, "v0": 0, "y": 0, "v": 0}).value
    assert abs(c - (2 * 2 * 9.81 * 1 / 400) ** 0.5) < 1e-3          # squash: unstated c0 is 0
    assert reasoner.physics(brain, "v", {"y0": 2, "v0": 0, "y": 3}).value is None
    assert reasoner.physics(brain, "v", {"y": 0}).value is None     # nothing about the start


def test_momentum_any_unknown(trained):
    brain, _ = trained
    q = {"m1": 3, "v1": 5, "v2": 0, "v1_after": 1, "v2_after": 2}
    assert abs(reasoner.physics(brain, "m2", q).value - 6) < 1e-9
    q = {"m1": 4, "m2": 2, "v2": -3, "v1_after": 0.5, "v2_after": 2}
    assert abs(reasoner.physics(brain, "v1", q).value - 3) < 1e-9


def test_counted_answers_say_so(trained):
    brain, _ = trained
    assert "counted" in reasoner.physics(brain, "coils", {"F": 50, "x": 0.5}).text
    assert "whole coils" in reasoner.physics(brain, "coils", {"F": 36, "x": 0.4}).text


def test_blind_failures_stay_fixed(trained):
    """Questions from the independent examiners that Ultron once got wrong."""
    brain, _ = trained
    ask = lambda q: reasoner.arithmetic(brain, q)
    assert ask("what plus 314159265358979 equals 271828182845904").text == "-42331082513075"
    assert ask("what times 7 equals 1234567").text == "1234567/7"
    assert ask("27/8 power -2/3").text == "4/9"
    assert ask("5/6 divided what equals -10/3").text == "-1/4"
    assert ask("what divided 2 equals 3").text == "6"
    assert ask("0 divided 0").value is None                      # every amount works
    assert ask("0 power -1").value is None                       # nothing undoes times 0
    assert reasoner.physics(brain, "a", {"x": 0, "m": 5}, {"spring": "S2"}).value == 0
    assert reasoner.physics(brain, "a", {"F": 10, "m": 0}).value is None


def test_independent_blind_tests_pass(trained):
    """Written by examiners who never saw code, tests or exams (see blind/SYLLABUS.md)."""
    import pathlib
    from ultron.__main__ import score_blind
    for name in ("independent_1.txt", "independent_2.txt"):
        path = pathlib.Path(__file__).parent.parent / "blind" / name
        right, total, _ = score_blind(trained[0], path.read_text())
        assert right == total, name
