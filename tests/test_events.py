"""Stage 3, L2: words for what happens, bound to its own kinds of law and to quantities
it measures (the heavier one by its momentum law)."""

import random

from ultron.brain import events
from ultron.brain.brain import Brain
from ultron.brain.invariants import ConservationLaw
from ultron.brain.language import learn_relations, name_with, relate_with
from ultron.senses import floor as fl
from ultron.trainer.language_lessons import (EVENT_HELD_OUT, RELATION_HELD_OUT, VERBS,
                                             WordsForWhatHappens, held_out_in)

KINDS = [("nothing changes", events.STILL, ""), ("equal steps", events.STEADY, ""),
         ("kind 1", {"y_ops": ["Δ", "ρ"], "x_op": None}, ""),
         ("kind 7", {"y_ops": ["Δ", "Δ"], "x_op": None}, "")]


def _track(xs, ys, noise=0.05, seed=0):
    rng = random.Random(seed)
    return {"t": list(range(len(xs))), "x": [x + rng.gauss(0, noise) for x in xs],
            "y": [y + rng.gauss(0, noise) for y in ys], "reach": 4.0, "reach_y": 4.0}


def test_a_fall_is_steps_changing_evenly_then_rest():
    ys = fl.fall(3, 20.0, 70.0)
    m = events.motion(_track([40.0] * fl.FRAMES, ys), KINDS)
    assert KINDS[m["updown"]][0] == "kind 7"
    assert m["across"] == 0 and m["turns back"] == 0
    assert abs(m["start"] - 4) <= 1


def test_a_bounce_comes_back_and_a_slide_settles():
    m = events.motion(_track([40.0] * fl.FRAMES, fl.fall(0, 20.0, 70.0, 0.7)), KINDS)
    assert m["turns back"] == 1 and KINDS[m["updown"]][0] == "kind 7"
    m = events.motion(_track(fl.slide(2, 10.0, 3.0, 0.8), [70.0] * fl.FRAMES), KINDS)
    assert KINDS[m["across"]][0] == "kind 1" and m["updown"] == 0
    m = events.motion(_track(fl.roll(0, 10.0, 1.5), [70.0] * fl.FRAMES), KINDS)
    assert KINDS[m["across"]][0] == "equal steps"


def test_a_still_thing_does_not_move():
    for seed in range(5):
        m = events.motion(_track([30.0] * fl.FRAMES, [50.0] * fl.FRAMES, 0.1, seed), KINDS)
        assert m["across"] == 0 and m["updown"] == 0 and m["start"] is None


def test_turns():
    assert events._turns([0, 1, 2, 3, 2, 1, 0, 1, 2]) == 2
    assert events._turns([0, 0.5, 0.2, 0.6]) == 0           # under a pixel: no turn


def test_how_heavy_from_the_momentum_law():
    """Two things knock; its law Σ m·v says the ratio of their masses."""
    brain = Brain()
    brain.claws = {"collide": [ConservationLaw("collide", {"m": 1, "v": 1}, "all")]}
    for ma, mb in ((1.0, 2.5), (3.0, 1.2)):
        xa, xb, met = fl.collide(10.0, 1.5, 50.0, -0.5, ma, mb, 0.9, 8.0)
        raw = []
        for xs, seed in ((xa, 1), (xb, 2)):
            tr = _track(xs, [70.0] * fl.FRAMES, 0.05, seed)
            keep = [n for n in tr["t"] if abs(n - met) > 1.5]
            for k in ("t", "x", "y"):
                tr[k] = [tr[k][n] for n in keep]
            raw.append((tr, events.motion(tr, KINDS)))
        when = (int(met) - 1, int(met) + 2)
        got = events._meetings(brain, raw, KINDS, {(0, 1): when})
        logratio, sure, _ = got["0,1"]
        assert abs(2 ** logratio - ma / mb) < 0.1 * ma / mb
        assert sure < 0.1


def _film(qa, qb):
    return {"things": [{"q": qa}, {"q": qb}], "masses": {}}


