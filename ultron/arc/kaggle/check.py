"""End-to-end check of the Kaggle package on the public training split (never the
evaluation split): write a challenges file in the competition's format, run submit.py
on it, score the submission with the official rule."""

import json
import os
import sys
import tempfile

from .. import data
from . import submit


def main(limit=40):
    tasks = data.load("arc1", "training")
    ids = sorted(tasks)[:limit]
    chal = {t: {"train": [{"input": i.tolist(), "output": o.tolist()} for i, o in tasks[t]["train"]],
                "test": [{"input": i.tolist()} for i, _ in tasks[t]["test"]]} for t in ids}
    d = tempfile.mkdtemp()
    cp, sp = os.path.join(d, "challenges.json"), os.path.join(d, "submission.json")
    with open(cp, "w") as f:
        json.dump(chal, f)
    submit.main([cp, sp, "--workers", "4"])
    with open(sp) as f:
        sub = json.load(f)
    total = 0.0
    for t in ids:
        outs = [o.tolist() for _, o in tasks[t]["test"]]
        assert len(sub[t]) == len(outs)
        ok = [o in (s["attempt_1"], s["attempt_2"]) for s, o in zip(sub[t], outs)]
        total += sum(ok) / len(ok)
    print(f"submission format OK; official score on {limit} training tasks: "
          f"{100 * total / limit:.1f}%")


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 40)
