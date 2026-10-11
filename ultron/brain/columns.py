"""Inventing column arithmetic (place-value algorithms).

Ultron adds and multiplies by counting, which gets slow for big numbers. But it
also has its place-value law, numeral(left, right) = ten groups of left, plus
right. Reflecting, it checks four identities with its own laws on many examples:

  columns  plus(numeral(a, b), numeral(c, d)) = numeral(plus(a, c), plus(b, d))
  carry    numeral(a, b) = numeral(a + 1, b - 10)   when b is 10 or more
  spread   times(numeral(a, b), k) = numeral(times(a, k), times(b, k))
  shift    numeral(x, 0) = times(x, 10)

Together they say a number can be worked on column by column. So it builds the
column methods from them (add with carries, take away with borrows, multiply
digit by digit and shift). Every single-digit fact comes from its own counting
laws, remembered like a times table. Before trusting a method for one of its laws,
it compares the two on dozens of examples; only laws that always agree get the
quicker way.

The digits of a count are read and written the way Ultron reads and writes
numerals: as the marks of its own place-value notation.
"""

import math
import random

from .dsl import Overflow

KEY = "columns"
MAX_DIGITS = 320        # past this, a number is too big to write out


def _slow(library, law, a, b):
    """One of Ultron's laws, worked out by counting (small numbers only)."""
    from .dsl import evaluate
    rule = library.laws[law]
    key = ("slow", law, a, b)
    memo = library._memo
    if key not in memo:
        library._counting += 1          # a basic fact: no shortcuts while counting it
        try:
            memo[key] = evaluate(rule.expr, {rule.params[0]: a, rule.params[1]: b}, library)
        finally:
            library._counting -= 1
    return memo[key]


def _word_law(brain, word):
    m = brain.vocab.get(word)
    return m[1] if m and m[0] == "op" else None


# --------------------------------------------------------------- discovery
def look_for_columns(brain):
    if KEY in brain.inventions:
        return None
    plus, times = _word_law(brain, "plus"), _word_law(brain, "times")
    num = "numeral"
    if not (plus and times and brain.trusts(num) and brain.trusts(plus)
            and brain.trusts(times)):
        return None
    facts = {"plus": [plus, brain.vocab["plus"][2]], "times": [times, brain.vocab["times"][2]]}
    lib = brain.library
    P = lambda x, y: _slow(lib, plus, *((x, y) if facts["plus"][1] == "xy" else (y, x)))
    T = lambda x, y: _slow(lib, times, *((x, y) if facts["times"][1] == "xy" else (y, x)))
    N = lambda l, r: _slow(lib, num, l, r)
    rng = random.Random(4)
    try:
        for _ in range(40):
            a, b, c, d, k = (rng.randint(0, 9) for _ in range(5))
            if P(N(a, b), N(c, d)) != N(P(a, c), P(b, d)):
                return None
            r = rng.randint(0, 8)
            big = P(r, 10)                      # a column holding 10 or more
            if N(a, big) != N(P(a, 1), r):
                return None
            if T(N(a, b), k) != N(T(a, k), T(b, k)):
                return None
            if N(a, 0) != T(a, 10):
                return None
    except (Overflow, KeyError):
        return None
    story = ("My place-value law hides a shortcut. I checked on 40 examples each: adding two "
             "numerals is adding their columns; ten in a column is one in the next (a carry); "
             "times spreads over the columns; and a 0 on the end is times ten. So I never need "
             "to count a big number out: I can work column by column, where every step is a "
             "small sum or product I already know by heart. That is column arithmetic.")
    inv = {"shape": "algorithm", "primitives": [], "lesson": brain.lesson, "story": story,
           "facts": facts}
    brain.inventions[KEY] = inv
    brain.note("invent", story)
    attach(brain)
    trust_fast_paths(brain)
    return inv


def attach(brain):
    """Give the library the column methods (after inventing them, or after loading)."""
    inv = brain.inventions.get(KEY)
    if inv is not None:
        brain.library._columns = Columns(brain.library, inv["facts"])
        brain.library._fast_fns = (worth_it, fast_call)


def invented(brain):
    return KEY in brain.inventions


