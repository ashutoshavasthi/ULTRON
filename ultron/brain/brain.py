"""Ultron's brain: predict -> act -> observe -> compare -> revise -> store.

Everything Ultron knows lives in this object and can be saved to one JSON
file. Nothing in here contains a law or a formula; the laws are found by the
hypothesis engines from Ultron's own experiences.
"""

import json

from . import units as U
from .curiosity import Curiosity
from .dsl import BOOL, Law, Library, safe_evaluate, show, size
from .invariants import (ConservationLaw, QuantityLaw, SumLaw, law_from_json,
                         search_conservation, search_invariant, search_sum_invariant)
from .invariants import monomial_str
from .memory import Memory, Spec
from .synth import synthesize

CONFIRM_STREAK = 8   # correct predictions in a row before a law is trusted
ESTABLISHED = 3      # confirmations before a measured law stops being tentative
N_RIVALS = 3         # alternative explanations kept to design experiments against


class Brain:
    def __init__(self, name="Ultron"):
        self.name = name
        self.memory = Memory()
        self.library = Library()            # confirmed discrete laws (building blocks)
        self.hypotheses = {}                # spec -> current discrete law (maybe unconfirmed)
        self.streak = {}                    # spec -> correct predictions in a row
        self.failed_search = {}             # spec -> episodes seen at last failed search
        self.qlaws = {}                     # spec -> QuantityLaw
        self.claws = {}                     # spec -> [ConservationLaw]
        self.vocab = {}                     # token -> meaning
        self.names = {}                     # concept id -> word the Trainer taught
        self.curiosity = Curiosity()
        self.log = []
        self.search_steps = {}              # spec -> steps spent searching (effort)
        self.rivals = {}                    # spec -> other programs explaining the same data
        self.inventions = {}                # concepts Ultron made up itself
        self.active = True                  # design experiments when ideas disagree
        self.found_at = {}                  # spec -> experiences when current idea was found
        self.compress = True                # look for patterns among its own laws
        self.quantities = {}                # lengths etc. Ultron holds an idea about
        self.candidates = {}                # spec -> predictions kept in mind, not assumed
        self.lesson = None

    # ------------------------------------------------------------------ utils
    def note(self, kind, text, **extra):
        self.log.append({"lesson": self.lesson, "kind": kind, "text": text, **extra})

    def meet(self, spec):
        """First contact with a new kind of experiment."""
        if spec.name not in self.memory.specs:
            self.memory.know(spec)
            self.note("meet", f"new kind of experience: {spec.name}")
            from .compression import seed_predictions
            seed_predictions(self, spec)

    def constants(self):
        """0 and 1 are innate; numbers that have been given names become usable too."""
        named = {m[1] for m in self.vocab.values() if m[0] == "number"}
        return tuple(sorted({0, 1} | {n for n in named if n <= 10}))

    def primitives(self):
        """Invented primitives now available to the hypothesis engine."""
        return tuple(sorted({p for inv in self.inventions.values() for p in inv["primitives"]}))

    def status(self, spec_name):
        """How much Ultron trusts its law for this kind of experience."""
        spec = self.memory.specs.get(spec_name)
        if spec is None:
            return "unknown"
        if spec.kind == "program":
            return "established" if spec_name in self.library else "tentative"
        if spec.kind == "quantity":
            law = self.qlaws.get(spec_name)
            return ("established" if law and law.provenance.get("support", 0) >= ESTABLISHED
                    else "tentative")
        laws = self.claws.get(spec_name, [])
        return ("established" if laws and min(l.provenance.get("support", 0) for l in laws)
                >= ESTABLISHED else "tentative")

    @staticmethod
    def kind_of(inputs):
        """The qualitative shape of a situation: which amounts are zero, and how
        each pair of amounts compares. '3 and 5' and '4 and 9' are the same kind."""
        names = sorted(k for k, v in inputs.items()
                       if isinstance(v, int) and not isinstance(v, bool))
        zeros = tuple(inputs[n] == 0 for n in names)
        order = tuple((inputs[a] > inputs[b]) - (inputs[a] < inputs[b])
                      for i, a in enumerate(names) for b in names[i + 1:])
        flags = tuple(sorted((k, v) for k, v in inputs.items() if isinstance(v, bool)))
        return (zeros, order, flags)

    def unsure(self, options):
        """Kinds of experience where I hold an idea I haven't confirmed yet."""
        for name in options:
            spec = self.memory.specs.get(name)
            if spec is None or spec.kind != "program" or self.hypotheses.get(name) is None:
                continue
            law = self.library.get(name)
            if law is None or law.provenance.get("doubted"):
                return name
        return None

    def trusts(self, name):
        law = self.library.get(name)
        return law is not None and not law.provenance.get("doubted")

    def propose(self, spec_name, options):
        """Design an experiment. First, the situation where my current explanation
        and its rivals disagree most, so the world decides between them. If they all
        agree everywhere I could look, a kind of situation I have never tried: my
        ideas might all be wrong in the same way there."""
        if not self.active or not options:
            return None
        expr = self.hypotheses.get(spec_name)
        ideas = ([expr] if expr is not None else []) + self.rivals.get(spec_name, [])
        best, best_key = None, (1, 0)
        if len(ideas) > 1:
            for inputs in options:
                outs = {repr(safe_evaluate(e, inputs, self.library)) for e in ideas}
                # split my ideas as much as possible; among equally good splits prefer
                # rich situations (bigger numbers): tiny ones like "0 groups of 1" fit
                # almost any rule, so they teach the least
                richness = sum(abs(v) for v in inputs.values()
                               if isinstance(v, int) and not isinstance(v, bool))
                key = (len(outs), richness)
                if len(outs) > 1 and key > best_key:
                    best, best_key = inputs, key
        if best is not None:
            self.note("design", f"{spec_name}: my {len(ideas)} explanations disagree about "
                                f"{best}; I'll set that up to find out")
            return best
        seen = {self.kind_of(e["inputs"]) for e in self.memory.of(spec_name)}
        for inputs in options:
            if self.kind_of(inputs) not in seen:
                self.note("design", f"{spec_name}: my ideas agree, but I've never tried a "
                                    f"situation like {inputs}; I'll set that up")
                return inputs
        return None

    def known_forms(self):
        return [law.powers for law in self.qlaws.values() if not isinstance(law, SumLaw)]

    # ------------------------------------------------------------- predicting
    def predict(self, spec_name, inputs):
        spec = self.memory.specs.get(spec_name)
        if spec is None:
            return None     # never met this kind of experience
        if spec.kind == "program":
            expr = self.hypotheses.get(spec_name)
            return None if expr is None else safe_evaluate(expr, inputs, self.library)
        if spec.kind == "quantity":
            law = self.qlaws.get(spec_name)
            group = inputs.get(spec.group_by) if spec.group_by else None
            if law is None or not self.law_applies(spec_name, group):
                return None
            return law.solve(spec.target, inputs, group)
        if spec.kind == "conservation":
            return self._predict_collision(spec_name, inputs)
        if spec.kind == "measure":
            return self._predict_reading(spec, inputs)
        raise ValueError(spec.kind)

    def _predict_reading(self, spec, inputs):
        """A ruler with `marks` per unit passes c marks when the length lies between
        c/marks and (c+1)/marks: pin the length at exactly that kind of piece."""
        from . import gaps
        idea = self.quantities.get(spec.target)
        if idea is None:
            return None
        c = gaps.pin(self, gaps.Gap.from_json(idea), inputs["marks"])
        return None if c is None else c[0]

    def _predict_collision(self, spec_name, inp):
        for law in self.claws.get(spec_name, []):
            if law.scope == "all" and law.powers.get("v") == 1:
                p = law.powers.get("m", 0)
                total = inp["m1"] ** p * inp["v1"] + inp["m2"] ** p * inp["v2"]
                return (total - inp["m1"] ** p * inp["v1_after"]) / inp["m2"] ** p
        return None

    def law_applies(self, spec_name, group):
        """A law learned only around the Sun says nothing yet about Saturn: a
        never-seen kind of situation is outside experience, however well the law
        worked elsewhere."""
        spec = self.memory.specs[spec_name]
        if not spec.group_by or group is None:
            return True
        return any(e.get(spec.group_by) == group for e in self.memory.of(spec_name))

    @staticmethod
    def error(predicted, actual):
        if predicted is None:
            return 1.0
        if isinstance(actual, bool) or isinstance(predicted, bool):
            return 0.0 if predicted == actual else 1.0
        if isinstance(actual, int) and isinstance(predicted, int):
            return 0.0 if predicted == actual else 1.0
        scale = abs(actual) if actual else 1.0
        return min(1.0, abs(predicted - actual) / scale)

    # -------------------------------------------------------------- observing
    def experience(self, spec_name, inputs, outcome):
        """Predict first, then look at what really happened and learn from it."""
        spec = self.memory.specs[spec_name]
        predicted = self.predict(spec_name, inputs)
        err = self.error(predicted, outcome)
        # with imprecise instruments, small misses are expected, not surprising
        surprised = err > spec.surprise + 2 * (len(spec.inputs) + 1) * spec.precision
        self.curiosity.record(spec_name, 0.0 if not surprised else err)
        if spec.kind == "program":
            self.memory.store(spec_name, {"inputs": inputs, "outcome": outcome})
            revised = self._learn_program(spec, surprised)
        elif spec.kind == "quantity":
            self.memory.store(spec_name, {**inputs, spec.target: outcome})
            revised = self._learn_quantity(spec, surprised)
        elif spec.kind == "measure":
            self.memory.store(spec_name, {"inputs": inputs, "outcome": outcome})
            revised = None
            if surprised:
                self.note("doubt", f"{spec_name}: my idea of {spec.target} predicted "
                                   f"{predicted}, but the ruler read {outcome}")
        else:
            self.memory.store(spec_name, {"inputs": inputs, "outcome": outcome})
            revised = self._learn_conservation(spec, surprised)
        return {"predicted": predicted, "actual": outcome, "error": err,
                "surprised": surprised, "revised": revised}

    def _learn_program(self, spec, surprised):
        name = spec.name
        if not surprised:
            self.streak[name] = self.streak.get(name, 0) + 1
            last = self.memory.of(name)[-1]
            self.rivals[name] = [r for r in self.rivals.get(name, [])
                                 if safe_evaluate(r, last["inputs"], self.library) == last["outcome"]]
            expr = self.hypotheses.get(name)
            if expr is not None and self.streak[name] == CONFIRM_STREAK:
                self._confirm_program(spec, expr)
            return None
        self.streak[name] = 0
        trusted = self.library.get(name)
        if trusted is not None and not trusted.provenance.get("doubted"):
            trusted.provenance["doubted"] = True
            self.note("doubt", f"{name}: my confirmed law {show(trusted.expr)} just failed; "
                               f"I don't trust it any more until a better one is confirmed")
        eps = self.memory.of(name)
        for cand in self.candidates.get(name, []):
            if not all(safe_evaluate(cand, e["inputs"], self.library) == e["outcome"]
                       for e in eps):
                continue
            old = self.hypotheses.get(name)
            self.hypotheses[name] = cand
            self.found_at[name] = len(eps)
            if len(eps) < ESTABLISHED:
                # one or two experiences can fit almost anything by coincidence: test it,
                # don't trust it
                self.note("revise", f"{name}: a prediction I had in mind, {show(cand)}, fits "
                                    f"my first {len(eps)} experience(s); only a suspicion, so "
                                    f"I'll test it before searching for anything else")
            else:
                self.candidates[name] = [c for c in self.candidates[name] if c != cand]
                self.note("revise", f"{name}: a prediction I had in mind, {show(cand)}, fits "
                                    f"all {len(eps)} experiences (was "
                                    f"{show(old) if old else 'nothing'})")
            return show(cand)
        self.candidates[name] = [c for c in self.candidates.get(name, []) if all(
            safe_evaluate(c, e["inputs"], self.library) == e["outcome"] for e in eps)]
        for rival in self.rivals.get(name, []):
            if all(safe_evaluate(rival, e["inputs"], self.library) == e["outcome"] for e in eps):
                old = self.hypotheses.get(name)
                self.hypotheses[name] = rival
                self.rivals[name] = [r for r in self.rivals[name] if r != rival]
                self.found_at[name] = len(eps)
                self.note("revise", f"{name}: surprised; my other idea {show(rival)} fits "
                                    f"everything (was {show(old) if old else 'nothing'})")
                return show(rival)
        last_fail = self.failed_search.get(name)
        if last_fail is not None and len(eps) < 2 * last_fail:
            return None     # "I couldn't explain this before; wait for more evidence"
        result = synthesize([e["inputs"] for e in eps], [e["outcome"] for e in eps],
                            spec.inputs, spec.out_type, self.library, self.constants(),
                            rivals=N_RIVALS, extra=self.primitives())
        self.search_steps[name] = self.search_steps.get(name, 0) + result.steps
        old = self.hypotheses.get(name)
        if result.expr is None:
            self.failed_search[name] = len(eps)
            self.hypotheses.pop(name, None)
            self.note("stuck", f"{name}: no simple law explains all {len(eps)} experiences "
                               f"(searched {result.steps} programs)")
            return None
        self.failed_search.pop(name, None)
        self.hypotheses[name] = result.expr
        self.rivals[name] = result.rivals
        self.found_at[name] = len(eps)
        self.note("revise", f"{name}: surprised; new best explanation is "
                            f"{show(result.expr)} (was {show(old) if old else 'nothing'}; "
                            f"{len(eps)} experiences, {result.steps} programs searched)")
        return show(result.expr)

    def _confirm_program(self, spec, expr):
        law = Law(spec.name, sorted(spec.inputs), expr, spec.out_type, {
            "lesson": self.lesson, "experiences": len(self.memory.of(spec.name)),
            "found_after": self.found_at.get(spec.name), "size": size(expr)})
        self.library.add(law)
        self.note("confirm", f"{spec.name}: {show(expr)} predicted {CONFIRM_STREAK} new "
                             f"experiences in a row; added to my library of building blocks")
        from .compression import confirm_predictions
        confirm_predictions(self, expr)

    def _learn_quantity(self, spec, surprised):
        name = spec.name
        eps = self.memory.of(name)
        law = self.qlaws.get(name)
        if not surprised:
            if law is not None:
                self._refine(law, eps)
                law.provenance["support"] = law.provenance.get("support", 0) + 1
                if law.provenance["support"] == ESTABLISHED:
                    self.note("establish", f"{name}: {law.formula()} has now predicted "
                                           f"{ESTABLISHED} new experiences; no longer tentative")
            return None
        new_object = (law is not None and law.kind == "grouped"
                      and eps[-1].get(spec.group_by) not in law.properties)
        if (law is not None and not new_object
                and law.provenance.get("support", 0) >= ESTABLISHED):
            self.note("doubt", f"{name}: my established law {law.formula()} just failed; "
                               f"back to being unsure")
        names = list(spec.inputs) + [spec.target]
        result = search_invariant(name, eps, names, spec.tol, group_by=spec.group_by,
                                  prior_powers=self.known_forms(), precision=spec.precision)
        self.search_steps[name] = self.search_steps.get(name, 0) + result.steps
        if result.law is None and spec.group_by:
            # no single product stays constant: is something *shared* between two forms?
            result = search_sum_invariant(name, eps, names, spec.tol + 4 * spec.precision,
                                          spec.group_by)
            self.search_steps[name] += result.steps
        if result.law is None:
            self.note("stuck", f"{name}: nothing stays constant yet ({len(eps)} experiences)")
            return None
        new = result.law
        if isinstance(new, SumLaw):
            return self._adopt_sum_law(spec, law, new, eps)
        if (law is not None and law.kind == new.kind == "grouped"
                and law.powers == new.powers):
            # same law, new object: just measure the newcomer's property
            law.properties = new.properties
            group = eps[-1][spec.group_by]
            self.note("measure", f"{name}: met new {spec.group_by} {group}; measured its "
                                 f"property {law.formula()} = {law.properties[group]:.6g}")
            return None
        new.provenance = {"lesson": self.lesson, "experiences": len(eps), "support": 0}
        self.qlaws[name] = new
        dims = U.of_monomial(new.powers, spec.units)
        what = (f"{new.formula()} = {new.constant:.6g} [{U.name(dims)}] in every experiment"
                if new.kind == "global" else
                f"{new.formula()} is constant for each {spec.group_by} but differs between "
                f"them: a hidden property of each {spec.group_by} [{U.name(dims)}]")
        self.note("revise", f"{name}: {what} ({result.steps} candidates searched; tentative "
                            f"until it predicts {ESTABLISHED} new experiences)")
        return new.formula()

    def _adopt_sum_law(self, spec, old, new, eps):
        name = spec.name
        if isinstance(old, SumLaw) and [p for p, _ in old.terms] == [p for p, _ in new.terms]:
            old.properties, old.terms = new.properties, new.terms
            group = eps[-1][spec.group_by]
            self.note("measure", f"{name}: new {spec.group_by} {group}; its hidden amount is "
                                 f"{old.properties[group]:.6g}")
            return None
        new.provenance = {"lesson": self.lesson, "experiences": len(eps), "support": 0}
        self.qlaws[name] = new
        first = monomial_str(new.terms[0][0])
        forms = [monomial_str(p) for p, _ in new.terms]
        story = (f"Along each {spec.group_by}, none of {', '.join(forms)} stays the same, but "
                 f"{new.formula()} does. Each {spec.group_by} has its own amount of this hidden "
                 f"quantity: whatever {first} is lost turns up as "
                 f"{' and '.join(forms[1:])}, and the total never changes.")
        for p, c in new.terms[1:]:
            dims_t = U.of_monomial(p, spec.units)
            dims_a = U.of_monomial(new.terms[0][0], spec.units)
            if dims_t is None or dims_a is None:
                continue
            inv_dims = tuple(y - x for x, y in zip(dims_a, dims_t))
            like = next(((v, n) for n, sp in sorted(self.memory.specs.items()) if n != name
                         for v, d in sorted(sp.units.items()) if tuple(d) == inv_dims), None)
            if like:
                story += (f" (The coefficient of {monomial_str(p)} is one over {1 / c:.4g} "
                          f"{U.name(inv_dims)}: the same units as '{like[0]}' in my "
                          f"'{like[1]}' experiences.)")
        self.note("revise", f"{name}: {story}")
        key = f"hidden:{name}"
        if key in self.inventions and len(new.terms) > len(
                self.inventions[key].get("terms", [None, None])):
            self.inventions.pop(key)      # a richer hidden quantity replaces a simpler idea
        if key not in self.inventions:
            self.inventions[key] = {"shape": "hidden quantity", "law": name, "primitives": [],
                                    "lesson": self.lesson, "story": story,
                                    "terms": [monomial_str(p) for p, _ in new.terms]}
            self.note("invent", story)
        return new.formula()

    def _refine(self, law, eps):
        """Keep improving the constant's estimate as evidence accumulates."""
        if isinstance(law, SumLaw):
            groups = {}
            for e in eps:
                groups.setdefault(e[law.group_by], []).append(law.total(e))
            law.properties = {k: sum(v) / len(v) for k, v in sorted(groups.items())}
            return
        if law.kind == "global":
            vals = [self._monomial(e, law.powers) for e in eps]
            law.constant = sum(vals) / len(vals)
        else:
            groups = {}
            for e in eps:
                groups.setdefault(e[law.group_by], []).append(self._monomial(e, law.powers))
            law.properties = {k: sum(v) / len(v) for k, v in sorted(groups.items())}

    @staticmethod
    def _monomial(ep, powers):
        v = 1.0
        for var, p in powers.items():
            v *= ep[var] ** p
        return v

    def reflect(self):
        """Look back over everything remembered, even what caused no surprise.
        Prediction only needs one conserved quantity; reflection can find more."""
        for name in sorted(self.memory.specs):
            spec = self.memory.specs[name]
            if spec.kind == "conservation" and self.memory.of(name):
                self._learn_conservation(spec, True, reflecting=True)
        from .invention import find_inverses, look_for_shapes
        from .compression import look_for_ladders
        from .gaps import look_for_gaps
        self._check_symmetry()
        look_for_shapes(self)
        find_inverses(self)
        look_for_ladders(self)
        look_for_gaps(self)

    def _check_symmetry(self):
        """Which of my laws give the same result either way round? (checked, not assumed)"""
        from .dsl import Overflow
        for law in self.library.binary_int_laws():
            if law.name in self.library.symmetric or not self.trusts(law.name):
                continue
            try:
                same = all(self.library.call(law.name, x, y) == self.library.call(law.name, y, x)
                           for x in range(0, 7) for y in range(0, 7))
            except Overflow:
                same = False
            if same:
                self.library.symmetric.add(law.name)
                self.note("reflect", f"'{law.name}' gives the same answer either way round, so "
                                     f"I can count along the smaller number")

    def _learn_conservation(self, spec, surprised, reflecting=False):
        if not surprised and spec.name in self.claws:
            kind = self.memory.of(spec.name)[-1]["inputs"]["kind"]
            for law in self.claws[spec.name]:
                if law.scope == "all" or kind in law.scope:
                    law.provenance["support"] = law.provenance.get("support", 0) + 1
            return None
        eps = self.memory.of(spec.name)
        events = [{"before": [(e["inputs"]["m1"], e["inputs"]["v1"]),
                              (e["inputs"]["m2"], e["inputs"]["v2"])],
                   "after": [(e["inputs"]["m1"], e["inputs"]["v1_after"]),
                             (e["inputs"]["m2"], e["outcome"])],
                   "kind": e["inputs"]["kind"]} for e in eps]
        laws, steps = search_conservation(spec.name, events, tol=spec.tol)
        for law in laws:
            law.provenance["support"] = sum(
                1 for ev in events if law.scope == "all" or ev["kind"] in law.scope)
        self.search_steps[spec.name] = self.search_steps.get(spec.name, 0) + steps
        old = [l.formula() for l in self.claws.get(spec.name, [])]
        self.claws[spec.name] = laws
        new = [l.formula() for l in laws]
        if new != old:
            desc = "; ".join(f"total {l.formula()} is the same before and after "
                             + ("in every collision" if l.scope == "all"
                                else f"only in {'/'.join(l.scope)} collisions")
                             + ("" if l.provenance.get("support", 0) >= ESTABLISHED
                                else f" [tentative: {l.provenance.get('support', 0)} event(s)]")
                             for l in laws) or "nothing"
            self.note("reflect" if reflecting else "revise",
                      f"{spec.name}: {desc} ({len(eps)} experiences)")
        return new

    # ------------------------------------------------------------- language
    def bind(self, token, meaning):
        self.vocab[token] = tuple(meaning)

    # -------------------------------------------------------------- saving
    def to_json(self):
        return {
            "name": self.name,
            "library": {k: v.to_json() for k, v in sorted(self.library.laws.items())},
            "hypotheses": {k: show(v) for k, v in sorted(self.hypotheses.items())},
            "quantity_laws": {k: v.to_json() for k, v in sorted(self.qlaws.items())},
            "conservation_laws": {k: [l.to_json() for l in v] for k, v in sorted(self.claws.items())},
            "vocabulary": {k: list(v) for k, v in sorted(self.vocab.items())},
            "names": dict(sorted(self.names.items())),
            "search_steps": dict(sorted(self.search_steps.items())),
            "inventions": dict(sorted(self.inventions.items())),
            "quantities": dict(sorted(self.quantities.items())),
            "inverses": dict(sorted(self.library.inverses.items())),
            "cycles": dict(sorted(self.library.cycles.items())),
            "symmetric": sorted(self.library.symmetric),
            "curiosity": self.curiosity.to_json(),
            "memory": self.memory.to_json(),
            "log": self.log,
        }

    def save(self, path):
        with open(path, "w") as f:
            json.dump(self.to_json(), f, indent=1, sort_keys=True)
            f.write("\n")

    @classmethod
    def load(cls, path):
        with open(path) as f:
            d = json.load(f)
        b = cls(d.get("name", "Ultron"))
        for k, v in d["library"].items():
            b.library.add(Law.from_json(v))
            b.hypotheses[k] = b.library.get(k).expr
        b.qlaws = {k: law_from_json(v) for k, v in d["quantity_laws"].items()}
        b.claws = {k: [ConservationLaw.from_json(l) for l in v]
                   for k, v in d["conservation_laws"].items()}
        b.vocab = {k: tuple(v) for k, v in d["vocabulary"].items()}
        b.names = dict(d.get("names", {}))
        b.search_steps = dict(d.get("search_steps", {}))
        b.inventions = dict(d.get("inventions", {}))
        b.quantities = dict(d.get("quantities", {}))
        b.library.inverses = dict(d.get("inverses", {}))
        b.library.cycles = dict(d.get("cycles", {}))
        b.library.symmetric = set(d.get("symmetric", []))
        b.curiosity = Curiosity.from_json(d.get("curiosity", {}))
        b.memory = Memory.from_json(d["memory"])
        b.log = list(d.get("log", []))
        return b


__all__ = ["Brain", "Spec", "BOOL"]
