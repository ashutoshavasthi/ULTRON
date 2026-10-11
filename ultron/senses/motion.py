"""Seeing what moves in a real film, and following it.

Real lab films are not like the camera simulator's pictures: a ball the size of ten
pixels, a still room around it, an arm that throws it, and video compression that
leaves faint blocky speckle everywhere. Two things animals do let its eyes cope:

  * **What changes stands out.** The eyes compare each picture with how the scene
    usually looks (the middle of all its pictures, the way a still room fades from
    attention) and look only at what is different: brighter than usual (ON) or darker
    than usual (OFF). The strongest changes in the film are put at the contrast its eyes
    are used to, so faint compression speckle stays faint.
  * **Things keep moving as they were moving.** A thing seen now is where it was heading
    a moment ago (infants expect this too). A thing that moves steadily across many
    pictures is a real moving thing; speckle comes and goes.

Interlaced video (a camera taking two half-pictures per frame, 1/60 s apart) is looked
at half-picture by half-picture; which half came first is decided the way an animal
would, by which order makes the thing move smoothly.
"""

import numpy as np

from .retina import _box


# ---------------------------------------------------------------- pictures
def half_pictures(pictures):
    """Each frame's two half-pictures (rows 0, 2, 4... and rows 1, 3, 5...), each made
    full size again by repeating its rows, in both possible orders. Returns
    (top-first sequence, bottom-first sequence)."""
    tops, bottoms = [], []
    for p in pictures:
        a = np.asarray(p, dtype=float)
        top = np.repeat(a[0::2], 2, axis=0)[:a.shape[0]]
        bottom = np.vstack([a[1:2], np.repeat(a[1::2], 2, axis=0)])[:a.shape[0]]
        tops.append(top)
        bottoms.append(bottom)
    tf = [x for pair in zip(tops, bottoms) for x in pair]
    bf = [x for pair in zip(bottoms, tops) for x in pair]
    return tf, bf


def changes(pictures):
    """How each picture differs from how the scene usually looks (each point averaged
    with its neighbours), and how strong the film's strongest changes are."""
    a = np.asarray(pictures, dtype=float)
    usual = np.median(a, axis=0)
    diffs = np.array([_box(p - usual, 3) for p in a])
    strong = float(np.percentile(np.abs(diffs), 99.99)) or 1.0
    return diffs, strong


def view(eyes, diff, strong, sign):
    """A change picture in the units its eyes grew up with: the background where it is
    used to it, the film's strongest changes as clear as the things it learned."""
    return np.clip(0.1 + eyes.contrast_ref * sign * diff / strong, 0.0, 1.0)


def see_changes(eyes, pictures, sign):
    """[(x, y, strength)] per picture: what is brighter (sign +1) or darker (-1) than
    usual. Each picture is also looked at from further back (things here are larger
    than the ones its eyes learned)."""
    diffs, strong = changes(pictures)
    return [eyes.see_views(view(eyes, d, strong, sign)) for d in diffs]


# ---------------------------------------------------------------- following
def follow(per_frame, reach=60.0, slack=6.0, memory=2):
    """Tracks [{frame: (x, y)}] of things that keep moving as they were moving: each
    thing is looked for where it was heading (its last step repeated), within `slack`
    pixels plus a quarter of its step; a thing seen once may be anywhere within
    `reach`. A thing missed for up to `memory` pictures may come back."""
    tracks, active = [], []                       # active: track indices
    for f, pts in enumerate(per_frame):
        pts = [tuple(p[:2]) for p in pts]
        pairs = []
        for k, t in enumerate(active):
            frames = sorted(tracks[t])
            last = frames[-1]
            gap = f - last
            if gap > memory + 1:
                continue
            x, y = tracks[t][last]
            if len(frames) >= 2:
                prev = frames[-2]
                vx = (x - tracks[t][prev][0]) / (last - prev)
                vy = (y - tracks[t][prev][1]) / (last - prev)
                px, py = x + vx * gap, y + vy * gap
                radius = slack + 0.25 * np.hypot(vx, vy) * gap
            else:
                px, py, radius = x, y, reach
            for j, (qx, qy) in enumerate(pts):
                d = float(np.hypot(qx - px, qy - py))
                if d <= radius:
                    pairs.append((d, k, j))
        pairs.sort()
        used_t, used_p = set(), set()
        for d, k, j in pairs:
            if k in used_t or j in used_p:
                continue
            used_t.add(k)
            used_p.add(j)
            tracks[active[k]][f] = pts[j]
        keep = [t for k, t in enumerate(active)
                if k in used_t or f - max(tracks[t]) <= memory]
        for j, p in enumerate(pts):
            if j not in used_p:
                tracks.append({f: p})
                keep.append(len(tracks) - 1)
        active = keep
    return tracks


