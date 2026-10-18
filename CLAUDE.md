# ULTRON: notes for anyone working on it (including Claude)

## The goal
Grow from a child's start to the most advanced intelligence we can reach: human level, then
beyond. Ultron climbs a ladder of capability levels L0–L6 (foundations; concepts and
language; causes, agents and plans; knowledge and science; expert reasoning; general; beyond
human), each ending at a gate of outside benchmarks.
- **It is not a simulated child.** The order of learning is borrowed from children; the
  destination is not, and human level is a checkpoint, not a ceiling.
- **Where things are:** the spec is [docs/MASTER_PLAN.md](docs/MASTER_PLAN.md), the plan
  is [docs/ROADMAP.md](docs/ROADMAP.md), and where earlier work belongs is in
  [docs/LEVEL_MAP.md](docs/LEVEL_MAP.md). The PRDs are historical.

## Current level
**L0, foundations** ([docs/LEVEL_0_PLAN.md](docs/LEVEL_0_PLAN.md)): the room, the body, the
teacher, attention, curiosity, memory and sleep are built. The gate tests L0-1 to L0-11 and
IntPhys are open.

## Rules (from MASTER_PLAN §4; they never bend)
1. Only the current level is the main line. Work on a higher level is a labelled prototype
   and is never claimed as met.
2. Every gate needs an outside yardstick **and** the owner's blind check. A test written by
   Claude is never the only check.
3. L0 builds its foundations in the room; from L1 any world may be used.
4. Data and compute per capability are measured against fixed baselines.
5. The starting kit is fixed. Adding to it needs the owner's approval.
6. Keep the ledger of hand-built mechanisms for each level.
7. Merge to `main` at every gate.
8. Exit tests are fixed before the work. Never change a pass rule after seeing a result;
   if a protocol changes, report both results.
9. Human level is a checkpoint, not a ceiling; no gate asks Ultron to act like a human of
   some age.
10. No pretrained models and no language model inside Ultron.
11. Claim only what a passed test shows. Report failures as plainly as successes.

## Working on the code
- `python -m ultron train` retrains everything (about 20 minutes) and must be
  byte-identical across runs. `python -m pytest` runs the tests. `python -m ultron stress`
  runs the failure lab. `python -m ultron room` lives a day in the room (L0) as the explorer,
  and writes `reports/room.md` and `reports/room.png`.
- Layout:
  - `ultron/brain` (the explanation engine, memory, curiosity, language);
  - `ultron/senses` (camera, retina, eyes, tracking);
  - `ultron/env` (worlds);
  - `ultron/room` (L0: the room, the body, the teacher, days and nights);
  - `ultron/trainer` (lessons);
  - `ultron/judge` (exams, failure lab);
  - `ultron/arc`;
  - `reports/`;
  - `docs/`.
- Every lesson 0–33 must keep passing on the first attempt as a regression check.
- The teacher's script (`ultron/room/teacher.py`) is hashed in
  `docs/LEVEL_0_PLAN.md`. Changing it means recording the new hash in the plan, as a visible
  change.

## Open branches (2026-10-18)
- `claude/integrate-stages-5hnowy` (PR #12): all the earlier work combined (lessons 0–33).
- `claude/stage-coding-engc-1j7rdc`: Code stage C1–C4(a), not yet in PR #12. Banked for
  L4.
- `claude/dreamy-darwin-neiflp`: the ladder plan and Level 0 work, on top of PR #12 (draft PR #13).
