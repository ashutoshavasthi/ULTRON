"""Inventing new *kinds* of hypothesis.

Every law Ultron found before Phase 3 was one of a few kinds I gave it: "a product
of powers stays the same", "a sum of parts stays the same along a run", "a total
stays the same before and after", "this law is that law repeated", the shapes of
its states, numbers in gaps. It invented concepts *with* those kinds, never a kind.

Here the kinds become data. A kind is a template:

    transform   what to compute from a sequence of readings, written in a small
                grammar: Δ (the step from one reading to the next), ρ (how many
                times bigger the next reading is), composed; optionally divided by
                the step in what was changed (Δy/Δx)
    scope       where that transform stays the same: for everything (global), or
                separately for each object or run (per group)

When no kind it knows explains a world, Ultron searches the grammar, shortest
description first (MDL), for a transform that stays the same. The winner is a law
*and* a new kind of explanation, kept and tried first next time. The innate kinds
are listed here too, so all its kinds live in one library.

What is still mine is the grammar: Δ, ρ, composition and the two scopes. The
kinds themselves are no longer mine. That is one level up again, not the end of
the problem.
"""

import itertools
import statistics

KEY = "kinds"

INNATE = {
    "product": "a product of powers of the readings stays the same (for everything, or "
               "for each object)",
    "sum": "a sum of parts stays the same along a run",
    "conserved total": "a total over objects stays the same before and after an event",
    "repeat": "this law is that law, repeated",
    "shape": "the states my laws walk through form a line, a cycle or a finer line",
    "gap": "an answer is always squeezed between two piles, never on one",
}

OPS = ("Δ", "ρ")
SCOPES = ("global", "per group")
MAX_DEPTH = 2
MIN_GROUPS = 3


# ------------------------------------------------------------------ transforms
def _apply(op, seq):
    out = []
    for a, b in zip(seq, seq[1:]):
        if op == "Δ":
            out.append(b - a)
        else:
            if a == 0:
                return None
            out.append(b / a)
    return out


def transform(template, xs, ys):
    """The template's values along one ordered sequence (xs: what was changed)."""
    zs = list(ys)
    for op in template["y_ops"]:
        zs = _apply(op, zs)
        if zs is None:
            return None
    if template.get("x_op"):
        dx = _apply(template["x_op"], list(xs))
        if dx is None or len(dx) != len(zs) or any(d == 0 for d in dx):
            return None
        zs = [z / d for z, d in zip(zs, dx)]
    return zs


def grammar():
    """Every template, shortest description first."""
    out = []
    for depth in range(1, MAX_DEPTH + 1):
        for ops in itertools.product(OPS, repeat=depth):
            out.append({"y_ops": list(ops), "x_op": None})
        if depth == 1:
            out.append({"y_ops": ["Δ"], "x_op": "Δ"})
    return sorted(out, key=size)


def size(template):
    return len(template["y_ops"]) + (1 if template.get("x_op") else 0)


def describe(template, y="y", x="x"):
    inner = y
    for op in template["y_ops"]:
        inner = f"{op}({inner})"
    return f"{inner}/Δ({x})" if template.get("x_op") else inner


def words(template):
    """The kind in plain words (used in Ultron's own story about it)."""
    ops = template["y_ops"]
    if template.get("x_op"):
        return "equal steps in what I change give equal steps in what I read"
    if ops == ["Δ"]:
        return "each reading goes up by the same step"
    if ops == ["ρ"]:
        return "each reading is the same number of times the one before"
    if ops == ["Δ", "ρ"]:
        return ("the steps between readings shrink (or grow) by the same fraction each "
                "time: it settles toward a resting value")
    if ops == ["Δ", "Δ"]:
        return "the steps between readings change by the same amount each time"
    return f"{describe(template)} stays the same"


