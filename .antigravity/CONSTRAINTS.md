# Primordia-AI Constraints

> Critical rules agents MUST follow when modifying this repository.

## ⛔ Hard Constraints

1. **Deterministic by Default** - Same input must produce same output
2. **No External AI Calls** - Pure heuristic evaluation only
3. **NumPy for Tensors** - No custom matrix implementations
4. **Edition-Agnostic Core** - Edition specifics via configuration

## 📊 Evaluation Rules

### Heuristic Invariants
- All scores normalized to 0.0-1.0 range
- Weights must sum to 1.0
- Negative scores forbidden
- NaN/Inf must be handled to 0.0

### Position Encoding
```python
# Tensor shape requirements
BOARD_SHAPE = (24, 24, 8)  # x, y, channels
UNIT_EMBEDDING_DIM = 64
MAX_UNITS_PER_SIDE = 50
```

### Opening Book Format
```python
{
    "position_hash": str,  # SHA-256 of encoded state
    "match_count": int,
    "win_rate": float,
    "avg_turns": float
}
```

## ⚠️ Performance Requirements

- Single position eval: < 50ms
- Batch eval (100 positions): < 1s
- Memory per position: < 10MB
- Opening book lookup: < 5ms

## 🔒 Data Integrity

- Opening book is read-only at runtime
- Position hashes must be collision-resistant
- No mutable global state allowed

## 🧪 Testing Requirements

Before merging:
- [ ] `pytest` passes
- [ ] Property-based tests pass (Hypothesis)
- [ ] Performance benchmarks within bounds
- [ ] Determinism tests pass (same input → same output)
