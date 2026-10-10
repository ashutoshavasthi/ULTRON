"""A retina in front of the eyes, the part of vision that is innate in animals too.

Real pictures are not like the camera simulator's: the light is uneven, the contrast
is low, and things may be darker than the background instead of brighter. A retina
copes before any learning: each point is compared with its surroundings (centre minus
surround, as retinal ganglion cells do), the result is scaled by how noisy the picture
is (contrast adaptation), and there are two channels, ON (lighter than around it) and
OFF (darker than around it). After the retina, a spot looks the same to the eyes
whatever the lighting.
"""

import numpy as np

SURROUND = 15       # pixels: the size of the neighbourhood a point is compared with


def luminance(img):
    a = np.asarray(img, dtype=float)
    if a.ndim == 3:
        a = a[:, :, :3] @ np.array([0.299, 0.587, 0.114])
    return a


def _box(a, k):
    """Mean over a k×k neighbourhood (edges: what is available)."""
    pad = k // 2
    p = np.pad(a, pad, mode="reflect")
    c = np.cumsum(np.cumsum(p, axis=0), axis=1)
    c = np.pad(c, ((1, 0), (1, 0)))
    h, w = a.shape
    s = c[k:k + h, k:k + w] - c[:h, k:k + w] - c[k:k + h, :w] + c[:h, :w]
    return s / (k * k)


def channels(img):
    """(ON, OFF) pictures, in the same units the eyes grew up with: background 0.1,
    noise about 0.08, a clear thing about 0.6-1."""
    a = luminance(img)
    centre = _box(a, 3)
    diff = centre - _box(a, SURROUND)
    noise = 1.4826 * np.median(np.abs(diff - np.median(diff))) or 1e-9
    z = diff / noise
    scale = 0.08 * 1.5          # a 1-sigma wobble of the averaged centre ≈ camera noise
    on = np.clip(0.1 + scale * z, 0.0, 1.0)
    off = np.clip(0.1 - scale * z, 0.0, 1.0)
    return on, off
