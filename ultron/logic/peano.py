"""From discovered laws to formal proofs.

A law Ultron found of the form "repeat n times [F] starting from x" is exactly
a pair of Peano-style rules:

    L(..., n=0,    ...) -> x
    L(..., n=S(k), ...) -> F(L(..., n=k, ...))

So the rules are *derived from its own programs*, not typed in. The prover
rewrites a term step by step; the checker independently verifies that every
single step is a legal use of a rule. Both are completely deterministic.

Terms: ("0",) ; ("S", t) ; ("P", t) ; (law_name, a, b) ; pattern vars ("?", name)
"""

ZERO = ("0",)
MAX_STEPS = 5000


def numeral(n):
    t = ZERO
    for _ in range(n):
        t = ("S", t)
    return t


def value(t):
    n = 0
    while t[0] == "S":
        n += 1
        t = t[1]
    return n if t == ZERO else None


def show(t):
    v = value(t)
    if v is not None:
        return str(v)
    if t[0] == "?":
        return t[1]
    if t[0] in ("S", "P"):
        return f"{t[0]}({show(t[1])})"
    return f"{t[0]}({', '.join(show(a) for a in t[1:])})"


PRED_RULES = [
    ("P-zero", ("P", ZERO), ZERO),
    ("P-succ", ("P", ("S", ("?", "x"))), ("?", "x")),
]


def _pattern(expr):
    tag = expr[0]
    if tag == "var":
        return ("?", expr[1])
    if tag == "const" and isinstance(expr[1], int):
        return numeral(expr[1])
    raise ValueError("only variables and numbers can appear here")


def rules_from_law(law):
    """Turn a law into rewrite rules, or None if it can't be written in Peano
    arithmetic (e.g. a law using the invented 'down' step, which goes below zero,
    where Peano's numbers don't exist)."""
    e = law.expr
    if len(law.params) != 2:
        return None
    if e[0] == "call" and e[2][0] == "var" and e[3][0] == "var":
        # a law defined as another law: get_paid(purse, wage) -> merge(wage, purse)
        head = (law.name,) + tuple(("?", p) for p in law.params)
        return [(f"{law.name}-def", head, (e[1], ("?", e[2][1]), ("?", e[3][1])))]
    if e[0] != "iter" or e[2][0] != "var" or e[1][0] not in ("succ", "pred", "call"):
        return None
    counter = e[2][1]
    try:
        start = _pattern(e[3])
        step_arg = _pattern(e[1][2]) if e[1][0] == "call" else None
    except ValueError:
        return None
    k = ("?", "k")

    def head(counter_term):
        return (law.name,) + tuple(counter_term if p == counter else ("?", p) for p in law.params)

    def apply_f(acc):
        if e[1][0] == "succ":
            return ("S", acc)
        if e[1][0] == "pred":
            return ("P", acc)
        return (e[1][1], acc, step_arg)

    return [(f"{law.name}-zero", head(ZERO), start),
            (f"{law.name}-step", head(("S", k)), apply_f(head(k)))]


def all_rules(library):
    rules = list(PRED_RULES)
    for name in sorted(library.laws):
        r = rules_from_law(library.laws[name])
        if r:
            rules.extend(r)
    return rules


def match(pattern, term, env):
    if pattern[0] == "?":
        name = pattern[1]
        if name in env:
            return env[name] == term
        env[name] = term
        return True
    if pattern[0] != term[0] or len(pattern) != len(term):
        return False
    return all(match(p, t, env) for p, t in zip(pattern[1:], term[1:]))


def fill(pattern, env):
    if pattern[0] == "?":
        return env[pattern[1]]
    return (pattern[0],) + tuple(fill(p, env) for p in pattern[1:])


def at(term, path):
    for i in path:
        term = term[i]
    return term


def replace(term, path, new):
    if not path:
        return new
    i = path[0]
    return term[:i] + (replace(term[i], path[1:], new),) + term[i + 1:]


def _redex(term, rules, path=()):
    """Innermost-leftmost position where some rule applies."""
    for i in range(1, len(term)):
        if isinstance(term[i], tuple):
            found = _redex(term[i], rules, path + (i,))
            if found:
                return found
    for name, lhs, rhs in rules:
        env = {}
        if match(lhs, term, env):
            return path, name, fill(rhs, env)
    return None


def prove(term, rules):
    """Rewrite until no rule applies. Returns the list of steps."""
    steps = []
    while len(steps) < MAX_STEPS:
        found = _redex(term, rules)
        if not found:
            break
        path, name, new = found
        after = replace(term, path, new)
        steps.append({"rule": name, "path": path, "before": term, "after": after})
        term = after
    return steps


def check(claim_lhs, claim_value, steps, rules):
    """Independently verify a proof. Returns (ok, message)."""
    by_name = {name: (lhs, rhs) for name, lhs, rhs in rules}
    current = claim_lhs
    for i, st in enumerate(steps):
        if st["before"] != current:
            return False, f"step {i + 1} doesn't start where the last one ended"
        if st["rule"] not in by_name:
            return False, f"step {i + 1} uses an unknown rule"
        lhs, rhs = by_name[st["rule"]]
        env = {}
        if not match(lhs, at(current, st["path"]), env):
            return False, f"step {i + 1}: rule {st['rule']} doesn't apply there"
        if replace(current, st["path"], fill(rhs, env)) != st["after"]:
            return False, f"step {i + 1}: wrong result for rule {st['rule']}"
        current = st["after"]
    if value(current) != claim_value:
        return False, f"the proof ends at {show(current)}, not {claim_value}"
    return True, f"checked: {len(steps)} steps, each a legal rule use"
