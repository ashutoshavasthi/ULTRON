"""What happens in a film, in Ultron's own kinds of law (stage 3, L2).

Ultron follows each thing through a film (senses/things.py: watch_film) and gets, for
each picture, where the thing was across and up-down. It describes each of those two
sequences as the shortest run of pieces, each piece a kind of law it already has:

  nothing changes             the innate "stays the same"
  equal steps                 the innate Δ: each reading goes up by the same step
  and every kind it found itself (brain.kinds) that a sequence of positions can have:
  steps that change by the same amount (ΔΔ), steps that shrink by the same fraction
  (Δρ, "it settles toward a resting value"), readings that are each the same number of
  times the one before (ρ).

Shortest is in bits (MDL): what is left unexplained, at the camera's own noise, plus
half log2(n) bits for each number a piece needs, plus which kind it is and where it
starts. A piece costs more than it saves unless the motion really changed.

From the pieces it reads what the thing did: which kind of law its longest move
across followed, and its longest move up-down; how many times it turned back; when it
started and stopped moving; how fast it went. When two things meet and both change
how they move, its momentum law (Σ m·v the same before and after, lesson 5) says how
heavy one is compared with the other.
"""

import math

import numpy as np

STILL = {"y_ops": [], "x_op": None}
STEADY = {"y_ops": ["Δ"], "x_op": None}
GRID = [round(0.30 + 0.02 * i, 2) for i in range(35)] + \
       [round(1.02 + 0.02 * i, 2) for i in range(15)]     # fractions tried for ρ
MIN_NOISE = 0.03    # pixels: it never trusts its eyes beyond this
SEEN_TO_MOVE = 1.0  # pixels: a thing that goes less far than this in a piece of film is
                    # not seen to move (its eyes resolve a pixel, not a hundredth of one)


# ---------------------------------------------------------------- kinds it can use
def motion_kinds(brain):
    """[(name, template, words)] for every kind of law a sequence of positions can
    follow, simplest first: the innate ones, then those it found (in the order found)."""
    from .kinds import words
    out = [("nothing changes", STILL, "it stays where it is"),
           ("equal steps", STEADY, words(STEADY))]
    seen = [STILL, STEADY]
    for name, k in sorted(brain.kinds.items(), key=lambda kv: kv[1].get("order", 0)):
        t = {"y_ops": list(k["template"].get("y_ops", [])), "x_op": k["template"].get("x_op")}
        if k["template"].get("rec") or k["template"].get("pow") is not None:
            continue
        if _basis(t) is None or t in seen:
            continue
        seen.append(t)
        out.append((name, t, k.get("words") or words(t)))
    return out


def _basis(template):
    """The sequences a template allows, as readings it explains with numbers to fit:
    'Δ' applied k times staying the same is a polynomial of degree k (k+1 numbers); 'Δ'
    k times then 'ρ' is a polynomial of degree k-1 plus c·r^t. (A law about steps in what
    is changed, or a mix of the last readings, is not used here.) Returns (how many
    polynomial terms, uses a ratio) or None."""
    if template.get("x_op"):
        return None
    ops = template["y_ops"]
    if all(op == "Δ" for op in ops):
        return len(ops) + 1, False
    if ops[-1] == "ρ" and all(op == "Δ" for op in ops[:-1]):
        return len(ops) - 1, True
    return None


# ---------------------------------------------------------------- noise
def noise_of(track, axes=("x", "y")):
    """How much the camera's noise moves this thing's position about (pixels), from how
    much the third steps between consecutive pictures wobble: they are pure noise for
    any motion whose steps change evenly, and a sudden change (a bounce) shows up as a
    few outliers, which are set aside (beyond 4 times the typical size)."""
    d3 = []
    t = track["t"]
    for axis in axes:
        v = track[axis]
        for i in range(len(t) - 3):
            if t[i + 3] - t[i] == 3:
                d3.append(v[i + 3] - 3 * v[i + 2] + 3 * v[i + 1] - v[i])
    if len(d3) < 4:
        return MIN_NOISE
    d3 = np.asarray(d3)
    typical = 1.4826 * float(np.median(np.abs(d3)))
    kept = d3[np.abs(d3) <= 4 * typical] if typical > 0 else d3
    return max(float(np.sqrt(np.mean(kept ** 2) / 20.0)), MIN_NOISE)


