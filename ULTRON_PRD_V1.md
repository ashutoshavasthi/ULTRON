# Ultron — Product Requirements Document (PRD)

**Version:** 1.0  
**Status:** Active  
**Owner:** Ultron Project  
**Goal:** Build Ultron into an ASI-capable, prediction-driven, self-improving reasoning system

---

## 1. Vision

Ultron is not a database. It is a learning system modeled on how a child develops intelligence — starting from seeds, building causal world models, predicting before observing, correcting itself from error, and growing autonomously toward deeper understanding. The long-term target is an ASI-capable system that knows more than all of human knowledge combined, improves its own reasoning loop through experience, and does so safely and verifiably.

---

## 2. Core Design Philosophy

| Principle | Description |
|---|---|
| **Prediction before storage** | Ultron must predict what it expects before ingesting new information. Learning happens from the gap between prediction and reality, not from storing facts. |
| **Causality over correlation** | All knowledge must be represented as causal relationships, not statistical associations. Ultron must understand *why*, not just *what*. |
| **Curiosity-driven exploration** | Topics with the highest prediction uncertainty are pursued first. Ultron explores where it is most wrong, not where it is safest. |
| **Belief revision, not accumulation** | Competing beliefs are detected, scored by source reliability and temporal evidence, and resolved. Old beliefs can be rolled back if revisions worsen performance. |
| **Self-improvement under supervision** | The Captain and Thanos layers must evaluate every reasoning cycle. Self-improvement is gated by benchmark performance, not applied blindly. |
| **Grounded in the real world** | Ultron verifies its beliefs against multiple external sources. Knowledge must be anchored to evidence, not self-referential. |

---

## 3. Architecture Overview

```
Seed
 └── Captain (metacognitive supervisor)
      ├── STARK (semantic extraction, web grounding)
      ├── Semantic Engine (ensemble parser → logical forms)
      ├── Prediction Engine (predict before observe)
      ├── Curiosity Signal (uncertainty-driven curriculum)
      ├── Knowledge Graph + LogicTree (causal world model)
      ├── Temporal Reasoning (time-tagged beliefs)
      ├── Belief Revision Engine (contradiction handling, versioned history)
      ├── Theorem Prover (given-clause FOL proof engine)
      ├── Causal Engine (do-calculus, counterfactual reasoning)
      ├── Hypothesis Engine (generalization from causal patterns)
      ├── Reasoning Engine (query answering over graph)
      ├── Goal System (always-learning curriculum)
      └── Thanos (RSI sandbox, experiment logger, rollback evaluator)
```

---

## 4. Component Specifications

### 4.1 Seed
- **Purpose:** Initialize the system with fundamental ontological primitives
- **Required behaviour:** On startup, seed inserts core conceptual nodes (entity, event, property, relation, causality, time, space) into the knowledge graph before any learning begins
- **Exit criteria:** Graph contains at least 7 seed nodes at initialization

### 4.2 STARK (Semantic Trigger And Retrieval of Knowledge)
- **Purpose:** Ingest text from any source and extract structured claims
- **Required behaviour:**
  - Ensemble parser (LLM adapter → spaCy → regex fallback) produces SemanticFrames
  - Each frame carries subject, predicate, object, confidence, temporal status, and provenance
  - Claims are grounded against Wikipedia, Wikidata, and DuckDuckGo (3-source minimum)
  - Credibility score weights evidence by source reliability
- **Quality bar:** ≥90% correct extraction on curated regression suite (100 sentences)
- **Exit criteria:** Ensemble parser active, 3-source verification active, SemanticFrame schema stable

### 4.3 Semantic Engine
- **Purpose:** Convert natural language into logical forms Ultron can reason over
- **Required behaviour:**
  - spaCy transformer parser (en_core_web_trf preferred) for dependency and SRL extraction
  - Entity resolution maps surface forms to canonical concept nodes
  - Temporal modifiers (past/now/future) preserved in every frame
  - Negation, modality, and conditionality handled explicitly
- **Quality bar:** ≥90% accuracy on semantic regression suite
- **Exit criteria:** SRL active, entity linker active, temporal parsing active

### 4.4 Prediction Engine
- **Purpose:** Make Ultron a learner, not a database
- **Required behaviour:**
  - Before ingesting a new topic, generate predicted claims from the current graph state
  - Compute prediction error = 1 − (correct predictions / total expected claims)
  - Update causal edge weights in the graph proportional to prediction error
  - Error shrinks over cycles for well-understood topics; stays high for novel ones
