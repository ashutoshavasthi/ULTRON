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


def _moved_back(p, dx, dy):
    """A picture moved back by (dx, dy) pixels: each point read from where it went."""
    h, w = p.shape
    yy, xx = np.mgrid[0:h, 0:w].astype(float)
    x, y = np.clip(xx + dx, 0, w - 1), np.clip(yy + dy, 0, h - 1)
    x0, y0 = np.floor(x).astype(int), np.floor(y).astype(int)
    x1, y1 = np.minimum(x0 + 1, w - 1), np.minimum(y0 + 1, h - 1)
    fx, fy = x - x0, y - y0
    return ((1 - fy) * ((1 - fx) * p[y0, x0] + fx * p[y0, x1])
            + fy * ((1 - fx) * p[y1, x0] + fx * p[y1, x1]))


def _drift(p, usual, rounds=3):
    """How far the whole picture moved against the usual one, to a fraction of a pixel:
    the move that best explains its change from the edges of everything in it, leaving
    out what changed for another reason (a thing that moved by itself)."""
    gy, gx = np.gradient(usual)
    keep = np.ones(p.shape, bool)
    dx = dy = 0.0
    for _ in range(rounds):
        q = _moved_back(p, dx, dy) if (dx or dy) else p
        a = np.stack([gx[keep], gy[keep]], 1)
        ex, ey = np.linalg.lstsq(a, (usual - q)[keep], rcond=None)[0]
        dx, dy = dx + ex, dy + ey
        r = np.abs(_moved_back(p, dx, dy) - usual)
        keep = r <= 3 * np.median(r) + 2
    return float(dx), float(dy)


def steady(pictures):
    """The pictures held still, as eyes hold the world still when the head moves. If the
    camera shook (moving its pictures back explains most of how they differ from the
    usual one, over the film), each picture that moved a quarter of a pixel or more is
    moved back; a camera on a stand leaves the film as it is."""
    a = np.asarray(pictures, dtype=float)
    usual = np.median(a, axis=0)
    moves = [_drift(p, usual) for p in a]
    moved = [(k, d) for k, d in enumerate(moves) if np.hypot(*d) >= 0.25]
    if not moved:
        return a
    left = [np.mean(np.abs(_moved_back(a[k], *d) - usual)) / max(np.mean(np.abs(a[k] - usual)),
                                                               1e-9) for k, d in moved]
    if np.median(left) > 0.75:
        return a
    out = a.copy()
    for k, d in moved:
        out[k] = _moved_back(a[k], *d)
    return out


def changes(pictures):
    """How each picture differs from how the scene usually looks (each point averaged
    with its neighbours), and how strong the film's strongest changes are. A picture in
    which most of the scene changed (a blank picture, a cut) is not a picture of the
    scene, and shows no change. A shaking camera's pictures are held still first."""
    a = steady(pictures)
    usual = np.median(a, axis=0)
    diffs = np.array([_box(p - usual, 3) if np.median(np.abs(p - usual)) <= 10.0
                      else np.zeros_like(usual) for p in a])
    strong = float(np.percentile(np.abs(diffs), 99.99)) or 1.0
    return diffs, strong


