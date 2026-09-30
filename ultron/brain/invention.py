"""Inventing kinds of number from the *shape* of experience.

Shape discovery. Suppose Ultron has confirmed laws saying how an action changes a
state (e.g. what "tick" does to the pointer of a wheel, or what "earn a coin" does
to a purse of coins and IOU notes). Starting from the empty state, it imagines
repeating the action using only its own laws, and looks at the shape it traces:

  * it comes back to the start after k steps: a CYCLE. Numbers go round: after
    k-1 comes 0 again; k repeats change nothing; going back one is going on k-1.
  * it never comes back, and another action undoes it and runs off the *other*
    way from the empty state: a LINE through zero. The far side is below zero,
    and a new step "down", with no floor, comes with it.
  * it never comes back and nothing runs the other way: the ordinary counting
    numbers, which it already has, so nothing new.

  * walking by a smaller unit, it passes each whole unit every n steps, and in
    between is at places no whole number reaches: a FINER line. The places
    between are new numbers (fractions).

In every case it also checks that every state it has ever seen lies on the shape,
and that the steps coincide with something it already counts, so the shape's
positions really are numbers. The same code finds negative numbers in a purse,
clock numbers on a wheel and fractions in a bakery; nothing in it is specific to
any of them. For the finer line it even works out, by testing, which input of its
law is the count, which the kind of piece, and which the wholes.
"""

import itertools

from .dsl import safe_evaluate

REACH = 12  # how far it imagines walking in each direction


def _step(brain, laws, state):
    nxt = {}
    for var, law in laws.items():
        v = safe_evaluate(law.expr, state, brain.library)
        if v is None:
            return None
        nxt[var] = v
    return nxt


def _key(state):
    return tuple(sorted(state.items()))


def _families(brain):
    """action -> {state var: confirmed law}, for complete state descriptions."""
    fam = {}
    for name, spec in brain.memory.specs.items():
        if spec.action and spec.state_var and brain.trusts(name):
            fam.setdefault(spec.action, {})[spec.state_var] = brain.library.get(name)
    out = {}
    for action, laws in fam.items():
        some = next(iter(laws.values()))
        if set(laws) == set(some.params):
            out[action] = laws
    return out


def _seen_states(brain, actions):
    seen = {}
    for name, spec in brain.memory.specs.items():
        if spec.action in actions:
            for ep in brain.memory.of(name):
                seen[_key(ep["inputs"])] = dict(ep["inputs"])
    return list(seen.values())


def _walk(brain, laws, start, steps):
    out, s = [], start
    for _ in range(steps):
        s = _step(brain, laws, s)
        if s is None:
            return out, False
        out.append(s)
    return out, True


def _counts_up(walk, vars_):
    """A variable that reads 1, 2, 3... along the walk (something it already counts)."""
    for v in vars_:
        if all(s[v] == k + 1 for k, s in enumerate(walk)):
            return v
    return None


def look_for_shapes(brain):
    """Record and return the first new shape found, or None."""
    finer = _finer_line(brain)
    if finer:
        return finer
    fams = _families(brain)
    for a in sorted(fams):
        vars_ = sorted(fams[a])
        base = {v: 0 for v in vars_}
        seen = _seen_states(brain, (a,))
        if base not in seen:
            continue
        walk, ok = _walk(brain, fams[a], base, REACH)
        if not ok:
            continue
        back = next((k for k, s in enumerate(walk) if s == base), None)
        if back is not None:
            found = _cycle(brain, a, fams, vars_, base, walk[:back + 1], seen)
        else:
            found = _line(brain, a, fams, vars_, base, walk, seen)
        if found:
            key, inv = found
            brain.inventions[key] = inv
            if inv["shape"] == "cycle" and len(vars_) == 1:
                brain.library.cycles[fams[a][vars_[0]].name] = inv["size"]
            brain.note("invent", inv["story"])
            return inv
    return None


