"""Ultron's eyes: a small neural network it trains itself, grounded by touch.

The network turns a picture into a map of "something is here". It is three
convolution layers (3x3 filters: 1 -> 8 -> 8 -> 1 channels), trained with plain
gradient descent (Adam) written out by hand in numpy. Nothing about objects is
built in except what a newborn plausibly has: looking for the strongest spots in
the map (local peaks), and looking again when unsure.

How it learns, like a child: while it handles things, touch tells it where each
object is. The pictures it sees at the same moment, paired with those touches, are
its training data. After that lesson touch is gone, and the eyes are all it has.
It also learns how strong a spot must be to count as a thing, by choosing the
threshold that best matches what its hands felt, and remembers what the pictures it
learned from were like (how noisy, how bright its things were).

Counting a still scene uses three things animals do too (Stage 2: eyes that generalise):
  * look longer when the picture is noisier than usual: several pictures of the still
    scene, lined up against the camera's shake, averaged until the picture is a little
    cleaner than the ones its eyes are used to (its own noise measure, as the retina's);
  * adapt to the light: the background put where its eyes are used to it, and in a dim
    scene, after looking long enough that something really stands out, the contrast
    turned up to what it is used to;
  * step back: the picture also looked at shrunk 2x and 3x, keeping the view where its
    eyes respond most strongly (where things look like the things it learned).

Looking closely at a crowd, it also explains away: two things just touching make one
ridge in its map, not two peaks, and the dimmer one sits on its neighbour's shoulder.
From touch it knows what one thing looks like in its map (its footprint); taking away
what each thing it saw accounts for, whatever still clearly stands out right beside one
of them is a thing too. How strong such a leftover must be is learned from touch as
well: clearly stronger than any leftover its hands said was nothing.
"""

import numpy as np

LAYERS = ((1, 8), (8, 8), (8, 1))
SIGMA = 0.7         # how wide a spot it learns to light up where its hands felt a thing
BACKGROUND = 0.1    # where the background sits in the pictures its eyes grew up with
DIM = 0.45          # things standing out less than this (of what it's used to): a dim scene
STEP_BACK = 1.5     # a view from further back must look this much clearer to be preferred
CLEANER = 0.8       # a noisy scene is looked at until it is this clean (of what it's used to)
CROWDED = 5.0       # things this close (median distance to a neighbour, pixels): crowded
CROWDED_LOOKS = 4   # pictures it averages when a scene is crowded
FOOT = 3            # one thing's footprint in the map: (2·FOOT + 1)² pixels
ALONE = 7.0         # a handled thing this far from any other shows its footprint alone
NEAR = 4.0          # a thing hidden on a neighbour's shoulder is this close to it (pixels)
CLEARLY = 1.2       # a leftover must be this much stronger than any its hands said was nothing


def _box(a, k):
    """Mean over a k x k neighbourhood."""
    pad = k // 2
    p = np.pad(a, pad, mode="reflect")
    c = np.pad(np.cumsum(np.cumsum(p, axis=0), axis=1), ((1, 0), (1, 0)))
    h, w = a.shape
    return (c[k:k + h, k:k + w] - c[:h, k:k + w] - c[k:k + h, :w] + c[:h, :w]) / (k * k)


def noise_of(img):
    """How noisy a picture is, measured from the picture itself (robust spread of what
    is left after smoothing)."""
    r = np.asarray(img, dtype=float) - _box(np.asarray(img, dtype=float), 3)
    return float(1.4826 * np.median(np.abs(r - np.median(r))))


def contrast_of(img):
    """How far the brightest thing stands out from the background."""
    a = np.asarray(img, dtype=float)
    return float(np.max(_box(a, 3)) - np.median(a))


def _align(ref, img, r=2):
    """img shifted by the few pixels that line it up best with ref (camera shake)."""
    best = None
    rc = ref - ref.mean()
    for dy in range(-r, r + 1):
        for dx in range(-r, r + 1):
            s = np.roll(np.roll(img, dy, 0), dx, 1)
            c = float(((s - s.mean()) * rc).sum())
            if best is None or c > best[0]:
                best = (c, s)
    return best[1]


