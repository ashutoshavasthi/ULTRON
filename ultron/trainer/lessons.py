"""The curriculum. Each lesson gives Ultron things to play with and, sometimes,
words for what it has already understood. A lesson never contains a law:
scenes are set up in a world, and the world does what it does.

The `goal` text is for humans reading the reports; Ultron never sees it.
"""

from ..brain.dsl import BOOL, INT, LIST
from ..brain.memory import Spec
from ..brain.perception import count, present, read_marks
from ..env import dataworld
from ..env.physics import CoilShop, PhysicsSandbox, SpringTrack, Track
from ..env.toyworld import Bakery, Dish, ShopWorld, Tiles, ToyWorld, Wheel

NUMBER_WORDS = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
                "nine", "ten"]
MARKS = "0123456789"

# dimensions (M, L, T)
FORCE, MASS, ACCEL, LENGTH, SPEED = (1, 1, -2), (1, 0, 0), (0, 1, -2), (0, 1, 0), (0, 1, -1)


class Lesson:
    number = None
    title = ""
    goal = ""
    kind = "play"           # "play": curiosity-driven; "guided": trainer-led
    budget = 200
    # A curated trainer picks helpful scenes (e.g. many equal trays). An uncurated
    # one shows uniformly random scenes over a wider range: that is where designing
    # your own experiments should matter.
    curated = True
    # A biased trainer never shows one kind of situation (e.g. equal trays, or a purse
    # in debt). Ultron can still set that situation up itself, if it thinks to.
    biased = False

    @property
    def top(self):
        return 5 if self.curated else 20

    def __init__(self, seed=0):
        self.seed = seed

    def specs(self):
        return []

    def scene(self, name, wide=False, request=None):
        raise NotImplementedError

    def options(self, name):
        """Situations Ultron could set up itself in this lesson (empty: it can't)."""
        return []


# ---------------------------------------------------------------- lesson 0
class Permanence(Lesson):
    number, title = 0, "Hidden things"
    goal = ("Discover that things hidden under a cup are all still there later: as many "
            "come out as went in, however long it waits.")

    def __init__(self, seed=0):
        super().__init__(seed)
        self.world = ToyWorld(seed)

    def specs(self):
        return [Spec("peekaboo", "program", {"hidden": INT, "waited": INT}, "found",
                     out_type=INT)]

    def options(self, name):
        return [{"hidden": h, "waited": t} for h in range(self.top + 1) for t in range(1, 7)]

    def scene(self, name, wide=False, request=None):
        w, rng = self.world, self.world.rng
        w.clear()
        n = request["hidden"] if request else rng.randint(0, 9 if wide else self.top)
        objs = w.put("table", n)
        w.hide("cup", objs)
        waited = request["waited"] if request else rng.randint(1, 40 if wide else 6)
        w.wait(waited)
        return {"hidden": count(objs), "waited": waited}, count(w.reveal("cup"))


# ---------------------------------------------------------------- lesson 1
class Pairing(Lesson):
    number, title = 1, "Same number"
    goal = "Discover that two trays pair off exactly when they have the same count."

    def __init__(self, seed=0):
        super().__init__(seed)
        self.world = ToyWorld(seed)

    def specs(self):
        return [Spec("pair_off", "program", {"nA": INT, "nB": INT}, "all_paired",
                     out_type=BOOL)]

    def options(self, name):
        return [{"nA": a, "nB": b} for a in range(self.top + 1) for b in range(self.top + 1)]

    def scene(self, name, wide=False, request=None):
        w, rng = self.world, self.world.rng
        top = 9 if wide else self.top
        a = rng.randint(0, top)
        b = a if self.curated and rng.random() < 0.4 else rng.randint(0, top)
        while self.biased and b == a:
            b = rng.randint(0, top)
        if request:
            a, b = request["nA"], request["nB"]
        w.put("A", a)
        w.put("B", b)
        left_a, left_b = w.pair_off("A", "B")
        return ({"nA": count(w.trays["A"]), "nB": count(w.trays["B"])},
                count(left_a) == 0 and count(left_b) == 0)


