"""The learning loop that compounds (docs/PLAN.md): Ultron's language, kept and grown.

Ultron's experience (data.experience()) is split once, for good, into a **practice half**
it learns from and a **held-out half** it never learns from. Each round:

  1. wake: it writes programs (compose.py) for the practice tasks it hasn't explained yet,
     with every word it has grown so far (climbing: only what is still unexplained);
  2. sleep: its words are learned again from *every* explanation it has ever found
     (spelled out in the given steps first, so words built from words can appear, and a
     word that stopped paying is dropped);
  3. dreams and intuition: it makes puzzles from its own language (dreams.py, from
     practice-half pictures only) and learns from them and from its real solutions which
     steps a puzzle needs from what it looks like (a guide); its search tries those first
     (compose.ORDER), so it reaches the programs a puzzle needs within the same budget;
  4. test: the held-out half, with its words and intuition and (once, cached) without any.
     A held-out answer must earn its place: the explanation must also hold when any one
     example is left out (compose.earns), or it gives no answer;
  5. a bottleneck report says why the held-out tasks it misses are missed, and a 95%
     bootstrap interval says whether its gain over knowing nothing is real;
  6. the round is written to reports/learning_curve.md, and the language and everything it
     explained are kept in brain/language.json for the next round.

Learning compounds when the held-out gain grows from round to round. The main solver's
fallback on small steps (solve.predict) uses the kept words (load_words()).

    python -m ultron learn [--rounds 1] [--quick] [--workers 4]
"""

import datetime
import json
import os

from contextlib import contextmanager

import numpy as np

from . import compose, data, dreams, grow

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
STRICT = ("\n## From here on: held-out answers must earn their place\n\n"
          "Rows above answered whenever any program fit the examples, and their wrong answers "
          "rose with the right ones. From here on a held-out answer is given only when its "
          "explanation also holds with any one example left out (as the main solver does), "
          "and Ultron tries first the steps it uses most (its intuition). **Net** = right - "
          "wrong; **precision** = right / answered. Learning compounds when net and right "
          "rise while wrong stays low.\n\n"
          "| Round | When | Run | Practice explained (new) | Words | Held out without: right "
          "(wrong) | with its words and intuition | Net (without -> with) | Precision | Change "
          "in net from last round |\n|---|---|---|---|---|---|---|---|---|---|\n")


def halves(quick=False):
    tasks = data.experience()
    ids = sorted(tasks)
    practice, held = ids[0::2], ids[1::2]
    if quick:
        practice, held = practice[:60], held[:60]
    return tasks, practice, held


def load(path=STATE):
    if not os.path.exists(path):
        return {"rounds": [], "explained": {}, "words": [], "without": None,
                "strict_without": None, "order": None}
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


DREAMS = 3000           # dreams each night (full); a fifth of that in quick runs
SAMPLE = 40             # held-out misses re-searched with 4x the budget, for the report


def load_order(path=STATE):
    """Its intuition for the main solver: the guide it learned (dreams.py), else how often
    it uses each step, else None."""
    state = load(path)
    return dreams.Guide.from_json(state.get("guide")) or state.get("order") or None


def _guide(state):
    return dreams.Guide.from_json(state.get("guide")) or state.get("order")


def _outcomes(rows, ids):
    """+1 right, -1 wrong, 0 no answer, for each task."""
    return {t: (1 if rows[t]["right"] else -1) if t in rows else 0 for t in ids}


def interval(with_, without, n=2000, seed=0):
    """95% bootstrap interval of the gain in net (right - wrong), task by task."""
    ids = sorted(with_)
    diff = np.array([with_[t] - without.get(t, 0) for t in ids])
    if not len(diff):
        return (0, 0)
    rng = np.random.default_rng(seed)
    sums = [diff[rng.integers(0, len(diff), len(diff))].sum() for _ in range(n)]
    return (int(np.percentile(sums, 2.5)), int(np.percentile(sums, 97.5)))


