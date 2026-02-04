# Primordia AI

> **The Stockfish of Warhammer** — Deterministic tactical engine for optimal play and machine learning

[![Priority: #3](https://img.shields.io/badge/Priority-%233-orange)]()
[![Status: Pre-Alpha](https://img.shields.io/badge/Status-Pre--Alpha-lightgrey)]()

## Vision

**Primordia AI** is a tactical engine that calculates optimal plays, predicts game outcomes, and learns from structured match data. It is the **primary consumer** of WARScribe transcripts.

### Positioning

| Aspect | Meta-Oracle | Primordia AI |
|--------|-------------|--------------| 
| **Role** | Observer | Player |
| **Focus** | Meta analysis | Tactical execution |
| **Output** | Tier lists, upsets | Optimal moves, win probability |
| **Analogy** | Sports commentator | Chess engine |

> *"Meta-Oracle tells you what's strong in the meta. Primordia tells you the best move right now."*

## Core Capabilities

1. **Position Evaluation** — Given a game state, calculate who's winning
2. **Best Move Calculation** — Given a position, find the optimal play
3. **Game Outcome Prediction** — Before/during a game, predict the winner
4. **Opening Book Database** — Standard deployments for each faction matchup
5. **Training Pipeline** — Learn from historical WARScribe transcripts

## Key Stakeholders

| Stakeholder | Value |
|-------------|-------|
| **Competitive Players** | Calculate optimal plays during practice |
| **Tournament Organizers** | Fair AI opponent for byes |
| **Content Creators** | "AI Analysis" overlays for streams |
| **Opening Book Users** | "Book" setups for each matchup |
| **Meta-Oracle** | Game analysis feeds meta predictions |

## Technology Stack

- **Language**: Python (typed)
- **ML Framework**: PyTorch or JAX
- **Search**: Monte Carlo Tree Search (MCTS)
- **Rules Engine**: WARScribe-Core
- **Storage**: DuckDB for game database

## Getting Started

```bash
# Coming soon - Pre-alpha development
pip install primordia-ai

# Evaluate a position
primordia eval game_state.json

# Get best move
primordia move game_state.json
```

## Dependencies

- **WARScribe-Core** — Structured game notation
- **Agent-Auditor-SDK** — Token quota management

## Roadmap

See [ROADMAP.md](./ROADMAP.md) for detailed milestones.

| Phase | Target | Status |
|-------|--------|--------|
| v0.1.0 | Foundation | 🔲 Planned |
| v0.1.5 | Opening Book | 🔲 Planned |
| v0.2.0 | Search Engine | 🔲 Planned |
| v0.3.0 | Learning Pipeline | 🔲 Planned |
| v1.0.0 | Production | 🔲 Planned |

## License

MIT License

---

*Part of the Vindicta Platform*
