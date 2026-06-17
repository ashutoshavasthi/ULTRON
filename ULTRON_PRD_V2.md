# Ultron — Revised PRD v2.0
**Version:** 2.0  
**Status:** Active  
**Date:** June 2026  
**Supersedes:** PRD v1.0  
**Goal:** Build Ultron into an ASI-capable system that builds mathematical and scientific logic from first principles, generalises learned logic to new situations, and understands rather than memorises.

---

## 1. Vision

Ultron must reason the way a child learns mathematics and science — not by memorising formulas but by building axioms from primitives, deriving rules through pattern recognition, and applying those rules to completely new situations through generalisation and analogy.

The system starts from zero: it learns what a number is before it learns arithmetic. It learns what equality means before it learns equations. It learns what force means before it learns Newton's laws. Every piece of knowledge is derived, not inserted.

The long-term target: a system that can encounter a physics problem it has never seen, recognise that it resembles known causal structures, apply the correct logical rules, and derive the answer — without being told the formula.

---

## 2. Core Design Philosophy

| Principle | Description |
|---|---|
| Primitives first | Every domain starts from irreducible axioms. Numbers before arithmetic. Sets before algebra. Forces before mechanics. |
| Derivation over memorisation | Rules are derived from axioms + observations, not stored as lookup tables. |
| Prediction before observation | Ultron predicts outcomes before seeing them. Learning happens from the prediction-reality gap. |
| Generalisation as the primary goal | The test of understanding is not recall — it is correctly solving unseen problems using acquired logic. |
| Analogical transfer | Logic learned in one domain (e.g., arithmetic) is tested for applicability in another (e.g., chemistry ratios). |
| Contradiction is signal, not error | When a prediction fails or a contradiction is detected, that is the most valuable learning signal. |
| Causal world model | Every relationship is a directed causal edge with weight, not a flat association. |
| Self-supervised curriculum | Curiosity signal drives what is learned next. No external teacher required after seeding. |

---

## 3. Full Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         ULTRON CORE LOOP                            │
│                                                                     │
│  [Seed Layer]                                                       │
│       └── Mathematical Primitives (number, set, operation, equality)│
│       └── Scientific Primitives (entity, force, energy, state,      │
│                                  change, causality, space, time)    │
│       └── Linguistic Primitives (token, morpheme, word, relation)   │
│                                                                     │
│  [Perception & Language Stack]                                      │
│       └── Tokeniser → Morphological Analyser → POS Tagger           │
│       └── Lexical Sense Disambiguator (WordNet)                     │
│       └── Connector/Conjunction Handler (logical operators)         │
│       └── Dependency Parser → Semantic Role Labeller (SRL)          │
│       └── Logical Form Builder → SemanticFrame                      │
│                                                                     │
│  [Domain Parsing Layer]                                             │
│       └── Math Parser (equations, inequalities, operations, proofs) │
│       └── Science Parser (laws, experiments, observations, units)   │
│       └── Logic Parser (propositions, rules, implications, axioms)  │
│                                                                     │
│  [STARK — Knowledge Extraction]                                     │
│       └── Ensemble extractor (LLM adapter > spaCy > regex)         │
│       └── Multi-source verifier (Wikipedia, Wikidata, DuckDuckGo)   │
│       └── Claim credibility scorer                                  │
│                                                                     │
│  [Knowledge Representation]                                         │
│       └── Knowledge Graph (concept nodes, typed causal edges)       │
│       └── LogicTree (indexed theorems and axioms)                   │
│       └── Domain Ontologies (Math, Physics, Chemistry, Bio, Logic)  │
│       └── Rule Store (derived rules with proof lineage)             │
│                                                                     │
│  [Reasoning Engines]                                                │
│       └── FOL Theorem Prover (modus ponens chains, resolution)      │
│       └── Mathematical Reasoner (axiom derivation, proof steps)     │
│       └── Scientific Reasoner (hypothesis formation, law testing)   │
│       └── Causal Engine (Pearl do-calculus, counterfactuals)        │
│       └── Analogical Engine (structural mapping across domains)     │
│       └── Hypothesis Engine (mediator inference, generalisation)    │
│                                                                     │
│  [Learning Engines]                                                 │
│       └── Prediction Engine (predict before observe)                │
│       └── Prediction Error Tracker (per domain, per concept)        │
│       └── Curiosity Signal (highest-error topic first)              │
│       └── Generalisation Tester (probe unseen situations)           │
│       └── Analogy Mapper (apply logic across domain boundaries)     │
│                                                                     │
│  [Belief Management]                                                │
│       └── Belief Revision Engine (contradiction, scoring, status)   │
│       └── Temporal Reasoning (time-tagged beliefs, priority)        │
│       └── Belief History (versioned per cycle, rollback ready)      │
│                                                                     │
│  [Metacognition]                                                    │
│       └── Captain (cycle evaluator, strategy corrector, gating)     │
│       └── Thanos (RSI sandbox, experiment logger, rollback gate)    │
│       └── Goal System (curiosity-driven curriculum, benchmarks)     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 4. The Mathematical Logic Stack (New)

