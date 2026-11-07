"""The learning loop that compounds (docs/PLAN.md): Ultron's language, kept and grown.

Ultron's experience (data.experience()) is split once, for good, into a **practice half**
it learns from and a **held-out half** it never learns from. Each round:

  1. wake: it writes programs (compose.py) for the practice tasks it hasn't explained yet,
     with every word it has grown so far (climbing: only what is still unexplained);
  2. sleep: its words are learned again from *every* explanation it has ever found
     (spelled out in the given steps first, so words built from words can appear, and a
     word that stopped paying is dropped);
  3. intuition: it counts how often each step and word appears in everything it explained,
     and tries the most used first (compose.ORDER), so its search reaches the programs it
     tends to write within the same budget;
  4. test: the held-out half, with its words and intuition and (once, cached) without any.
     A held-out answer must earn its place: the explanation must also hold when any one
     example is left out (compose.earns), or it gives no answer;
  5. the round is written to reports/learning_curve.md, and the language and everything it
     explained are kept in brain/language.json for the next round.

Learning compounds when the held-out gain grows from round to round. The main solver's
fallback on small steps (solve.predict) uses the kept words (load_words()).

    python -m ultron learn [--rounds 1] [--quick] [--workers 4]
"""

import datetime
import json
import os

from contextlib import contextmanager

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


def load_order(path=STATE):
    """Its intuition: how often it uses each step (for the main solver), or None."""
    return load(path).get("order") or None


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
    """Right and wrong on the held-out half, answering only when it earns it; the score
    without anything grown is computed once and kept."""
    if state.get("strict_without") is None:
        with _setting(order=None, loo=True):
            base = grow.run(tasks, held, grow.BUDGET, None, workers)
        state["strict_without"] = [len(grow._right(base)), len(grow._wrong(base))]
    with _setting(order=order, loo=True):
        test = grow.run(tasks, held, grow.BUDGET, words, workers)
    return len(grow._right(test)), len(grow._wrong(test))


def round_(state, tasks, practice, held, wake_budget, workers, mode, wake=True):
    """One round. With wake=False it only measures what it has now (no learning)."""
    words = state["words"]
    order = state.get("order")
    explained = {t: grow._tuple(e) for t, e in state["explained"].items()}
    new = {}
    if wake:
        # 1. wake: only what it hasn't explained yet, with everything it has grown
        todo = [t for t in practice if t not in explained]
        with _setting(order=order, loo=False):
            found = grow.run(tasks, todo, wake_budget, words, workers)
        new = {t: compose.inline(grow._tuple(r["expr"]), words)
               for t, r in found.items() if r["right"]}
        explained.update(new)
        # 2. sleep: its words, learned again from everything it ever explained
        words = compose.learn_library(explained)
        # 3. intuition: how often it uses each step and word
        order = compose.uses(explained.values(), words)
    # 4. test on the held-out half
    right, wrong = held_out(state, tasks, held, words, order, workers)
    net = right - wrong
    strict = [r for r in state["rounds"] if r.get("strict")]
    last = strict[-1]["net"] if strict else None
    row = {"round": (len(state["rounds"]) + 1) if wake else f"{len(state['rounds'])}b",
           "mode": mode, "strict": True,
           "when": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M"),
           "explained": len(explained), "new": len(new), "words": len(words),
           "held_out": len(held), "right": right, "wrong": wrong, "net": net,
           "change": None if last is None else net - last,
           "word_list": [compose.describe_step(e) for e in words]}
    state.update(words=words, order=order,
                 explained={t: grow._plain(e) for t, e in explained.items()})
    if wake:
        state["rounds"].append(row)
    else:
        state.setdefault("rescored", []).append(row)
    return row


def write_curve(row, without, path=CURVE):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    text = open(path).read() if os.path.exists(path) else HEADER
    if "From here on: held-out answers must earn their place" not in text:
        text += STRICT
    w_net = without[0] - without[1]
    answered = row["right"] + row["wrong"]
    precision = f"{100 * row['right'] / answered:.0f}%" if answered else "-"
    change = "-" if row["change"] is None else f"{row['change']:+d}"
    text += (f"| {row['round']} | {row['when']} | {row['mode']} ({row['held_out']} held out) "
             f"| {row['explained']} (+{row['new']}) | {row['words']} | {without[0]} ({without[1]}) "
             f"| {row['right']} ({row['wrong']}) | {w_net} -> {row['net']} | {precision} "
             f"| {change} |\n")
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