# --------------------------------------------------------- the column methods
class Columns:
    """Column methods built from Ultron's own single-digit facts."""

    def __init__(self, library, facts):
        self.library = library
        self.facts = facts
        (plus, po), (times, to) = facts["plus"], facts["times"]
        self._plus = lambda x, y: _slow(library, plus, *((x, y) if po == "xy" else (y, x)))
        self._times = lambda x, y: _slow(library, times, *((x, y) if to == "xy" else (y, x)))
        # the small facts, once worked out by counting, are known by heart (a times table)
        self._by_heart = {"+": {}, "x": {}, "split": {}, "diff": {}}

    def plus(self, x, y):
        table = self._by_heart["+"]
        v = table.get((x, y))
        if v is None:
            v = table[(x, y)] = self._plus(x, y)
        return v

    def times(self, x, y):
        table = self._by_heart["x"]
        v = table.get((x, y))
        if v is None:
            v = table[(x, y)] = self._times(x, y)
        return v

    def _diff(self, big, small):
        """big - small for small digits: count up from the smaller one."""
        table = self._by_heart["diff"]
        if (big, small) not in table:
            table[(big, small)] = self._count_up(big, small)
        return table[(big, small)]

    def _count_up(self, big, small):
        r = 0
        while self.plus(small, r) != big:
            r += 1
        return r

    @staticmethod
    def digits(n):
        """A count written as its marks, lowest place first."""
        return [int(ch) for ch in reversed(str(n))]

    @staticmethod
    def value(ds):
        """Marks read back as a count."""
        ds = list(ds)
        while len(ds) > 1 and ds[-1] == 0:
            ds.pop()
        return int("".join(str(d) for d in reversed(ds))) if ds else 0

    def _split(self, s):
        """A small total (under 100) as (tens, units), using its times law."""
        table = self._by_heart["split"]
        if s not in table:
            table[s] = self._split_slow(s)
        return table[s]

    def _split_slow(self, s):
        tens = 0
        while self.times(tens + 1, 10) <= s:
            tens += 1
        return tens, self._diff(s, self.times(tens, 10))

    def add(self, xs, ys):
        out, carry = [], 0
        for i in range(max(len(xs), len(ys))):
            s = self.plus(xs[i] if i < len(xs) else 0, ys[i] if i < len(ys) else 0)
            s = self.plus(s, carry)
            carry, unit = self._split(s)
            out.append(unit)
        if carry:
            out.append(carry)
        return out

    def sub(self, xs, ys):
        """xs - ys for xs >= ys, borrowing from the next column."""
        out, borrow = [], 0
        for i in range(len(xs)):
            top = xs[i]
            need = self.plus(ys[i] if i < len(ys) else 0, borrow)
            if top < need:
                top, borrow = self.plus(top, 10), 1
            else:
                borrow = 0
            out.append(self._diff(top, need))
        return out

    def mul_digit(self, xs, k):
        out, carry = [], 0
        for x in xs:
            p = self.plus(self.times(x, k), carry)
            carry, unit = self._split(p)
            out.append(unit)
        while carry:
            carry, unit = self._split(carry)
            out.append(unit)
        return out

    def mul(self, xs, ys):
        total = [0]
        for j, y in enumerate(ys):
            total = self.add(total, [0] * j + self.mul_digit(xs, y))
        return total

    @staticmethod
    def less(xs, ys):
        xs, ys = Columns.digits(Columns.value(xs)), Columns.digits(Columns.value(ys))
        if len(xs) != len(ys):
            return len(xs) < len(ys)
        for x, y in zip(reversed(xs), reversed(ys)):
            if x != y:
                return x < y
        return False

    # signed numbers: sign and marks, combined by the rules its own laws obey
    def add_signed(self, a, b):
        if (a < 0) == (b < 0):
            m = self.value(self.add(self.digits(abs(a)), self.digits(abs(b))))
            return -m if a < 0 else m
        big, small = (a, b) if not self.less(self.digits(abs(a)), self.digits(abs(b))) else (b, a)
        m = self.value(self.sub(self.digits(abs(big)), self.digits(abs(small))))
        return -m if big < 0 else m

    def mul_signed(self, a, b):
        m = self.value(self.mul(self.digits(abs(a)), self.digits(abs(b))))
        return -m if (a < 0) != (b < 0) and m else m

    def power(self, a, n):
        if n < 0:
            return None
        if getattr(self.library, "squaring", False):
            # its law of repeating (repeat p, then that q times = repeat p·q) lets it square
            # instead of multiplying one step at a time: a^(2k) = (a^k)^2
            result, sq, k = 1, a, n
            while k:
                if k % 2:
                    result = self.mul_signed(result, sq)
                    if len(str(abs(result))) > MAX_DIGITS:
                        return None
                k //= 2
                if k:
                    sq = self.mul_signed(sq, sq)
                    if len(str(abs(sq))) > MAX_DIGITS:
                        return None
            return result
        acc = 1
        for _ in range(n):
            acc = self.mul_signed(acc, a)
            if len(str(abs(acc))) > MAX_DIGITS:
                return None
        return acc


