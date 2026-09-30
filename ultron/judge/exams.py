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
    def __init__(self, name, tol=None):
        self.name = name
        self.tol = tol
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


EXAMS = {0: exam_permanence, 1: exam_pairing, 2: exam_combining, 3: exam_groups,
         4: exam_language, 5: exam_mechanics, 6: exam_real_data, 7: exam_noisy_lab,
         8: exam_owing, 9: exam_sharing, 10: exam_final, 11: exam_wheel, 12: exam_ramps,
         13: exam_growing, 14: exam_springy, 15: exam_diagonal, 16: exam_phase2}
