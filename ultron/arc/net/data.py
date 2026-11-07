"""Puzzles for the network: token grids, augmentations, and the training set.

A grid becomes 30 x 30 tokens: 0 is empty space, 1 marks the edge just past the grid
(right and below), and colours 0-9 are tokens 2-11. The network reads a puzzle as one
input grid plus a learned embedding for that puzzle (as TRM does): what the puzzle asks
is learned from its examples into its embedding.

Augmentations: each puzzle is also seen turned or mirrored (the 8 symmetries of a square)
and with its colours 1-9 renamed (colour 0, usually the background, stays). Each
augmented view is its own puzzle id, and each view can be undone exactly, so answers
from many views can be mapped back and compared (the judge votes on them).

The guard: a puzzle that is tested on gives the network its examples, never the answer
of its test. `pairs()` is the only way training pairs are made, and it enforces this.
"""

import numpy as np

SIZE = 30
PAD, EDGE, COLOUR0 = 0, 1, 2
VOCAB = 12


def encode(g):
    """A grid (h x w, colours 0-9) as 30 x 30 tokens."""
    g = np.asarray(g)
    h, w = g.shape
    out = np.full((SIZE, SIZE), PAD, dtype=np.int64)
    out[:h, :w] = g + COLOUR0
    if w < SIZE:
        out[:h, w] = EDGE
    if h < SIZE:
        out[h, :min(w + 1, SIZE)] = EDGE
    return out


def decode(t):
    """30 x 30 tokens back to a grid: the colours up to the first edge mark (None if the
    tokens don't make a grid)."""
    t = np.asarray(t)
    row = t[0]
    w = next((i for i, v in enumerate(row) if v < COLOUR0), SIZE)
    col = t[:, 0]
    h = next((i for i, v in enumerate(col) if v < COLOUR0), SIZE)
    if h == 0 or w == 0:
        return None
    g = t[:h, :w]
    if (g < COLOUR0).any():
        return None
    return (g - COLOUR0).astype(np.int8)


# ------------------------------------------------------------------ augmentations
def dihedral(g, k):
    """The k-th of the 8 symmetries of a square (k = 0 is the identity)."""
    g = np.rot90(g, k % 4)
    return g.T if k >= 4 else g


def undo_dihedral(g, k):
    g = g.T if k >= 4 else g
    return np.rot90(g, -(k % 4))


def views(n, seed):
    """n augmentations [(symmetry, colour renaming)]; the first is the identity."""
    rng = np.random.default_rng(seed)
    out = [(0, np.arange(10))]
    while len(out) < n:
        perm = np.concatenate([[0], 1 + rng.permutation(9)])
        out.append((int(rng.integers(8)), perm))
    return out


def apply(g, view):
    k, perm = view
    return dihedral(perm[np.asarray(g)], k).astype(np.int8)


def undo(g, view):
    k, perm = view
    inv = np.argsort(perm)
    return inv[undo_dihedral(np.asarray(g), k)].astype(np.int8)


# ------------------------------------------------------------------ the training set
def pairs(tasks, learn_answers, examples_only, dreams=(), n_views=8, seed=0, dream_views=1):
    """Training pairs [(puzzle id, input tokens, output tokens)] and the ids' meaning.

    learn_answers: puzzles whose test answers may be learned (the practice half).
    examples_only: puzzles that will be tested on (held out): only their examples are
    used, never their test answers. dreams: puzzles it made itself (dreams.make).
    Every real puzzle is seen in n_views augmented views, each its own id; a dream (there
    are always more) in dream_views."""
    clash = set(learn_answers) & set(examples_only)
    if clash:
        raise ValueError(f"a puzzle can't be both learned and tested on: {sorted(clash)[:3]}")
    ids, X, Y, P = [], [], [], []
    vs = views(n_views, seed)

    def add(name, examples, n=n_views):
        for v, view in enumerate(vs[:n]):
            pid = len(ids)
            ids.append((name, v))
            for i, o in examples:
                X.append(encode(apply(i, view)).astype(np.uint8))
                Y.append(encode(apply(o, view)).astype(np.uint8))
                P.append(pid)

    for t in sorted(learn_answers):
        add(t, list(tasks[t]["train"]) + [(i, o) for i, o in tasks[t]["test"] if o is not None])
    for t in sorted(examples_only):
        add(t, list(tasks[t]["train"]))                 # the guard: never tasks[t]["test"]
    for k, d in enumerate(dreams):
        add(f"dream{k}", list(d["train"]) + list(d["test"]), dream_views)
    return {"ids": ids, "views": vs, "x": np.stack(X), "y": np.stack(Y),
            "puzzle": np.array(P, dtype=np.int64)}


def test_inputs(tasks, names, dataset):
    """For each tested puzzle, its test inputs in every view: [(name, test index, view
    index, puzzle id, input tokens)]."""
    where = {key: pid for pid, key in enumerate(dataset["ids"])}
    out = []
    for t in names:
        for j, (i, _) in enumerate(tasks[t]["test"]):
            for v, view in enumerate(dataset["views"]):
                out.append((t, j, v, where[(t, v)], encode(apply(i, view))))
    return out