# ------------------------------------------------------------------ data
def sequences(episodes, target, order_by, group_by):
    """{group: (xs, ys)} ordered by what was changed; repeated readings averaged."""
    groups = {}
    for ep in episodes:
        g = ep.get(group_by) if group_by else "_"
        groups.setdefault(g, {}).setdefault(ep[order_by], []).append(ep[target])
    out = {}
    for g, by_x in groups.items():
        xs = sorted(by_x)
        out[g] = (xs, [sum(by_x[x]) / len(by_x[x]) for x in xs])
    return out


def _even(xs):
    """Readings taken at equal steps (needed when the transform ignores x)."""
    steps = [b - a for a, b in zip(xs, xs[1:])]
    return all(abs(s - steps[0]) <= 1e-9 * max(1.0, abs(steps[0])) for s in steps)


def _same(values, tol):
    """Do these values stay the same, within the instruments' tolerance?"""
    m = statistics.median(values)
    scale = max(abs(m), max(abs(v) for v in values), 1e-12)
    return max(abs(v - m) for v in values) <= tol * scale


class Found:
    def __init__(self, template, scope, constant, properties, steps, spread):
        self.template, self.scope = template, scope
        self.constant, self.properties = constant, properties
        self.steps, self.spread = steps, spread


def test(template, scope, seqs, tol, needs_even=True):
    """Does this template stay the same under this scope? Returns (Found or None, steps)."""
    per_group, steps = {}, 0
    for g, (xs, ys) in seqs.items():
        if not template.get("x_op") and needs_even and not _even(xs):
            return None, steps
        zs = transform(template, xs, ys)
        steps += len(ys)
        if zs is None:
            return None, steps
        if len(zs) >= 2:
            per_group[g] = zs
    if len(per_group) < MIN_GROUPS:
        return None, steps
    if any(abs(statistics.median(z)) < 1e-12 for z in per_group.values()):
        return None, steps      # a transform that is always nothing explains nothing
    if scope == "global":
        allz = [v for z in per_group.values() for v in z]
        if not _same(allz, tol):
            return None, steps
        c = statistics.median(allz)
        return Found(template, scope, c, {}, steps, _spread(allz)), steps
    if not all(_same(z, tol) for z in per_group.values()):
        return None, steps
    props = {g: statistics.median(z) for g, z in per_group.items()}
    return Found(template, scope, None, props, steps,
                 max(_spread(z) for z in per_group.values())), steps


def _spread(values):
    m = statistics.median(values)
    return max(abs(v - m) for v in values) / max(abs(m), 1e-12)


def search(seqs, tol, templates, budget=10_000):
    """Try templates in order (both scopes, global first: it says more). Returns
    (Found or None, steps)."""
    total = 0
    for t in templates:
        for scope in SCOPES:
            found, steps = test(t, scope, seqs, tol)
            total += steps
            if found is not None:
                return found, total
            if total > budget:
                return None, total
    return None, total


# ------------------------------------------------------------------ laws
def _power(c, n):
    return c ** n if c > 0 else (-1) ** int(round(n)) * abs(c) ** n


