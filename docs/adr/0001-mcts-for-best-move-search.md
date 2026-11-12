# ADR-0001: Monte Carlo tree search for best-move search

- Status: proposed (February 2026); never executed. Recorded 2026-11-05 as part of the design record.
- Deciders: Brandon Fox

## Context

Tabletop wargame turns have a large, irregular branching factor (movement in continuous space, dice-resolved combat, order of activation) and no cheap exact evaluation. Alpha-beta search needs a reliable static evaluator and a manageable branching factor; neither exists here. The engine must also work with incomplete information about the opponent's hidden choices.

## Decision

Use Monte Carlo tree search (UCT) over legal moves supplied by the rules engine, with playouts resolved by the deterministic dice engine seeded from the entropy buffer so that any search can be replayed exactly. The heuristic evaluator (`evaluation.py`) seeds playout value estimates; a learned evaluator may replace it later without changing the search.

## Consequences

- Determinism is preserved: the same seed and the same game state yield the same search tree, which is the property the whole platform is built on.
- Search quality depends on playout cost; the rules engine must expose a fast "resolve one activation" path.
- Hidden information is approximated by sampling opponent states; this is a known weakness and the first thing to revisit if the engine is ever built.
