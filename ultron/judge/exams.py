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
from ..brain.dsl import show
from ..brain.invariants import SumLaw
from ..brain.language import read_number
from ..logic import peano
from ..env import dataworld
from fractions import Fraction

from ..trainer.lessons import Combining, Mechanics, NoisyLab, NUMBER_WORDS, Owing, RealData

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
    def __init__(self, name, tol=None, abs_tol=None):
        self.name = name
        self.tol = tol
        self.abs_tol = abs_tol      # when a relative tolerance would be unfair (tiny values)
        self.scores = {"ultron": [0, 0], "lookup": [0, 0], "nearest": [0, 0]}
        self.examples = []

    def ok(self, got, truth):
        if truth == REFUSE:
            return got is None
        if isinstance(got, tuple) and got and got[0] == "between":
            lo, hi = got[1], got[2]
            return (isinstance(truth, float) and lo[0] / lo[1] <= truth <= hi[0] / hi[1]
                    and hi[0] / hi[1] - lo[0] / lo[1] <= (self.tol or 1.0))
        if got is None:
            return False
        if self.abs_tol is not None:
            return abs(got - truth) <= self.abs_tol
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
                "tolerance": self.tol if self.abs_tol is None else f"±{self.abs_tol}"}


def _result(lesson, tallies, threshold, extra=None):
    passed = all(t.rate() is not None and t.rate() >= threshold for t in tallies)
    return {"lesson": lesson, "passed": passed, "threshold": threshold,
            "items": [t.to_json() for t in tallies], **(extra or {})}


# ---------------------------------------------------------------- lessons 0-3
def exam_permanence(brain, seed=1000):
    b, rng = copy.deepcopy(brain), random.Random(seed)
    t = Tally("all 6-30 hidden things still there after long hides (waited 50-5000)")
    mem = b.memory.of("peekaboo")
    for _ in range(40):
        inputs = {"hidden": rng.randint(6, 30), "waited": rng.randint(50, 5000)}
        t.item(inputs, inputs["hidden"], b.predict("peekaboo", inputs), mem, "found", inputs)
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


def active_vs_passive(upto=8, curated=True):
    """Experiences Ultron needed before it first held the law it finally kept, when it
    designs its own experiments versus when it only watches the scenes it is shown.
    curated=False: the teacher shows uniformly random scenes over a wider range."""
    from ..trainer.trainer import Trainer
    out = {}
    for mode in ("active", "passive"):
        brain = Brain(mode)
        brain.active = mode == "active"
        trainer = Trainer(brain)
        for n in range(upto + 1):
            lesson = trainer.lessons[n]
            lesson.curated = curated
            brain.lesson = n
            for spec in lesson.specs():
                brain.meet(spec)
            if n == 4:
                trainer.teach_names(lesson)
            elif n == 6:
                trainer.teach_real_data(lesson)
            elif n == 8:
                trainer.teach_owing(lesson)
            else:
                from ..trainer.trainer import free_play
                free_play(brain, lesson, lesson.budget)
        out[mode] = {name: law.provenance.get("found_after")
                     for name, law in sorted(brain.library.laws.items())}
    return out


def biased_teacher():
    """A trainer who never shows equal trays (lesson 1) and never lets the purse be
    empty or in debt (lesson 8). Can Ultron still learn, by setting those situations
    up itself? Compared with the same brain when it only watches."""
    from ..trainer.trainer import Trainer
    out = {}
    for mode in ("active", "passive"):
        brain = Brain(mode)
        brain.active = mode == "active"
        trainer = Trainer(brain)
        for n in (1, 8):
            trainer.lessons[n].biased = True
        row = {}
        for n in range(9):
            r = trainer.run(n)
            if n in (1, 8):
                row[str(n)] = {"passed": r["passed"],
                               "scores": [i["scores"]["ultron"] for i in r["items"]]}
        row["invented_below_zero"] = "line:earn/spend" in brain.inventions
        out[mode] = row
    return out


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
def exam_owing(brain, seed=1009):
    b, rng = copy.deepcopy(brain), random.Random(seed)
    invented = Tally("invented numbers below zero, without being told")
    inv = b.inventions.get(Owing.LINE)
    invented.item("purse line", True, bool(inv and "down" in inv["primitives"]))
    pay = Tally("paying from purses of -40..40 with prices 10-60 (trained: -5..5, up to 8)")
    paid = Tally("getting paid into purses of -40..40, wages 10-60")
    for _ in range(30):
        inputs = {"purse": rng.randint(-40, 40), "price": rng.randint(10, 60)}
        pay.item(inputs, inputs["purse"] - inputs["price"], b.predict("pay", inputs),
                 b.memory.of("pay"), "purse_after", inputs)
        inputs = {"purse": rng.randint(-40, 40), "wage": rng.randint(10, 60)}
        paid.item(inputs, inputs["purse"] + inputs["wage"], b.predict("get_paid", inputs),
                  b.memory.of("get_paid"), "purse_after", inputs)
    words = Tally("questions with negative numbers, in marks and words")
    for _ in range(20):
        form = rng.randrange(4)
        x, y = rng.randint(0, 9), rng.randint(0, 9)
        if form == 0:
            q, t = f"{x} minus {x + y + 1}", -(y + 1)
        elif form == 1:
            q, t = f"-{x + 1} plus {y}", -(x + 1) + y
        elif form == 2:
            q, t = f"negative {NUMBER_WORDS[x + 1]} minus {y}", -(x + 1) - y
        else:
            q, t = f"what plus {x + y + 1} equals {x}", -(y + 1)
        words.item(q, str(t), reasoner.arithmetic(b, q).text)
    swap = Tally("adding a below-zero amount, reached by symmetry it checked ('5 plus -3')")
    for _ in range(10):
        x, y = rng.randint(1, 9), rng.randint(1, 9)
        q = f"{x} plus -{y}"
        swap.item(q, str(x - y), reasoner.arithmetic(b, q).text)
    undo = Tally("never experienced, reached by 'below-zero times = undo': "
                 "'5 minus -3', '-4 plus -2', '-2 times -3'")
    for _ in range(20):
        x, y = rng.randint(1, 9), rng.randint(1, 9)
        form = rng.randrange(4)
        if form == 0:
            q, t = f"{x} minus -{y}", x + y
        elif form == 1:
            q, t = f"-{x} plus -{y}", -x - y
        elif form == 2:
            q, t = f"-{x} times {y}", -x * y
        else:
            q, t = f"-{x} times -{y}", x * y
        undo.item(q, str(t), reasoner.arithmetic(b, q).text)
    refuse = Tally("still impossible: zero groups of anything is zero")
    for _ in range(10):
        q = f"what times 0 equals -{rng.randint(1, 50)}"
        refuse.item(q, REFUSE, reasoner.arithmetic(b, q).value)
    return _result(8, [invented, pay, paid, words, swap, undo, refuse], 0.99,
                   {"story": inv["story"] if inv else None})


