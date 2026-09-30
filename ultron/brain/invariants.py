"""The hypothesis engine for measured quantities (physics and real data).

Ultron looks for the simplest combination of measured quantities that stays
the same in every experiment (the approach of Langley's BACON program):

    product of  quantity_i ** power_i   =  constant

Candidates are tried in order of complexity (sum of |powers|). A combination
that is constant across everything is a *law*. One that is constant for each
object but different between objects means that each object carries its own
hidden property (e.g. a spring's stiffness): the brain invents that property.
Choosing between the two uses minimum description length: a per-object law
must pay for one extra constant per object.

Conservation laws (collisions) use the same idea: a per-object quantity whose
total before equals its total after.

Hidden quantities: when no single product stays constant, Ultron also tries
*sums*: A + λ·B, where A and B are simple products and it fits λ itself. If that
stays constant along each run (but differs between runs), it has found a hidden
quantity that flows between A and B while its total never changes.
"""

import itertools
import math

MAX_POWER = 4


class QuantityLaw:
    """product(var ** power) == constant (global) or == property(group)."""

    def __init__(self, etype, powers, kind, constant=None, group_by=None, properties=None,
                 spread=0.0, provenance=None):
        self.etype = etype
        self.powers = dict(powers)          # var -> nonzero int power
        self.kind = kind                    # "global" | "grouped"
        self.constant = constant
        self.group_by = group_by
        self.properties = dict(properties or {})
        self.spread = spread
        self.provenance = provenance or {}

    @property
    def complexity(self):
        return sum(abs(p) for p in self.powers.values())

    def value_for(self, group=None):
        if self.kind == "global":
            return self.constant
        return self.properties.get(group)

    def solve(self, target, known, group=None):
        """Solve the law for one unknown quantity. Returns None if it can't."""
        p = self.powers.get(target)
        c = self.value_for(group)
        if not p or c is None:
            return None
        rest = 1.0
        for var, power in self.powers.items():
            if var == target:
                continue
            if var not in known or known[var] == 0:
                return None
            rest *= known[var] ** power
        x = c / rest
        if x < 0 and p % 2 == 0:
            return None
        return math.copysign(abs(x) ** (1.0 / p), x)

    def formula(self):
        return monomial_str(self.powers)

    def variables(self):
        return list(self.powers)

    def to_json(self):
        return {"form": "product", "etype": self.etype, "powers": self.powers, "kind": self.kind,
                "constant": self.constant, "group_by": self.group_by,
                "properties": self.properties, "spread": self.spread,
                "provenance": self.provenance}

    @classmethod
    def from_json(cls, d):
        return cls(d["etype"], d["powers"], d["kind"], d.get("constant"), d.get("group_by"),
                   d.get("properties"), d.get("spread", 0.0), d.get("provenance"))


class SumLaw:
    """A + coef·B == property(group): a hidden quantity conserved along each group
    (e.g. each run of a ball), shared between two measurable forms."""

    kind = "grouped"

    def __init__(self, etype, a, b, coef, group_by, properties, spread=0.0, provenance=None):
        self.etype = etype
        self.a = dict(a)
        self.b = dict(b)
        self.coef = coef
        self.group_by = group_by
        self.properties = dict(properties)
        self.spread = spread
        self.provenance = provenance or {}

    @property
    def powers(self):
        """Every quantity the law involves (for chaining)."""
        out = dict(self.a)
        out.update(self.b)
        return out

    def variables(self):
        return sorted(set(self.a) | set(self.b))

    def value_for(self, group=None):
        return self.properties.get(group)

    def total(self, values):
        return _mono(values, self.a) + self.coef * _mono(values, self.b)

    def solve(self, target, known, group=None):
        e = self.value_for(group)
        if e is None:
            return None
        for mono, other, scale in ((self.a, self.b, 1.0), (self.b, self.a, self.coef)):
            if target in mono and target not in other:
                try:
                    rest = _mono(known, {k: v for k, v in mono.items() if k != target})
                    other_part = _mono(known, other) * (self.coef if scale == 1.0 else 1.0)
                except (KeyError, ZeroDivisionError):
                    return None
                x = (e - other_part) / (scale * rest)
                p = mono[target]
                if x < 0 and p % 2 == 0:
                    return None     # e.g. a speed that would need a negative square
                return math.copysign(abs(x) ** (1.0 / p), x)
        return None

    def formula(self):
        return f"{monomial_str(self.a)} + {self.coef:.6g}·{monomial_str(self.b)}"

    def to_json(self):
        return {"form": "sum", "etype": self.etype, "a": self.a, "b": self.b,
                "coef": self.coef, "group_by": self.group_by, "properties": self.properties,
                "spread": self.spread, "provenance": self.provenance}

    @classmethod
    def from_json(cls, d):
        return cls(d["etype"], d["a"], d["b"], d["coef"], d["group_by"], d["properties"],
                   d.get("spread", 0.0), d.get("provenance"))