### 4.M1 — Mathematical Primitives (Seed Level)

These are inserted at initialisation and never derived — they are the axioms from which everything else is built.

| Primitive | Symbol | Meaning |
|---|---|---|
| Zero | 0 | The additive identity |
| One | 1 | The multiplicative identity |
| Successor | S(n) | The next natural number after n |
| Equality | = | Two expressions denote the same object |
| Set | { } | A collection of distinct objects |
| Membership | ∈ | An element belongs to a set |
| Operation | ⊕ | A rule combining two objects into one |

From these seven primitives, Ultron must **derive** all of arithmetic, not be given it.

**Derivation path:**
```
Primitive: 0, S(n), =
  → Addition: a + 0 = a; a + S(b) = S(a + b)              [Peano axioms]
  → Subtraction: inverse of addition
  → Multiplication: a × 0 = 0; a × S(b) = (a × b) + a
  → Division: inverse of multiplication (with remainder)
  → Integers: extend natural numbers with negatives
  → Rationals: pairs of integers (a/b where b ≠ 0)
  → Reals: limits of rational sequences
  → Functions: mappings between sets
  → Calculus: limits, derivatives, integrals as operations on functions
```

Each derivation is a **proof step** stored in LogicTree with its premises and the axioms it depends on. Ultron does not "know" multiplication — it derives it from Peano axioms each time, and caches the result as a verified theorem.

### 4.M2 — Mathematical Reasoner

- **Purpose:** Apply axioms and derived theorems to solve mathematical problems
- **Required behaviour:**
  - Receives a problem statement: `"What is 3 × 4?"`
  - Checks LogicTree for cached proof of `3 × 4`
  - If absent, derives from axioms: `3 × 4 = 3 × S(3) = (3 × 3) + 3 = ...`
  - Returns answer with full proof trace, not just a number
  - Updates LogicTree with the new derived fact
- **Generalisation test:** Can Ultron solve `n × 0 = 0` for any `n` it has never seen? If yes, it has internalised the rule, not just memorised instances.
- **Exit criteria:** Proof traces for all basic arithmetic operations. Generalisation to novel inputs confirmed.

### 4.M3 — Mathematical Analogy Engine

- **Purpose:** Recognise that mathematical patterns apply across different surface forms
- **Required behaviour:**
  - Structural mapping: `a + b = b + a` (commutativity of addition)
  - Recognise same structure in multiplication: `a × b = b × a`
  - Recognise same structure in set union: `A ∪ B = B ∪ A`
  - Store the abstract rule: `∀ commutative_op: x ⊕ y = y ⊕ x`
  - Apply to new operator it has never seen: `if ⊗ is commutative, then a ⊗ b = b ⊗ a`
- **Exit criteria:** Commutativity, associativity, distributivity generalised across operators.

---

## 5. The Scientific Logic Stack (New)

### 4.S1 — Scientific Primitives (Seed Level)

| Primitive | Meaning |
|---|---|
| Entity | A thing that exists and can have properties |
| Property | An attribute of an entity (mass, charge, temperature) |
| State | A complete description of an entity's properties at a moment |
| Change | A transition between states |
| Causality | A directed relationship: A produces change in B |
| Conservation | A quantity that does not change under a defined class of operations |
| Measurement | A mapping from a property to a number with a unit |
| Law | A universally quantified causal rule, verified against observations |

### 4.S2 — Scientific Reasoner

- **Purpose:** Derive physical and chemical laws from observations, not from stored formulas
- **Required behaviour:**
  - Receive observation: `"A 10kg object accelerates at 2 m/s² when a 20N force is applied"`
  - Recognise this as a (force, mass, acceleration) triple
  - Check if a law relating these three quantities exists in LogicTree
  - If not: generate hypothesis `Force = f(mass, acceleration)` and compute `f` from the observation
  - Run this against more observations to validate or refine
  - Once validated across N observations: promote to Law with confidence score
  - Store: `Newton_Second_Law: Force = mass × acceleration` with proof lineage (all supporting observations)
- **Generalisation test:** Given a new mass and acceleration it has never seen, can Ultron predict force using the derived law?
- **Exit criteria:** Laws derivable from observations. Predictions testable against new data.

### 4.S3 — Units and Dimensional Analysis

