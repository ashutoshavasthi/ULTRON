"""Phase 3 lessons with senses: Ultron learns its eyes, then relearns what it knows
through them. Nothing here hands Ultron a number the camera didn't show it, except
its own actions (how hard it pushes, how many blocks it hangs) and what is printed
on its instruments (the camera's pictures per second, the ruler marks a metre apart).
"""

import statistics

from ..brain.dsl import INT
from ..brain.memory import Spec
from .lessons import ACCEL, FORCE, LENGTH, MASS, SPEED, Lesson


class Handling(Lesson):
    number, title = 19, "Handling things"
    goal = ("Ultron picks things up and puts them down. Touch tells it where each thing is; "
            "the camera shows it pixels at the same moment. From these pairs it trains a "
            "small neural network (its eyes) to find things in pictures. Afterwards touch "
            "is gone: can it count trays of up to 30 things, and find where they are, from "
            "noisy pixels alone?")
    kind = "guided"
    SCENES = 400

    def __init__(self, seed=0):
        super().__init__(seed)
        from ..senses.world import Trays
        self.trays = Trays(seed)

    def handling(self):
        rng = self.trays.rng
        for i in range(self.SCENES):
            n = int(rng.integers(0, 14)) if i % 4 else int(rng.integers(14, 30))
            yield self.trays.handle(n)


class SeeingNumbers(Lesson):
    number, title = 20, "Seeing numbers"
    goal = ("Putting trays together and taking things away again, but now Ultron only "
            "sees pictures and counts with its own eyes (looking again when unsure). Does it "
            "find that what it sees obeys the addition and subtraction it already knows?")
    budget = 80

    def __init__(self, seed=0):
        super().__init__(seed)
        from ..senses.world import Trays
        self.trays = Trays(seed)
        self.looks = 0

    def specs(self):
        return [Spec("see_merge", "program", {"nA": INT, "nB": INT}, "total", out_type=INT),
                Spec("see_take", "program", {"nA": INT, "n_taken": INT}, "left", out_type=INT)]

    def options(self, name):
        if name == "see_merge":
            return [{"nA": a, "nB": b} for a in range(0, 13) for b in range(0, 13)]
        return [{"nA": a, "n_taken": t} for a in range(0, 13) for t in range(0, a + 1)]

    def _count(self, n):
        c, glances = self.brain.eyes.count(self.trays.tray(n))
        self.looks += glances
        return c

    def scene(self, name, wide=False, request=None):
        rng = self.trays.rng
        if name == "see_merge":
            a = request["nA"] if request else int(rng.integers(0, 13))
            b = request["nB"] if request else int(rng.integers(0, 13))
            return {"nA": self._count(a), "nB": self._count(b)}, self._count(a + b)
        a = request["nA"] if request else int(rng.integers(0, 13))
        t = request["n_taken"] if request else int(rng.integers(0, a + 1))
        return {"nA": self._count(a), "n_taken": self._count(t)}, self._count(a - t)