def law_from_json(d):
    return SumLaw.from_json(d) if d.get("form") == "sum" else QuantityLaw.from_json(d)


def _mono(values, powers):
    v = 1.0
    for var, p in powers.items():
        v *= values[var] ** p
    return v


def monomials(names, max_complexity=2):
    """Simple products (one quantity allowed), simplest first; powers are positive."""
    out = []
    for c in range(1, max_complexity + 1):
        for combo in itertools.product(range(0, MAX_POWER + 1), repeat=len(names)):
            if sum(combo) == c:
                out.append({n: p for n, p in zip(names, combo) if p})
    return out


def search_sum_invariant(etype, episodes, names, tol, group_by, max_complexity=2):
    """Find A + λ·B constant within each group (not across groups), smallest first."""
    names = sorted(names)
    monos = monomials(names, max_complexity)
    groups = {}
    for ep in episodes:
        groups.setdefault(ep[group_by], []).append(ep)
    multi = [g for g in groups.values() if len(g) >= 2]
    steps = 0
    if len(multi) < 2:
        return InvariantResult(None, steps)
    best = None
    for i, a in enumerate(monos):
        for b in monos[i + 1:]:
            steps += 1
            if set(a) & set(b):
                continue
            lambdas = []
            for g in multi:
                av = [_mono(e, a) for e in g]
                bv = [_mono(e, b) for e in g]
                for k in range(1, len(g)):
                    db = bv[k] - bv[0]
                    if abs(db) > 1e-12:
                        lambdas.append(-(av[k] - av[0]) / db)
            if len(lambdas) < 2:
                continue
            lam = sum(lambdas) / len(lambdas)
            if lam == 0 or _spread(lambdas) > tol * 10:
                continue
            props, worst = {}, 0.0
            for key, g in groups.items():
                vals = [_mono(e, a) + lam * _mono(e, b) for e in g]
                props[key] = sum(vals) / len(vals)
                if len(vals) >= 2:
                    worst = max(worst, (max(vals) - min(vals)) / (abs(props[key]) or 1.0))
            if worst > tol:
                continue
            distinct = len({round(v, 9) for v in props.values()}) > 1
            if not distinct:
                continue    # the same everywhere: a plain law, not a hidden quantity
            score = sum(a.values()) + sum(b.values()) + 1 + len(groups)
            if best is None or score < best[0]:
                best = (score, SumLaw(etype, a, b, lam, group_by,
                                      dict(sorted(props.items())), worst))
    return InvariantResult(best[1] if best else None, steps)


class ConservationLaw:
    """sum over objects of (m ** p * v ** q) is the same before and after."""

    def __init__(self, etype, powers, scope, provenance=None):
        self.etype = etype
        self.powers = dict(powers)      # {"m": p, "v": q}
        self.scope = scope              # "all" or a list of kinds it holds for
        self.provenance = provenance or {}

    def formula(self):
        return monomial_str(self.powers)

    def to_json(self):
        return {"etype": self.etype, "powers": self.powers, "scope": self.scope,
                "provenance": self.provenance}

    @classmethod
    def from_json(cls, d):
        return cls(d["etype"], d["powers"], d["scope"], d.get("provenance"))


def monomial_str(powers):
    num, den = [], []
    for var in sorted(powers):
        p = powers[var]
        term = var if abs(p) == 1 else f"{var}^{abs(p)}"
        (num if p > 0 else den).append(term)
    top = "·".join(num) or "1"
    return top if not den else f"{top} / ({'·'.join(den)})" if len(den) > 1 else f"{top} / {den[0]}"


def power_vectors(n, complexity):
    """All power vectors over n quantities with sum |p| == complexity, touching
    at least two quantities, first nonzero power positive (p and -p are the
    same law). Deterministic order."""
    out = []
    for combo in itertools.product(range(-MAX_POWER, MAX_POWER + 1), repeat=n):
        if sum(abs(c) for c in combo) != complexity:
            continue
        nonzero = [c for c in combo if c]
        if len(nonzero) < 2 or nonzero[0] < 0:
            continue
        out.append(combo)
    return out