# ---------------------------------------------------------------- lesson 2
class Combining(Lesson):
    number, title = 2, "Putting together and taking away"
    goal = ("Discover addition and subtraction as laws about counts; ignore the "
            "randomly flickering lamp panel once it proves unlearnable.")

    def __init__(self, seed=0):
        super().__init__(seed)
        self.world = ToyWorld(seed)

    def specs(self):
        return [Spec("merge", "program", {"nA": INT, "nB": INT}, "total", out_type=INT),
                Spec("take_away", "program", {"nA": INT, "n_taken": INT}, "left",
                     out_type=INT),
                Spec("lamps", "program", {"lit_before": INT}, "lit_after", out_type=INT)]

    def options(self, name):
        n = self.top + 1
        if name == "merge":
            return [{"nA": a, "nB": b} for a in range(n) for b in range(n)]
        if name == "take_away":
            return [{"nA": a, "n_taken": t} for a in range(n) for t in range(a + 1)]
        return []

    def scene(self, name, wide=False, request=None):
        w, rng = self.world, self.world.rng
        top = 9 if wide else self.top
        if name == "merge":
            w.put("A", request["nA"] if request else rng.randint(0, top))
            w.put("B", request["nB"] if request else rng.randint(0, top))
            inputs = {"nA": count(w.trays["A"]), "nB": count(w.trays["B"])}
            return inputs, count(w.merge(["A", "B"], "C"))
        if name == "take_away":
            a = request["nA"] if request else rng.randint(0, top)
            w.put("A", a)
            inputs = {"nA": count(w.trays["A"])}
            w.take("A", request["n_taken"] if request else rng.randint(0, a), "hand")
            inputs["n_taken"] = count(w.trays["hand"])
            return inputs, count(w.trays["A"])
        before = w.flicker()
        return {"lit_before": before}, w.flicker()


# ---------------------------------------------------------------- lesson 3
class Groups(Lesson):
    number, title = 3, "Groups of groups"
    goal = "Discover multiplication, building on the addition law from lesson 2."

    def __init__(self, seed=0):
        super().__init__(seed)
        self.world = ToyWorld(seed)

    def specs(self):
        return [Spec("groups", "program", {"groups": INT, "size": INT}, "total", out_type=INT)]

    def options(self, name):
        top = 4 if self.curated else 10
        return [{"groups": g, "size": z} for g in range(top + 1) for z in range(top + 1)]

    def scene(self, name, wide=False, request=None):
        w, rng = self.world, self.world.rng
        w.clear()
        top = 6 if wide else (4 if self.curated else 10)
        g, s = rng.randint(0, top), rng.randint(0, top)
        if request:
            g, s = request["groups"], request["size"]
        trays = [f"G{i}" for i in range(g)]
        for t in trays:
            w.put(t, s)
        size_seen = count(w.trays[trays[0]]) if trays else rng.randint(0, top)
        total = count(w.merge(trays, "all")) if trays else 0
        return {"groups": count(trays), "size": size_seen}, total


# ---------------------------------------------------------------- lesson 4
class Names(Lesson):
    number, title = 4, "Names for things"
    goal = ("Learn marks 0-9 and words zero-ten for quantities it can count; ground "
            "'plus', 'minus', 'times', 'equals' in its own laws; discover place value "
            "from two-mark numerals so it can read and write any number.")
    kind = "guided"

    def __init__(self, seed=0):
        super().__init__(seed)
        self.world = ToyWorld(seed)
        self.brain_vocab = {}   # the Trainer lets the lesson see which marks Ultron knows

    def specs(self):
        return [Spec("numeral", "program", {"left": INT, "right": INT}, "count", out_type=INT)]

    def show_pile(self, n):
        self.world.put("pile", n)
        return count(self.world.trays["pile"])

    def naming_scenes(self):
        """(token, pile size) pairs: the Trainer points at a pile and says a word."""
        out = [(MARKS[n], n) for n in range(10)]
        out += [(NUMBER_WORDS[n], n) for n in range(11)]
        return out

    def operation_demos(self, brain):
        """The Trainer acts things out and says them, e.g. '3 plus 4 equals 7'."""
        rng = self.world.rng
        demos = {"plus": [], "+": [], "minus": [], "-": [], "times": [], "×": [], "*": []}
        equals = []
        for _ in range(6):
            a, b = rng.randint(0, 9), rng.randint(0, 9)
            self.world.put("A", a)
            self.world.put("B", b)
            total = count(self.world.merge(["A", "B"], "C"))
            for word in ("plus", "+"):
                demos[word].append((a, b, total))
            equals.append((total, total))   # '... equals 7' said next to the result
            a = rng.randint(0, 9)
            b = rng.randint(0, a)
            self.world.put("A", a)
            self.world.take("A", b, "hand")
            left = count(self.world.trays["A"])
            for word in ("minus", "-"):
                demos[word].append((a, b, left))
            g, s = rng.randint(0, 5), rng.randint(0, 5)
            trays = [f"G{i}" for i in range(g)]
            for t in trays:
                self.world.put(t, s)
            total = count(self.world.merge(trays, "all")) if trays else 0
            for word in ("times", "×", "*"):
                demos[word].append((g, s, total))
        return demos, equals

    def scene(self, name, wide=False, request=None):
        """Two-mark numeral next to a pile: the Trainer writes it, Ultron reads marks."""
        rng = self.world.rng
        n = rng.randint(10, 99)
        pile = self.show_pile(n)
        marks = f"{n}"      # the Trainer writes; Ultron only sees two marks
        left, right = read_marks(marks, self.brain_vocab)
        return {"left": left, "right": right}, pile


