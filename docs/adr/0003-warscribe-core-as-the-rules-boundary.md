# ADR-0003: WARScribe-Core as the rules boundary

- Status: proposed (February 2026); boundary defined, engine incomplete. Recorded 2026-11-05 as part of the design record.
- Deciders: Brandon Fox

## Context

A tactical engine that embeds its own copy of the game rules drifts from the rules the platform actually enforces, and two copies of a rulebook are two sources of bugs. The platform already has a notation and rules layer (WARScribe-Core, spec 015) that defines what a legal action is.

## Decision

Primordia never decides legality. It asks WARScribe-Core for the legal moves from a state and for the resolution of a chosen move; the engine only searches and evaluates. The `GameState` it encodes is the one WARScribe-Core produces.

## Consequences

- One rules implementation, one place to fix a rules bug, and the engine's output is legal by construction.
- The engine's performance is bounded by the rules layer's move generation; ADR-0001 depends on that path being fast.
- Primordia cannot run standalone; it is a consumer of the platform, which is the intended relationship.
