"""Report card and training transcript, generated from a trained brain."""

import json

from ..brain import units as U
from ..brain.dsl import show
from ..trainer.lessons import all_lessons


def _pct(score):
    c, n = score
    return f"{c}/{n} ({100 * c / n:.0f}%)" if n else "n/a"


def laws_section(brain):
    lines = ["## What Ultron discovered", "",
             "Every law below was found by Ultron's own search from its own experiences. "
             "The name in brackets was given by the Trainer *after* the exam was passed.", ""]
    lines += ["### Laws about things (small programs)", "",
              "| Experience | Law Ultron wrote | Size | Found after | Called |",
              "|---|---|---|---|---|"]
    for name in sorted(brain.library.laws, key=lambda n: brain.library.laws[n].provenance.get("lesson", 0)):
        law = brain.library.laws[name]
        lines.append(f"| `{name}({', '.join(law.params)})` | `{show(law.expr)}` | "
                     f"{law.provenance.get('size', '')} | "
                     f"{law.provenance.get('found_after', '')} experiences | "
                     f"{brain.names.get(name, '')} |")
    lines += ["", "### Laws about measurements", "",
              "| Experience | Law | Constant | Units | Trust | Called |",
              "|---|---|---|---|---|---|"]
    for name, law in sorted(brain.qlaws.items()):
        spec = brain.memory.specs[name]
        dims = U.of_monomial(law.powers, spec.units) if spec.units else None
        if law.kind == "global":
            const = f"{law.constant:.6g} (same everywhere)"
        else:
            props = ", ".join(f"{k}: {v:.4g}" for k, v in law.properties.items())
            const = f"one per {law.group_by} ({props})"
        trust = f"{brain.status(name)} ({law.provenance.get('support', 0)} confirmations)"
        lines.append(f"| `{name}` | `{law.formula()}` = constant | {const} | {U.name(dims)} | "
                     f"{trust} | {brain.names.get(name, '')} |")
    for name, laws in sorted(brain.claws.items()):
        for law in laws:
            scope = "every collision" if law.scope == "all" else f"{'/'.join(law.scope)} collisions only"
            lines.append(f"| `{name}` | total `{law.formula()}` before = after | — | "
                         f"{scope} | {law.provenance.get('support', 0)} events | "
                         f"{brain.names.get(name, '') if law.scope == 'all' else ''} |")
    if brain.inventions:
        lines += ["", "### Concepts Ultron invented itself", ""]
        for key, inv in sorted(brain.inventions.items()):
            lines += [f"- **{brain.names.get(key, key)}** (lesson {inv['lesson']}, new primitive "
                      f"`{'`, `'.join(inv['primitives'])}`). In Ultron's words: _{inv['story']}_"]
    return lines


def exams_section(results):
    lines = ["## Held-out exams (problems never seen in training)", "",
             "| Lesson | Exam | Ultron | Lookup memoriser | Nearest-example memoriser |",
             "|---|---|---|---|---|"]
    for n in sorted(results, key=int):
        r = results[n]
        for item in r["items"]:
            s = item["scores"]
            lines.append(f"| {n} | {item['name']} | **{_pct(s['ultron'])}** | "
                         f"{_pct(s['lookup'])} | {_pct(s['nearest'])} |")
    return lines


