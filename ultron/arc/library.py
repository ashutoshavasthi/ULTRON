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
STEP = "?"              # an open step: any one operation, chosen per task


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
        steps = [_norm(s) for s in prog if s[0] not in ("colourmap", "cells", "things", "marks", "pick", "moves", "symmetry", "copies", "gaps", "summary")]
        steps = [(n, _tup(p)) for n, p in steps]
        for n in (2, 3, 4):
            for i in range(len(steps) - n + 1):
                piece = tuple(steps[i:i + n])
                seen.setdefault(piece, set()).add(task)
                # the same piece with one colour left open
                for j, st in enumerate(piece):
                    ab = _abstract(st)
                    if ab is not None:
                        open_piece = piece[:j] + (ab,) + piece[j + 1:]
                        seen.setdefault(open_piece, set()).add(task)
                # ... or with one inner step left open ("turn, do something, turn back")
                if n == 3:
                    seen.setdefault((piece[0], (STEP, None), piece[2]), set()).add(task)
    return seen


def _cost(piece):
    """What writing the block down costs (its fixed steps), and what each use saves
    (the steps it replaces, minus the block's own name and any step left open)."""
    fixed = sum(1 for name, _ in piece if name != STEP)
    return fixed, fixed - 1


def learn(programs):
    """The building blocks worth having: pieces whose use saves more description than
    they cost. Returns [{"steps": [...], "uses": n, "saving": s}] best first."""
    out = []
    for piece, tasks in candidates(programs).items():
        uses = len(tasks)
        # written once it costs its fixed steps; each use then names 1 step instead of
        # them (an open colour or step is named per use either way)
        cost, per_use = _cost(piece)
        saving = uses * per_use - cost
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
        if any(name not in funcs and name != STEP for name, _ in steps):
            continue
        has_open = any(p == OPEN or (isinstance(p, (list, tuple)) and OPEN in p)
                       for _, p in steps)
        colours = sorted(set(ctx["out_colours"]) | set(ctx["in_colours"])) if has_open \
            else [None]
        inner = [(n, q) for n, _, q in O.registry(ctx)] if any(n == STEP for n, _ in steps) \
            else [None]

        def run(g, param, steps=steps):
            colour, step = param
            for name, p in steps:
                if g is None:
                    return None
                if name == STEP:
                    name, p = step
                g = funcs[name](g, _fill(p, colour))
                if g is not None and (g.size == 0 or g.shape[0] > 30 or g.shape[1] > 30):
                    return None
            return g
        for c in colours:
            for st in inner:
                out.append((f"block{i + 1}", run, (c, st)))
    return out


def describe(b):
    return " ▸ ".join("(any step)" if name == STEP else name if p is None else f"{name}({p})"
                      for name, p in b["steps"])


def show_use(b, param):
    """A block as it was used in a task: its open colour and step filled in."""
    colour, step = param
    out = []
    for name, p in b["steps"]:
        if name == STEP:
            name, p = step
        p = _fill(p, colour)
        out.append(name if p is None else f"{name}({p})")
    return "[" + " ▸ ".join(out) + "]"
