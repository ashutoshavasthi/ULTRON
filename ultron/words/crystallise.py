"""Is a learned word new, or an abbreviation of words Ultron already had?

The learned word is shown some pictures and its results are written down. Then the
hand-written words alone are searched for a program that gives the same results. If one
is found, the word is an abbreviation and that program is its definition. If none is
found within the search limit, the word does something the language could not say before:
a new primitive. That count is the scoreboard's "new primitives".
"""

import random

from . import curriculum
from .search import explain


def imitate(model, vocab, word, grids, side, known=None, depth=3, examples=5, seed=3):
    """A hand-written program that does what `word` does on `examples` pictures it
    changes, or None. Also returns how many pictures the word changed."""
    rng = random.Random(seed)
    pairs = []
    for _ in range(examples * 40):
        g = curriculum.state(grids, vocab.known, rng, side)
        out = model.run([g], [vocab.ids(word)])[0]
        if out is not None and not (out.shape == g.shape and (out == g).all()):
            pairs.append((g, out))
            if len(pairs) == examples:
                break
    if len(pairs) < 2:
        return None, len(pairs)
    progs = explain({"train": pairs}, vocab, depth=depth, side=side, want=1, known=known)
    return (progs[0] if progs else None), len(pairs)