# ---------------------------------------------------------------- pieces
def _columns(terms, ratios, t):
    """The basis at times t: [len(ratios) or 1, len(t), terms (+1)]."""
    poly = np.stack([t ** p for p in range(terms)], axis=1) if terms else np.zeros((len(t), 0))
    if ratios is None:
        return poly[None]
    r = np.asarray(ratios)[:, None] ** t[None, :]
    return np.concatenate([np.broadcast_to(poly, (len(ratios),) + poly.shape),
                           r[:, :, None]], axis=2)


def _fits(ts, vs, terms, ratios):
    """For every piece [i, j) of the readings and every ratio: the least-squares fit of
    this basis. Yields (i, j, rss[ratio], coefficients[ratio]) for pieces with at least
    two readings more than the numbers fitted."""
    n = len(ts)
    k = terms + (0 if ratios is None else 1)
    for i in range(n - k - 1):
        t = ts[i:] - ts[i]
        a = _columns(terms, ratios, t)                      # [R, L, k]
        y = vs[i:]
        ata = np.cumsum(a[:, :, :, None] * a[:, :, None, :], axis=1)[:, k + 1:]
        aty = np.cumsum(a * y[None, :, None], axis=1)[:, k + 1:]
        yy = np.cumsum(y * y)[k + 1:]
        ridge = 1e-10 * np.trace(ata, axis1=2, axis2=3)[:, :, None, None] * np.eye(k)
        c = np.linalg.solve(ata + ridge + 1e-300, aty[..., None])[..., 0]
        rss = np.maximum(yy[None, :] - np.einsum("rmk,rmk->rm", aty, c), 0.0)
        for m in range(rss.shape[1]):
            yield i, i + k + 2 + m, rss[:, m], c[:, m]


def _travel(c, terms, ratio, span):
    """How far the law's curve goes over a piece (its range, in pixels)."""
    t = np.linspace(0.0, span, 25)
    curve = _columns(terms, None if ratio is None else [ratio], t)[0] @ c
    return float(curve.max() - curve.min())


def pieces(ts, vs, sigma, kinds):
    """The shortest description of one sequence of positions as pieces, each following
    one kind. Returns [{"kind": index into kinds, "from": t, "to": t, "c": coefficients,
    "ratio": r or None}] covering every reading."""
    ts = np.asarray(ts, dtype=float)
    vs = np.asarray(vs, dtype=float)
    n = len(ts)
    head = math.log2(len(kinds)) + math.log2(max(n, 2))       # which kind, where it starts
    # a piece never spans pictures where it lost sight of the thing (it was touching
    # another): it can't say what happened meanwhile
    lost = np.concatenate([[0], np.cumsum(np.diff(ts) > 1)])
    best_piece = {}
    for ki, (_, template, _) in enumerate(kinds):
        terms, uses_ratio = _basis(template)
        ratios = GRID if uses_ratio else None
        params = terms + (2 if uses_ratio else 0)       # the ratio is a number to state too
        for i, j, rss, c in _fits(ts, vs, terms, ratios):
            if lost[j - 1] != lost[i]:
                continue
            r = int(np.argmin(rss))
            if ki != 0 and _travel(c[r], terms, GRID[r] if uses_ratio else None,
                                   ts[j - 1] - ts[i]) < SEEN_TO_MOVE:
                continue            # a move too small to see is no move
            bits = float(rss[r]) / (2 * sigma * sigma * math.log(2)) + \
                0.5 * params * math.log2(j - i) + head
            if (i, j) not in best_piece or bits < best_piece[(i, j)][0] - 1e-9:
                best_piece[(i, j)] = (bits, ki, GRID[r] if uses_ratio else None, c[r])
    # the shortest chain of pieces (dynamic programming over where pieces start)
    total = [math.inf] * (n + 1)
    back = [None] * (n + 1)
    total[0] = 0.0
    for j in range(1, n + 1):
        for i in range(j):
            p = best_piece.get((i, j))
            if p is not None and total[i] + p[0] < total[j] - 1e-9:
                total[j], back[j] = total[i] + p[0], i
    if back[n] is None:
        return [{"kind": 0, "from": float(ts[0]), "to": float(ts[-1]),
                 "c": [float(np.mean(vs))], "ratio": None}]
    out, j = [], n
    while j > 0:
        i = back[j]
        _, ki, r, c = best_piece[(i, j)]
        out.append({"kind": ki, "from": float(ts[i]), "to": float(ts[j - 1]),
                    "c": [float(x) for x in c], "ratio": r})
        j = i
    return out[::-1]