# ---------------------------------------------------------------- lesson 9
def _frac(x):
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def exam_sharing(brain, seed=1010):
    from ..brain import amounts
    b, rng = copy.deepcopy(brain), random.Random(seed)
    invented = Tally("invented amounts between numbers (fractions), without being told")
    invented.item("cakes", True, amounts.invented(b))
    bal = Tally("balance: 20-120 pieces of cakes cut into 7-20, vs 3-10 cakes (trained: up "
                "to 12 pieces, cut into up to 6)")
    for _ in range(30):
        n, w = rng.randint(7, 20), rng.randint(3, 10)
        k = w * n if rng.random() < 0.5 else rng.randint(20, 120)
        inputs = {"pieces": k, "cut": n, "wholes": w}
        bal.item(inputs, k == w * n, b.predict("cake_balance", inputs),
                 b.memory.of("cake_balance"), "level", inputs)
    ask = lambda q: reasoner.arithmetic(b, q).text
    inv = Tally("'what times 3 equals -7': no whole answer, never taught fractions")
    for _ in range(15):
        y, x = rng.randint(2, 9), rng.randint(-30, 30)
        if x % y == 0:
            x += 1
        q = f"what times {y} equals {x}"
        inv.item(q, _frac(Fraction(x, y)), ask(q))
    div = Tally("'divided', learned from sharing cakes ('7 divided 2')")
    for _ in range(15):
        x, y = rng.randint(-20, 40), rng.randint(1, 9)
        q = f"{x} divided {y}"
        div.item(q, _frac(Fraction(x, y)), ask(q))
    ops = Tally("adding, taking away and multiplying amounts ('1/2 plus 1/3')")
    for _ in range(20):
        a = Fraction(rng.randint(-5, 9), rng.randint(1, 6))
        c = Fraction(rng.randint(-5, 9), rng.randint(1, 6))
        word, f = [("plus", lambda p, q: p + q), ("minus", lambda p, q: p - q),
                   ("times", lambda p, q: p * q)][rng.randrange(3)]
        q = f"{a.numerator}/{a.denominator} {word} {c.numerator}/{c.denominator}"
        ops.item(q, _frac(f(a, c)), ask(q))
    refuse = Tally("still impossible: zero groups, or a cake cut into 0 pieces")
    for _ in range(10):
        q = (f"what times 0 equals {rng.randint(1, 30)}" if rng.random() < 0.5
             else f"{rng.randint(1, 9)}/0 plus 1")
        refuse.item(q, REFUSE, reasoner.arithmetic(b, q).value)
    inv_rec = amounts.record(b)
    return _result(9, [invented, bal, inv, div, ops, refuse], 0.99,
                   {"story": inv_rec["story"] if inv_rec else None})


# ---------------------------------------------------------------- lesson 10
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
            q = f"what times 0 equals -{rng.randint(1, 99)}"
        elif form == 1:
            q = f"what is {rng.randint(10, 99)} modulo {rng.randint(2, 9)}"
        else:
            q = f"what times 0 equals {rng.randint(1, 99)}"
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

    return _result(10, [div, inv, chain, impossible, phys, back, phys_no, sky], 0.9)


# ================================================================ PHASE 2
def exam_wheel(brain, seed=1011):
    b, rng = copy.deepcopy(brain), random.Random(seed)
    inv = b.inventions.get("cycle:tick")
    invented = Tally("invented numbers that go round (a cycle), without being told")
    invented.item("wheel", 6, inv["size"] if inv else None)
    spin = Tally("spins of 1,000-1,000,000 ticks (trained: up to 8)")
    for _ in range(30):
        inputs = {"start": rng.randrange(6), "ticks": rng.randint(1000, 10 ** 6)}
        spin.item(inputs, (inputs["start"] + inputs["ticks"]) % 6, b.predict("spin", inputs),
                  b.memory.of("spin"), "end", inputs)
    ask = lambda q: reasoner.arithmetic(b, q)
    words = Tally("'17 after 4' in words")
    for _ in range(20):
        t, s0 = rng.randint(7, 200), rng.randrange(6)
        words.item(f"{t} after {s0}", str((s0 + t) % 6), ask(f"{t} after {s0}").text)
    back = Tally("going backwards: '-2 after 3' (never experienced)")
    for _ in range(10):
        t, s0 = rng.randint(1, 30), rng.randrange(6)
        back.item(f"-{t} after {s0}", str((s0 - t) % 6), ask(f"-{t} after {s0}").text)
    inverse = Tally("'what after 4 equals 1' (the nearest answer)")
    for _ in range(10):
        s0, e = rng.randrange(6), rng.randrange(6)
        d = (e - s0) % 6
        best = min((d, d - 6), key=lambda x: (abs(x), -x))
        inverse.item(f"what after {s0} equals {e}", str(best),
                     ask(f"what after {s0} equals {e}").text)
    refuse = Tally("impossible: a position that isn't on the wheel")
    for _ in range(10):
        v = rng.choice([rng.randint(6, 30), -rng.randint(1, 9)])
        q = (f"{rng.randint(1, 9)} after {v}" if rng.random() < 0.5
             else f"what after {v} equals {rng.randrange(6)}")
        refuse.item(q, REFUSE, ask(q).value)
    return _result(11, [invented, spin, words, back, inverse, refuse], 0.99,
                   {"story": inv["story"] if inv else None,
                    "tick_law": show_law(b, "tick")})