def test_comparing_words_bind_to_the_quantity_that_always_holds():
    rng = random.Random(3)
    heard = []
    for k in range(60):
        word = ["faster", "before", "more"][k % 3]
        sa, sb = rng.uniform(0.5, 2), rng.uniform(0.5, 2)
        ta, tb = rng.randint(0, 10), rng.randint(0, 10)
        if word == "faster":
            sa, sb = max(sa, sb) * 1.4, min(sa, sb)
        if word == "before":
            ta, tb = min(ta, tb), max(ta, tb) + 3
        film = _film({"speed": [sa, 0.01], "start": [ta, 0.5], "count": [1, 0]},
                     {"speed": [sb, 0.01], "start": [tb, 0.5], "count": [1, 0]})
        if word == "more":
            film = {"things": [{"q": {}}] * 5, "masses": {}}
            heard.append(([word, "than"], film, [0, 1, 2], [3, 4]))
        else:
            heard.append(([word, "than"], film, [0], [1]))
    best, rivals = learn_relations(heard, rivals=True)
    assert best["faster"] == ("speed", ">")
    assert best["before"] == ("start", "<")
    assert best["more"] == ("count", ">")
    assert best["than"] is None
    film = _film({"speed": [2.0, 0.01], "start": [3, 0.5], "count": [1, 0]},
                 {"speed": [1.0, 0.01], "start": [3, 0.5], "count": [1, 0]})
    assert relate_with(best, rivals, film, [0], [1]) == ["faster"]


def test_teaching_never_shows_a_held_out_pair():
    lesson = WordsForWhatHappens(4)
    for said, _, things, target in lesson.event_talks(40):
        assert said.split()[-1] in VERBS
        for t in things:
            if t.get("event") in VERBS:
                assert not any((w, t["event"]) in EVENT_HELD_OUT
                               for w in (t["colour"], t["size"], t["shape"]))
    for said, _, things, target in lesson.event_talks(10, held_out=True):
        t = things[target]
        assert any((w, t["event"]) in EVENT_HELD_OUT for w in (t["colour"], t["size"], t["shape"]))
    for said, *_ in lesson.relation_talks(30):
        assert not held_out_in(said.split(), RELATION_HELD_OUT)
    for said, *_ in lesson.relation_talks(12, held_out=True):
        assert held_out_in(said.split(), RELATION_HELD_OUT)


def test_lesson_30_exam(trained):
    """L2 on the trained brain: what happens named right >= 90% in new films about things
    never seen doing it; comparing words filled in right >= 90%."""
    r = trained[1][30]
    assert r["passed"]
    assert sorted(r["event_words"]) == sorted(VERBS)


def test_naming_says_when_it_cannot_tell():
    lexicon = {"falls": (("updown", 4),), "rolls": (("across", 1),)}
    falling = {"across": 0, "updown": 4, "turns back": 0}
    assert name_with(lexicon, [], falling, [falling])[0] == "falls"
    # a word for what happens whose meaning it hasn't found might be the word for this
    assert name_with(dict(lexicon, bounces=()), [], falling, [falling])[0] is None
    # two words that seem to mean the same: it can't tell which to say
    assert name_with(dict(lexicon, drops=(("updown", 4),)), [], falling, [falling])[0] is None
    # it never saw the thing do anything
    still = {"across": 0, "updown": 0, "turns back": 0}
    assert name_with({"stays": (("across", 0),)}, [], still, [still])[0] is None


def test_events_failure_lab_breakpoints_stay(trained):
    """Breakpoints found by the failure lab (2026-10-11) must never move back, and in no
    row does it give a wrong answer."""
    from ultron.judge import failures
    rows = {r["level"]: r for r in failures.events_stress(trained[0])["rows"]}
    for level in ("0% of event sentences say the wrong word",
                  "10% of event sentences say the wrong word", "50 event sentences heard",
                  "25 event sentences heard", "0% of comparing sentences say the wrong word",
                  "10% of comparing sentences say the wrong word"):
        assert rows[level]["ok"], level
    for r in rows.values():
        assert r["right"] == r["gave"], r["level"]
