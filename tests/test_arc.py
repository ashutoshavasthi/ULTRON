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