def exam_ramps(brain, seed=1012):
    from ..env.physics import Track
    b, rng = copy.deepcopy(brain), random.Random(seed)
    world = Track(seed, prefix="Exam")
    invented = Tally("invented a hidden quantity shared by height and speed")
    invented.item("ramps", True, "hidden:roll" in b.inventions)
    high = Tally("runs 10-50 m high (trained: 1-5 m): speed, after one look at the release",
                 tol=0.01)
    climb = Tally("NEVER TRAINED: how high does it climb on the far side?", tol=0.01)
    throw = Tally("NEVER TRAINED: a ball thrown straight up at 5-40 m/s: how high?", tol=0.01)
    refuse = Tally("impossible: its speed at a height above where it was let go")
    for _ in range(10):
        h, m = rng.uniform(10, 50), rng.uniform(1, 9)
        run = world.new_run(h, m)
        b.experience("roll", {"y": h, "m": m, "run": run}, 0.0)
        for _ in range(3):
            y = rng.uniform(0, h)
            inputs = {"y": y, "m": m, "run": run}
            high.item(inputs, world.speed_at(y), b.predict("roll", inputs),
                      b.memory.of("roll"), "v", inputs)
        ans = reasoner.physics(b, "y", {"v": 0.0}, {"run": run})
        climb.item(run, h, ans.value)
        refuse.item(run, REFUSE, b.predict("roll", {"y": h * 1.5, "m": m, "run": run}))
    for _ in range(10):
        u = rng.uniform(5, 40)
        run = world.new_run(u * u / (2 * world.G), 1.0)
        b.experience("roll", {"y": 0.0, "m": 1.0, "run": run}, u)
        ans = reasoner.physics(b, "y", {"v": 0.0}, {"run": run})
        throw.item(u, u * u / (2 * world.G), ans.value)
    inv = b.inventions.get("hidden:roll")
    return _result(12, [invented, high, climb, throw, refuse], 0.99,
                   {"story": inv["story"] if inv else None})


def exam_growing(brain, seed=1013):
    b, rng = copy.deepcopy(brain), random.Random(seed)
    ladder = b.inventions.get("ladder", {})
    predicted_at = next((e["lesson"] for e in b.log if e["kind"] == "invent"
                         and "repeated_groups" in e["text"]), None)
    foresight = Tally("predicted this law from a pattern in its own laws, lessons before "
                      "meeting it")
    foresight.item("REPEAT", True, predicted_at is not None and predicted_at < 13)
    right = Tally("the world confirmed the prediction")
    law = b.library.get("repeated_groups")
    right.item("repeated_groups", True, bool(law) and not law.provenance.get("predicted"))
    grow = Tally("5-10 days of splitting into 2-6 (trained: up to 4 days, 4-way splits)")
    for _ in range(30):
        inputs = {"split": rng.randint(2, 6), "days": rng.randint(5, 10)}
        grow.item(inputs, inputs["split"] ** inputs["days"], b.predict("grow", inputs),
                  b.memory.of("grow"), "cells", inputs)
    words = Tally("'3 power 4' in words")
    for _ in range(15):
        x, y = rng.randint(2, 9), rng.randint(0, 6)
        words.item(f"{x} power {y}", str(x ** y), reasoner.arithmetic(b, f"{x} power {y}").text)
    stop = Tally("sees that REPEAT can't say what comes after powers, and doesn't guess")
    stop.item("next rung", True, ladder.get("stops_at") == "repeated_groups"
              and len(ladder.get("predicted", [])) == 1)
    return _result(13, [foresight, right, grow, words, stop], 0.99,
                   {"story": ladder.get("story"), "search_steps": b.search_steps.get("grow")})


def exam_phase2(brain, seed=1014):
    from ..env.physics import Track
    b, rng = copy.deepcopy(brain), random.Random(seed)
    ask = lambda q: reasoner.arithmetic(b, q).text
    roots = Tally("square and cube roots, never taught ('what power 2 equals 81')")
    for _ in range(12):
        x, p = rng.randint(-12, 12), rng.choice([2, 3])
        if p == 2:
            x = abs(x)
        q = f"what power {p} equals {x ** p}"
        want = abs(x) if p == 2 else x
        roots.item(q, str(want), ask(q))
    logs = Tally("logarithms, never taught ('2 power what equals 1024')")
    for _ in range(12):
        base, e = rng.randint(2, 6), rng.randint(0, 8)
        q = f"{base} power what equals {base ** e}"
        logs.item(q, str(e), ask(q))
    neg = Tally("negative powers and powers of fractions ('3 power -2', '2/3 power 3')")
    for _ in range(12):
        if rng.random() < 0.5:
            base, e = rng.randint(2, 5), -rng.randint(1, 3)
            q, t = f"{base} power {e}", Fraction(base) ** e
        else:
            fr = Fraction(rng.randint(1, 4), rng.randint(2, 5))
            e = rng.randint(1, 3)
            q, t = f"{fr.numerator}/{fr.denominator} power {e}", fr ** e
        neg.item(q, _frac(t), ask(q))
    clock = Tally("clock numbers with huge backward spins ('-1000 after 2')")
    for _ in range(10):
        t, s0 = rng.randint(100, 100000), rng.randrange(6)
        clock.item(f"-{t} after {s0}", str((s0 - t) % 6), ask(f"-{t} after {s0}"))
    chains = Tally("chains of fractions ('1/2 plus 1/3 plus 1/6')")
    for _ in range(10):
        parts = [Fraction(rng.randint(1, 5), rng.randint(2, 6)) for _ in range(3)]
        q = " plus ".join(f"{p.numerator}/{p.denominator}" for p in parts)
        chains.item(q, _frac(sum(parts)), ask(q))
    drop = Tally("energy: a ball dropped from 2-80 m, speed at the ground", tol=0.01)
    world = Track(seed, prefix="Drop")
    for _ in range(10):
        h = rng.uniform(2, 80)
        run = world.new_run(h, 1.0)
        b.experience("roll", {"y": h, "m": 1.0, "run": run}, 0.0)
        ans = reasoner.physics(b, "v", {"y": 0.0}, {"run": run})
        drop.item(h, world.speed_at(0.0), ans.value)
    irrational = Tally("'what power 2 equals 2': no fraction works; pinned in a gap of its line "
                       "(to within 1/20)", tol=0.05)
    for n in (2, 3, 5, 7, 8):
        irrational.item(n, n ** 0.5, reasoner.arithmetic(b, f"what power 2 equals {n}").value)
    return _result(16, [roots, logs, neg, clock, chains, drop, irrational], 0.99)


