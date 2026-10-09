"""Does Ultron's own learning make unseen puzzles easier? (cross-validated)

Ultron's experience (data.experience(): ARC-AGI-1 training plus the ARC-AGI-2 training
tasks in no evaluation split) is split into two halves. Ultron practises on one half
(a long search: the "wake"), learns building blocks from what it solved there, and is
then tested on the other half, which it has never seen, with the normal budget, with and
without its blocks. Then the halves swap. Rounds repeat: in round k the wake itself uses
the blocks learned in round k-1, so learning can compound.

    python -m ultron.arc.curve [--rounds 2] [--wake 400000] [--workers 4]
"""

import argparse
import json
import os

from . import data, harness, library, solve


def _solved(result):
    return {r["task"]: r["steps"] for r in result["rows"] if r["score"] == 1.0}


def _score(tasks, ids, budget, blocks, workers):
    solve.LIBRARY[0] = blocks or None
    try:
        return harness.score_set("arc1", "training", tasks=tasks, ids=ids, budget=budget,
                                 workers=workers)
    finally:
        solve.LIBRARY[0] = None


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--rounds", type=int, default=2)
    ap.add_argument("--wake", type=int, default=400_000)
    ap.add_argument("--budget", type=int, default=solve.BUDGET)
    ap.add_argument("--workers", type=int, default=4)
    a = ap.parse_args(argv)
    tasks = data.experience()
    ids = sorted(tasks)
    halves = [ids[0::2], ids[1::2]]
    rows = []
    base = [_score(tasks, h, a.budget, None, a.workers) for h in halves]
    blocks = [None, None]
    for k in range(1, a.rounds + 1):
        for f in (0, 1):
            practice, unseen = halves[f], halves[1 - f]
            wake = _score(tasks, practice, a.wake, blocks[f], a.workers)
            blocks[f] = library.learn(_solved(wake))
            test = _score(tasks, unseen, a.budget, blocks[f], a.workers)
            row = {"round": k, "practice_half": f, "practised": len(practice),
                   "solved_in_practice": len(_solved(wake)), "blocks": len(blocks[f]),
                   "block_list": [library.describe(b) for b in blocks[f]],
                   "unseen": len(unseen),
                   "without_blocks": round(base[1 - f]["percent"], 2),
                   "with_blocks": round(test["percent"], 2),
                   "gained": sorted(set(_solved(test)) - set(_solved(base[1 - f]))),
                   "lost": sorted(set(_solved(base[1 - f])) - set(_solved(test)))}
            rows.append(row)
            print(f"round {k}, practise on half {f}: solved {row['solved_in_practice']}, "
                  f"learned {row['blocks']} blocks; unseen half: {row['without_blocks']}% "
                  f"without, {row['with_blocks']}% with", flush=True)
    os.makedirs("reports", exist_ok=True)
    with open(os.path.join("reports", "arc_learning_curve.json"), "w") as f:
        json.dump(rows, f, indent=1)
        f.write("\n")
    # the blocks learned from ALL experience are what Ultron keeps
    final = _score(tasks, ids, a.wake, library.load() or None, a.workers)
    library.save(library.learn(_solved(final)))
    print(f"kept {len(library.load())} blocks in brain/arc_library.json")


if __name__ == "__main__":
    main()
