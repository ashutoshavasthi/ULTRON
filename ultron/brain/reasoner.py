"""The reasoner: answer questions by grounding words in concepts, running the
laws Ultron found, and keeping every step so it can say *why*."""

from . import units as U
from .dsl import Overflow, show
from .language import prefixes, read_number, speak_number

FILLER = {"what", "is", "?", "whats", "what's", "equals", "=", "how", "much"}
EQUALS = {"equals", "="}
UNKNOWN = "what"
_ORDER = {-1: "less than", 0: "the same as", 1: "more than"}


def _cmp(a, b):
    return (a > b) - (a < b)


def _join_prefix_words(brain, tokens):
    """'negative three' is one number, not two words."""
    words = {p for p in prefixes(brain) if p.isalpha()}
    out, i = [], 0
    while i < len(tokens):
        if tokens[i] in words and i + 1 < len(tokens):
            out.append(tokens[i] + " " + tokens[i + 1])
            i += 2
        else:
            out.append(tokens[i])
            i += 1
    return out


def symmetric(brain, law_name):
    """How many experiences show that swapping the two inputs never changes this
    law's result? Checked on every experience where the swapped version can be
    worked out; 0 if any of them disagrees (or too few could be checked)."""
    law = brain.library.get(law_name)
    eps = brain.memory.of(law_name)
    if law is None or len(law.params) != 2:
        return 0
    p, q = law.params
    checked = 0
    for e in eps:
        try:
            swapped = brain.library.call(law_name, e["inputs"][q], e["inputs"][p])
        except Overflow:
            continue    # the swapped situation is itself outside what the law covers
        if swapped != e["outcome"]:
            return 0
        checked += 1
    return checked if checked >= 5 else 0


def outside_experience(brain, law_name, a, b):
    """Magnitude is not a problem (rules generalise), but a *kind* of situation
    Ultron has never once met is: e.g. taking away more than there is.
    Returns an explanation if (a, b) relate in a way never experienced."""
    law = brain.library.get(law_name)
    eps = brain.memory.of(law_name)
    if not eps or len(law.params) != 2:
        return None
    p, q = law.params
    for name, v in ((p, a), (q, b)):
        if v < 0 and not any(e["inputs"][name] < 0 for e in eps):
            return (f"in all {len(eps)} of my '{law_name}' experiences, {name} was never "
                    f"below zero; I have never seen this happen, so I can't say")
    seen = {_cmp(e["inputs"][p], e["inputs"][q]) for e in eps}
    if _cmp(a, b) in seen:
        return None
    return (f"in all {len(eps)} of my '{law_name}' experiences, {p} was never "
            f"{_ORDER[_cmp(a, b)]} {q}; I have never seen this happen, so I can't say")


class Answer:
    def __init__(self, value, text, steps):
        self.value = value
        self.text = text
        self.steps = steps

    def __str__(self):
        lines = [self.text] + [f"  - {s}" for s in self.steps]
        return "\n".join(lines)


def _law_note(brain, law_name):
    law = brain.library.get(law_name)
    where = law.provenance.get("lesson")
    return f"my law '{law_name}' (found in lesson {where}): {law_name}(" + \
           ", ".join(law.params) + f") = {show(law.expr)}"