def _cycle(brain, a, fams, vars_, base, loop, seen):
    key = f"cycle:{a}"
    k = len(loop)
    if key in brain.inventions or k < 2 or len({_key(s) for s in loop}) != k:
        return None
    counted = _counts_up(loop[:-1], vars_)
    if counted is None:
        return None
    on_cycle = {_key(s) for s in loop}
    if any(_key(s) not in on_cycle for s in seen):
        return None
    story = (f"Repeating '{a}' from the start, {counted} counts 1, 2, ... {k - 1}, and the "
             f"{k}th '{a}' brings me back to the start. So here numbers go round: after "
             f"{k - 1} comes 0 again. {k} '{a}'s change nothing, and going back one is the "
             f"same as going on {k - 1}. These are a new kind of number that repeats "
             f"every {k}.")
    return key, {"shape": "cycle", "size": k, "up": a, "vars": vars_, "counted": counted,
                 "primitives": [], "lesson": brain.lesson, "story": story}


def _line(brain, a, fams, vars_, base, walk, seen):
    if len({_key(s) for s in walk} | {_key(base)}) != len(walk) + 1:
        return None
    for b in sorted(fams):
        if b == a or set(fams[b]) != set(vars_):
            continue
        key = f"line:{min(a, b)}/{max(a, b)}"
        if key in brain.inventions:
            return None
        both = _seen_states(brain, (a, b))
        # the two actions undo each other on everything seen
        if any(_step(brain, fams[b], _step(brain, fams[a], s) or s) != s or
               _step(brain, fams[a], _step(brain, fams[b], s) or s) != s for s in both):
            continue
        other, ok = _walk(brain, fams[b], base, REACH)
        visited = {_key(base)} | {_key(s) for s in walk}
        if not ok or any(_key(s) in visited for s in other) or \
                len({_key(s) for s in other}) != len(other):
            continue     # b doesn't run off the other way: nothing below zero
        visited |= {_key(s) for s in other}
        if any(_key(s) not in visited for s in both if max(s.values()) <= REACH):
            continue
        up, down = (a, b) if _counts_up(walk, vars_) else (b, a)
        counted = _counts_up(walk if up == a else other, vars_)
        if counted is None:
            continue
        rest = [v for v in vars_ if v != counted]
        story = (f"My {'/'.join(vars_)} states all lie on ONE line: '{up}' and '{down}' undo "
                 f"each other, and from the empty state '{up}' counts {counted} up 1, 2, 3... "
                 f"But '{down}' from the empty state doesn't stop: it keeps going, into states "
                 f"with {', '.join(rest)}. Those are places *below* zero. I'll treat them as "
                 f"numbers too, and use a new step 'down' that has no floor.")
        return key, {"shape": "line", "up": up, "down": down, "vars": vars_,
                     "counted": counted, "primitives": ["down"], "lesson": brain.lesson,
                     "story": story}
    return None


def _holds(brain, law, env):
    try:
        return safe_evaluate(law.expr, env, brain.library)
    except Exception:
        return None


