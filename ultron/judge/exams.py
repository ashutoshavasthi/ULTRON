"""The Judge: held-out exams on problems Ultron has never seen.

Every exam runs on a *copy* of the brain, so being examined never teaches it
anything. Each item is also answered by two memorisers built from exactly the
same experiences Ultron had:

  * lookup   - answers only if it has seen these exact inputs before
  * nearest  - answers with the outcome of the most similar past experience
"""

import copy
import random

from ..brain import reasoner
from ..brain.brain import Brain
from ..brain.language import read_number
from ..logic import peano
from ..env import dataworld
from ..trainer.lessons import Combining, Mechanics, NoisyLab, NUMBER_WORDS, RealData

REFUSE = "I can't"      # the right answer to an impossible question


# ---------------------------------------------------------------- baselines
def _inputs_of(ep, target):
    if "inputs" in ep:
        return ep["inputs"], ep["outcome"]
    return {k: v for k, v in ep.items() if k != target}, ep[target]


def lookup(episodes, target, inputs):
    for ep in episodes:
        inp, out = _inputs_of(ep, target)
        if inp == inputs:
            return out
    return None


def nearest(episodes, target, inputs):
    best, best_d = None, None
    for ep in episodes:
        inp, out = _inputs_of(ep, target)
        d = 0.0
        for k, v in inputs.items():
            w = inp.get(k)
            if isinstance(v, (int, float)) and not isinstance(v, bool):
                d += abs(v - w) / (abs(v) + abs(w) + 1e-12)
            elif v != w:
                d += 1e9
        if best_d is None or d < best_d:
            best, best_d = out, d
    return best


class Tally:
    def __init__(self, name, tol=None):
        self.name = name
        self.tol = tol
        self.scores = {"ultron": [0, 0], "lookup": [0, 0], "nearest": [0, 0]}
        self.examples = []

    def ok(self, got, truth):
        if truth == REFUSE:
            return got is None
        if got is None:
            return False
        if self.tol is None:
            return got == truth
        return abs(got - truth) <= self.tol * abs(truth)

    def add(self, who, got, truth):
        s = self.scores[who]
        s[1] += 1
        s[0] += self.ok(got, truth)

    def item(self, question, truth, ultron, memory=None, target=None, inputs=None):
        self.add("ultron", ultron, truth)
        if memory is not None:
            self.add("lookup", lookup(memory, target, inputs), truth)
            self.add("nearest", nearest(memory, target, inputs), truth)
        if len(self.examples) < 3:
            self.examples.append({"question": question, "truth": truth, "ultron": ultron})

    def rate(self, who="ultron"):
        c, n = self.scores[who]
        return c / n if n else None

    def to_json(self):
        return {"name": self.name, "scores": self.scores, "examples": self.examples,
                "tolerance": self.tol}


def _result(lesson, tallies, threshold, extra=None):
    passed = all(t.rate() is not None and t.rate() >= threshold for t in tallies)
    return {"lesson": lesson, "passed": passed, "threshold": threshold,
            "items": [t.to_json() for t in tallies], **(extra or {})}


# ---------------------------------------------------------------- lessons 0-3
def exam_permanence(brain, seed=1000):
    b, rng = copy.deepcopy(brain), random.Random(seed)
    t = Tally("object still there after long hides (waited 50-5000)")
    mem = b.memory.of("peekaboo")
    for _ in range(40):
        inputs = {"went_in": rng.random() < 0.5, "waited": rng.randint(50, 5000)}
        truth = inputs["went_in"]
        t.item(inputs, truth, b.predict("peekaboo", inputs), mem, "there", inputs)
    return _result(0, [t], 0.99)


def exam_pairing(brain, seed=1001):
    b, rng = copy.deepcopy(brain), random.Random(seed)
    t = Tally("pairing trays of 6-30 objects")
    mem = b.memory.of("pair_off")
    for _ in range(60):
        a = rng.randint(6, 30)
        c = a if rng.random() < 0.4 else rng.randint(6, 30)
        inputs = {"nA": a, "nB": c}
        t.item(inputs, a == c, b.predict("pair_off", inputs), mem, "all_paired", inputs)
    return _result(1, [t], 0.99)