def arithmetic(brain, question):
    raw = _join_prefix_words(brain, question.lower().replace("?", " ").split())
    if any(t in EQUALS for t in raw) and UNKNOWN in raw[1:] or (
            any(t in EQUALS for t in raw) and raw and raw[0] == UNKNOWN
            and len(raw) > 1 and brain.vocab.get(raw[1], ("",))[0] == "op"):
        return inverse(brain, raw)
    tokens = [t for t in raw if t not in FILLER]
    if not tokens:
        return Answer(None, "I didn't hear a question.", [])
    from . import amounts
    if amounts.invented(brain):
        sep = amounts.separator(brain)
        if any((sep and sep in t and not t.startswith(sep)) or
               brain.vocab.get(t, ("",))[0] == "inv_op" for t in tokens):
            value, text, steps = amounts.arithmetic(brain, tokens)
            if value is None:
                return Answer(None, f"I can't answer that: {text}", steps)
            return Answer(value, text, steps)
    steps = []
    value, why = read_number(brain, tokens[0])
    if value is None:
        return Answer(None, why, steps)
    steps.append(why)
    i = 1
    while i < len(tokens):
        op = brain.vocab.get(tokens[i])
        if not op or op[0] != "op":
            return Answer(None, f"I don't know what '{tokens[i]}' means as an operation", steps)
        if i + 1 >= len(tokens):
            return Answer(None, f"'{tokens[i]}' needs something after it", steps)
        right, why = read_number(brain, tokens[i + 1])
        if right is None:
            return Answer(None, why, steps)
        steps.append(why)
        a, b = (value, right) if op[2] == "xy" else (right, value)
        strange = outside_experience(brain, op[1], a, b)
        checked = symmetric(brain, op[1]) if strange else 0
        if checked and not outside_experience(brain, op[1], b, a):
            steps.append(f"{strange.split(';')[0]}; but in all {checked} of my '{op[1]}' "
                         f"experiences where I could check, swapping the two amounts gave the "
                         f"same result, and swapped, this is a situation I know")
            a, b, strange = b, a, None
        if strange and "below zero" in strange and brain.library.inverses:
            steps.append(f"{strange.split(';')[0]}; but my law works by repeating steps, and "
                         f"repeating a step a below-zero number of times naturally means "
                         f"undoing it that many times. I know what undoes each step, so I'll "
                         f"use that")
            strange = None
        if strange:
            return Answer(None, f"I can't answer that: {strange}", steps)
        try:
            result = brain.library.call(op[1], a, b)
        except Overflow:
            return Answer(None, "that is more than I am willing to count", steps)
        steps.append(f"'{tokens[i]}' is {_law_note(brain, op[1])}; with {a} and {b} it gives "
                     f"{result}")
        value = result
        i += 2
    spoken = speak_number(brain, value)
    text = spoken if spoken is not None else f"{value} (I have no marks for it)"
    steps.append(f"I write {value} as '{text}' by running my place-value law backwards")
    return Answer(value, text, steps)


def inverse(brain, raw):
    """'what times 4 equals 20': find the unknown by trying 0, 1, 2, ... with the
    law itself. Nobody taught division; this is reasoning backwards."""
    eq = next(i for i, t in enumerate(raw) if t in EQUALS)
    left = [t for t in raw[:eq] if t not in ("is", "whats", "what's")]
    if left[:1] == [UNKNOWN] and len(left) == 4 and left[1] == UNKNOWN:
        left = left[1:]
    right = raw[eq + 1:]
    if len(left) != 3 or len(right) != 1 or UNKNOWN not in (left[0], left[2]):
        return Answer(None, "I can only answer 'what OP number equals number' or "
                            "'number OP what equals number'", [])
    op = brain.vocab.get(left[1])
    if not op or op[0] != "op":
        return Answer(None, f"I don't know what '{left[1]}' means as an operation", [])
    steps = []
    known_tok = left[2] if left[0] == UNKNOWN else left[0]
    from . import amounts
    sep = amounts.separator(brain) if amounts.invented(brain) else None
    if sep and any(sep in t and not t.startswith(sep) for t in (known_tok, right[0])):
        goal_a, why = amounts.read_amount(brain, right[0])
        known_a, why2 = amounts.read_amount(brain, known_tok)
        if goal_a is None or known_a is None:
            return Answer(None, why if goal_a is None else why2, steps)
        x = amounts.solve(brain, op[1], op[2], known_a, goal_a, left[0] == UNKNOWN)
        if x is None:
            return Answer(None, "no number or amount I know works", steps)
        steps.append(f"'{left[1]}' is {_law_note(brain, op[1])}")
        steps.append(f"I looked through cakes cut into 1, 2, 3... pieces and found "
                     f"{amounts.show(brain, x)}")
        return Answer(x, amounts.show(brain, x), steps)
    goal, why = read_number(brain, right[0])
    if goal is None:
        return Answer(None, why, steps)
    known, why = read_number(brain, known_tok)
    if known is None:
        return Answer(None, why, steps)
    unknown_first = left[0] == UNKNOWN
    limit = 2 * abs(goal) + abs(known) + 10
    tried = 0
    # with numbers below zero invented, the unknown may be on either side of zero
    candidates = [0] + [v for k in range(1, limit + 1)
                        for v in ((k, -k) if brain.inventions else (k,))]
    for x in candidates:
        xy = (x, known) if unknown_first else (known, x)
        a, b = xy if op[2] == "xy" else (xy[1], xy[0])
        why_not = outside_experience(brain, op[1], a, b)
        if why_not and not ("below zero" in why_not and brain.library.inverses):
            continue
        tried += 1
        try:
            if brain.library.call(op[1], a, b) != goal:
                continue
        except Overflow:
            break
        steps.append(f"'{left[1]}' is {_law_note(brain, op[1])}")
        order = "0, 1, -1, 2, -2" if brain.inventions else "0, 1, 2"
        steps.append(f"I tried numbers {order}, ... in its place and {x} was the first that "
                     f"gives {goal} ({tried} tried)")
        spoken = speak_number(brain, x)
        return Answer(x, spoken if spoken is not None else str(x), steps)
    span = f"-{limit} to {limit}" if brain.inventions else f"0 to {limit}"
    from . import amounts
    if amounts.invented(brain):
        x = amounts.solve(brain, op[1], op[2], (known, 1), (goal, 1), unknown_first)
        if x is not None:
            steps.append(f"'{left[1]}' is {_law_note(brain, op[1])}")
            steps.append(f"no whole number from {span} works, so I looked at amounts: pieces "
                         f"of cakes cut into 2, 3, ... and found {amounts.show(brain, x)}")
            return Answer(x, amounts.show(brain, x), steps)
        return Answer(None, f"no number or amount I know works: for cakes cut into up to 60 "
                            f"pieces, no count of pieces gives {goal}", steps)
    return Answer(None, f"no number I know works: I tried every number from {span} "
                        f"and none of them gives {goal}", steps)