- **Exit criteria:** Prediction error logged per cycle, causal weights update after every ingestion

### 4.5 Curiosity Signal
- **Purpose:** Drive autonomous exploration toward areas of maximum uncertainty
- **Required behaviour:**
  - Maintain a curiosity score per topic = last prediction error on that topic
  - Topics with score = 1.0 (never seen) are visited first
  - After all topics have been seen, the topic with the highest error is prioritised next
  - Captain can override curiosity priority for benchmark or safety evaluations
- **Exit criteria:** Curiosity scores exist per topic, next-topic selection uses curiosity not random order

### 4.6 Knowledge Graph + LogicTree
- **Purpose:** Store Ultron's causal world model as a live, weighted, versioned graph
- **Required behaviour:**
  - Every node represents a concept; every edge represents a typed causal/logical relationship
  - Edge weights are updated by prediction error, not only by source confidence
  - Graph is exportable to JSON (for D3 viewer) after every cycle
  - LogicTree indexes theorems derived from graph edges for fast proof lookup
- **Exit criteria:** Graph persists across cycles, weights update from prediction error, JSON export active

### 4.7 Temporal Reasoning Engine
- **Purpose:** Track belief evolution over time and reason about past, present, and future states
- **Required behaviour:**
  - Claims tagged as past / current / future at extraction time
  - Reasoner prioritises current-tagged claims when answering queries
  - Temporal contradictions (same subject/predicate, different time, conflicting object) detected separately from atemporal contradictions
  - Temporal summary artifact produced every cycle
- **Exit criteria:** Temporal tags in graph, reasoner uses temporal priority, temporal summary in run artifacts

### 4.8 Belief Revision Engine
- **Purpose:** Resolve competing beliefs and maintain an auditable truth store
- **Required behaviour:**
  - Contradiction detector groups claims by (subject, predicate, temporal_status)
  - Belief scorer = confidence × source_weight + verification_bonus + temporal_bonus
  - Winning belief marked `accepted`; others marked `contested`
  - Belief history versioned per cycle with rollback support
- **Source weights:** wikidata=0.82, wikipedia=0.72, duckduckgo=0.55, llm=0.60, spacy=0.58, regex=0.45
- **Exit criteria:** Contradictions detected, belief_history.json written per run, rollback to any prior version functional

### 4.9 Theorem Prover
- **Purpose:** Formal proof over the knowledge graph using First-Order Logic
- **Required behaviour:**
  - Given-clause style resolution with modus ponens chain support
  - ProofObject returned with steps, premises, and score
  - Proof score degrades with chain length (penalise long, uncertain chains)
  - Future: full resolution with paramodulation and indexing
- **Exit criteria:** ProofObject produced per cycle, multi-step modus ponens chains functional

### 4.10 Causal Engine
- **Purpose:** Understand intervention and counterfactual outcomes
- **Required behaviour:**
  - Pearl do-calculus rule transformations: front-door, back-door criteria
  - `explain(graph)` returns causal chain with confidence and temporal status
  - Counterfactual queries: "What if X had not caused Y?"
- **Exit criteria:** Causal explanation produced per cycle, do-calculus rule stubs active

### 4.11 Hypothesis Engine
- **Purpose:** Generate new testable hypotheses from causal patterns
- **Required behaviour:**
  - Infer implicit mediators from existing causal chains
  - Score hypotheses by plausibility (causal weight × path support)
  - Top-5 hypotheses returned per cycle; Captain decides which to pursue
- **Exit criteria:** Hypotheses generated per cycle, scored and ranked

### 4.12 Reasoning Engine
- **Purpose:** Answer natural language queries over the current world model
- **Required behaviour:**
  - `what is X` queries resolved via graph lookup with temporal priority
  - `why does X cause Y` queries resolved via causal chain traversal
  - `is X true` queries resolved via theorem prover
  - Answer includes provenance, source, confidence, and temporal status
- **Exit criteria:** All three query types handled, provenance attached to every answer

### 4.13 Goal System / Always-Learning
- **Purpose:** Drive continuous autonomous learning without external prompting
- **Required behaviour:**
  - GoalQueue driven by curiosity signal, not a static list
  - Captain can inject benchmark goals or safety evaluation topics
  - Always-learning loop: no idle state; system pursues next goal immediately after cycle completion