def _finer_line(brain):
    """Is there a law comparing piles of pieces with whole things, where walking by
    pieces is a finer walk than walking by wholes?"""
    if any(inv.get("shape") == "finer line" for inv in brain.inventions.values()):
        return None
    lib = brain.library
    for law in sorted(lib.laws.values(), key=lambda l: l.name):
        if law.out_type != "bool" or len(law.params) != 3 or not brain.trusts(law.name):
            continue
        for count, kind, whole in itertools.permutations(law.params):
            env = lambda c, k, w: {count: c, kind: k, whole: w}
            # 1. pieces of kind 1 ARE whole things: the walk it already knows
            if not all(_holds(brain, law, env(w, 1, w)) and
                       not _holds(brain, law, env(w, 1, w + 1)) for w in range(6)):
                continue
            # 2. a finer walk: n pieces make one whole, one piece makes no whole
            for n in range(2, 7):
                if not _holds(brain, law, env(n, n, 1)):
                    continue
                if any(_holds(brain, law, env(1, n, w)) for w in range(0, 4)):
                    continue
                # 3. can it re-cut in imagination? find a law that scales count and kind
                #    together without changing what balances
                scale = next((t.name for t in lib.binary_int_laws() if all(
                    _holds(brain, law, env(c, k, w)) ==
                    _holds(brain, law, env(lib.call(t.name, c, m), lib.call(t.name, k, m), w))
                    for c in range(0, 7) for k in range(1, 4) for w in range(0, 3)
                    for m in range(1, 4))), None)
                if scale is None:
                    continue
                story = (f"Walking by single pieces of a cake cut into {n}, I pass a whole every "
                         f"{n} steps, and in between I'm at places no whole number reaches: one "
                         f"piece balances no whole number of cakes, yet {n} of them balance "
                         f"exactly 1. So my number line is FINER than I thought: there are "
                         f"numbers *between* my numbers. Every pile of equal pieces is one. "
                         f"And since scaling the count and the kind of piece together with my "
                         f"'{scale}' law never changes what balances, two piles are the same "
                         f"number when, cut into the same kind of piece, they have the same "
                         f"count. My whole numbers are piles of pieces 'cut into 1'.")
                key = f"finer:{law.name}"
                inv = {"shape": "finer line", "law": law.name,
                       "roles": {"count": count, "kind": kind, "whole": whole},
                       "scale": scale, "primitives": [], "lesson": brain.lesson,
                       "example": n, "story": story}
                brain.inventions[key] = inv
                brain.note("invent", story)
                return inv
    return None


# kept for callers that only care about lines
look_for_line = look_for_shapes


def position(brain, key, state):
    """Where a state sits on an invented shape: on a line, +k above the empty state
    or -k below it; on a cycle, how many steps round from the start."""
    inv = brain.inventions.get(key)
    if inv is None:
        return None
    fams = _families(brain)
    base = {v: 0 for v in inv["vars"]}
    state = {v: state[v] for v in inv["vars"]}
    if inv["shape"] == "cycle":
        s = base
        for k in range(inv["size"]):
            if s == state:
                return k
            s = _step(brain, fams[inv["up"]], s)
        return None
    toward_down, toward_up = state, state
    for k in range(sum(abs(v) for v in state.values()) + 2):
        if toward_down == base:
            return k
        if toward_up == base:
            return -k
        toward_down = _step(brain, fams[inv["down"]], toward_down) if toward_down else None
        toward_up = _step(brain, fams[inv["up"]], toward_up) if toward_up else None
    return None


def find_inverses(brain):
    """Once numbers below zero exist, work out which steps undo which, by imagining
    with its own laws. up/down come from the line itself; for each law used as a
    step, look for another law that always brings the result back."""
    from .dsl import Overflow
    line = next((inv for inv in brain.inventions.values() if "down" in inv["primitives"]), None)
    if line is None:
        return
    lib = brain.library
    if "succ" not in lib.inverses:
        lib.inverses["succ"] = ["down"]
        lib.inverses["down"] = ["succ"]
        brain.note("reflect", "'up one' and 'down one' undo each other on my line")
    for law in lib.binary_int_laws():
        if law.name in lib.inverses:
            continue
        for other in lib.binary_int_laws():
            if other.name == law.name:
                continue
            for order in ("acc_first", "t_first"):
                ok = True
                try:
                    for x in range(-5, 6):
                        for t in range(0, 5):
                            y = lib.call(law.name, x, t)
                            back = lib.call(other.name, y, t) if order == "acc_first" \
                                else lib.call(other.name, t, y)
                            if back != x:
                                ok = False
                                break
                        if not ok:
                            break
                except Overflow:
                    ok = False
                if ok:
                    lib.inverses[law.name] = [other.name, order]
                    brain.note("reflect", f"imagining with my laws: '{other.name}' always undoes "
                                          f"'{law.name}'")
                    break
            if law.name in lib.inverses:
                break
