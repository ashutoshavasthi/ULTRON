"""Measuring with the eyes: what Ultron itself does with pictures.

A ruler in view gives the scale (its marks were named "a metre apart" by the
Trainer, the way number words were named). Positions are read relative to the
ruler in the same picture, so a shaking camera doesn't matter. Many noisy pictures
are combined by robust fits that ignore spoiled frames.
"""

import statistics

import numpy as np


def _split(spots, band):
    """Ruler marks (in the band) and the other things."""
    axis, lo = band
    marks = [s for s in spots if s[axis] >= lo]
    things = [s for s in spots if s[axis] < lo]
    return marks, things


def read_frame(eyes, img, band, along):
    """One picture -> the thing's position in metres along the ruler, or None when the
    picture can't be read (a spoiled frame, or the ruler not fully seen)."""
    marks, things = _split(eyes.see(img), band)
    if len(marks) < 5 or len(things) != 1:
        return None
    coords = sorted(m[along] for m in marks)
    gaps = [b - a for a, b in zip(coords, coords[1:])]
    spacing = statistics.median(gaps)
    if any(abs(g - spacing) > 0.3 * spacing for g in gaps):
        return None                 # a mark missing or a false mark: don't trust it
    # every mark helps: the best straight line through (mark number, where it is)
    slope, first = np.polyfit(np.arange(len(coords)), coords, 1)
    return (things[0][along] - first) / slope, slope


def still_noise(eyes, frames, band, along):
    """Look at a still scene many times: how much do the readings wobble (metres)?"""
    xs = [r[0] for r in (read_frame(eyes, f, band, along) for f in frames) if r]
    if len(xs) < 3:
        return None
    return statistics.pstdev(xs)


def robust_mean(values):
    """Mean after dropping readings far from the rest; (mean, standard error)."""
    v = np.array(values, dtype=float)
    for _ in range(3):
        med = np.median(v)
        mad = 1.4826 * np.median(np.abs(v - med)) or 1e-9
        keep = np.abs(v - med) <= 4 * mad
        if keep.all():
            break
        v = v[keep]
    return float(v.mean()), float(v.std(ddof=1) / np.sqrt(len(v))) if len(v) > 1 else None


def robust_line(values):
    """Readings that drift steadily (a moving thing): the value in the middle of the
    handful, and its standard error, from a straight-line fit that drops bad readings."""
    x = np.arange(len(values), dtype=float)
    v = np.array(values, dtype=float)
    for _ in range(3):
        k, c = np.polyfit(x, v, 1)
        r = v - (k * x + c)
        mad = 1.4826 * np.median(np.abs(r - np.median(r))) or 1e-9
        keep = np.abs(r) <= 4 * mad
        if keep.all() or keep.sum() < 4:
            break
        x, v = x[keep], v[keep]
    k, c = np.polyfit(x, v, 1)
    r = v - (k * x + c)
    centre = (len(values) - 1) / 2
    sigma = float(np.sqrt((r @ r) / max(1, len(v) - 2)))
    return float(k * centre + c), float(sigma / np.sqrt(len(v)))


def fit_start_from_rest(ts, xs):
    """x = x0 + a·t²/2 (let go from rest), fitted robustly. Returns (a, standard error)."""
    t, x = np.array(ts, dtype=float), np.array(xs, dtype=float)
    for _ in range(4):
        A = np.stack([np.ones_like(t), t * t / 2], axis=1)
        coef, *_ = np.linalg.lstsq(A, x, rcond=None)
        r = x - A @ coef
        sigma = 1.4826 * np.median(np.abs(r - np.median(r))) or 1e-9
        keep = np.abs(r) <= 4 * sigma
        if keep.all() or keep.sum() < 5:
            break
        t, x = t[keep], x[keep]
    A = np.stack([np.ones_like(t), t * t / 2], axis=1)
    coef, *_ = np.linalg.lstsq(A, x, rcond=None)
    r = x - A @ coef
    dof = max(1, len(x) - 2)
    s2 = float(r @ r) / dof
    cov = s2 * np.linalg.inv(A.T @ A)
    return float(coef[1]), float(np.sqrt(cov[1, 1]))


BOTTOM = ((1, 39.0), 0)     # table: ruler along the bottom; positions along x
SIDE = ((0, 40.0), 1)       # stand: ruler up the side; positions along y


def acceleration(eyes, frames, fps):
    """Watch a video of something let go from rest: its acceleration (m/s²) and error."""
    ts, xs = [], []
    for i, f in enumerate(frames):
        r = read_frame(eyes, f, *BOTTOM)
        if r is not None:
            ts.append(i / fps)
            xs.append(r[0])
    if len(xs) < 6:
        return None, None
    return fit_start_from_rest(ts, xs)


def position(eyes, frames, where=SIDE):
    """Where the thing hangs, from many pictures of it standing still (metres)."""
    ys = [r[0] for r in (read_frame(eyes, f, *where) for f in frames) if r]
    if len(ys) < 3:
        return None, None
    return robust_mean(ys)


def path(eyes, frames, fps, where=SIDE):
    """A moving thing's heights and speeds, frame by frame (speed from a smooth local
    fit over 5 frames). Returns [(height, speed)], heights up from the lowest mark."""
    pts = []
    for i, f in enumerate(frames):
        spots = eyes.see(f)
        marks, things = _split(spots, (0, f.shape[1] - 8.0))
        if len(marks) < 5 or len(things) != 1:
            pts.append(None)
            continue
        coords = sorted(m[1] for m in marks)
        spacing = statistics.median([b - a for a, b in zip(coords, coords[1:])])
        bottom = coords[-1]
        pts.append(((things[0][0] - marks[0][0]) / spacing, (bottom - things[0][1]) / spacing))
    out = []
    for i in range(2, len(pts) - 2):
        window = [(j, pts[j]) for j in range(i - 2, i + 3) if pts[j] is not None]
        if len(window) < 4 or pts[i] is None:
            continue
        t = np.array([j / fps for j, _ in window])
        vx = np.polyfit(t, [p[0] for _, p in window], 2)
        vy = np.polyfit(t, [p[1] for _, p in window], 2)
        ti = i / fps
        speed = float(np.hypot(2 * vx[0] * ti + vx[1], 2 * vy[0] * ti + vy[1]))
        out.append((pts[i][1], speed))
    return out


def path_samples(eyes, frames, fps, per=6, where=SIDE):
    """A few careful readings instead of many rough ones: the frame-by-frame heights and
    speeds, combined in consecutive handfuls (robustly, so a bad frame can't spoil one).
    Returns [(height, speed, its uncertainty, speed's uncertainty)]."""
    pts = path(eyes, frames, fps, where)
    out = []
    for s in range(0, len(pts) - per + 1, per):
        chunk = pts[s:s + per]
        y, sy = robust_line([p[0] for p in chunk])
        v, sv = robust_line([p[1] for p in chunk])
        out.append((y, v, sy, sv))
    return out
