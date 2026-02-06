"""
Pydantic models for OpeningBookDB return types.

Typed return models per Issue #7.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, validator


class HistoricalGameResult(BaseModel):
    """Result from a historical game lookup."""
    game_id: str
    player1_faction: str
    player2_faction: str
    winner: int = Field(..., ge=1, le=2, description="1 or 2")
    score_differential: int
    turn_count: int
    date_played: Optional[datetime] = None
    
    @validator('winner')
    def validate_winner(cls, v):
        if v not in (1, 2):
            raise ValueError('winner must be 1 or 2')
        return v


class DeploymentPattern(BaseModel):
    """Common deployment pattern from historical data."""
    pattern_id: str
    faction: str
    description: str
    frequency: float = Field(..., ge=0.0, le=1.0)
    win_rate: float = Field(..., ge=0.0, le=1.0)
    sample_size: int


class FactionStatistics(BaseModel):
    """Aggregate statistics for a faction matchup."""
    player_faction: str
    opponent_faction: str
    total_games: int
    wins: int
    losses: int
    
    @property
    def win_rate(self) -> float:
        """Calculate win rate."""
        if self.total_games == 0:
            return 0.0
        return self.wins / self.total_games
