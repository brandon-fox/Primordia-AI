"""
DuckDB schema and persistence for OpeningBook.

Provides storage for:
- Historical games indexed by faction matchup
- Army list hashes for similarity queries
- Win/loss statistics
"""

from datetime import datetime
from pathlib import Path
from typing import Optional, TYPE_CHECKING

from pydantic import BaseModel, Field, field_validator, computed_field

try:
    import duckdb
    HAS_DUCKDB = True
except ImportError:
    HAS_DUCKDB = False
    duckdb = None  # type: ignore

if TYPE_CHECKING:
    from primordia.models import GameState


class HistoricalGameResult(BaseModel):
    """A historical game result from the database.
    
    This model represents a single game record with full validation.
    The winner field is constrained to be either 1 or 2.
    """
    
    id: str
    player1_faction: str
    player2_faction: str
    player1_list_hash: str
    player2_list_hash: str
    winner: int = Field(..., ge=1, le=2, description="Winner must be 1 or 2")
    player1_vp: int = 0
    player2_vp: int = 0
    turn_count: int = 5
    game_date: Optional[datetime] = None
    source: str = "user"
    
    @field_validator("winner")
    @classmethod
    def validate_winner(cls, v: int) -> int:
        """Ensure winner is exactly 1 or 2."""
        if v not in (1, 2):
            raise ValueError("winner must be 1 or 2")
        return v
    
    @computed_field
    @property
    def player1_won(self) -> bool:
        """Check if player 1 won the game."""
        return self.winner == 1
    
    @computed_field
    @property
    def vp_differential(self) -> int:
        """Calculate VP differential (positive = player 1 advantage)."""
        return self.player1_vp - self.player2_vp


class FactionStatistics(BaseModel):
    """Aggregate statistics for a faction matchup.
    
    This model represents win/loss statistics for a specific
    faction vs opponent combination.
    """
    
    faction: str
    opponent: str
    games: int = 0
    wins: int = 0
    losses: int = 0
    avg_vp_scored: float = 0.0
    avg_vp_conceded: float = 0.0
    
    @computed_field
    @property
    def win_rate(self) -> float:
        """Calculate win rate (0.0 to 1.0)."""
        if self.games == 0:
            return 0.0
        return self.wins / self.games


# Default database path
DEFAULT_DB_PATH = Path.home() / ".primordia" / "opening_book.duckdb"


SCHEMA_SQL = """
-- Historical games table
CREATE TABLE IF NOT EXISTS historical_games (
    id VARCHAR PRIMARY KEY,
    
    -- Factions
    player1_faction VARCHAR NOT NULL,
    player2_faction VARCHAR NOT NULL,
    
    -- Army list hashes (for similarity matching)
    player1_list_hash VARCHAR NOT NULL,
    player2_list_hash VARCHAR NOT NULL,
    
    -- Result
    winner INTEGER NOT NULL CHECK (winner IN (1, 2)),
    
    -- Final scores
    player1_vp INTEGER DEFAULT 0,
    player2_vp INTEGER DEFAULT 0,
    
    -- Metadata
    turn_count INTEGER DEFAULT 5,
    game_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    source VARCHAR DEFAULT 'user'
);

-- Index for faction matchup queries
CREATE INDEX IF NOT EXISTS idx_faction_matchup 
ON historical_games(player1_faction, player2_faction);

-- Index for list similarity queries
CREATE INDEX IF NOT EXISTS idx_list_hash 
ON historical_games(player1_list_hash, player2_list_hash);


-- Deployment patterns table
CREATE TABLE IF NOT EXISTS deployment_patterns (
    id VARCHAR PRIMARY KEY,
    
    -- Pattern identification
    player_faction VARCHAR NOT NULL,
    opponent_faction VARCHAR NOT NULL,
    pattern_name VARCHAR NOT NULL,
    
    -- Pattern data (JSON)
    deployment_zones JSON NOT NULL,
    description VARCHAR,
    
    -- Statistics
    games_used INTEGER DEFAULT 0,
    wins INTEGER DEFAULT 0
);

-- Index for pattern lookup
CREATE INDEX IF NOT EXISTS idx_pattern_matchup 
ON deployment_patterns(player_faction, opponent_faction);


-- Faction statistics view
CREATE VIEW IF NOT EXISTS faction_stats AS
SELECT 
    player1_faction AS faction,
    player2_faction AS opponent,
    COUNT(*) AS games,
    SUM(CASE WHEN winner = 1 THEN 1 ELSE 0 END) AS wins,
    SUM(CASE WHEN winner = 2 THEN 1 ELSE 0 END) AS losses,
    AVG(player1_vp) AS avg_vp_scored,
    AVG(player2_vp) AS avg_vp_conceded
FROM historical_games
GROUP BY player1_faction, player2_faction;
"""


