"""Inventing concepts from the shape of experience.

Line discovery: suppose Ultron has confirmed laws saying how two actions change
a state (e.g. what "earn a coin" and "spend a coin" do to a purse of coins and
IOU notes). It imagines applying them, using only its own laws, and checks:

  1. the two actions undo each other on every state it has met;
  2. starting from the empty state, repeating either action never revisits a
     state, so all states lie on ONE line through the empty state;
  3. every state it has ever seen lies on that line;
  4. along one direction, the steps coincide with something it already counts
     (coins). That side is the numbers it already knows.

Then the states on the *other* side are something new: positions that continue
past the empty state, below zero. Ultron makes up that idea itself, and with it
a new primitive: "down", a step that has no floor at zero. Nobody names it
until afterwards.
"""

from .dsl import safe_evaluate

REACH = 12  # how far it imagines walking along the line in each direction


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
        if spec.action and spec.state_var and name in brain.library:
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


def look_for_line(brain):
    """Returns the invention record if a line was found (and records it)."""
    fams = _families(brain)
    actions = sorted(fams)
    for i, a in enumerate(actions):
        for b in actions[i + 1:]:
            if set(fams[a]) != set(fams[b]):
                continue
            key = f"line:{a}/{b}"
            if key in brain.inventions:
                continue
            found = _try_line(brain, a, b, fams)
            if found:
                brain.inventions[key] = found
                brain.note("invent", found["story"])
                return found
    return None


def _try_line(brain, a, b, fams):
    seen = _seen_states(brain, (a, b))
    vars_ = sorted(fams[a])
    base = {v: 0 for v in vars_}
    if base not in seen:
        return None
    # 1. the actions undo each other
    for s in seen:
        sa, sb = _step(brain, fams[a], s), _step(brain, fams[b], s)
        if sa is None or sb is None:
            return None
        if _step(brain, fams[b], sa) != s or _step(brain, fams[a], sb) != s:
            return None
    # 2. walking from the empty state never revisits a state
    chains = {}
    visited = {_key(base)}
    for act in (a, b):
        chain, s = [], base
        for _ in range(REACH):
            s = _step(brain, fams[act], s)
            if s is None or _key(s) in visited:
                return None
            visited.add(_key(s))
            chain.append(s)
        chains[act] = chain
    # 3. everything seen lies on the line
    if any(_key(s) not in visited for s in seen if max(s.values()) <= REACH):
        return None
    # 4. which direction is counting up something it already knows?
    up = None
    for act in (a, b):
        for v in vars_:
            if all(s[v] == k + 1 for k, s in enumerate(chains[act])):
                up, counted = act, v
                break
        if up:
            break
    if up is None:
        return None
    down = b if up == a else a
    other = [v for v in vars_ if v != counted]
    story = (f"My {'/'.join(vars_)} states all lie on ONE line: '{up}' and '{down}' undo "
             f"each other, and from the empty state '{up}' counts {counted} up 1, 2, 3... "
             f"But '{down}' from the empty state doesn't stop: it keeps going, into states "
             f"with {', '.join(other)}. Those are places *below* zero. I'll treat them as "
             f"numbers too, and use a new step 'down' that has no floor.")
    return {"up": up, "down": down, "vars": vars_, "counted": counted,
            "primitives": ["down"], "lesson": brain.lesson, "story": story}


def position(brain, key, state):
    """Where a state sits on an invented line: +k above the empty state, -k below.
    Walks both ways at once until it reaches the empty state."""
    inv = brain.inventions.get(key)
    if inv is None:
        return None
    fams = _families(brain)
    base = {v: 0 for v in inv["vars"]}
    state = {v: state[v] for v in inv["vars"]}
    toward_down, toward_up = state, state
    for k in range(sum(abs(v) for v in state.values()) + 2):
        if toward_down == base:
            return k
        if toward_up == base:
            return -k
        toward_down = _step(brain, fams[inv["down"]], toward_down) if toward_down else None
        toward_up = _step(brain, fams[inv["up"]], toward_up) if toward_up else None
    return None
