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
threshold that best matches what its hands felt.
"""

import numpy as np

LAYERS = ((1, 8), (8, 8), (8, 1))
SIGMA = 1.0


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

    # ---------------------------------------------------------------- seeing
    def see(self, img):
        """The things in one picture: [(x, y, strength)], positions to a fraction of a pixel."""
        return _peaks(self.heat(img), self.threshold)

    def count(self, look, glances=5):
        """How many things? Looks, and looks again until two glances agree."""
        seen = []
        for _ in range(glances):
            seen.append(len(self.see(look())))
            for n in set(seen):
                if seen.count(n) >= 2:
                    return n, len(seen)
        return max(set(seen), key=lambda n: (seen.count(n), -n)), len(seen)

    def to_json(self):
        return {"layers": [[w.tolist(), b.tolist()] for w, b in self.params],
                "threshold": self.threshold, "trained_on": self.trained_on}

    @classmethod
    def from_json(cls, d):
        e = cls()
        e.params = [[np.array(w, dtype=float), np.array(b, dtype=float)] for w, b in d["layers"]]
        e.threshold = d["threshold"]
        e.trained_on = d.get("trained_on", 0)
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