def _at(piece, kinds, t, deriv=False):
    """Where the piece's law puts the thing at time t (or how fast it moves)."""
    npoly, uses_ratio = _basis(kinds[piece["kind"]][1])
    s = t - piece["from"]
    c = piece["c"]
    if deriv:
        v = sum(p * c[p] * s ** (p - 1) for p in range(1, npoly))
        if uses_ratio:
            v += c[-1] * math.log(piece["ratio"]) * piece["ratio"] ** s
        return v
    v = sum(c[p] * s ** p for p in range(npoly))
    if uses_ratio:
        v += c[-1] * piece["ratio"] ** s
    return v


# ---------------------------------------------------------------- what a thing did
def _turns(path):
    """How many times a path, having gone one way, comes back by SEEN_TO_MOVE."""
    if not path:
        return 0
    turns, way, far = 0, 0, path[0]        # far: the furthest it got going this way
    for v in path[1:]:
        if way == 0:
            if abs(v - far) >= SEEN_TO_MOVE:
                way, far = (1 if v > far else -1), v
        elif (v - far) * way > 0:
            far = v
        elif (far - v) * way >= SEEN_TO_MOVE:
            turns, way, far = turns + 1, -way, v
    return turns


def motion(track, kinds):
    """What a thing did in a film, in its own terms."""
    ts = track["t"]
    # each way may be noisier than the other (a long thing's ends flicker); a guess from
    # one way's few pictures can come out low, so it never trusts it beyond both together
    both = noise_of(track)
    sigma = {a: max(noise_of(track, (a,)), both) for a in ("x", "y")}
    out = {"pieces": {}}
    moving = []
    speeds = {}
    for axis, name in (("x", "across"), ("y", "updown")):
        ps = pieces(ts, track[axis], sigma[axis], kinds)
        out["pieces"][axis] = ps
        longest = max((p for p in ps if p["kind"] != 0),
                      key=lambda p: (p["to"] - p["from"], -p["from"]), default=None)
        out[name] = 0 if longest is None else longest["kind"]
        for p in ps:
            if p["kind"] != 0:
                moving.append((p["from"], p["to"]))
        speeds[axis] = {t: _at(p, kinds, t, deriv=True)
                        for p in ps for t in ts if p["from"] <= t <= p["to"]}
    # how many times it turned back: went at least SEEN_TO_MOVE back the way it came,
    # along the path its laws give
    turns = 0
    for axis in ("x", "y"):
        path = [_at(p, kinds, t) for p in out["pieces"][axis] for t in ts
                if p["from"] <= t <= p["to"]]
        turns += _turns(path)
    out["turns"] = turns
    out["start"] = start = min((a for a, _ in moving), default=None)
    out["end"] = end = max((b for _, b in moving), default=None)

    def mean_speed(a, b):
        sp = [math.hypot(speeds["x"].get(t, 0.0), speeds["y"].get(t, 0.0)) for t in ts
              if a <= t <= b]
        return float(np.mean(sp)) if sp else 0.0

    out["speed"], out["speed unsure"] = 0.0, 0.0
    if start is not None:
        # how fast it went while it was seen moving: once what is left of its move is
        # under a pixel (a thing settling), it no longer sees it move
        at = {a: {t: _at(p, kinds, t) for p in out["pieces"][a] for t in ts
                  if p["from"] <= t <= p["to"]} for a in ("x", "y")}
        left = lambda t: math.hypot(at["x"].get(end, 0.0) - at["x"].get(t, 0.0),
                                    at["y"].get(end, 0.0) - at["y"].get(t, 0.0))
        seen = [t for t in ts if start <= t < end and left(t) >= SEEN_TO_MOVE]
        seen_end = min(max(seen) + 1, end) if seen else end
        out["speed"] = mean_speed(start, seen_end)
        # it can't say to the picture when moving began and ended: the average is only
        # as sure as it is about those
        tries = [mean_speed(a, b) for a in (start - 1, start, start + 1)
                 for b in (seen_end - 1, seen_end, seen_end + 1, end) if b > a]
        out["speed unsure"] = (max(tries) - min(tries)) / 2
    out["noise"] = sigma
    out["turns back"] = 1 if turns else 0
    return out