def _crowding(seen):
    """How close things sit: the median distance from each to its nearest neighbour."""
    if len(seen) < 2:
        return float("inf")
    p = np.array([(x, y) for x, y, _ in seen])
    d = np.sqrt(((p[:, None] - p[None]) ** 2).sum(-1))
    np.fill_diagonal(d, np.inf)
    return float(np.median(d.min(axis=1)))


def _shrink(img, s):
    h, w = (img.shape[0] // s) * s, (img.shape[1] // s) * s
    return img[:h, :w].reshape(h // s, s, w // s, s).mean(axis=(1, 3))


# ------------------------------------------------------------------ convolution
def _im2col(x):
    n, c, h, w = x.shape
    xp = np.pad(x, ((0, 0), (0, 0), (1, 1), (1, 1)))
    patches = np.stack([xp[:, :, i:i + h, j:j + w] for i in range(3) for j in range(3)],
                       axis=2)                                   # n, c, 9, h, w
    return patches.transpose(0, 3, 4, 1, 2).reshape(n, h * w, c * 9)


def _col2im(cols, shape):
    n, c, h, w = shape
    d = cols.reshape(n, h, w, c, 9).transpose(0, 3, 4, 1, 2)     # n, c, 9, h, w
    xp = np.zeros((n, c, h + 2, w + 2))
    k = 0
    for i in range(3):
        for j in range(3):
            xp[:, :, i:i + h, j:j + w] += d[:, :, k]
            k += 1
    return xp[:, :, 1:-1, 1:-1]


class Eyes:
    def __init__(self, seed=0):
        rng = np.random.default_rng(seed)
        self.params = []
        for cin, cout in LAYERS:
            w = rng.normal(0.0, np.sqrt(2.0 / (cin * 9)), size=(cin * 9, cout))
            self.params.append([w, np.zeros(cout)])
        self.threshold = 0.5
        self.trained_on = 0
        self.noise_ref = 0.08       # how noisy the pictures it learned from were
        self.contrast_ref = 0.75    # how far their things stood out
        self.footprint = None       # what one thing looks like in its map (learned by touch)
        self.leftover = None        # how strong a leftover beside a thing must be to be one

    # ---------------------------------------------------------------- network
    def _forward(self, x):
        cache, a = [], x
        for li, (w, b) in enumerate(self.params):
            n, _, h, wd = a.shape
            cols = _im2col(a)
            z = cols @ w + b                                     # n, h*w, cout
            out = z.reshape(n, h, wd, -1).transpose(0, 3, 1, 2)
            relu = li < len(self.params) - 1
            cache.append((a.shape, cols, z, relu))
            a = np.maximum(out, 0.0) if relu else out
        return a, cache

    def heat(self, img):
        """The 'something is here' map for one picture. (Looking is the same sums as
        learning, done a filter position at a time so big pictures need little memory.)"""
        a = np.asarray(img, dtype=np.float32)[None]               # channels, h, w
        for li, (w, b) in enumerate(self.params):
            cin = a.shape[0]
            h, wd = a.shape[1:]
            p = np.pad(a, ((0, 0), (1, 1), (1, 1)))
            k = w.astype(np.float32).reshape(cin, 9, -1)          # (c, position, out)
            out = np.empty((w.shape[1], h, wd), dtype=np.float32)
            out[:] = b.astype(np.float32)[:, None, None]
            for pos in range(9):
                i, j = divmod(pos, 3)
                shifted = p[:, i:i + h, j:j + wd].reshape(cin, -1)
                out += (k[:, pos, :].T @ shifted).reshape(-1, h, wd)
            a = np.maximum(out, 0.0) if li < len(self.params) - 1 else out
        return a[0].astype(float)

    def learn(self, images, touches, seed=0, epochs=14, batch=16, lr=0.01):
        """images: pictures; touches: for each, the (x, y) where its hands felt things."""
        x = np.stack([np.asarray(im, dtype=float) for im in images])[:, None]
        y = np.stack([_target(im.shape, t) for im, t in zip(images, touches)])[:, None]
        rng = np.random.default_rng(seed)
        m = [[np.zeros_like(w), np.zeros_like(b)] for w, b in self.params]
        v = [[np.zeros_like(w), np.zeros_like(b)] for w, b in self.params]
        step, losses = 0, []
        for _ in range(epochs):
            order = rng.permutation(len(x))
            total = 0.0
            for s in range(0, len(x), batch):
                idx = order[s:s + batch]
                out, cache = self._forward(x[idx])
                diff = out - y[idx]
                # things are rare in a picture: errors on them count more
                weight = 1.0 + 4.0 * y[idx]
                total += float(np.sum(weight * diff ** 2))
                grad = 2.0 * weight * diff / diff.size
                step += 1
                for li in range(len(self.params) - 1, -1, -1):
                    shape, cols, z, relu = cache[li]
                    n, _, h, wd = shape
                    g = grad.transpose(0, 2, 3, 1).reshape(n, h * wd, -1)
                    if relu:
                        g = g * (z > 0)
                    w, b = self.params[li]
                    gw = cols.reshape(-1, cols.shape[-1]).T @ g.reshape(-1, g.shape[-1])
                    gb = g.sum(axis=(0, 1))
                    grad = _col2im(g @ w.T, shape)
                    for pi, gp in enumerate((gw, gb)):
                        m[li][pi] = 0.9 * m[li][pi] + 0.1 * gp
                        v[li][pi] = 0.999 * v[li][pi] + 0.001 * gp * gp
                        mh = m[li][pi] / (1 - 0.9 ** step)
                        vh = v[li][pi] / (1 - 0.999 ** step)
                        self.params[li][pi] = self.params[li][pi] - lr * mh / (np.sqrt(vh) + 1e-8)
            losses.append(total / len(x))
        self.trained_on += len(images)
        self._calibrate(images, touches)
        self._learn_footprint(images, touches)
        self.noise_ref = float(np.median([noise_of(im) for im in images]))
        self.contrast_ref = float(np.median([contrast_of(im) for im, t in zip(images, touches)
                                             if len(t)]))
        return losses

    def _calibrate(self, images, touches):
        """How strong must a spot be to be a thing? The one that best matches touch."""
        # every candidate spot once; a stronger threshold just keeps fewer of them
        strengths = [[p[2] for p in _peaks(self.heat(im), 0.05)] for im in images]
        best = None
        for th in np.arange(0.05, 0.85, 0.025):
            right = sum(sum(v > th for v in st) == len(t) for st, t in zip(strengths, touches))
            if best is None or right > best[0]:
                best = (right, float(round(th, 3)))
        self.threshold = best[1]

    def _learn_footprint(self, images, touches):
        """What one thing looks like in its map, from things its hands found alone; and how
        strong a leftover must be: clearly stronger than any its hands said was nothing."""
        acc, k = np.zeros((2 * FOOT + 1, 2 * FOOT + 1)), 0
        maps = [self.heat(im) for im in images]
        for hm, t in zip(maps, touches):
            h, w = hm.shape
            p = np.array(t, dtype=float).reshape(-1, 2)
            for i, (x, y) in enumerate(p):
                d = np.hypot(p[:, 0] - x, p[:, 1] - y)
                d[i] = np.inf
                xi, yi = int(round(x)), int(round(y))
                if d.min() > ALONE and FOOT <= xi < w - FOOT and FOOT <= yi < h - FOOT:
                    patch = hm[yi - FOOT:yi + FOOT + 1, xi - FOOT:xi + FOOT + 1]
                    if patch[FOOT, FOOT] > 0:
                        acc += patch / patch[FOOT, FOOT]
                        k += 1
        if not k:
            self.footprint = self.leftover = None
            return
        self.footprint = acc / k
        nothing = 0.0
        for hm, t in zip(maps, touches):
            seen = _peaks(hm, self.threshold)
            for x, y, v in self._leftovers(hm, seen, 0.0):
                felt = [(a, b) for a, b in t if np.hypot(a - x, b - y) <= 1.5]
                hidden = any(min(np.hypot(a - sx, b - sy) for sx, sy, _ in seen) > 1.5
                             for a, b in felt)
                if not hidden:
                    nothing = max(nothing, v)
        self.leftover = float(CLEARLY * max(nothing, self.threshold))

    def _leftovers(self, hm, seen, threshold):
        """Spots that still stand out right beside a thing seen, once what each thing seen
        accounts for (its footprint, as strong as it is) is taken away."""
        h, w = hm.shape
        rest = hm.copy()
        for x, y, v in seen:
            xi, yi = int(round(x)), int(round(y))
            y0, y1 = max(0, yi - FOOT), min(h, yi + FOOT + 1)
            x0, x1 = max(0, xi - FOOT), min(w, xi + FOOT + 1)
            rest[y0:y1, x0:x1] -= v * self.footprint[y0 - yi + FOOT:y1 - yi + FOOT,
                                                     x0 - xi + FOOT:x1 - xi + FOOT]
        out = []
        for q in _peaks(rest, threshold):
            d2 = [(q[0] - x) ** 2 + (q[1] - y) ** 2 for x, y, _ in seen]
            if d2 and 2.0 ** 2 < min(d2) <= NEAR ** 2:
                out.append(q)
        return out

    # ---------------------------------------------------------------- seeing
    def see_closely(self, img):
        """The things in one picture, a crowd looked at closely: the things it sees, and
        those hidden on a neighbour's shoulder (explaining away)."""
        hm = self.heat(img)
        seen = _peaks(hm, self.threshold)
        if self.footprint is None or not seen:
            return seen
        return sorted(seen + self._leftovers(hm, seen, self.leftover),
                      key=lambda p: (p[1], p[0]))

    def see(self, img):
        """The things in one picture: [(x, y, strength)], positions to a fraction of a pixel."""
        return _peaks(self.heat(img), self.threshold)

    def count(self, look, glances=5):
        """How many things in a still scene? Looks (longer if it must), steps back if it
        helps, and looks again until two glances agree."""
        seen = []
        for _ in range(glances):
            seen.append(len(self.look_at(look)))
            for n in set(seen):
                if seen.count(n) >= 2:
                    return n, len(seen)
        return max(set(seen), key=lambda n: (seen.count(n), -n)), len(seen)

    def look_at(self, look):
        """The things in a still scene. In a crowded scene, where neighbours can blur into
        one, it looks a little longer (a few pictures lined up and averaged) and closely
        (explaining away)."""
        img = self.stare(look)
        seen = self.see_views(img)
        if _crowding(seen) <= CROWDED:
            frames = [img] + [look() for _ in range(CROWDED_LOOKS - 1)]
            avg = np.mean(frames, axis=0)
            for _ in range(2):
                frames = [_align(avg, f) for f in frames]
                avg = np.mean(frames, axis=0)
            closer = self.see_closely(self._adapt(avg))
            if len(closer) >= len(seen):
                seen = closer
        return seen

    # ---------------------------------------------------------------- still scenes
    def stare(self, look, cap=64):
        """One picture of a still scene, as clean and as clear as the ones it learned from."""
        first = look()
        if noise_of(first) <= 1.25 * self.noise_ref and \
                contrast_of(first) >= DIM * self.contrast_ref:
            return first                # like the pictures its eyes are used to: one look
        avg, frames = self._longer(look, [first], CLEANER * self.noise_ref, cap)
        c = contrast_of(avg)
        if c < DIM * self.contrast_ref:
            # a dim scene: look longer still; if something really stands out, turn the
            # contrast up to what its eyes are used to
            avg2, frames = self._longer(look, frames,
                                        CLEANER * self.noise_ref * c / self.contrast_ref, cap)
            c2 = contrast_of(avg2)
            if c2 > 6 * noise_of(avg2):
                g = min(self.contrast_ref / c2, 6.0)
                avg = np.median(avg2) + g * (avg2 - np.median(avg2))
        return self._adapt(avg)

    def _adapt(self, img):
        """Adapt to the light: the background put where its eyes are used to it, when it
        is noticeably elsewhere."""
        off = float(np.median(img)) - BACKGROUND
        return np.clip(img - off, 0.0, 1.0) if abs(off) > 0.5 * self.noise_ref else img

    def _longer(self, look, frames, target, cap):
        avg = np.mean(frames, axis=0)
        while noise_of(avg) > target and len(frames) < cap:
            frames = frames + [look() for _ in range(len(frames))]
            avg = np.mean(frames, axis=0)
            for _ in range(2):          # line each picture up against the camera's shake
                frames = [_align(avg, f) for f in frames]
                avg = np.mean(frames, axis=0)
        return avg, frames

    def see_views(self, img, scales=(1, 2, 3)):
        """Step back: the picture as it is and shrunk; the view where its eyes respond
        most strongly (positions given in the picture's own pixels)."""
        best = None
        for s in scales:
            view = _shrink(img, s) if s > 1 else img
            # close up, crowds are looked at closely; stepping back is for big things
            seen = self.see_closely(self._adapt(view)) if s == 1 else self.see(self._adapt(view))
            strength = float(np.mean([p[2] for p in seen])) if seen else 0.0
            # step back only when things clearly look more like what its eyes learned
            if best is None or strength > STEP_BACK * best[0]:
                best = (strength, [(x * s + (s - 1) / 2, y * s + (s - 1) / 2, v)
                                   for x, y, v in seen])
        return best[1]

    def to_json(self):
        return {"layers": [[w.tolist(), b.tolist()] for w, b in self.params],
                "threshold": self.threshold, "trained_on": self.trained_on,
                "noise_ref": self.noise_ref, "contrast_ref": self.contrast_ref,
                "footprint": self.footprint.tolist() if self.footprint is not None else None,
                "leftover": self.leftover}

    @classmethod
    def from_json(cls, d):
        e = cls()
        e.params = [[np.array(w, dtype=float), np.array(b, dtype=float)] for w, b in d["layers"]]
        e.threshold = d["threshold"]
        e.trained_on = d.get("trained_on", 0)
        e.noise_ref = d.get("noise_ref", e.noise_ref)
        e.contrast_ref = d.get("contrast_ref", e.contrast_ref)
        if d.get("footprint") is not None:
            e.footprint = np.array(d["footprint"], dtype=float)
            e.leftover = d["leftover"]
        return e


def _target(shape, touches):
    h, w = shape
    yy, xx = np.mgrid[0:h, 0:w]
    t = np.zeros(shape)
    for x, y in touches:
        t = np.maximum(t, np.exp(-((xx - x) ** 2 + (yy - y) ** 2) / (2 * SIGMA ** 2)))
    return t


def _peaks(hm, threshold):
    h, w = hm.shape
    p = np.pad(hm, 1, constant_values=-np.inf)
    neigh = np.stack([p[i:i + h, j:j + w] for i in range(3) for j in range(3)
                      if (i, j) != (1, 1)])
    is_peak = (hm > threshold) & np.all(hm >= neigh, axis=0)
    out = []
    for y, x in zip(*np.nonzero(is_peak)):
        # the top of a parabola through the peak and its two neighbours, each way
        fx, fy = float(x), float(y)
        if 0 < x < w - 1:
            l, c, r = hm[y, x - 1], hm[y, x], hm[y, x + 1]
            d = l - 2 * c + r
            if d < 0:
                fx += float(np.clip((l - r) / (2 * d), -0.5, 0.5))
        if 0 < y < h - 1:
            u, c, dn = hm[y - 1, x], hm[y, x], hm[y + 1, x]
            d = u - 2 * c + dn
            if d < 0:
                fy += float(np.clip((u - dn) / (2 * d), -0.5, 0.5))
        out.append((fx, fy, float(hm[y, x])))
    # two peaks right next to each other are one thing seen twice
    out.sort(key=lambda p: -p[2])
    kept = []
    for q in out:
        if all((q[0] - k[0]) ** 2 + (q[1] - k[1]) ** 2 > 2.0 ** 2 for k in kept):
            kept.append(q)
    return sorted(kept, key=lambda p: (p[1], p[0]))
