"""Laws about its own laws.

When Ultron finds that each object carries its own hidden property (each spring its
stiffness, each run its energy), it treats that property as an *arbitrary* fact about
the object. Reflecting, it asks the next question a scientist asks: why this value?

It turns its own invented properties into data. For every object it has both a
property for and some other observation of (e.g. the number of coils it counted by
looking at the spring), it builds a table and runs its usual hypothesis engine on it,
one level up. A law found there (stiffness × coils is the same for every spring) is
a law about a law: it lets Ultron know a new object's property without measuring it
the usual way, and so predict experiments it has never done.

This doesn't let Ultron invent arbitrary new kinds of hypothesis. It composes the
kinds it has at a new level, which is how a lot of science actually proceeds.
"""

from . import units as U
from .invariants import QuantityLaw, search_invariant

SUFFIX = ".property"


def property_var(law_name):
    return f"{law_name}{SUFFIX}"


def _features(brain, group_by):
    """Per-object observations from 'feature' experiences: {object: {feature: value}}."""
    out = {}
    for name, spec in brain.memory.specs.items():
        if spec.kind != "feature" or spec.group_by != group_by:
            continue
        for ep in brain.memory.of(name):
            obj = ep["inputs"][group_by]
            out.setdefault(obj, {})[spec.target] = ep["outcome"]
    return out


def look_for_property_laws(brain):
    """Record and return a new law about one of its own grouped laws, if one is found."""
    from .invariants import SumLaw
    for name, law in sorted(brain.qlaws.items()):
        if law.kind != "grouped" or isinstance(law, SumLaw) or not brain.trusts_quantity(name):
            continue
        meta_name = f"{name}~why"
        if meta_name in brain.qlaws:
            continue
        feats = _features(brain, law.group_by)
        rows = []
        for obj, value in sorted(law.properties.items()):
            if obj in feats:
                row = {property_var(name): value}
                row.update(feats[obj])
                rows.append(row)
        if len(rows) < 4:
            continue
        names = sorted(rows[0])
        spec = brain.memory.specs[name]
        result = search_invariant(meta_name, rows, names, max(spec.tol, 1e-6) * 10,
                                  precision=spec.precision)
        meta = result.law
        if meta is None or meta.kind != "global" or property_var(name) not in meta.powers:
            continue
        meta.provenance = {"lesson": brain.lesson, "objects": len(rows), "support": len(rows)}
        brain.qlaws[meta_name] = meta
        feature = ", ".join(v for v in names if v != property_var(name))
        dims = U.of_monomial(law.powers, spec.units)
        story = (f"Each {law.group_by}'s {law.formula()} (a property I invented, in "
                 f"{U.name(dims)}) isn't arbitrary: {meta.formula().replace(property_var(name), 'it')} "
                 f"is the same, {meta.constant:.6g}, for all {len(rows)} {law.group_by}s whose "
                 f"{feature} I have counted. That's a law about my law. Now I can know a new "
                 f"{law.group_by}'s property just by counting its {feature}, and predict "
                 f"what it will do before I ever try it.")
        brain.inventions[f"why:{name}"] = {"shape": "law about a law", "law": meta_name,
                                            "primitives": [], "lesson": brain.lesson,
                                            "story": story}
        brain.note("invent", story)
        return meta
    return None


def predicted_property(brain, law_name, obj):
    """A property for an object never measured the usual way, from a law about the law."""
    meta = brain.qlaws.get(f"{law_name}~why")
    if meta is None:
        return None
    law = brain.qlaws[law_name]
    feats = _features(brain, law.group_by).get(obj)
    if not feats:
        return None
    return meta.solve(property_var(law_name), feats)
