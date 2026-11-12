# ADR-0002: DuckDB for the game database

- Status: accepted (February 2026); implemented in `src/primordia/database.py`. Recorded 2026-11-05 as part of the design record.
- Deciders: Brandon Fox

## Context

The engine needs a local store for encoded positions, opening-book entries and, eventually, millions of playout records for training. Queries are analytical (aggregate over positions, join on encodings) rather than transactional. The platform's privacy stance prefers local files over a hosted database.

## Decision

Use DuckDB as an embedded, single-file analytical database. Position encodings are stored as fixed-width arrays; opening-book entries are keyed by matchup and encoded deployment. No server, no network dependency.

## Consequences

- Zero operational footprint and fast columnar scans for training-set assembly.
- Concurrency is single-writer; a future multi-process ingestion pipeline would need a queue in front of it.
- The schema lives in code (`database.py`) rather than migrations; acceptable at this size, revisit if the project is ever revived.
