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
