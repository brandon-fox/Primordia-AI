# Specification: Foundation (v0.1.0)

**Feature ID:** 001-foundation
**Milestone:** v0.1.0 — Foundation
**Priority:** P0
**Status:** Specified
**Target Date:** Feb 17, 2026

---

## 1. Problem Statement

The Vindicta Platform requires an AI engine capable of evaluating game states
and recommending optimal actions for tabletop wargaming. Primordia-AI needs a
foundational layer that can encode Vindicta-Core `GameState` objects into
numerical representations suitable for search algorithms, and apply heuristic
evaluation functions to score positions.

---

## 2. Vision

Create the core AI evaluation framework: state encoding for MCTS search trees,
heuristic evaluation functions for position scoring, and a basic best-move
recommendation engine.

---

## 3. User Stories

### US-01: State Encoding

> As the **MCTS search engine**,
> I want to **encode a GameState into a fixed-size numerical tensor**,
> So that **the search tree can efficiently compare and cache states**.

**Acceptance Criteria:**

- [ ] `StateEncoder.encode(game_state)` → numpy array
- [ ] Encoding is deterministic (same state → same encoding)
- [ ] Encoding captures: unit positions, health, phase, turn, scores
- [ ] Encoding is hashable for transposition table support

### US-02: Heuristic Evaluation

> As the **Primordia AI engine**,
> I want to **evaluate a game state and return a numerical score**,
> So that **the search algorithm can compare candidate moves**.

**Acceptance Criteria:**

- [ ] `Evaluator.evaluate(game_state, player_id)` → float score
- [ ] Score considers: material (surviving models), position, VP
- [ ] Higher score = better position for the given player
- [ ] Evaluation < 1ms per state

### US-03: Move Generation

> As the **recommendation engine**,
> I want to **generate all legal actions** for the current state,
> So that **the search tree can explore all options**.

**Acceptance Criteria:**

- [ ] `MoveGenerator.generate(game_state)` → list of Action
- [ ] Actions are valid Vindicta-Core Action types
- [ ] Generator respects phase constraints (only move in Movement, etc.)
- [ ] "Pass" action always available

### US-04: Best Move Recommendation

> As a **Vindicta-Portal user**,
> I want to **ask the AI for a recommended action**,
> So that **I can see what the AI would do in my position**.

**Acceptance Criteria:**

- [ ] `Engine.recommend(game_state)` → Action + evaluation score
- [ ] Uses greedy 1-ply search (heuristic on all immediate moves)
- [ ] Returns within 100ms for typical game states
- [ ] Future: MCTS depth search (v0.2.0+)

---

## 4. Functional Requirements

### 4.1 StateEncoder

| Method       | Signature                   | Description                    |
| ------------ | --------------------------- | ------------------------------ |
| `encode`     | `(GameState) -> np.ndarray` | Fixed-size float32 vector      |
| `hash_state` | `(GameState) -> int`        | Integer hash for transposition |
| `decode`     | `(np.ndarray) -> dict`      | Debug: interpret encoding      |

Encoding schema:
- Unit block: 64 floats per unit (stats, health, position, status)
- Max 30 units per player → 3840 floats for units
- Global: turn, phase, CP, VP, active player → 10 floats
- Total: ~3850 float32 values

### 4.2 Evaluator

| Component | Weight | Description                           |
| --------- | ------ | ------------------------------------- |
| Material  | 0.4    | Surviving model points / total points |
| Position  | 0.2    | Objective control scoring             |
| VP        | 0.3    | Current VP / max VP                   |
| Tempo     | 0.1    | Phase advantage (acting vs waiting)   |

Configurable weights via `EvaluationConfig`.

### 4.3 MoveGenerator

Phase-aware action generation:
- **Command Phase**: Use stratagem (stub), pass
- **Movement Phase**: Move actions for each eligible unit
- **Shooting Phase**: Shoot actions for each unit with ranged weapons
- **Charge Phase**: Charge actions for eligible units
- **Fight Phase**: Fight actions for engaged units

### 4.4 Engine

```python
from primordia_ai import PrimordiaEngine

engine = PrimordiaEngine()
result = engine.recommend(game_state)
print(f"Best move: {result.action}, Score: {result.score:.3f}")
```

---

## 5. Non-Functional Requirements

| Category         | Requirement                              |
| ---------------- | ---------------------------------------- |
| **Performance**  | Evaluation < 1ms; Recommend < 100ms      |
| **Dependencies** | numpy, vindicta-core                     |
| **Type Safety**  | 100% strict mypy                         |
| **Determinism**  | Same input → same output (no randomness) |

---

## 6. Out of Scope

- MCTS search (v0.2.0)
- Opening book database (v0.1.5)
- Neural network evaluation
- Training pipeline

---

## 7. Success Criteria

| Metric         | Target                  |
| -------------- | ----------------------- |
| State encoding | Deterministic, hashable |
| Evaluation     | < 1ms per state         |
| Recommendation | < 100ms per call        |
| Type safety    | Zero mypy errors        |
| Test coverage  | > 90%                   |