def exam_springy(brain, seed=1015):
    from ..env.physics import SpringTrack
    b, rng = copy.deepcopy(brain), random.Random(seed)
    world = SpringTrack(seed, prefix="ExamS")
    inv = b.inventions.get("hidden:bounce")
    invented = Tally("invented a hidden quantity with THREE parts: height, speed, squash")
    invented.item("spring", ["c^2", "v^2", "y"], sorted(inv["terms"]) if inv else None)
    speed = Tally("runs 10-40 m high (trained: 1-5 m): speed on the hills and in the spring",
                  tol=0.01)
    squash = Tally("NEVER TRAINED: how far will the spring squash?", tol=0.01)
    launch = Tally("NEVER TRAINED: a ball pushed off a squashed spring: how high does it go?",
                   tol=0.01)
    refuse = Tally("impossible: its speed with the spring squashed further than it can be")
    for _ in range(10):
        h = rng.uniform(10, 40)
        run = world.new_run(h, world.MASS)
        b.experience("bounce", {"y": h, "c": 0.0, "run": run}, 0.0)
        for y, c in ((rng.uniform(0, h), 0.0), (0.0, rng.uniform(0, world.max_squash()))):
            inputs = {"y": y, "c": c, "run": run}
            speed.item(inputs, world.speed(y, c), b.predict("bounce", inputs),
                       b.memory.of("bounce"), "v", inputs)
        ans = reasoner.physics(b, "c", {"y": 0.0, "v": 0.0}, {"run": run})
        squash.item(run, world.max_squash(), ans.value)
        refuse.item(run, REFUSE, b.predict("bounce", {"y": 0.0, "c": world.max_squash() * 1.3,
                                                       "run": run}))
    for _ in range(10):
        c0 = rng.uniform(0.2, 1.5)
        height = world.STIFFNESS * c0 ** 2 / (2 * world.MASS * world.G)
        run = world.new_run(height, world.MASS)
        b.experience("bounce", {"y": 0.0, "c": c0, "run": run}, 0.0)
        ans = reasoner.physics(b, "y", {"v": 0.0, "c": 0.0}, {"run": run})
        launch.item(c0, height, ans.value)
    return _result(14, [invented, speed, squash, launch, refuse], 0.99,
                   {"story": inv["story"] if inv else None})


def exam_diagonal(brain, seed=1016):
    from ..env.toyworld import Tiles
    from ..brain import gaps
    b, rng = copy.deepcopy(brain), random.Random(seed)
    world = Tiles(seed)
    first = next((e["lesson"] for e in b.log if e["kind"] == "invent"
                  and "GAPS" in e["text"]), None)
    invented = Tally("invented numbers in the gaps of its line by reasoning, before this lesson")
    invented.item("gaps", True, first is not None and first < 15)
    diag = Tally("concluded the diagonal is the gap number whose square is 2 tiles")
    idea = b.quantities.get("diagonal")
    diag.item("diagonal", [2, 1], idea and idea.get("goal"))
    ruler = Tally("rulers never used (31-300 marks): the reading, predicted before measuring")
    for _ in range(10):
        m = rng.randint(31, 300)
        ruler.item({"marks": m}, world.ruler_reading(m), b.predict("ruler", {"marks": m}),
                   b.memory.of("ruler"), "diagonal", {"marks": m})
    roots = Tally("square roots of non-squares, pinned in a gap (to within 1/20)", tol=0.05)
    for _ in range(10):
        n = rng.randint(2, 60)
        while int(n ** 0.5) ** 2 == n:
            n += 1
        roots.item(n, n ** 0.5, reasoner.arithmetic(b, f"what power 2 equals {n}").value)
    cubes = Tally("cube roots of non-cubes, pinned in a gap (to within 1/10)", tol=0.1)
    for n in (2, 3, 5):
        cubes.item(n, n ** (1 / 3), reasoner.arithmetic(b, f"what power 3 equals {n}").value)
    refuse = Tally("still impossible: zero groups of anything is zero")
    for n in (5, 12):
        refuse.item(n, REFUSE, reasoner.arithmetic(b, f"what times 0 equals {n}").value)
    inv = b.inventions.get("gaps")
    return _result(15, [invented, diag, ruler, roots, cubes, refuse], 0.99,
                   {"story": inv["story"] if inv else None})


# ================================================================ PHASE 3
def exam_coils(brain, seed=1017):
    from ..env.physics import CoilShop
    b, rng = copy.deepcopy(brain), random.Random(seed)
    world = CoilShop(seed, prefix="New")
    meta = b.qlaws.get("coil_stretch~why")
    found = Tally("found a law about its own stiffness law (stiffness × coils)")
    found.item("why", {"coil_stretch.property": 1, "coils": 1}, meta.powers if meta else None)
    never = Tally("springs NEVER stretched: pull predicted from counting coils alone", tol=0.01)
    chain = Tally("NEVER TRAINED: how many coils for a spring that pulls F at stretch x?",
                  tol=0.01)
    for _ in range(15):
        spring = world.new_spring(rng.randint(2, 30))
        coils = len(world.count_coils(spring))
        b.experience("coil_look", {"spring": spring}, coils)
        x = round(rng.uniform(0.05, 2.0), 3)
        inputs = {"x": x, "spring": spring}
        never.item(inputs, world.stretch(spring, x), b.predict("coil_stretch", inputs),
                   b.memory.of("coil_stretch"), "F", inputs)
    for _ in range(10):
        coils = rng.randint(2, 40)
        x = round(rng.uniform(0.05, 2.0), 3)
        F = world.WIRE / coils * x
        ans = reasoner.physics(b, "coils", {"F": F, "x": x}, {"spring": "Unseen"})
        chain.item((F, x), float(coils), ans.value)
    inv = b.inventions.get("why:coil_stretch")
    return _result(17, [found, never, chain], 0.99, {"story": inv["story"] if inv else None})


