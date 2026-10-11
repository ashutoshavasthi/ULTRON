"""Exams for the code lessons (docs/STAGE_CODE_PLAN.md). Exam seeds are 70xx and are
never used while developing (development uses 75xx)."""

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