def _around(diff, strong):
    """How strong the changes are around each point: the strongest change within about a
    sixteenth of the picture, but never below an eighth of the film's strongest (so
    quiet places don't turn noise into things)."""
    h, w = diff.shape
    b = max(8, int(max(h, w) / 16))
    nh, nw = -(-h // b), -(-w // b)
    pad = np.zeros((nh * b, nw * b))
    pad[:h, :w] = np.abs(diff)
    blocks = np.pad(pad.reshape(nh, b, nw, b).max(axis=(1, 3)), 1)
    near = np.max([blocks[i:i + nh, j:j + nw] for i in range(3) for j in range(3)], axis=0)
    return np.maximum(np.kron(near, np.ones((b, b)))[:h, :w], strong / 8)


def view(eyes, diff, strong, sign):
    """A change picture in the units its eyes grew up with: the background where it is
    used to it, and each change as clear as the strongest changes around it (as a retina
    adapts to the light where it looks: a ball beside a person moving is still seen)."""
    return np.clip(0.1 + eyes.contrast_ref * sign * diff / _around(diff, strong), 0.0, 1.0)


def look_closer(diff, x, y, sign, reach):
    """Where exactly a thing is: looking closely at full sharpness, the middle of the
    patch of change that holds the strongest point near (x, y), as far as it stays at
    least half as strong (a gap of up to two pixels, such as a stripe across it, doesn't
    split it; a neighbour further off is a separate thing and is left out)."""
    h, w = diff.shape
    cx, cy = int(round(x)), int(round(y))
    x0, x1 = max(0, cx - reach), min(w, cx + reach + 1)
    y0, y1 = max(0, cy - reach), min(h, cy + reach + 1)
    patch = sign * diff[y0:y1, x0:x1]
    if patch.size == 0 or patch.max() <= 0:
        return x, y
    core = reach // 2
    inner = patch[max(0, cy - core - y0):cy + core + 1 - y0,
                  max(0, cx - core - x0):cx + core + 1 - x0]
    if inner.size == 0 or inner.max() <= 0:
        return x, y
    iy, ix = np.unravel_index(int(np.argmax(inner)), inner.shape)
    sy, sx = iy + max(0, cy - core - y0), ix + max(0, cx - core - x0)
    level = 0.5 * patch[sy, sx]
    part = np.zeros(patch.shape, bool)
    todo = [(sy, sx)]
    part[sy, sx] = True
    while todo:
        a, b = todo.pop()
        for na, nb in ((a + i, b + j) for i in range(-3, 4) for j in range(-3, 4)):
            if 0 <= na < patch.shape[0] and 0 <= nb < patch.shape[1] and not part[na, nb] \
                    and patch[na, nb] >= level:
                part[na, nb] = True
                todo.append((na, nb))
    weight = np.where(part, patch, 0.0)
    yy, xx = np.mgrid[y0:y1, x0:x1]
    total = weight.sum()
    return float((weight * xx).sum() / total), float((weight * yy).sum() / total)


def see_changes(eyes, pictures, sign, scales=(1, 2, 3, 4, 6)):
    """[(x, y, strength)] per picture: what is brighter (sign +1) or darker (-1) than
    usual. Each picture is looked at as it is and from further back, and each thing is
    kept at the view where it looks most like the things its eyes learned (things here
    are often larger than those); then it looks closer to see exactly where it is."""
    from .eyes import _shrink
    diffs, strong = changes(pictures)
    out = []
    for d in diffs:
        v = view(eyes, d, strong, sign)
        found = []
        for s in scales:
            small = _shrink(v, s) if s > 1 else v
            for x, y, st in eyes.see(eyes._adapt(small)):
                found.append((st, x * s + (s - 1) / 2, y * s + (s - 1) / 2, s))
        found.sort(key=lambda f: -f[0])
        kept = []
        for st, x, y, s in found:
            if all(np.hypot(x - kx, y - ky) > 2 * max(s, ks) + 2 for _, kx, ky, ks in kept):
                kept.append((st, x, y, s))
        seen = []
        for st, x, y, s in kept:             # strongest first; two looks that close in on
            cx, cy = look_closer(d, x, y, sign, 24)   # the same patch: one thing
            if all(np.hypot(cx - px, cy - py) > 3.0 for px, py, _ in seen):
                seen.append((cx, cy, st))
        out.append(seen)
    return out


# ---------------------------------------------------------------- following
def follow(per_frame, reach=60.0, slack=6.0, memory=2):
    """Tracks [{frame: (x, y)}] of things that keep moving as they were moving: each
    thing is looked for where it was heading (its last step repeated, speeding up or
    slowing down as it just did), within `slack`
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
                ax = ay = 0.0
                if gap == 1 and len(frames) >= 3 and last - prev == 1 and prev - frames[-3] == 1:
                    ax = vx - (tracks[t][prev][0] - tracks[t][frames[-3]][0])
                    ay = vy - (tracks[t][prev][1] - tracks[t][frames[-3]][1])
                px, py = x + vx * gap + ax, y + vy * gap + ay
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


def moving_smoothly(track, slack=6.0):
    """In how many pictures a track moves the way a thing moves: going somewhere (a pixel
    a picture or more), and going on much as it was going (its change of step within
    `slack` pixels plus a quarter of its step). Flickering speckle joined up by chance
    jumps about; a thing at rest goes nowhere."""
    n = 0
    for f in track:
        if f - 1 in track and f + 1 in track:
            step = np.subtract(track[f + 1], track[f - 1]) / 2
            turn = np.add(track[f + 1], track[f - 1]) - 2 * np.asarray(track[f])
            if np.hypot(*step) >= 1 and np.hypot(*turn) <= slack + 0.25 * np.hypot(*step):
                n += 1
    return n


def _mover_key(track):
    return (roughness(track) <= 1.0, moving_smoothly(track), travel(track))


def whole_mover(tracks, lasting=8):
    """The thing that moved, once each lasting track is joined with what it is seen
    again as after a brief loss (a thing glimpsed in pieces is still one thing): of
    those that move smoothly overall (third differences within a pixel), the one seen
    moving as a thing moves in the most pictures."""
    joined = [chain(t, tracks) for t in tracks if len(t) >= lasting]
    return max(joined, key=_mover_key) if joined else None


def _heading(track, ends):
    """Where a track is heading past one of its ends ("last" or "first"): (frame, x, y,
    step per picture)."""
    frames = sorted(track)
    if ends == "first":
        frames = frames[::-1]
    a, b = frames[-1], (frames[-2] if len(frames) > 1 else frames[-1])
    (x, y), (px, py) = track[a], track[b]
    d = abs(a - b) or 1
    return a, x, y, ((x - px) / d, (y - py) / d)


def coincide(a, b, near=12.0, shared=2):
    """Two tracks that are at the same place at the same time, over the pictures they
    share, are the same thing seen twice."""
    both = [f for f in a if f in b]
    if len(both) < shared:
        return False
    d = [np.hypot(a[f][0] - b[f][0], a[f][1] - b[f][1]) for f in both]
    return float(np.median(d)) < near


def chain(track, tracks, gap=4, slack=8.0):
    """Object permanence across a brief loss: a track that begins just after this one
    ends, where this one was heading, is the same thing seen again (and likewise before
    it began); so is one that starts again right where it was, as after a bounce. A track
    that coincides with it where both were seen is also the same
    thing. Returns the joined track."""
    whole = dict(track)
    used = {id(track)}
    grew = True
    while grew:
        grew = False
        for t in tracks:
            if id(t) not in used and len(t) >= 3 and coincide(whole, t, near=6.0):
                used.add(id(t))
                for k, v in t.items():
                    whole.setdefault(k, v)
                grew = True
    for ends in ("last", "first"):
        while True:
            f, x, y, (vx, vy) = _heading(whole, ends)
            speed = float(np.hypot(vx, vy))
            ahead, turned = [], []
            for t in tracks:
                if id(t) in used or len(t) < 3:
                    continue
                g = (min(t) - f) if ends == "last" else (f - max(t))
                if not 0 <= g <= gap:
                    continue
                sx, sy = t[min(t) if ends == "last" else max(t)]
                d = float(np.hypot(sx - (x + vx * g), sy - (y + vy * g)))
                fs = sorted(t) if ends == "last" else sorted(t)[::-1]
                ux, uy = np.subtract(t[fs[1]], t[fs[0]]) / (fs[1] - fs[0])
                # where it was heading, and moving on as it was moving
                if g >= 1 and d <= slack + 0.5 * speed * g and \
                        float(np.hypot(ux - vx, uy - vy)) <= slack + 0.5 * speed * g:
                    ahead.append((d, t))
                # or, going fast, it hit something and came back (a bounce): it starts
                # again moving back, no further from where it was than its speed could
                # take it. Of those, the one that lasts longest (a reflection or a
                # shadow flickers)
                turn = float(np.hypot(sx - x, sy - y))
                back = (ux * vx + uy * vy) < 0
                if speed > slack and back and turn <= slack + speed * max(g, 1):
                    turned.append((-len(t), turn, t))
            best = None
            if ahead:
                best = min(ahead, key=lambda c: c[0])
            elif turned:
                best = min(turned, key=lambda c: c[:2])[1:]
            if best is None:
                break
            used.add(id(best[1]))
            for k, v in best[1].items():
                whole.setdefault(k, v)
    return whole


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
        return coincide(track, o, shared=1)
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
    per frame). The channel is the one in which the moving thing (`whole_mover`) is seen
    moving as a thing moves for longest; of the two orders of half-pictures, the one in
    which it moves more smoothly."""
    seqs = half_pictures(pictures) if interlaced else (list(pictures),)
    best = None
    for sign in (1, -1):
        for seq in seqs:
            reach = max(60.0, max(np.shape(seq[0])) / 10)    # a tenth of the picture
            tracks = follow(see_changes(eyes, seq, sign), reach=reach)
            t = whole_mover(tracks)
            if t is None:
                continue
            key = _mover_key(t)
            same_channel = best is not None and best[2] == sign
            if best is None or (same_channel and -roughness(t) > -roughness(best[1])) or \
                    (not same_channel and key > best[0]):
                best = (key, t, sign, tracks)
    per = 2 if interlaced else 1
    if best is None:
        return None, per, None, []
    return best[1], per, ("ON" if best[2] > 0 else "OFF"), best[3]


# ---------------------------------------------------------------- measuring
def swing(track, rate):
    """How a swinging thing swings, from its track (`rate` pictures per second).

    The middle of the swing is halfway between its furthest points left and right; each
    time it crosses the middle (timed between pictures) starts a half swing. The period
    is twice the mean half swing over whole swings there and back. Its error is the
    scatter of those timings (with a single half swing, the pictures' resolution: each
    end timed to one picture). Its path is a circle about the pivot, so the angle of the swing needs no
    scale: the furthest it goes from the middle, against the circle's radius.
    Returns None if it doesn't cross the middle at least twice."""
    frames = sorted(track)
    xs = np.array([track[f][0] for f in frames])
    ys = np.array([track[f][1] for f in frames])
    mid = (xs.max() + xs.min()) / 2
    cross = []
    for a, b in zip(frames, frames[1:]):
        u, v = track[a][0] - mid, track[b][0] - mid
        if u == 0 or u * v < 0:
            cross.append(a + (b - a) * u / (u - v))
    if len(cross) < 2:
        return None
    k = len(cross) - 1
    if k >= 2:
        k -= k % 2                                # whole swings only
    halves = np.diff(cross[:k + 1]) / rate
    if k > 1:
        error = 2 * halves.std(ddof=1) / np.sqrt(k)
    else:                                         # one half swing: one picture each end
        error = 2 * np.sqrt(2) / rate
    m = np.stack([xs, ys, np.ones_like(xs)], 1)
    c = np.linalg.lstsq(m, xs ** 2 + ys ** 2, rcond=None)[0]
    radius = float(np.sqrt(c[2] + (c[0] / 2) ** 2 + (c[1] / 2) ** 2))
    reach = []
    for a, b in zip(cross[:k], cross[1:k + 1]):
        reach.append(max(abs(track[f][0] - mid) for f in frames if a < f < b))
    angle = float(np.arcsin(min(1.0, np.sqrt(np.mean(np.square(reach))) / radius)))
    return {"period": float(2 * halves.mean()), "error": float(error),
            "half_swings": [float(h) for h in halves], "crossings": [float(c) for c in cross],
            "angle": angle, "radius_px": radius}



def bounces(track, least=5):
    """How much of its speed a bouncing thing keeps at each bounce, from its track.

    A bounce is where it is lowest between two flights (picture rows grow downward).
    Each flight's height is fitted with a parabola in time, leaving out the picture
    nearest each bounce (it is touching the floor) and any pictures before it started to
    move (still held). The bounce happens where the two flights' parabolas meet; what it
    keeps is the upward speed after over the downward speed before. A bounce counts only
    if both its flights keep at least `least` pictures. Returns [(frame, kept)]."""
    frames = sorted(track)
    y = {f: track[f][1] for f in frames}
    lows = [b for a, b, c in zip(frames, frames[1:], frames[2:])
            if y[b] >= y[a] and y[b] > y[c] and y[b] - min(y[f] for f in frames
                                                        if abs(f - b) <= 6) > 10]
    edges = [frames[0] - 1] + lows + [frames[-1] + 1]
    fits = []
    for a, b in zip(edges, edges[1:]):
        part = [f for f in frames if a < f < b]
        moving = [f for i, f in enumerate(part)
                  if all(abs(y[g] - y[h]) > 1 for g, h in zip(part[i:], part[i + 1:]))]
        part = moving[:1] and [f for f in part if f >= moving[0]]
        fits.append(np.polyfit(part, [y[f] for f in part], 2) if len(part) >= least else None)
    out = []
    for low, p, q in zip(lows, fits, fits[1:]):
        if p is None or q is None:
            continue
        roots = np.roots(np.subtract(p, q))
        roots = [r.real for r in roots if abs(r.imag) < 1e-9]
        if not roots:
            continue
        t = min(roots, key=lambda r: abs(r - low))
        before, after = np.polyval(np.polyder(p), t), np.polyval(np.polyder(q), t)
        if before > 0 > after:
            out.append((low, float(-after / before)))
    return out


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
