"""ARC-AGI: grid perception, operations, the solver, and evaluation discipline."""

import numpy as np
import pytest

from ultron.arc import data, ops, solve
from ultron.arc.grid import background, parts, things


def g(rows):
    return np.array(rows, dtype=np.int8)


def test_perception():
    x = g([[0, 1, 1, 0], [0, 1, 0, 0], [0, 0, 0, 2]])
    assert background(x) == 0
    ts = things(x)
    assert sorted(t.size for t in ts) == [1, 3]
    split = g([[1, 0, 5, 2, 2], [1, 1, 5, 0, 2]])
    assert [p.tolist() for p in parts(split)] == [[[1, 0], [1, 1]], [[2, 2], [0, 2]]]


def test_operations():
    x = g([[0, 0, 0, 0], [0, 3, 3, 0], [0, 3, 0, 0], [0, 0, 0, 0]])
    assert ops.crop_content(x).tolist() == [[3, 3], [3, 0]]
    ring = g([[0, 0, 0, 0, 0], [0, 2, 2, 2, 0], [0, 2, 0, 2, 0], [0, 2, 2, 2, 0], [0, 0, 0, 0, 0]])
    assert ops.fill_enclosed(ring, 4)[2, 2] == 4
    assert ops.gravity(g([[1, 0], [0, 0]]), "down").tolist() == [[0, 0], [1, 0]]
    assert ops.upscale(g([[1, 2]]), 2).tolist() == [[1, 1, 2, 2], [1, 1, 2, 2]]
    assert ops.downscale(g([[1, 1, 2, 2], [1, 1, 2, 2]]), 2).tolist() == [[1, 2]]


def test_solver_finds_a_two_step_rule():
    # the rule: flip left-right, then fill enclosed holes with 4
    train = []
    rng = np.random.default_rng(0)
    for _ in range(3):
        x = np.zeros((7, 7), dtype=np.int8)
        r, c = rng.integers(0, 4, size=2)
        x[r:r + 3, c:c + 3] = 2
        x[r + 1, c + 1] = 0
        x[0, 6] = 1
        train.append((x, ops.fill_enclosed(x[:, ::-1], 4)))
    test = np.zeros((7, 7), dtype=np.int8)
    test[3:6, 1:4] = 2
    test[4, 2] = 0
    test[6, 0] = 1
    attempts, used, _ = solve.predict(train, [test])
    want = ops.fill_enclosed(test[:, ::-1], 4)
    assert any(np.array_equal(a, want) for a in attempts[0])


def test_learned_colour_map():
    train = [(g([[1, 2], [3, 1]]), g([[5, 6], [4, 5]])), (g([[2, 3]]), g([[6, 4]]))]
    attempts, _, _ = solve.predict(train, [g([[3, 2, 1]])])
    assert attempts[0][0].tolist() == [[4, 6, 5]]


def test_evaluation_split_is_locked():
    with pytest.raises(data.EvaluationLocked):
        data.load("arc1", "evaluation")


def test_hand_written_operations_are_frozen():
    # new abilities must come from Ultron's own library learning, not from its designer
    ctx = {"out_colours": [1, 2], "in_colours": [1, 2], "scales_up": [2], "scales_down": [2],
           "tiles": [(2, 2)], "ratios": [((2, 1), (2, 1))]}
    names = {n for n, _, _ in ops.registry(ctx)}
    assert names == set(ops.FROZEN) and len(ops.FROZEN) == 38


def test_library_learns_a_recurring_piece_and_uses_it():
    from ultron.arc import library
    # three solved tasks share "flip, then fill holes" (with different colours)
    programs = {"a": [["flip_h", None], ["fill_enclosed", 4]],
                "b": [["flip_h", None], ["fill_enclosed", 3]],
                "c": [["flip_h", None], ["fill_enclosed", 6], ["rot90", None]],
                "d": [["rot180", None]]}
    blocks = library.learn(programs)
    top = blocks[0]
    assert top["steps"] == [["flip_h", None], ["fill_enclosed", "C"]] and top["uses"] == 3
    # a piece used once is never worth its own description
    assert all(b["uses"] >= 2 for b in blocks)
    # as one step, the block makes a 3-operation program a 2-step one, so it is preferred
    from ultron.arc import grid
    grid.TASK_BACKGROUND[0] = 0
    train = []
    rng = np.random.default_rng(1)
    for _ in range(3):
        x = np.zeros((7, 7), dtype=np.int8)
        r, c = rng.integers(0, 4, size=2)
        x[r:r + 3, c:c + 3] = 2
        x[r + 1, c + 1] = 0
        x[0, 6] = 1
        train.append((x, ops.flip_v(ops.fill_enclosed(x[:, ::-1], 4), None)))
    solve.LIBRARY[0] = [top]
    try:
        found, _ = solve.solve(train, max_depth=3)
    finally:
        solve.LIBRARY[0] = None
    assert found and any(n.startswith("block") for n, _ in found[0])


def test_thing_law_with_a_default_and_marks_around_things():
    from ultron.arc import grid, objects
    grid.TASK_BACKGROUND[0] = 0
    # things with a hole turn 3; solid things stay as they are
    def pic(holed, solid):
        x = np.zeros((9, 9), dtype=np.int8)
        for r, c, w in holed:
            x[r:r + 3, c:c + w] = 1
            x[r + 1, c + 1:c + w - 1] = 0
        for r, c, h, w in solid:
            x[r:r + h, c:c + w] = 1
        return x
    train = []
    for holed, solid in [([(0, 0, 3)], [(5, 5, 2, 2)]), ([(4, 4, 4), (0, 5, 3)], [(0, 0, 3, 3)]),
                         ([(5, 0, 4)], [(0, 0, 1, 3), (0, 6, 2, 3)])]:
        x = pic(holed, solid)
        y = x.copy()
        for r, c, w in holed:
            y[r:r + 3, c:c + w][x[r:r + 3, c:c + w] == 1] = 3
        train.append((x, y))
    law = objects.learn([i for i, _ in train], [o for _, o in train])
    assert law is not None and law[1] == ("holes",)
    test = pic([(6, 6, 3)], [(0, 0, 2, 2), (3, 3, 2, 3)])
    out = objects.apply(law, test)
    assert (out[6:9, 6:9][test[6:9, 6:9] == 1] == 3).all() and (out[0:2, 0:2] == 1).all()
    # every red dot gets four yellow corners; nothing else is painted
    train = []
    for dots in ([(2, 2), (6, 5)], [(1, 6), (5, 2)], [(4, 4)]):
        x = np.zeros((8, 8), dtype=np.int8)
        y = x.copy()
        for r, c in dots:
            x[r, c] = y[r, c] = 2
            for dr in (-1, 1):
                for dc in (-1, 1):
                    y[r + dr, c + dc] = 4
        train.append((x, y))
    rule = objects.learn_marks([i for i, _ in train], [o for _, o in train])
    assert rule is not None
    t = np.zeros((8, 8), dtype=np.int8)
    t[3, 3] = 2
    out = objects.apply_marks(rule, t)
    assert out is not None and int((out == 4).sum()) == 4 and out[2, 2] == 4
