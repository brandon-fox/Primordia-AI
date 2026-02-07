"""
Position evaluation models for Primordia-AI.

Defines the interface for heuristic position evaluation per Issue #2.
"""

from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class EvaluationFactor(str, Enum):
    """Factors used in position evaluation."""
    BOARD_CONTROL = "board_control"
    OBJECTIVE_CONTROL = "objective_control"
    UNIT_PRESERVATION = "unit_preservation"
    THREAT_PROJECTION = "threat_projection"
    MOBILITY = "mobility"
    SYNERGY = "synergy"


class FactorScore(BaseModel):
    """Score for a single evaluation factor."""
    factor: EvaluationFactor
    score: float = Field(..., ge=-1.0, le=1.0, description="Normalized score")
    weight: float = Field(default=1.0, ge=0.0, description="Factor weight")
    reasoning: Optional[str] = None


class PositionEvaluation(BaseModel):
    """
    Heuristic evaluation of a game position.
    
    Scores are normalized to range [-1.0, +1.0]:
    - +1.0 = Decisive advantage for player 1
    - 0.0 = Equal position
    - -1.0 = Decisive advantage for player 2
    """
    overall_score: float = Field(..., ge=-1.0, le=1.0)
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)
    factor_scores: list[FactorScore] = Field(default_factory=list)
    reasoning: Optional[str] = None
    
    def is_winning(self, threshold: float = 0.3) -> bool:
        """Check if position is winning for player 1."""
        return self.overall_score >= threshold
    
    def is_losing(self, threshold: float = 0.3) -> bool:
        """Check if position is losing for player 1."""
        return self.overall_score <= -threshold
