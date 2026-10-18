# Ultron roadmap: the ladder

> The architecture and the rules are in [MASTER_PLAN.md](MASTER_PLAN.md). Where every
> earlier result now sits is in [LEVEL_MAP.md](LEVEL_MAP.md). The current level is planned in
> [LEVEL_0_PLAN.md](LEVEL_0_PLAN.md). Every known way to fail is in
> [FAILURE_ATLAS.md](FAILURE_ATLAS.md).

## North star

**Grow from a child's start to the most advanced intelligence we can reach:** human level
and then beyond, built on understanding instead of volume. Each level of the ladder ends at
a gate that **could fail**, checked on situations Ultron has never met, against baselines
and outside benchmarks, and by someone who did not build it. A claim is earned only when
its gate is passed.

## The ladder

| Level | Status | What it can do | Gate |
|---|---|---|---|
| **L0 Foundations** | **main line, now** | Sees things, acts with a body; things persist and fall; knows what its actions do; gets what is out of reach; notices change; remembers and consolidates its days | L0-1 to L0-11 and IntPhys 2019 ([LEVEL_0_PLAN.md](LEVEL_0_PLAN.md)) |
| **L1 Concepts & language** | planned at L0's gate | Categories, number, words from a teacher, grammar, following gaze, copying | SCAN, COGS, number tasks, word learning from few exposures |
| **L2 Causes, agents & plans** | to plan | Causal learning by intervention, modelling other agents, games with unknown rules, planning | Baby Intuitions Benchmark, ARC-AGI-3, W1–W8 |
| **L3 Knowledge & science** | results banked | School mathematics through algebra, laws from data and real films, reading simple text as claims | TIMSS and PISA released items, ARC-AGI-1 and -2, real footage V2–V6 |
| **L4 Expert reasoning** | results banked | Proofs, programming and algorithms, learning machines, reading at length | Machine-checked proofs, program-synthesis benchmarks, Code C1–C8 |
| **L5 General (human level)** | the checkpoint | Learns new fields from a few examples and some reading, explains itself | The general battery ([MASTER_PLAN.md](MASTER_PLAN.md) §5) |
| **L6 Beyond human** | the goal | Improves itself under approval; verified knowledge beyond the best experts | C9 with zero regressions; verified new results |

**"Results banked"** means work already done that belongs to that level (lessons 5–30, the
ARC work, the Code stage). It keeps passing as a regression check and is re-examined at its
own level's gate against that level's outside yardsticks. It is not claimed until then.

**Pace.** The low levels exist to give the higher ones their foundations, and take only as
long as that needs. Most of the effort goes into L3 and up.

## Where Ultron stands (2026-10-18)

- **L0:** the room, the body, the teacher, and the explorer's attention, curiosity, memory
  and sleep are built (WP1–WP3), and its failure lab runs. The gate tests are open: the
  eyes in the room, then objects and actions, then IntPhys.
- **Above L0:** strong banked results built at a desk in worlds we designed: invented
  numbers, physics laws, real films, a grammar, reading Engc and Python. Where it met the
  outside world, the gap shows: ARC-AGI-1 evaluation 12.75%, and real pendulum and bouncing
  films only partly met.

## Next steps

From [LEVEL_0_PLAN.md](LEVEL_0_PLAN.md):
1. **WP0:** obtain IntPhys 2019 and copy its scoring and published results into the plan,
   before any run.
2. **WP4:** its eyes trained from touch in the room (L0-1).
3. **WP5:** objects and actions: predicting what happens, searching for hidden things,
   means-end, noticing change (L0-2 to L0-11).
4. **WP6, the L0 gate:** every test, the owner's blind check, the ledger, merge to `main`,
   and the L1 plan written with its exit tests fixed.

**Waiting for the owner:** three proposed additions to the starting kit (a blurry wide
view, saccadic suppression, inhibition of return; see [LEDGER.md](LEDGER.md)).

## How we got here

- **2026-06-17.** PRD v1 and v2: a knowledge graph, an NLP pipeline, web checking, a
  theorem prover. Replaced in practice by grounded learning from experience; kept as
  history.
- **2026-09-30 to 10-09, Phases 1–3:** inventing numbers and laws, eyes from touch, laws from
  video, new kinds of explanation, acting by running laws backwards
  ([`judge_verdict.md`](../reports/judge_verdict.md),
  [`phase2_verdict.md`](../reports/phase2_verdict.md),
  [`phase3_verdict.md`](../reports/phase3_verdict.md),
  [`phase3_senses_verdict.md`](../reports/phase3_senses_verdict.md)).
- **2026-10-09 to 10-12, a 9-stage campaign:** the core and ARC (Stage 1: ARC ≥ 25% not
  met; [`stage1_verdict.md`](../reports/stage1_verdict.md)), real films (Stage 2), language
  L1–L3 (Stage 3), the Code stage C1–C4(a). All of it was combined in PR #12
  ([`integration.md`](../reports/integration.md)).
- **2026-10-15, first rebuild.** A review found the campaign:
  - moving on whenever a stage got hard;
  - measuring itself mostly in its own worlds;
  - grading itself;
  - starting at school level with no foundations.

  The plan was rebuilt "from a child stage", but too literally: as human ages, with a
  simulated baby (a caregiver, comfort, crying, infant-study protocols). WP1–WP3 were built
  that way.
- **2026-10-18, second rebuild (this plan).** The owner's goal is growth *from* a child's
  start *to* the most advanced intelligence, not a simulated child. Ages became capability
  levels with no ceiling, and the child-imitation parts were removed from the code. The
  useful core was kept (the room, the body, the teacher, attention, curiosity, memory and
  sleep), and the anti-drift rules stayed.

### What the earlier work taught us (still true)

- **Ultron's own law-finding applied to what it sees is what works.** Hand-written ARC
  operations hit diminishing returns. Laws learned per task took ARC-AGI-1 evaluation from
  7.75% to 12.75%.
- **Expressiveness, not search order, was ARC's bottleneck.**
- **Library learning needs material**, meaning a finer-grained base where solutions share
  pieces.
- **Precision matters as much as score.**
- **Benchmarks hide leaks:** experience must exclude held-out tasks by name.
- **Designed worlds flatter.** Hence outside yardsticks at every gate.
- **Imitating a child is not the same as growing like one** (2026-10-18). The order of
  learning is borrowed from children; the destination is not.

## Competitions

Public benchmarks are **yardsticks**, not the goal. Ultron enters a competition only when
its logged held-out score beats the best published score for that track.

## Honest difficulty

- **L0–L1** are concrete. The hard part is passing them with one general learner, not one
  module per test; the ledger will show which.
- **L2–L4** are where the bet is really tested: learning from people and text without a
  pretrained language model, and scaling the core to big programs and proofs.
- **L5–L6** are unsolved in general. Nobody, including us, can promise them.
