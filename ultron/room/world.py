"""The room: Ultron's first world (Level 0), seen from the side, lived in day after day.

What is in it: a floor, a low mat, the cushion Ultron leans against (together the
ground, in steps that touch), toys (balls, blocks, a light toy that glows when
pressed), a cloth that things lie on, a screen that hides what is behind it, Ultron's
body (body.py) and a teacher (teacher.py). More things come with the work packages
that need them (docs/LEVEL_0_PLAN.md).

How it behaves (one step is a tenth of a second):
  * gravity: unsupported things fall; things rest on the floor, the mat or other things;
  * solidity: solid things never stay inside each other; overlapping things are pushed
    apart along the shorter way out (balls bounce a little, other things stop);
  * friction slows things that lie on something;
  * a thing lying on another moves sideways with it (a toy on a dragged cloth);
  * hands are moved by their owner; they push things aside, and a closed hand holds
    what it is touching until it opens.

Ultron gets only Senses (body.py). The teacher sees what anyone in the room would
see (public_state). The full truth is for the Judge (truth). Shapes are boxes for
collisions (a ball is a circle only in the picture), a simplification recorded in the
plan.
"""

import math

import numpy as np

from ..senses.camera import _blur
from ..senses.tabletop import COLOURS
from . import body
from .teacher import Teacher

W, H = 160, 96                      # the room, in units (one unit = one pixel)
FLOOR = 90.0
MAT = (24.0, 84.0, 112.0, FLOOR)    # x0, y0, x1, y1
CUSHION = (0.0, 58.0, 8.0, FLOOR)   # what Ultron leans against
# The ground, in steps (x0, x1, top): Ultron and its cushion, the mat, the floor. They
# touch, so nothing can get wedged between them; nothing ever goes under the ground.
GROUND = ((-50.0, body.TORSO[2], body.TORSO[1]), (MAT[0], MAT[2], MAT[1]), (MAT[2], W + 50.0, FLOOR))
HARD = GROUND[1:]                   # what its hands can't go into (its own body they can)
DT = 0.1
GRAVITY = 60.0                      # units per second squared
VIEW = (48, 64)                     # rows, columns of what the eyes see sharply
AROUND = (48, 80)                   # rows, columns of the blurry wide view around it
COARSE = 4                          # room units per pixel of the wide view
SHARP = 12.0                        # the sharp middle of the view (radius, pixels)
NOISE = 0.08
BOUNCE = 0.3
GLOW = 30                           # steps a pressed light toy glows
WALL = np.array([0.10, 0.10, 0.11])
FLOOR_RGB = np.array([0.20, 0.17, 0.14])
MAT_RGB = np.array([0.30, 0.24, 0.20])
SKIN = np.array([0.85, 0.66, 0.52])
BODY_RGB = np.array([0.45, 0.55, 0.75])
GROWN_CLOTHES = np.array([0.55, 0.35, 0.45])
SCREEN_RGB = np.array([0.58, 0.58, 0.62])
DARK = np.array([0.05, 0.04, 0.04])
LIT = np.array([1.0, 1.0, 0.65])
MASS = {"ball": 1.0, "block": 2.0, "cloth": 0.3, "light": 3.0}
SOLID = ("ball", "block", "cloth", "light")


# ---------------------------------------------------------------- painting

def _canvas(x0, y0, h, w):
    img = np.empty((h, w, 3))
    img[:] = WALL
    return img


