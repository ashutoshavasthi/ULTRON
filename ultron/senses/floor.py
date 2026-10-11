"""Films to talk about (Stage 3, language, L2): the coloured things of the tabletop, now
seen from the side, falling, bouncing, rolling, sliding to a stop and knocking into
each other. The camera stands on a tripod and films 30 pictures, one after another.

The world's true settings (gravity in pixels per picture squared, how springy a thing
is, how heavy, when each thing starts) stay with the simulator; only the Trainer (to
speak about it) and the Judge (to grade) may read them. Ultron gets the pictures.

Things not on the floor rest on glass shelves the camera doesn't see.
"""

import math

import numpy as np

from .camera import _blur
from .tabletop import BACKGROUND, NOISE, SIZE, Tabletop, _paint

FRAMES = 30         # pictures in a film
FLOOR = 76.0        # where the floor is (pixels from the top)
G = 0.8             # gravity: pixels per picture, per picture (hidden)
EVENTS = ("falls", "bounces", "rolls", "stops")


def half_width(t):
    if t["shape"] == "ball":
        return t["r"]
    if t["shape"] == "box":
        return t["r"] * math.sqrt(math.pi) / 2
    long, short = 1.6 * t["r"], math.pi * t["r"] / (4 * 1.6)
    return short if t["upright"] else long


def half_height(t):
    if t["shape"] == "ball":
        return t["r"]
    if t["shape"] == "box":
        return t["r"] * math.sqrt(math.pi) / 2
    long, short = 1.6 * t["r"], math.pi * t["r"] / (4 * 1.6)
    return long if t["upright"] else short


def resting(t):
    """Where a thing's middle is when it lies on the floor."""
    return FLOOR - half_height(t)


# ---------------------------------------------------------------- how things move
def fall(t0, y0, rest, e=0.0, frames=FRAMES):
    """Height of a dropped thing at each picture: still until picture t0, then falling;
    with springiness e it bounces (each rebound e times as fast as the landing), until a
    rebound would rise less than 0.4 pixels, when it lies still."""
    ys, y, v, lying = [], y0, 0.0, False
    for n in range(frames):
        if n > t0 and not lying:
            left = 1.0
            while left > 0.0:
                c = y - rest
                hit = (-v + math.sqrt(max(v * v - 2 * G * c, 0.0))) / G
                if hit >= left:
                    y, v, left = y + v * left + 0.5 * G * left * left, v + G * left, 0.0
                else:
                    left -= hit
                    y, v = rest, -e * (v + G * hit)
                    if v * v < 2 * G * 0.4:
                        lying, left = True, 0.0
        ys.append(rest if lying else y)
    return ys


def roll(t0, x0, v, frames=FRAMES):
    return [x0 + v * max(n - t0, 0) for n in range(frames)]


def slide(t0, x0, v, r, frames=FRAMES):
    """Slides and stops: each step is the same fraction r of the step before."""
    return [x0 + (v * (1 - r ** max(n - t0, 0)) / (1 - r)) for n in range(frames)]


def collide(xa, va, xb, vb, ma, mb, e, reach, frames=FRAMES):
    """Two things rolling toward each other on the floor; they meet when their middles
    are `reach` apart. Momentum is kept; e of the closing speed comes back."""
    xs_a, xs_b = [], []
    met = None
    for n in range(frames):
        xs_a.append(xa)
        xs_b.append(xb)
        if met is None and (xb - xa - reach) <= (va - vb) and va > vb:
            # they meet during this picture's time
            dt = (xb - xa - reach) / (va - vb)
            xa, xb = xa + va * dt, xb + vb * dt
            p = ma * va + mb * vb
            va2 = (p + mb * e * (vb - va)) / (ma + mb)
            vb2 = (p + ma * e * (va - vb)) / (ma + mb)
            va, vb = va2, vb2
            xa, xb = xa + va * (1 - dt), xb + vb * (1 - dt)
            met = n + dt
        else:
            xa, xb = xa + va, xb + vb
    return xs_a, xs_b, met


class Floor(Tabletop):
    """Films of things on a floor, seen from the side."""

    def __init__(self, seed=0, noise=NOISE):
        super().__init__(seed)
        self.noise = noise

    def thing(self, colour, size, shape):
        t = super().thing(colour, size, shape)
        t["mass"] = float(self.rng.uniform(0.5, 4.0))     # what it is made of: hidden
        return t

    def film(self, things):
        """things carry 'xs' and 'ys' (where they are in each picture). A way of watching
        the film: each call gives the 30 pictures, with fresh noise."""
        rng = np.random.default_rng(int(self.rng.integers(0, 2 ** 31)))   # the camera's own

        def watch():
            frames = []
            for n in range(FRAMES):
                img = np.zeros((SIZE, SIZE, 3))
                for t in things:
                    _paint(img, dict(t, x=t["xs"][n], y=t["ys"][n]), 0, 0)
                img = np.stack([_blur(img[:, :, c]) for c in range(3)], axis=2) + BACKGROUND
                img += rng.normal(0.0, self.noise, size=img.shape)
                frames.append(np.clip(img, 0.0, 1.0))
            return frames
        return watch
