"""Kinds of thing, found before any word for them (Stage 3, language).

Ultron measures every thing it sees (senses/things.py): its hue, size, elongation, fill
and place. Looking at many tables, it asks of each measure on its own: do the values fall
into separate groups? A grouping is kept only when it is the shorter description (MDL):
saying which group a value is in, and where in its group, must cost fewer bits than
saying where it is in the whole range, including the cost of the group boundaries.
Values spread evenly (where things lie on the table) never pay for a boundary.

These groups are concepts before words: later, a word can mean "in this group".
"""

import math

PRECISION = 1000        # values are told apart to a thousandth of what the measure spans
CIRCULAR = {"hue": 360.0}


def _cost(values, groups, span):
    """Bits to describe sorted values given groups [(lo, hi)]: which group (by its share)
    and where inside it, to the measure's precision; plus each boundary."""
    delta = span / PRECISION
    n = len(values)
    bits = 2 * math.log2(PRECISION) * len(groups)
    for lo, hi in groups:
        k = sum(1 for v in values if lo <= v <= hi)
        if k < 2:
            return math.inf         # one value says nothing about where a group lies
        # k values seen in a group: its true width is likely wider than theirs
        # (the unbiased guess for evenly spread values is (k + 1) / (k - 1) times wider)
        width = (hi - lo + delta) * (k + 1) / (k - 1)
        bits += k * (math.log2(n / k) + math.log2(width / delta))
    return bits


def _best_split(values, span, max_groups=8):
    """The shortest description of sorted values: cut at some of the widest gaps."""
    gaps = sorted(range(1, len(values)), key=lambda i: (-(values[i] - values[i - 1]), i))
    best = None
    for k in range(0, min(max_groups, len(values)) ):
        cuts = sorted(gaps[:k])
        bounds = [0] + cuts + [len(values)]
        groups = [(values[a], values[b - 1]) for a, b in zip(bounds, bounds[1:])]
        bits = _cost(values, groups, span)
        if best is None or bits < best[0] - 1e-9:
            best = (bits, groups)
    return best


def discover(things, measures):
    """things: [{measure: value}]. Returns {measure: {"groups": [[lo, hi]], "turn": t,
    "bits": (one group, grouped)}} for every measure, groups or not."""
    found = {}
    for m in measures:
        vals = [t[m] for t in things]
        turn = 0.0
        if m in CIRCULAR:
            # a circle: cut it where the widest empty arc is, then it is a line
            full = CIRCULAR[m]
            s = sorted(v % full for v in vals)
            arcs = [(s[i] - s[i - 1]) % full if i else (s[0] + full - s[-1]) for i in range(len(s))]
            i = max(range(len(s)), key=lambda j: (arcs[j], -j))
            turn = round(s[i] - arcs[i] / 2, 6) % full      # the middle of the empty arc
            vals = [(v - turn) % full for v in vals]
        vals = sorted(vals)
        span = (vals[-1] - vals[0]) or 1.0
        one = _cost(vals, [(vals[0], vals[-1])], span)
        bits, groups = _best_split(vals, span)
        found[m] = {"groups": [[round(lo, 6), round(hi, 6)] for lo, hi in groups],
                    "turn": turn, "bits": [round(one, 1), round(bits, 1)]}
    return found


def group_of(categories, measure, value):
    """Which group a value falls in: the one it is inside, or else the nearest (a value
    between two groups goes to the closer edge). None when the measure has one group."""
    c = categories[measure]
    if len(c["groups"]) < 2:
        return None
    if measure in CIRCULAR:
        value = (value - c["turn"]) % CIRCULAR[measure]
    best = min(range(len(c["groups"])),
               key=lambda i: (max(c["groups"][i][0] - value, value - c["groups"][i][1], 0.0), i))
    return best


def kinds_of(categories, thing):
    """A thing as the groups it is in: {measure: group} for measures that group."""
    out = {}
    for m in sorted(categories):
        g = group_of(categories, m, thing[m])
        if g is not None:
            out[m] = g
    return out
