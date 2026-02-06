# Feature Specification: Game State Encoder

**Feature Branch**: `023-state-encoder`  
**Created**: 2026-02-06  
**Status**: Draft  
**Target**: Week 2 | **Repository**: Primordia-AI

## User Scenarios & Testing

### User Story 1 - Encode Game State (Priority: P1)

System converts game state to normalized vector representation.

**Acceptance Scenarios**:
1. **Given** game state, **When** encode called, **Then** vector returned
2. **Given** encoded vector, **When** decode called, **Then** state reconstructed

---

## Requirements

### Functional Requirements
- **FR-001**: System MUST encode state to fixed-size vector
- **FR-002**: System MUST support decode (reversible)
- **FR-003**: System MUST handle variable army compositions

### Key Entities
- **GameState**: units[], board, turn, phase
- **EncodedState**: vector[], metadata

## Success Criteria
- **SC-001**: Encode/decode round-trip lossless
- **SC-002**: Encoding in <50ms
