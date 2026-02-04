"""
Primordia: The Stockfish of Warhammer.

A deterministic tactical AI engine for tabletop wargaming.
"""

from primordia.evaluation import PositionEvaluation
from primordia.models import GameState, Move, MoveRecommendation, Unit

__version__ = "0.1.0"

__all__ = [
    "GameState",
    "Move",
    "MoveRecommendation",
    "PositionEvaluation",
    "Unit",
]