def _methods(cols):
    return {
        "add": lambda a, b: cols.add_signed(a, b),
        "take away": lambda a, b: cols.add_signed(a, -b),
        "times": lambda a, b: cols.mul_signed(a, b),
        "repeated times": lambda a, b: cols.power(a, b),
    }


def trust_fast_paths(brain):
    """For each of its laws, is there a column method that always agrees with it?
    Checked on many examples (with numbers below zero too, once it has them)."""
    if not invented(brain):
        return
    attach(brain)
    cols = brain.library._columns
    signed = any(inv.get("shape") == "line" for inv in brain.inventions.values())
    rng = random.Random(7)
    lo = -25 if signed else 0
    for law in brain.library.binary_int_laws():
        if law.name in brain.library.fast or law.name == "numeral":
            continue
        for label, method in _methods(cols).items():
            for order in ("xy", "yx"):
                ok = True
                for _ in range(60):
                    a, b = rng.randint(lo, 60), rng.randint(lo, 60)
                    if label == "repeated times":
                        b = rng.randint(0, 6)
                        a = rng.randint(lo if signed else 0, 12)
                    x, y = (a, b) if order == "xy" else (b, a)
                    try:
                        slow = brain.library.call(law.name, a, b)
                    except Overflow:
                        continue
                    if method(x, y) != slow:
                        ok = False
                        break
                if ok:
                    brain.library.fast[law.name] = (label, order)
                    brain.note("reflect", f"the column way of '{label}' gives the same answer as "
                                          f"my law '{law.name}' on 60 examples; I'll use it for "
                                          f"big numbers")
                    break
            if law.name in brain.library.fast:
                break


def worth_it(library, name, a, b):
    """Columns only when counting it out would be long: small sums are quicker by
    counting (or from memory), big ones are quicker written out in columns."""
    label, order = library.fast[name]
    a, b = (abs(a), abs(b)) if order == "xy" else (abs(b), abs(a))
    if label in ("add", "take away"):
        return min(a, b) > 2000
    if label == "times":
        return a * b > 20000
    return a > 1 and b > 12 or a > 50   # repeated times: (amount, how many times)


def fast_call(brain_library, name, a, b):
    """Used by the library: the column method for a law that earned it."""
    from . import dsl
    label, order = brain_library.fast[name]
    cols = brain_library._columns
    x, y = (a, b) if order == "xy" else (b, a)
    # effort: one step per pair of columns worked on (so budgets see column work too)
    da, db = len(str(abs(x))), len(str(abs(y)))
    if label == "times":
        dsl.STEPS[0] += da * db
    elif label == "repeated times":
        if getattr(brain_library, "squaring", False):
            dsl.STEPS[0] += max(1, y).bit_length() * (da * max(1, y)) ** 2 // 4 + 1
        else:
            dsl.STEPS[0] += max(0, y) ** 2 * da * da // 2 + 1
    else:
        dsl.STEPS[0] += max(da, db)
    if label == "repeated times" and y > 0 and len(str(abs(x))) * y > MAX_DIGITS * 2:
        raise Overflow()        # far too big to write out
    # while imagining many candidates (tighter limits), an answer bigger than it is
    # willing to hold is refused before it is written out: the number of columns alone
    # says how big it will be
    if dsl.MAX_VALUE < dsl._DEFAULT_LIMITS[1]:
        limit = len(str(dsl.MAX_VALUE)) + 1
        if label == "times" and da + db - 1 > limit:
            raise Overflow()
        if label == "repeated times" and y > 1 and abs(x) > 1 and \
                y * math.log10(abs(x)) > limit:
            raise Overflow()
        if label == "add" and max(da, db) > limit:
            raise Overflow()
    v = _methods(cols)[label](x, y)
    if v is None or len(str(abs(v))) > MAX_DIGITS:
        raise Overflow()
    return v