def exam_phase3(brain, seed=1018):
    b, rng = copy.deepcopy(brain), random.Random(seed)
    ask = lambda q: reasoner.arithmetic(b, q)
    big = Tally("huge numbers, exact (column arithmetic): 12-20 digits")
    for _ in range(10):
        x, y = rng.randint(10 ** 11, 10 ** 20), rng.randint(10 ** 5, 10 ** 12)
        word, f = [("times", lambda p, q: p * q), ("plus", lambda p, q: p + q),
                   ("minus", lambda p, q: p - q)][rng.randrange(3)]
        big.item(f"{x} {word} {y}", str(f(x, y)), ask(f"{x} {word} {y}").text)
    powers = Tally("big powers, exact ('3 power 40')")
    for _ in range(6):
        a, n = rng.randint(2, 9), rng.randint(20, 60)
        powers.item(f"{a} power {n}", str(a ** n), ask(f"{a} power {n}").text)
    logs = Tally("logarithms with no fraction answer, pinned in a gap (to within 1/50)",
                 tol=0.02)
    import math
    for _ in range(6):
        a, n = rng.randint(2, 9), rng.randint(2, 20)
        while round(math.log(n, a)) == math.log(n, a) or a ** round(math.log(n, a)) == n:
            n += 1
        logs.item(f"{a} power what equals {n}", math.log(n, a),
                  ask(f"{a} power what equals {n}").value)
    frac = Tally("fractional powers ('8 power 2/3', '2 power 1/2')", tol=0.02)
    for base, p, q in ((8, 2, 3), (27, 1, 3), (16, 3, 4), (2, 1, 2), (10, 1, 2), (5, 2, 3)):
        truth = base ** (p / q)
        v = ask(f"{base} power {p}/{q}").value
        if isinstance(v, tuple) and v and v[0] != "between":
            v = v[0] / v[1]
            frac.item(f"{base}^{p}/{q}", round(truth), round(v) if abs(v - round(v)) < 1e-9 else v)
        else:
            frac.item(f"{base}^{p}/{q}", truth, v)
    impossible = Tally("still impossible: 'what times 0 equals 5', '3 power what equals -1'")
    for q in ("what times 0 equals 5", "3 power what equals -1", "what times 0 equals -2"):
        impossible.item(q, REFUSE, ask(q).value)
    return _result(18, [big, powers, logs, frac, impossible], 0.99)


def compression_benefit(upto=13):
    """Growing lesson with and without compression: how much searching did it take?"""
    from ..trainer.trainer import Trainer
    out = {}
    for mode in ("compressing", "not compressing"):
        brain = Brain(mode)
        brain.compress = mode == "compressing"
        trainer = Trainer(brain)
        for n in range(upto + 1):
            trainer.run(n)
        law = brain.library.get("grow")
        out[mode] = {"programs_searched": brain.search_steps.get("grow", 0),
                     "found_after": law.provenance.get("found_after") if law else None,
                     "passed": trainer.results[13]["passed"]}
    return out


def show_law(brain, name):
    from ..brain.dsl import show as show_expr
    law = brain.library.get(name)
    return show_expr(law.expr) if law else None


# ---------------------------------------------------------------- Phase 3: senses
def exam_eyes(brain, seed=1019):
    import numpy as np
    from ..senses.eyes import Eyes
    from ..senses.world import Trays
    b = copy.deepcopy(brain)
    trays = Trays(seed)
    rng = np.random.default_rng(seed)
    learned = Tally("learned its eyes from touch (a neural network, 3 conv layers)")
    learned.item("eyes", True, b.eyes is not None and b.eyes.trained_on > 0)
    count = Tally("counts NEW trays of 0-30 things from noisy pixels (looking again when unsure)")
    big = Tally("NEVER PRACTISED: trays of 31-50 things in a bigger picture")
    glances = []
    blank = Eyes(seed=seed)         # the same network before any learning
    blank_right = 0
    for _ in range(60):
        n = int(rng.integers(0, 31))
        look = trays.tray(n)
        c, g = b.eyes.count(look)
        glances.append(g)
        count.item(n, n, c)
        blank_right += blank.count(look)[0] == n
    for _ in range(20):
        n = int(rng.integers(31, 51))
        big.item(n, n, b.eyes.count(trays.tray(n))[0])
    where = Tally("finds where each thing is, to within half a pixel")
    for _ in range(30):
        img, touch = trays.handle(int(rng.integers(1, 15)))
        seen = b.eyes.see(img)
        for x, y in touch:
            d = min(((sx - x) ** 2 + (sy - y) ** 2) ** 0.5 for sx, sy, _ in seen) if seen else 9
            where.add("ultron", d <= 0.5, True)
    inv = b.inventions.get("eyes")
    return _result(19, [learned, count, big, where], 0.95,
                   {"story": inv["story"] if inv else None,
                    "mean_glances": sum(glances) / len(glances),
                    "untrained_network_right": f"{blank_right}/60"})


def exam_seeing_numbers(brain, seed=1020):
    import numpy as np
    from ..senses.world import Trays
    b = copy.deepcopy(brain)
    trays = Trays(seed)
    rng = np.random.default_rng(seed)
    same = Tally("recognised that what it sees obeys the addition and subtraction it knows")
    same.item("see_merge", True, b.library.get("see_merge") is not None)
    same.item("see_take", True, b.library.get("see_take") is not None)
    add = Tally("PICTURES of trays of 5-25 things: how many together? (played with up to 12)")
    take = Tally("PICTURES: a tray of 10-25, some taken away: how many left?")
    for _ in range(25):
        a, c = int(rng.integers(5, 26)), int(rng.integers(5, 26))
        inputs = {"nA": b.eyes.count(trays.tray(a))[0], "nB": b.eyes.count(trays.tray(c))[0]}
        add.item(inputs, a + c, b.predict("see_merge", inputs), b.memory.of("see_merge"),
                 "total", inputs)
        a = int(rng.integers(10, 26))
        t = int(rng.integers(0, a + 1))
        inputs = {"nA": b.eyes.count(trays.tray(a))[0], "n_taken": b.eyes.count(trays.tray(t))[0]}
        take.item(inputs, a - t, b.predict("see_take", inputs), b.memory.of("see_take"),
                  "left", inputs)
    laws = {n: show(b.library.get(n).expr) for n in ("see_merge", "see_take")
            if b.library.get(n)}
    return _result(20, [same, add, take], 0.95, {"laws": laws})


