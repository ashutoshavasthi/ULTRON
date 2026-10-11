"""A simulated camera: the world as noisy grayscale pixels, nothing else.

Every picture has the nuisances of a real cheap camera: sensor noise, blur, a
background that isn't flat, the camera shaking by a pixel, objects of different
sizes and brightness, and now and then a spoiled frame (a hand in the way, or a
dropped frame). The world's true state stays with the simulator; only the Judge
may read it.
"""

import numpy as np

NOISE = 0.08          # sensor noise (standard deviation, in units of full brightness)
SPOILED = 0.02        # fraction of frames spoiled by a hand in the way or dropped


def _blob(img, x, y, r, b):
    h, w = img.shape
    yy, xx = np.mgrid[0:h, 0:w]
    d = np.sqrt((xx - x) ** 2 + (yy - y) ** 2)
    img += b * np.clip(r + 0.5 - d, 0.0, 1.0)


def _blur(img):
    k = np.array([0.25, 0.5, 0.25])
    img = np.apply_along_axis(lambda row: np.convolve(row, k, mode="same"), 1, img)
    return np.apply_along_axis(lambda col: np.convolve(col, k, mode="same"), 0, img)


def shoot(blobs, rng, size=48, jitter=True, spoil=True, noise=NOISE):
    """blobs: [(x, y, radius, brightness)] in pixel coordinates. Returns (image, shake)
    where shake is the camera's (dx, dy) that frame (hidden from Ultron)."""
    h, w = (size, size) if isinstance(size, int) else size
    img = np.zeros((h, w))
    dx, dy = (int(rng.integers(-1, 2)), int(rng.integers(-1, 2))) if jitter else (0, 0)
    for x, y, r, b in blobs:
        _blob(img, x + dx, y + dy, r, b)
    img = _blur(img)
    gx, gy = rng.uniform(-0.05, 0.05, size=2)
    yy, xx = np.mgrid[0:h, 0:w]
    img += 0.1 + gx * (xx / w - 0.5) + gy * (yy / h - 0.5)
    if spoil and rng.random() < SPOILED:
        if rng.random() < 0.5:
            img[:] = 0.1                    # a dropped frame: nothing to see
        else:
            x0, y0 = int(rng.integers(0, w // 2)), int(rng.integers(0, h // 2))
            img[y0:y0 + h // 2, x0:x0 + w // 2] = 0.05     # a hand in the way
    img += rng.normal(0.0, noise, size=img.shape)
    return np.clip(img, 0.0, 1.0), (dx, dy)


def scatter(n, rng, size=48, margin=4, gap=5.0, radius=(1.4, 2.6)):
    """n objects placed at random, never overlapping (as things on a tray)."""
    pts, tries = [], 0
    while len(pts) < n:
        tries += 1
        if tries > 20000:
            raise ValueError(f"can't fit {n} objects")
        x, y = rng.uniform(margin, size - margin, size=2)
        if all((x - a) ** 2 + (y - b) ** 2 >= gap ** 2 for a, b, _, _ in pts):
            pts.append((float(x), float(y), float(rng.uniform(*radius)),
                        float(rng.uniform(0.55, 1.0))))
    return pts
