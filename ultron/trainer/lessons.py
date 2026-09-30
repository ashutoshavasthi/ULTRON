"""The curriculum. Each lesson gives Ultron things to play with and, sometimes,
words for what it has already understood. A lesson never contains a law:
scenes are set up in a world, and the world does what it does.

The `goal` text is for humans reading the reports; Ultron never sees it.
"""

from ..brain.dsl import BOOL, INT
from ..brain.memory import Spec
from ..brain.perception import count, present, read_marks
from ..env import dataworld
from ..env.physics import PhysicsSandbox
from ..env.toyworld import ToyWorld

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

    def __init__(self, seed=0):
        self.seed = seed

    def specs(self):
        return []

    def scene(self, name, wide=False):
        raise NotImplementedError


# ---------------------------------------------------------------- lesson 0
class Permanence(Lesson):
    number, title = 0, "Hidden things"
    goal = "Discover that an object hidden under a cup is still there later."

    def __init__(self, seed=0):
        super().__init__(seed)
        self.world = ToyWorld(seed)

    def specs(self):
        return [Spec("peekaboo", "program", {"went_in": BOOL, "waited": INT}, "there",
                     out_type=BOOL)]

    def scene(self, name, wide=False):
        w, rng = self.world, self.world.rng
        w.clear()
        objs = w.put("table", 1) if rng.random() < 0.6 else []
        w.hide("cup", objs)
        waited = rng.randint(1, 40 if wide else 6)
        w.wait(waited)
        return {"went_in": present(objs), "waited": waited}, present(w.reveal("cup"))


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

    def scene(self, name, wide=False):
        w, rng = self.world, self.world.rng
        top = 9 if wide else 5
        a = rng.randint(0, top)
        b = a if rng.random() < 0.4 else rng.randint(0, top)
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

    def scene(self, name, wide=False):
        w, rng = self.world, self.world.rng
        top = 9 if wide else 5
        if name == "merge":
            w.put("A", rng.randint(0, top))
            w.put("B", rng.randint(0, top))
            inputs = {"nA": count(w.trays["A"]), "nB": count(w.trays["B"])}
            return inputs, count(w.merge(["A", "B"], "C"))
        if name == "take_away":
            a = rng.randint(0, top)
            w.put("A", a)
            inputs = {"nA": count(w.trays["A"])}
            w.take("A", rng.randint(0, a), "hand")
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

    def scene(self, name, wide=False):
        w, rng = self.world, self.world.rng
        w.clear()
        top = 6 if wide else 4
        g, s = rng.randint(0, top), rng.randint(0, top)
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

    def scene(self, name, wide=False):
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

    def scene(self, name, wide=False):
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

    def scene(self, name, wide=False):
        w, rng = self.world, self.rng
        if name == "lab_push":
            m, F = rng.uniform(1, 5), rng.uniform(1, 20)
            return {"F": w.read(F), "m": w.read(m)}, w.read(w.push(m, F))
        spring, x = rng.choice(w.springs), rng.uniform(0.01, 0.5)
        return {"x": w.read(x), "spring": spring}, w.read(w.stretch(spring, x))


# ---------------------------------------------------------------- lesson 8
class FinalExam(Lesson):
    number, title = 8, "The tough final exam"
    goal = ("No teaching at all. Kinds of question never practised: division (never "
            "taught), inverse and chained questions, backwards physics chains, unseen "
            "real bodies, and impossible questions where the only right answer is "
            "'I can't'.")
    kind = "exam"


def all_lessons(seed=0):
    return [Permanence(seed), Pairing(seed + 1), Combining(seed + 2), Groups(seed + 3),
            Names(seed + 4), Mechanics(seed + 5), RealData(seed + 6), NoisyLab(seed + 7),
            FinalExam(seed + 8)]