# ---------------------------------------------------------------- lesson 5
class Mechanics(Lesson):
    number, title = 5, "Pushing, stretching, colliding"
    goal = ("Discover F = m·a, that each spring has its own stiffness (F = k·x), and "
            "that m·v is conserved in every collision (m·v² only when balls bounce).")
    budget = 240

    def __init__(self, seed=0):
        super().__init__(seed)
        self.world = PhysicsSandbox(seed)
        self.rng = self.world.rng

    def specs(self):
        return [
            Spec("push", "quantity", {"F": FORCE, "m": MASS}, "a",
                 units={"F": FORCE, "m": MASS, "a": ACCEL}),
            Spec("stretch", "quantity", {"x": LENGTH}, "F", group_by="spring",
                 units={"F": FORCE, "x": LENGTH}),
            Spec("collide", "conservation", {}, "v2_after",
                 units={"m": MASS, "v": SPEED}),
        ]

    def scene(self, name, wide=False, request=None):
        rng = self.rng
        r = lambda lo, hi: round(rng.uniform(lo, hi), 3)
        if name == "push":
            m, F = r(1, 5 if not wide else 10), r(1, 20)
            return {"F": F, "m": m}, self.world.push(m, F)
        if name == "stretch":
            spring = rng.choice(self.world.springs)
            x = r(0.01, 0.5)
            return {"x": x, "spring": spring}, self.world.stretch(spring, x)
        m1, m2 = r(1, 5), r(1, 5)
        v1 = r(1, 5)
        v2 = r(-5, v1 - 0.5)
        kind = rng.choice(["clay", "steel"])
        u1, u2 = self.world.collide(m1, v1, m2, v2, kind)
        return {"m1": m1, "v1": v1, "m2": m2, "v2": v2, "kind": kind, "v1_after": u1}, u2


# ---------------------------------------------------------------- lesson 6
ORBIT_UNITS = {"r": LENGTH, "T": (0, 0, 1)}
# Boyle measured pressure in inches of mercury and the *length* of the trapped air
# column, not SI units, so the brain is not told their dimensions.
GAS_UNITS = {}


class RealData(Lesson):
    number, title = 6, "Real measurements"
    goal = ("From real planetary data find T²/r³ = constant (Kepler's third law); carry "
            "it to Jupiter's moons from a single moon; find P·V = constant in Boyle's "
            "1662 air measurements.")
    kind = "guided"

    PLANETS_TRAIN = ["Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn"]
    PLANETS_TEST = ["Uranus", "Neptune"]
    MOON_SHOWN = ["Io"]
    MOONS_TEST = ["Europa", "Ganymede", "Callisto"]

    def specs(self):
        return [
            Spec("orbit", "quantity", {"r": LENGTH}, "T", group_by="system",
                 units=ORBIT_UNITS, tol=0.02, surprise=0.02),
            Spec("gas", "quantity", {"V": None}, "P", units=GAS_UNITS,
                 tol=0.02, surprise=0.02),
        ]

    @staticmethod
    def bodies(names):
        rows = {r["body"]: r for r in dataworld.orbits()}
        return [rows[n] for n in names]

    @staticmethod
    def gas_split():
        rows = dataworld.boyle()
        return [r for r in rows if r["V"] >= 24], [r for r in rows if r["V"] < 24]


# ---------------------------------------------------------------- lesson 7
class NoisyLab(Lesson):
    number, title = 7, "A lab with cheap instruments"
    goal = ("Rediscover F = m·a and spring stiffness when every instrument reading is off "
            "by up to ±1%; predict the *true* values, not the noisy ones.")
    budget = 240
    PRECISION = 0.01    # printed on the instruments; Ultron is allowed to know it

    def __init__(self, seed=0):
        super().__init__(seed)
        self.world = PhysicsSandbox(seed, spring_prefix="L", precision=self.PRECISION)
        self.rng = self.world.rng

    def specs(self):
        p = self.PRECISION
        return [
            Spec("lab_push", "quantity", {"F": FORCE, "m": MASS}, "a",
                 units={"F": FORCE, "m": MASS, "a": ACCEL}, precision=p),
            Spec("lab_stretch", "quantity", {"x": LENGTH}, "F", group_by="spring",
                 units={"F": FORCE, "x": LENGTH}, precision=p),
        ]

    def scene(self, name, wide=False, request=None):
        w, rng = self.world, self.rng
        if name == "lab_push":
            m, F = rng.uniform(1, 5), rng.uniform(1, 20)
            return {"F": w.read(F), "m": w.read(m)}, w.read(w.push(m, F))
        spring, x = rng.choice(w.springs), rng.uniform(0.01, 0.5)
        return {"x": w.read(x), "spring": spring}, w.read(w.stretch(spring, x))


