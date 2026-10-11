"""Stage 2, V3: real lab films of falling. Seeing what moves, following it while nothing
touches it, and the law of falling with g from real pixels."""

import numpy as np

from ultron.senses import motion


def test_g_from_real_films_of_falling(trained):
    """Lesson 29: the law (change of speed ∝ time) found from three real films, and g
    within twice its measured error of 9.80 m/s², that error at most 3%."""
    brain, results = trained
    r = results[29]
    assert r["passed"]
    assert brain.qlaws["fall"].powers in ({"dv": 1, "tau": -1}, {"dv": -1, "tau": 1})
    assert r["v3"]["passed"] and r["v3"]["films"] == 3
    assert abs(r["g"] - 9.80) <= 2 * r["measured_error"] <= 0.06 * 9.80


def test_following_keeps_a_thing_moving_as_it_was():
    """Two things crossing: each keeps its own course (a nearest-neighbour rule would
    swap them where they meet)."""
    frames = []
    for f in range(20):
        frames.append([(10 + 4 * f, 50.0), (90 - 4 * f, 52.0 + 0.1 * f)])
    tracks = [t for t in motion.follow(frames) if len(t) >= 15]
    assert len(tracks) == 2
    for t in tracks:
        xs = [t[f][0] for f in sorted(t)]
        steps = np.diff(xs)
        assert np.all(steps > 0) or np.all(steps < 0)


def test_on_its_own_only_when_nothing_touches_it_and_wholly_in_view():
    ball = {f: (100.0, 20.0 + 10 * f) for f in range(30)}
    hand = {f: (125.0 + 3 * f, 20.0 + 9 * f) for f in range(6)}        # holds it, lets go
    free = motion.alone(ball, [ball, hand], shape=(260, 300))
    assert min(free) >= 4                       # not while the hand is near
    assert max(free) <= 23                      # not once it reaches the picture's edge


def test_half_pictures_keep_positions_in_full_frame_rows():
    """A dot on row 40 (top half) and one on row 61 (bottom half): each half-picture,
    made full size again, shows its dot where it was."""
    a = np.zeros((100, 20))
    a[40, 10] = 1.0
    a[61, 5] = 1.0
    tf, bf = motion.half_pictures([a])
    top, bottom = tf
    assert top[40, 10] == 1.0 and top[41, 10] == 1.0 and top[:, 5].max() == 0.0
    assert bottom[61, 5] == 1.0 and bottom[62, 5] == 1.0 and bottom[:, 10].max() == 0.0
    assert bf[0] is not None and np.array_equal(bf[0], bottom)
