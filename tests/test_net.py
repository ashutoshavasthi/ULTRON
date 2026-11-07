"""Engine 2 (Ultron's own network) and the judge."""

import numpy as np
import pytest

torch = pytest.importorskip("torch")

from ultron.arc import judge                     # noqa: E402
from ultron.arc.net import data                  # noqa: E402
from ultron.arc.net.model import Recursive       # noqa: E402


def _grid(rng, h, w):
    return rng.integers(0, 10, size=(h, w)).astype(np.int8)


def test_grids_survive_encoding():
    rng = np.random.default_rng(0)
    for h, w in ((1, 1), (3, 7), (30, 30), (29, 1), (12, 30)):
        g = _grid(rng, h, w)
        assert np.array_equal(data.decode(data.encode(g)), g)


def test_every_view_can_be_undone_exactly():
    rng = np.random.default_rng(1)
    g = _grid(rng, 5, 8)
    for view in data.views(40, seed=2):
        assert np.array_equal(data.undo(data.apply(g, view), view), g)
    assert data.views(5, 3)[0][0] == 0                       # the first view is the identity


def test_tested_puzzles_never_give_away_their_answers():
    rng = np.random.default_rng(3)
    secret = np.full((4, 4), 7, dtype=np.int8)
    tasks = {
        "learn": {"train": [(_grid(rng, 3, 3), _grid(rng, 3, 3))],
                  "test": [(_grid(rng, 3, 3), _grid(rng, 3, 3))]},
        "held": {"train": [(_grid(rng, 3, 3), _grid(rng, 3, 3))],
                 "test": [(_grid(rng, 4, 4), secret)]},
    }
    ds = data.pairs(tasks, ["learn"], ["held"], n_views=6, seed=0)
    secrets = {data.encode(data.apply(secret, v)).astype(np.uint8).tobytes()
               for v in ds["views"]}
    assert not any(y.tobytes() in secrets for y in ds["y"])
    with pytest.raises(ValueError):
        data.pairs(tasks, ["learn", "held"], ["held"])


def test_a_tiny_network_can_learn_one_puzzle():
    torch.manual_seed(0)
    rng = np.random.default_rng(4)
    pairs = [(_grid(rng, 3, 3), None) for _ in range(2)]
    pairs = [(i, np.rot90(i)) for i, _ in pairs]
    x = torch.from_numpy(np.stack([data.encode(i) for i, _ in pairs]))
    y = torch.from_numpy(np.stack([data.encode(o) for _, o in pairs]))
    pid = torch.zeros(2, dtype=torch.long)
    model = Recursive(1, hidden=48, heads=4, layers=2, H=1, L=1)
    opt = torch.optim.AdamW(model.parameters(), lr=3e-3)
    for _ in range(150):
        emb = model.embed(x, pid)
        yy, zz = model.start(emb)
        _, _, logits = model.step(emb, yy, zz)
        loss = torch.nn.functional.cross_entropy(logits.reshape(-1, data.VOCAB), y.reshape(-1))
        opt.zero_grad()
        loss.backward()
        opt.step()
    pred = model.predict(x, pid, 1)
    assert all(np.array_equal(data.decode(p.numpy()), o) for p, (_, o) in zip(pred, pairs))


def test_the_judge_needs_enough_agreeing_views():
    a, b = np.zeros((2, 2), np.int8), np.ones((2, 2), np.int8)
    tasks = {"t": {"train": [], "test": [(a, b)]}}
    votes = {("t", 0): [(b, 3)]}
    assert judge.combine({}, votes, tasks, ["t"], k=4) == {"t": [[]]}
    got = judge.combine({}, votes, tasks, ["t"], k=3)
    assert np.array_equal(got["t"][0][0], b)
    assert judge.outcomes(got, tasks) == {"t": 1}
    wrong = judge.combine({"t": [[a]]}, {}, tasks, ["t"], k=1)
    assert judge.outcomes(wrong, tasks) == {"t": -1}
    assert judge.summary({"t": 1, "u": -1, "v": 0})["precision"] == 0.5
