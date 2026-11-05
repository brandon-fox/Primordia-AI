# Primordia AI

> **Status:** design study with a foundation module; implementation unscheduled. The game-state encoding, data models, opening-book store and a heuristic evaluator exist with tests (about 770 lines of typed Python, February 2026). Search, outcome prediction and the learning pipeline were designed but never built. Kept public as a record of how the system was thought through.

Primordia was designed as the tactical engine for the [Vindicta Platform](https://github.com/vindicta-platform): given a tabletop wargame state, evaluate who is winning, find the best move, and learn from recorded battles. The analogy that drove the design is a chess engine, with [WARScribe](https://github.com/vindicta-platform/specs/tree/main/015-warscribe-core-notation) transcripts as the game record.

## Positioning (as designed)

| Aspect | Meta-Oracle | Primordia AI |
|--------|-------------|--------------|
| Role | Observer | Player |
| Focus | Meta analysis | Tactical execution |
| Output | Tier lists, upsets | Optimal moves, win probability |
| Analogy | Sports commentator | Chess engine |

> "Meta-Oracle tells you what's strong in the meta. Primordia tells you the best move right now."

## What exists

| Module | Lines | What it does | Tests |
| --- | --- | --- | --- |
| `src/primordia/encoding.py` | 184 | Encodes a `GameState` into a fixed-width feature vector for evaluation and search. | `tests/test_encoding.py` |
| `src/primordia/models.py` | 136 | Pydantic models for positions, moves and evaluations. | `tests/test_models.py` |
| `src/primordia/database.py` | 226 | DuckDB-backed store for positions and opening-book entries. | `tests/test_database.py` |
| `src/primordia/opening_book.py`, `opening_models.py` | 172 | Opening-book lookup and its models. | — |
| `src/primordia/evaluation.py` | 42 | Heuristic position evaluation interface. | — |

## What was designed and not built

| Capability | Design | Status |
| --- | --- | --- |
| Position evaluation | [spec 001-foundation](specs/001-foundation/spec.md); [vindicta-platform/specs 045](https://github.com/vindicta-platform/specs/tree/main/045-positional-heuristics) | heuristic interface only |
| Best-move search | Monte Carlo tree search over the rules engine; [vindicta-platform/specs 044](https://github.com/vindicta-platform/specs/tree/main/044-mcts-foundation); [ADR-0001](docs/adr/0001-mcts-for-best-move-search.md) | not started |
| Roster synergy and outcome prediction | [vindicta-platform/specs 046](https://github.com/vindicta-platform/specs/tree/main/046-roster-synergy), [047](https://github.com/vindicta-platform/specs/tree/main/047-upset-detector) | not started |
| Game database | DuckDB; [ADR-0002](docs/adr/0002-duckdb-for-the-game-database.md) | store implemented, no ingestion |
| Rules boundary | WARScribe-Core as the only source of legal moves; [ADR-0003](docs/adr/0003-warscribe-core-as-the-rules-boundary.md) | boundary defined, engine incomplete |

The February 2026 six-week schedule in [`ROADMAP.md`](ROADMAP.md) is kept as a historical document; none of its milestones past the foundation shipped.

## Running what exists

```bash
uv sync --extra dev
uv run pytest
```

There is no CLI and no package on PyPI.

## License and author

MIT License, copyright Brandon Fox. See [`LICENSE`](LICENSE).

## Independence

This is a personal project by Brandon Fox, built on my own time and equipment. It is not affiliated with, endorsed by, or derived from the work of any employer, current or former, and does not represent their views, products or practices. Licensed under the MIT License; principles at [First-ADE/PRINCIPLES.md](https://github.com/First-ADE/.github/blob/main/PRINCIPLES.md).
