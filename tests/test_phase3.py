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
