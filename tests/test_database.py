"""
Unit tests for OpeningBookDB DuckDB storage.

Tests cover:
- Database initialization and schema
- Game indexing operations
- Matchup queries with Pydantic returns
- Statistics calculations
- Error handling
"""
import pytest
from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock, patch
import tempfile
import os

# Skip all tests if DuckDB not installed
pytest.importorskip("duckdb")

from primordia.database import OpeningBookDB, SCHEMA_SQL, HAS_DUCKDB
from primordia.opening_models import (
    HistoricalGameResult,
    DeploymentPattern,
    FactionStatistics,
)


# =============================================================================
# Fixtures
# =============================================================================

@pytest.fixture
def temp_db_path():
    """Create a temporary database path."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir) / "test_opening_book.duckdb"


@pytest.fixture
async def db(temp_db_path):
    """Create and connect to a test database."""
    database = OpeningBookDB(db_path=temp_db_path)
    await database.connect()
    yield database
    await database.close()


@pytest.fixture
def sample_game_data():
    """Sample game data for testing."""
    return {
        "game_id": "game-001",
        "player1_faction": "Space Marines",
        "player2_faction": "Orks",
        "player1_list_hash": "sm-hash-123",
        "player2_list_hash": "ork-hash-456",
        "winner": 1,
        "player1_vp": 85,
        "player2_vp": 70,
        "turn_count": 5,
    }


# =============================================================================
# Initialization Tests
# =============================================================================

class TestDatabaseInitialization:
    """Test database connection and schema setup."""

    @pytest.mark.asyncio
    async def test_connect_creates_database(self, temp_db_path):
        """connect() should create database file."""
        db = OpeningBookDB(db_path=temp_db_path)
        await db.connect()
        
        assert temp_db_path.exists()
        await db.close()

    @pytest.mark.asyncio
    async def test_connect_creates_parent_dirs(self, temp_db_path):
        """connect() should create parent directories."""
        nested_path = temp_db_path.parent / "nested" / "deep" / "db.duckdb"
        db = OpeningBookDB(db_path=nested_path)
        await db.connect()
        
        assert nested_path.parent.exists()
        await db.close()

    @pytest.mark.asyncio
    async def test_schema_creates_tables(self, db):
        """Schema should create required tables."""
        result = db._conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )
        tables = [row[0] for row in result.fetchall()]
        
        assert "historical_games" in tables
        assert "deployment_patterns" in tables

    @pytest.mark.asyncio
    async def test_close_disconnects(self, temp_db_path):
        """close() should disconnect from database."""
        database = OpeningBookDB(db_path=temp_db_path)
        await database.connect()
        await database.close()
        
        assert database._conn is None


# =============================================================================
# Index Game Tests
# =============================================================================

class TestIndexGame:
    """Test game indexing functionality."""

    @pytest.mark.asyncio
    async def test_index_game_inserts_record(self, db, sample_game_data):
        """index_game() should insert a game record."""
        await db.index_game(**sample_game_data)
        
        result = db._conn.execute(
            "SELECT COUNT(*) FROM historical_games"
        ).fetchone()
        assert result[0] == 1

    @pytest.mark.asyncio
    async def test_index_game_stores_all_fields(self, db, sample_game_data):
        """index_game() should store all provided fields."""
        await db.index_game(**sample_game_data)
        
        result = db._conn.execute(
            "SELECT * FROM historical_games WHERE id = ?",
            [sample_game_data["game_id"]]
        ).fetchone()
        
        assert result is not None
        # Check key fields (positions may vary)
        assert sample_game_data["player1_faction"] in str(result)
        assert sample_game_data["player2_faction"] in str(result)

    @pytest.mark.asyncio
    async def test_index_game_upserts(self, db, sample_game_data):
        """index_game() should update existing games."""
        await db.index_game(**sample_game_data)
        
        # Update with same ID
        sample_game_data["winner"] = 2
        await db.index_game(**sample_game_data)
        
        result = db._conn.execute(
            "SELECT COUNT(*) FROM historical_games"
        ).fetchone()
        assert result[0] == 1  # Still only one record

    @pytest.mark.asyncio
    async def test_index_game_requires_connection(self, temp_db_path, sample_game_data):
        """index_game() should raise if not connected."""
        db = OpeningBookDB(db_path=temp_db_path)
        
        with pytest.raises(RuntimeError, match="not connected"):
            await db.index_game(**sample_game_data)


# =============================================================================
# Query Matchup Tests
# =============================================================================

class TestQueryMatchup:
    """Test matchup query functionality."""

    @pytest.mark.asyncio
    async def test_query_matchup_returns_typed_models(self, db, sample_game_data):
        """query_matchup() should return HistoricalGameResult models."""
        await db.index_game(**sample_game_data)
        
        results = await db.query_matchup(
            player_faction="Space Marines",
            opponent_faction="Orks"
        )
        
        assert len(results) == 1
        assert isinstance(results[0], HistoricalGameResult)

    @pytest.mark.asyncio
    async def test_query_matchup_fields(self, db, sample_game_data):
        """query_matchup() results should have all fields."""
        await db.index_game(**sample_game_data)
        
        results = await db.query_matchup(
            player_faction="Space Marines",
            opponent_faction="Orks"
        )
        
        game = results[0]
        assert game.game_id == "game-001"
        assert game.player1_faction == "Space Marines"
        assert game.player2_faction == "Orks"
        assert game.winner == 1
        assert game.score_differential == 15  # 85 - 70

    @pytest.mark.asyncio
    async def test_query_matchup_empty(self, db):
        """query_matchup() should return empty list for no matches."""
        results = await db.query_matchup(
            player_faction="Necrons",
            opponent_faction="Tau"
        )
        
        assert results == []

    @pytest.mark.asyncio
    async def test_query_matchup_respects_limit(self, db):
        """query_matchup() should respect limit parameter."""
        # Insert 5 games
        for i in range(5):
            await db.index_game(
                game_id=f"game-{i}",
                player1_faction="Marines",
                player2_faction="Eldar",
                player1_list_hash=f"hash-{i}",
                player2_list_hash=f"hash-e-{i}",
                winner=1,
            )
        
        results = await db.query_matchup(
            player_faction="Marines",
            opponent_faction="Eldar",
            limit=3
        )
        
        assert len(results) == 3

    @pytest.mark.asyncio
    async def test_query_matchup_orders_by_date(self, db):
        """query_matchup() should return most recent first."""
        # Insert games (order matters for date)
        for i in range(3):
            await db.index_game(
                game_id=f"game-{i}",
                player1_faction="Marines",
                player2_faction="Tyranids",
                player1_list_hash=f"h{i}",
                player2_list_hash=f"t{i}",
                winner=1,
            )
        
        results = await db.query_matchup(
            player_faction="Marines",
            opponent_faction="Tyranids"
        )
        
        # Most recent should be game-2
        assert results[0].game_id == "game-2"


# =============================================================================
# Get Matchup Stats Tests
# =============================================================================

class TestGetMatchupStats:
    """Test faction statistics retrieval."""

    @pytest.mark.asyncio
    async def test_get_matchup_stats_returns_typed_model(self, db, sample_game_data):
        """get_matchup_stats() should return FactionStatistics."""
        await db.index_game(**sample_game_data)
        
        stats = await db.get_matchup_stats(
            player_faction="Space Marines",
            opponent_faction="Orks"
        )
        
        assert isinstance(stats, FactionStatistics)

    @pytest.mark.asyncio
    async def test_get_matchup_stats_calculates_correctly(self, db):
        """get_matchup_stats() should calculate wins/losses correctly."""
        # 3 wins for Marines
        for i in range(3):
            await db.index_game(
                game_id=f"win-{i}",
                player1_faction="Marines",
                player2_faction="Chaos",
                player1_list_hash=f"w{i}",
                player2_list_hash=f"c{i}",
                winner=1,
            )
        # 2 losses for Marines
        for i in range(2):
            await db.index_game(
                game_id=f"loss-{i}",
                player1_faction="Marines",
                player2_faction="Chaos",
                player1_list_hash=f"l{i}",
                player2_list_hash=f"x{i}",
                winner=2,
            )
        
        stats = await db.get_matchup_stats(
            player_faction="Marines",
            opponent_faction="Chaos"
        )
        
        assert stats.total_games == 5
        assert stats.wins == 3
        assert stats.losses == 2
        assert stats.win_rate == 0.6

    @pytest.mark.asyncio
    async def test_get_matchup_stats_none_for_no_data(self, db):
        """get_matchup_stats() should return None for no data."""
        stats = await db.get_matchup_stats(
            player_faction="Unknown",
            opponent_faction="Faction"
        )
        
        assert stats is None


# =============================================================================
# Context Manager Tests
# =============================================================================

class TestContextManager:
    """Test context manager functionality."""

    def test_enter_returns_self(self, temp_db_path):
        """__enter__ should return the database instance."""
        db = OpeningBookDB(db_path=temp_db_path)
        
        with db as instance:
            assert instance is db

    def test_exit_closes_connection(self, temp_db_path):
        """__exit__ should close the connection."""
        db = OpeningBookDB(db_path=temp_db_path)
        db._conn = MagicMock()
        
        db.__exit__()
        
        db._conn.close.assert_called_once()


# =============================================================================
# Model Validation Tests
# =============================================================================

class TestOpeningModels:
    """Test Pydantic model validation."""

    def test_historical_game_result_validates_winner(self):
        """HistoricalGameResult should validate winner field."""
        with pytest.raises(ValueError):
            HistoricalGameResult(
                game_id="test",
                player1_faction="A",
                player2_faction="B",
                winner=3,  # Invalid!
                score_differential=0,
                turn_count=5,
            )

    def test_historical_game_result_accepts_valid_winner(self):
        """HistoricalGameResult should accept 1 or 2."""
        for winner in [1, 2]:
            game = HistoricalGameResult(
                game_id="test",
                player1_faction="A",
                player2_faction="B",
                winner=winner,
                score_differential=0,
                turn_count=5,
            )
            assert game.winner == winner

    def test_faction_statistics_win_rate_property(self):
        """FactionStatistics.win_rate should calculate correctly."""
        stats = FactionStatistics(
            player_faction="A",
            opponent_faction="B",
            total_games=10,
            wins=7,
            losses=3,
        )
        
        assert stats.win_rate == 0.7

    def test_faction_statistics_win_rate_zero_games(self):
        """FactionStatistics.win_rate should return 0 for no games."""
        stats = FactionStatistics(
            player_faction="A",
            opponent_faction="B",
            total_games=0,
            wins=0,
            losses=0,
        )
        
        assert stats.win_rate == 0.0

    def test_deployment_pattern_validates_ranges(self):
        """DeploymentPattern should validate frequency and win_rate."""
        with pytest.raises(ValueError):
            DeploymentPattern(
                pattern_id="test",
                faction="A",
                description="Test",
                frequency=1.5,  # Out of range
                win_rate=0.5,
                sample_size=10,
            )
