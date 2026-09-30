"""Grounded language: words are attached to concepts Ultron already has.

  * a number word or mark is bound to a quantity it can count;
  * an operation word is bound to whichever of *its own* laws reproduces every
    demonstration the Trainer gave (and in which argument order);
  * a relation word is bound to an innate relation ("same", "fewer").

A word nobody demonstrated stays meaningless to it.
"""

from .dsl import Overflow

NUMERAL_LAW = "numeral"     # the place-value law Ultron discovers in lesson 4


def bind_number(brain, token, pile_count):
    known = brain.vocab.get(token)
    if known and known != ("number", pile_count):
        brain.note("conflict", f"'{token}' was shown for {known[1]} and for {pile_count}")
    brain.bind(token, ("number", pile_count))


def bind_operation(brain, token, demos):
    """demos: [(x, y, result)] as Ultron perceived them. Returns the binding or None."""
    for law in brain.library.binary_int_laws():
        for order in ("xy", "yx"):
            ok = True
            for x, y, r in demos:
                a, b = (x, y) if order == "xy" else (y, x)
                try:
                    if brain.library.call(law.name, a, b) != r:
                        ok = False
                        break
                except Overflow:
                    ok = False
                    break
            if ok:
                brain.bind(token, ("op", law.name, order))
                brain.note("word", f"'{token}' behaves exactly like my law '{law.name}' "
                                   f"(arguments {order}) in all {len(demos)} demonstrations")
                return brain.vocab[token]
    brain.note("word", f"'{token}': none of my laws matches the demonstrations")
    return None


def bind_relation(brain, token, demos):
    """demos: [(left, right)] pairs the Trainer said this word joins."""
    relations = {"same": lambda a, b: a == b, "fewer": lambda a, b: a < b}
    for name, rel in relations.items():
        if all(rel(a, b) for a, b in demos):
            brain.bind(token, ("relation", name))
            brain.note("word", f"'{token}' joins things that are the {name} amount")
            return brain.vocab[token]
    return None


def is_numeral(brain, token):
    return bool(token) and all(brain.vocab.get(ch, ("",))[0] == "number" and len(ch) == 1
                               for ch in token)


def read_number(brain, token):
    """Returns (value, explanation) or (None, reason)."""
    meaning = brain.vocab.get(token)
    if meaning and meaning[0] == "number":
        things = "thing" if meaning[1] == 1 else "things"
        return meaning[1], f"'{token}' is a word I was shown with {meaning[1]} {things}"
    if not is_numeral(brain, token):
        return None, f"I don't know the word '{token}'"
    law = brain.library.get(NUMERAL_LAW)
    if law is None:
        return None, "I can't read numerals with more than one mark yet"
    value = brain.vocab[token[0]][1]
    for ch in token[1:]:
        value = brain.library.call(NUMERAL_LAW, value, brain.vocab[ch][1])
    return value, (f"I read '{token}' mark by mark with my place-value law "
                   f"(value so far, next mark) -> {NUMERAL_LAW}")


def speak_number(brain, n):
    """Write a quantity as marks by inverting the place-value law."""
    marks = {m[1]: tok for tok, m in brain.vocab.items()
             if m[0] == "number" and len(tok) == 1}
    if n in marks:
        return marks[n]
    if brain.library.get(NUMERAL_LAW) is None:
        return None
    for last in sorted(marks):
        lo, hi = 1, n
        while lo <= hi:     # the law grows with its first argument: search by halving
            mid = (lo + hi) // 2
            try:
                v = brain.library.call(NUMERAL_LAW, mid, last)
            except Overflow:
                return None
            if v == n:
                prefix = speak_number(brain, mid)
                return None if prefix is None else prefix + marks[last]
            if v < n:
                lo = mid + 1
            else:
                hi = mid - 1
    return None
