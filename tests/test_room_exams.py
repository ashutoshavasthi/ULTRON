"""Level 0's seeing test (L0-1): the Judge's scenes, its retina, the baseline."""

from ultron.judge import room_exams as X


def test_scenes_are_the_same_twice_and_hold_every_toy_whole():
    for seed in X.DEV_SEEDS[:6]:
        a, toys_a = X.scene(seed)
        b, toys_b = X.scene(seed)
        assert [t["id"] for t in toys_a] == [t["id"] for t in toys_b]
        assert a.truth()["things"] == b.truth()["things"]
        _, truth = X.glance(a, toys_a)
        for (x, y), t in zip(truth, toys_a):
            assert t["hx"] <= x <= 64 - t["hx"] and t["hy"] <= y <= 48 - t["hy"]


def test_exam_seeds_are_kept_apart():
    assert min(X.EXAM_SEEDS) >= 8001
    assert max(X.DEV_SEEDS + X.FRESH_SEEDS) < 8001


def test_its_retina_sees_far_better_than_bright_spots():
    seeds = X.DEV_SEEDS[:10]
    retina = X.seeing(X.by_retina, seeds)
    bright = X.seeing(X.by_brightness, seeds)
    assert retina[0] > bright[0] and retina[1] > bright[1]