# ---------------------------------------------------------------- whole films
MEASURES = ("across", "updown", "turns back")
QUANTITIES = ("count", "speed", "start", "end", "mass", "size", "height", "place")
TOUCH = 3.0         # pixels: two things this close have met


def categories(brain):
    """The kinds of motion it can tell apart: which kind of law (by its list of kinds),
    across and up-down, and whether it came back the way it went."""
    k = len(motion_kinds(brain))
    out = {m: {"groups": [[float(i), float(i)] for i in range(k)], "turn": 0.0}
           for m in ("across", "updown")}
    out["turns back"] = {"groups": [[0.0, 0.0], [1.0, 1.0]], "turn": 0.0}
    return out


def watch(brain, frames):
    """A film as the things in it: what each looks like and what it did, and how heavy
    some are compared with others (when they met)."""
    from ..senses.things import watch_film
    kinds = motion_kinds(brain)
    tracks = watch_film(brain.eyes, frames)
    # while two things touch, what it sees of each is not to be trusted: set it aside
    meet = {}
    for i in range(len(tracks)):
        for j in range(i + 1, len(tracks)):
            w = _meeting(tracks[i], tracks[j])
            # they touched when it lost sight of one of them while they were that close
            if w is not None and any(f not in tracks[k]["t"] for k in (i, j)
                                     for f in range(w[0], w[1] + 1)):
                meet[(i, j)] = w
                for k in (i, j):
                    tr = tracks[k]
                    keep = [n for n, t in enumerate(tr["t"]) if not w[0] <= t <= w[1]]
                    if len(keep) >= 6:
                        for key in ("t", "x", "y"):
                            tr[key] = [tr[key][n] for n in keep]
    things, raw = [], []
    for tr in tracks:
        m = motion(tr, kinds)
        span = max(tr["t"][-1] - tr["t"][0], 1)
        sx, sy = m["noise"]["x"], m["noise"]["y"]
        t = dict(tr["look"])
        t.update({k: m[k] for k in MEASURES})
        t["q"] = {"count": [1, 0.0],
                  "size": [tr["look"]["size"], tr["size_se"]],
                  "height": [-tr["y"][0], sy], "place": [tr["x"][0], sx]}
        if m["start"] is not None:
            t["q"]["start"] = [m["start"], 0.5]
            t["q"]["end"] = [m["end"], 0.5]
            t["q"]["speed"] = [round(m["speed"], 4),
                               round(math.hypot(math.hypot(sx, sy) / span * 2,
                                                m["speed unsure"]), 4)]
        things.append(t)
        raw.append((tr, m))
    return {"things": things, "masses": _meetings(brain, raw, kinds, meet)}


def _speed_se(p, sigma):
    n = max(p["to"] - p["from"] + 1, 2)
    return sigma * math.sqrt(12.0 / (n ** 3)) if p["kind"] else 0.0


def _piece_at(ps, t):
    return next((p for p in ps if p["from"] <= t <= p["to"]), None)


def _meeting(ti, tj):
    """The pictures during which two things were touching (or so close it lost sight of
    one), as (first, last), or None if they never met."""
    seen_i = {t: (x, y) for t, x, y in zip(ti["t"], ti["x"], ti["y"])}
    seen_j = {t: (x, y) for t, x, y in zip(tj["t"], tj["x"], tj["y"])}
    frames = range(min(ti["t"][0], tj["t"][0]), max(ti["t"][-1], tj["t"][-1]) + 1)

    def gap(f):
        (xi, yi), (xj, yj) = seen_i[f], seen_j[f]
        return max(abs(xi - xj) - (ti["reach"] + tj["reach"]),
                   abs(yi - yj) - (ti["reach_y"] + tj["reach_y"]))

    near = [f for f in frames if f in seen_i and f in seen_j and gap(f) <= TOUCH]
    # or one lost from sight right after they came within a picture's move of touching
    for f in frames:
        if (f not in seen_i or f not in seen_j) and f - 1 in seen_i and f - 1 in seen_j \
                and f - 2 in seen_i and f - 2 in seen_j:
            step = sum(abs(a - b) for a, b in zip(seen_i[f - 1] + seen_j[f - 1],
                                                  seen_i[f - 2] + seen_j[f - 2]))
            if gap(f - 1) - step <= TOUCH:
                near.append(f)
    if not near:
        return None
    a, b = min(near), max(near)
    # while touching, either may be lost from sight: the meeting lasts until both are seen
    while a - 1 in frames and (a - 1 not in seen_i or a - 1 not in seen_j):
        a -= 1
    while b + 1 in frames and (b + 1 not in seen_i or b + 1 not in seen_j):
        b += 1
    return a, b


