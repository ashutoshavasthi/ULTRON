"""Real lab films of falling, swinging and bouncing, fetched from the internet.

Most films are the Tracker project's (Douglas Brown and colleagues, Open Source Physics;
GPL-3.0; https://github.com/OpenSourcePhysics/resources and .../tracker-website); the
bouncing balls are from Singapore's Open Source Physics collection (iwant2study.org,
Loo Kang Wee and colleagues; CC BY-SA 4.0). They are real classroom-lab footage, made for
students to measure physics from. Each file is fetched from a pinned commit or address
and its SHA-256 checked against the manifest committed here; the decoded pictures are checked too, so every run sees exactly the same pixels.
Nothing is committed to this repository except the manifest. Files are cached under
data/real/footage/ (not in git).

Decoding needs ffmpeg (the system's, or the one in the imageio-ffmpeg package). Only the
brightness of each picture is used (the Y plane of the video, copied exactly), so any
standard decoder gives the same pixels.

Ultron gets the pictures and what is written on the film: the frame rate in the file,
whether the camera took half-pictures (interlaced video), and the scale written on the
metre stick in view. Nothing else: no positions, no tracks, no answers.
"""

import hashlib
import io
import json
import os
import shutil
import subprocess
import urllib.request
import zipfile

HERE = os.path.dirname(__file__)
MANIFEST = os.path.join(HERE, "data", "real", "footage.json")
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
CACHE = os.environ.get("ULTRON_DATA", os.path.join(ROOT, "data"))


class Unavailable(Exception):
    """A film couldn't be fetched or decoded (no network, no ffmpeg) and isn't cached."""


def manifest():
    with open(MANIFEST) as f:
        return json.load(f)


def _archive(man, name):
    src = man["archives"][name]
    path = os.path.join(CACHE, "real", "footage", name)
    if os.path.exists(path):
        with open(path, "rb") as f:
            data = f.read()
        if hashlib.sha256(data).hexdigest() == src["sha256"]:
            return data
    url = src.get("url") or \
        f"https://raw.githubusercontent.com/{src['repo']}/{src['commit']}/{src['path']}"
    try:
        req = urllib.request.Request(url, headers={     # Wikimedia asks every client
            "User-Agent": "Ultron/0.1 (https://github.com/ashutoshavasthi/ULTRON)"})
        with urllib.request.urlopen(req, timeout=120) as r:
            data = r.read()
    except OSError as e:
        raise Unavailable(f"can't fetch {url}: {e}") from e
    if hashlib.sha256(data).hexdigest() != src["sha256"]:
        raise Unavailable(f"{name}: downloaded bytes don't match the manifest")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(data)
    return data


def _ffmpeg():
    exe = shutil.which("ffmpeg")
    if exe:
        return exe
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception as e:            # not installed, or no binary for this machine
        raise Unavailable("no ffmpeg to decode the film (install ffmpeg or imageio-ffmpeg)"
                          ) from e


def member(film_name, kind="video"):
    """The raw bytes of a film's video (or its Tracker file, kind="tracker")."""
    man = manifest()
    film = man["films"][film_name]
    data = _archive(man, film["archive"])
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        return z.read(film[kind])


def frames(film_name):
    """The film as a list of brightness pictures (2-D uint8 arrays), in order: the whole
    film, or the stretch and part of the picture the manifest names (where a teaching
    film also shows a lesson, the Trainer shows only the experiment)."""
    import numpy as np
    film = manifest()["films"][film_name]
    path = os.path.join(CACHE, "real", "footage", film_name + ".mp4")
    if not os.path.exists(path):
        data = member(film_name) if "archive" in film else _archive(manifest(), film["file"])
        with open(path, "wb") as f:
            f.write(data)
    w, h = film["size"]
    cut = []                                  # the part of the film the Trainer shows
    if "start_s" in film:
        cut = ["-ss", str(film["start_s"]), "-t", str(film["seconds"])]
    view = []
    if "crop" in film:
        x, y, w, h = film["crop"]
        view = ["-vf", f"crop={w}:{h}:{x}:{y}"]
    run = subprocess.run([_ffmpeg(), "-v", "error", *cut, "-i", path, *view, "-f",
                          "rawvideo", "-pix_fmt", "gray", "-"], capture_output=True)
    if run.returncode != 0:
        raise Unavailable(f"ffmpeg couldn't decode {film_name}: {run.stderr[:200]!r}")
    raw = run.stdout
    if hashlib.sha256(raw).hexdigest() != film["pixels_sha256"]:
        raise Unavailable(f"{film_name}: decoded pixels don't match the manifest")
    return list(np.frombuffer(raw, np.uint8).reshape(-1, h, w))


def label(film_name):
    """What is written on the film: frame rate, interlacing, and the stick's scale."""
    film = manifest()["films"][film_name]
    keys = ("fps", "interlaced", "pixels_per_metre", "scale_from", "length_m")
    return {k: film[k] for k in keys if k in film}


def tracker_file(film_name):
    """The lab's own analysis of the film in Tracker (XML), for the Judge only: Ultron
    never sees it."""
    return member(film_name, "tracker").decode("utf-8")
