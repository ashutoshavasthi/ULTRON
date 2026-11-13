"""A grid as tokens on a small square canvas (the scheme of ultron/arc/net/data.py, with
the canvas size as a setting).

0 is empty space, 1 marks the edge just past the grid (right and below), and colours 0-9
are tokens 2-11. A grid of up to (size-1) x (size-1) always shows both of its edges, so
its height and width can be read back exactly.
"""

import numpy as np

PAD, EDGE, COLOUR0 = 0, 1, 2
VOCAB = 12


def fits(g, size):
    return g is not None and g.ndim == 2 and 0 < g.shape[0] < size and 0 < g.shape[1] < size


def encode(g, size):
    """A grid (h x w, colours 0-9) as size x size tokens."""
    g = np.asarray(g)
    h, w = g.shape
    out = np.full((size, size), PAD, dtype=np.int64)
    out[:h, :w] = g + COLOUR0
    out[:h, w] = EDGE
    out[h, :w + 1] = EDGE
    return out


def decode(t, size):
    """Tokens back to a grid, or None when they don't make one: the colours must fill a
    rectangle exactly, edged right and below, with empty space everywhere else."""
    t = np.asarray(t).reshape(size, size)
    w = next((i for i, v in enumerate(t[0]) if v < COLOUR0), size)
    h = next((i for i, v in enumerate(t[:, 0]) if v < COLOUR0), size)
    if h == 0 or w == 0 or h >= size or w >= size:
        return None
    g = (t[:h, :w] - COLOUR0).astype(np.int8)
    return g if np.array_equal(t, encode(g, size)) and (t[:h, :w] >= COLOUR0).all() else None
