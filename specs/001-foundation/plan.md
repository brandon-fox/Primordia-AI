# Implementation Plan: Foundation (v0.1.0)

**Spec Reference:** [spec.md](./spec.md)

---

## Proposed Changes

```
src/primordia_ai/
├── __init__.py          # PrimordiaEngine re-export
├── encoding/
│   ├── __init__.py
│   └── state_encoder.py # StateEncoder: GameState → numpy
├── evaluation/
│   ├── __init__.py
│   ├── evaluator.py     # Evaluator with configurable weights
│   └── config.py        # EvaluationConfig model
├── generation/
│   ├── __init__.py
│   └── move_generator.py # Phase-aware action generation
└── engine/
    ├── __init__.py
    └── primordia.py     # PrimordiaEngine: recommend()
```

### Tests

```
tests/
├── test_encoding.py       # Determinism, hashability
├── test_evaluation.py     # Score ranges, weight sensitivity
├── test_move_generation.py # Phase constraints, pass action
├── test_engine.py         # Full recommend pipeline
└── fixtures/              # Sample GameState objects
```

---

## Verification

```powershell
uv run pytest tests/ -v
uv run mypy src/primordia_ai/ --strict
uv run python -c "
import time
from primordia_ai import PrimordiaEngine
engine = PrimordiaEngine()
# ... create sample game state ...
# benchmark evaluation speed
"
```