def physics(brain, target, knowns, objects=None):
    """Chain quantity laws: repeatedly use any law with exactly one unknown."""
    objects = dict(objects or {})
    known = dict(knowns)
    steps = []
    units = {}
    for spec in brain.memory.specs.values():
        units.update(spec.units)
    progress = True
    while target not in known and progress:
        progress = False
        # when two laws relate the same quantities, trust the most precise evidence
        for name in sorted(brain.qlaws, key=lambda n: (brain.qlaws[n].spread, n)):
            law = brain.qlaws[name]
            unknown = [v for v in law.powers if v not in known]
            if len(unknown) != 1:
                continue
            spec = brain.memory.specs[name]
            group = objects.get(spec.group_by) if spec.group_by else None
            if law.kind == "grouped" and group not in law.properties:
                continue
            if not brain.law_applies(name, group):
                continue
            value = law.solve(unknown[0], known, group)
            if value is None:
                continue
            known[unknown[0]] = value
            c = law.value_for(group)
            label = brain.names.get(name, name)
            where = (f"= {c:.6g}" if law.kind == "global"
                     else f"= {c:.6g} for {law.group_by} {group}")
            steps.append(f"{label}: {law.formula()} {where}  =>  {unknown[0]} = {value:.6g} "
                         f"{U.name(units.get(unknown[0]))}")
            progress = True
    if target not in known:
        return Answer(None, f"I can't work out {target} from what I know", steps)
    dims = units.get(target)
    return Answer(known[target], f"{target} = {known[target]:.6g} {U.name(dims)}", steps)


def parse_physics(text):
    """'find a given F=21 m=7 spring=S3' -> ('a', {'F': 21.0, 'm': 7.0}, {'spring': 'S3'})"""
    words = text.replace(",", " ").split()
    if len(words) < 2 or words[0] != "find":
        raise ValueError("ask like: find a given F=21 m=7")
    target = words[1]
    knowns, objects = {}, {}
    for w in words[2:]:
        if "=" not in w:
            continue
        k, v = w.split("=", 1)
        try:
            knowns[k] = float(v)
        except ValueError:
            objects[k] = v
    return target, knowns, objects
