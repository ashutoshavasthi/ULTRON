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


class ShopWorld:
    """A purse holding coins and IOU notes (promises to pay a coin later).

    Earning a coin first tears up an IOU if there is one; otherwise the coin goes
    in the purse. Spending a coin takes one from the purse; if the purse is
    empty, the shop hands over an IOU note instead. Nothing here mentions
    numbers below zero: there are only coins and notes.
    """

    def __init__(self, seed=0):
        self.rng = random.Random(seed)
        self.coins = []
        self.notes = []
        self._next = 0

    def _new(self):
        self._next += 1
        return self._next

    def set_purse(self, coins, notes):
        self.coins = [self._new() for _ in range(coins)]
        self.notes = [self._new() for _ in range(notes)]

    def earn(self):
        if self.notes:
            self.notes.pop()
        else:
            self.coins.append(self._new())

    def spend(self):
        if self.coins:
            self.coins.pop()
        else:
            self.notes.append(self._new())


class Bakery:
    """Identical cakes, a knife that cuts anything into equal pieces, and a balance.

    The world knows how heavy each piece really is (an exact share of a cake).
    Ultron only sees how many pieces there are, how many pieces a cake was cut
    into, and which pan of the balance goes down. Nothing here mentions fractions.
    """

    def __init__(self, seed=0):
        from fractions import Fraction
        self._F = Fraction
        self.rng = random.Random(seed)

    def cut(self, cakes, into):
        """Cut `cakes` whole cakes into `into` equal pieces each."""
        return [self._F(1, into)] * (cakes * into)

    def recut(self, pieces, into):
        return [p / into for p in pieces for _ in range(into)]

    @staticmethod
    def wholes(n):
        from fractions import Fraction
        return [Fraction(1)] * n

    @staticmethod
    def balance(left, right):
        """-1 if the left pan goes up, 0 if level, 1 if it goes down."""
        a, b = sum(left), sum(right)
        return (a > b) - (a < b)