- **Purpose:** Ensure that derived rules are dimensionally consistent
- **Required behaviour:**
  - Every quantity carries a unit (kg, m/s², N, J, etc.)
  - Every derived rule is checked for dimensional consistency
  - `Force = mass × acceleration` → `[N] = [kg] × [m/s²]` ✓
  - Dimensional mismatch triggers contradiction signal
- **Exit criteria:** Unit tracking on all scientific claims. Dimensional mismatch detection active.

### 4.S4 — Scientific Analogy Engine

- **Purpose:** Recognise structural similarity between different scientific domains
- **Required behaviour:**
  - Ohm's Law: `V = I × R` (electrical domain)
  - Newton's Second Law: `F = m × a` (mechanical domain)
  - Both have structure: `effect = intensity × resistance_to_change`
  - Analogy mapper detects structural isomorphism: `V↔F, I↔a, R↔m`
  - This generates hypothesis: thermal law `ΔT = Q × R_thermal` before being told it
- **Exit criteria:** Cross-domain structural analogies detected and logged as hypotheses.

---

## 6. Generalisation Engine (New — Core Upgrade)

This is the single most important new component. It sits above all domain reasoners and is responsible for answering the question: **"Can Ultron apply what it learned here, there?"**

### 4.G1 — Abstract Rule Extractor

- **Purpose:** Lift domain-specific rules to abstract, domain-independent rules
- **Required behaviour:**
  - Learns: `2 + 3 = 3 + 2` (arithmetic instance)
  - Recognises pattern across instances: commutativity
  - Abstracts: `∀ a, b ∈ Domain: a ⊕ b = b ⊕ a` (if ⊕ is commutative)
  - Stores abstract rule in Rule Store with confidence and provenance
  - Tests abstract rule against new domains automatically

### 4.G2 — Analogy Mapper

- **Purpose:** Map structural relationships across domains using graph isomorphism
- **Required behaviour:**
  - Represent both domains as subgraphs of the Knowledge Graph
  - Find structural correspondence: which nodes/edges in domain A map to which in domain B
  - Transfer rules from A to B as hypotheses (not accepted beliefs — hypotheses)
  - Test transferred hypotheses against domain B observations
  - Promote to accepted beliefs if validated
- **This is how Ultron applies physics logic to chemistry without being told to**

### 4.G3 — Generalisation Test Suite

- **Purpose:** Continuously measure whether Ultron is learning or memorising
- **Required behaviour:**
  - Every cycle: probe Ultron with problems that are structurally similar to what it learned but with unseen numbers/entities
  - Example: learned `F = 10kg × 2m/s² = 20N` → test with `F = 7kg × 3m/s²`
  - Record: hit (correct) or miss (wrong/no answer)
  - Track generalisation rate over cycles — this must increase over time
  - If generalisation rate is flat or falling: Captain triggers strategy correction
- **Exit criteria:** Generalisation rate logged per cycle. Increasing trend confirmed over 10+ cycles.

---

## 7. Linguistic Foundation Layer (Updated from v1.0)

### 4.L1 — Morphological Analyser
- Breaks any word into root + affixes
- Maps affixes to grammatical roles (tense, person, number, negation, capability)
- All surface forms of a root map to the same concept node in the KG

### 4.L2 — Lexical Sense Disambiguator
- WordNet sense mapping for every content word
- Context-aware sense selection (fire in chemistry ≠ fire in employment)
- Semantic similarity via word vectors stored per concept node

### 4.L3 — Connector and Conjunction Handler
| Word class | Logical mapping |
|---|---|
| and, both, also | A ∧ B |
| or, either | A ∨ B |
| not, never, un- | ¬A |
| if...then, therefore | A ⇒ B |
| because, since, causes | causes(A, B) |
| although, despite | A ∧ ¬expected(B) ⇒ B |
| before, after, when | temporal(A, B) |
| equals, is, same as | A = B |
| greater than, more than | A > B |

### 4.L4 — Dependency Parser + SRL
- spaCy en_core_web_trf: dependency tree per sentence
- AllenNLP SRL: semantic role labels (ARG0, ARG1, ARGM-TMP, etc.)
- Logical Form Builder: converts dependency tree + roles into FOL-compatible triples

### 4.L5 — Logical Form Builder
- Converts full parsed sentence into a set of formal logical expressions
- Preserves: negation, modality, conditionality, temporal modifiers, quantifiers
- Output format: Claim objects with structured metadata, not flat strings

---

## 8. Updated Component Specifications

### 4.1 Seed (Updated)
- Inserts mathematical primitives (0, 1, S(n), =, ∈, ⊕, set) at init
- Inserts scientific primitives (entity, property, state, change, causality, conservation, measurement, law) at init
- Inserts linguistic primitives (token, morpheme, word, connector, quantifier) at init
- Exit criteria: ≥21 seed nodes (7 math + 7 science + 7 linguistic) before cycle 1