def _spread(values):
    mean = sum(values) / len(values)
    if mean == 0:
        return math.inf
    return (max(values) - min(values)) / abs(mean)


def _values(episodes, names, combo):
    vals = []
    for ep in episodes:
        v = 1.0
        for name, p in zip(names, combo):
            if p:
                x = ep[name]
                if x == 0:
                    return None
                v *= x ** p
        vals.append(v)
    return vals


class InvariantResult:
    def __init__(self, law, steps):
        self.law = law
        self.steps = steps


def search_invariant(etype, episodes, names, tol, group_by=None, max_complexity=6,
                     prior_powers=(), min_group_members=2, precision=0.0):
    """Find the law with the smallest description length.

    prior_powers: power dicts of laws already known. They are tried first (this
    is how earlier learning speeds up later learning), but an accepted prior
    still has to beat every simpler candidate on description length.
    """
    names = sorted(names)
    steps = 0
    best = None  # (score, complexity, law)

    def allowed(c):
        # error propagation: each reading is off by up to ±precision, and a
        # product of powers multiplies that by sum |power|; the spread
        # (max - min) can be twice that
        return tol + 2 * c * precision

    def evaluate(combo, ordering, needed_groups):
        nonlocal steps, best
        steps += 1
        vals = _values(episodes, names, combo)
        if vals is None or len(vals) < 2:
            return
        powers = {n: p for n, p in zip(names, combo) if p}
        c = sum(abs(p) for p in combo)
        spread = _spread(vals)
        if spread <= allowed(c):
            score = c + 1
            if best is None or (score, ordering) < best[0]:
                law = QuantityLaw(etype, powers, "global", constant=sum(vals) / len(vals),
                                  spread=spread)
                best = ((score, ordering), c, law)
            return
        if group_by is None:
            return
        groups = {}
        for ep, v in zip(episodes, vals):
            groups.setdefault(ep[group_by], []).append(v)
        multi = [g for g in groups.values() if len(g) >= 2]
        if len(multi) < needed_groups:
            return
        worst = max(_spread(g) for g in multi)
        if worst <= allowed(c):
            score = c + len(groups)
            if best is None or (score, ordering) < best[0]:
                props = {k: sum(g) / len(g) for k, g in sorted(groups.items())}
                law = QuantityLaw(etype, powers, "grouped", group_by=group_by,
                                  properties=props, spread=worst)
                best = ((score, ordering), c, law)

    tried = set()
    for pp in prior_powers:
        if set(pp) <= set(names) and len(pp) >= 2:
            combo = tuple(pp.get(n, 0) for n in names)
            if combo not in tried:
                tried.add(combo)
                # a form that already worked elsewhere gets the benefit of the doubt:
                # one well-observed group is enough to carry it to a new one
                evaluate(combo, 0, 1)
    for c in range(2, max_complexity + 1):
        if best is not None and best[0][0] <= c + 1:
            break   # nothing this complex can have a shorter description
        for combo in power_vectors(len(names), c):
            if combo in tried:
                continue
            tried.add(combo)
            evaluate(combo, 1, min_group_members)
    return InvariantResult(best[2] if best else None, steps)


def search_conservation(etype, episodes, max_complexity=4, tol=1e-6):
    """episodes: dicts with 'before': [(m, v), ...], 'after': [(m, v), ...], 'kind'.
    Returns every conserved quantity m^p·v^q (q >= 1) up to max_complexity,
    each with the kinds of event it holds for."""
    kinds = sorted({ep["kind"] for ep in episodes})
    found = []
    steps = 0
    for c in range(1, max_complexity + 1):
        for q in range(1, c + 1):
            p = c - q
            steps += 1
            holds = {}
            for ep in episodes:
                before = sum(m ** p * v ** q for m, v in ep["before"])
                after = sum(m ** p * v ** q for m, v in ep["after"])
                scale = sum(abs(m ** p * v ** q) for m, v in ep["before"] + ep["after"]) or 1.0
                ok = abs(before - after) <= tol * scale
                holds[ep["kind"]] = holds.get(ep["kind"], True) and ok
            good = [k for k in kinds if holds.get(k)]
            if good:
                scope = "all" if good == kinds else good
                powers = {"m": p, "v": q} if p else {"v": q}
                found.append(ConservationLaw(etype, powers, scope))
    return found, steps
