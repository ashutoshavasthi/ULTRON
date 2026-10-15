"""The newborn mind (Age 0, WP3): habituation, memory, sleep, comfort."""

import numpy as np

from ultron.brain.newborn import Newborn
from ultron.judge.nursery_lab import habituated, showings
from ultron.nursery.life import Life
from ultron.nursery.world import Nursery


def test_looking_falls_for_a_familiar_toy_and_comes_back_for_a_new_one():
    times = showings(11)
    assert habituated(times), times


def test_sleep_keeps_what_matters_and_forgets_the_rest():
    w, mind = Nursery(3), Newborn(3)
    life = Life(w, mind)
    stored = {}
    real_sleep = mind.sleep

    def sleep(log=None):
        stored.update(real_sleep(log))
        return stored
    mind.sleep = sleep
    life.day(steps=2500)
    assert stored["before"] >= 10 * stored["after"], stored
    assert mind.vivid and mind.protos
    assert all(p["habit"] == 0.0 for p in mind.protos)    # a new day: fresh eyes


def test_it_remembers_where_it_last_saw_a_thing():
    w, mind = Nursery(4), Newborn(4)
    Life(w, mind).day(steps=1500)
    seen = [p for p in mind.protos if p["where"] is not None]
    assert seen
    p = max(seen, key=lambda q: q["seen"])
    assert mind.where_last(p["what"]) == (p["where"], p["last"])
    assert mind.where_last(np.array([9.0, 9.0, 9.0, 9.0, 9.0])) is None


def test_a_lonely_baby_fusses_and_the_caregiver_comes():
    w, mind = Nursery(5), Newborn(5)
    mind.comfort = 0.2
    senses = w.senses()
    for _ in range(600):
        w.act(mind.act(senses))
        w.step()
        senses = w.senses()
    episodes = [e["episode"] for e in w.caregiver.log]
    assert w.stats["fussing"] > 0
    assert "stroke" in episodes
    assert mind.comfort > 0.6 and not mind.fussing


def test_a_newborn_day_is_the_same_twice():
    a, b = Nursery(6), Nursery(6)
    ma, mb = Newborn(6), Newborn(6)
    Life(a, ma).day(steps=800)
    Life(b, mb).day(steps=800)
    assert a.truth() == b.truth()
    assert ma.vivid == mb.vivid
