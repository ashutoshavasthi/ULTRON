"""Programs of both kinds of word: the shortest one that explains a puzzle exactly.

Hand-written words are run by their code; learned words are run by the interpreter and
snapped to exact pictures. A program counts only if it turns every example's input into
its output exactly. Shortest first, so the first program found is a shortest one.
"""

import numpy as np

from .measure import same
from .vocab import run


def _key(grids):
    return tuple(None if g is None else (g.shape, g.tobytes()) for g in grids)


def _free_words(vocab, slots, puzzle):
    cols = sorted({int(c) for _, o in puzzle["train"] for c in np.unique(o)})
    out = []
    for op, takes_colour in slots:
        out += [vocab.free(op, c) for c in cols] if takes_colour else [vocab.free(op)]
    return out


def explain(puzzle, vocab, model=None, slots=(), depth=2, side=10, want=2, known=None):
    """Up to `want` shortest programs (lists of words) that explain the puzzle's examples."""
    known = vocab.known if known is None else known
    free = _free_words(vocab, slots, puzzle) if model is not None else []
    ins = [g for g, _ in puzzle["train"]]
    outs = [o for _, o in puzzle["train"]]
    level = [((), ins)]
    seen = {_key(ins)}
    found = []
    for _ in range(depth):
        nxt = []
        for prog, grids in level:                   # hand-written words: by code
            for w in known:
                res = [run(w, g) for g in grids]
                if any(r is None or max(r.shape) > side for r in res):
                    continue
                nxt.append((prog + (w,), res))
        if free:                                    # learned words: by the interpreter
            jobs = [(prog, w, g) for prog, grids in level for w in free for g in grids]
            preds = model.run([g for _, _, g in jobs], [vocab.ids(w) for _, w, _ in jobs])
            n = len(ins)
            for k in range(0, len(jobs), n):
                res = preds[k:k + n]
                if all(r is not None for r in res):
                    nxt.append((jobs[k][0] + (jobs[k][1],), res))
        level = []
        for prog, res in nxt:
            if all(same(r, o) for r, o in zip(res, outs)):
                found.append(list(prog))
                if len(found) == want:
                    return found
                continue
            k = _key(res)
            if k not in seen:
                seen.add(k)
                level.append((prog, res))
        if found:
            return found
    return found


def carry_out(program, g, vocab, model=None):
    """Run a program on one picture (None when a step doesn't give a picture)."""
    for w in program:
        if g is None:
            return None
        g = model.run([g], [vocab.ids(w)])[0] if vocab.is_free(w) else run(w, g)
    return g


def solve(puzzle, vocab, model=None, slots=(), depth=2, side=10, known=None):
    """The puzzle's test answered by its shortest explanations: (right?, programs)."""
    progs = explain(puzzle, vocab, model, slots, depth, side, known=known)
    answers = [carry_out(p, puzzle["test"][0], vocab, model) for p in progs]
    return any(same(a, puzzle["test"][1]) for a in answers), progs
