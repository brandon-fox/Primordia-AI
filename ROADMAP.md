# Primordia AI Roadmap

> **Vision**: The Stockfish of Warhammer — deterministic tactical engine  
> **Status**: Pre-Alpha  
> **Last Updated**: 2026-02-05

---

## 📅 6-Week Schedule (Feb 4 - Mar 17, 2026)

> **GitHub Project**: https://github.com/orgs/vindicta-platform/projects/4  
> **Master Roadmap**: https://github.com/vindicta-platform/.github/blob/master/ROADMAP.md

### Week 1: Feb 4-10 — Heuristic Evaluation ✅
| Day | Task | Priority | Status |
|-----|------|----------|--------|
| Mon 4 | Define heuristic evaluation interface | P1 | ✅ PR #5 |
| Tue 5 | Continue heuristic evaluation | P1 | ✅ PR #5 |
| Wed 6 | Opening book database design | P1 | ✅ Issue #3 |
| Thu 7 | DuckDB setup for opening book | P1 | ✅ PR #6 |

**Status**: 100% complete! Opening book database schema implemented and merged.

### Week 2: Feb 11-17 — State Encoding
| Day | Task | Priority |
|-----|------|----------|
| Mon 11 | Opening book data population | P1 |
| Tue 12 | Opening book data population | P1 |
| Wed 13 | State encoding implementation | P1 |
| Thu 14 | Evaluation functions | P1 |
| **Sun 17** | **v0.1.0 Foundation Release** | ⭐ |

### Week 3: Feb 18-24 — Opening Book
| Day | Task | Priority |
|-----|------|----------|
| Mon 18 | Opening book database implementation | P1 |
| Tue 19 | Faction analysis features | P1 |
| Wed 20 | Recommendation API | P1 |
| **Sun 24** | **v0.1.5 Opening Book Release** | ⭐ |

### Week 4: Feb 25 - Mar 3 — MCTS Foundation
| Day | Task | Priority |
|-----|------|----------|
| Mon 25 | MCTS foundation (part 1) | P1 |
| Tue 26 | MCTS foundation (part 2) | P1 |
| Wed 27 | Search depth implementation | P1 |
| Thu 28 | Evaluation improvements | P1 |

### Week 5: Mar 4-10 — MCTS Polish
| Day | Task | Priority |
|-----|------|----------|
| Mon 4 | MCTS polish | P1 |
| Tue 5 | Move depth 3+ | P1 |
| Wed 6 | Performance optimization | P1 |
| Thu 7 | Tests | P1 |
| **Sun 10** | **v0.2.0 Search Engine Release** | ⭐ |

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
- [x] Heuristic evaluation interface defined
- [x] Opening book database schema (DuckDB)
- [x] Faction matchup queries
- [x] Historical game storage
- [ ] Opening book data population (Week 2)
- [ ] State encoding implementation (Week 2)

### Key Measurable Results
| Metric | Target | Status |
|--------|--------|--------|
| **Opening Book Schema** | Complete with matchup queries | ✅ Complete |
| **Test Coverage** | ≥80% | ⚠️ Pending (Week 2) |
| **Type Safety** | Pydantic models for all return types | ⚠️ Issue #7 |

### Exit Criteria
- [x] DuckDB schema deployed
- [x] Faction matchup indexing functional
- [ ] Pydantic return types (Issue #7 - Week 2)
- [ ] Unit tests for opening book

**Status**: 50% complete for v0.1.0. Week 1 deliverables complete, Week 2 items on track.

---

*Last Updated: 2026-02-05*