def exam_combining(brain, seed=1002):
    b, rng = copy.deepcopy(brain), random.Random(seed)
    add = Tally("putting together piles of 6-30")
    sub = Tally("taking away from piles of 6-60")
    for _ in range(60):
        inputs = {"nA": rng.randint(6, 30), "nB": rng.randint(6, 30)}
        add.item(inputs, inputs["nA"] + inputs["nB"], b.predict("merge", inputs),
                 b.memory.of("merge"), "total", inputs)
        n = rng.randint(6, 60)
        inputs = {"nA": n, "n_taken": rng.randint(0, n)}
        sub.item(inputs, n - inputs["n_taken"], b.predict("take_away", inputs),
                 b.memory.of("take_away"), "left", inputs)
    return _result(2, [add, sub], 0.99, {"noisy_tv": noisy_tv_report(brain)})


def noisy_tv_report(brain):
    order = [e for e in brain.log if e.get("kind") == "choice" and e.get("lesson") == 2]
    total = len(order)
    lamps = [i for i, e in enumerate(order) if e["choice"] == "lamps"]
    return {"total_choices": total, "lamp_choices": len(lamps),
            "last_lamp_choice": (lamps[-1] + 1) if lamps else None,
            "lamps_law": brain.hypotheses.get("lamps") is not None}


def exam_groups(brain, seed=1003, blank=True):
    b, rng = copy.deepcopy(brain), random.Random(seed)
    t = Tally("groups: 5-30 groups of 5-30")
    items = [{"groups": rng.randint(5, 30), "size": rng.randint(5, 30)} for _ in range(40)]
    for inputs in items:
        t.item(inputs, inputs["groups"] * inputs["size"], b.predict("groups", inputs),
               b.memory.of("groups"), "total", inputs)
    extra = {}
    if blank:
        extra["blank_brain"] = blank_brain_groups(items)
    return _result(3, [t], 0.99, extra)


def blank_brain_groups(items, seed=3):
    """A brand-new brain gets the same groups lesson but no earlier lessons."""
    from ..trainer.lessons import Groups
    from ..trainer.trainer import free_play
    fresh = Brain("blank")
    lesson = Groups(seed)
    for spec in lesson.specs():
        fresh.meet(spec)
    free_play(fresh, lesson, lesson.budget)
    t = Tally("blank brain: groups")
    for inputs in items:
        t.item(inputs, inputs["groups"] * inputs["size"], fresh.predict("groups", inputs))
    return {"score": t.scores["ultron"], "law": fresh.hypotheses.get("groups") is not None,
            "note": "same lesson, same budget, but no addition law in its library"}


# ---------------------------------------------------------------- lesson 4
def exam_language(brain, seed=1004):
    b, rng = copy.deepcopy(brain), random.Random(seed)
    read = Tally("reading numerals with 3-4 marks (100-9999)")
    for _ in range(30):
        n = rng.randint(100, 9999)
        v, _ = read_number(b, str(n))
        read.item(str(n), n, v)
    ask = Tally("answering written questions (numbers 10-999)")
    ops = [("+", lambda x, y: x + y), ("plus", lambda x, y: x + y),
           ("minus", lambda x, y: x - y), ("-", lambda x, y: x - y),
           ("times", lambda x, y: x * y), ("×", lambda x, y: x * y)]
    for _ in range(30):
        word, f = ops[rng.randrange(len(ops))]
        x, y = rng.randint(10, 999), rng.randint(10, 999)
        if word in ("minus", "-") and y > x:
            x, y = y, x
        if word in ("times", "×"):
            y = rng.randint(2, 40)
        q = f"what is {x} {word} {y}?"
        ask.item(q, str(f(x, y)), reasoner.arithmetic(b, q).text)
    words = Tally("questions in words (zero-ten)")
    for _ in range(20):
        x, y = rng.randint(0, 10), rng.randint(0, 10)
        word, f = [("plus", lambda p, q: p + q), ("times", lambda p, q: p * q)][rng.randrange(2)]
        q = f"{NUMBER_WORDS[x]} {word} {NUMBER_WORDS[y]}"
        words.item(q, str(f(x, y)), reasoner.arithmetic(b, q).text)
    proofs = Tally("Peano proofs derived from its own laws, independently checked")
    rules = peano.all_rules(b.library)
    for _ in range(10):
        law = rng.choice(["merge", "groups"])
        x, y = rng.randint(0, 9), rng.randint(0, 6)
        lhs = (law, peano.numeral(x), peano.numeral(y))
        truth = x + y if law == "merge" else x * y
        steps = peano.prove(lhs, rules)
        ok, _ = peano.check(lhs, truth, steps, rules)
        proofs.item(peano.show(lhs), True, ok)
    return _result(4, [read, ask, words, proofs], 0.99)


