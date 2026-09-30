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
*sums*: A + λ·B (+ μ·C ...), where the terms are simple products and it fits the
coefficients itself. If that
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
        zero = False
        for var, power in self.powers.items():
            if var == target:
                continue
            if var not in known:
                return None
            if known[var] == 0:
                # target = c^(1/p) · Π known^(-power/p): a zero makes the target zero
                # when its exponent there is positive, and no number when negative
                if -power / p < 0:
                    return None
                zero = True
                continue
            rest *= known[var] ** power
        if zero:
            return 0.0
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
    """term_1 + c_2·term_2 + ... == property(group): a hidden quantity conserved along
    each group (e.g. each run of a ball), shared between several measurable forms."""

    kind = "grouped"

    def __init__(self, etype, terms, group_by, properties, spread=0.0, provenance=None):
        self.etype = etype
        self.terms = [(dict(p), float(c)) for p, c in terms]   # first coefficient is 1
        self.group_by = group_by
        self.properties = dict(properties)
        self.spread = spread
        self.provenance = provenance or {}

    # the two-term view (kept for readers of simple laws)
    @property
    def a(self):
        return self.terms[0][0]

    @property
    def b(self):
        return self.terms[1][0]

    @property
    def coef(self):
        return self.terms[1][1]

    @property
    def powers(self):
        """Every quantity the law involves (for chaining)."""
        out = {}
        for p, _ in self.terms:
            out.update(p)
        return out

    def variables(self):
        return sorted(self.powers)

    def value_for(self, group=None):
        return self.properties.get(group)

    def total(self, values):
        return sum(c * _mono(values, p) for p, c in self.terms)

    def solve(self, target, known, group=None):
        e = self.value_for(group)
        if e is None:
            return None
        holders = [(p, c) for p, c in self.terms if target in p]
        if len(holders) != 1:
            return None
        mono, scale = holders[0]
        try:
            others = sum(c * _mono(known, p) for p, c in self.terms if target not in p)
            rest = _mono(known, {k: v for k, v in mono.items() if k != target})
        except (KeyError, ZeroDivisionError):
            return None
        x = (e - others) / (scale * rest)
        pw = mono[target]
        if x < 0 and pw % 2 == 0:
            return None     # e.g. a speed that would need a negative square
        return math.copysign(abs(x) ** (1.0 / pw), x)

    def formula(self):
        parts = [monomial_str(self.terms[0][0])]
        parts += [f"{c:.6g}·{monomial_str(p)}" for p, c in self.terms[1:]]
        return " + ".join(parts)

    def to_json(self):
        return {"form": "sum", "etype": self.etype,
                "terms": [[p, c] for p, c in self.terms], "group_by": self.group_by,
                "properties": self.properties, "spread": self.spread,
                "provenance": self.provenance}

    @classmethod
    def from_json(cls, d):
        terms = d.get("terms") or [[d["a"], 1.0], [d["b"], d["coef"]]]
        return cls(d["etype"], [(p, c) for p, c in terms], d["group_by"], d["properties"],
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


def _fit(groups, monos):
    """Least-squares coefficients c_2..c_k making term_1 + Σ c_i·term_i the same within
    every group. Returns (coefficients, worst relative spread, properties) or None."""
    rows, rhs = [], []
    for g in groups.values():
        if len(g) < 2:
            continue
        base = g[0]
        for e in g[1:]:
            rows.append([_mono(e, m) - _mono(base, m) for m in monos[1:]])
            rhs.append(-(_mono(e, monos[0]) - _mono(base, monos[0])))
    k = len(monos) - 1
    if len(rows) < k + 1:
        return None
    # normal equations (k is 1 or 2, so this is tiny)
    ata = [[sum(r[i] * r[j] for r in rows) for j in range(k)] for i in range(k)]
    atb = [sum(r[i] * y for r, y in zip(rows, rhs)) for i in range(k)]
    try:
        if k == 1:
            coefs = [atb[0] / ata[0][0]]
        else:
            det = ata[0][0] * ata[1][1] - ata[0][1] * ata[1][0]
            if abs(det) < 1e-12 * (abs(ata[0][0] * ata[1][1]) + 1e-300):
                return None
            coefs = [(atb[0] * ata[1][1] - atb[1] * ata[0][1]) / det,
                     (ata[0][0] * atb[1] - ata[1][0] * atb[0]) / det]
    except ZeroDivisionError:
        return None
    if any(abs(c) < 1e-12 for c in coefs):
        return None
    terms = [(monos[0], 1.0)] + list(zip(monos[1:], coefs))
    props, worst = {}, 0.0
    for key, g in groups.items():
        vals = [sum(c * _mono(e, m) for m, c in terms) for e in g]
        props[key] = sum(vals) / len(vals)
        if len(vals) >= 2:
            worst = max(worst, (max(vals) - min(vals)) / (abs(props[key]) or 1.0))
    return terms, worst, props


def search_sum_invariant(etype, episodes, names, tol, group_by, max_complexity=2, max_terms=3):
    """Find the simplest sum of terms that stays constant within each group (and differs
    between groups): two terms first, then three. Coefficients are fitted, not given."""
    names = sorted(names)
    monos = monomials(names, max_complexity)
    groups = {}
    for ep in episodes:
        groups.setdefault(ep[group_by], []).append(ep)
    steps = 0
    if sum(1 for g in groups.values() if len(g) >= 2) < 2:
        return InvariantResult(None, steps)
    best = None
    for n_terms in range(2, max_terms + 1):
        for combo in itertools.combinations(monos, n_terms):
            steps += 1
            if any(set(x) & set(y) for x, y in itertools.combinations(combo, 2)):
                continue    # a quantity may appear in only one term
            fit = _fit(groups, list(combo))
            if fit is None:
                continue
            terms, worst, props = fit
            if worst > tol:
                continue
            if len({round(v, 9) for v in props.values()}) < 2:
                continue    # the same everywhere: a plain law, not a hidden quantity
            score = sum(sum(p.values()) for p, _ in terms) + n_terms - 1 + len(groups)
            if best is None or score < best[0]:
                best = (score, SumLaw(etype, terms, group_by, dict(sorted(props.items())), worst))
        if best is not None:
            break           # fewer terms always wins when they explain everything
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
