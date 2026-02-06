# Tasks: Opening Book Lookup

**Input**: specs/022-opening-book/ | **Prerequisites**: spec.md, plan.md

## Phase 1: Setup

- [ ] T001 Create `src/openings/` directory
- [ ] T002 [P] Create `src/data/openings.json`

---

## Phase 2: Foundational

- [ ] T003 Define Opening Pydantic model
- [ ] T004 [P] Define LookupResult Pydantic model
- [ ] T005 Populate initial opening database

---

## Phase 3: User Story 1 - Lookup Opening Position (P1) 🎯 MVP

- [ ] T006 [US1] Implement `lookup()` method
- [ ] T007 [US1] Match position against database
- [ ] T008 [US1] Return opening with confidence
- [ ] T009 [US1] Support faction-specific filtering

---

## Phase 4: Polish

- [ ] T010 [P] Optimize for <100ms lookup
- [ ] T011 [P] Write unit tests
- [ ] T012 [P] Add opening database CRUD utilities
