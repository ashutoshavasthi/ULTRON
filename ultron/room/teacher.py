"""The teacher: another agent in the room, scripted, who shows Ultron things.

It has a head with eyes that open and close (where its eyes sit shows where it looks), a
body and two hands. It comes and goes, looks at things, shows them, hands them over,
hides them behind the screen and presses the light toy. Later levels give it more to do
(naming things, demonstrating) in new work packages; each change is recorded.

What it may not do (docs/LEVEL_0_PLAN.md): read anything inside Ultron, change what it
does depending on how an exam is going, reward the answer to an exam, or act on exam
seeds. It sees only what anyone in the room could see (Room.public_state) and it never
imports Ultron's brain. Its randomness is its own. Everything it does is logged.

Modes (for the failure lab): "normal"; "off" (it never comes); "misleading_gaze" (it
looks at a different thing from the one it acts on).

This file's SHA-256 is recorded in docs/LEVEL_0_PLAN.md; a test checks it, so any change
to the script is a visible change to the plan.
"""

import numpy as np

HOME_X = 128.0          # where it sits
AWAY_X = 182.0          # out of the room
HEAD_Y = 44.0           # where its head is (it sits on the floor)
LEARNER = (16.0, 50.0)  # Ultron's head, where it looks when it looks at Ultron
IN_FRONT = (50.0, 46.0)     # where it holds a thing up for Ultron to see
TOYS = ("ball", "block", "light")
EPISODES = (("look", 3), ("show", 3), ("hand_over", 2), ("hide", 2), ("press", 2),
            ("idle", 3))
MODES = ("normal", "off", "misleading_gaze")


