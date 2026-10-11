"""Descriptions with exceptions: what Ultron can learn from a task it has not solved.

A program that explains every example exactly is a description of the task. A program
that gets most of each answer right is one too, if it is written down together with the
cells it gets wrong (a law with exceptions, as everywhere in Ultron). It counts only if
the program and its exceptions together are SHORTER than describing the answers without
it: copying the input and listing the cells that change, or, when the answer has another
shape, writing the answer out.

Ultron never answers with such a description (it would be a guess). It learns from it:
pieces that recur across the descriptions of many tasks can become its own building
blocks (library.py), since the shortest description of everything it has seen then gets
shorter.

Lengths are in bits:
  * a program: log2(number of operations it chooses from) per step;
  * an exception: where (log2 of the cells) and what colour (log2 10), plus how many;
  * an answer written out: log2 10 per cell, plus its shape.
"""

import math

COLOUR_BITS = math.log2(10)
SHAPE_BITS = 2 * math.log2(30)


def _cells_bits(n_wrong, n_cells):
    return math.log2(n_cells + 1) + n_wrong * (math.log2(n_cells) + COLOUR_BITS)


def exceptions(outs, targets):
    """Bits to list the cells these pictures get wrong, or None if a shape is wrong."""
    total = 0.0
    for g, t in zip(outs, targets):
        if g.shape != t.shape:
            return None
        total += _cells_bits(int((g != t).sum()), t.size)
    return total


def baseline(ins, targets):
    """Bits to describe the answers with no program at all."""
    total = 0.0
    for i, t in zip(ins, targets):
        if i.shape == t.shape:
            total += _cells_bits(int((i != t).sum()), t.size)
        else:
            total += SHAPE_BITS + t.size * COLOUR_BITS
    return total


def program_bits(length, n_ops):
    """A program's own length (solve.length, in steps) in bits."""
    return length * math.log2(max(2, n_ops))


class Best:
    """The shortest description found so far for one task (a list hook for the search)."""

    def __init__(self, ins, targets, n_ops):
        self.base = baseline(ins, targets)
        self.n_ops = n_ops
        self.bits, self.program, self.wrong = self.base, (), None

    def offer(self, program, length, outs, targets):
        p = program_bits(length, self.n_ops)
        if p >= self.bits:
            return
        e = exceptions(outs, targets)
        if e is None or p + e >= self.bits:
            return
        self.bits, self.program = p + e, program
        self.wrong = int(sum(int((g != t).sum()) for g, t in zip(outs, targets)))

    def offer_exact(self, program, length):
        p = program_bits(length, self.n_ops)
        if p < self.bits:
            self.bits, self.program, self.wrong = p, program, 0

    def saving(self):
        return self.base - self.bits


def best(train, budget=None, **kw):
    """The shortest description of a task within the budget: (bits saved, program,
    cells it gets wrong), or None when nothing beats describing the answers outright."""
    from . import solve
    solve.DESCRIBE[0] = []
    try:
        solve.solve(train, **({"budget": budget} if budget else {}), **kw)
        d = solve.DESCRIBE[0][0] if solve.DESCRIBE[0] else None
    finally:
        solve.DESCRIBE[0] = None
    if d is None or not d.program:
        return None
    return d.saving(), d.program, d.wrong

