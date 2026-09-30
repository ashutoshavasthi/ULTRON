"""Inventing numbers in the gaps of the finer line (irrational numbers).

Ultron asks itself inverse questions with its own laws, e.g. "what power 2 equals 2".
No whole number and no pile of pieces answers it (it tries cakes cut into up to 60
pieces). But the answer is always *squeezed*: some pile gives too little and the
next pile, one piece bigger, too much, however finely it cuts. So its finer line has
gaps: places no pile of pieces reaches. It invents numbers that live in those gaps.
It can't write one as pieces, but it can pin it between two piles as tightly as its
counting allows.

A gap number is kept as the question that defines it (law, the known amount, the
goal) and is used by pinning it: for any kind of piece d, find the count c with
c/d too small and (c+1)/d too big. Everything is worked out with Ultron's own laws
on amounts; no square roots are built in.
"""

from . import amounts
from .dsl import Overflow

KEY = "gaps"
PRECISIONS = (10, 100, 1000)    # pin to a tenth, then a hundredth, then a thousandth ...
EFFORT = 1_500_000              # ... while the counting it expects to need stays in budget


class Gap:
    def __init__(self, law, order, known, goal, unknown_first, one_input=False):
        self.law, self.order = law, order
        self.known, self.goal = tuple(known), tuple(goal)
        self.unknown_first = unknown_first
        self.one_input = one_input      # e.g. "tiles in a square of side s"

    def to_json(self):
        return {"law": self.law, "order": self.order, "known": list(self.known),
                "goal": list(self.goal), "unknown_first": self.unknown_first,
                "one_input": self.one_input}

    @classmethod
    def from_json(cls, d):
        return cls(d["law"], d["order"], d["known"], d["goal"], d["unknown_first"],
                   d.get("one_input", False))


def _side(brain, gap, x):
    """-1 if x gives too little, 0 if exactly right, 1 if too much (None: can't say)."""
    pair = (x, gap.known) if gap.unknown_first else (gap.known, x)
    try:
        if gap.one_input:
            rule = brain.library.get(gap.law)
            res = amounts.evaluate_amount(brain, rule.expr, {rule.params[0]: x})
        else:
            res, _ = amounts.combine(brain, gap.law, pair[0], pair[1], gap.order)
        if res is None:
            return None
        c1, c2, _ = amounts.common(brain, res, gap.goal)
    except Overflow:
        return None
    return (c1 > c2) - (c1 < c2)


def pin(brain, gap, d, coarser=None):
    """(c, d): the count of 1/d pieces just below the gap number (so it lies between
    c/d and (c+1)/d). With a coarser pin (c', d') it only looks inside that bracket;
    otherwise it searches upward from 0 by doubling. Then it halves."""
    s0 = _side(brain, gap, (0, d))
    if s0 is None:
        return None
    if coarser is None and d > 20:
        coarser = pin(brain, gap, 10)       # a cheap rough pin first, then look only there
    if coarser is not None:
        c, e = coarser
        lo, hi = (c * d) // e, -((-(c + 1) * d) // e)
    else:
        lo, hi = 0, 1
        while True:
            s = _side(brain, gap, (hi, d))
            if s is None or hi > 10 ** 7:
                return None
            if s != s0:
                break
            lo, hi = hi, hi * 2
    while hi - lo > 1:
        mid = (lo + hi) // 2
        s = _side(brain, gap, (mid, d))
        if s is None:
            return None
        if s == s0:
            lo = mid
        else:
            hi = mid
    return (lo, d)


def squeezed(brain, law, order, known, goal, unknown_first):
    """Is this question's answer squeezed into a gap? (no pile works, but for every
    kind of piece tried, some pile is too small and the next one too big)"""
    gap = Gap(law, order, known, goal, unknown_first)
    sides = [_side(brain, gap, (c, 1)) for c in range(0, 12)]
    if None in sides or 0 in sides or len(set(sides)) < 2:
        return None
    # the sign changes exactly once among whole numbers: an increasing (or decreasing) law
    flips = sum(1 for a, b in zip(sides, sides[1:]) if a != b)
    if flips != 1:
        return None
    for d in (2, 3, 5, 7, 10):
        c = pin(brain, gap, d)
        if c is None or _side(brain, gap, c) == 0 or _side(brain, gap, (c[0] + 1, d)) == 0:
            return None
    return gap


def look_for_gaps(brain):
    """Reflection: ask itself 'what <law> k equals n' questions, looking for gaps."""
    if KEY in brain.inventions or not amounts.invented(brain):
        return None
    for law in brain.library.binary_int_laws():
        if law.name == amounts._scale(brain) or amounts.scale_compatible(brain, law.name):
            continue        # laws that work piece by piece never leave gaps between pieces
        for known in (2, 3):
            for goal in range(2, 8):
                for unknown_first in (True, False):
                    try:
                        exact = amounts.solve(brain, law.name, "xy", (known, 1), (goal, 1),
                                              unknown_first)
                    except Overflow:
                        continue
                    if exact is not None:
                        continue
                    gap = squeezed(brain, law.name, "xy", (known, 1), (goal, 1), unknown_first)
                    if gap is None:
                        continue
                    lo = pin(brain, gap, 5)
                    q = (f"{law.name}(?, {known}) = {goal}" if unknown_first
                         else f"{law.name}({known}, ?) = {goal}")
                    story = (f"I asked myself {q}. No whole number works, and no pile of pieces "
                             f"either (I tried cakes cut into up to {amounts.LAST_CUT[0]}). But "
                             f"the answer is "
                             f"squeezed: {amounts.show(brain, lo)} gives too little, "
                             f"{amounts.show(brain, (lo[0] + 1, lo[1]))} too much, and however "
                             f"finely I cut, it is always caught between two piles, never on one. "
                             f"So my finer line has GAPS: places no pile of pieces reaches. I'll "
                             f"treat each such place as a number too: I can't write it as pieces, "
                             f"but I can pin it between two piles as tightly as I can count.")
                    inv = {"shape": "gaps in the finer line", "primitives": [],
                           "lesson": brain.lesson, "first": gap.to_json(), "story": story}
                    brain.inventions[KEY] = inv
                    brain.note("invent", story)
                    return inv
    return None


def invented(brain):
    return KEY in brain.inventions


def describe(brain, gap):
    """Pin a gap number as tightly as its counting allows: each finer pin costs more
    counting; it measures what a pin cost and stops before the next would blow the
    effort budget. Returns ((lo, hi), text, d)."""
    from . import dsl
    best, used, last_cost = None, None, None
    for i, d in enumerate(PRECISIONS):
        before = dsl.STEPS[0]
        c = pin(brain, gap, d, best)
        if c is None:
            break
        best, used = c, d
        cost = max(1, dsl.STEPS[0] - before)
        growth = max(10, cost // last_cost) if last_cost else 1000
        last_cost = cost
        if i + 1 == len(PRECISIONS) or cost * growth > EFFORT:
            break           # the next pin would cost more counting than it's worth
    if best is None:
        return None, "I can't pin it down", None
    lo = amounts.simplest(brain, best)
    hi = amounts.simplest(brain, (best[0] + 1, used))
    return (lo, hi), f"between {amounts.show(brain, lo)} and {amounts.show(brain, hi)}", used
