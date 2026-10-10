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
ANY = "*"               # an open parameter: any value its operation takes, chosen per task
# steps whose content is a law learned from each task's own examples: a block may end
# with one ("..., then learn a thing law on the result"); the law is learned per task
LAWS = ("cells", "things", "marks", "pick", "moves", "symmetry", "copies", "gaps",
        "summary", "tiles")
MAX_BLOCKS = 24


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


def _pieces(steps):
    """Contiguous pieces of 2-4 steps; a learned law may only end a piece."""
    for n in (2, 3, 4):
        for i in range(len(steps) - n + 1):
            piece = tuple(steps[i:i + n])
            if any(name in LAWS for name, _ in piece[:-1]):
                continue
            yield piece


def candidates(programs):
    """Pieces of the programs that describe tasks: {piece: set of tasks that used it}.
    Besides each piece as it is: the piece with one colour left open, with one parameter
    left open, or ("turn, do something, turn back") with its inner step left open."""
    seen = {}
    for task, prog in programs.items():
        steps = [_norm(s) for s in prog if s[0] != "colourmap"]
        steps = [(n, None if n in LAWS else _tup(p)) for n, p in steps]
        for piece in _pieces(steps):
            seen.setdefault(piece, set()).add(task)
            for j, (name, p) in enumerate(piece):
                ab = _abstract((name, p))
                if ab is not None:
                    seen.setdefault(piece[:j] + (ab,) + piece[j + 1:], set()).add(task)
                if p is not None and name not in LAWS:
                    seen.setdefault(piece[:j] + ((name, ANY),) + piece[j + 1:],
                                    set()).add(task)
            if len(piece) == 3 and piece[1][0] not in LAWS:
                seen.setdefault((piece[0], (STEP, None), piece[2]), set()).add(task)
    return seen


def _cost(piece):
    """What writing the block down costs (its fixed steps), and what each use saves
    (the steps it replaces, minus the block's own name). An open colour, parameter or
    step is named per use either way: each choice is one entry of the search's list."""
    fixed = sum(1 for name, _ in piece if name != STEP)
    return fixed, fixed - 1


def learn(programs):
    """The building blocks worth having: pieces whose use saves more description than
    they cost. Returns [{"steps": [...], "uses": n, "saving": s}] best first.

    programs: {task: steps} -- exact solutions, or descriptions with exceptions
    (descriptions.py): both are the shortest descriptions Ultron has of those tasks."""
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
    # equally short: the block with the narrower open slot (fewer choices for the search)
    out.sort(key=lambda b: (-b["saving"], -len(b["steps"]), _width(b["steps"]),
                            json.dumps(b["steps"])))
    # a block adds nothing when a block already kept is at least as long and is used by
    # every task this one is (it is a piece of that block, or a more specific copy)
    kept = []
    for b in out:
        if any(set(b["tasks"]) <= set(k["tasks"]) and len(k["steps"]) >= len(b["steps"])
               for k in kept):
            continue
        kept.append(b)
        if len(kept) == MAX_BLOCKS:
            break
    return kept


def _width(steps):
    return sum(2 if n == STEP else 1 if p == ANY else 0 for n, p in steps)


def law_tail(b):
    """The kind of law a block ends with (learned per task on its result), or None."""
    name = b["steps"][-1][0]
    return name if name in LAWS else None


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


def _spell(steps, param):
    """A block's steps with its open colour, parameter or step filled in (a law tail
    is left out: the search learns it on the result)."""
    colour, fill = param
    out = []
    for name, p in steps:
        if name in LAWS:
            continue
        if name == STEP:
            name, p = fill
        elif p == ANY:
            p = fill
        out.append((name, _fill(p, colour)))
    return out


def operations(blocks, ctx):
    """Each block as one operation for the search (an open colour ranges over the task's
    colours, an open parameter over the values its operation takes for this task, an
    open step over every operation)."""
    out = []
    reg = O.registry(ctx)
    funcs = {name: f for name, f, _ in reg}
    values = {}
    for name, _, p in reg:
        values.setdefault(name, []).append(p)
    for i, b in enumerate(blocks):
        steps = [(n, _tup(p)) for n, p in b["steps"]]
        if any(name not in funcs and name != STEP and name not in LAWS for name, _ in steps):
            continue
        has_open = any(p == OPEN or (isinstance(p, (list, tuple)) and OPEN in p)
                       for _, p in steps)
        colours = sorted(set(ctx["out_colours"]) | set(ctx["in_colours"])) if has_open \
            else [None]
        fills = [None]
        if any(n == STEP for n, _ in steps):
            fills = [(n, q) for n, _, q in reg]
        for n, p in steps:
            if p == ANY:
                fills = values.get(n, [])

        def run(g, param, steps=steps):
            for name, p in _spell(steps, param):
                if g is None:
                    return None
                g = funcs[name](g, p)
                if g is not None and (g.size == 0 or g.shape[0] > 30 or g.shape[1] > 30):
                    return None
            return g
        for c in colours:
            for fill in fills:
                out.append((f"block{i + 1}", run, (c, fill)))
    return out


def describe(b):
    return " ▸ ".join("(any step)" if name == STEP else f"(learn a {name} law)" if name in LAWS
                      else name if p is None else f"{name}(any)" if p == ANY
                      else f"{name}({p})" for name, p in b["steps"])


def show_use(b, param):
    """A block as it was used in a task: its open colour, parameter and step filled in."""
    out = [name if p is None else f"{name}({p})" for name, p in _spell(b["steps"], param)]
    return "[" + " ▸ ".join(out) + "]"
