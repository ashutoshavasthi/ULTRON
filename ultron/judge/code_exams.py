"""Exams for the code lessons (docs/STAGE_CODE_PLAN.md). Exam seeds are 70xx and are
never used while developing (development uses 75xx)."""

from ..brain.dsl import from_json, show
from ..code.reading import Reader, Unknown
from ..trainer import engc_programs as P

C1_ITEMS, C1_RIGHT, C1_PRECISION, C1_MARGIN = 200, 190, 0.99, 0.30


def _edit(a, b):
    """Words to change to turn one program into another (the nearest baseline)."""
    a, b = a.split(), b.split()
    prev = list(range(len(b) + 1))
    for i, x in enumerate(a, 1):
        cur = [i]
        for j, y in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (x != y)))
        prev = cur
    return prev[-1]


def exam_reading_engc(brain, seed=7001, items=None):
    """C1: 200 held-out expressions with 3-6 operators and numbers up to 999 (the lesson
    showed at most 2 operators and numbers up to 20). Ultron says what each will print
    without running it, or that it doesn't know."""
    if not brain.code:
        return {"lesson": 100, "passed": False, "items": [],
                "note": "lesson 100 was never taken"}
    reader = Reader(brain, brain.code)
    progs = items or P.exam_programs(seed, C1_ITEMS)
    seen = [(p, o) for p, o in reader.runs if o is not None]
    flat = {"levels": {c: (1 if reader.phrases[c]["arity"] == 1 else 0)
                       for c in reader.classes()}, "assoc": {},
            "marks": {m: "ignore" for m in reader.marks}}
    scores = {"ultron": [0, 0], "lookup": [0, 0], "nearest": [0, 0], "left to right": [0, 0]}
    answered, examples, wrong = 0, [], []
    for text, printed in progs:
        truth = printed[0]
        guess = reader.predict(text)
        answered += guess is not None
        ok = guess == truth
        scores["ultron"][0] += ok
        if guess is not None and not ok and len(wrong) < 10:
            wrong.append({"program": text, "truth": truth, "ultron": guess})
        look = next((o[0] for p, o in seen if p == text), None)
        scores["lookup"][0] += look == truth
        near = min(seen, key=lambda r: _edit(r[0], text))[1][0] if seen else None
        scores["nearest"][0] += near == truth
        try:
            ltr = reader.predict(text, **flat)
        except Unknown:
            ltr = None
        scores["left to right"][0] += ltr == truth
        for s in scores.values():
            s[1] += 1
        if len(examples) < 3:
            examples.append({"question": text, "truth": truth, "ultron": guess})
    right = scores["ultron"][0]
    precision = right / answered if answered else None
    best = max(v[0] for k, v in scores.items() if k != "ultron")
    passed = (right >= C1_RIGHT and precision is not None and precision >= C1_PRECISION
              and right - best >= C1_MARGIN * len(progs))
    item = {"name": "what 200 held-out Engc expressions print (3-6 operators, numbers to "
                    "999), worked out without running them",
            "scores": scores, "examples": examples, "tolerance": None}
    return {"lesson": 100, "passed": passed, "threshold": C1_RIGHT / C1_ITEMS,
            "items": [item], "answered": answered, "precision": precision,
            "runs": {"trainer": reader.stats.get("trainer", 0),
                     "own": reader.stats.get("own", 0)},
            "wrong": wrong,
            "meanings": {k: p["law"] for k, p in sorted(reader.phrases.items())},
            "grammar": reader.describe_grammar() if reader.levels else None}


C2_ITEMS, C2_RIGHT, C2_PRECISION, C2_MARGIN = 200, 180, 0.98, 0.30


def _straight(m, text):
    """The straight-line baseline: every line once, top to bottom, with Ultron's own
    meanings for names, values and printing, but no tests, loops or routines."""
    from ..code.statements import Program
    prog = Program(text)
    env, out = {}, []
    for toks in prog.lines:
        if not toks:
            continue
        k = m.kinds.get(toks[0])
        if not k or k["does"] not in ("set", "print", "walk"):
            continue
        words = toks[k["span"][0]:len(toks) - k["span"][1]]
        try:
            v = m.value(words, env)
        except Unknown:
            continue
        if k["does"] == "set":
            env[toks[k["name"]]] = v
        elif k["does"] == "walk":
            if isinstance(v, tuple) and v:
                env[toks[k["name"]]] = v[0]
        else:
            shown = m.show_value(v)
            if shown is not None:
                out.append(shown)
    return out


def exam_reading_statements(brain, seed=7002, items=None):
    """C2: 200 held-out programs of 5-40 lines (loops of up to 1,000 turns, blocks
    nested up to 3 deep, recursion); Ultron says everything each one prints, without
    running it, or that it doesn't know."""
    from ..code.statements import Machine
    from ..trainer import engc_statements as S
    if not brain.code or not brain.code.get("statements"):
        return {"lesson": 101, "passed": False, "items": [],
                "note": "lesson 101 was never taken"}
    reader = Reader(brain, brain.code)
    m = Machine(brain, reader, brain.code["statements"])
    progs = items or S.exam_programs(seed, C2_ITEMS)
    seen = brain.code["statements"].get("seen", [])
    scores = {"ultron": [0, 0], "lookup": [0, 0], "nearest": [0, 0], "straight line": [0, 0]}
    answered, examples, wrong = 0, [], []
    for text, printed in progs:
        guess = m.predict(text)
        answered += guess is not None
        ok = guess == printed
        scores["ultron"][0] += ok
        if guess is not None and not ok and len(wrong) < 10:
            wrong.append({"program": text, "truth": printed[:8], "ultron": guess[:8]})
        look = next((o for p, o in seen if p == text), None)
        scores["lookup"][0] += look == printed
        near = min(seen, key=lambda r: _edit(r[0], text))[1] if seen else None
        scores["nearest"][0] += near == printed
        scores["straight line"][0] += _straight(m, text) == printed
        for s in scores.values():
            s[1] += 1
        if len(examples) < 2:
            examples.append({"question": text, "truth": printed[:8], "ultron": (guess or [])[:8]})
    right = scores["ultron"][0]
    precision = right / answered if answered else None
    best = max(v[0] for k, v in scores.items() if k != "ultron")
    runs = m.stats.get("trainer", 0) + m.stats.get("own", 0)
    passed = (right >= C2_RIGHT and precision is not None and precision >= C2_PRECISION
              and right - best >= C2_MARGIN * len(progs) and runs <= 1000)
    item = {"name": "everything 200 held-out Engc programs print (5-40 lines, loops up to "
                    "1,000 turns, blocks nested up to 3 deep, recursion), worked out without "
                    "running them",
            "scores": scores, "examples": examples, "tolerance": None}
    return {"lesson": 101, "passed": passed, "threshold": C2_RIGHT / C2_ITEMS,
            "items": [item], "answered": answered, "precision": precision,
            "runs": {"trainer": m.stats.get("trainer", 0), "own": m.stats.get("own", 0)},
            "wrong": wrong, "kinds": {k: m.describe(k) for k in sorted(m.kinds)},
            "phrases": {k: show(from_json(p["law"])) for k, p in sorted(m.phrases.items())
                        if p.get("law")}}
