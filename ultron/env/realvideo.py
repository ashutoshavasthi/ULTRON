"""Real video from the world: a laboratory microscope film, fetched from the internet.

The film is trackpy-examples' `bulk_water` sequence: 1-micron latex spheres diffusing
in water, 300 frames, recorded by scientists (BSD-3-Clause or CC BY 3.0, trackpy-examples
contributors, https://github.com/soft-matter/trackpy-examples). It is fetched from a
pinned commit and every frame's SHA-256 is checked against the manifest committed here,
so every run sees exactly the same pixels. Frames are cached under data/real/ (not in
git). Ultron gets the pictures and the film's label (24 frames per second, 2.85 pixels
per micron), the way it was allowed to read its own camera's frame rate. Nothing else:
no positions, no tracks, no answers.
"""

import hashlib
import json
import os
import urllib.request

HERE = os.path.dirname(__file__)
MANIFEST = os.path.join(HERE, "data", "real", "bulk_water.json")
REFERENCE = os.path.join(HERE, "data", "real", "bulk_water_trackpy.json")
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
CACHE = os.environ.get("ULTRON_DATA", os.path.join(ROOT, "data"))


class Unavailable(Exception):
    """The film couldn't be fetched (no network) and isn't cached."""


def manifest():
    with open(MANIFEST) as f:
        return json.load(f)


def _fetch(man, name, path):
    url = (f"https://raw.githubusercontent.com/soft-matter/trackpy-examples/"
           f"{man['commit']}/{man['path']}/{name}")
    try:
        with urllib.request.urlopen(url, timeout=60) as r:
            data = r.read()
    except OSError as e:
        raise Unavailable(f"can't fetch {url}: {e}") from e
    if hashlib.sha256(data).hexdigest() != man["files"][name]:
        raise Unavailable(f"{name}: downloaded bytes don't match the manifest")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(data)


def frames():
    """The film as a list of RGB pixel arrays, in order."""
    import numpy as np
    from PIL import Image
    man = manifest()
    folder = os.path.join(CACHE, "real", "bulk_water")
    out = []
    for name in sorted(man["files"]):
        path = os.path.join(folder, name)
        ok = os.path.exists(path)
        if ok:
            with open(path, "rb") as f:
                ok = hashlib.sha256(f.read()).hexdigest() == man["files"][name]
        if not ok:
            _fetch(man, name, path)
        out.append(np.array(Image.open(path).convert("RGB")))
    return out


def label():
    """What is written on the film: its frame rate and its scale."""
    man = manifest()
    return {"fps": man["fps"], "pixels_per_micron": man["pixels_per_micron"]}


def reference():
    """The Judge's reference: trackpy, the scientists' own tool, run on the same film
    (see ultron/judge/real_reference.py). Ultron never sees this."""
    with open(REFERENCE) as f:
        return json.load(f)