def exam_watching(brain, seed=1021):
    from ..senses.world import G, HillTrack, PushTable
    from ..trainer.senses_lessons import WatchingMotion
    from ..trainer.trainer import free_play
    b = copy.deepcopy(brain)
    lesson = WatchingMotion(seed)
    lesson.brain = b
    found = Tally("rediscovered F = m·a, stiffness and energy from video alone")
    push = b.qlaws.get("see_push")
    found.item("F=ma", True, bool(push) and push.powers == {"F": 1, "a": -1, "m": -1}
               and abs(push.constant - 1) < 0.02)
    st = b.qlaws.get("see_stretch")
    found.item("stiffness", True, bool(st) and st.kind == "grouped"
               and st.powers == {"W": 1, "x": -1})
    roll = b.qlaws.get("see_roll")
    found.item("energy", True, isinstance(roll, SumLaw) and roll.a == {"y": 1}
               and roll.b == {"v": 2} and abs(roll.coef * 2 * G - 1) < 0.03)
    # the same, starting from a blank brain that has only these eyes
    fresh = Brain("blank")
    fresh.eyes = b.eyes
    fresh_lesson = WatchingMotion(seed + 1)
    fresh_lesson.brain = fresh
    for spec in fresh_lesson.specs():
        fresh.meet(spec)
    free_play(fresh, fresh_lesson, fresh_lesson.budget)
    fp, fs, fr = (fresh.qlaws.get(n) for n in ("see_push", "see_stretch", "see_roll"))
    blank = Tally("a BLANK brain with only these eyes rediscovers all three too")
    blank.item("F=ma", True, bool(fp) and fp.powers == {"F": 1, "a": -1, "m": -1})
    blank.item("stiffness", True, bool(fs) and fs.powers == {"W": 1, "x": -1})
    blank.item("energy", True, isinstance(fr, SumLaw) and fr.b == {"v": 2})
    pushes = Tally("new pushes: acceleration predicted BEFORE watching, vs the true one",
                   tol=0.03)
    table = PushTable(seed)
    rng = random.Random(seed)
    for _ in range(12):
        F, blocks = rng.randint(1, 20), rng.randint(1, 9)
        m, _ = b.eyes.count(table.load(blocks))
        inputs = {"F": float(F), "m": float(m)}
        pushes.item(inputs, PushTable.truth(F, blocks), b.predict("see_push", inputs),
                    b.memory.of("see_push"), "a", inputs)
    hang = Tally("NEVER HUNG: 4-5 blocks on its springs; how far will each stretch?", tol=0.04)
    stand = WatchingMotion(seed=21).stand     # the springs it played with (Judge's truth)
    for spring in sorted(st.properties) if st else []:
        for blocks in (4, 5):
            hang.item((spring, blocks), stand.extension(spring, blocks),
                      st.solve("x", {"W": float(blocks)}, spring))
    hills = Tally("new balls in the valley: after watching a moment, the speed at every "
                  "later height", tol=0.05)
    from ..senses import measure
    track = HillTrack(seed, prefix="ExamHill")
    for release in (0.15, 0.45, 0.8, 1.05):
        run, pics, truth, fps = track.film(release)
        # heights are read up from the lowest ruler mark, which is the valley floor
        first = measure.path_samples(b.eyes, pics[:14], fps)[:1]
        for y, v, sy, sv in first:
            b.experience("see_roll", {"y": y, "run": run, "±y": sy, "±v": sv}, v)
        law = b.qlaws.get("see_roll")
        for x, y, v in truth[20::8]:
            got = law.solve("v", {"y": y}, run) if isinstance(law, SumLaw) else None
            if v > 0.5:
                hills.item((run, round(y, 2)), v, got)
    return _result(21, [found, blank, pushes, hang, hills], 0.9,
                   {"push_law": push.formula() if push else None,
                    "energy_law": roll.formula() if roll else None,
                    "blank_brain_laws": sorted(fresh.qlaws)})


# ---------------------------------------------------------------- Phase 3: new kinds
def _watch(b, spec_name, world, obj, xs):
    """Ultron watches the first readings of a new object (this is allowed to teach the
    exam copy about that one object, as looking at a new cup would)."""
    spec = b.memory.specs[spec_name]
    for x in xs:
        b.experience(spec_name, {spec.order_by: x, spec.group_by: obj}, world.read(obj, x))


def _ablated_fails(brain, spec_name):
    """The same brain, with every invented kind and law removed and inventing switched
    off, relearns from the same readings: can it explain them?"""
    b = copy.deepcopy(brain)
    b.kinds, b.slaws, b.inventing = {}, {}, False
    b.kind_steps.pop(spec_name, None)
    b._learn_sequence(b.memory.specs[spec_name], True)
    return spec_name not in b.slaws


def _scratch_steps(brain, spec_name, reuse=False):
    """What explaining this world costs on the same readings: searching the whole
    grammar from scratch, or (reuse=True) trying its invented kinds first."""
    from ..brain import kinds
    spec = brain.memory.specs[spec_name]
    seqs = kinds.sequences(brain.memory.of(spec_name), spec.target, spec.order_by,
                           spec.group_by)
    templates = ([k["template"] for k in kinds.learned(brain)] if reuse
                 else kinds.grammar())
    _, steps = kinds.search(seqs, max(spec.tol, 1e-9) + 4 * spec.precision, templates,
                            budget=10 ** 9)
    return steps


