# Tasks: Position Evaluation Heuristics

**Input**: specs/021-position-eval/ | **Prerequisites**: spec.md, plan.md

## Phase 1: Setup

- [ ] T001 Create `src/evaluation/` directory
- [ ] T002 [P] Create `src/models/evaluation.py`

---

## Phase 2: Foundational

- [ ] T003 Define Evaluation Pydantic model
- [ ] T004 [P] Define Factor Pydantic model
- [ ] T005 Create base Evaluator class

---

## Phase 3: User Story 1 - Evaluate Board Position (P1) 🎯 MVP

- [ ] T006 [US1] Implement `evaluate()` method
- [ ] T007 [US1] Define core evaluation factors
- [ ] T008 [US1] Configure factor weights
- [ ] T009 [US1] Calculate composite score
- [ ] T010 [US1] Return factor breakdown

---

## Phase 4: Polish

- [ ] T011 [P] Optimize for <500ms performance
- [ ] T012 [P] Write unit tests
- [ ] T013 [P] Add calibration utilities
