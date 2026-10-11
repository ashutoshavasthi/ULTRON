"""A small network trained on one puzzle alone (prototype; NOT used by the solver).

Measured on the 185 unsolved same-size training tasks: 0 right, 1 wrong, 184 no
answer (861 s on one CPU core). It is kept so the measurement can be reproduced:
    for each task: neural.answer(train_pairs, test_inputs)
A tiny network trained for 300 steps on 2-4 examples does not generalise; results
like CompressARC's need far larger networks and GPU-length training.


When no short program explains a puzzle, Ultron can still try a different kind of
explanation: a small convolutional network (numpy, written out by hand, as its eyes
are) that learns, from the puzzle's own examples only, what colour each cell becomes
given what is around it. Nothing is pretrained; nothing outside the puzzle is used.

A network can fit anything, so it must earn the right to answer the way any law does
in Ultron: it is trained on all the examples but one and must predict the one left out
EXACTLY, for every example in turn. Only then does it answer the test. Otherwise it
says nothing.
"""

import numpy as np

from .eyes_math import col2im, im2col

HIDDEN = 24
STEPS = 300
LR = 0.01


def _onehot(g):
    x = np.zeros((10,) + g.shape)
    for c in range(10):
        x[c] = g == c
    return x


class Net:
    def __init__(self, seed=0, hidden=HIDDEN):
        rng = np.random.default_rng(seed)
        sizes = [(10, hidden), (hidden, hidden), (hidden, 10)]
        self.params = [[rng.normal(0, np.sqrt(2.0 / (ci * 9)), size=(ci * 9, co)),
                        np.zeros(co)] for ci, co in sizes]
        self.m = [[np.zeros_like(w), np.zeros_like(b)] for w, b in self.params]
        self.v = [[np.zeros_like(w), np.zeros_like(b)] for w, b in self.params]
        self.t = 0

    def forward(self, x):
        cache, a = [], x
        for li, (w, b) in enumerate(self.params):
            n, _, h, wd = a.shape
            cols = im2col(a)
            z = cols @ w + b
            out = z.reshape(n, h, wd, -1).transpose(0, 3, 1, 2)
            cache.append((a.shape, cols, z))
            a = np.maximum(out, 0) if li < len(self.params) - 1 else out
        return a, cache

    def step(self, xs, ys):
        """One step of Adam on cross-entropy over every cell of every example."""
        grads = [[np.zeros_like(w), np.zeros_like(b)] for w, b in self.params]
        loss = 0.0
        for x, y in zip(xs, ys):
            logits, cache = self.forward(x[None])
            z = logits[0] - logits[0].max(axis=0, keepdims=True)
            p = np.exp(z) / np.exp(z).sum(axis=0, keepdims=True)
            loss -= np.log(np.take_along_axis(p, y[None], 0) + 1e-12).mean()
            d = p.copy()
            np.put_along_axis(d, y[None], np.take_along_axis(d, y[None], 0) - 1, 0)
            d = d[None] / y.size
            for li in range(len(self.params) - 1, -1, -1):
                shape, cols, zl = cache[li]
                n, _, h, wd = shape
                dz = d.transpose(0, 2, 3, 1).reshape(n, h * wd, -1)
                if li < len(self.params) - 1:
                    dz = dz * (zl > 0)
                grads[li][0] += cols.reshape(-1, cols.shape[-1]).T @ dz.reshape(-1, dz.shape[-1])
                grads[li][1] += dz.sum(axis=(0, 1))
                if li:
                    d = col2im(dz @ self.params[li][0].T, shape)
        self.t += 1
        for li, (w, b) in enumerate(self.params):
            for k, g in enumerate(grads[li]):
                self.m[li][k] = 0.9 * self.m[li][k] + 0.1 * g
                self.v[li][k] = 0.999 * self.v[li][k] + 0.001 * g * g
                mh = self.m[li][k] / (1 - 0.9 ** self.t)
                vh = self.v[li][k] / (1 - 0.999 ** self.t)
                self.params[li][k] -= LR * mh / (np.sqrt(vh) + 1e-8)
        return loss / len(xs)

    def predict(self, g):
        logits, _ = self.forward(_onehot(g)[None])
        return logits[0].argmax(axis=0).astype(g.dtype)


def fit(pairs, seed=0, steps=STEPS):
    net = Net(seed)
    xs = [_onehot(i) for i, _ in pairs]
    ys = [o.astype(np.int64) for _, o in pairs]
    for _ in range(steps):
        net.step(xs, ys)
    return net


def earns_its_answer(pairs, seed=0):
    """Trained without each example in turn, does it predict that example exactly?"""
    if len(pairs) < 2:
        return False
    for k in range(len(pairs)):
        rest = pairs[:k] + pairs[k + 1:]
        net = fit(rest, seed)
        if not np.array_equal(net.predict(pairs[k][0]), pairs[k][1]):
            return False
    return True


def answer(train, tests, seed=0):
    """The network's answers for the tests, or None if it hasn't earned the right."""
    if any(i.shape != o.shape for i, o in train):
        return None
    if not earns_its_answer(train, seed):
        return None
    net = fit(train, seed)
    return [net.predict(t) for t in tests]
