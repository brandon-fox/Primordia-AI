# Feature Specification: State Encoding & Heuristic Evaluation

**Feature Branch**: `001-state-encoding-heuristics`
**Created**: 2026-02-08
**Status**: Implemented (documenting existing)
**Target**: Week 1-2 | **Repository**: Primordia-AI
**Milestone**: v0.1.0 — Foundation
**Feature ID**: PRIM-001
**Priority**: P0

---

## 1. Problem Statement

Primordia-AI needs to evaluate wargame positions for the Meta-Oracle's list grading and future MCTS search. This requires:

1. **State encoding**: Convert complex game states (units, positions, VP) into normalized numerical vectors suitable for ML model input
2. **Heuristic evaluation**: Score game positions on a [-1.0, +1.0] scale across multiple strategic factors without ML models

---

## 2. Vision

Provide the **foundation layer** for all Primordia-AI intelligence: a game state encoder that produces fixed-size normalized vectors, and a heuristic evaluation framework that scores positions using domain-expert knowledge.

---

## 3. User Stories

### US-01: AI Search Engine

> As the **future MCTS search engine**,
> I want **fixed-size normalized state vectors**,
> So that **I can evaluate leaf positions during tree search**.

**Acceptance Criteria:**

- [x] `GameStateEncoder.encode(state)` returns `EncodedState` with numpy arrays
- [x] Global features: 8 dimensions (turn, phase, active player, VP, unit counts)
- [x] Unit features: 12 dimensions per unit (position, health, status, actions)
- [x] Fixed-size output (20 units per player, zero-padded)
- [x] Attention masks for valid vs padding units

### US-02: Position Evaluator

> As the **Meta-Oracle list grader**,
> I want **heuristic position scores with factor breakdown**,
> So that **I can explain why a position favors one player**.

**Acceptance Criteria:**

- [x] `PositionEvaluation` with overall_score [-1.0, +1.0]
- [x] `FactorScore` with per-factor weights: board control, objective control, unit preservation, threat projection, mobility, synergy
- [x] `is_winning()` / `is_losing()` threshold methods
- [x] Confidence score [0.0, 1.0]
- [x] Optional reasoning string

### US-03: Game State Model

> As the **platform developer**,
> I want **Pydantic game state models specific to Primordia's needs**,
> So that **encoding and evaluation have well-typed input data**.

**Acceptance Criteria:**

- [x] `Unit` model with position, wounds, models, status, action flags
- [x] `GameState` with players, turns, phase, VP tracking
- [x] `Phase` enum and `UnitStatus` enum
- [x] All models serializable

---

## 4. Existing Implementation

| File                              | Status        | Contents                                                           |
| --------------------------------- | ------------- | ------------------------------------------------------------------ |
| `src/primordia/encoding.py`       | ✅ Implemented | `GameStateEncoder`, `EncodedState` (195 lines)                     |
| `src/primordia/evaluation.py`     | ✅ Implemented | `EvaluationFactor`, `FactorScore`, `PositionEvaluation` (51 lines) |
| `src/primordia/models.py`         | ✅ Implemented | `Unit`, `GameState`, `Phase`, `UnitStatus`                         |
| `src/primordia/opening_book.py`   | ✅ Implemented | Opening Book database                                              |
| `src/primordia/opening_models.py` | ✅ Implemented | Opening Book data models                                           |
| `src/primordia/database.py`       | ✅ Implemented | DuckDB integration                                                 |

---

## 5. Remaining Work (Spec → Tasks)

While core implementation exists, the following formalization work is needed:

1. **Test coverage**: No tests directory exists — need tests for encoding, evaluation, models
2. **Type checking**: Need mypy strict compliance verification
3. **Integration with Vindicta-Core**: Models should reference `vindicta_core.wargame` models (after 041 merges)
4. **Documentation**: Models lack module-level documentation and usage examples
5. **Opening Book tests**: Database and opening book need test coverage

---

## 6. Constraints

| Constraint                             | Source               |
| -------------------------------------- | -------------------- |
| NumPy for encoding (only external dep) | Performance          |
| Pydantic v2 for models                 | Platform standard    |
| DuckDB for Opening Book                | Free-tier compliance |
| No ML model inference in v0.1.0        | Heuristics only      |

---

## 7. Quality Checklist

- [x] Problem statement clearly defines the gap
- [x] Vision connects to platform-wide architecture
- [x] User stories cover search, evaluation, and data modeling
- [x] Implementation status documented
- [x] Remaining work identified
- [x] Constraints stated
