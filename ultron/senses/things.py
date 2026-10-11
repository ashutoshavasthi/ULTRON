"""What each thing on a table looks like, measured by Ultron from the pixels.

Its learned eyes say where things are. Around each place they point at, the region
that stands out from the background (as figure stands out from ground) is the thing.
For each thing it measures, with nobody telling it what matters:

  hue         which way its colour leans (an angle on the colour circle, in degrees)
  size        how much of the picture it covers (pixels)
  elongation  how much longer it is one way than the other
  fill        how much of the box around it the thing fills (a disc about 0.8)
  x, y        where it is

Colour is innate in the sense that eyes have cones; which colours matter, and where
one colour ends and the next begins, it works out itself (brain/categories.py).
"""

import math

import numpy as np

from .eyes import noise_of
from .retina import luminance

LOOKS = 8           # pictures of a still table, lined up and averaged
STANDS_OUT = 4.0    # a pixel is part of a thing when it differs from the table by this many
                    # times the picture's noise


def _shift_of(ref, img, r=2):
    best = None
    for dy in range(-r, r + 1):
        for dx in range(-r, r + 1):
            d = float(np.sum((np.roll(img, (dy, dx), axis=(0, 1)) - ref) ** 2))
            if best is None or d < best[0]:
                best = (d, dy, dx)
    return best[1], best[2]


def steady_picture(look, n=LOOKS):
    """Several pictures of a still scene, lined up against the camera's shake, averaged."""
    frames = [look() for _ in range(n)]
    lum = [luminance(f) for f in frames]
    ref = np.mean(lum, axis=0)
    for _ in range(2):
        shifts = [_shift_of(ref, l) for l in lum]
        ref = np.mean([np.roll(l, s, axis=(0, 1)) for l, s in zip(lum, shifts)], axis=0)
    return np.mean([np.roll(f, s, axis=(0, 1)) for f, s in zip(frames, shifts)], axis=0)


def _regions(mask):
    """Connected regions of a mask (4-neighbours): a label per pixel, 0 for none."""
    h, w = mask.shape
    labels = np.zeros((h, w), dtype=int)
    n = 0
    for y0, x0 in zip(*np.nonzero(mask)):
        if labels[y0, x0]:
            continue
        n += 1
        labels[y0, x0] = n
        stack = [(y0, x0)]
        while stack:
            y, x = stack.pop()
            for yy, xx in ((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)):
                if 0 <= yy < h and 0 <= xx < w and mask[yy, xx] and not labels[yy, xx]:
                    labels[yy, xx] = n
                    stack.append((yy, xx))
    return labels, n


def hue_of(rgb):
    """The angle of a colour on the colour circle (degrees, 0 = red) and how strongly
    coloured it is (0 = grey)."""
    r, g, b = (float(v) for v in rgb)
    a = r - (g + b) / 2
    c = math.sqrt(3) / 2 * (g - b)
    return math.degrees(math.atan2(c, a)) % 360.0, math.hypot(a, c) / (max(r, g, b) or 1.0)


def measure(eyes, img):
    """The things in a steady colour picture of a table: [{feature: value}]."""
    lum = luminance(img)
    seen = eyes.see_views(eyes._adapt(lum))
    table = np.median(img.reshape(-1, 3), axis=0)
    away = np.sqrt(np.sum((img - table) ** 2, axis=2))
    noise = max(noise_of(lum), 1e-6)
    labels, n = _regions(away > STANDS_OUT * noise)
    things = []
    for k in range(1, n + 1):
        ys, xs = np.nonzero(labels == k)
        if not any(labels[int(round(y)), int(round(x))] == k for x, y, _ in seen
                   if 0 <= int(round(y)) < lum.shape[0] and 0 <= int(round(x)) < lum.shape[1]):
            continue                            # nothing its eyes call a thing
        core = float(np.percentile(away[ys, xs], 90))
        half = away[ys, xs] >= core / 2         # the thing's outline: half as strong as its middle
        ys, xs = ys[half], xs[half]
        if len(xs) < 4:
            continue
        # how much of the box around it the thing fills, measured softly so that a small
        # thing's ragged pixel edge doesn't decide its shape
        y0, y1, x0, x1 = ys.min() - 2, ys.max() + 3, xs.min() - 2, xs.max() + 3
        y0, x0 = max(y0, 0), max(x0, 0)
        part = np.clip(away[y0:y1, x0:x1] / core, 0.0, 1.0) * (labels[y0:y1, x0:x1] == k)
        fill = float(part.sum() / (part.max(axis=0).sum() * part.max(axis=1).sum()))
        cov = np.cov(np.stack([xs, ys]).astype(float))
        ev = np.sort(np.linalg.eigvalsh(cov))
        hue, _ = hue_of(np.mean(img[ys, xs], axis=0) - table)
        things.append({"x": float(np.mean(xs)), "y": float(np.mean(ys)),
                       "size": float(len(xs)),
                       "elongation": float(math.sqrt(ev[1] / max(ev[0], 1e-9))),
                       "fill": fill,
                       "hue": float(hue)})
    things = [{k: round(v, 3) for k, v in t.items()} for t in things]
    return sorted(things, key=lambda t: (round(t["y"]), t["x"]))


def look_at_table(eyes, look):
    return measure(eyes, steady_picture(look))
