"""
OpeningBook: Database of opening setups and historical games.

Provides deployment recommendations based on faction matchups
and similar army lists.
"""

from typing import Optional, TYPE_CHECKING

from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from primordia.models import GameState


class DeploymentRecommendation(BaseModel):
    """Recommended deployment setup."""
    
    # Setup description
    name: str
    description: str
    
    # Zones/positions
    deployment_zones: dict[str, str] = Field(default_factory=dict)  # unit_name -> zone
    
    # Confidence
    confidence: float = Field(ge=0.0, le=1.0, default=0.5)
    
    # Source
    based_on_games: int = 0
    win_rate: float = 0.0


class HistoricalGame(BaseModel):
    """A historical game from the database."""
    
    id: str
    player1_faction: str
    player2_faction: str
    winner: int = Field(ge=1, le=2, description="Winner must be player 1 or 2")
    
    # Lists (simplified)
    player1_list_hash: str
    player2_list_hash: str
    
    # Similarity to query
    similarity_score: float = 0.0


class FactionStatistics(BaseModel):
    """Aggregated statistics for a faction matchup."""
    
    player_faction: str
    opponent_faction: str
    
    # Win rates
    total_games: int = Field(ge=0)
    wins: int = Field(ge=0)
    losses: int = Field(ge=0)
    win_rate: float = Field(ge=0.0, le=1.0)
    
    # Deployment patterns
    most_common_deployment: Optional[str] = None
    avg_deployment_confidence: float = Field(ge=0.0, le=1.0, default=0.5)
    
    # Last updated
    last_game_indexed: Optional[str] = None  # ISO 8601 timestamp


class OpeningBook:
    """
    Database of opening setups.
    
    Provides deployment recommendations based on:
    - Faction matchups
    - Similar army lists
    - Historical game outcomes
    
    Note: This is a stub for v0.1.0. Will be backed by DuckDB in v0.1.5.
    """
    
    async def get_book_setup(
        self,
        player_faction: str,
        player_list_hash: str,
        opponent_faction: str
    ) -> Optional[DeploymentRecommendation]:
        """
        Get recommended deployment setup.
        
        Args:
            player_faction: The player's faction.
            player_list_hash: Hash of the player's army list.
            opponent_faction: The opponent's faction.
            
        Returns:
            DeploymentRecommendation if found, None otherwise.
        """
        # Stub for v0.1.0 - returns generic advice
        return DeploymentRecommendation(
            name="Standard Deployment",
            description=f"Generic deployment for {player_faction} vs {opponent_faction}",
            deployment_zones={},
            confidence=0.3,
            based_on_games=0,
            win_rate=0.5
        )
    
    async def get_historical_games(
        self,
        player_faction: str,
        player_list_hash: Optional[str] = None,
        opponent_faction: Optional[str] = None,
        limit: int = 10
    ) -> list[HistoricalGame]:
        """
        Find similar historical games.
        
        Args:
            player_faction: The player's faction.
            player_list_hash: Optional hash for list similarity.
            opponent_faction: Optional opponent filter.
            limit: Maximum games to return.
            
        Returns:
            List of similar historical games.
        """
        # Stub for v0.1.0 - returns empty list
        return []
    
    async def index_game(self, game_state: "GameState", winner: int) -> None:
        """
        Index a completed game for future reference.
        
        Args:
            game_state: The final game state.
            winner: Which player won (1 or 2).
        """
        # Stub for v0.1.0 - no-op
        pass
