from ultron.brain.dsl import INT, BOOL, Law, Library, evaluate, show
from ultron.brain.synth import synthesize


def _add_examples():
    pairs = [(2, 1), (3, 2), (0, 4), (5, 5), (1, 3), (4, 0)]
    return [{"nA": a, "nB": b} for a, b in pairs], [a + b for a, b in pairs]


def test_finds_addition_from_six_examples():
    inputs, targets = _add_examples()
    r = synthesize(inputs, targets, {"nA": INT, "nB": INT}, INT, Library())
    assert r.expr is not None and r.expr[0] == "iter"
    lib = Library()
    for a, b in [(17, 26), (100, 1), (0, 0)]:
        assert evaluate(r.expr, {"nA": a, "nB": b}, lib) == a + b


def test_multiplication_needs_the_addition_law():
    inputs, targets = _add_examples()
    lib = Library()
    lib.add(Law("merge", ["nA", "nB"],
                synthesize(inputs, targets, {"nA": INT, "nB": INT}, INT, lib).expr, INT))
    pairs = [(2, 3), (4, 1), (0, 5), (3, 3), (1, 4), (4, 4)]
    inp = [{"groups": g, "size": s} for g, s in pairs]
    out = [g * s for g, s in pairs]
    with_lib = synthesize(inp, out, {"groups": INT, "size": INT}, INT, lib)
    assert with_lib.expr is not None
    assert evaluate(with_lib.expr, {"groups": 13, "size": 17}, lib) == 221
    blank = synthesize(inp, out, {"groups": INT, "size": INT}, INT, Library())
    assert blank.expr is None


def test_shortest_explanation_wins():
    inputs = [{"nA": a, "nB": b} for a, b in [(1, 1), (2, 3), (4, 4), (0, 2)]]
    r = synthesize(inputs, [a == b for a, b in [(1, 1), (2, 3), (4, 4), (0, 2)]],
                   {"nA": INT, "nB": INT}, BOOL, Library())
    assert show(r.expr) == "eq(nA, nB)"


def test_search_is_deterministic():
    inputs, targets = _add_examples()
    a = synthesize(inputs, targets, {"nA": INT, "nB": INT}, INT, Library())
    b = synthesize(inputs, targets, {"nA": INT, "nB": INT}, INT, Library())
    assert a.expr == b.expr and a.steps == b.steps