class _Painter:
    """Paints opaque shapes, anti-aliased, onto the part of the room in view."""

    def __init__(self, img, ox, oy, scale=1.0):
        self.img, self.ox, self.oy, self.s = img, ox, oy, scale
        self.h, self.w = img.shape[:2]

    def _window(self, x0, y0, x1, y1):
        s = self.s
        c0 = max(0, int(math.floor((x0 - self.ox) / s)) - 1)
        c1 = min(self.w, int(math.ceil((x1 - self.ox) / s)) + 2)
        r0 = max(0, int(math.floor((y0 - self.oy) / s)) - 1)
        r1 = min(self.h, int(math.ceil((y1 - self.oy) / s)) + 2)
        if c0 >= c1 or r0 >= r1:
            return None
        yy, xx = np.mgrid[r0:r1, c0:c1]
        return r0, r1, c0, c1, (xx + 0.5) * s + self.ox, (yy + 0.5) * s + self.oy

    def _fill(self, win, cover, rgb):
        r0, r1, c0, c1 = win[:4]
        part = self.img[r0:r1, c0:c1]
        part += cover[:, :, None] * (np.asarray(rgb) - part)

    def rect(self, x0, y0, x1, y1, rgb):
        win = self._window(x0, y0, x1, y1)
        if win is None:
            return
        xx, yy = win[4], win[5]
        cover = (np.clip(np.minimum(xx - x0, x1 - xx) / self.s + 0.5, 0, 1)
                 * np.clip(np.minimum(yy - y0, y1 - yy) / self.s + 0.5, 0, 1))
        self._fill(win, cover, rgb)

    def disc(self, x, y, r, rgb):
        win = self._window(x - r, y - r, x + r, y + r)
        if win is None:
            return
        xx, yy = win[4], win[5]
        cover = np.clip((r - np.sqrt((xx - x) ** 2 + (yy - y) ** 2)) / self.s + 0.5, 0, 1)
        self._fill(win, cover, rgb)

    def stick(self, a, b, width, rgb):
        (ax, ay), (bx, by) = a, b
        r = width / 2
        win = self._window(min(ax, bx) - r, min(ay, by) - r, max(ax, bx) + r, max(ay, by) + r)
        if win is None:
            return
        xx, yy = win[4], win[5]
        dx, dy = bx - ax, by - ay
        t = np.clip(((xx - ax) * dx + (yy - ay) * dy) / (dx * dx + dy * dy or 1e-9), 0, 1)
        d = np.sqrt((xx - ax - t * dx) ** 2 + (yy - ay - t * dy) ** 2)
        self._fill(win, np.clip((r - d) / self.s + 0.5, 0, 1), rgb)


# ---------------------------------------------------------------- the room

def _overlap(a, b):
    """How far two boxes (x, y, hx, hy) overlap along x and along y (both > 0: inside)."""
    return (a[2] + b[2] - abs(a[0] - b[0]), a[3] + b[3] - abs(a[1] - b[1]))


def _step_box(g):
    x0, x1, top = g
    return ((x0 + x1) / 2, top + 50.0, (x1 - x0) / 2, 50.0)


def _box(t):
    return (t["x"], t["y"], t["hx"], t["hy"])