@contextmanager
def _setting(**kw):
    """Set compose/grow switches for a run (forked workers inherit them), then restore."""
    old = {"ORDER": compose.ORDER[0], "LOO": grow.LOO[0]}
    compose.ORDER[0] = kw.get("order", old["ORDER"])
    grow.LOO[0] = kw.get("loo", old["LOO"])
    try:
        yield
    finally:
        compose.ORDER[0], grow.LOO[0] = old["ORDER"], old["LOO"]


def held_out(state, tasks, held, words, order, workers):
    """Each held-out task's outcome (+1, -1, 0), answering only when it earns it; the
    outcomes without anything grown are computed once and kept."""
    if state.get("strict_without_tasks") is None:
        with _setting(order=None, loo=True):
            base = grow.run(tasks, held, grow.BUDGET, None, workers)
        state["strict_without_tasks"] = _outcomes(base, held)
        state["strict_without"] = [len(grow._right(base)), len(grow._wrong(base))]
    with _setting(order=order, loo=True):
        test = grow.run(tasks, held, grow.BUDGET, words, workers)
    return _outcomes(test, held)


def bottleneck(tasks, outcomes, words, order, workers):
    """Why held-out tasks are missed: answered wrong; found with 4x the budget (search
    is what limits it); not found even then (beyond its language or its eyes)."""
    missed = sorted(t for t, v in outcomes.items() if v == 0)
    sample = missed[:: max(1, len(missed) // SAMPLE)][:SAMPLE]
    with _setting(order=order, loo=True):
        longer = grow.run(tasks, sample, 4 * grow.BUDGET, words, workers)
    budget = len(grow._right(longer))
    return {"wrong": sum(1 for v in outcomes.values() if v < 0), "missed": len(missed),
            "sampled": len(sample), "found with 4x budget": budget,
            "not found": len(sample) - budget}


def round_(state, tasks, practice, held, wake_budget, workers, mode, wake=True):
    """One round. With wake=False it only measures what it has now (no learning)."""
    words = state["words"]
    guide = _guide(state)
    explained = {t: grow._tuple(e) for t, e in state["explained"].items()}
    new, n_dreams = {}, 0
    if wake:
        # 1. wake: only what it hasn't explained yet, with everything it has grown
        todo = [t for t in practice if t not in explained]
        with _setting(order=guide, loo=False):
            found = grow.run(tasks, todo, wake_budget, words, workers)
        new = {t: compose.inline(grow._tuple(r["expr"]), words)
               for t, r in found.items() if r["right"]}
        explained.update(new)
        # 2. sleep: its words, learned again from everything it ever explained
        words = compose.learn_library(explained)
        # 3. dreams and the guide
        usage = compose.uses(explained.values(), words)
        n = DREAMS if mode == "full" else DREAMS // 5
        dreamt = dreams.make(tasks, practice, words, n=n, seed=len(state["rounds"]) + 1,
                             weights=usage)
        n_dreams = len(dreamt)
        names = [name for name, _, _, _ in compose.STEPS] + [w["name"] for w in words]
        real = [(tasks[t]["train"], p) for t, p in sorted(explained.items())]
        guide = dreams.Guide.fit([(d["train"], d["program"]) for d in dreamt] + 5 * real,
                                 names)
        state["order"] = usage
        state["guide"] = guide.to_json()
    # 4. test on the held-out half
    outcomes = held_out(state, tasks, held, words, guide, workers)
    right = sum(1 for v in outcomes.values() if v > 0)
    wrong = sum(1 for v in outcomes.values() if v < 0)
    net = right - wrong
    lo, hi = interval(outcomes, state["strict_without_tasks"])
    # 5. why it misses what it misses
    report = bottleneck(tasks, outcomes, words, guide, workers)
    strict = [r for r in state["rounds"] if r.get("strict")]
    last = strict[-1]["net"] if strict else None
    row = {"round": (len(state["rounds"]) + 1) if wake else f"{len(state['rounds'])}b",
           "mode": mode, "strict": True, "dreams": n_dreams,
           "when": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M"),
           "explained": len(explained), "new": len(new), "words": len(words),
           "held_out": len(held), "right": right, "wrong": wrong, "net": net,
           "change": None if last is None else net - last, "interval": [lo, hi],
           "bottleneck": report,
           "word_list": [compose.describe_step(e) for e in words]}
    state.update(words=words, explained={t: grow._plain(e) for t, e in explained.items()})
    if wake:
        state["rounds"].append(row)
    else:
        state.setdefault("rescored", []).append(row)
    return row


M1 = ("\n## From here on: dreams and a learned guide (M1 in docs/history/PLAN_M1_M2.md)\n\n"
      "Each night Ultron makes puzzles from its own language (dreams) and learns from them and "
      "from its real solutions which steps a puzzle needs (its guide). **Interval**: 95% "
      "bootstrap interval of the gain in net over knowing nothing; the gain is real when it "
      "excludes 0. **Missed**: held-out tasks with no answer; of a sample of them re-searched "
      "with 4x the budget, how many were then found (search limits it) or not (its language "
      "or eyes limit it). M1's target: practice explained >= 80 and net gain >= +15 at >= 95% "
      "precision within 3 rounds; if the gain is < +10 after 3 rounds, program search stops "
      "being the main line.\n\n"
      "| Round | When | Run | Practice explained (new) | Words | Dreams | Held out: right "
      "(wrong) | Net (without -> with) | Interval of the gain | Precision | Missed: found with "
      "4x budget / not found (of sample) |\n"
      "|---|---|---|---|---|---|---|---|---|---|---|\n")


def write_curve(row, without, path=CURVE):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    text = open(path).read() if os.path.exists(path) else HEADER
    if "From here on: held-out answers must earn their place" not in text:
        text += STRICT
    w_net = without[0] - without[1]
    answered = row["right"] + row["wrong"]
    precision = f"{100 * row['right'] / answered:.0f}%" if answered else "-"
    change = "-" if row["change"] is None else f"{row['change']:+d}"
    if "interval" not in row:
        text += (f"| {row['round']} | {row['when']} | {row['mode']} ({row['held_out']} held "
                 f"out) | {row['explained']} (+{row['new']}) | {row['words']} | {without[0]} "
                 f"({without[1]}) | {row['right']} ({row['wrong']}) | {w_net} -> {row['net']} "
                 f"| {precision} | {change} |\n")
    else:
        if "dreams and a learned guide (M1" not in text:
            text += M1
        b = row["bottleneck"]
        lo, hi = row["interval"]
        text += (f"| {row['round']} | {row['when']} | {row['mode']} ({row['held_out']} held "
                 f"out) | {row['explained']} (+{row['new']}) | {row['words']} | {row['dreams']} "
                 f"| {row['right']} ({row['wrong']}) | {w_net} -> {row['net']} | {lo:+d} to "
                 f"{hi:+d} | {precision} | {b['missed']}: {b['found with 4x budget']} / "
                 f"{b['not found']} (of {b['sampled']}) |\n")
    with open(path, "w") as f:
        f.write(text)


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
        write_curve(row, state["strict_without"])
        rows.append(row)
    return rows, state


def rescore(quick=False, workers=4, state_path=STATE):
    """Measure what it has now under the held-out rule, without learning (a 'b' row)."""
    tasks, practice, held = halves(quick)
    state = load(state_path)
    if state.get("order") is None and state["explained"]:
        state["order"] = compose.uses([grow._tuple(e) for e in state["explained"].values()],
                                      state["words"])
    row = round_(state, tasks, practice, held, 0, workers, "quick" if quick else "full",
                 wake=False)
    save(state, state_path)
    write_curve(row, state["strict_without"])
    return row, state
