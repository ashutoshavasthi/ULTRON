"""Ultron's brain: predict -> act -> observe -> compare -> revise -> store.

Everything Ultron knows lives in this object and can be saved to one JSON
file. Nothing in here contains a law or a formula; the laws are found by the
hypothesis engines from Ultron's own experiences.
"""

import json

from . import units as U
from .curiosity import Curiosity
from .dsl import BOOL, INT, LIST, Law, Library, safe_evaluate, show, size
from .invariants import (ConservationLaw, QuantityLaw, SumLaw, law_from_json,
                         search_conservation, search_invariant, search_sum_invariant)
from .invariants import monomial_str
from .memory import Memory, Spec
from .synth import synthesize

CONFIRM_STREAK = 8   # correct predictions in a row before a law is trusted
ESTABLISHED = 3      # confirmations before a measured law stops being tentative
N_RIVALS = 3         # alternative explanations kept to design experiments against


MIN_FOR_EXCEPTIONS = 10    # fewer experiences than this: too few to call any of them wrong


def worth_listing(law_size, n_odd, n):
    """MDL: is a law plus a list of its exceptions a shorter description of n experiences
    than no law at all (about one unit per experience)? Never more than a quarter odd."""
    from .synth import EXCEPTION_COST
    return n_odd <= n // 4 and law_size + EXCEPTION_COST * n_odd < n


