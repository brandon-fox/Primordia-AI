# Tasks: Game State Encoder

**Input**: specs/023-state-encoder/ | **Prerequisites**: spec.md, plan.md

## Phase 1: Setup

- [ ] T001 Create `src/encoding/` directory

---

## Phase 2: Foundational

- [ ] T002 Define GameState Pydantic model
- [ ] T003 [P] Define EncodedState model
- [ ] T004 Define encoding schema

---

## Phase 3: User Story 1 - Encode Game State (P1) 🎯 MVP

- [ ] T005 [US1] Implement `encode()` method
- [ ] T006 [US1] Normalize unit data to vectors
- [ ] T007 [US1] Encode board state
- [ ] T008 [US1] Implement `decode()` method
- [ ] T009 [US1] Verify round-trip lossless

---

## Phase 4: Polish

- [ ] T010 [P] Optimize for <50ms encoding
- [ ] T011 [P] Write unit tests