# ---------------------------------------------------------------- lesson 5
def exam_mechanics(brain, seed=1005):
    b, rng = copy.deepcopy(brain), random.Random(seed)
    world = Mechanics(seed=5).world     # same springs Ultron trained with
    r = lambda lo, hi: round(rng.uniform(lo, hi), 3)
    push = Tally("push: heavy balls (20-100 kg), big forces (100-1000 N)", tol=0.01)
    for _ in range(30):
        inputs = {"F": r(100, 1000), "m": r(20, 100)}
        push.item(inputs, world.push(inputs["m"], inputs["F"]), b.predict("push", inputs),
                  b.memory.of("push"), "a", inputs)
    stretch = Tally("stretch: known springs, long stretches (0.6-2 m)", tol=0.01)
    for _ in range(30):
        inputs = {"x": r(0.6, 2.0), "spring": rng.choice(world.springs)}
        stretch.item(inputs, world.stretch(inputs["spring"], inputs["x"]),
                     b.predict("stretch", inputs), b.memory.of("stretch"), "F", inputs)
    new = Tally("new spring: one measurement, then predict", tol=0.01)
    world.add_spring("S_new")
    x0 = 0.1
    b.experience("stretch", {"x": x0, "spring": "S_new"}, world.stretch("S_new", x0))
    for _ in range(10):
        inputs = {"x": r(0.2, 2.0), "spring": "S_new"}
        new.item(inputs, world.stretch("S_new", inputs["x"]), b.predict("stretch", inputs),
                 b.memory.of("stretch"), "F", inputs)
    launch = Tally("NEVER TRAINED: ball on a stretched spring, first acceleration", tol=0.01)
    traces = []
    for _ in range(20):
        spring, x, m = rng.choice(world.springs), r(0.1, 1.0), r(1, 50)
        ans = reasoner.physics(b, "a", {"x": x, "m": m}, {"spring": spring})
        launch.item({"spring": spring, "x": x, "m": m}, world.launch(spring, x, m), ans.value)
        if len(traces) < 1:
            traces.append(str(ans))
    collide = Tally("collisions of heavy balls (10-50 kg)", tol=0.01)
    for _ in range(30):
        m1, m2, v1 = r(10, 50), r(10, 50), r(1, 5)
        v2 = r(-5, v1 - 0.5)
        kind = rng.choice(["clay", "steel"])
        u1, u2 = world.collide(m1, v1, m2, v2, kind)
        inputs = {"m1": m1, "v1": v1, "m2": m2, "v2": v2, "kind": kind, "v1_after": u1}
        collide.item(inputs, u2, b.predict("collide", inputs), b.memory.of("collide"),
                     "v2_after", inputs)
    return _result(5, [push, stretch, new, launch, collide], 0.99,
                   {"launch_trace": traces[0] if traces else None})


