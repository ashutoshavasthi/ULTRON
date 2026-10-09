"""Library learning: Ultron grows its own building blocks.

The 38 hand-written operations are frozen. New abilities come from Ultron's own
experience. It looks across the programs it found for solved tasks for pieces that keep
recurring: a chain of two or three operations, possibly with a colour left open (a slot
to be filled per task). A piece becomes a new building block when adding it shortens the
total description of everything Ultron has solved (minimum description length): the
block costs its own length once, and saves (length - 1) every time it is used.

A new block then counts as ONE step in the search, so programs that were too long to
reach become short. That is how learning compounds: the same way multiplication was
found by reusing addition.
"""

import json
import os

from . import ops as O

HERE = os.path.dirname(__file__)
PATH = os.path.join(HERE, "..", "..", "brain", "arc_library.json")
OPEN = "C"              # an open colour slot


def _abstract(step):
    """The step with its colour left open, if it has one."""
    name, p = step
    if name in O.COLOUR_PARAM and isinstance(p, int):
        return (name, OPEN)
    if name in O.COLOUR_IN_TUPLE and isinstance(p, (tuple, list)):
        i = O.COLOUR_IN_TUPLE[name]
        q = list(p)
        q[i] = OPEN
        return (name, tuple(q))
    return None


def _norm(step):
    name, p = step
    return (name, tuple(p) if isinstance(p, list) else p)


def _tup(p):
    return tuple(_tup(x) for x in p) if isinstance(p, (list, tuple)) else p


def candidates(programs):
    """Pieces of solved programs: {piece: set of tasks that used it}."""
    seen = {}
    for task, prog in programs.items():
        steps = [_norm(s) for s in prog if s[0] not in ("colourmap", "cells")]
        steps = [(n, _tup(p)) for n, p in steps]
        for n in (2, 3):
            for i in range(len(steps) - n + 1):
                piece = tuple(steps[i:i + n])
                seen.setdefault(piece, set()).add(task)
                # the same piece with one colour left open
                for j, st in enumerate(piece):
                    ab = _abstract(st)
                    if ab is not None:
                        open_piece = piece[:j] + (ab,) + piece[j + 1:]
                        seen.setdefault(open_piece, set()).add(task)
    return seen


def learn(programs):
    """The building blocks worth having: pieces whose use saves more description than
    they cost. Returns [{"steps": [...], "uses": n, "saving": s}] best first."""
    out = []
    for piece, tasks in candidates(programs).items():
        uses = len(tasks)
        n = len(piece)
        # written once it costs its n steps; each use then names 1 step instead of n (an
        # open colour is named per use either way, so it costs nothing extra)
        saving = uses * (n - 1) - n
        if uses >= 2 and saving > 0:
            out.append({"steps": [list(s) for s in piece], "uses": uses, "saving": saving,
                        "tasks": sorted(tasks)})
    out.sort(key=lambda b: (-b["saving"], -len(b["steps"]), json.dumps(b["steps"])))
    # don't keep a block that is just a more specific copy of a better one
    kept, have = [], set()
    for b in out:
        k = json.dumps(b["steps"])
        if k not in have:
            have.add(k)
            kept.append(b)
    return kept


def save(blocks, path=PATH):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump({"blocks": blocks}, f, indent=1)
        f.write("\n")


def load(path=PATH):
    if not os.path.exists(path):
        return []
    with open(path) as f:
        return json.load(f)["blocks"]


def _fill(p, colour):
    if p == OPEN:
        return colour
    if isinstance(p, (list, tuple)):
        return tuple(_fill(x, colour) for x in p)
    return p


def operations(blocks, ctx):
    """Each block as one operation for the search (open colours range over the task's
    output colours)."""
    out = []
    funcs = {name: f for name, f, _ in O.registry(ctx)}
    for i, b in enumerate(blocks):
        steps = [tuple(s) for s in b["steps"]]
        if any(name not in funcs for name, _ in steps):
            continue
        has_open = any(p == OPEN or (isinstance(p, (list, tuple)) and OPEN in p)
                       for _, p in steps)
        colours = sorted(set(ctx["out_colours"]) | set(ctx["in_colours"])) if has_open \
            else [None]

        def run(g, colour, steps=steps):
            for name, p in steps:
                if g is None:
                    return None
                g = funcs[name](g, _fill(p, colour))
                if g is not None and (g.size == 0 or g.shape[0] > 30 or g.shape[1] > 30):
                    return None
            return g
        for c in colours:
            out.append((f"block{i + 1}", run, c))
    return out


def describe(b):
    return " ▸ ".join(name if p is None else f"{name}({p})" for name, p in b["steps"])
