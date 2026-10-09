"""ARC-AGI tasks, from the public repositories pinned in manifest.json.

Discipline: everything Ultron is developed on uses the *training* split. The
*evaluation* split is only opened through `load(..., split="evaluation",
i_am_scoring=True)`, which the scoring command uses and logs.
"""

import hashlib
import json
import os
import subprocess

import numpy as np

HERE = os.path.dirname(__file__)
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
CACHE = os.environ.get("ULTRON_DATA", os.path.join(ROOT, "data"))
SETS = {"arc1": "ARC-AGI-1", "arc2": "ARC-AGI-2"}


class EvaluationLocked(Exception):
    """The evaluation split was requested by something that isn't the scoring run."""


def manifest():
    with open(os.path.join(HERE, "manifest.json")) as f:
        return json.load(f)


def _folder(name):
    return os.path.join(CACHE, "arc", name)


def fetch(name):
    """Clone the set at its pinned commit if it isn't here yet."""
    info = manifest()["sets"][name]
    folder = _folder(name)
    if not os.path.isdir(os.path.join(folder, "data")):
        os.makedirs(os.path.dirname(folder), exist_ok=True)
        subprocess.run(["git", "clone", "-q", info["url"], folder], check=True,
                       env={**os.environ, "GIT_LFS_SKIP_SMUDGE": "1"})
    head = subprocess.run(["git", "-C", folder, "rev-parse", "HEAD"], capture_output=True,
                          text=True).stdout.strip()
    if head != info["commit"]:
        subprocess.run(["git", "-C", folder, "fetch", "-q", "--depth", "1", "origin",
                        info["commit"]], check=False)
        subprocess.run(["git", "-C", folder, "checkout", "-q", info["commit"]], check=True)
    return folder


def load(name="arc1", split="training", i_am_scoring=False):
    """{task_id: {"train": [(input, output)], "test": [(input, output)]}} with numpy
    grids. Every file is checked against the manifest."""
    if split == "evaluation" and not i_am_scoring:
        raise EvaluationLocked("the evaluation split is opened only by the scoring run")
    info = manifest()["sets"][name]
    folder = fetch(name)
    tasks = {}
    for key, digest in sorted(info["files"].items()):
        s, fname = key.split("/")
        if s != split:
            continue
        path = os.path.join(folder, "data", s, fname)
        with open(path, "rb") as f:
            raw = f.read()
        if hashlib.sha256(raw).hexdigest() != digest:
            raise ValueError(f"{key}: file differs from the pinned version")
        d = json.loads(raw)
        tasks[fname[:-5]] = {
            "train": [(np.array(p["input"], dtype=np.int8), np.array(p["output"], dtype=np.int8))
                      for p in d["train"]],
            "test": [(np.array(p["input"], dtype=np.int8),
                      np.array(p["output"], dtype=np.int8) if "output" in p else None)
                     for p in d["test"]]}
    return tasks
