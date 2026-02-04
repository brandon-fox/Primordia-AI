# Primordia AI Roadmap

> **Vision**: The Stockfish of Warhammer — deterministic tactical engine  
> **Status**: Pre-Alpha  
> **Last Updated**: 2026-02-03

---

## v1.0 Target: June 2026

### Mission Statement
Deliver a production-ready tactical AI engine that evaluates game positions, calculates optimal moves, and learns from WARScribe transcripts — becoming the "Stockfish" of Warhammer.

---

## Milestone Timeline

```
┌─────────────────────────────────────────────────────────────────┐
│  Feb 2026          Mar 2026          Apr 2026         Jun 2026  │
│  ─────────────────────────────────────────────────────────────  │
│  [v0.1.0] [v0.1.5] [v0.2.0]          [v0.3.0]         [v1.0.0]  │
│  Foundation Book   Search            Learning          Prod     │
│                                                                  │
│  Week 2-3  Week 4  Week 5-6          Week 7-10        Week 12+  │
└─────────────────────────────────────────────────────────────────┘
```

---

## v0.1.0 — Foundation (Target: Feb 17, 2026)

### Deliverables
- [ ] Define game state representation
- [ ] Implement position encoding
- [ ] Basic evaluation heuristics (no ML)
- [ ] Integration with WARScribe-Core
- [ ] Action space definition
- [ ] Unit capability modeling

### Key Measurable Results
| Metric | Target | Measurement |
|--------|--------|-------------|
| **Position Encoding** | Encodes all unit types | Unit tests |
| **Heuristic Evaluation** | Correlates with win rate | Historical data |
| **WARScribe Integration** | Parse any valid transcript | Integration test |

### Exit Criteria
- [ ] Evaluate a game position with heuristic scoring
- [ ] Output who's ahead and why
- [ ] Process WARScribe transcripts

---

## v0.1.5 — Opening Book Database (Target: Feb 24, 2026)

### Deliverables
- [ ] Define deployment recommendation schema
- [ ] Historical game storage (DuckDB)
- [ ] Faction archetype matching
- [ ] List similarity scoring
- [ ] "Book" setup recommendations

### Key Measurable Results
| Metric | Target | Measurement |
|--------|--------|-------------|
| **Faction Coverage** | All major factions | Database count |
| **Historical Games** | 100+ indexed | Database count |
| **Book Quality** | Recommended by experienced players | Manual review |

### Exit Criteria
- [ ] Given a list, return book setup vs each faction
- [ ] Surface historical games with similar lists
- [ ] API accessible from Logi-Slate-UI

---

## v0.2.0 — Search Engine (Target: Mar 10, 2026)

### Deliverables
- [ ] Monte Carlo Tree Search implementation
- [ ] Move generation from game state
- [ ] Basic policy (random → weighted)
- [ ] Depth-limited search
- [ ] Time-bounded search

### Key Measurable Results
| Metric | Target | Measurement |
|--------|--------|-------------|
| **Search Depth** | 3+ moves ahead | Benchmark |
| **Calculation Speed** | <10 seconds per move | Benchmark |
| **Move Quality** | Beats random baseline | Win rate test |

### Exit Criteria
- [ ] Calculate "best move" for a given position
- [ ] Complete search within 10 seconds
- [ ] Beat random play in simulation

---

## v0.3.0 — Learning Pipeline (Target: Apr 14, 2026)

### Deliverables
- [ ] Training pipeline from WARScribe transcripts
- [ ] Position evaluation network
- [ ] Policy network for move selection
- [ ] Self-play for improvement
- [ ] Model versioning

### Key Measurable Results
| Metric | Target | Measurement |
|--------|--------|-------------|
| **Training Data** | 1000+ games | Dataset size |
| **Eval Improvement** | 20%+ over heuristic | Comparison test |
| **Self-Play Cycles** | 100+ games | Training logs |

### Exit Criteria
- [ ] Train on 1000+ games
- [ ] Beat heuristic-only version
- [ ] Model improves with more data

---

## v1.0.0 — Production Release (Target: June 1, 2026)

### Deliverables
- [ ] API server for inference
- [ ] Logi-Slate-UI integration
- [ ] Stream overlay component
- [ ] Performance optimization
- [ ] Documentation and tutorials

### Key Measurable Results
| Metric | Target | Measurement |
|--------|--------|-------------|
| **Calculation Speed** | <1 second per move | Benchmark |
| **API Uptime** | 99%+ | Monitoring |
| **Community Testing** | 50+ beta testers | Sign-ups |
| **Model Accuracy** | Correlates with human experts | Expert review |

### Exit Criteria
- [ ] <1 second move calculation
- [ ] Playable via Logi-Slate
- [ ] Stream overlay functional
- [ ] No critical bugs for 2 weeks

---

## Core Components

### Position Evaluation

```python
class PositionEvaluation:
    player_advantage: float  # -1.0 to +1.0
    win_probability: float   # 0.0 to 1.0
    key_factors: list[str]   # Why this evaluation
    confidence: float        # How certain
```

### Opening Book

```python
class OpeningBook:
    async def get_book_setup(
        player_list: WARScribeList,
        opponent_faction: str
    ) -> DeploymentRecommendation
    
    async def get_historical_games(
        player_list: WARScribeList,
        opponent_list: WARScribeList | None
    ) -> list[HistoricalGame]
```

---

## Technical Challenges

| Challenge | Approach |
|-----------|----------|
| **Hidden Information** | Model opponent decisions probabilistically |
| **Dice Variance** | Model distributions, not outcomes |
| **Large Action Space** | Hierarchical search (phase → unit → action) |
| **State Complexity** | Neural network feature extraction |

---

## Dependencies

| Dependency | Status | Notes |
|------------|--------|-------|
| WARScribe-Core | 🔄 Parallel | Game notation |
| Agent-Auditor-SDK | 🔄 Parallel | LLM quota (optional) |
| DuckDB | ✅ Available | Game database |
| PyTorch/JAX | ✅ Available | ML framework |

---

## Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Warhammer too complex | Medium | High | Start with simplified scenarios |
| Insufficient training data | High | High | Prioritize WARScribe adoption |
| Dice variance too high | Medium | Medium | Model distributions |
| Community rejects AI play | Medium | Medium | Position as training tool |

---

## Success Criteria for v1

1. **Intelligence**: Beats random play convincingly
2. **Speed**: Sub-second move calculation
3. **Opening Book**: Coverage for all major factions
4. **Adoption**: 50+ beta testers actively using

---

*Maintained by: Vindicta Platform Team*