def exam_cooling(brain, seed=1022):
    from ..env.sequences import CoolingCups
    b, rng = copy.deepcopy(brain), random.Random(seed)
    world = CoolingCups(seed, prefix="ExamCup")
    invented = Tally("invented a new KIND of explanation (none of its innate kinds fit)")
    invented.item("cool", True, "kind:cool" in b.inventions)
    ablation = Tally("the same brain without inventing kinds can't explain cooling at all")
    ablation.item("cool", True, _ablated_fails(b, "cool"))
    future = Tally("new cups, after 3 looks: the temperature 3-20 minutes on", tol=0.01)
    room = Tally("NEVER MEASURED: the room's temperature (where a cup settles)", tol=0.02)
    for _ in range(10):
        cup = world.new_cup()
        _watch(b, "cool", world, cup, [0, 1, 2])
        for t in sorted(rng.sample(range(3, 21), 4)):
            inputs = {"t": t, "cup": cup}
            future.item(inputs, world.read(cup, t), b.predict("cool", inputs),
                        b.memory.of("cool"), "T", inputs)
        law = b.slaws.get("cool")
        rest = law.resting_value(b.history(b.memory.specs["cool"], cup), cup) if law else None
        room.item(cup, world.room(cup), rest)
    inv = b.inventions.get("kind:cool")
    return _result(22, [invented, ablation, future, room], 0.95,
                   {"story": inv["story"] if inv else None,
                    "effort": dict(b.kind_steps.get("cool", {}))})


def exam_settling(brain, seed=1023):
    from ..env.sequences import Batteries, BouncingBalls, Candles, HangingSprings
    b, rng = copy.deepcopy(brain), random.Random(seed)
    reused = Tally("REUSED its invented 'settling' kind for bounces and batteries, and its "
                   "'equal steps' kind for candles (no new kind invented)")
    for name in ("bounces", "charge", "burn"):
        reused.item(name, True, name in b.slaws and f"kind:{name}" not in b.inventions)
    second = Tally("invented a second kind where the first didn't fit (spring lengths)")
    second.item("hang", True, "kind:hang" in b.inventions)
    cheaper = Tally("on the same readings, trying its invented kinds first never takes more "
                    "search than the whole grammar, and takes less for bounces and batteries")
    for name in ("bounces", "charge", "burn"):
        mine, scratch = _scratch_steps(b, name, reuse=True), _scratch_steps(b, name)
        cheaper.item(name, True, mine < scratch if name != "burn" else mine <= scratch)
    noise = Tally("the randomly blown marker, even after watching 8 more walks of 20 "
                  "steps: explained by nothing, and no kind invented for it")
    from ..env.sequences import Wanderers
    walkers = Wanderers(seed, prefix="ExamWalker")
    for _ in range(8):
        _watch(b, "wander", walkers, walkers.new_walker(), list(range(20)))
    noise.item("wander", True, "wander" not in b.slaws and "kind:wander" not in b.inventions)
    bounce = Tally("new balls, after 3 bounces: heights of bounces 3-8", tol=0.01)
    balls = BouncingBalls(seed, prefix="ExamBall")
    for _ in range(8):
        ball = balls.new_ball()
        _watch(b, "bounces", balls, ball, [0, 1, 2])
        for k in (3, 5, 8):
            inputs = {"k": k, "ball": ball}
            bounce.item(inputs, balls.read(ball, k), b.predict("bounces", inputs),
                        b.memory.of("bounces"), "h", inputs)
    full = Tally("NEVER MEASURED: a new battery's full charge, after 3 readings", tol=0.02)
    bats = Batteries(seed, prefix="ExamBattery")
    for _ in range(8):
        bat = bats.new_battery()
        _watch(b, "charge", bats, bat, [0, 1, 2])
        law = b.slaws.get("charge")
        got = law.resting_value(b.history(b.memory.specs["charge"], bat), bat) if law else None
        full.item(bat, bats.hidden[bat]["full"], got)
    hang = Tally("new springs, after 2 weights: length with other weights", tol=0.01)
    rest = Tally("NEVER MEASURED: a spring's unstretched length", tol=0.01)
    springs = HangingSprings(seed, prefix="ExamCoil")
    for _ in range(8):
        sp = springs.new_spring()
        _watch(b, "hang", springs, sp, [2.0, 10.0])
        for F in (5.0, 20.0, 40.0):
            inputs = {"F": F, "spring": sp}
            hang.item(inputs, springs.read(sp, F), b.predict("hang", inputs),
                      b.memory.of("hang"), "L", inputs)
        rest.item(sp, springs.hidden[sp]["rest"], b.predict("hang", {"F": 0.0, "spring": sp}))
    burn = Tally("NEVER TRAINED: when will a new candle burn out? (after 2 looks)", tol=0.02)
    candles = Candles(seed, prefix="ExamCandle")
    for _ in range(8):
        c = candles.new_candle()
        _watch(b, "burn", candles, c, [0, rng.randint(2, 6)])
        law = b.slaws.get("burn")
        got = None
        if law is not None:
            xs, ys = b.history(b.memory.specs["burn"], c)
            slope = law.value_for(c, (xs, ys))
            got = xs[-1] - ys[-1] / slope if slope else None
        h = candles.hidden[c]
        burn.item(c, h["tall"] / h["rate"], got)
    return _result(23, [reused, second, cheaper, noise, bounce, full, hang, rest, burn], 0.95,
                   {"effort": {n: dict(b.kind_steps.get(n, {})) for n in
                               ("bounces", "charge", "hang", "burn", "wander")},
                    "scratch": {n: _scratch_steps(b, n) for n in ("bounces", "charge", "burn")
                                if n in b.slaws},
                    "reuse": {n: _scratch_steps(b, n, reuse=True)
                              for n in ("bounces", "charge", "burn") if n in b.slaws}})


