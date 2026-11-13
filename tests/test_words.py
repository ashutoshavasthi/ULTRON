"""Learned words (docs/MECHANISM.md): small checks of each part. The measured result is
gate G0 (`python -m ultron words g0`, reports/words_g0.md), not these tests."""

import random

import numpy as np
import pytest

torch = pytest.importorskip("torch")

from ultron.arc import ops  # noqa: E402
from ultron.words import crystallise, curriculum, learn, search, state  # noqa: E402
from ultron.words.interpreter import Interpreter  # noqa: E402
from ultron.words.vocab import ARGS, HIDDEN_G0, KNOWN_G0, Vocab, Word, run  # noqa: E402

G = np.array([[0, 0, 3, 0], [0, 3, 3, 0], [5, 0, 0, 0]], dtype=np.int8)


def test_a_picture_survives_the_trip_to_tokens_and_back():
    for size in (5, 9, 11):
        assert np.array_equal(state.decode(state.encode(G, size), size), G)
    t = state.encode(G, 6)
    t[1, 1] = state.PAD                      # a hole in the picture: not a picture
    assert state.decode(t, 6) is None
    t = state.encode(G, 6)
    t[5, 5] = state.COLOUR0                  # a colour out in empty space
    assert state.decode(t, 6) is None


def test_hidden_words_are_never_among_the_taught_ones():
    taught = {w.op for w in KNOWN_G0}
    assert not taught & set(HIDDEN_G0)
    assert taught | set(HIDDEN_G0) <= set(ops.FROZEN)
    vocab = Vocab(KNOWN_G0, n_free=3)
    assert len({vocab.ids(w) for w in KNOWN_G0}) == len(KNOWN_G0)
    assert vocab.ids(vocab.free(0)) != vocab.ids(vocab.free(0, 3)) != vocab.ids(vocab.free(1, 3))
    # the colour 1 and the number 1 are different arguments
    assert vocab.ids(Word("remove_colour", 1))[1] != vocab.ids(Word("remove_specks", 1))[1]


def test_a_hand_written_word_runs_its_own_code():
    assert np.array_equal(run(Word("rot180"), G), ops.rot180(G))
    assert np.array_equal(run(Word("gravity", "down"), G), ops.gravity(G, "down"))


def test_a_puzzle_follows_its_hidden_program():
    rng = random.Random(0)
    grids = [rng_grid(rng) for _ in range(60)]
    program = [Word("rot180"), Word("gravity", "down")]
    p = curriculum.puzzle(program, grids, rng, side=6)
    assert p and len(p["train"]) == 3
    for g, o in p["train"] + [p["test"]]:
        assert np.array_equal(run(program[1], run(program[0], g)), o)


def rng_grid(rng):
    h, w = rng.randint(3, 6), rng.randint(3, 6)
    return np.array([[rng.choice((0, 0, 0, 1, 2, 3)) for _ in range(w)] for _ in range(h)],
                    dtype=np.int8)


def test_search_finds_the_shortest_hand_written_program():
    rng = random.Random(1)
    grids = [rng_grid(rng) for _ in range(80)]
    vocab = Vocab(KNOWN_G0)
    p = curriculum.puzzle([Word("transpose"), Word("remove_colour", 2)], grids, rng, side=6)
    right, progs = search.solve(p, vocab, depth=2, side=6)
    assert right and len(progs[0]) == 2
    # a word outside the taught ones leaves the puzzle unexplained
    q = curriculum.puzzle([Word("flip_h")], grids, rng, side=6)
    assert search.explain(q, vocab, depth=2, side=6) == []


class Told:
    """Stands in for a taught interpreter: each free word is given its meaning outright."""

    def __init__(self, vocab, meanings):
        self.meanings = {vocab.op_id[k]: v for k, v in meanings.items()}

    def run(self, grids, ids):
        return [self.meanings[op](g) for g, (op, _) in zip(grids, ids)]


def test_learned_and_hand_written_words_work_in_one_program():
    rng = random.Random(2)
    grids = [rng_grid(rng) for _ in range(80)]
    vocab = Vocab(KNOWN_G0, n_free=1)
    model = Told(vocab, {"new0": ops.flip_h})
    p = curriculum.puzzle([Word("flip_h"), Word("remove_colour", 1)], grids, rng, side=6)
    assert not search.solve(p, vocab, depth=2, side=6)[0]              # without the word
    right, progs = search.solve(p, vocab, model, [(0, False)], depth=2, side=6)
    assert right and any(vocab.is_free(w) for w in progs[0])


def test_a_new_primitive_is_told_from_an_abbreviation():
    rng = random.Random(3)
    grids = [rng_grid(rng) for _ in range(80)]
    vocab = Vocab(KNOWN_G0, n_free=2)
    model = Told(vocab, {"new0": ops.flip_h,                             # not sayable
                         "new1": lambda g: ops.transpose(ops.rot180(g))})  # two known words
    new, _ = crystallise.imitate(model, vocab, vocab.free(0), grids, side=6, depth=2)
    old, _ = crystallise.imitate(model, vocab, vocab.free(1), grids, side=6, depth=2)
    assert new is None
    assert old is not None and len(old) <= 2


def test_the_interpreter_learns_from_dreams():
    rng = random.Random(4)
    grids = [rng_grid(rng) for _ in range(200)]
    vocab = Vocab([Word("rot180"), Word("transpose")], n_free=1)
    torch.manual_seed(0)
    model = Interpreter(len(vocab.ops), len(ARGS), size=7, hidden=32, heads=2, layers=1, loops=2)
    batch = learn.tensors(learn.dream(grids, vocab, random.Random(5), 6, 64), vocab, 7)
    before = learn.loss_of(model, batch).item()
    taught = learn.teach(model, vocab, grids, steps=120, side=6, batch=32, warmup=20,
                         every=10 ** 9, log=lambda s: None)
    assert learn.loss_of(model, batch).item() < before / 2
    out = taught.run(grids[:4], [vocab.ids(Word("rot180"))] * 4)
    assert len(out) == 4                      # pictures or None, never a crash


def test_a_free_word_is_tried_bare_and_with_each_answer_colour():
    vocab = Vocab(KNOWN_G0, n_free=2)
    p = {"train": [(G, ops.recolour_all(G, 4))]}
    assert learn.options(vocab, (0, False), p) == [Word("new0")]
    assert learn.options(vocab, (1, True), p) == [Word("new1", 0), Word("new1", 4)]
