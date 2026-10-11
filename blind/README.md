# Blind tests for Ultron

The only honest proof of understanding is a test written by someone who is **not**
Ultron's trainer. Write your own questions here and score Ultron on them.

## Format

One question per line: `question | expected answer`.
Use `refuse` as the expected answer when the only right response is "I can't".
Use `~1.41421` for a number Ultron can only pin between two fractions (it passes if
the value lies inside Ultron's range).
Lines starting with `#` are comments.

```
what is 23 plus 19 | 42
what times 6 equals 54 | 9
5 minus 8 | -3
find a given F=30 m=6 | 5
find T given r=227956000000 system=Sun | 59355072
what is 7 divided 2 | 7/2
what power 2 equals 2 | ~1.41421
```

- Arithmetic answers are compared exactly as Ultron writes them (e.g. `-3`).
- Physics questions start with `find`. Numeric answers must be within 2%.
- Ultron only knows what it was taught (see `docs/ARCHITECTURE.md` and
  `reports/report_card.md`). Asking outside that should earn a refusal. A
  refusal on a fair question counts as wrong.

## Run

```bash
python -m ultron train                 # once, if brain/ultron_brain.json is missing
python -m ultron blind blind/my_test.txt
```

`example_not_blind.txt` was written by the trainer (Claude) and is **not**
blind. It only shows the format.

`independent_1.txt` and `independent_2.txt` were written from
[`SYLLABUS.md`](SYLLABUS.md) by separate agents that never saw the code, tests or
exams. First-sight scores: 55/60 and 54/60. `independent_3.txt` (Phase 3 worlds) scored
45/50 on first sight. The failures were fixed afterwards, so
those files are now regression tests. The examiners were the same underlying model
as the trainer, so a test written by a person is still the real proof. Start
from `SYLLABUS.md`.