class WatchingMotion(Lesson):
    number, title = 21, "Watching motion"
    goal = ("Ultron pushes loaded pucks, hangs blocks on springs and lets balls roll in a "
            "valley, and only SEES what happens: positions in pixels, a ruler in the picture, "
            "a camera that shakes and sometimes spoils a frame. It measures its own eyes' "
            "noise first. Can it rediscover F = m·a, each spring's stiffness, and energy "
            "(height + speed²/2g) from video alone?")
    budget = 150

    def __init__(self, seed=0):
        super().__init__(seed)
        from ..senses.world import HillTrack, PushTable, SpringStand
        self.table = PushTable(seed)
        self.stand = SpringStand(seed + 1)
        for _ in range(5):
            self.stand.new_spring()
        self.hills = HillTrack(seed + 2)
        self.rng = self.table.rng
        self._specs = None
        self.samples = []
        self.rest = {}

    # ------------------------------------------------ measuring its own eyes first
    def calibrate(self):
        """Practise a few times and see how much its measurements wobble."""
        from ..senses import measure
        from ..senses.world import FPS
        eyes, rel = self.brain.eyes, []
        for F, blocks in ((3, 2), (6, 4), (8, 5)):
            a, se = measure.acceleration(eyes, self.table.film(F, blocks), FPS)
            if a:
                rel.append(se / a)
        push = max(0.005, round(3 * statistics.median(rel), 3))
        diffs = []
        for spring in self.stand.springs[:3]:
            exts = []
            for _ in range(2):
                y0, _ = measure.position(eyes, self.stand.look(spring, 0))
                y2, _ = measure.position(eyes, self.stand.look(spring, 2))
                exts.append(y2 - y0)
            diffs.append(abs(exts[0] - exts[1]) / (sum(exts) / 2))
        stretch = max(0.01, round(3 * statistics.median(diffs), 3))
        return push, stretch

    def specs(self):
        if self._specs is None:
            push, stretch = self.calibrate()
            self.brain.note("reflect", f"I practised measuring with my eyes: accelerations "
                                       f"wobble by about ±{push:.1%}, spring stretches by about "
                                       f"±{stretch:.1%}; heights and speeds I'll judge picture "
                                       f"by picture")
            self._specs = [
                Spec("see_push", "quantity", {"F": FORCE, "m": MASS}, "a",
                     units={"F": FORCE, "m": MASS, "a": ACCEL}, precision=push),
                Spec("see_stretch", "quantity", {"x": LENGTH}, "W", group_by="spring",
                     units={"x": LENGTH}, precision=stretch),
                Spec("see_roll", "quantity", {"y": LENGTH}, "v", group_by="run",
                     units={"y": LENGTH, "v": SPEED}, precision=0.02,
                     errors={"y": "±y", "v": "±v"}),
            ]
        return self._specs

    def push(self, F, blocks):
        """Load the puck, count the blocks by eye, push, and watch."""
        from ..senses import measure
        from ..senses.world import FPS
        m, _ = self.brain.eyes.count(self.table.load(blocks))
        for _ in range(3):
            a, se = measure.acceleration(self.brain.eyes, self.table.film(F, blocks), FPS)
            if a is not None:
                return m, a
        return m, None

    def stretch(self, spring, blocks):
        from ..senses import measure
        if spring not in self.rest:
            self.rest[spring], _ = measure.position(self.brain.eyes, self.stand.look(spring, 0))
        y, _ = measure.position(self.brain.eyes, self.stand.look(spring, blocks))
        return None if y is None or self.rest[spring] is None else y - self.rest[spring]

    def roll(self, release_x):
        """Let a ball go and film it: careful (height, speed) readings with their ±."""
        from ..senses import measure
        run, pics, truth, fps = self.hills.film(release_x)
        return run, measure.path_samples(self.brain.eyes, pics, fps), truth

    def scene(self, name, wide=False, request=None):
        rng = self.rng
        if name == "see_push":
            F = request["F"] if request else int(rng.integers(1, 11))
            blocks = request["m"] if request else int(rng.integers(1, 7))
            m, a = self.push(F, blocks)
            return {"F": float(F), "m": float(m)}, a
        if name == "see_stretch":
            spring = self.stand.springs[int(rng.integers(0, len(self.stand.springs)))]
            blocks = int(rng.integers(1, 4))
            return {"x": self.stretch(spring, blocks), "spring": spring}, float(blocks)
        if not self.samples:
            run, samples, _ = self.roll(float(rng.uniform(0.1, 1.2)))
            self.samples = [(run, s) for s in samples]
        run, (y, v, sy, sv) = self.samples.pop(0)
        return {"y": y, "run": run, "±y": sy, "±v": sv}, v


class UsingWhatItKnows(Lesson):
    number, title = 24, "Using what it knows"
    goal = ("Ultron kicks pucks along a wooden floor and watches where they stop (it finds "
            "stopping distance / speed² is fixed: friction). Then the exam gives it GOALS: a "
            "painted mark to stop on, on wood and on a carpet it has never touched. It must "
            "run its law backwards to choose a kick, watch the result, and if it misses, "
            "treat the miss as a measurement and correct, not flail.")
    budget = 40

    def __init__(self, seed=0):
        super().__init__(seed)
        from ..senses.world import Floors
        self.floors = Floors(seed)
        self.rng = self.floors.rng

    def specs(self):
        return [Spec("slide", "quantity", {"u": SPEED}, "d", group_by="floor",
                     units={"u": SPEED, "d": LENGTH}, precision=0.02)]

    def watch_kick(self, floor, u, floors=None):
        """Kick at speed u and see how far the puck went (metres), by eye."""
        from ..senses import measure
        floors = floors or self.floors
        start, _ = measure.position(self.brain.eyes, floors.before(), measure.BOTTOM)
        pics = floors.kick(floor, u)
        if pics is None or start is None:
            return None
        end, _ = measure.position(self.brain.eyes, pics, measure.BOTTOM)
        return None if end is None else end - start

    def scene(self, name, wide=False, request=None):
        for _ in range(5):
            u = round(float(self.rng.uniform(1.0, 3.8)), 2)
            d = self.watch_kick("wood", u)
            if d is not None:
                return {"u": u, "floor": "wood"}, d
        return {"u": u, "floor": "wood"}, None


class Phase3SensesExam(Lesson):
    number, title = 25, "Phase 3 exam: seeing, inventing, acting"
    goal = ("No teaching. Count from pixels; predict motion before watching it; meet a "
            "world it has never seen (a draining tank) and explain it with a kind of "
            "explanation it invented earlier; reach goals on an icy floor it has never "
            "touched; and show that without inventing kinds, the same brain can't.")
    kind = "exam"


def senses_lessons(seed=0):
    return [Handling(seed + 19), SeeingNumbers(seed + 20), WatchingMotion(seed + 21)]


def later_lessons(seed=0):
    return [UsingWhatItKnows(seed + 24), Phase3SensesExam(seed + 25)]
