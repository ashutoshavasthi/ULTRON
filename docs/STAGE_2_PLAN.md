# Stage 2: the real world through its eyes

**Mission.** Ultron has seen one real film, and its eyes don't generalise. Stage 2 gives
it eyes that hold up in hard conditions, then has it rediscover physics from **real
footage**.

## Exit test (fixed now, from `MASTER_PLAN.md`)

| # | Criterion |
|---|---|
| V1 | **Eyes:** every gating row of the failure lab's *eyes* experiment ≥ 23/25 trays counted right, with no regressions elsewhere in the lab |
| V2 | **Diffusion** from the real microscope film (lesson 26): Ultron's D agrees with the scientists' own tool within measured error |
| V3 | **g** from real footage of falling, within measured error |
| V4 | **Pendulum periods** from real footage, within measured error (and the √length law) |
| V5 | **Restitution** from real footage of bouncing, within measured error |
| V6 | **Detection on par with lab tools** on the same real footage (positions, counts) |

Everything Stage 1 passed must still pass: the curriculum, every exam, the failure lab
and the blind tests. A retrain must stay byte for byte identical.

## Where the eyes stand (failure lab, 2026-10-11)

| Condition | Trays counted right |
|---|---|
| normal (8% noise) | 25/25 |
| 16% noise | 1/25 |
| 32% noise | 0/25 |
| big things (radius 4–6) | 0/25 |
| faint things (30% brightness) | 2/25 |
| touching (gap = diameter) | 19/25 |
| overlapping | 14/25 (a physical limit, reported only) |

## Status

| # | Status |
|---|---|
| V1 | ✅ **met** (2026-10-11): every gating eyes row 24–25/25 in the failure lab (was 25, 1, 0, 0, 2, 19); on a second set of unseen trays 24–25/25. No regressions elsewhere in the lab; all 28 lessons pass on the first attempt; a retrain is byte-identical; 109 tests pass |
| V2–V6 | open |

How V1 was met (`senses/eyes.py`, `senses/world.py`):
- **Looking longer:** when a still scene is noisier than usual (its own noise measure, as
  the retina's), pictures are lined up against shake and averaged until as clean as
  usual. 16% noise: 1 → 25; 32%: 0 → 25.
- **Adapting to the light:** the background is moved back to where the eyes are used to
  it, but only when it is noticeably off. In a dim scene, once looking long enough makes
  something really stand out, the contrast is turned up to how things look in its clear
  views. Faint: 2 → 25.
- **Stepping back:** the picture shrunk 2× and 3×, kept only when its eyes respond
  clearly more strongly there. Big things: 0 → 25.
- **Broader handling:** lesson 19 handles things in varied spacing, size, light and
  camera noise. Touching: 19 → 24.

Two measured pitfalls, fixed:
- recentring the background on every picture dimmed small crowded things;
- "usual brightness" averaged over dim scenes was too low.

## Work packages

### WP1: eyes that generalise (V1)

Each change is general, plausible for an animal, and measured against every row. It is
kept only if no row regresses and the curriculum still passes.

1. **Look longer at a still scene.** Average several frames, aligned for camera shake,
   until the picture's own noise, which Ultron measures itself (as the retina does), is
   down to what its eyes grew up with. This targets the 16% and 32% noise rows.
2. **Adapt to the light.** Choose "how strong must a spot be" relative to the picture's
   own noise, not as one fixed number. This targets the faint row.
3. **Step back.** Look at the picture shrunk 2× and 3× as well, and keep, for each thing,
   the scale where it looks most like the things the eyes learned. This targets the big
   row.
4. **Broader handling.** In lesson 19, touch also covers things that are close
   together, faint, larger, and in dimmer and noisier light, as a child handles things in
   all conditions. This targets the touching row and makes the eyes more robust overall.

### WP2: lesson 26, the real microscope film (V2)

Finish the work in progress end to end: real particles through the retina, tracks,
mean squared displacement, then D compared with the scientists' tool on the same film.

### WP3: more real footage (V3–V6)

Real videos of falling, swinging and bouncing. The network policy decides the sources:
Wikimedia, YouTube and archive.org are blocked here. The order of preference:
1. footage hosted on GitHub or PyPI;
2. the environment's network settings opened for those sites (owner's choice);
3. failing both, footage the owner provides.

Each video is measured with Ultron's own eyes and compared with a lab tool (for
example, a standard blob tracker) on the same frames.

## Order

WP1 first: the roadmap says *eyes first*. Then WP2, then WP3.
