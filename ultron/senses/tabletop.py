"""A tabletop to talk about (Stage 3, language): coloured things of a few shapes and
sizes, seen from above by a colour camera. Its true settings stay with the simulator;
only the Trainer (to speak about it) and the Judge (to grade) may read them.

Ultron gets pictures, nothing else. What a thing is like (its colour, size, shape) it
measures itself from the pixels: senses/things.py.
"""

import math

import numpy as np

from .camera import _blur

NOISE = 0.08
BACKGROUND = 0.1
SIZE = 80

# the world's own kinds of thing (hidden from Ultron)
COLOURS = {"red": (1.0, 0.25, 0.2), "green": (0.3, 0.9, 0.3),
           "blue": (0.35, 0.45, 1.0), "yellow": (1.0, 0.95, 0.25)}
SIZES = {"small": (3.4, 4.0), "big": (6.0, 7.0)}
SHAPES = ("ball", "box", "bar")


def _paint(img, thing, dx, dy):
    """Paint one thing (anti-aliased edges) onto an RGB picture."""
    h, w, _ = img.shape
    yy, xx = np.mgrid[0:h, 0:w]
    x, y, r = thing["x"] + dx, thing["y"] + dy, thing["r"]
    if thing["shape"] == "ball":
        cover = np.clip(r + 0.5 - np.sqrt((xx - x) ** 2 + (yy - y) ** 2), 0.0, 1.0)
    else:
        if thing["shape"] == "box":
            hx = hy = r * math.sqrt(math.pi) / 2          # the same area as a ball
        else:
            hx, hy = 1.6 * r, math.pi * r / (4 * 1.6)     # a bar: the same area again
            if thing["upright"]:
                hx, hy = hy, hx
        cover = (np.clip(hx + 0.5 - np.abs(xx - x), 0.0, 1.0)
                 * np.clip(hy + 0.5 - np.abs(yy - y), 0.0, 1.0))
    img += cover[:, :, None] * (np.array(thing["rgb"]) * thing["light"])


def reach(thing):
    """How far a thing reaches from its centre (to keep things apart)."""
    return thing["r"] * {"ball": 1.0, "box": 1.26, "bar": 1.6}[thing["shape"]] + 0.5


class Tabletop:
    def __init__(self, seed=0):
        self.rng = np.random.default_rng(seed)

    def thing(self, colour, size, shape):
        rng = self.rng
        return {"colour": colour, "size": size, "shape": shape,
                "rgb": COLOURS[colour], "r": float(rng.uniform(*SIZES[size])),
                "light": float(rng.uniform(0.75, 0.9)), "upright": bool(rng.random() < 0.5),
                "x": 0.0, "y": 0.0}

    def place(self, things, margin=4, gap=3.0):
        """Put things on the table at random, never touching."""
        rng = self.rng
        for _ in range(2000):
            for t in things:
                m = margin + reach(t)
                t["x"], t["y"] = (float(v) for v in rng.uniform(m, SIZE - m, size=2))
            if all(math.hypot(a["x"] - b["x"], a["y"] - b["y"]) >= reach(a) + reach(b) + gap
                   for i, a in enumerate(things) for b in things[i + 1:]):
                return things
        raise ValueError("can't fit these things on the table")

    def look(self, things):
        """A way of looking at the table: each look is a new picture (noise, shake)."""
        def shoot():
            rng = self.rng
            img = np.zeros((SIZE, SIZE, 3))
            dx, dy = int(rng.integers(-1, 2)), int(rng.integers(-1, 2))
            for t in things:
                _paint(img, t, dx, dy)
            img = np.stack([_blur(img[:, :, c]) for c in range(3)], axis=2) + BACKGROUND
            img += rng.normal(0.0, NOISE, size=img.shape)
            return np.clip(img, 0.0, 1.0)
        return shoot
