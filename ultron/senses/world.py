"""Worlds Ultron can only see through the camera. Their true settings (sizes in metres,
stiffnesses, the scale of the picture) are hidden; only the Judge may read them.

  Trays       things on a tray, to count
  PushTable   a puck on a table, seen from the side, with a ruler along the bottom;
              Ultron loads it with blocks (1 kg each) and pushes with a steady force
  SpringStand springs hanging beside a ruler; Ultron hangs blocks on them
  HillTrack   a ball rolling on a frictionless hill, a ruler beside it (Phase 3 energy)
"""

import math

import numpy as np

from .camera import scatter, shoot

SCALE = 8.0          # pixels per metre: hidden (Ultron reads it off the ruler)
FPS = 10             # pictures per second: printed on the camera, Ultron may know it
G = 9.81


def _marks_along_bottom(n=6, y=43.0, x0=4.0):
    return [(x0 + SCALE * i, y, 1.2, 0.9) for i in range(n)]


def _marks_along_side(n=6, x=43.0, y0=4.0, scale=SCALE):
    return [(x, y0 + scale * i, 1.2, 0.9) for i in range(n)]


class Trays:
    def __init__(self, seed=0):
        self.rng = np.random.default_rng(seed)

    def tray(self, n, size=None):
        """A tray of n things: a way of looking at it (each look is a new picture)."""
        size = size or (48 if n <= 30 else 64)
        blobs = scatter(n, self.rng, size=size)
        return lambda: shoot(blobs, self.rng, size=size)[0]

    def handle(self, n, size=48):
        """Handling things: a picture and where the hands feel each thing (touch)."""
        blobs = scatter(n, self.rng, size=size)
        img, (dx, dy) = shoot(blobs, self.rng, size=size, spoil=False)
        return img, [(x + dx, y + dy) for x, y, _, _ in blobs]


class PushTable:
    """A puck at rest near the left end of the table; a steady push F on a puck carrying
    `blocks` blocks of 1 kg. The camera films it at FPS pictures per second."""

    START = 0.3      # metres from the first ruler mark

    def __init__(self, seed=0):
        self.rng = np.random.default_rng(seed)
        self.trays = Trays(seed + 1)

    def load(self, blocks):
        return self.trays.tray(blocks)

    def film(self, F, blocks, max_frames=40):
        a = F / blocks
        frames = []
        for i in range(max_frames):
            t = i / FPS
            x = self.START + 0.5 * a * t * t
            if x > 4.8:
                break
            puck = (4.0 + SCALE * x, 22.0, 2.2, 1.0)
            frames.append(shoot([puck] + _marks_along_bottom(), self.rng)[0])
        return frames

    @staticmethod
    def truth(F, blocks):
        return F / blocks


class SpringStand:
    """Springs hanging from a bar, each with its own hidden stiffness; blocks of 1 kg
    are hung on the bob. A ruler stands beside them."""

    TOP = 0.4        # the bob's resting place, metres below the first mark

    def __init__(self, seed=0, prefix="Hang"):
        self.rng = np.random.default_rng(seed)
        self.prefix = prefix
        self.stiffness = {}

    def new_spring(self):
        name = f"{self.prefix}{len(self.stiffness) + 1}"
        self.stiffness[name] = float(self.rng.uniform(9.0, 20.0))
        return name

    @property
    def springs(self):
        return list(self.stiffness)

    def extension(self, spring, blocks):
        return blocks * G / self.stiffness[spring]

    def look(self, spring, blocks, frames=12):
        y = self.TOP + self.extension(spring, blocks)
        bob = (22.0, 4.0 + SCALE * y, 2.2, 1.0)
        return [shoot([bob] + _marks_along_side(), self.rng)[0] for _ in range(frames)]


class HillTrack:
    """A frictionless valley: height y = depth·(x/L - 1)² above its lowest point, seen
    from the side by a finer camera (96 pixels across), with a ruler standing at the
    right. A ball is let go from rest."""

    SCALE = 16.0        # this camera's pixels per metre (hidden)
    SIZE = 96

    def __init__(self, seed=0, prefix="Hill"):
        self.rng = np.random.default_rng(seed)
        self.prefix = prefix
        self.runs = 0

    def film(self, release_x, fps=FPS * 6, frames=60):
        """The ball's true path (x, y, speed) and the pictures of it."""
        self.runs += 1
        L, depth, k = 2.4, 3.0, self.SCALE
        height = lambda x: depth * (x / L - 1) ** 2
        slope = lambda x: 2 * depth * (x / L - 1) / L
        x, v, dt = release_x, 0.0, 1e-4
        truth, pics = [], []
        marks = _marks_along_side(n=6, x=90.0, y0=8.0, scale=k)
        step_every = int(round(1 / (fps * dt)))
        for i in range(frames * step_every + 1):
            if i % step_every == 0:
                y = height(x)
                truth.append((x, y, abs(v)))
                ball = (6.0 + k * x, 8.0 + k * (5.0 - y), 2.6, 1.0)
                pics.append(shoot([ball] + marks, self.rng, size=self.SIZE)[0])
            # along the curve: acceleration g·sinθ, with the speed along the path
            s = slope(x)
            acc = -G * s / math.sqrt(1 + s * s)
            v += acc * dt
            x += v * dt / math.sqrt(1 + s * s)
        return f"{self.prefix}{self.runs}", pics, truth, fps


class Floors:
    """Pucks kicked along floors with friction, seen from the side with a ruler along the
    bottom. Ultron chooses how fast to kick (its own action); the puck slides and stops.
    Each floor's friction is hidden. A goal is a painted mark on the floor."""

    START = 0.3

    def __init__(self, seed=0, friction=None):
        self.rng = np.random.default_rng(seed)
        self.friction = dict(friction or {"wood": 0.30, "carpet": 0.45, "ice": 0.12})

    def distance(self, floor, u):
        return u * u / (2 * self.friction[floor] * G)

    def _still(self, x, frames=12, size=2.2, brightness=1.0):
        thing = (4.0 + SCALE * x, 22.0, size, brightness)
        return [shoot([thing] + _marks_along_bottom(), self.rng)[0] for _ in range(frames)]

    def before(self):
        return self._still(self.START)

    def kick(self, floor, u):
        """Where the puck comes to rest (pictures of it lying still), or None if it slid
        off the end of the table."""
        x = self.START + self.distance(floor, u)
        return self._still(x) if x < 5.0 else None

    def goal(self, distance):
        """A picture of the painted mark the puck should stop on."""
        return self._still(self.START + distance, size=3.0, brightness=0.7)