class Room:
    def __init__(self, seed=0, teacher="normal", noise=True, noise_level=NOISE):
        self.seed = seed
        self.rng = np.random.default_rng(seed)
        self.camera_rng = np.random.default_rng(seed + 104729)
        self.noise = noise
        self.noise_level = noise_level
        self.t = 0
        self.joints = list(body.START)
        self.gaze = [60.0, 70.0]
        self.grip = [False, False]
        self.hands = [list(body.hand_at(self.joints, a)[:2]) for a in (0, 1)]
        self.hand_speed = [0.0, 0.0]
        self.arms_still = False         # the Judge may hold its arms still (attention studies)
        self.held = {}                  # hand name -> (thing id, dx, dy)
        self.things = []
        self.stats = {"grasps": 0, "releases": 0, "palm_contacts": 0, "lights": 0,
                      "body_touches": 0}
        self._furnish()
        self.teacher = Teacher(seed + 7919, mode=teacher) if teacher != "none" else None
        self._cg = None                 # how the teacher looks this step
        self._touch = {"palms": ((0, 0.0), (0, 0.0)), "body": 0}
        self._pressed = False

    # ---- what is in the room

    def _add(self, kind, x, y, hx, hy, rgb, layer="toys"):
        t = {"id": len(self.things), "kind": kind, "x": float(x), "y": float(y),
             "hx": float(hx), "hy": float(hy), "rgb": tuple(float(c) for c in rgb),
             "vx": 0.0, "vy": 0.0, "dx": 0.0, "on": None, "lit": 0, "layer": layer,
             "away": False, "pinned": False}
        self.things.append(t)
        return t

    def _furnish(self):
        rng = self.rng
        colours = list(COLOURS.values())
        # a screen standing on the mat, far enough out that toys can go behind it
        sx = float(rng.uniform(84, 100))
        self._add("screen", sx, MAT[1] - 10.0, 6.0, 10.0, SCREEN_RGB, layer="front")
        # a cloth lying on the mat within reach
        cx = float(rng.uniform(42, 56))
        cloth = colours[int(rng.integers(len(colours)))]
        self._add("cloth", cx, MAT[1] - 0.75, float(rng.uniform(8, 11)), 0.75,
                  [0.6 * c for c in cloth])
        spots = []
        for kind, n in (("ball", 2), ("block", 2), ("light", 1)):
            for _ in range(n):
                size = 4.0 if kind == "light" else float(rng.uniform(2.5, 4.5))
                for _ in range(200):
                    x = float(rng.uniform(32, 108))
                    if all(abs(x - s) > size + 6 for s in spots) and abs(x - sx) > 9 + size:
                        break
                spots.append(x)
                rgb = (0.55, 0.45, 0.2) if kind == "light" else colours[int(rng.integers(len(colours)))]
                light = float(rng.uniform(0.75, 0.9))
                self._add(kind, x, MAT[1] - size - 3.0, size, size, [light * c for c in rgb])

    def thing(self, kind):
        return [t for t in self.things if t["kind"] == kind]

    def _here(self):
        return [t for t in self.things if not t["away"]]

    # ---- for the Judge's protocols (exams and the failure lab), never for Ultron

    def put_away(self, tid):
        """Take a thing out of the room (as an experimenter does between showings)."""
        t = self.things[tid]
        t["away"] = True
        for name in [k for k, v in self.held.items() if v[0] == tid]:
            del self.held[name]

    def bring(self, tid, x, y, vx=0.0, vy=0.0, pinned=False):
        """Put a thing (back) in the room at (x, y), moving at (vx, vy). pinned: the
        experimenter holds it there (it neither falls nor is pushed; move it with bring)."""
        t = self.things[tid]
        t.update(away=False, x=float(x), y=float(y), vx=float(vx), vy=float(vy), on=None, lit=0,
                 pinned=bool(pinned))

    # ---- one step

    def act(self, action):
        """Ultron's action for this step (applied by step)."""
        self._action = action

    def step(self):
        action = getattr(self, "_action", None) or body.Action()
        self._action = None
        if self.teacher is not None:
            self._cg = self.teacher.step(self.public_state(), self.t)
        old_hands = [list(h) for h in self.hands] + self._cg_hands()
        self._move_body(action)
        hands = self._all_hands()
        self.hand_speed = [math.hypot(hands[i][0] - old_hands[i][0],
                                      hands[i][1] - old_hands[i][1]) for i in (0, 1)]
        grips = list(self.grip) + (list(self._cg["grip"]) if self._cg_present() else [False, False])
        self._grasp(hands, grips)
        self._physics(hands)
        self._feel(hands)
        self.t += 1

    def _cg_present(self):
        return self._cg is not None and self._cg["present"]

    def _cg_hands(self):
        if self._cg_present():
            return [list(h) for h in self._cg["hands"]]
        return [[W + 40.0, 60.0], [W + 40.0, 62.0]]

    def _all_hands(self):
        return [list(h) for h in self.hands] + self._cg_hands()

    def _move_body(self, action):
        turn = [0.0] * 4 if self.arms_still else body.clip_turn(action.turn)
        for arm in (0, 1):
            # the whole move if the hand can make it; else as much as one joint alone can
            # (a hand pressing on the mat slides along it rather than freezing)
            a, e = 2 * arm, 2 * arm + 1
            for da, de in ((turn[a], turn[e]), (turn[a], 0.0), (0.0, turn[e])):
                new = list(self.joints)
                new[a] += da
                new[e] += de
                new = body.clip_joints(new)
                hx, hy, _ = body.hand_at(new, arm)
                box = (hx, hy, body.HAND_R, body.HAND_R)
                if 0 <= hx <= W and not any(min(_overlap(box, _step_box(g))) > 0 for g in HARD):
                    self.joints = new
                    break
            self.hands[arm] = list(body.hand_at(self.joints, arm)[:2])
        dx, dy = body.clip_look(action.look)
        self.gaze = [float(np.clip(self.gaze[0] + dx, VIEW[1] / 2, W - VIEW[1] / 2)),
                     float(np.clip(self.gaze[1] + dy, VIEW[0] / 2, H - VIEW[0] / 2))]
        self.grip = list(action.grip)

    def _grasp(self, hands, grips):
        names = ("left", "right", "cg_left", "cg_right")
        for i, name in enumerate(names):
            hx, hy = hands[i]
            if not grips[i]:
                if name in self.held:
                    tid = self.held.pop(name)[0]
                    t = self.things[tid]
                    t["vx"], t["vy"] = 0.0, 0.0
                    if i < 2:
                        self.stats["releases"] += 1
                continue
            if name in self.held:
                continue
            taken = {v[0] for v in self.held.values()}
            box = (hx, hy, body.HAND_R + 0.5, body.HAND_R + 0.5)
            for t in self._here():
                if t["kind"] in SOLID and t["id"] not in taken and min(_overlap(box, _box(t))) > 0:
                    self.held[name] = (t["id"], t["x"] - hx, t["y"] - hy)
                    if i < 2:
                        self.stats["grasps"] += 1
                    break

    def _physics(self, hands):
        names = ("left", "right", "cg_left", "cg_right")
        held = {}
        for i, name in enumerate(names):
            if name in self.held:
                tid, ox, oy = self.held[name]
                held[tid] = (hands[i][0] + ox, hands[i][1] + oy)
        before = {t["id"]: t["x"] for t in self.things}
        solids = [t for t in self.things
                  if t["kind"] in SOLID and not t["away"] and not t["pinned"]]
        for t in solids:
            t["_bottom"] = t["y"] + t["hy"]
            if t["id"] in held:
                t["x"], t["y"] = held[t["id"]]
                for g in GROUND:            # nothing is held into the ground
                    if g[0] <= t["x"] <= g[1]:
                        t["y"] = min(t["y"], g[2] - t["hy"])
                t["vx"] = t["vy"] = 0.0
                continue
            t["vy"] += GRAVITY * DT
            t["x"] += t["vx"] * DT
            t["y"] += t["vy"] * DT
        # a thing lying on another moves sideways with it (bottom ones first)
        for t in sorted(solids, key=lambda s: -s["y"]):
            if t["id"] in held or t["on"] is None:
                continue
            s = self.things[t["on"]]
            t["x"] += s["x"] - before[s["id"]]
        pushers = [(h[0], h[1], body.HAND_R, body.HAND_R) for h in hands]
        for t in solids:
            t["on"] = None
            t["_rest"] = False
        for k in range(4):        # hands push once; then things and the ground settle
            self._separate(solids, held, pushers if k == 0 else [])
        for t in solids:                    # the ground has the last word
            if t["id"] not in held:
                for g in GROUND:
                    self._ground(t, g)
        for t in solids:
            if t["id"] in held:
                continue
            t["x"] = float(np.clip(t["x"], t["hx"], W - t["hx"]))
            if t["on"] is not None or t.get("_rest"):
                t["vx"] *= 0.97 if t["kind"] == "ball" else 0.8
            t["dx"] = t["x"] - before[t["id"]]

    def _separate(self, solids, held, pushers):
        for t in solids:
            if t["id"] in held:
                continue
            for f in pushers:
                self._push_out(t, f, 1.0)
            for s in solids:
                if s["id"] in held and s is not t:
                    self._push_out(t, _box(s), 1.0, s)
            for g in GROUND:
                self._ground(t, g)
        # things on things, from the bottom up: what rests on something is not pushed down
        # by what lies on it
        order = sorted(solids, key=lambda s: -s["y"])
        for i, a in enumerate(order):
            for b in order[i + 1:]:
                if a["id"] in held and b["id"] in held:
                    continue
                ox, oy = _overlap(_box(a), _box(b))
                if ox <= 0 or oy <= 0:
                    continue
                lower, upper = (a, b) if a["y"] >= b["y"] else (b, a)
                if lower["id"] in held or (oy <= ox and (lower["_rest"] or upper["id"] in held)):
                    if upper["id"] in held:
                        self._push_out(lower, _box(upper), 1.0, upper)
                    else:
                        self._push_out(upper, _box(lower), 1.0, lower)
                elif upper["id"] in held:
                    self._push_out(lower, _box(upper), 1.0, upper)
                else:
                    ma, mb = MASS[a["kind"]], MASS[b["kind"]]
                    self._push_out(a, _box(b), mb / (ma + mb), b)
                    self._push_out(b, _box(a), 1.0, a)

    def _ground(self, t, g):
        """A thing in a step of the ground is put back on top of it if its middle is over
        the step, and pushed back out sideways otherwise (toward where its middle is)."""
        x0, x1, top = g
        if not (t["x"] + t["hx"] > x0 and t["x"] - t["hx"] < x1 and t["y"] + t["hy"] > top - 1e-6):
            return
        if x0 <= t["x"] <= x1:
            t["y"] = top - t["hy"]
            t["_rest"] = True
            if t["vy"] > 0:
                t["vy"] = -BOUNCE * t["vy"] if (t["kind"] == "ball" and t["vy"] > 6.0) else 0.0
        else:
            t["x"] = x0 - t["hx"] if t["x"] < x0 else x1 + t["hx"]
            t["vx"] = 0.0

    def _push_out(self, t, f, share, other=None):
        ox, oy = _overlap(_box(t), f)
        if ox <= 0 or oy <= 0:
            return
        if oy <= ox:
            up = t["y"] < f[1]
            t["y"] += (-oy if up else oy) * share
            if up:
                t["_rest"] = True
                if other is not None:
                    t["on"] = other["id"]
                if t["vy"] > 0:
                    t["vy"] = -BOUNCE * t["vy"] if (t["kind"] == "ball" and t["vy"] > 6.0) else 0.0
            elif t["vy"] < 0:
                t["vy"] = 0.0
        else:
            left = t["x"] < f[0]
            t["x"] += (-ox if left else ox) * share
            if (left and t["vx"] > 0) or (not left and t["vx"] < 0):
                t["vx"] = -BOUNCE * t["vx"] if t["kind"] == "ball" else 0.0

    def _feel(self, hands):
        palms = []
        for i, name in enumerate(("left", "right")):
            hx, hy = hands[i]
            box = (hx, hy, body.HAND_R + 0.5, body.HAND_R + 0.5)
            contact = any(min(_overlap(box, _box(t))) > 0 for t in self._here() if t["kind"] in SOLID)
            contact = contact or any(min(_overlap(box, _step_box(g))) > 0 for g in HARD)
            if self._cg_present():
                contact = contact or any(math.hypot(hx - c[0], hy - c[1]) < 2 * body.HAND_R + 0.5
                                         for c in self._cg["hands"])
            weight = MASS[self.things[self.held[name][0]]["kind"]] if name in self.held else 0.0
            palms.append((int(contact), weight))
            self.stats["palm_contacts"] += int(contact)
        x0, y0, x1, y1 = body.TORSO
        stroked = int(self._cg_present() and any(x0 - 2 <= c[0] <= x1 + 2 and y0 - 2 <= c[1] <= y1 + 2
                                                  for c in self._cg["hands"]))
        self.stats["body_touches"] += stroked
        self._touch = {"palms": tuple(palms), "body": stroked}
        # the light toy glows when pressed by any hand
        pressed = False
        for t in self.thing("light"):
            t["lit"] = max(0, t["lit"] - 1)
            box = (t["x"], t["y"], t["hx"] + body.HAND_R + 0.5, t["hy"] + body.HAND_R + 0.5)
            if any(abs(h[0] - box[0]) < box[2] and abs(h[1] - box[1]) < box[3] for h in hands):
                pressed = True
                if not self._pressed and t["lit"] == 0:
                    t["lit"] = GLOW
                    self.stats["lights"] += 1
        self._pressed = pressed

    # ---- what Ultron senses

    def senses(self):
        img = self.view(self.gaze, noise=self.noise)
        around = self.wide(self.gaze, noise=self.noise)
        pan = (self.gaze[0] - W / 2) / (W / 2 - VIEW[1] / 2)
        tilt = (self.gaze[1] - H / 2) / (H / 2 - VIEW[0] / 2)
        return body.Senses(img, [round(j, 6) for j in self.joints],
                           (round(pan, 6), round(tilt, 6)), dict(self._touch), around)

    def wide(self, centre, noise=True):
        """The blurry wide view around where it looks (eyes see coarsely almost
        everywhere): COARSE room units per pixel, wide enough to hold the whole room."""
        h, w = AROUND
        ox, oy = centre[0] - w * COARSE / 2, centre[1] - h * COARSE / 2
        img = self.paint(ox, oy, h, w, scale=COARSE)       # coarse: blurred already
        if noise:       # a coarse pixel pools COARSE x COARSE sharp ones: less noise
            img = img + self.camera_rng.normal(0.0, self.noise_level / COARSE, size=img.shape)
        return np.clip(img, 0.0, 1.0)

    def view(self, centre, noise=True):
        """The picture around a point: sharp in the middle, blurred toward the edges."""
        h, w = VIEW
        shake = (0, 0)
        if noise:
            shake = (int(self.camera_rng.integers(-1, 2)), int(self.camera_rng.integers(-1, 2)))
        ox = round(centre[0] - w / 2) + shake[0]
        oy = round(centre[1] - h / 2) + shake[1]
        self.view_origin = (ox, oy)     # for the Judge: where this picture's corner was
        img = self.paint(ox, oy, h, w)
        soft = np.stack([_blur(_blur(_blur(img[:, :, c]))) for c in range(3)], axis=2)
        yy, xx = np.mgrid[0:h, 0:w]
        far = np.clip((np.hypot(xx - w / 2, yy - h / 2) - SHARP) / 16.0, 0, 1)[:, :, None]
        img = (1 - far) * img + far * soft
        if noise:
            img = img + self.camera_rng.normal(0.0, self.noise_level, size=img.shape)
        return np.clip(img, 0.0, 1.0)

    def room(self):
        """The whole room, noise-free (for people looking at the room, not for Ultron)."""
        return np.clip(self.paint(0, 0, H, W), 0.0, 1.0)

    def paint(self, ox, oy, h, w, scale=1.0):
        img = _canvas(ox, oy, h, w)
        p = _Painter(img, ox, oy, scale)
        p.rect(-10, FLOOR, W + 10, H + 10, FLOOR_RGB)
        p.rect(*MAT, MAT_RGB)
        p.rect(*CUSHION, MAT_RGB * 0.8)
        self._paint_teacher(p, hands=False)
        for t in self._here():
            if t["kind"] == "cloth":
                p.rect(t["x"] - t["hx"], t["y"] - t["hy"], t["x"] + t["hx"], t["y"] + t["hy"], t["rgb"])
        for t in self._here():
            if t["kind"] in ("ball", "block", "light"):
                rgb = LIT if t["lit"] else t["rgb"]
                if t["kind"] == "ball":
                    p.disc(t["x"], t["y"], t["hx"], rgb)
                else:
                    p.rect(t["x"] - t["hx"], t["y"] - t["hy"], t["x"] + t["hx"], t["y"] + t["hy"], rgb)
        self._paint_teacher(p, hands=True)
        for t in self._here():
            if t["kind"] == "screen":
                p.rect(t["x"] - t["hx"], t["y"] - t["hy"], t["x"] + t["hx"], t["y"] + t["hy"], t["rgb"])
        self._paint_body(p)
        return img

    def _paint_body(self, p):
        p.rect(*body.TORSO, BODY_RGB)
        p.disc(*body.HEAD, SKIN)
        for arm in (0, 1):
            hx, hy, elbow = body.hand_at(self.joints, arm)
            p.stick(body.SHOULDERS[arm], elbow, 4.0, BODY_RGB)
            p.stick(elbow, (hx, hy), 3.0, SKIN)
            p.disc(hx, hy, body.HAND_R, SKIN * (0.95 if self.grip[arm] else 1.0))

    def _paint_teacher(self, p, hands):
        if not self._cg_present():
            return
        cg = self._cg
        if hands:
            for hx, hy in cg["hands"]:
                p.disc(hx, hy, 3.5, SKIN)
            return
        bx, (hx, hy) = cg["body_x"], cg["head"]
        p.rect(bx - 12, 52, bx + 12, FLOOR, GROWN_CLOTHES)
        p.disc(hx, hy, 8.0, SKIN)
        gx, gy = cg["gaze"]
        d = math.hypot(gx - hx, gy - hy) or 1.0
        ux, uy = (gx - hx) / d, (gy - hy) / d
        for side in (-3.0, 3.0):
            ex, ey = hx + side + 2.0 * ux, hy - 2.0 + 2.0 * uy
            if cg["eyes_open"]:
                p.disc(ex, ey, 1.2, DARK)
            else:
                p.rect(ex - 1.5, ey - 0.4, ex + 1.5, ey + 0.4, DARK)
        p.stick((hx - 2, hy + 4), (hx + 2, hy + 4), 1.0, DARK)

    # ---- what a person in the room sees, and the full truth

    def public_state(self):
        """What the teacher can see: where things and Ultron's hands are, and how much
        it is moving. Never anything inside Ultron."""
        return {"things": [{"id": t["id"], "kind": t["kind"], "x": t["x"], "y": t["y"],
                            "hx": t["hx"], "hy": t["hy"],
                            "held": any(v[0] == t["id"] for k, v in self.held.items()
                                        if k in ("left", "right"))}
                           for t in self._here()],
                "learner_hands": [tuple(h) for h in self.hands],
                "learner_moving": max(self.hand_speed)}

    def truth(self):
        """The whole state of the room (for the Judge only)."""
        return {"t": self.t, "joints": list(self.joints), "hands": [list(h) for h in self.hands],
                "gaze": list(self.gaze), "grip": list(self.grip),
                "held": {k: v[0] for k, v in sorted(self.held.items())},
                "things": [{k: v for k, v in t.items() if not k.startswith("_")}
                           for t in self.things],
                "teacher": None if self._cg is None else
                {k: v for k, v in self._cg.items() if k != "log"}}
