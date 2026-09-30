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