def travel(track):
    pts = np.array([track[f] for f in sorted(track)])
    return float(np.hypot(*(pts.max(axis=0) - pts.min(axis=0))))


def mover(tracks, lasting=8):
    """The thing that moved: of the tracks that last, the one that went furthest."""
    lasting_tracks = [t for t in tracks if len(t) >= lasting]
    return max(lasting_tracks, key=travel) if lasting_tracks else None


def roughness(track):
    """How unsmoothly a track moves: the typical size of its third differences
    (a thing moving under steady forces has none)."""
    frames = sorted(track)
    run = [f for f in frames if f + 1 in track and f + 2 in track and f + 3 in track]
    if not run:
        return float("inf")
    j = [np.subtract(np.subtract(track[f + 3], track[f]),
                     3 * np.subtract(track[f + 2], track[f + 1])) for f in run]
    return float(np.median(np.abs(np.array(j))))


def alone(track, tracks, shape, gap=40.0, moved=10.0, margin=8.0):
    """The pictures in which the thing is on its own and wholly in view: no other moving
    thing (a hand, an arm) within `gap` pixels, so nothing touches it, and not at the
    picture's edge, where part of it may be cut off. Returns the longest run of such
    pictures (a picture or two unseen may be skipped)."""
    def same_thing(o):              # moves along with it, a few pixels away: part of it
        shared = [f for f in o if f in track]
        d = [np.hypot(track[f][0] - o[f][0], track[f][1] - o[f][1]) for f in shared]
        return bool(d) and float(np.median(d)) < 12.0
    others = [t for t in tracks if t is not track and len(t) >= 3 and travel(t) > moved
              and not same_thing(t)]
    free = []
    for f in sorted(track):
        x, y = track[f]
        if not (margin <= x <= shape[1] - 1 - margin and margin <= y <= shape[0] - 1 - margin):
            continue
        near = [o[f] for o in others if f in o]
        if all(np.hypot(x - ox, y - oy) >= gap for ox, oy in near):
            free.append(f)
    runs, run = [], []
    for f in free:
        if run and f - run[-1] > 3:
            runs.append(run)
            run = []
        run.append(f)
    if run:
        runs.append(run)
    best = max(runs, key=len) if runs else []
    return {f: track[f] for f in best}


def watch(eyes, pictures, interlaced=False):
    """Follow the moving thing in a film. Returns (track, pictures per frame, channel,
    all tracks): the track's frames count half-pictures when the film is interlaced (2
    per frame). The channel is the one where something travels furthest; of the two
    orders of half-pictures, the one in which it moves more smoothly."""
    seqs = half_pictures(pictures) if interlaced else (list(pictures),)
    best = None
    for sign in (1, -1):
        for seq in seqs:
            tracks = follow(see_changes(eyes, seq, sign))
            t = mover(tracks)
            if t is None:
                continue
            key = (travel(t), -roughness(t))
            same_channel = best is not None and best[2] == sign
            if best is None or (same_channel and key[1] > best[0][1]) or \
                    (not same_channel and key[0] > best[0][0]):
                best = (key, t, sign, tracks)
    per = 2 if interlaced else 1
    if best is None:
        return None, per, None, []
    return best[1], per, ("ON" if best[2] > 0 else "OFF"), best[3]


# ---------------------------------------------------------------- measuring
def speeds(track, rate, scale):
    """Downward speed (metres per second) between each two neighbouring pictures of a
    track: [(picture, speed)], `rate` pictures per second, `scale` pixels per metre."""
    return [(f, (track[f + 1][1] - track[f][1]) * rate / scale)
            for f in sorted(track) if f + 1 in track]


def speed_change(track, lag, rate, scale, start=None):
    """How much faster it goes after `lag` pictures: the mean change of its downward
    speed over every starting picture (or only those `start` picks). Returns (change in
    m/s, number of pairs)."""
    v = dict(speeds(track, rate, scale))
    pairs = [v[f + lag] - v[f] for f in sorted(v)
             if f + lag in v and (start is None or start(f))]
    if not pairs:
        return None, 0
    return float(np.mean(pairs)), len(pairs)


def steady_change(track, rate, scale):
    """Once it knows its speed changes steadily: how fast (m/s per second), from the
    straight line through all its speeds, and that line's standard error."""
    v = speeds(track, rate, scale)
    t = np.array([f / rate for f, _ in v])
    s = np.array([x for _, x in v])
    A = np.stack([np.ones_like(t), t], axis=1)
    coef, *_ = np.linalg.lstsq(A, s, rcond=None)
    r = s - A @ coef
    s2 = float(r @ r) / max(1, len(s) - 2)
    return float(coef[1]), float(np.sqrt(s2 * np.linalg.inv(A.T @ A)[1, 1]))
