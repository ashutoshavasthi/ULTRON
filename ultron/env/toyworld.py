"""ToyWorld: a table with trays of objects and cups to hide them under.

The world only *does* things (put, hide, reveal, pair off, merge, take away).
It never explains itself. Everything is deterministic given the seed.
"""

import random


class ToyWorld:
    def __init__(self, seed=0):
        self.rng = random.Random(seed)
        self.trays = {}
        self.cups = {}
        self._next = 0
        self.clock = 0

    def _new(self, n):
        ids = list(range(self._next, self._next + n))
        self._next += n
        return ids

    def clear(self):
        self.trays = {}
        self.cups = {}

    # -- things a trainer (or Ultron) can do
    def put(self, tray, n):
        self.trays[tray] = self._new(n)
        return self.trays[tray]

    def hide(self, cup, objects):
        self.cups[cup] = list(objects)

    def wait(self, steps):
        self.clock += steps

    def reveal(self, cup):
        return self.cups.pop(cup, [])

    def pair_off(self, a, b):
        """Match objects one to one; return what is left over in each tray."""
        left_a, left_b = list(self.trays[a]), list(self.trays[b])
        while left_a and left_b:
            left_a.pop()
            left_b.pop()
        return left_a, left_b

    def merge(self, sources, into):
        merged = []
        for s in sources:
            merged.extend(self.trays.pop(s))
        self.trays[into] = merged
        return merged

    def take(self, source, n, into):
        objs = self.trays[source]
        self.trays[into], self.trays[source] = objs[:n], objs[n:]
        return self.trays[source]

    def flicker(self):
        """A panel of lamps that lights up at random: pure noise."""
        return self.rng.randint(0, 9)