def allowed_exceptions(n):
    return max(1, n // 4)


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
        self.kinds = {}                     # kinds of explanation it invented (kinds.py)
        self.slaws = {}                     # spec -> SequenceLaw (a law of an invented kind)
        self.kind_steps = {}                # spec -> {"innate", "reuse", "invent"} effort
        self.inventing = True               # may it invent new kinds? (off: ablation)
        self.eyes = None                    # learned in Phase 3 (senses/eyes.py)
        self.exceptions = {}                # spec -> experiences its law doesn't fit
        self.ambiguous = {}                 # spec -> equally simple rival laws
        self.quantity_rivals = {}           # spec -> their powers (to design experiments)
        self.group_fails = {}               # (spec, object) -> failures in a row
        self.since = {}                     # spec -> first experience after the world changed
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
        """Kinds of experience where I hold an idea I haven't confirmed yet, or where I
        haven't yet watched enough to test any idea at all (a few readings of one cup
        can't be boring: they can't say anything yet). A fair look at a world of objects
        is several WHOLE objects: the one I'm still watching doesn't count yet."""
        from .kinds import MIN_GROUPS, sequences
        for name in options:
            spec = self.memory.specs.get(name)
            if spec is not None and spec.kind == "sequence" and name not in self.slaws:
                eps = self.memory.of(name)
                seqs = sequences(eps, spec.target, spec.order_by, spec.group_by)
                current = eps[-1].get(spec.group_by) if eps else None
                whole = sum(1 for g, (xs, ys) in seqs.items() if len(ys) >= 4 and g != current)
                if whole < MIN_GROUPS:
                    return name
            if spec is None or spec.kind != "program" or self.hypotheses.get(name) is None:
                continue
            law = self.library.get(name)
            if law is None or law.provenance.get("doubted"):
                return name
        return None

    def trusts_quantity(self, name):
        law = self.qlaws.get(name)
        return law is not None and law.provenance.get("support", 0) >= ESTABLISHED

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
        spec = self.memory.specs.get(spec_name)
        if spec is not None and spec.kind == "quantity" and self.quantity_rivals.get(spec_name):
            pick = self._separate_quantity_laws(spec, options)
            if pick is not None:
                return pick
        if spec is not None and spec.kind == "quantity":
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

    def _separate_quantity_laws(self, spec, options):
        """Equally simple measurement laws fit everything seen (two quantities always
        moved together): set up the experiment where their predictions differ most."""
        law = self.qlaws.get(spec.name)
        if law is None or law.kind != "global":
            return None
        eps = self.memory.of(spec.name)
        laws = [law]
        for powers in self.quantity_rivals[spec.name]:
            vals = []
            for ep in eps:
                v = 1.0
                for q, p in powers.items():
                    v *= ep[q] ** p if ep.get(q) else float("nan")
                vals.append(v)
            vals = sorted(v for v in vals if v == v)
            if vals:
                laws.append(QuantityLaw(spec.name, powers, "global",
                                        constant=vals[len(vals) // 2]))
        if len(laws) < 2:
            return None
        best, best_gap = None, 0.0
        for inputs in options:
            try:
                preds = [l.solve(spec.target, inputs) for l in laws]
            except (KeyError, ZeroDivisionError, ValueError, TypeError):
                continue
            preds = [p for p in preds if p is not None]
            if len(preds) < 2:
                continue
            mean = sum(abs(p) for p in preds) / len(preds)
            gap = (max(preds) - min(preds)) / mean if mean else 0.0
            if gap > best_gap:
                best, best_gap = inputs, gap
        if best is not None and best_gap > 0.01:
            self.note("design", f"{spec.name}: {law.formula()} and its rivals "
                                f"{', '.join(QuantityLaw(spec.name, r, 'global').formula() for r in self.quantity_rivals[spec.name])} "
                                f"disagree most about {best}; I'll set that up to find out")
            return best
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
            if law is None:
                return None
            if not self.law_applies(spec_name, group):
                from .metalaws import predicted_property
                prop = predicted_property(self, spec_name, group)
                if prop is None or law.kind != "grouped":
                    return None
                law = QuantityLaw(law.etype, law.powers, "global", constant=prop)
                return law.solve(spec.target, inputs)
            return law.solve(spec.target, inputs, group)
        if spec.kind == "feature":
            return None
        if spec.kind == "sequence":
            return self._predict_sequence(spec, inputs)
        if spec.kind == "conservation":
            return self._predict_collision(spec_name, inputs)
        if spec.kind == "measure":
            return self._predict_reading(spec, inputs)
        raise ValueError(spec.kind)

    def history(self, spec, group):
        """This object's readings so far, ordered: (xs, ys)."""
        from .kinds import sequences
        eps = [e for e in self.memory.of(spec.name)
               if not spec.group_by or e.get(spec.group_by) == group]
        return sequences(eps, spec.target, spec.order_by, spec.group_by).get(
            group if spec.group_by else "_", ([], []))

    def _predict_sequence(self, spec, inputs):
        law = self.slaws.get(spec.name)
        if law is None:
            return None
        group = inputs.get(spec.group_by) if spec.group_by else None
        return law.predict(self.history(spec, group), inputs[spec.order_by], group)

    def _learn_sequence(self, spec, surprised):
        """Readings along a sequence: first the kinds it was born with, then the kinds it
        invented, then (if still stuck) a new kind from the grammar."""
        from . import kinds
        name = spec.name
        law = self.slaws.get(name)
        eps = self.memory.of(name)
        if law is not None and not surprised:
            law.provenance["support"] = law.provenance.get("support", 0) + 1
            return None
        if law is not None and law.scope == "per group":
            group = eps[-1].get(spec.group_by)
            hist = self.history(spec, group)
            if group not in law.properties:
                c = law.value_for(group, hist)
                zs = kinds.transform(law.template, *hist)
                if c is not None and zs and len(zs) >= 2 and kinds._same(
                        zs, max(spec.tol, 1e-9) + 4 * spec.precision):
                    law.properties[group] = c
                    self.note("measure", f"{name}: met new {spec.group_by} {group}; its "
                                         f"{law.formula()} = {c:.6g}")
                    return None
                if not zs or len(zs) < 2:
                    return None     # too few readings of this one to say anything yet
        seqs = kinds.sequences(eps, spec.target, spec.order_by, spec.group_by)
        if sum(1 for xs, ys in seqs.values() if len(ys) >= 4) < kinds.MIN_GROUPS:
            return None             # not enough to go on yet
        effort = self.kind_steps.setdefault(name, {"innate": 0, "reuse": 0, "invent": 0})
        if law is None and not effort["innate"]:
            # the kinds it was born with: a product, or a sum, of the readings
            names = list(spec.inputs) + [spec.target]
            rows = [{k: e[k] for k in names + ([spec.group_by] if spec.group_by else [])}
                    for e in eps]
            r1 = search_invariant(name, rows, names, max(spec.tol, 1e-9) + 4 * spec.precision,
                                  group_by=spec.group_by)
            effort["innate"] += r1.steps
            if r1.law is None and spec.group_by:
                r2 = search_sum_invariant(name, rows, names, spec.tol + 4 * spec.precision,
                                          spec.group_by)
                effort["innate"] += r2.steps
            if r1.law is not None:
                self.note("stuck", f"{name}: {r1.law.formula()} stays the same, but only for "
                                   f"these readings; I keep looking")
            else:
                self.note("stuck", f"{name}: no product or sum of the readings stays the same; "
                                   f"none of the kinds of explanation I was born with fits")
        new, steps, kind = kinds.explain(self, spec, eps)
        effort["reuse"] += steps["reuse"]
        effort["invent"] += steps["invent"]
        self.search_steps[name] = self.search_steps.get(name, 0) + steps["reuse"] + steps["invent"]
        if new is None:
            if effort.get("stuck_at") != len(seqs):
                effort["stuck_at"] = len(seqs)
                self.note("stuck", f"{name}: nothing I can express stays the same "
                                   f"({len(seqs)} {spec.group_by or 'sequence'}s, "
                                   f"{len(eps)} readings)")
            if law is not None:
                self.note("doubt", f"{name}: {law.formula()} just failed; back to being unsure")
                del self.slaws[name]
            return None
        if law is None or law.template != new.template or law.scope != new.scope:
            self.slaws[name] = new
            self.note("revise", f"{name}: {new.formula()} stays the same "
                                f"{'for everything' if new.scope == 'global' else 'for each ' + str(spec.group_by)}"
                                f" ({kind['name']}: {kind['words']})")
        else:
            law.properties.update(new.properties)
            law.constant = new.constant
            law.provenance.pop("common_rest", None)
            if "common_rest" in new.provenance:
                law.provenance["common_rest"] = new.provenance["common_rest"]
        return new

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
        if isinstance(actual, (list, tuple)) or isinstance(predicted, (list, tuple)):
            same = isinstance(actual, (list, tuple)) and isinstance(predicted, (list, tuple)) \
                and tuple(actual) == tuple(predicted)
            return 0.0 if same else 1.0
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
        elif spec.kind == "feature":
            self.memory.store(spec_name, {"inputs": inputs, "outcome": outcome})
            revised = None
        elif spec.kind == "sequence":
            self.memory.store(spec_name, {**inputs, spec.target: outcome})
            revised = self._learn_sequence(spec, surprised)
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
        held = self.hypotheses.get(name)
        eps = self.memory.of(name)
        if held is not None and len(eps) >= MIN_FOR_EXCEPTIONS:
            odd = [e for e in eps if safe_evaluate(held, e["inputs"], self.library) != e["outcome"]]
            if worth_listing(size(held), len(odd), len(eps)):
                # a few anomalies don't bring a theory down at once: first a short look for
                # a slightly bigger law that fits everything, and if there is none, keep the
                # law and list the anomalies (cheaper than having no law)
                quick = synthesize([e["inputs"] for e in eps], [e["outcome"] for e in eps],
                                   spec.inputs, spec.out_type, self.library, self.constants(),
                                   max_size=min(7, size(held) + 2), max_bank=20000,
                                   rivals=N_RIVALS, extra=self.primitives())
                self.search_steps[name] = self.search_steps.get(name, 0) + quick.steps
                if quick.expr is None:
                    self.exceptions[name] = odd
                    self.note("doubt", f"{name}: {eps[-1]['inputs']} -> {eps[-1]['outcome']} "
                                       f"doesn't fit {show(held)}, and no slightly bigger law fits "
                                       f"everything; {len(odd)} of {len(eps)} don't fit, few "
                                       f"enough to list as mis-recorded, so I keep my law")
                    return None
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
        if result.expr is None and len(eps) >= MIN_FOR_EXCEPTIONS:
            # nothing fits everything: does something short fit all but a few? A few
            # mis-recorded experiences shouldn't hide a law (if listing them is cheaper
            # than having no law at all)
            allowed = allowed_exceptions(len(eps))
            tolerant = synthesize([e["inputs"] for e in eps], [e["outcome"] for e in eps],
                                  spec.inputs, spec.out_type, self.library, self.constants(),
                                  extra=self.primitives(), exceptions=allowed)
            self.search_steps[name] += tolerant.steps
            if tolerant.expr is not None and worth_listing(
                    size(tolerant.expr), len(tolerant.exceptions), len(eps)):
                odd = [eps[i] for i in tolerant.exceptions]
                self.exceptions[name] = odd
                self.failed_search.pop(name, None)
                self.hypotheses[name] = tolerant.expr
                self.rivals[name] = []
                self.found_at[name] = len(eps)
                shown = "; ".join(f"{e['inputs']} -> {e['outcome']}" for e in odd[:3])
                self.note("revise", f"{name}: no law fits all {len(eps)} experiences, but "
                                    f"{show(tolerant.expr)} fits all except {len(odd)} "
                                    f"({shown}). Listing those few costs less than having no "
                                    f"law, so I think they were mis-recorded; I'll trust the "
                                    f"law only if it keeps predicting")
                return show(tolerant.expr)
        if result.expr is None:
            self.failed_search[name] = len(eps)
            self.hypotheses.pop(name, None)
            self.note("stuck", f"{name}: no simple law explains all {len(eps)} experiences "
                               f"(searched {result.steps} programs)")
            return None
        self.exceptions.pop(name, None)
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
        if any(t == LIST for t in spec.inputs.values()):
            law.provenance["list_params"] = True
        self.library.add(law)
        self.note("confirm", f"{spec.name}: {show(expr)} predicted {CONFIRM_STREAK} new "
                             f"experiences in a row; added to my library of building blocks")
        from .compression import confirm_predictions
        confirm_predictions(self, expr)

    def _learn_quantity(self, spec, surprised):
        name = spec.name
        eps = self.memory.of(name)[self.since.get(name, 0):]   # since the world last changed
        law = self.qlaws.get(name)
        group = eps[-1].get(spec.group_by) if spec.group_by else None
        if not surprised:
            self.group_fails.pop((name, group), None)
            if law is not None:
                self._refine(law, eps)
                law.provenance["support"] = law.provenance.get("support", 0) + 1
                if law.provenance["support"] == ESTABLISHED:
                    self.note("establish", f"{name}: {law.formula()} has now predicted "
                                           f"{ESTABLISHED} new experiences; no longer tentative")
            return None
        if self._changed(spec, law, group, eps):
            return None
        new_object = (law is not None and law.kind == "grouped"
                      and eps[-1].get(spec.group_by) not in law.properties)
        if (law is not None and not new_object
                and law.provenance.get("support", 0) >= ESTABLISHED):
            self.note("doubt", f"{name}: my established law {law.formula()} just failed; "
                               f"back to being unsure")
        names = list(spec.inputs) + [spec.target]
        result = search_invariant(name, eps, names, spec.tol, group_by=spec.group_by,
                                  prior_powers=self.known_forms(), precision=spec.precision,
                                  require=spec.target)
        self.search_steps[name] = self.search_steps.get(name, 0) + result.steps
        self.quantity_rivals[name] = list(result.rivals[:3]) if result.law is not None else []
        if result.law is not None and result.rivals:
            rivals = [QuantityLaw(name, r, "global").formula() for r in result.rivals[:3]]
            if self.ambiguous.get(name) != rivals:
                self.ambiguous[name] = rivals
                self.note("doubt", f"{name}: {result.law.formula()} fits, but so does "
                                   f"{' and '.join(rivals)}, just as simply: what I've seen "
                                   f"can't tell them apart (some things always moved together). "
                                   f"I need an experiment that changes one without the other")
        else:
            self.ambiguous.pop(name, None)
        if result.law is None and spec.group_by:
            # no single product stays constant: is something *shared* between two forms?
            result = search_sum_invariant(name, eps, names, spec.tol + 4 * spec.precision,
                                          spec.group_by, errors=spec.errors)
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

    def _changed(self, spec, law, group, eps):
        """An established law keeps failing for one object, and its recent readings agree
        with each other: the object itself changed (a spring replaced by a stiffer one
        with the same name). The old object becomes history; the new one is measured."""
        if (law is None or not isinstance(law, QuantityLaw)
                or (law.kind == "grouped" and group not in law.properties)
                or law.provenance.get("support", 0) < ESTABLISHED):
            return False
        key = (spec.name, group)
        self.group_fails[key] = self.group_fails.get(key, 0) + 1
        if self.group_fails[key] < 3:
            return False
        mine = [e for e in eps if law.kind == "global" or e.get(spec.group_by) == group]
        recent = mine[-3:]
        vals = [self._monomial(e, law.powers) for e in recent]
        c = sum(abs(p) for p in law.powers.values())
        mean = sum(vals) / len(vals)
        if mean == 0 or (max(vals) - min(vals)) / abs(mean) > max(spec.tol, 1e-9) + 2 * c * spec.precision + 1e-9:
            return False
        if law.kind == "global":
            old = law.constant
            # everything before the last three readings is history now
            self.since[spec.name] = len(self.memory.of(spec.name)) - len(recent)
            law.provenance.setdefault("history", []).append(old)
            law.constant = mean
            before = "the old world"
        else:
            old = law.properties[group]
            n = sum(1 for k in law.properties if k.startswith(f"{group}@before"))
            before = f"{group}@before{n + 1}"
            for e in mine[:-3]:
                e[spec.group_by] = before
            law.properties[before] = old
            law.properties[group] = mean
        self.group_fails.pop(key, None)
        self.note("revise", f"{spec.name}: {group or 'the world'} has changed. My law {law.formula()} kept "
                            f"failing for it alone, and its last {len(recent)} readings agree: "
                            f"{law.formula()} was {old:.6g}, now {mean:.6g}. I keep the old one "
                            f"as history ({before}) and carry on with the new")
        return True

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
            spec = self.memory.specs.get(law.etype)
            if spec is not None and spec.errors:
                import statistics      # noisy readings: the middle one, not the average
                law.properties = {k: statistics.median(v) for k, v in sorted(groups.items())}
            else:
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
        from .compression import look_for_exponent_laws, look_for_ladders
        from .gaps import look_for_gaps
        from .columns import look_for_columns, trust_fast_paths
        self._check_symmetry()
        look_for_shapes(self)
        find_inverses(self)
        look_for_ladders(self)
        look_for_columns(self)
        trust_fast_paths(self)
        look_for_exponent_laws(self)
        from .metalaws import look_for_property_laws
        look_for_property_laws(self)
        look_for_gaps(self)
        self._sleep()

    def _sleep(self):
        """Do my laws share a piece nobody taught me, worth writing once (it makes the
        description of everything I know shorter)? Then it becomes a building block."""
        from . import abstraction
        progs = [l.expr for n, l in sorted(self.library.laws.items())
                 if l.on_numbers and l.out_type == INT and not l.provenance.get("abstraction")]
        pieces, _ = abstraction.sleep(progs, self.library)
        for name, expr, sv in pieces:
            self.note("invent", f"while sleeping I noticed my laws share a piece: {name} = "
                                f"{show(expr)}; writing it once makes everything I know "
                                f"{sv} pieces shorter, so it is a building block now")

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
            "kinds": dict(sorted(self.kinds.items())),
            "sequence_laws": {k: v.to_json() for k, v in sorted(self.slaws.items())},
            "kind_steps": dict(sorted(self.kind_steps.items())),
            "eyes": self.eyes.to_json() if self.eyes is not None else None,
            "exceptions": dict(sorted(self.exceptions.items())),
            "since": dict(sorted(self.since.items())),
            "quantities": dict(sorted(self.quantities.items())),
            "inverses": dict(sorted(self.library.inverses.items())),
            "cycles": dict(sorted(self.library.cycles.items())),
            "symmetric": sorted(self.library.symmetric),
            "fast": dict(sorted(self.library.fast.items())),
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
        from .kinds import SequenceLaw
        b.kinds = dict(d.get("kinds", {}))
        b.slaws = {k: SequenceLaw.from_json(v) for k, v in d.get("sequence_laws", {}).items()}
        b.kind_steps = dict(d.get("kind_steps", {}))
        b.exceptions = dict(d.get("exceptions", {}))
        b.since = dict(d.get("since", {}))
        if d.get("eyes"):
            from ..senses.eyes import Eyes
            b.eyes = Eyes.from_json(d["eyes"])
        b.library.inverses = dict(d.get("inverses", {}))
        b.library.cycles = dict(d.get("cycles", {}))
        b.library.symmetric = set(d.get("symmetric", []))
        b.library.fast = {k: tuple(v) for k, v in d.get("fast", {}).items()}
        b.library.squaring = "fractional repeats" in d.get("inventions", {})
        from .columns import attach
        attach(b)
        b.curiosity = Curiosity.from_json(d.get("curiosity", {}))
        b.memory = Memory.from_json(d["memory"])
        b.log = list(d.get("log", []))
        return b


__all__ = ["Brain", "Spec", "BOOL"]