class Teacher:
    def __init__(self, seed, mode="normal"):
        if mode not in MODES:
            raise ValueError(f"unknown teacher mode {mode!r}")
        self.rng = np.random.default_rng(seed)
        self.mode = mode
        self.present = False
        self.body_x = AWAY_X
        self.hands = [[AWAY_X - 10, 70.0], [AWAY_X + 8, 72.0]]
        self.grip = [False, False]
        self.gaze = list(LEARNER)
        self.eyes_open = True
        self.log = []
        self.seen = None
        self.t = 0
        self._script = self._life()

    # ---- one step

    def step(self, seen, t):
        """seen: what anyone in the room could see. Returns how the teacher is now."""
        self.seen, self.t = seen, t
        next(self._script)
        return {"present": self.present, "body_x": self.body_x,
                "head": (self.body_x, HEAD_Y),
                "hands": [tuple(h) for h in self.hands], "grip": tuple(self.grip),
                "gaze": tuple(self.gaze), "eyes_open": self.eyes_open}

    def _note(self, episode, toy=None, gaze_toy=None):
        self.log.append({"t": self.t, "episode": episode, "toy": toy, "gaze_toy": gaze_toy})

    # ---- the script

    def _life(self):
        if self.mode == "off":
            while True:
                yield
        yield from self._wait(int(self.rng.integers(50, 400)))
        while True:
            yield from self._arrive()
            for _ in range(int(self.rng.integers(6, 16))):
                names = [e for e, _ in EPISODES]
                weights = np.array([w for _, w in EPISODES], dtype=float)
                episode = names[int(self.rng.choice(len(names), p=weights / weights.sum()))]
                yield from getattr(self, "_" + episode)()
            yield from self._leave()
            yield from self._wait(int(self.rng.integers(300, 2000)))

    def _wait(self, n):
        for _ in range(n):
            yield

    def _arrive(self):
        self._note("arrive")
        self.present = True
        yield from self._walk(HOME_X, 40)

    def _leave(self):
        self._note("leave")
        yield from self._walk(AWAY_X, 40)
        self.present = False

    def _walk(self, x, n):
        x0 = self.body_x
        h0 = [list(h) for h in self.hands]
        for i in range(1, n + 1):
            f = i / n
            self.body_x = x0 + f * (x - x0)
            for k, rest in enumerate(((-10.0, 70.0), (8.0, 72.0))):
                self.hands[k] = [h0[k][0] + f * (self.body_x + rest[0] - h0[k][0]),
                                 h0[k][1] + f * (rest[1] - h0[k][1])]
            self.gaze = list(LEARNER)
            yield

    def _move(self, k, target, n, carry_gaze=None):
        """Move hand k to target over n steps."""
        x0, y0 = self.hands[k]
        for i in range(1, n + 1):
            f = i / n
            self.hands[k] = [x0 + f * (target[0] - x0), y0 + f * (target[1] - y0)]
            if carry_gaze is not None:
                self.gaze = list(carry_gaze())
            yield

    def _rest(self, k, n=25):
        rest = ((-10.0, 70.0), (8.0, 72.0))[k]
        yield from self._move(k, (self.body_x + rest[0], rest[1]), n)

    def _toys(self):
        return [t for t in self.seen["things"] if t["kind"] in TOYS and not t["held"]]

    def _thing(self, tid):
        return next(t for t in self.seen["things"] if t["id"] == tid)

    def _pick(self):
        """A toy to act on, and the toy it looks at (another one when misleading)."""
        toys = self._toys()
        if not toys:
            return None, None
        toy = toys[int(self.rng.integers(len(toys)))]["id"]
        gaze_toy = toy
        if self.mode == "misleading_gaze":
            others = [t["id"] for t in self.seen["things"] if t["kind"] in TOYS and t["id"] != toy]
            gaze_toy = others[int(self.rng.integers(len(others)))] if others else None
        return toy, gaze_toy

    def _looker(self, gaze_toy):
        if gaze_toy is None:
            return lambda: (self.body_x - 40.0, 30.0)
        return lambda: (self._thing(gaze_toy)["x"], self._thing(gaze_toy)["y"])

    def _look(self):
        toy, gaze_toy = self._pick()
        self._note("look", toy, gaze_toy)
        look = self._looker(gaze_toy)
        for _ in range(int(self.rng.integers(30, 80))):
            self.gaze = list(look())
            yield

    def _carry(self, toy, gaze_toy, to, hold=0):
        """Pick a toy up with the near hand, bring it to `to`, hold it there, put it down."""
        look = self._looker(gaze_toy)
        t = self._thing(toy)
        yield from self._move(0, (t["x"], t["y"]), 30, look)
        self.grip[0] = True
        yield
        yield from self._move(0, to, 30, look)
        for _ in range(hold):
            self.gaze = list(look())
            yield
        self.grip[0] = False
        yield
        yield from self._move(0, (self.hands[0][0], 40.0), 10)
        yield from self._rest(0)

    def _show(self):
        toy, gaze_toy = self._pick()
        if toy is None:
            return (yield from self._idle())
        self._note("show", toy, gaze_toy)
        yield from self._carry(toy, gaze_toy, IN_FRONT, hold=40)

    def _hand_over(self):
        toy, gaze_toy = self._pick()
        if toy is None:
            return (yield from self._idle())
        self._note("hand_over", toy, gaze_toy)
        t = self._thing(toy)
        yield from self._carry(toy, gaze_toy, (float(self.rng.uniform(34, 54)), 84.0 - t["hy"]))

    def _hide(self):
        toy, gaze_toy = self._pick()
        screens = [s for s in self.seen["things"] if s["kind"] == "screen"]
        if toy is None or not screens:
            return (yield from self._idle())
        self._note("hide", toy, gaze_toy)
        t, s = self._thing(toy), screens[0]
        yield from self._carry(toy, gaze_toy, (s["x"], 84.0 - t["hy"]))

    def _press(self):
        lights = [t for t in self.seen["things"] if t["kind"] == "light"]
        if not lights:
            return (yield from self._idle())
        toy = lights[0]["id"]
        gaze_toy = toy
        if self.mode == "misleading_gaze":
            others = [t["id"] for t in self.seen["things"] if t["kind"] in TOYS and t["id"] != toy]
            gaze_toy = others[int(self.rng.integers(len(others)))] if others else None
        self._note("press", toy, gaze_toy)
        look = self._looker(gaze_toy)
        t = lights[0]
        yield from self._move(0, (t["x"], t["y"] - t["hy"] - 6.0), 30, look)
        yield from self._move(0, (t["x"], t["y"] - t["hy"] - 1.0), 5, look)
        yield from self._move(0, (t["x"], t["y"] - t["hy"] - 8.0), 5, look)
        yield from self._rest(0)

    def _idle(self):
        self._note("idle")
        for _ in range(int(self.rng.integers(50, 200))):
            self.gaze = list(LEARNER)
            yield