class SequenceLaw:
    kind = "sequence"
    form = "sequence"

    def __init__(self, etype, target, order_by, group_by, template, scope, constant=None,
                 properties=None, spread=0.0, provenance=None):
        self.etype, self.target = etype, target
        self.order_by, self.group_by = order_by, group_by
        self.template = {"y_ops": list(template["y_ops"]), "x_op": template.get("x_op")}
        self.scope = scope
        self.constant = constant
        self.properties = dict(properties or {})
        self.spread = spread
        self.provenance = provenance or {}

    def formula(self):
        return describe(self.template, self.target, self.order_by)

    def value_for(self, group=None, history=None):
        """The law's constant for this object: its own, from its readings so far if it's
        new, else the one for everything."""
        if self.scope == "global":
            return self.constant
        if group in self.properties:
            return self.properties[group]
        if history:
            xs, ys = history
            zs = transform(self.template, xs, ys)
            if zs:
                return statistics.median(zs)
        return None

    def predict(self, history, x_new, group=None):
        """history: (xs, ys) of this object's readings so far, ordered. The moment asked
        about may be later, earlier, or between readings: repeating a step a fraction of a
        time, or a below-zero number of times, means what it meant for powers."""
        xs, ys = history
        if x_new in xs:
            return ys[xs.index(x_new)]
        if not xs:
            return None
        if self.template.get("x_op"):
            c = self.value_for(group, history)
            # Δy/Δx = c: from the last reading, one straight step
            return None if c is None else ys[-1] + c * (x_new - xs[-1])
        if len(xs) < 2 or not _even(xs):
            return None
        step = xs[1] - xs[0]
        n = (x_new - xs[-1]) / step
        ops = self.template["y_ops"]
        c = self.value_for(group, history)
        if ops == ["Δ", "ρ"]:
            rest = self.common_rest() if len(ys) < 3 else None
            if c is None and rest is not None:
                # every one I've met settles at the same place: two readings are enough
                if ys[-2] == rest:
                    return None
                c = (ys[-1] - rest) / (ys[-2] - rest)
            if c is None:
                return None
            if abs(c - 1) < 1e-12:
                return ys[-1] + (ys[-1] - ys[-2]) * n
            if rest is None:
                rest = ys[-1] + (ys[-1] - ys[-2]) * c / (1 - c)
            if c <= 0 and abs(n - round(n)) > 1e-9:
                return None
            return rest + (ys[-1] - rest) * _power(c, n)
        if c is None:
            return None
        if ops == ["Δ"]:
            return ys[-1] + c * n
        if ops == ["ρ"]:
            return None if c <= 0 and abs(n - round(n)) > 1e-9 else ys[-1] * _power(c, n)
        if ops == ["Δ", "Δ"] and len(ys) >= 2:
            d = ys[-1] - ys[-2]
            return ys[-1] + d * n + c * n * (n + 1) / 2
        if n < 0 or abs(n - round(n)) > 1e-9 or n > 10_000:
            return None
        k = len(ops)
        if len(ys) < k + 1:
            return None
        if n < 0 or abs(n - round(n)) > 1e-9 or n > 10_000:
            return None
        levels = [list(ys)]
        for op in self.template["y_ops"]:
            nxt = _apply(op, levels[-1])
            if nxt is None:
                return None
            levels.append(nxt)
        for _ in range(int(round(n))):
            levels[-1].append(c)
            for i in range(len(levels) - 1, 0, -1):
                op = self.template["y_ops"][i - 1]
                prev = levels[i - 1][-1]
                levels[i - 1].append(prev + levels[i][-1] if op == "Δ" else prev * levels[i][-1])
        return levels[0][-1]

    def common_rest(self):
        """If every object I've met settles at the same value, that value."""
        return self.provenance.get("common_rest")

    def resting_value(self, history, group=None):
        """For a settling law (ρ of the steps below 1 in size): where it ends up."""
        if self.template["y_ops"] != ["Δ", "ρ"] or self.template.get("x_op"):
            return None
        xs, ys = history
        r = self.value_for(group, history)
        if r is None or not abs(r) < 1 or len(ys) < 2:
            return None
        return ys[-1] + (ys[-1] - ys[-2]) * r / (1 - r)

    def to_json(self):
        return {"form": "sequence", "etype": self.etype, "target": self.target,
                "order_by": self.order_by, "group_by": self.group_by,
                "template": self.template, "scope": self.scope, "constant": self.constant,
                "properties": self.properties, "spread": self.spread,
                "provenance": self.provenance}

    @classmethod
    def from_json(cls, d):
        return cls(d["etype"], d["target"], d["order_by"], d["group_by"], d["template"],
                   d["scope"], d.get("constant"), d.get("properties"), d.get("spread", 0.0),
                   d.get("provenance"))


