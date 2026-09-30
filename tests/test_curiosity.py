from ultron.brain.curiosity import NOVELTY_TRIES, Curiosity


def test_moves_on_from_mastered_things():
    c = Curiosity()
    for e in [1, 1, 0] + [0] * 20:
        c.record("easy", e)
    assert c.choose(["easy"]) is None


def test_abandons_pure_noise():
    c = Curiosity()
    for i in range(NOVELTY_TRIES + 8):
        c.record("noise", 1.0 if i % 10 else 0.0)
    assert c.choose(["noise"]) is None


def test_prefers_what_is_being_learned():
    c = Curiosity()
    for i in range(NOVELTY_TRIES):
        c.record("learning", 1.0 if i < 12 else 0.0)
        c.record("noise", 1.0)
    assert c.choose(["noise", "learning"]) == "learning"


def test_designs_rich_experiments_not_degenerate_ones():
    from ultron.brain.brain import Brain
    from ultron.brain.memory import Spec
    from ultron.brain.dsl import INT
    b = Brain()
    b.meet(Spec("f", "program", {"x": INT, "y": INT}, "out", out_type=INT))
    b.hypotheses["f"] = ("var", "x")
    b.rivals["f"] = [("var", "y")]
    options = [{"x": x, "y": y} for x in range(4) for y in range(4)]
    pick = b.propose("f", options)
    assert pick == {"x": 2, "y": 3}     # splits the ideas, with the biggest numbers (3,3 cannot)
