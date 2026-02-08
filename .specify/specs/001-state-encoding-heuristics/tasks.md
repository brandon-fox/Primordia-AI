# Tasks: State Encoding & Heuristic Evaluation

**Feature Branch**: `001-state-encoding-heuristics`
**Spec**: [spec.md](spec.md)
**Created**: 2026-02-08

---

## User Story: US-01 — AI Search Engine (Encoding)

### T-001: Unit tests for GameStateEncoder

- **Priority**: P0
- **Estimate**: 30 min
- **File**: `tests/test_encoding.py`
- **Acceptance Criteria**:
  - [ ] Test encode() produces correct shape arrays
  - [ ] Test global features normalization (turn, phase, VP)
  - [ ] Test unit features (position, health, status flags)
  - [ ] Test zero-padding for < MAX_UNITS units
  - [ ] Test attention masks
  - [ ] Test flat() and total_dim properties
- **Dependencies**: None

### T-002: Unit tests for EncodedState

- **Priority**: P1
- **Estimate**: 15 min
- **File**: `tests/test_encoding.py`
- **Acceptance Criteria**:
  - [ ] Test flat property concatenation
  - [ ] Test total_dim calculation
  - [ ] Test with edge cases (empty player units)
- **Dependencies**: None

---

## User Story: US-02 — Position Evaluator

### T-003: Unit tests for PositionEvaluation

- **Priority**: P0
- **Estimate**: 20 min
- **File**: `tests/test_evaluation.py`
- **Acceptance Criteria**:
  - [ ] Test overall_score range validation
  - [ ] Test is_winning/is_losing thresholds
  - [ ] Test factor_scores composition
  - [ ] Test confidence range
- **Dependencies**: None

---

## User Story: US-03 — Game State Model

### T-004: Unit tests for models

- **Priority**: P0
- **Estimate**: 25 min
- **File**: `tests/test_models.py`
- **Acceptance Criteria**:
  - [ ] Test Unit creation with all fields
  - [ ] Test GameState creation
  - [ ] Test Phase enum values
  - [ ] Test UnitStatus enum
  - [ ] Test position/wound calculations
- **Dependencies**: None

### T-005: Unit tests for Opening Book

- **Priority**: P1
- **Estimate**: 30 min
- **File**: `tests/test_opening_book.py`
- **Acceptance Criteria**:
  - [ ] Test database initialization
  - [ ] Test opening book queries
  - [ ] Test faction archetype matching
  - [ ] Test list similarity scoring
- **Dependencies**: None

---

## Cross-cutting: Quality Gates

### T-006: Mypy strict mode

- **Priority**: P0
- **Estimate**: 20 min
- **Acceptance Criteria**:
  - [ ] `uv run mypy src/primordia/ --strict` passes
  - [ ] Fix any type annotation issues
- **Dependencies**: None

### T-007: Test coverage gate

- **Priority**: P0
- **Estimate**: 10 min
- **Acceptance Criteria**:
  - [ ] `pytest --cov=primordia` >= 80%
  - [ ] All critical paths covered
- **Dependencies**: T-001 through T-005

### T-008: Integration with Vindicta-Core wargame models

- **Priority**: P2 (after Vindicta-Core 041 merges)
- **Estimate**: 45 min
- **Acceptance Criteria**:
  - [ ] Import models from `vindicta_core.wargame` instead of local `models.py`
  - [ ] Or maintain adapter pattern between local and shared models
  - [ ] All existing tests pass after migration
- **Dependencies**: Vindicta-Core #24

---

## Summary

| Metric         | Value              |
| -------------- | ------------------ |
| Total tasks    | 8                  |
| P0 tasks       | 4                  |
| P1 tasks       | 2                  |
| P2 tasks       | 2                  |
| New files      | 4 (all test files) |
| Modified files | 0                  |
| Estimated time | ~3 hours           |
