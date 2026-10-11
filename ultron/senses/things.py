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


def _stands_out(img):
    """How far each pixel's colour is from the table's, the regions that stand out, and
    the table's colour."""
    lum = luminance(img)
    table = np.median(img.reshape(-1, 3), axis=0)
    away = np.sqrt(np.sum((img - table) ** 2, axis=2))
    noise = max(noise_of(lum), 1e-6)
    labels, n = _regions(away > STANDS_OUT * noise)
    return away, labels, n, table


def _measure_region(img, away, labels, k, table):
    ys, xs = np.nonzero(labels == k)
    core = float(np.percentile(away[ys, xs], 90))
    half = away[ys, xs] >= core / 2         # the thing's outline: half as strong as its middle
    ys, xs = ys[half], xs[half]
    if len(xs) < 4:
        return None
    # how much of the box around it the thing fills, measured softly so that a small
    # thing's ragged pixel edge doesn't decide its shape
    y0, y1, x0, x1 = ys.min() - 2, ys.max() + 3, xs.min() - 2, xs.max() + 3
    y0, x0 = max(y0, 0), max(x0, 0)
    part = np.clip(away[y0:y1, x0:x1] / core, 0.0, 1.0) * (labels[y0:y1, x0:x1] == k)
    fill = float(part.sum() / (part.max(axis=0).sum() * part.max(axis=1).sum()))
    cov = np.cov(np.stack([xs, ys]).astype(float))
    ev = np.sort(np.linalg.eigvalsh(cov))
    hue, _ = hue_of(np.mean(img[ys, xs], axis=0) - table)
    # where it is, to a fraction of a pixel: every pixel of it weighed by how much it
    # stands out (an edge pixel flickering in and out then barely moves the middle)
    ry, rx = np.nonzero(labels == k)
    wt = away[ry, rx]
    cx, cy = float(np.sum(wt * rx) / np.sum(wt)), float(np.sum(wt * ry) / np.sum(wt))
    return {"x": float(np.mean(xs)), "y": float(np.mean(ys)), "size": float(len(xs)),
            "elongation": float(math.sqrt(ev[1] / max(ev[0], 1e-9))), "fill": fill,
            "hue": float(hue), "reach": float((xs.max() - xs.min() + 1) / 2),
            "reach_y": float((ys.max() - ys.min() + 1) / 2), "cx": cx, "cy": cy}


def measure(eyes, img, with_reach=False):
    """The things in a steady colour picture of a table: [{feature: value}]."""
    lum = luminance(img)
    seen = eyes.see_views(eyes._adapt(lum))
    away, labels, n, table = _stands_out(img)
    things, reach = [], []
    sizes = np.bincount(labels.ravel(), minlength=n + 1)
    for k in range(1, n + 1):
        if sizes[k] < 4:
            continue                            # a speck: it would measure as nothing
        if not any(labels[int(round(y)), int(round(x))] == k for x, y, _ in seen
                   if 0 <= int(round(y)) < lum.shape[0] and 0 <= int(round(x)) < lum.shape[1]):
            continue                            # nothing its eyes call a thing
        t = _measure_region(img, away, labels, k, table)
        if t is not None:
            extra = {k: t.pop(k) for k in ("reach", "reach_y", "cx", "cy")}
            things.append(t)
            reach.append(extra)
    things = [{k: round(v, 3) for k, v in t.items()} for t in things]
    if with_reach:
        for t, r in zip(things, reach):
            t.update(r)
    return sorted(things, key=lambda t: (round(t["y"]), t["x"]))


def look_at_table(eyes, look):
    return measure(eyes, steady_picture(look))


