"""The learning loop that compounds (docs/PLAN.md): Ultron's language, kept and grown.

Ultron's experience (data.experience()) is split once, for good, into a **practice half**
it learns from and a **held-out half** it never learns from. Each round:

  1. wake: it writes programs (compose.py) for the practice tasks it hasn't explained yet,
     with every word it has grown so far (climbing: only what is still unexplained);
  2. sleep: its words are learned again from *every* explanation it has ever found
     (spelled out in the given steps first, so words built from words can appear, and a
     word that stopped paying is dropped);
  3. test: the held-out half, with its words and (once, cached) without any;
  4. the round is written to reports/learning_curve.md, and the language and everything it
     explained are kept in brain/language.json for the next round.

Learning compounds when the held-out gain grows from round to round. The main solver's
fallback on small steps (solve.predict) uses the kept words (load_words()).

    python -m ultron learn [--rounds 1] [--quick] [--workers 4]
"""

import datetime
import json
import os

from . import compose, data, grow

STATE = os.path.join(data.ROOT, "brain", "language.json")
CURVE = os.path.join(data.ROOT, "reports", "learning_curve.md")
HEADER = ("# The learning curve\n\n"
          "One row per round of `python -m ultron learn` (docs/PLAN.md). Practice: tasks "
          "explained so far (new this round). Held out: tasks it never learns from, right "
          "(wrong), with its words; without any words it gets the number in the 'without' "
          "column. Learning compounds when the gain grows from round to round.\n\n"
          "| Round | When | Run | Practice explained (new) | Words | Held out: without "
          "| with its words | Gain | Change from last round |\n"
          "|---|---|---|---|---|---|---|---|---|\n")


def halves(quick=False):
    tasks = data.experience()
    ids = sorted(tasks)
    practice, held = ids[0::2], ids[1::2]
    if quick:
        practice, held = practice[:60], held[:60]
    return tasks, practice, held


def load(path=STATE):
    if not os.path.exists(path):
        return {"rounds": [], "explained": {}, "words": [], "without": None}
    with open(path) as f:
        s = json.load(f)
    s["words"] = grow.from_json(s["words"])
    return s


def save(state, path=STATE):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    out = dict(state, words=grow.to_json(state["words"]))
    with open(path, "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)
        f.write("\n")


def load_words(path=STATE):
    """The words Ultron has grown (for the main solver), or None."""
    return load(path)["words"] or None


def round_(state, tasks, practice, held, wake_budget, workers, mode):
    words = state["words"]
    explained = {t: grow._tuple(e) for t, e in state["explained"].items()}
    # 1. wake: only what it hasn't explained yet, with everything it has grown
    todo = [t for t in practice if t not in explained]
    wake = grow.run(tasks, todo, wake_budget, words, workers)
    new = {t: compose.inline(grow._tuple(r["expr"]), words)
           for t, r in wake.items() if r["right"]}
    explained.update(new)
    # 2. sleep: its words, learned again from everything it ever explained
    words = compose.learn_library(explained)
    # 3. test on the held-out half
    if state["without"] is None:
        base = grow.run(tasks, held, grow.BUDGET, None, workers)
        state["without"] = [len(grow._right(base)), len(grow._wrong(base))]
    test = grow.run(tasks, held, grow.BUDGET, words, workers)
    right, wrong = len(grow._right(test)), len(grow._wrong(test))
    gain = right - state["without"][0]
    last = state["rounds"][-1]["gain"] if state["rounds"] else 0
    row = {"round": len(state["rounds"]) + 1, "mode": mode,
           "when": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M"),
           "explained": len(explained), "new": len(new), "words": len(words),
           "held_out": len(held), "right": right, "wrong": wrong, "gain": gain,
           "change": gain - last, "word_list": [compose.describe_step(e) for e in words]}
    state.update(words=words, explained={t: grow._plain(e) for t, e in explained.items()})
    state["rounds"].append(row)
    return row


def write_curve(row, without, path=CURVE):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if not os.path.exists(path):
        with open(path, "w") as f:
            f.write(HEADER)
    with open(path, "a") as f:
        f.write(f"| {row['round']} | {row['when']} | {row['mode']} ({row['held_out']} held out) "
                f"| {row['explained']} (+{row['new']}) | {row['words']} | {without[0]} "
                f"({without[1]}) | {row['right']} ({row['wrong']}) | {row['gain']:+d} "
                f"| {row['change']:+d} |\n")


def run(rounds=1, quick=False, workers=4, state_path=STATE):
    tasks, practice, held = halves(quick)
    mode = "quick" if quick else "full"
    state = load(state_path)
    if state["rounds"] and state["rounds"][0]["mode"] != mode:
        raise ValueError(f"{state_path} holds {state['rounds'][0]['mode']} rounds; "
                         "use another --state for a different mode")
    rows = []
    for _ in range(rounds):
        row = round_(state, tasks, practice, held, 50_000 if quick else 200_000, workers, mode)
        save(state, state_path)
        write_curve(row, state["without"])
        rows.append(row)
    return rows, state