# ---------------------------------------------------------------- lesson 6
def exam_real_data(brain):
    b = copy.deepcopy(brain)
    planets = Tally("Kepler: predict orbital period of Uranus and Neptune", tol=0.02)
    for row in RealData.bodies(RealData.PLANETS_TEST):
        inputs = {"r": row["r"], "system": row["system"]}
        planets.item(row["body"], row["T"], b.predict("orbit", inputs), b.memory.of("orbit"),
                     "T", inputs)
    moons = Tally("Jupiter's moons after seeing only Io (one-shot transfer)", tol=0.02)
    blank = Tally("blank brain after seeing only Io", tol=0.02)
    fresh = Brain("blank")
    for spec in RealData().specs():
        fresh.meet(spec)
    for row in RealData.bodies(RealData.MOON_SHOWN):
        for who in (b, fresh):
            who.experience("orbit", {"r": row["r"], "system": row["system"]}, row["T"])
    for row in RealData.bodies(RealData.MOONS_TEST):
        inputs = {"r": row["r"], "system": row["system"]}
        moons.item(row["body"], row["T"], b.predict("orbit", inputs), b.memory.of("orbit"),
                   "T", inputs)
        blank.item(row["body"], row["T"], fresh.predict("orbit", inputs))
    sun, jup = (b.qlaws["orbit"].value_for("Sun"), b.qlaws["orbit"].value_for("Jupiter")
                ) if b.qlaws.get("orbit") and b.qlaws["orbit"].kind == "grouped" else (None, None)
    gas = Tally("Boyle: predict pressure at small volumes (V < 24, unseen)", tol=0.02)
    _, test = RealData.gas_split()
    for row in test:
        gas.item({"V": row["V"]}, row["P"], b.predict("gas", {"V": row["V"]}),
                 b.memory.of("gas"), "P", {"V": row["V"]})
    extra = {"blank_one_shot": blank.to_json(),
             "sun_vs_jupiter": (jup / sun) if sun and jup else None}
    return _result(6, [planets, moons, gas], 0.99, extra)


# ---------------------------------------------------------------- lesson 7
def exam_noisy_lab(brain, seed=1007):
    b, rng = copy.deepcopy(brain), random.Random(seed)
    world = NoisyLab(seed=7).world
    push = Tally("noisy lab: TRUE acceleration of heavy balls (20-100 kg)", tol=0.03)
    for _ in range(30):
        m, F = rng.uniform(20, 100), rng.uniform(100, 1000)
        inputs = {"F": world.read(F), "m": world.read(m)}      # Ultron sees noisy readings
        push.item(inputs, world.push(m, F), b.predict("lab_push", inputs),
                  b.memory.of("lab_push"), "a", inputs)
    stretch = Tally("noisy lab: TRUE spring force at long stretches", tol=0.03)
    for _ in range(30):
        spring, x = rng.choice(world.springs), rng.uniform(0.6, 2.0)
        inputs = {"x": world.read(x), "spring": spring}
        stretch.item(inputs, world.stretch(spring, x), b.predict("lab_stretch", inputs),
                     b.memory.of("lab_stretch"), "F", inputs)
    return _result(7, [push, stretch], 0.99, {"effort": noisy_effort(brain)})


def noisy_effort(brain, seed=7):
    """How much searching did the noisy lab take, compared with a blank brain?"""
    from ..trainer.trainer import free_play
    fresh = Brain("blank")
    lesson = NoisyLab(seed)
    for spec in lesson.specs():
        fresh.meet(spec)
    free_play(fresh, lesson, lesson.budget)
    return {"ultron_steps": {k: brain.search_steps.get(k, 0) for k in ("lab_push", "lab_stretch")},
            "blank_steps": {k: fresh.search_steps.get(k, 0) for k in ("lab_push", "lab_stretch")},
            "blank_laws": sorted(fresh.qlaws)}


