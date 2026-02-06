# Feature Specification: Opening Book Lookup

**Feature Branch**: `022-opening-book`  
**Created**: 2026-02-06  
**Status**: Draft  
**Target**: Week 3 | **Repository**: Primordia-AI

## User Scenarios & Testing

### User Story 1 - Lookup Opening Position (Priority: P1)

System matches game state to known opening theory.

**Acceptance Scenarios**:
1. **Given** early game state, **When** lookup called, **Then** matching opening returned
2. **Given** unknown position, **When** lookup called, **Then** null returned

---

## Requirements

### Functional Requirements
- **FR-001**: System MUST match positions to opening database
- **FR-002**: System MUST return opening name and expected lines
- **FR-003**: System MUST support faction-specific openings

### Key Entities
- **Opening**: name, faction, moves[], winRate
- **LookupResult**: opening, confidence, nextMoves[]

## Success Criteria
- **SC-001**: Lookup in <100ms
- **SC-002**: 95% accuracy on known openings