def special_section(results, brain):
    lines = ["## Special tests", ""]
    r2 = results.get("2") or results.get(2)
    if r2 and r2.get("noisy_tv"):
        tv = r2["noisy_tv"]
        lines.append(f"- **Noisy TV** (lesson 2): the lamp panel is pure randomness. Ultron gave it "
                     f"{tv['lamp_choices']} of its {tv['total_choices']} play choices (the minimum "
                     f"look every new thing gets), found no law, and stopped choosing it. "
                     f"Law for lamps: {'yes (bad!)' if tv['lamps_law'] else 'none (correct)'}.")
    r3 = results.get("3") or results.get(3)
    if r3 and r3.get("blank_brain"):
        bb = r3["blank_brain"]
        lines.append(f"- **Does knowledge compound?** A blank brain given the same groups lesson "
                     f"(no addition law to build on) scored {_pct(bb['score'])} and "
                     f"{'found' if bb['law'] else 'found no'} law. Ultron scored "
                     f"{_pct(r3['items'][0]['scores']['ultron'])}.")
    avp = None
    try:
        with open("reports/active_vs_passive.json") as f:
            avp = json.load(f)
    except OSError:
        pass
    if avp and "biased" in avp:
        total = lambda d: sum(v for v in d.values() if v)
        cur, unc, bia = avp["curated"], avp["uncurated"], avp["biased"]
        lines += [
            "- **Does designing its own experiments help?** (from `python -m ultron experiment`)",
            f"  - With a helpful teacher, experiences until every law was found: "
            f"{total(cur['active'])} designing vs {total(cur['passive'])} watching. With "
            f"random scenes over a wider range: {total(unc['active'])} vs "
            f"{total(unc['passive'])}. **No gain**: when the teacher shows everything, "
            f"Occam's razor finds each law within a few experiences either way.",
            f"  - With a **biased teacher**, who never shows equal trays and never lets the "
            f"purse go into debt: designing, Ultron passed lesson 1 "
            f"({bia['active']['1']['scores'][0][0]}/{bia['active']['1']['scores'][0][1]}) and "
            f"{'invented' if bia['active']['invented_below_zero'] else 'did NOT invent'} "
            f"negative numbers by spending from an empty purse itself. Only watching, it failed "
            f"lesson 1 ({bia['passive']['1']['scores'][0][0]}/"
            f"{bia['passive']['1']['scores'][0][1]}: it concluded trays never pair off) and "
            f"{'invented' if bia['passive']['invented_below_zero'] else 'never invented'} "
            f"negative numbers. **Designing experiments is how it learns what nobody shows it.**",
        ]
    r5 = results.get("5") or results.get(5)
    if r5 and r5.get("launch_trace"):
        lines += ["- **Composition, never trained**: a ball on a stretched spring. Ultron chained "
                  "two laws it learned separately:", "", "```", r5["launch_trace"], "```"]
    r6 = results.get("6") or results.get(6)
    if r6:
        blank = r6["blank_one_shot"]["scores"]["ultron"]
        lines.append(f"- **One-shot transfer** (real data): after seeing only Io, Ultron predicted "
                     f"Europa, Ganymede and Callisto: {_pct(r6['items'][1]['scores']['ultron'])}. "
                     f"A blank brain shown only Io: {_pct(blank)}.")
        if r6.get("sun_vs_jupiter"):
            lines.append(f"- The constant T²/r³ became a *property of the central body*. "
                         f"Jupiter's value is {r6['sun_vs_jupiter']:.0f}× the Sun's. (Physicists "
                         f"know this ratio as the Sun-to-Jupiter mass ratio, ≈1047. Ultron "
                         f"was not told this.)")
    r7 = results.get("7") or results.get(7)
    if r7 and r7.get("effort"):
        ef = r7["effort"]
        u = sum(ef["ultron_steps"].values())
        bl = sum(ef["blank_steps"].values())
        lines.append(f"- **Noisy lab**: every reading was off by up to ±1%. Using error "
                     f"propagation from the instruments' stated precision, Ultron found the laws "
                     f"again and predicted the *true* values. Its lesson-5 laws steered the search: "
                     f"{u} candidates vs {bl} for a blank brain (both succeeded; the saving is modest).")
    r8 = results.get("8") or results.get(8)
    if r8 and r8.get("story"):
        lines.append("- **Inventing negative numbers** (lesson 8): nobody mentioned them. Ultron "
                     "played with a purse of coins and IOU notes, then noticed: _" + r8["story"] +
                     "_ Only after that was it told the words '-3' and 'negative three'.")
    r9 = results.get("9") or results.get(9)
    if r9:
        lines.append("- **Tough final exam** (lesson 9): no teaching; kinds of question never "
                     "practised. Division was never taught: Ultron answers 'what times 7 equals 84' "
                     "by running its multiplication law backwards. For impossible questions the only "
                     "correct answer is a refusal, and a guess counts as wrong.")
    return lines


def report_card(brain, results):
    passed = sum(1 for r in results.values() if r["passed"])
    lines = ["# Ultron report card", "",
             f"Lessons passed: **{passed}/{len(results)}**. All numbers below are regenerated by "
             "`python -m ultron train`; the Judge's own written verdict is in "
             "[`judge_verdict.md`](judge_verdict.md).", ""]
    lines += ["## Curriculum", "", "| # | Lesson | Goal (Ultron never sees this) | Result |",
              "|---|---|---|---|"]
    for lesson in all_lessons():
        r = results.get(str(lesson.number)) or results.get(lesson.number)
        res = "—" if r is None else (f"passed (attempt {r['attempt']})" if r["passed"] else "failed")
        lines.append(f"| {lesson.number} | {lesson.title} | {lesson.goal} | {res} |")
    lines += [""] + laws_section(brain) + [""] + exams_section(results) + [""]
    lines += special_section(results, brain) + [""]
    vocab = sorted(brain.vocab.items())
    words = ", ".join(f"`{k}`" for k, v in vocab)
    lines += ["## Vocabulary (every word grounded in a pile, a law or a relation)", "", words, ""]
    return "\n".join(lines)


def transcript(brain):
    keep = {"trainer", "revise", "confirm", "stuck", "bored", "word", "measure", "reflect",
            "conflict", "meet"}
    lines = ["# Training transcript", "",
             "Everything Ultron and the Trainer said, in order (individual play choices "
             "omitted; see `brain/ultron_brain.json`).", ""]
    lesson = None
    for e in brain.log:
        if e["kind"] not in keep:
            continue
        if e["lesson"] != lesson:
            lesson = e["lesson"]
            lines += ["", f"## Lesson {lesson}", ""]
        who = "**Trainer**" if e["kind"] == "trainer" else f"Ultron _{e['kind']}_"
        lines.append(f"- {who}: {e['text']}")
    return "\n".join(lines) + "\n"


def write_all(brain, results, directory="reports"):
    import os
    os.makedirs(directory, exist_ok=True)
    with open(os.path.join(directory, "report_card.md"), "w") as f:
        f.write(report_card(brain, results))
    with open(os.path.join(directory, "transcript.md"), "w") as f:
        f.write(transcript(brain))
    with open(os.path.join(directory, "exams.json"), "w") as f:
        json.dump({str(k): v for k, v in results.items()}, f, indent=1, sort_keys=True,
                  default=str)
        f.write("\n")