# ---------------------------------------------------------------- Phase 3: acting
def _goals(b, floor, n, rng, lesson, floors, tries=2):
    """Painted marks to stop on. Returns (first-try hits, hits within `tries`, traces)."""
    from ..brain.body import reach
    from ..senses import measure
    first, hit, traces = 0, 0, []
    for _ in range(n):
        want_true = rng.uniform(0.8, 3.5)
        # Ultron sees the goal: where is the mark, measured from the start?
        start, _ = measure.position(b.eyes, floors.before(), measure.BOTTOM)
        mark, _ = measure.position(b.eyes, floors.goal(want_true), measure.BOTTOM)
        want = mark - start
        out = reach(b, "slide", "u", "d", want,
                    lambda u: lesson.watch_kick(floor, u, floors), place=floor, tries=tries)
        # the Judge checks where the puck REALLY stopped against where the mark REALLY is
        first += out["hit"] and out["tries"] == 1
        hit += out["hit"]
        if len(traces) < 2:
            traces.append(out["trace"])
    return first, hit, traces


def exam_acting(brain, seed=1024):
    from ..senses.world import Floors
    from ..trainer.senses_lessons import UsingWhatItKnows
    b, rng = copy.deepcopy(brain), random.Random(seed)
    lesson = UsingWhatItKnows(seed)
    lesson.brain = b
    floors = Floors(seed)
    law = Tally("found how far a kicked puck slides (distance / speed² fixed on a floor)")
    slide = b.qlaws.get("slide")
    law.item("slide", True, bool(slide) and slide.powers == {"d": 1, "u": -2})
    wood = Tally("goals on WOOD (the floor it played on): stopped within 10 cm, first try")
    carpet = Tally("goals on CARPET (never touched): a cautious first kick, then within 10 "
                   "cm on the second try")
    f1, h1, t1 = _goals(b, "wood", 12, rng, lesson, floors)
    f2, h2, t2 = _goals(b, "carpet", 12, rng, lesson, floors)
    for i in range(12):
        wood.add("ultron", i < f1, True)
        carpet.add("ultron", i < h2, True)
    # a body without understanding: kicks at random within what it tried in play
    lucky = 0
    for _ in range(200):
        want, u = rng.uniform(0.8, 3.5), rng.uniform(1.0, 3.8)
        lucky += abs(floors.distance("wood", u) - want) <= 0.1
    return _result(24, [law, wood, carpet], 0.9,
                   {"carpet_first_try": f"{f2}/12", "random_kicks_hit": f"{lucky / 200:.0%}",
                    "traces": t1[:1] + t2[:1]})


def exam_phase3_senses(brain, seed=1025):
    import numpy as np
    from ..brain import kinds
    from ..env.sequences import DrainingTanks
    from ..senses.world import Floors, PushTable, Trays
    from ..trainer.senses_lessons import UsingWhatItKnows
    b, rng = copy.deepcopy(brain), random.Random(seed)
    trays = Trays(seed)
    nrng = np.random.default_rng(seed)
    sees = Tally("counts trays of 0-50 things from pixels")
    for _ in range(20):
        n = int(nrng.integers(0, 51))
        sees.item(n, n, b.eyes.count(trays.tray(n))[0])
    motion = Tally("predicts a push's acceleration BEFORE watching, counting the load by eye",
                   tol=0.03)
    table = PushTable(seed)
    for _ in range(10):
        F, blocks = rng.randint(2, 30), rng.randint(1, 12)
        m, _ = b.eyes.count(table.load(blocks))
        motion.item((F, blocks), F / blocks, b.predict("see_push", {"F": float(F),
                                                                    "m": float(m)}))
    # a world never met: draining tanks
    tanks = DrainingTanks(seed)
    from ..brain.memory import Spec
    spec = Spec("drain", "sequence", {"t": None}, "h", group_by="tank", order_by="t",
                tol=0.01, surprise=0.005)
    b.meet(spec)
    for _ in range(5):
        _watch(b, "drain", tanks, tanks.new_tank(), list(range(8)))
    new_world = Tally("a NEW world (draining tanks): explained on first meeting by a kind of "
                      "explanation it invented lessons earlier, no new search needed")
    eff = b.kind_steps.get("drain", {})
    new_world.item("drain", True, "drain" in b.slaws and not eff.get("invent")
                   and "kind:drain" not in b.inventions)
    drain = Tally("new tanks after 3 readings: level 3-15 minutes on", tol=0.01)
    for _ in range(6):
        tank = tanks.new_tank()
        _watch(b, "drain", tanks, tank, [0, 1, 2])
        for t in (3, 8, 15):
            inputs = {"t": t, "tank": tank}
            drain.item(inputs, tanks.read(tank, t), b.predict("drain", inputs),
                       b.memory.of("drain"), "h", inputs)
    hole = Tally("NEVER MEASURED: how high the hole is (where the water stops), after 6 "
                 "readings, to within 5 mm", abs_tol=0.005)
    for _ in range(6):
        tank = tanks.new_tank()
        _watch(b, "drain", tanks, tank, list(range(6)))
        law = b.slaws.get("drain")
        rest = law.resting_value(b.history(spec, tank), tank) if law else None
        hole.item(tank, tanks.hidden[tank]["hole"], rest)
    ablation = Tally("the same brain with its invented kinds removed can't explain the tanks")
    ablation.item("drain", True, _ablated_fails(b, "drain"))
    lesson = UsingWhatItKnows(seed)
    lesson.brain = b
    ice = Tally("goals on ICE (never touched): a cautious first kick, then within 10 cm on "
                "the second try")
    _, h, traces = _goals(b, "ice", 10, rng, lesson, Floors(seed))
    for i in range(10):
        ice.add("ultron", i < h, True)
    return _result(25, [sees, motion, new_world, drain, hole, ablation, ice], 0.9,
                   {"drain_effort": dict(eff), "drain_scratch": _scratch_steps(b, "drain"),
                    "ice_trace": traces[:1]})


EXAMS = {0: exam_permanence, 1: exam_pairing, 2: exam_combining, 3: exam_groups,
         4: exam_language, 5: exam_mechanics, 6: exam_real_data, 7: exam_noisy_lab,
         8: exam_owing, 9: exam_sharing, 10: exam_final, 11: exam_wheel, 12: exam_ramps,
         13: exam_growing, 14: exam_springy, 15: exam_diagonal, 16: exam_phase2,
         17: exam_coils, 18: exam_phase3, 19: exam_eyes, 20: exam_seeing_numbers,
         21: exam_watching, 22: exam_cooling, 23: exam_settling, 24: exam_acting,
         25: exam_phase3_senses}