# ------------------------------------------------------------------ the library
def learned(brain):
    """Kinds Ultron invented, oldest first."""
    return [k for _, k in sorted(brain.kinds.items(), key=lambda kv: kv[1]["order"])]


def explain(brain, spec, episodes):
    """Try the kinds it has learned first (cheap), then invent from the grammar.
    Returns (SequenceLaw or None, {"reuse": steps, "invent": steps}, invented kind or None)."""
    seqs = sequences(episodes, spec.target, spec.order_by, spec.group_by)
    tol = max(spec.tol, 1e-9) + 4 * spec.precision
    steps = {"reuse": 0, "invent": 0}
    mine = learned(brain)
    found, s = search(seqs, tol, [k["template"] for k in mine])
    steps["reuse"] = s
    kind = None
    if found is not None:
        kind = next(k for k in mine if k["template"] == found.template)
    elif brain.inventing:
        known = [k["template"] for k in mine]
        found, s = search(seqs, tol, [t for t in grammar() if t not in known])
        steps["invent"] = s
    if found is None:
        return None, steps, None
    law = SequenceLaw(spec.name, spec.target, spec.order_by, spec.group_by, found.template,
                      found.scope, found.constant, found.properties, found.spread,
                      {"lesson": brain.lesson, "support": 0,
                       "groups": sum(1 for xs, ys in seqs.values() if len(ys) >= 3)})
    note_common_rest(law, seqs, tol)
    if kind is None:
        kind = _record(brain, spec, found, len(seqs))
    elif spec.name not in kind["uses"]:
        kind["uses"].append(spec.name)
        brain.note("reuse", f"{spec.name}: nothing I was born with explains it, but a kind of "
                            f"explanation I invented does: {kind['words']} "
                            f"({describe(found.template, spec.target, spec.order_by)} stays "
                            f"the same {'for everything' if found.scope == 'global' else 'for each ' + str(spec.group_by)}); "
                            f"{steps['reuse']} steps of checking")
    return law, steps, kind


def note_common_rest(law, seqs, tol):
    """A law about the law: do all the objects settle at the same value?"""
    if law.template != {"y_ops": ["Δ", "ρ"], "x_op": None}:
        return
    rests, scale = [], 0.0
    for g, (xs, ys) in seqs.items():
        r = law.resting_value((xs, ys), g) if len(ys) >= 3 else None
        if r is not None:
            rests.append(r)
            scale = max(scale, max(abs(y) for y in ys))
    if len(rests) >= MIN_GROUPS:
        m = statistics.median(rests)
        if max(abs(r - m) for r in rests) <= 2 * tol * scale:
            law.provenance["common_rest"] = round(m, 9) if abs(m) > tol * scale else 0.0
        else:
            law.provenance.pop("common_rest", None)


def _record(brain, spec, found, n_groups):
    name = f"kind {len(brain.kinds) + 1}"
    text = words(found.template)
    where = "for everything" if found.scope == "global" else f"for each {spec.group_by}"
    story = (f"None of the kinds of explanation I was born with fits '{spec.name}': no "
             f"product and no sum of the readings stays the same. So I searched a new "
             f"space: things I can compute along a sequence of readings, shortest first. "
             f"{describe(found.template, spec.target, spec.order_by)} stays the same {where} "
             f"({n_groups} {spec.group_by or 'sequence'}s). That is a new KIND of "
             f"explanation, not just a new law: {text}. I'll keep it and try it first "
             f"next time.")
    kind = {"name": name, "template": found.template, "words": text, "story": story,
            "found_in": spec.name, "lesson": brain.lesson, "uses": [spec.name],
            "order": len(brain.kinds)}
    brain.kinds[name] = kind
    brain.inventions[f"kind:{spec.name}"] = {"shape": "new kind of explanation",
                                             "kind": name, "primitives": [],
                                             "lesson": brain.lesson, "story": story}
    brain.note("invent", story)
    return kind
