"""
Position evaluation models and heuristic evaluator for Primordia-AI.

Defines the interface for heuristic position evaluation per Issue #2.
"""

import math
from enum import Enum
from typing import TYPE_CHECKING

from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from primordia.models import GameState


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
    reasoning: str | None = None


class PositionEvaluation(BaseModel):
    """
    Heuristic evaluation of a game position.

    Scores are normalized to range [-1.0, +1.0]:
    - +1.0 = Decisive advantage for player 1
    - 0.0 = Equal position
    - -1.0 = Decisive advantage for player 2
    """

    player_advantage: float = Field(default=0.0, ge=-1.0, le=1.0)
    overall_score: float = Field(default=0.0, ge=-1.0, le=1.0)
    win_probability: float = Field(default=0.5, ge=0.0, le=1.0)
    key_factors: list[str] = Field(default_factory=list)
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)
    factor_scores: list[FactorScore] = Field(default_factory=list)
    reasoning: str | None = None
    material_score: float = 0.0
    position_score: float = 0.0
    tempo_score: float = 0.0
    vp_score: float = 0.0

    def model_post_init(self, __context: object, /) -> None:
        if self.overall_score == 0.0 and self.player_advantage != 0.0:
            self.overall_score = self.player_advantage
        elif self.player_advantage == 0.0 and self.overall_score != 0.0:
            self.player_advantage = self.overall_score

    def is_winning(self, threshold: float = 0.3) -> bool:
        """Check if position is winning for player 1."""
        return self.overall_score >= threshold

    def is_losing(self, threshold: float = 0.3) -> bool:
        """Check if position is losing for player 1."""
        return self.overall_score <= -threshold

    def explain(self) -> str:
        """Generate human-readable explanation."""
        if self.player_advantage > 0.3:
            advantage = "Player 1 has a significant advantage"
        elif self.player_advantage > 0.1:
            advantage = "Player 1 has a slight advantage"
        elif self.player_advantage < -0.3:
            advantage = "Player 2 has a significant advantage"
        elif self.player_advantage < -0.1:
            advantage = "Player 2 has a slight advantage"
        else:
            advantage = "The position is roughly equal"

        factors = (
            ", ".join(self.key_factors) if self.key_factors else "No specific factors"
        )
        return (
            f"{advantage}. Key factors: {factors}. "
            f"Win probability: {self.win_probability:.0%}"
        )


class HeuristicEvaluator:
    """Heuristic-based position evaluator."""

    def evaluate(self, state: "GameState") -> PositionEvaluation:
        """Evaluate a game position."""
        key_factors: list[str] = []

        p1_points = sum(u.points_cost for u in state.player1_units if u.is_alive)
        p2_points = sum(u.points_cost for u in state.player2_units if u.is_alive)

        total_points = p1_points + p2_points
        material_score = (
            (p1_points - p2_points) / total_points if total_points > 0 else 0.0
        )

        if abs(material_score) > 0.1:
            winner = "Player 1" if material_score > 0 else "Player 2"
            key_factors.append(f"{winner} has more material")

        vp_diff = state.player1_vp - state.player2_vp
        max_vp = max(state.player1_vp + state.player2_vp, 1)
        vp_score = vp_diff / max_vp if max_vp > 0 else 0.0

        if abs(vp_diff) >= 5:
            winner = "Player 1" if vp_diff > 0 else "Player 2"
            key_factors.append(f"{winner} leads on VP")

        player_advantage = (material_score * 0.4) + (vp_score * 0.6)
        player_advantage = max(-1.0, min(1.0, player_advantage))
        win_probability = 1 / (1 + math.exp(-player_advantage * 3))
        confidence = min(0.3 + (state.turn_number * 0.1), 0.9)

        return PositionEvaluation(
            player_advantage=player_advantage,
            overall_score=player_advantage,
            win_probability=win_probability,
            key_factors=key_factors,
            confidence=confidence,
            material_score=material_score,
            vp_score=vp_score,
        )
