"""Stage 3, L1: kinds of thing found before words, and words by pointing."""

import random

from ultron.brain.brain import Brain
from ultron.brain.categories import discover, group_of, kinds_of
from ultron.brain.language import learn_lexicon, refer
from ultron.trainer.language_lessons import HELD_OUT, WordsByPointing, holds_out

COLOUR_HUE = {"red": 3.0, "yellow": 57.0, "green": 120.0, "blue": 232.0}


def _measured(thing, rng):
    """What Ultron would measure of a thing, without the camera (for fast tests)."""
    return {"hue": (COLOUR_HUE[thing["colour"]] + rng.uniform(-2, 2)) % 360,
            "size": (40 if thing["size"] == "small" else 130) + rng.uniform(-8, 8),
            "elongation": (3.2 if thing["shape"] == "bar" else 1.05) + rng.uniform(-.1, .1),
            "fill": (0.8 if thing["shape"] == "ball" else 0.92) + rng.uniform(-.02, .02),
            "x": rng.uniform(5, 75), "y": rng.uniform(5, 75)}


def _world(talks=120, seed=0):
    rng = random.Random(seed)
    lesson = WordsByPointing(seed)
    seen = [_measured(t, rng) for _ in range(200) for t in lesson.random_things(3)]
    cats = discover(seen, WordsByPointing.MEASURES)
    heard = []
    for said, _, things, _ in lesson.talks(talks):
        heard.append((said.split(), [kinds_of(cats, _measured(t, rng)) for t in things]))
    return lesson, cats, heard, rng


def test_kinds_are_found_and_even_spreads_are_not_split():
    _, cats, _, _ = _world(talks=1)
    groups = {m: len(c["groups"]) for m, c in cats.items()}
    assert groups == {"hue": 4, "size": 2, "elongation": 2, "fill": 2, "x": 1, "y": 1}


def test_colour_circle_wraps():
    rng = random.Random(1)
    vals = [{"hue": (rng.choice([0.0, 120.0]) + rng.uniform(-3, 3)) % 360} for _ in range(80)]
    cats = discover(vals, ["hue"])
    assert len(cats["hue"]["groups"]) == 2      # reds on both sides of 0 are one group
    assert group_of(cats, "hue", 359.5) == group_of(cats, "hue", 0.5)


def test_teaching_never_says_a_held_out_pair():
    lesson = WordsByPointing(3)
    for said, _, things, target in lesson.talks(200):
        assert not holds_out(said.split())
        assert said.split()[-1] == things[target]["shape"]
    for said, _, _, _ in lesson.talks(50, held_out=True):
        assert holds_out(said.split())
    assert len(HELD_OUT) == 7


def _brain_with(cats, heard):
    lexicon, rivals = learn_lexicon(heard, cats, rivals=True)
    b = Brain()
    b.categories = cats
    for w, m in lexicon.items():
        b.bind(w, ("look", [list(p) for p in m]))
    b.rival_lexicons = [{w: [list(p) for p in m] for w, m in r.items() if m != lexicon[w]}
                        for r in rivals]
    return b, lexicon


def test_words_learned_and_used_in_combinations_never_heard():
    lesson, cats, heard, rng = _world()
    b, lexicon = _brain_with(cats, heard)
    assert lexicon["the"] == ()
    assert len(lexicon["red"]) == 1 and lexicon["red"][0][0] == "hue"
    assert len(lexicon["big"]) == 1 and lexicon["big"][0][0] == "size"
    right = gave = 0
    for said, _, things, target in WordsByPointing(99).talks(100, held_out=True):
        got, _ = refer(b, said, [_measured(t, rng) for t in things])
        gave += got is not None
        right += got == target
    assert right == gave            # never wrong
    assert right >= 95


def test_a_word_never_taught_is_refused():
    lesson, cats, heard, rng = _world()
    b, _ = _brain_with(cats, heard)
    things = [_measured(t, rng) for t in lesson.random_things(3)]
    got, why = refer(b, "the purple ball", things)
    assert got is None and "purple" in why


def test_not_sure_when_heard_too_little():
    """With very few sentences, rival accounts disagree and it says so, not guesses."""
    _, cats, heard, rng = _world(talks=12, seed=5)
    b, _ = _brain_with(cats, heard)
    right = gave = 0
    for said, _, things, target in WordsByPointing(98).talks(60, held_out=True):
        got, _ = refer(b, said, [_measured(t, rng) for t in things])
        gave += got is not None
        right += got == target
    assert gave < 60
    assert right >= 0.9 * gave


def test_lesson_30_exam(trained):
    """L1 on the trained brain: held-out combinations, words never taught, quick learning,
    a 20-point margin over both baselines, and never a wrong answer."""
    r = trained[1][30]
    assert r["passed"]
    right, gave = r["precision"]
    assert right == gave
    assert r["margin_over_baselines"] >= 0.20


def test_words_failure_lab_breakpoints_stay(trained):
    """Breakpoints found by the failure lab (2026-10-11) must never move back, and in no
    row does it give a wrong answer."""
    from ultron.judge import failures
    rows = {r["level"]: r for r in failures.words_stress(trained[0])["rows"]}
    for level in ("0% of sentences name the wrong thing", "5% of sentences name the wrong thing",
                  "10% of sentences name the wrong thing", "120 sentences heard"):
        assert rows[level]["ok"], level
    for r in rows.values():
        assert r["right"] == r["gave"], r["level"]
