"""Perception: turning what is in front of Ultron into facts it can reason about.

Counting is done by tallying objects one at a time. This (like "same" and
"fewer") is treated as innate, the way babies can track small sets of things.
"""


def count(objects):
    n = 0
    for _ in objects:
        n += 1
    return n


def present(objects):
    return count(objects) > 0


def read_marks(marks, vocab):
    """Read written marks (e.g. '4', '7') into the quantities they were
    taught to mean. Unknown marks come back as None."""
    out = []
    for m in marks:
        meaning = vocab.get(m)
        out.append(meaning[1] if meaning and meaning[0] == "number" else None)
    return out