- **Exit criteria:** Curiosity-driven topic selection active, Captain can inject goals

### 4.14 Captain (Metacognitive Supervisor)
- **Purpose:** Evaluate every cycle, correct bad reasoning strategies, gate self-improvement
- **Required behaviour:**
  - Evaluate: answer_supported, proof_success, verification_score, accepted/contested beliefs, prediction_error, rollback_ready, generalization score
  - Detect: reasoning strategy failures (e.g., deduction used where abduction needed)
  - Correct: update reasoning strategy weights, not just output labels
  - Gate: self-improvement changes proposed by Thanos only applied if benchmark performance does not regress
  - Generalization test: probe unseen entities every cycle and log hit/miss
- **Exit criteria:** All metrics logged per cycle, generalization test active, benchmark gate functional

### 4.15 Thanos (RSI Sandbox)
- **Purpose:** Recursive self-improvement under supervision
- **Required behaviour:**
  - Log every experiment to JSONL file with cycle, topic, and all metrics
  - Propose reasoning weight updates based on accumulated error patterns
  - Test proposals in a sandboxed copy of the graph before applying to main graph
  - Rollback if sandbox performance is worse than current baseline
- **Exit criteria:** JSONL experiment log active, sandbox testing functional, rollback gate active

---

## 5. Data Artifacts (Required Per Run)

| Artifact | Path | Description |
|---|---|---|
| `last_run_vX_X.json` | `artifacts/` | Full cycle output including metrics, beliefs, proofs |
| `kg_export.json` | `artifacts/` | Graph nodes + weighted edges for D3 viewer |
| `belief_history.json` | `artifacts/` | All versioned belief states across cycles |
| `rollback_snapshot_v2.json` | `artifacts/` | Example rollback to version 2 for validation |
| `experiments.jsonl` | `ultron/thanos/` | Thanos experiment log across all runs |

---

## 6. Benchmark and Quality Gates

| Gate | Metric | Pass threshold |
|---|---|---|
| Semantic extraction accuracy | % correct on 100-sentence regression suite | ≥ 90% |
| Prediction error trend | Avg error across cycles for seen topics | Decreasing over 10+ cycles |
| Proof success rate | % of goals proved across cycles | ≥ 60% |
| Verification support rate | % of answers with external evidence | ≥ 50% |
| Generalization hit rate | Hits on unseen entity probe | Increasing trend |
| Belief acceptance rate | % accepted vs contested | ≥ 60% accepted |
| Rollback integrity | Rollback restores exact versioned state | 100% fidelity |

---

## 7. Version Roadmap

| Version | Theme | Key additions |
|---|---|---|
| v3.2 | Multi-source verification | 3-source verifier (Wikipedia + Wikidata + DuckDuckGo) |
| v3.3 | Contradiction handling | Belief revision engine, source weights, contradiction detector |
| v3.4 | Temporal reasoning | Time-tagged claims, belief history, rollback manager |
| v3.5 | Prediction-error learning | Prediction engine, curiosity signal, generalization test, causal weight update |
| **v3.6** | Real semantic parsing | spaCy en_core_web_trf, SRL layer, entity linker, 100-sentence regression suite |
| **v3.7** | Given-clause theorem prover | Full resolution loop, paramodulation, proof indexing, proof score calibration |
| **v3.8** | Do-calculus causal engine | Front-door / back-door criterion, counterfactual reasoning, intervention queries |
| **v3.9** | Captain reasoning strategy | Strategy classifier, strategy weight update, benchmark-gated self-improvement |
| **v4.0** | Thanos RSI sandbox | Sandboxed graph copy, proposal testing, rollback gate, RSI loop end-to-end |
| **v4.1** | Always-learning loop | Infinite cycle with curiosity queue, no idle state, autonomous curriculum |
| **v4.2** | Simulation grounding | PyBullet / grid-world environment for physical causality testing |
| **v4.3** | ASI validation | Long-run trials, external benchmark suite, PRD checklist audit |

---

## 8. What Ultron Is NOT

- Not a language model — it does not predict tokens
- Not a retrieval system — it does not return documents
- Not a static knowledge base — beliefs update from prediction error, not only from ingestion
- Not a classifier — it reasons, proves, and revises

---

## 9. Single Line of Truth

> Ultron learns by predicting, failing, and updating. Every claim it holds was either derived from reasoning over evidence, or is actively marked contested until it is.

