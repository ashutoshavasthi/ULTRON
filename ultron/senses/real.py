"""What Ultron does with a real film: look through the retina, decide which channel
shows things that last, improve its eyes on what lasted (no labels), follow things,
and measure how far they get."""

import copy

import numpy as np

from . import track
from .retina import channels


def looks(eyes, pictures, channel):
    return [eyes.see(channels(p)[channel]) for p in pictures]


def choose_channel(eyes, pictures):
    """ON or OFF? The one whose things last from picture to picture (real things do)."""
    best = None
    for ch, name in ((0, "ON"), (1, "OFF")):
        dets = looks(eyes, pictures, ch)
        tracks = track.link(dets)
        seen = sum(len(d) for d in dets) or 1
        lasting = sum(len(t) for t in track.lasting(tracks, len(pictures) // 2)) / seen
        if best is None or lasting > best[1]:
            best = (ch, lasting, name)
    return best


def self_teach(eyes, pictures, channel, tracks, replay, seed=0, crops=240, size=48):
    """Improve the eyes on real pictures with no labels: what lasted is taken as a real
    thing (like touch was), everything else as nothing. Simulator scenes are mixed in so
    it doesn't forget them. Returns the improved eyes (a copy)."""
    rng = np.random.default_rng(seed)
    views = [channels(p)[channel] for p in pictures]
    h, w = views[0].shape
    imgs, touches = [], []
    for _ in range(crops):
        f = int(rng.integers(0, len(views)))
        y0, x0 = int(rng.integers(0, h - size)), int(rng.integers(0, w - size))
        pts = [(t[f][0] - x0, t[f][1] - y0) for t in tracks
               if f in t and x0 <= t[f][0] < x0 + size and y0 <= t[f][1] < y0 + size]
        imgs.append(views[f][y0:y0 + size, x0:x0 + size])
        touches.append(pts)
    for img, pts in replay:
        imgs.append(img)
        touches.append(pts)
    better = copy.deepcopy(eyes)
    better.learn(imgs, touches, seed=seed, epochs=8)
    return better


def follow(eyes, pictures, channel, lasting=25):
    dets = looks(eyes, pictures, channel)
    tracks = track.lasting(track.link(dets), lasting)
    return dets, tracks, track.drift(tracks, len(pictures))
