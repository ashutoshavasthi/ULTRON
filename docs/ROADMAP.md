# Ultron roadmap: from infant to a self-improving expert

One rule governs every phase: **a phase is not done until Ultron solves
problems it has never seen**, and a memorising baseline fails on those same
problems. That is how understanding is proven instead of claimed.

The order matters. Grounding comes first, language comes after the concepts
it names, and self-modification comes last. Self-modification is always
sandboxed and gated by the exams.

| Phase | Name | What gets added | Exit test | Status |
|---|---|---|---|---|
| 1 | **Baby Ultron** | Brain (program synthesis + invariant search, MDL, learning-progress curiosity, growing library), ToyWorld, physics sandbox, real data, Trainer, Judge | Held-out exams across 11 lessons including a noisy lab, a debts world, a cake-sharing world and a tough no-teaching final exam; memorisers fail; blank brain can't multiply; one-shot transfer; refuses what it has never experienced; trust per law; designs experiments; **invented negative numbers and fractions** | **done** (see [`reports/`](../reports/)); awaiting a blind test from someone other than its trainer |
| 2 | Inventing its own concepts, generally | Library learning (compress recurring sub-programs into new named primitives), experiment design that measurably pays off in bigger worlds | Invents several useful concepts with one general mechanism, not a mechanism per concept (Phase 1 needed a separate mechanism for negatives and for fractions; Phase 2 must invent concepts like energy as a hidden conserved quantity, powers from repeated multiplication, or averages, with one mechanism) | next |
| 3 | Real senses | Learned perception from pixels/sensors to objects. **Neural networks belong here.** A hybrid: neural "eyes", symbolic reasoning core | Rediscovers the Phase 1 laws from raw simulation video | |
| 4 | A body and goals | 3D simulation (PyBullet/MuJoCo), goals, planning with its world model, causal interventions | Solves new tasks by planning (build a taller tower than ever seen, use an object as a tool) | |
| 5 | Grounded language → English | Words by pointing, then grammar, then conversation. Only then reading, and everything read is a claim to test, not a truth (STARK fits here) | Understands new sentences about its world, detects false statements, asks questions | |
| 6 | Logic of coding | Grow its program language into a general programming language. Deep learning is trained on its *own* search traces to guide synthesis (a DreamCoder-style recognition model): the net proposes, the checker verifies | Writes correct programs for unseen specs, verified by execution; the guide measurably cuts search effort | |
| 7 | Knowing itself | Ultron studies its own Python source as an environment: predicts what its own functions will do, then runs them to check | Explains and predicts its own modules' behaviour on unseen inputs | |
| 8 | Learning Engc | The [Engc-V1](https://github.com/ashutoshavasthi/Engc-V1) interpreter becomes a world: programs are experiments, outputs are observations. Ultron learns Engc's semantics the way it learned arithmetic | Writes working Engc programs for unseen tasks | |
| 9 | The Engc twin | Ultron writes its own core in Engc and transfers its brain (the brain file is already a portable JSON format) | **Differential test:** the twin passes every held-out exam with identical answers to the Python Ultron | |
| 10 | Self-improvement | Thanos sandbox: Ultron proposes changes to its own code; each runs in isolation and is kept only if every exam still passes and learning efficiency improves; rollback always available; a human approves merges | Measurably better at *learning* (fewer experiences and less search per law) with zero regressions | |
| 11 | Scientist → expert | Cross-domain analogy, self-designed experiments, reading real literature as claims to verify; deep mastery of one domain (e.g. maths with machine-checked proofs) | Discovers a law in a held-out field; expert-level problems outside its curriculum | |

## Honest difficulty

- **Phases 1–2** are realistic in this repository.
- **Phases 3–9** are active research. The pieces exist but nobody has combined
  them well. Phase 9 is mostly engineering once phases 6–8 hold.
- **Phases 10–11** are unsolved in general. Phase 10 is also where safety
  matters most: an agent editing itself must never be able to edit its own
  exams or its sandbox.
