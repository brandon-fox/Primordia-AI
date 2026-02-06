# Feature Specification: Position Evaluation Heuristics

**Feature Branch**: `021-position-eval`  
**Created**: 2026-02-06  
**Status**: Draft  
**Target**: Week 2 | **Repository**: Primordia-AI

## User Scenarios & Testing

### User Story 1 - Evaluate Board Position (Priority: P1)

System evaluates current game position and returns numeric score.

**Acceptance Scenarios**:
1. **Given** game state input, **When** evaluate called, **Then** score returned (-100 to +100)
2. **Given** evaluation result, **When** queried, **Then** factor breakdown available

---

## Requirements

### Functional Requirements
- **FR-001**: System MUST evaluate position on -100 to +100 scale
- **FR-002**: System MUST provide factor-by-factor breakdown
- **FR-003**: System MUST complete evaluation in under 500ms

### Key Entities
- **Evaluation**: score, factors[], confidence, computeTimeMs
- **Factor**: name, weight, contribution

## Success Criteria
- **SC-001**: Evaluation in <500ms
- **SC-002**: Score correlates with win probability