# ---------------------------------------------------------------- lesson 8
def exam_final(brain, seed=1008):
    b, rng = copy.deepcopy(brain), random.Random(seed)
    ask = lambda q: reasoner.arithmetic(b, q).value

    div = Tally("division - never taught ('what times 7 equals 84')")
    for _ in range(20):
        x, y = rng.randint(2, 30), rng.randint(2, 12)
        div.item(f"what times {y} equals {x * y}", x, ask(f"what times {y} equals {x * y}"))

    inv = Tally("inverse questions ('12 minus what equals 5', 'what plus 9 equals 30')")
    for _ in range(20):
        x, y = rng.randint(0, 60), rng.randint(0, 60)
        form = rng.randrange(3)
        if form == 0:
            q, t = f"what plus {y} equals {x + y}", x
        elif form == 1:
            q, t = f"{x + y} minus what equals {x}", y
        else:
            q, t = f"what minus {y} equals {x}", x + y
        inv.item(q, t, ask(q))

    chain = Tally("chains of three operations ('100 minus 37 plus 12 minus 5')")
    for _ in range(15):
        if rng.random() < 0.5:
            v = rng.randint(50, 500)
            q = str(v)
            for _ in range(3):
                n = rng.randint(1, 40)
                if rng.random() < 0.5:
                    q, v = q + f" plus {n}", v + n
                else:
                    q, v = q + f" minus {n}", v - n
        else:
            ns = [rng.randint(2, 12) for _ in range(3)]
            q, v = " times ".join(map(str, ns)), ns[0] * ns[1] * ns[2]
        chain.item(q, v, ask(q))

    impossible = Tally("impossible questions: the only right answer is 'I can't'")
    for _ in range(15):
        form = rng.randrange(3)
        if form == 0:
            x = rng.randint(0, 20)
            q = f"{x} minus {x + rng.randint(1, 20)}"
        elif form == 1:
            y = rng.randint(2, 12)
            q = f"what times {y} equals {y * rng.randint(1, 20) + rng.randint(1, y - 1)}"
        else:
            y = rng.randint(10, 40)
            q = f"what plus {y} equals {rng.randint(0, y - 1)}"
        impossible.item(q, REFUSE, ask(q))

    mech = Mechanics(seed=5).world
    phys = Tally("physics solved for a different unknown (mass, stretch, force)", tol=0.01)
    for _ in range(15):
        form = rng.randrange(3)
        if form == 0:
            m, F = rng.uniform(1, 80), rng.uniform(1, 900)
            ans = reasoner.physics(b, "m", {"F": F, "a": mech.push(m, F)})
            phys.item(("m", F), m, ans.value)
        elif form == 1:
            s, x = rng.choice(mech.springs), rng.uniform(0.05, 3)
            ans = reasoner.physics(b, "x", {"F": mech.stretch(s, x)}, {"spring": s})
            phys.item(("x", s), x, ans.value)
        else:
            m, F = rng.uniform(1, 80), rng.uniform(1, 900)
            ans = reasoner.physics(b, "F", {"m": m, "a": mech.push(m, F)})
            phys.item(("F", m), F, ans.value)

    back = Tally("backwards chain: mass from spring, stretch and acceleration", tol=0.01)
    for _ in range(10):
        s, x, m = rng.choice(mech.springs), rng.uniform(0.1, 1.5), rng.uniform(1, 60)
        ans = reasoner.physics(b, "m", {"x": x, "a": mech.launch(s, x, m)}, {"spring": s})
        back.item((s, x), m, ans.value)

    phys_no = Tally("impossible physics: unknown spring, or a quantity no law relates")
    for i in range(10):
        if i % 2:
            ans = reasoner.physics(b, "a", {"x": 0.3, "m": 2.0}, {"spring": "S99"})
        else:
            ans = reasoner.physics(b, "v", {"F": rng.uniform(1, 50), "m": rng.uniform(1, 9)})
        phys_no.item(i, REFUSE, ans.value)

    sky = Tally("unseen real bodies: Ceres, Halley's Comet; Earth's distance from its year; "
                "Titan (unknown system: must refuse)", tol=0.02)
    for row in dataworld.unseen_orbits():
        inputs = {"r": row["r"], "system": row["system"]}
        truth = row["T"] if row["system"] == "Sun" else REFUSE
        sky.item(row["body"], truth, b.predict("orbit", inputs))
    earth = next(r for r in dataworld.orbits() if r["body"] == "Earth")
    ans = reasoner.physics(b, "r", {"T": earth["T"]}, {"system": "Sun"})
    sky.item("Earth's distance from its year", earth["r"], ans.value)

    return _result(8, [div, inv, chain, impossible, phys, back, phys_no, sky], 0.9)


EXAMS = {0: exam_permanence, 1: exam_pairing, 2: exam_combining, 3: exam_groups,
         4: exam_language, 5: exam_mechanics, 6: exam_real_data, 7: exam_noisy_lab,
         8: exam_final}
