"""Stage 2, V3-V6: real lab films. Seeing what moves, following it while nothing touches
it, the law of falling with g from real pixels, pendulum periods, and positions against
the lab's own hand marks."""

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


def test_positions_on_par_with_the_labs_hand_marks(trained):
    """V6: on both films the lab marked by hand, Ultron finds the object in at least 90%
    of the marked pictures, within its radius of the marks, and no more scattered about
    a smooth path than 1.5x the lab's own marks."""
    from ultron.judge import footage_checks
    brain, _ = trained
    v6 = footage_checks.v6(brain.eyes)
    assert v6["passed"], v6


def test_pendulum_periods_are_measured_and_judged(trained):
    """V4 is judged, not assumed: both films are timed, the 1 m film agrees with the
    textbook but is too short (one swing) to be precise, and with two lengths the
    square-root law is not claimed."""
    from ultron.judge import footage_checks
    brain, _ = trained
    v4 = footage_checks.v4(brain.eyes)
    assert all(f["measured"] for f in v4["films"].values())
    assert v4["films"]["Pendulum"]["within"] and not v4["films"]["Pendulum"]["precise"]
    assert not v4["sqrt_law_judged"] and not v4["passed"]


def test_a_swing_is_timed_and_its_angle_read_without_a_scale():
    """A bob on a 200 px string swinging 30 degrees each way, period 1.5 s at 30 pictures a
    second: the period from crossings of the middle, the angle from the path's circle."""
    rate, period, length, amp = 30.0, 1.5, 200.0, np.radians(30)
    track = {}
    for f in range(120):
        th = amp * np.cos(2 * np.pi * f / rate / period)
        track[f] = (300 + length * np.sin(th), 50 + length * np.cos(th))
    s = motion.swing(track, rate)
    assert abs(s["period"] - period) < 0.01
    assert abs(np.degrees(s["angle"]) - 30) < 1.0
    assert abs(s["radius_px"] - length) < 1.0