### 4.2 STARK (Unchanged from v1.0)
### 4.3 Semantic Engine (Updated — now includes L1–L5 above)
### 4.4 Prediction Engine (Unchanged from v1.0)
### 4.5 Curiosity Signal (Unchanged from v1.0)
### 4.6 Knowledge Graph + LogicTree (Updated)
- Domain ontologies: Math, Physics, Chemistry, Biology, Logic, Language
- Rule Store: derived rules with proof lineage
- Law Store: validated scientific laws with supporting observations
### 4.7 Temporal Reasoning (Unchanged from v1.0)
### 4.8 Belief Revision Engine (Unchanged from v1.0)
### 4.9 Theorem Prover (Updated)
- Handles mathematical axiom chains (Peano, set theory, etc.)
- Handles scientific law derivation from observations
- Handles cross-domain analogy proofs
### 4.10 Causal Engine (Unchanged from v1.0)
### 4.11 Hypothesis Engine (Updated)
- Generates cross-domain hypotheses via analogy mapper
- Scores by structural similarity score × causal chain support
### 4.12 Reasoning Engine (Updated)
- Now handles: "what is X", "why does X cause Y", "is X true", "what is the value of X given Y"
- Mathematical query mode: solve equations, derive values from laws
- Scientific query mode: apply laws to new measurements
### 4.13 Goal System (Unchanged from v1.0)
### 4.14 Captain (Updated)
- Adds generalisation rate to cycle metrics
- Adds analogical transfer success/failure rate
- Strategy correction now also covers: "used memorisation where derivation was possible"
### 4.15 Thanos (Unchanged from v1.0)

---

## 9. Benchmark and Quality Gates (Updated)

| Gate | Metric | Pass threshold |
|---|---|---|
| Semantic extraction accuracy | % correct on 100-sentence suite | ≥90% |
| Prediction error trend | Avg error for seen topics | Decreasing over 10+ cycles |
| Proof success rate | % of goals proved | ≥60% |
| Verification support rate | % of answers with external evidence | ≥50% |
| Generalisation hit rate | Hits on unseen problem probes | Increasing trend |
| Belief acceptance rate | % accepted vs contested | ≥60% |
| Rollback integrity | Rollback restores exact prior state | 100% fidelity |
| Mathematical derivation | Can derive arithmetic from Peano axioms | All basic ops covered |
| Scientific law derivation | Can derive F=ma from observations | ≥3 laws derived |
| Cross-domain analogy | Detects structural isomorphism across domains | ≥1 analogy confirmed |
| Generalisation rate | % correct on structurally-novel problems | Increasing each phase |

---

## 10. Version Roadmap (Updated)

| Version | Theme | Key additions |
|---|---|---|
| v3.5 | Prediction-error learning | Prediction engine, curiosity signal, weight update ✓ |
| v3.6 | Linguistic foundation | Morphological analyser, WordNet, SRL, connector handler, logical form builder |
| v3.7 | FOL theorem prover upgrade | Full resolution, paramodulation, proof indexing |
| v3.8 | Mathematical logic stack | Peano seed, arithmetic derivation, math reasoner, math generalisation test |
| v3.9 | Scientific logic stack | Scientific primitives, law derivation from observation, unit/dimensional analysis |
| v4.0 | Analogical reasoning | Abstract rule extractor, analogy mapper, cross-domain hypothesis transfer |
| v4.1 | Generalisation engine | Generalisation test suite, generalisation rate metric, Captain generalisation gating |
| v4.2 | Causal + counterfactual | Do-calculus, front/back-door criteria, counterfactual queries |
| v4.3 | Captain RSI strategy | Strategy classifier, strategy weight update, benchmark-gated self-improvement |
| v4.4 | Thanos RSI sandbox | Sandboxed graph proposals, rollback gate, RSI loop end-to-end |
| v4.5 | Always-learning loop | Infinite curiosity-driven curriculum, no idle state |
| v4.6 | Simulation grounding | PyBullet/grid-world for physical causality testing |
| v4.7 | ASI validation | Long-run trials, PRD checklist audit, frontier benchmark evaluation |

---

## 11. What Ultron Is NOT

- Not a language model — does not predict tokens
- Not a retrieval system — does not return documents
- Not a formula lookup — derives mathematical results from axioms
- Not a static knowledge base — derives and updates from prediction error
- Not a classifier — reasons, proves, derives, generalises, and revises

---

## 12. Single Line of Truth

> Ultron understands something when it can solve a problem it has never seen, in a domain it learned from scratch, using logic it derived rather than memorised.

DOCEOF