class OpeningBookDB:
    """
    DuckDB-backed storage for the opening book.
    
    Features:
    - Historical game indexing
    - Faction matchup statistics
    - Deployment pattern storage
    
    Example:
        db = OpeningBookDB()
        await db.connect()
        games = await db.query_matchup("Space Marines", "Orks")
    """
    
    def __init__(self, db_path: Optional[Path] = None) -> None:
        """
        Initialize the database.
        
        Args:
            db_path: Path to DuckDB file. Defaults to ~/.primordia/opening_book.duckdb
        """
        self.db_path = db_path or DEFAULT_DB_PATH
        self._conn: Optional["duckdb.DuckDBPyConnection"] = None
    
    async def connect(self) -> None:
        """Connect to database and ensure schema exists."""
        if not HAS_DUCKDB:
            raise ImportError(
                "DuckDB not installed. Install with: pip install duckdb"
            )
        
        # Ensure directory exists
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Connect (DuckDB is sync but we simulate async interface)
        self._conn = duckdb.connect(str(self.db_path))
        
        # Create schema (execute as a script)
        self._conn.execute(SCHEMA_SQL)
    
    async def close(self) -> None:
        """Close database connection."""
        if self._conn:
            self._conn.close()
            self._conn = None
    
    async def index_game(
        self,
        game_id: str,
        player1_faction: str,
        player2_faction: str,
        player1_list_hash: str,
        player2_list_hash: str,
        winner: int,
        player1_vp: int = 0,
        player2_vp: int = 0,
        turn_count: int = 5
    ) -> None:
        """Index a completed game."""
        if not self._conn:
            raise RuntimeError("Database not connected")
        
        self._conn.execute("""
            INSERT OR REPLACE INTO historical_games 
            (id, player1_faction, player2_faction, player1_list_hash, 
             player2_list_hash, winner, player1_vp, player2_vp, turn_count)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, [
            game_id, player1_faction, player2_faction,
            player1_list_hash, player2_list_hash,
            winner, player1_vp, player2_vp, turn_count
        ])
    
    async def query_matchup(
        self,
        player_faction: str,
        opponent_faction: str,
        limit: int = 10
    ) -> list[HistoricalGameResult]:
        """Query historical games for a matchup.
        
        Returns:
            List of HistoricalGameResult models with full validation.
        """
        if not self._conn:
            raise RuntimeError("Database not connected")
        
        result = self._conn.execute("""
            SELECT * FROM historical_games
            WHERE player1_faction = ? AND player2_faction = ?
            ORDER BY game_date DESC
            LIMIT ?
        """, [player_faction, opponent_faction, limit])
        
        columns = [desc[0] for desc in result.description]
        return [
            HistoricalGameResult(**dict(zip(columns, row)))
            for row in result.fetchall()
        ]
    
    async def get_matchup_stats(
        self,
        player_faction: str,
        opponent_faction: str
    ) -> Optional[FactionStatistics]:
        """Get win/loss statistics for a matchup.
        
        Returns:
            FactionStatistics model with computed win_rate, or None if not found.
        """
        if not self._conn:
            raise RuntimeError("Database not connected")
        
        result = self._conn.execute("""
            SELECT * FROM faction_stats
            WHERE faction = ? AND opponent = ?
        """, [player_faction, opponent_faction])
        
        row = result.fetchone()
        if row:
            columns = [desc[0] for desc in result.description]
            return FactionStatistics(**dict(zip(columns, row)))
        return None
    
    def __enter__(self) -> "OpeningBookDB":
        return self
    
    def __exit__(self, *args) -> None:
        if self._conn:
            self._conn.close()
