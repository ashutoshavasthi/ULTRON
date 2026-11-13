"""What the interpreter learns from: dreams (hand-written words run on real pictures, so
every step has an exact answer) and puzzles made with a word it has never been shown.

Pictures come only from the practice half of Ultron's experience (ultron/arc/loop.py), and
are split by puzzle into pictures to learn from and pictures kept aside for testing.
"""

import random

import numpy as np

from ..arc import loop
from .vocab import changes, run


def pool(side=10, crops=2, seed=0):
    """Pictures of at most side x side from the practice half: (to learn from, kept
    aside). Bigger pictures give a few random windows. Every tenth puzzle is kept aside."""
    tasks, practice, _ = loop.halves()
    rng = random.Random(seed)
    learn, aside = [], []
    for n, tid in enumerate(practice):
        grids = [g for pair in tasks[tid]["train"] for g in pair]
        grids += [i for i, _ in tasks[tid]["test"]]
        out = aside if n % 10 == 9 else learn
        for g in grids:
            g = np.asarray(g, dtype=np.int8)
            if max(g.shape) <= side:
                out.append(g)
                continue
            for _ in range(crops):
                h, w = min(g.shape[0], rng.randint(3, side)), min(g.shape[1], rng.randint(3, side))
                r, c = rng.randint(0, g.shape[0] - h), rng.randint(0, g.shape[1] - w)
                out.append(np.ascontiguousarray(g[r:r + h, c:c + w]))
    return learn, aside


def state(grids, known, rng, side, depth=None):
    """A picture as the interpreter might meet it mid-program: a real picture after 0-2
    hand-written words."""
    g = rng.choice(grids)
    depth = rng.choice((0, 0, 0, 1, 1, 2)) if depth is None else depth
    for _ in range(depth):
        out = changes(rng.choice(known), g)
        if out is not None and max(out.shape) <= side:
            g = out
    return g


def step(grids, known, word, rng, side, tries=30, still=0.1):
    """One exact step for `word`: (picture, result). Mostly pictures the word changes;
    now and then one it leaves alone, so it also learns when to do nothing."""
    for _ in range(tries):
        g = state(grids, known, rng, side)
        out = run(word, g)
        if out is None or max(out.shape) > side:
            continue
        same = out.shape == g.shape and (out == g).all()
        if not same or rng.random() < still:
            return g, out
    return None


def chain(grids, known, rng, side, length, tries=200):
    """A program of `length` hand-written words in which every word changes the picture:
    (start, words, the picture after each word)."""
    for _ in range(tries):
        g = rng.choice(grids)
        words, trace = [], []
        for _ in range(length):
            for _ in range(20):
                w = rng.choice(known)
                out = changes(w, g if not trace else trace[-1])
                if out is not None and max(out.shape) <= side:
                    words.append(w)
                    trace.append(out)
                    break
            else:
                break
        if len(words) == length:
            return g, words, trace
    return None


def puzzle(program, grids, rng, side, examples=3, tries=400):
    """A puzzle whose hidden rule is `program` (a list of words run by code): `examples`
    pairs to learn from and one test pair. Every word must change every picture."""
    pairs, seen = [], set()
    for _ in range(tries):
        g = state(grids, (), rng, side, depth=0)
        if g.tobytes() in seen:
            continue
        cur = g
        for w in program:
            cur = changes(w, cur)
            if cur is None or max(cur.shape) > side:
                break
        else:
            seen.add(g.tobytes())
            pairs.append((g, cur))
            if len(pairs) == examples + 1:
                return {"program": list(program), "train": pairs[:examples], "test": pairs[examples]}
    return None