# ---------------------------------------------------------------- lesson 8
class Owing(Lesson):
    number, title = 8, "Owing"
    goal = ("A purse of coins and IOU notes. Nobody mentions numbers below zero. Can "
            "Ultron notice that its purse states form one line that continues past "
            "empty, *invent* numbers below zero, and then do arithmetic with them?")
    kind = "guided"
    budget = 200
    LINE = "line:earn/spend"

    def __init__(self, seed=0):
        super().__init__(seed)
        self.world = ShopWorld(seed)
        self.brain = None       # set by the Trainer: Ultron perceives purses its own way

    def purse_specs(self):
        return [Spec(f"{act}_{var}", "program", {"coins": INT, "notes": INT}, f"{var}_after",
                     out_type=INT, action=act, state_var=var)
                for act in ("earn", "spend") for var in ("coins", "notes")]

    def deal_specs(self):
        return [Spec("pay", "program", {"purse": INT, "price": INT}, "purse_after",
                     out_type=INT),
                Spec("get_paid", "program", {"purse": INT, "wage": INT}, "purse_after",
                     out_type=INT)]

    def specs(self):
        return self.purse_specs()

    def _random_purse(self, top=None):
        rng = self.world.rng
        n = rng.randint(0, self.top if top is None else top)
        if self.biased:
            return (max(n, 1), 0)       # never an empty purse, never a debt
        return (n, 0) if rng.random() < 0.5 else (0, n)

    def options(self, name):
        if name in ("pay", "get_paid"):
            return []
        return [{"coins": c, "notes": 0} for c in range(self.top + 1)] + \
               [{"coins": 0, "notes": n} for n in range(1, self.top + 1)]

    def perceive(self):
        from ..brain.invention import position
        return position(self.brain, self.LINE,
                        {"coins": len(self.world.coins), "notes": len(self.world.notes)})

    def scene(self, name, wide=False, request=None):
        w, rng = self.world, self.world.rng
        if name in ("pay", "get_paid"):
            w.set_purse(*self._random_purse())
            purse = self.perceive()
            amount = rng.randint(0, 8)
            for _ in range(amount):
                (w.spend if name == "pay" else w.earn)()
            key = "price" if name == "pay" else "wage"
            return {"purse": purse, key: amount}, self.perceive()
        c, n = (request["coins"], request["notes"]) if request else self._random_purse()
        w.set_purse(c, n)
        act, var = name.split("_")
        (w.earn if act == "earn" else w.spend)()
        return {"coins": c, "notes": n}, len(w.coins if var == "coins" else w.notes)

    def below_zero_names(self):
        """(written mark, spoken words, purse) the Trainer points at, AFTER the invention."""
        return [(f"-{n}", f"negative {NUMBER_WORDS[n]}", (0, n)) for n in range(1, 6)]

    def demos(self):
        """The Trainer acts out purchases and pay days and says them aloud."""
        rng = self.world.rng
        out = {"minus": [], "-": [], "plus": [], "+": []}
        for _ in range(8):
            c, n = self._random_purse()
            self.world.set_purse(c, n)
            before = self.perceive()
            k = rng.randint(0, 8)
            for _ in range(k):
                self.world.spend()
            out["minus"].append((before, k, self.perceive()))
            self.world.set_purse(*self._random_purse())
            before = self.perceive()
            k = rng.randint(0, 8)
            for _ in range(k):
                self.world.earn()
            out["plus"].append((before, k, self.perceive()))
        out["-"], out["+"] = out["minus"], out["plus"]
        return out


