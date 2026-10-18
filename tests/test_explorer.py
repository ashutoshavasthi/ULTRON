"""The explorer (Level 0, WP3): attention, memory, sleep."""

import numpy as np

from ultron.brain.explorer import Explorer
from ultron.judge.room_lab import habituated, showings
from ultron.room.life import Life
from ultron.room.world import Room


def test_looking_falls_for_a_familiar_toy_and_comes_back_for_a_new_one():
    times = showings(11)
    assert habituated(times), times


def test_sleep_keeps_what_matters_and_forgets_the_rest():
    w, mind = Room(3), Explorer(3)
    life = Life(w, mind)
    stored = {}
    real_sleep = mind.sleep

    def sleep(log=None):
        stored.update(real_sleep(log))
        return stored
    mind.sleep = sleep
    life.day()                      # one full day, as L0-4 is defined
    assert stored["before"] >= 10 * stored["after"], stored
    assert mind.vivid and mind.protos
    assert all(p["habit"] == 0.0 for p in mind.protos)    # a new day: fresh eyes


def test_it_remembers_where_it_last_saw_a_thing():
    w, mind = Room(4), Explorer(4)
    Life(w, mind).day(steps=1500)
    seen = [p for p in mind.protos if p["where"] is not None]
    assert seen
    p = max(seen, key=lambda q: q["seen"])
    assert mind.where_last(p["what"]) == (p["where"], p["last"])
    assert mind.where_last(np.array([9.0, 9.0, 9.0, 9.0, 9.0])) is None


def test_a_day_is_the_same_twice():
    a, b = Room(6), Room(6)
    ma, mb = Explorer(6), Explorer(6)
    Life(a, ma).day(steps=800)
    Life(b, mb).day(steps=800)
    assert a.truth() == b.truth()
    assert ma.vivid == mb.vivid
