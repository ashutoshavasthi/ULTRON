# ULTRON: notes for anyone working on it (including Claude)

## The goal
Human-like general intelligence, grown the way a child grows. Ultron is raised from a
newborn through Ages 0–6 (newborn, infant, toddler, preschool, school child, adolescent,
adult). Each age ends at a gate of real child-development milestones. The spec is
[docs/MASTER_PLAN.md](docs/MASTER_PLAN.md), the plan is
[docs/ROADMAP.md](docs/ROADMAP.md), and where earlier work belongs is in
[docs/DEVELOPMENT_MAP.md](docs/DEVELOPMENT_MAP.md). The PRDs are historical.

## Current age
**Age 0, newborn** ([docs/AGE_0_1_PLAN.md](docs/AGE_0_1_PLAN.md)): the nursery, the body,
the caregiver, eyes, habituation, memory and sleep. Age 1's exit tests are already fixed in
the same plan.

## Rules (from MASTER_PLAN §4; they never bend)
1. Only the current age is the main line. Work on a later age is a labelled prototype and
   is never claimed as met.
2. Every gate needs an outside yardstick with human data **and** the owner's blind check.
   A test written by Claude is never the only check.
3. Ages 0–3 happen in the nursery, through the body and the caregiver. Desk lessons are
   allowed from Age 4.
4. Experience is counted in simulated days, next to children's.
5. The innate endowment is fixed. Adding to it needs the owner's approval.
6. Keep the ledger of hand-built mechanisms for each age.
7. Merge to `main` at every gate.
8. Exit tests are fixed before the work. Never change a pass rule after seeing a result;
   if a protocol changes, report both results.
9. No pretrained models and no language model inside Ultron.
10. Claim only what a passed test shows. Report failures as plainly as successes.

## Working on the code
- `python -m ultron train` retrains everything (about 20 minutes) and must be
  byte-identical across runs. `python -m pytest` runs the tests. `python -m ultron stress`
  runs the failure lab.
- Layout:
  - `ultron/brain` (the explanation engine, memory, curiosity, language);
  - `ultron/senses` (camera, retina, eyes, tracking);
  - `ultron/env` (worlds);
  - `ultron/trainer` (lessons);
  - `ultron/judge` (exams, failure lab);
  - `ultron/arc`;
  - `reports/`;
  - `docs/`.
- Every lesson 0–33 must keep passing on the first attempt as a regression check.

## Open branches (2026-10-15)
- `claude/integrate-stages-5hnowy` (PR #12): all the earlier work combined (lessons 0–33).
- `claude/stage-coding-engc-1j7rdc`: Code stage C1–C4(a), not yet in PR #12. Banked for
  Ages 4–5.
- `claude/dreamy-darwin-neiflp`: this rebuilt plan, on top of PR #12.
