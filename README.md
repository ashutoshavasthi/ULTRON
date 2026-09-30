# ULTRON

A learner that understands instead of memorising. It is built like a child: a
**Brain** in an **Environment**, taught by a **Trainer** and examined by a
**Judge** on problems it has never seen.

Baby Ultron (Phase 1) starts from a few innate abilities (counting, "same",
"one more", "do this n times"). From its own experiences it discovers:
- object permanence, number, addition, subtraction, multiplication and place value;
- the words for them;
- Newton's second law, spring stiffness (a property it invented), and momentum and energy conservation;
- Kepler's third law and Boyle's law, from real measurements.

It **invented negative numbers and fractions itself**. It lived with a purse of coins and IOU
notes, noticed that its purse states form one line continuing past empty, and
decided those were places below zero. It cut cakes and weighed the pieces,
found amounts *between* its numbers, and invented fractions. It was told the
words for them only afterwards.

**Phase 2** made its inventing general:
- One shape-finding module invents **negative numbers**, **clock numbers** and
  **fractions**.
- It invents **irrational numbers** by reasoning (√2 is always squeezed between
  two fractions), then confirms them by measuring a tile's diagonal.
- It invents **energy** with any number of parts (height, speed, a spring).
- From a pattern in its own laws it **predicts powers** ten lessons before
  meeting them, and declines to guess what comes after.
- It works out roots, logarithms and negative powers it was never taught.

It then passes a tough final exam with no teaching. The exam includes:
- division, which it was never taught (it reasons backwards through its
  multiplication law);
- unseen real bodies (Ceres and Halley's Comet);
- rediscovering its physics laws with noisy instruments;
- impossible questions, which it answers with "I can't" and a reason.

Every law is a small program or formula it wrote and can explain. Every answer
comes with its reasons.

```bash
python -m ultron train                          # ~35 s; no dependencies beyond Python 3.10+
python -m ultron ask "what is 347 plus 1289?"
python -m ultron ask "find a given spring=S2 x=0.3 m=4"
python -m ultron why "3 + 2"
python -m ultron blind blind/example_not_blind.txt   # then write your own blind test
```

- [How it works](docs/ARCHITECTURE.md)
- [Report card](reports/report_card.md), the [Phase 1 verdict](reports/judge_verdict.md) and the [Phase 2 verdict](reports/phase2_verdict.md)
- [Roadmap to a self-improving expert](docs/ROADMAP.md)
- Original requirements: [PRD v1](ULTRON_PRD_V1.md), [PRD v2](ULTRON_PRD_V2.md)