def _meetings(brain, raw, kinds, meet):
    """When two things meet and both change speed, its own law of what stays the same
    when things knock together (Σ m^p·v^q, lesson 5) says how heavy one is compared
    with the other: m_i/m_j = (-Δ(v_j^q) / Δ(v_i^q))^(1/p), with the speeds of the moves
    before and after the meeting. Returns {"i,j": [log2(m_i/m_j), how sure, when]}."""
    law = next((l for l in brain.claws.get("collide", []) if l.scope == "all"), None)
    if law is None:
        return {}
    p, q = law.powers.get("m", 1), law.powers.get("v", 1)

    def power(v):
        return math.copysign(abs(v) ** q, v)

    out = {}
    for i in range(len(raw)):
        for j in range(i + 1, len(raw)):
            (ti, mi), (tj, mj) = raw[i], raw[j]
            when = meet.get((i, j))
            if when is None:
                continue
            dv, se = [], []
            for tr, m in ((ti, mi), (tj, mj)):
                before = [t for t in tr["t"] if t < when[0]]
                after = [t for t in tr["t"] if t > when[1]]
                if not before or not after:
                    break
                pa = _piece_at(m["pieces"]["x"], before[-1])
                pb = _piece_at(m["pieces"]["x"], after[0])
                if pa is None or pb is None or pa is pb:
                    break
                va, vb = _at(pa, kinds, before[-1], True), _at(pb, kinds, after[0], True)
                dv.append(power(vb) - power(va))
                se.append(math.hypot(_speed_se(pa, m["noise"]["x"]),
                                     _speed_se(pb, m["noise"]["x"])) * q * max(abs(va), abs(vb), 1e-9) ** (q - 1))
            if len(dv) < 2 or dv[0] * dv[1] >= 0:
                continue                # not a knock: both must change, opposite ways
            if min(abs(dv[0]) - 2 * se[0], abs(dv[1]) - 2 * se[1]) <= 0:
                continue
            ratio = (-dv[1] / dv[0]) ** (1.0 / p)               # m_i / m_j
            rel = math.hypot(se[0] / abs(dv[0]), se[1] / abs(dv[1])) / p
            out[f"{i},{j}"] = [round(math.log2(ratio), 4), round(rel / math.log(2), 4),
                               round((when[0] + when[1]) / 2, 2)]
    return out


def kinds_of_thing(brain, thing):
    """A thing seen in a film, as the groups it is in: what it looks like and how it
    moved."""
    from .categories import kinds_of
    out = kinds_of(brain.categories, thing)
    for m in MEASURES:
        if m in thing:
            out[m] = int(thing[m])
    return out


def compare(film, a, b, quantity):
    """Is the first group more than the second in this quantity? True, False, or None
    when it can't tell (the difference is within twice how sure it is, or it can't
    measure it). a and b are lists of thing indices."""
    if quantity == "count":
        return None if len(a) == len(b) else len(a) > len(b)
    if len(a) != 1 or len(b) != 1:
        return None
    i, j = a[0], b[0]
    if i == j:
        return None
    if quantity == "mass":
        key, sign = (f"{i},{j}", 1) if i < j else (f"{j},{i}", -1)
        m = film["masses"].get(key)
        if m is None or abs(m[0]) <= 2 * m[1]:
            return None
        return sign * m[0] > 0
    qa, qb = film["things"][i]["q"].get(quantity), film["things"][j]["q"].get(quantity)
    if qa is None or qb is None:
        return None
    if abs(qa[0] - qb[0]) <= 2 * math.hypot(qa[1], qb[1]):
        return None
    return qa[0] > qb[0]