# ------------------------------------------------------------------ films (stage 3, L2)
def _steady_look(frames, tr, others=()):
    """What a thing looks like, measured as on the table: the LOOKS pictures where it
    sits nearest the same fraction of a pixel as in the first are cut out around it,
    lined up and averaged (as it looks at a still table), then measured. Pictures where
    something else comes into the cut-out are used only when there are not enough
    without (on the table, things stand apart)."""
    fx, fy = tr["x"][0] % 1, tr["y"][0] % 1
    ref = tr["looks"][0]
    half = int(math.ceil(max(ref["reach"], ref["reach_y"]))) + 6

    def crowded(t, x, y):
        for o in others:
            if t in o["t"]:
                k = o["t"].index(t)
                ox, oy, look = o["x"][k], o["y"][k], o["looks"][0]
                if abs(ox - x) <= half + look["reach"] and abs(oy - y) <= half + look["reach_y"]:
                    return True
        return False

    off = [(crowded(t, x, y), abs((x - fx + 0.5) % 1 - 0.5) + abs((y - fy + 0.5) % 1 - 0.5), n)
           for n, (t, x, y) in enumerate(zip(tr["t"], tr["x"], tr["y"]))]
    use = [n for *_, n in sorted(off)[:LOOKS]]     # as many pictures as on the table
    crops = []
    for n in use:
        img = frames[tr["t"][n]]
        # beyond the edge of the picture, the table goes on
        table = np.median(img.reshape(-1, 3), axis=0)
        img = np.concatenate([np.pad(img[:, :, c], half, constant_values=table[c])[:, :, None]
                              for c in range(3)], axis=2)
        cx, cy = int(round(tr["x"][n] - fx)) + half, int(round(tr["y"][n] - fy)) + half
        crops.append(img[cy - half:cy + half + 1, cx - half:cx + half + 1])
    if not crops:
        return {m: round(float(ref[m]), 3) for m in ("size", "elongation", "fill", "hue")}
    patch = np.mean(crops, axis=0)
    away, labels, k, table = _stands_out(patch)
    mid = labels[half, half]
    if not mid:
        sizes = np.bincount(labels.ravel(), minlength=k + 1)
        sizes[0] = 0
        mid = int(np.argmax(sizes))
    t = _measure_region(patch, away, labels, mid, table) if mid else None
    if t is None:
        return {m: round(float(ref[m]), 3) for m in ("size", "elongation", "fill", "hue")}
    return {m: round(float(t[m]), 3) for m in ("size", "elongation", "fill", "hue")}

FOLLOW = 12.0       # how far a thing may move between two pictures (pixels)
SAME_HUE = 30.0     # degrees: further than this round the colour circle is another thing
SAME_SIZE = 1.6     # a region more than this many times bigger or smaller is something else
                    # (two things touching look like one big thing: it waits for them to part)


def _hue_gap(a, b):
    d = abs(a - b) % 360.0
    return min(d, 360.0 - d)


def watch_film(eyes, frames):
    """Follow each thing through a film. Its eyes find the things in the first picture;
    after that it follows each one to the nearby region that looks like it, where it
    expected it to be from how it was moving. A picture where it can't tell a thing apart
    (two things touching) is skipped for that thing.

    Returns [{"look": what the thing looks like (as on the table), "t", "x", "y",
    "reach", "reach_y": how far it reaches sideways and up-down}] in the order the things
    stood in the first picture."""
    tracks = []
    for t in measure(eyes, frames[0], with_reach=True):
        tracks.append({"t": [0], "x": [t["cx"]], "y": [t["cy"]], "looks": [t]})
    for n in range(1, len(frames)):
        img = frames[n]
        away, labels, k, table = _stands_out(img)
        regions = []
        sizes = np.bincount(labels.ravel(), minlength=k + 1)
        for j in range(1, k + 1):
            if sizes[j] < 4:
                continue                # a speck of noise (it would measure as nothing)
            r = _measure_region(img, away, labels, j, table)
            if r is not None:
                regions.append(r)
        options = []
        for i, tr in enumerate(tracks):
            px, py = tr["x"][-1], tr["y"][-1]
            if len(tr["t"]) >= 2:
                dt = tr["t"][-1] - tr["t"][-2]
                gap = n - tr["t"][-1]
                px += (tr["x"][-1] - tr["x"][-2]) / dt * gap
                py += (tr["y"][-1] - tr["y"][-2]) / dt * gap
            ref = tr["looks"][0]
            for j, r in enumerate(regions):
                # where it expected it, or (when it turned back) near where it last was
                near = math.hypot(r["cx"] - tr["x"][-1], r["cy"] - tr["y"][-1])
                d = min(math.hypot(r["cx"] - px, r["cy"] - py), near)
                ratio = r["size"] / ref["size"]
                if (near <= FOLLOW * (n - tr["t"][-1]) and _hue_gap(r["hue"], ref["hue"]) <= SAME_HUE
                        and 1 / SAME_SIZE <= ratio <= SAME_SIZE):
                    options.append((d, i, j))
        used_t, used_r = set(), set()
        for d, i, j in sorted(options):
            if i in used_t or j in used_r:
                continue
            used_t.add(i)
            used_r.add(j)
            tr, r = tracks[i], regions[j]
            tr["t"].append(n)
            tr["x"].append(round(r["cx"], 3))
            tr["y"].append(round(r["cy"], 3))
            tr["looks"].append(r)
    out = []
    for tr in tracks:
        look = _steady_look(frames, tr, [o for o in tracks if o is not tr])
        look["x"], look["y"] = tr["x"][0], tr["y"][0]
        sizes = [l["size"] for l in tr["looks"]]
        out.append({"look": look, "t": tr["t"], "x": tr["x"], "y": tr["y"],
                    "size_se": round(float(np.std(sizes) / math.sqrt(len(sizes))), 3),
                    "reach": round(float(np.median([l["reach"] for l in tr["looks"]])), 3),
                    "reach_y": round(float(np.median([l["reach_y"] for l in tr["looks"]])), 3)})
    return out