# ---------------------------------------------------------------- lesson 9
class Sharing(Lesson):
    number, title = 9, "Sharing cakes"
    goal = ("Cakes, a knife that cuts into equal pieces, and a balance. Nobody mentions "
            "fractions. Can Ultron notice amounts that lie *between* its numbers, invent "
            "them, and then answer 'what times 3 equals -7'?")
    kind = "guided"
    budget = 200

    def __init__(self, seed=0):
        super().__init__(seed)
        self.world = Bakery(seed)

    def specs(self):
        return [Spec("cake_balance", "program", {"pieces": INT, "cut": INT, "wholes": INT},
                     "level", out_type=BOOL),
                Spec("recut", "program", {"cut": INT, "recut": INT}, "pieces_per_cake",
                     out_type=INT)]

    def options(self, name):
        if name == "recut":
            return [{"cut": n, "recut": m} for n in range(1, 7) for m in range(1, 7)]
        return [{"pieces": k, "cut": n, "wholes": w}
                for n in range(1, 7) for w in range(0, 5) for k in range(0, 13)]

    def scene(self, name, wide=False, request=None):
        w, rng = self.world, self.world.rng
        if name == "recut":
            n = request["cut"] if request else rng.randint(1, 6)
            m = request["recut"] if request else rng.randint(1, 6)
            pieces = w.recut(w.cut(1, n), m)
            return {"cut": count(w.cut(1, n)), "recut": m}, count(pieces)
        n = request["cut"] if request else rng.randint(1, 6)
        wholes = request["wholes"] if request else rng.randint(0, 4)
        if request:
            k = request["pieces"]
        else:
            k = wholes * n if self.curated and rng.random() < 0.5 else rng.randint(0, 12)
        left = w.cut(k // n + 1, n)[:k]
        return ({"pieces": count(left), "cut": count(w.cut(1, n)), "wholes": wholes},
                w.balance(left, w.wholes(wholes)) == 0)

    def notation(self):
        """(what the Trainer writes, the pile Ultron sees: pieces, cut)."""
        return [("1/3", (1, 3)), ("2/3", (2, 3)), ("3/4", (3, 4)), ("5/2", (5, 2)),
                ("4/6", (4, 6))]

    def sharings(self):
        """The Trainer shares a cakes fairly between b people, and says 'a divided b'.
        Each person's share is what Ultron sees: a pieces of cakes cut into b."""
        rng = self.world.rng
        out = []
        for _ in range(6):
            a, b = rng.randint(0, 9), rng.randint(1, 6)
            share = count(self.world.cut(a, b)) // b
            out.append((a, b, (share, count(self.world.cut(1, b)))))
        return out


# ---------------------------------------------------------------- lesson 10
class FinalExam(Lesson):
    number, title = 10, "The tough final exam"
    goal = ("No teaching at all. Kinds of question never practised: division (never "
            "taught), inverse and chained questions, backwards physics chains, unseen "
            "real bodies, and impossible questions where the only right answer is "
            "'I can't'.")
    kind = "exam"


# ============================================================== PHASE 2
# ---------------------------------------------------------------- lesson 11
class WheelLesson(Lesson):
    number, title = 11, "The wheel"
    goal = ("A wheel with 6 slots and a pointer that ticks round. Nobody mentions clocks. "
            "The same shape discovery that found negative numbers should find that these "
            "positions go round, and invent clock numbers: '100 after 3', '-2 after 3'.")
    kind = "guided"
    budget = 200
    CYCLE = "cycle:tick"

    def __init__(self, seed=0):
        super().__init__(seed)
        self.world = Wheel(6, seed)
        self.rng = self.world.rng

    def specs(self):
        return [Spec("tick", "program", {"slot": INT}, "slot_after", out_type=INT,
                     action="tick", state_var="slot")]

    def spin_specs(self):
        return [Spec("spin", "program", {"start": INT, "ticks": INT}, "end", out_type=INT)]

    def options(self, name):
        if name == "tick":
            return [{"slot": p} for p in range(6)]
        return [{"start": p, "ticks": t} for p in range(6) for t in range(9)]

    def scene(self, name, wide=False, request=None):
        w, rng = self.world, self.rng
        if name == "tick":
            w.set(request["slot"] if request else rng.randrange(6))
            before = count(w.marks_past_top())
            w.tick()
            return {"slot": before}, count(w.marks_past_top())
        w.set(request["start"] if request else rng.randrange(6))
        start = count(w.marks_past_top())
        n = request["ticks"] if request else rng.randint(0, 8)
        for _ in range(n):
            w.tick()
        return {"start": start, "ticks": n}, count(w.marks_past_top())

    def after_demos(self):
        """The Trainer spins the wheel and says e.g. '3 after 5 equals 2'."""
        out = []
        for _ in range(6):
            start, n = self.rng.randrange(6), self.rng.randint(0, 9)
            self.world.set(start)
            for _ in range(n):
                self.world.tick()
            out.append((n, start, count(self.world.marks_past_top())))
        return out


# ---------------------------------------------------------------- lesson 12
class Ramps(Lesson):
    number, title = 12, "Hills and valleys"
    goal = ("Balls roll on a frictionless track. Nobody mentions energy. Can Ultron find "
            "a hidden quantity, shared between height and speed, that never changes along "
            "a run, and use it on runs 10 times higher and on balls thrown upwards?")
    budget = 120

    def __init__(self, seed=0):
        super().__init__(seed)
        self.world = Track(seed)
        self.rng = self.world.rng
        self.current = None
        self.left = 0

    def specs(self):
        return [Spec("roll", "quantity", {"y": LENGTH, "m": MASS}, "v", group_by="run",
                     units={"y": LENGTH, "m": MASS, "v": SPEED}, tol=1e-6)]

    def scene(self, name, wide=False, request=None):
        rng, w = self.rng, self.world
        if self.current is None or self.left == 0:
            self.current = w.new_run(round(rng.uniform(1, 5), 3), round(rng.uniform(1, 5), 3))
            self.left = rng.randint(3, 6)
            y = w.release                       # first reading: where it was let go
        else:
            y = round(rng.uniform(0, w.release), 3)
        self.left -= 1
        return {"y": y, "m": w.mass, "run": self.current}, w.speed_at(y)


# ---------------------------------------------------------------- lesson 13
class Growing(Lesson):
    number, title = 13, "Growing"
    goal = ("One cell in a dish; each day every cell splits into the same number. Ultron "
            "predicted a law like this ten lessons earlier, from a pattern in its own laws "
            "(REPEAT). Does the world agree? And does it see where the pattern stops?")
    budget = 150

    def __init__(self, seed=0):
        super().__init__(seed)
        self.world = Dish(seed)
        self.rng = self.world.rng

    def specs(self):
        return [Spec("grow", "program", {"split": INT, "days": INT}, "cells", out_type=INT)]

    def options(self, name):
        return [{"split": k, "days": d} for k in range(1, 5) for d in range(0, 5)]

    def scene(self, name, wide=False, request=None):
        k = request["split"] if request else self.rng.randint(1, 4)
        d = request["days"] if request else self.rng.randint(0, 4)
        self.world.start()
        for _ in range(d):
            self.world.day(k)
        return {"split": k, "days": d}, count(self.world.cells)

    def power_demos(self):
        out = []
        for _ in range(6):
            k, d = self.rng.randint(1, 4), self.rng.randint(0, 4)
            self.world.start()
            for _ in range(d):
                self.world.day(k)
            out.append((k, d, count(self.world.cells)))
        return out


# ---------------------------------------------------------------- lesson 14
class SpringyHills(Lesson):
    number, title = 14, "Hills and a spring"
    goal = ("The same track with a spring bumper at the bottom. Nobody says springs store "
            "anything. Can Ultron find that the hidden quantity now has THREE parts (height, "
            "speed and squash) and answer never-trained questions: how far will the spring "
            "squash? how high will a spring launch a ball?")
    budget = 160

    def __init__(self, seed=0):
        super().__init__(seed)
        self.world = SpringTrack(seed, prefix="S")
        self.rng = self.world.rng
        self.current = None
        self.left = 0

    def specs(self):
        return [Spec("bounce", "quantity", {"y": LENGTH, "c": LENGTH}, "v", group_by="run",
                     units={"y": LENGTH, "c": LENGTH, "v": SPEED}, tol=1e-6)]

    def scene(self, name, wide=False, request=None):
        rng, w = self.rng, self.world
        if self.current is None or self.left == 0:
            self.current = w.new_run(round(rng.uniform(1, 5), 3), w.MASS)
            self.left = rng.randint(4, 7)
            y, c = w.release, 0.0
        elif rng.random() < 0.5:
            y, c = round(rng.uniform(0, w.release), 3), 0.0
        else:
            y, c = 0.0, round(rng.uniform(0, w.max_squash()), 4)
        self.left -= 1
        return {"y": y, "c": c, "run": self.current}, w.speed(y, c)


# ---------------------------------------------------------------- lesson 15
class Diagonal(Lesson):
    number, title = 15, "The diagonal of a tile"
    goal = ("Ultron invented numbers in the gaps of its line by reasoning alone. Here the "
            "world checks it: counting tiles in squares, then the half-tiles in the square "
            "on a tile's diagonal, it must conclude the diagonal is the gap number whose "
            "square is 2, and predict every ruler reading before measuring.")
    kind = "guided"
    budget = 80

    def __init__(self, seed=0):
        super().__init__(seed)
        self.world = Tiles(seed)
        self.rng = self.world.rng

    def specs(self):
        return [Spec("square", "program", {"side": INT}, "tiles", out_type=INT)]

    def ruler_spec(self):
        return Spec("ruler", "measure", {"marks": INT}, "diagonal", out_type=INT)

    def options(self, name):
        return [{"side": s} for s in range(0, 7)]

    def scene(self, name, wide=False, request=None):
        side = request["side"] if request else self.rng.randint(0, 6)
        return {"side": side}, count(self.world.square(side))

    def ruler(self, marks):
        return {"marks": marks}, self.world.ruler_reading(marks)


# ---------------------------------------------------------------- lesson 16
class Phase2Exam(Lesson):
    number, title = 16, "Phase 2 final exam"
    goal = ("No teaching. Questions that combine Phase 2's inventions in ways never "
            "practised: square roots, logarithms and negative powers (never taught), "
            "fractions raised to powers, clock numbers with huge backward spins, energy for "
            "dropped balls, and 'what power 2 equals 2', which no fraction answers (Ultron "
            "must pin it in a gap of its line).")
    kind = "exam"


# ============================================================== PHASE 3
# ---------------------------------------------------------------- lesson 17
class CoiledSprings(Lesson):
    number, title = 17, "Coiled springs"
    goal = ("Springs wound from the same wire with different numbers of coils. Stretching "
            "one shows how hard it pulls; looking at it shows its coils. Can Ultron find a "
            "law about its own stiffness law (stiffness × coils is constant) and predict how "
            "hard a brand-new spring pulls without ever stretching it?")
    budget = 200

    def __init__(self, seed=0):
        super().__init__(seed)
        self.world = CoilShop(seed)
        self.rng = self.world.rng
        for _ in range(7):
            self.world.new_spring()

    def specs(self):
        return [Spec("coil_stretch", "quantity", {"x": LENGTH}, "F", group_by="spring",
                     units={"F": FORCE, "x": LENGTH}),
                Spec("coil_look", "feature", {"spring": None}, "coils", group_by="spring")]

    def scene(self, name, wide=False, request=None):
        spring = self.rng.choice(self.world.springs)
        if name == "coil_look":
            return {"spring": spring}, count(self.world.count_coils(spring))
        x = round(self.rng.uniform(0.01, 0.5), 3)
        return {"x": x, "spring": spring}, self.world.stretch(spring, x)


# ---------------------------------------------------------------- lesson 18
class Phase3Exam(Lesson):
    number, title = 18, "Phase 3 exam: the hardest questions"
    goal = ("No teaching. Huge numbers (column arithmetic), logarithms and fractional powers "
            "(fractional repeats), and springs never stretched (laws about laws).")
    kind = "exam"


# ------------------------------------------------------- Phase 3: new kinds
class _Sequences(Lesson):
    """Readings of one object after another, in order; Ultron picks which world to
    watch by curiosity."""
    READS = {}

    def __init__(self, seed=0):
        super().__init__(seed)
        import random
        self.rng = random.Random(seed)
        self.state = {}

    def worlds(self):
        return {}

    def xs(self, name):
        n = self.READS.get(name, 10)
        return list(range(n))

    def scene(self, name, wide=False, request=None):
        world, new, spec = self.worlds()[name]
        st = self.state.get(name)
        if st is None or not st["xs"]:
            st = self.state[name] = {"obj": new(), "xs": self.xs(name)}
        x = st["xs"].pop(0)
        return {spec.order_by: x, spec.group_by: st["obj"]}, world.read(st["obj"], x)


class CoolingLesson(_Sequences):
    number, title = 22, "Cooling cups"
    goal = ("Hot cups cool on a table; a thermometer is read once a minute. Newton's law of "
            "cooling fits none of Ultron's innate kinds of explanation (no product and no "
            "sum of readings stays the same). Can it invent a new KIND of explanation, "
            "'the steps shrink by the same fraction each time', and use it to predict new "
            "cups and the room's temperature it never measured?")
    budget = 80
    READS = {"cool": 10}

    def __init__(self, seed=0):
        super().__init__(seed)
        from ..env.sequences import CoolingCups
        self.cups = CoolingCups(seed)

    def specs(self):
        return [Spec("cool", "sequence", {"t": None}, "T", group_by="cup", order_by="t",
                     tol=0.01, surprise=0.005)]

    def worlds(self):
        return {"cool": (self.cups, self.cups.new_cup, self.specs()[0])}


class SettlingLesson(_Sequences):
    number, title = 23, "Bouncing, charging, hanging, burning, wandering"
    goal = ("Five new worlds. Balls bounce lower each time; batteries fill toward full; "
            "springs are measured by their whole length; candles burn down, read at odd "
            "times; and a marker blown about by random gusts. Does Ultron reuse the kind of "
            "explanation it invented (cheaply) where it fits, invent a second kind where it "
            "doesn't ('equal steps in what I change give equal steps in what I read'), carry "
            "that to candles, and refuse to explain the random marker at all?")
    budget = 400
    READS = {"bounces": 7, "charge": 10, "hang": 6, "burn": 8, "wander": 10}

    def __init__(self, seed=0):
        super().__init__(seed)
        from ..env.sequences import Batteries, BouncingBalls, Candles, HangingSprings, Wanderers
        self.balls, self.batteries = BouncingBalls(seed), Batteries(seed + 1)
        self.springs, self.candles = HangingSprings(seed + 2), Candles(seed + 3)
        self.walkers = Wanderers(seed + 4)

    def specs(self):
        seq = lambda name, x, y, g, tol=0.01: Spec(name, "sequence", {x: None}, y, group_by=g,
                                                  order_by=x, tol=tol, surprise=tol / 2)
        return [seq("bounces", "k", "h", "ball"), seq("charge", "t", "q", "battery"),
                seq("hang", "F", "L", "spring"), seq("burn", "t", "H", "candle"),
                seq("wander", "t", "x", "walker")]

    def worlds(self):
        s = {spec.name: spec for spec in self.specs()}
        return {"bounces": (self.balls, self.balls.new_ball, s["bounces"]),
                "charge": (self.batteries, self.batteries.new_battery, s["charge"]),
                "hang": (self.springs, self.springs.new_spring, s["hang"]),
                "burn": (self.candles, self.candles.new_candle, s["burn"]),
                "wander": (self.walkers, self.walkers.new_walker, s["wander"])}

    def xs(self, name):
        rng = self.rng
        if name == "hang":
            return sorted(round(rng.uniform(1, 30), 2) for _ in range(self.READS[name]))
        if name == "burn":
            t, out = 0, []
            for _ in range(self.READS[name]):
                out.append(t)
                t += rng.randint(1, 5)      # whenever someone looks
            return out
        return super().xs(name)


class ChangeLesson(_Sequences):
    number, title = 27, "Swinging, dying down, growing, emptying"
    goal = ("Four worlds where none of Ultron's kinds fit: pendulums swing, a car's body "
            "bobs and settles after a bump, yeast multiplies until its jar is crowded, and "
            "funnels empty faster when full. Can it invent kinds where how the state changes "
            "is a law of the state (the next reading a fixed mix of the last two), or a law "
            "about a power of the reading, reuse them across worlds, and work out what it "
            "never measured: a pendulum's period, how fast a bounce dies, a jar's capacity, "
            "when a funnel will be empty?")
    budget = 400
    READS = {"swings": 8, "bumps": 8, "yeast": 10, "funnel_h": 8}

    def __init__(self, seed=0):
        super().__init__(seed)
        from ..env.sequences import Funnels, Pendulums, ShockAbsorbers, YeastJars
        self.pendulums, self.cars = Pendulums(seed), ShockAbsorbers(seed + 1)
        self.jars, self.funnels = YeastJars(seed + 2), Funnels(seed + 3)

    def specs(self):
        seq = lambda name, x, y, g, tol=0.01: Spec(name, "sequence", {x: None}, y, group_by=g,
                                                  order_by=x, tol=tol, surprise=tol / 2)
        return [seq("swings", "t", "angle", "pendulum"), seq("bumps", "t", "z", "car"),
                seq("yeast", "t", "cells", "jar"), seq("funnel_h", "t", "h", "funnel")]

    def worlds(self):
        s = {spec.name: spec for spec in self.specs()}
        return {"swings": (self.pendulums, self.pendulums.new_pendulum, s["swings"]),
                "bumps": (self.cars, self.cars.new_car, s["bumps"]),
                "yeast": (self.jars, self.jars.new_jar, s["yeast"]),
                "funnel_h": (self.funnels, self.funnels.new_funnel, s["funnel_h"])}


class RowsLesson(Lesson):
    number, title = 28, "Rows of things"
    goal = ("A market stall: a basket of fruit with a price on each, a line of children "
            "against a height mark, a price list the day every price goes up by one, two "
            "rows of baskets put together. Each experience is a ROW of numbers, of any "
            "length. Can Ultron find laws about rows (how many, the total, those above a "
            "mark, each one stepped, two rows paired) built from laws it already knows, and "
            "use them on rows far longer than any it has seen?")
    budget = 240

    def __init__(self, seed=0):
        super().__init__(seed)
        import random
        self.rng = random.Random(seed)

    def specs(self):
        return [Spec("basket", "program", {"prices": LIST}, "to_pay", out_type=INT),
                Spec("tall", "program", {"heights": LIST, "mark": INT}, "taller",
                     out_type=INT),
                Spec("rise", "program", {"prices": LIST}, "new_prices", out_type=LIST),
                Spec("two_rows", "program", {"row_a": LIST, "row_b": LIST}, "together",
                     out_type=LIST)]

    def _row(self, n=None, top=None):
        rng = self.rng
        n = n if n is not None else rng.randint(1, 4)
        return [rng.randint(0, top or self.top + 4) for _ in range(n)]

    def scene(self, name, wide=False, request=None):
        rng = self.rng
        if name == "basket":
            p = self._row()
            return {"prices": p}, sum(p)
        if name == "tall":
            h, m = self._row(), rng.randint(0, self.top + 4)
            return {"heights": h, "mark": m}, sum(1 for x in h if x > m)
        if name == "rise":
            p = self._row()
            return {"prices": p}, [x + 1 for x in p]
        n = rng.randint(1, 4)
        a, b = self._row(n), self._row(n)
        return {"row_a": a, "row_b": b}, [x + y for x, y in zip(a, b)]


def all_lessons(seed=0):
    return [Permanence(seed), Pairing(seed + 1), Combining(seed + 2), Groups(seed + 3),
            Names(seed + 4), Mechanics(seed + 5), RealData(seed + 6), NoisyLab(seed + 7),
            Owing(seed + 8), Sharing(seed + 9), FinalExam(seed + 10),
            WheelLesson(seed + 11), Ramps(seed + 12), Growing(seed + 13),
            SpringyHills(seed + 14), Diagonal(seed + 15), Phase2Exam(seed + 16),
            CoiledSprings(seed + 17), Phase3Exam(seed + 18)] + _phase3(seed)


def _phase3(seed):
    """Phase 3 needs numpy for its senses; without it, lessons 0-18 still run."""
    try:
        from .senses_lessons import later_lessons, senses_lessons
    except ImportError:
        return []
    return (senses_lessons(seed) + [CoolingLesson(seed + 22), SettlingLesson(seed + 23)]
            + later_lessons(seed) + [ChangeLesson(seed + 27), RowsLesson(seed + 28)])
