"""
Position evaluation module.

Provides heuristic-based evaluation of game positions,
determining which player has the advantage.
"""

from dataclasses import dataclass, field
from typing import TYPE_CHECKING
import math

from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from primordia.models import GameState


class PositionEvaluation(BaseModel):
    """
    Evaluation of a game position.
    
    Based on the ROADMAP specification:
    - player_advantage: -1.0 to +1.0 (negative = player 2 ahead)
    - win_probability: 0.0 to 1.0
    - key_factors: Why this evaluation
    - confidence: How certain
    """
    
    player_advantage: float = Field(ge=-1.0, le=1.0)  # -1.0 to +1.0
    win_probability: float = Field(ge=0.0, le=1.0)    # 0.0 to 1.0
    key_factors: list[str] = Field(default_factory=list)
    confidence: float = Field(ge=0.0, le=1.0, default=0.5)
    
    # Detailed breakdown
    material_score: float = 0.0  # Units/wounds comparison
    position_score: float = 0.0  # Board control
    tempo_score: float = 0.0     # Initiative/activations
    vp_score: float = 0.0        # Victory points
    
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
        
        factors = ", ".join(self.key_factors) if self.key_factors else "No specific factors"
        
        return f"{advantage}. Key factors: {factors}. Win probability: {self.win_probability:.0%}"


class HeuristicEvaluator:
    """
    Heuristic-based position evaluator.
    
    Uses hand-crafted rules for v0.1.0.
    Will be replaced by neural network in v0.3.0.
    """
    
    def evaluate(self, state: "GameState") -> PositionEvaluation:
        """
        Evaluate a game position.
        
        Args:
            state: The current game state.
            
        Returns:
            PositionEvaluation with scores and explanation.
        """
        key_factors = []
        
        # Material evaluation (wounds/points)
        p1_wounds = sum(u.wounds_current for u in state.player1_units if u.is_alive)
        p2_wounds = sum(u.wounds_current for u in state.player2_units if u.is_alive)
        
        p1_points = sum(u.points_cost for u in state.player1_units if u.is_alive)
        p2_points = sum(u.points_cost for u in state.player2_units if u.is_alive)
        
        total_points = p1_points + p2_points
        if total_points > 0:
            material_score = (p1_points - p2_points) / total_points
        else:
            material_score = 0.0
        
        if abs(material_score) > 0.1:
            winner = "Player 1" if material_score > 0 else "Player 2"
            key_factors.append(f"{winner} has more material")
        
        # VP evaluation
        vp_diff = state.player1_vp - state.player2_vp
        max_vp = max(state.player1_vp + state.player2_vp, 1)
        vp_score = vp_diff / max_vp if max_vp > 0 else 0.0
        
        if abs(vp_diff) >= 5:
            winner = "Player 1" if vp_diff > 0 else "Player 2"
            key_factors.append(f"{winner} leads on VP")
        
        # Combined advantage
        player_advantage = (material_score * 0.4) + (vp_score * 0.6)
        player_advantage = max(-1.0, min(1.0, player_advantage))
        
        # Win probability (sigmoid of advantage)
        win_probability = 1 / (1 + math.exp(-player_advantage * 3))
        
        # Confidence based on game stage
        confidence = 0.3 + (state.turn_number * 0.1)
        confidence = min(confidence, 0.9)
        
        return PositionEvaluation(
            player_advantage=player_advantage,
            win_probability=win_probability,
            key_factors=key_factors,
            confidence=confidence,
            material_score=material_score,
            vp_score=vp_score,
        )
