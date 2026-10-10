"""Following things from picture to picture: object permanence, used on video.

A thing seen now is the same thing seen a moment ago nearby (the nearest one, if it
is close enough). A thing that vanishes for a picture or two may come back. Things
seen only briefly are not trusted: real things last.
"""

import numpy as np


def link(per_frame, max_step=5.0, memory=3):
    """per_frame: [[(x, y), ...] for each picture]. Returns tracks: [{frame: (x, y)}]."""
    tracks, active = [], []          # active: (track index, last frame, last x, last y)
    for f, pts in enumerate(per_frame):
        pts = [tuple(p[:2]) for p in pts]
        live = [a for a in active if f - a[1] <= memory + 1]
        pairs = []
        if live and pts:
            A = np.array([(a[2], a[3]) for a in live])
            P = np.array(pts)
            d = np.sqrt(((A[:, None, :] - P[None, :, :]) ** 2).sum(-1))
            for i, j in zip(*np.nonzero(d <= max_step)):
                pairs.append((d[i, j], i, j))
        pairs.sort()
        used_a, used_p, nxt = set(), set(), []
        for dist, i, j in pairs:
            if i in used_a or j in used_p:
                continue
            used_a.add(i)
            used_p.add(j)
            t = live[i][0]
            tracks[t][f] = pts[j]
            nxt.append((t, f, pts[j][0], pts[j][1]))
        for i, a in enumerate(live):
            if i not in used_a:
                nxt.append(a)
        for j, p in enumerate(pts):
            if j not in used_p:
                tracks.append({f: p})
                nxt.append((len(tracks) - 1, f, p[0], p[1]))
        active = nxt
    return tracks


def lasting(tracks, frames=25):
    return [t for t in tracks if len(t) >= frames]


def drift(tracks, n_frames):
    """How the whole picture slides (the water, the stage): the average step of all the
    things seen in both of two neighbouring pictures, added up."""
    steps = np.zeros((n_frames, 2))
    for f in range(1, n_frames):
        moves = [(t[f][0] - t[f - 1][0], t[f][1] - t[f - 1][1]) for t in tracks
                 if f in t and f - 1 in t]
        if moves:
            steps[f] = np.mean(moves, axis=0)
    return np.cumsum(steps, axis=0)


def spread(tracks, lag, shift=None, scale=1.0):
    """How far things typically get in `lag` pictures: the root of the mean squared
    distance, over every thing and every starting picture (drift removed)."""
    sq = []
    for t in tracks:
        for f, (x, y) in t.items():
            g = f + lag
            if g in t:
                dx, dy = t[g][0] - x, t[g][1] - y
                if shift is not None:
                    dx -= shift[g][0] - shift[f][0]
                    dy -= shift[g][1] - shift[f][1]
                sq.append(dx * dx + dy * dy)
    if not sq:
        return None, 0
    return float(np.sqrt(np.mean(sq))) * scale, len(sq)
