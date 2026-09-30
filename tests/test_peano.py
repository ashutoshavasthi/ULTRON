from ultron.brain.dsl import Law, Library, INT
from ultron.logic import peano

ADD = Law("merge", ["nA", "nB"], ("iter", ("succ",), ("var", "nA"), ("var", "nB")), INT)


def test_proves_and_checks_addition():
    lib = Library()
    lib.add(ADD)
    rules = peano.all_rules(lib)
    lhs = ("merge", peano.numeral(3), peano.numeral(4))
    steps = peano.prove(lhs, rules)
    assert peano.value(steps[-1]["after"]) == 7
    ok, _ = peano.check(lhs, 7, steps, rules)
    assert ok


def test_checker_rejects_a_forged_step():
    lib = Library()
    lib.add(ADD)
    rules = peano.all_rules(lib)
    lhs = ("merge", peano.numeral(2), peano.numeral(2))
    steps = peano.prove(lhs, rules)
    steps[-1] = dict(steps[-1], after=peano.numeral(5))
    ok, _ = peano.check(lhs, 5, steps, rules)
    assert not ok
