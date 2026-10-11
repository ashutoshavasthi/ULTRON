"""Intuition: which operations to try first, learned from Ultron's own solved tasks.

A task is described by a few plain features (is the output smaller, the same size or
bigger? are new colours added? are colours removed? is the picture divided into
panels?). From every task Ultron has solved, it counts which operations its programs
used under which features. On a new task it tries operations in order of how often they
helped in tasks like this one. The search itself is unchanged and every answer is still
checked against every example, so intuition can only make search faster, never wrong.
"""

import json
import math
import os

from .grid import colours, parts

HERE = os.path.dirname(__file__)
PATH = os.path.join(HERE, "guide.json")


def task_features(train):
    shapes = set()
    added = removed = False
    panels = False
    for i, o in train:
        shapes.add("same" if i.shape == o.shape else
                   "smaller" if o.size < i.size else "bigger")
        ci, co = set(colours(i)), set(colours(o))
        added |= bool(co - ci)
        removed |= bool(ci - co)
        panels |= parts(i) is not None
    shape = shapes.pop() if len(shapes) == 1 else "mixed"
    return [f"shape:{shape}", f"added:{added}", f"removed:{removed}", f"panels:{panels}"]


def learn(solved):
    """solved: [(features, [operation names])] -> counts per feature and operation."""
    counts, totals = {}, {}
    for feats, ops in solved:
        for f in feats:
            totals[f] = totals.get(f, 0) + 1
            for op in set(ops):
                counts.setdefault(f, {})
                counts[f][op] = counts[f].get(op, 0) + 1
    return {"counts": counts, "totals": totals, "tasks": len(solved)}


def save(guide, path=PATH):
    with open(path, "w") as f:
        json.dump(guide, f, indent=1, sort_keys=True)
        f.write("\n")


def load(path=PATH):
    if not os.path.exists(path):
        return None
    with open(path) as f:
        return json.load(f)


def score(guide, feats, op):
    """How promising an operation is for a task with these features (log-odds, smoothed)."""
    s = 0.0
    for f in feats:
        n = guide["totals"].get(f, 0)
        k = guide["counts"].get(f, {}).get(op, 0)
        s += math.log((k + 0.5) / (n + 1.0))
    return s


def order(guide, train, registry):
    """The registry, most promising operations first (ties keep the original order)."""
    if guide is None:
        return registry
    feats = task_features(train)
    ranked = sorted(range(len(registry)),
                    key=lambda i: (-score(guide, feats, registry[i][0]), i))
    return [registry[i] for i in ranked]
