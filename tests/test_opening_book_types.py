"""
Tests for OpeningBookDB Pydantic return types.

Issue #7: Type OpeningBookDB returns with Pydantic models.
RED phase: These tests define the expected behavior before implementation.
"""

import pytest
from pydantic import ValidationError

# These imports will fail until we implement the models
from primordia.database import (
    OpeningBookDB,
    HistoricalGameResult,
    FactionStatistics,
)


class TestHistoricalGameResultModel:
    """Tests for HistoricalGameResult Pydantic model."""

    def test_valid_game_result(self):
        """HistoricalGameResult should accept valid data."""
        result = HistoricalGameResult(
            id="game-001",
            player1_faction="Space Marines",
            player2_faction="Orks",
            player1_list_hash="abc123",
            player2_list_hash="def456",
            winner=1,
            player1_vp=50,
            player2_vp=30,
            turn_count=5
        )
        
        assert result.id == "game-001"
        assert result.player1_faction == "Space Marines"
        assert result.winner == 1

    def test_winner_must_be_1_or_2(self):
        """Winner must be either 1 or 2."""
        with pytest.raises(ValidationError):
            HistoricalGameResult(
                id="game-001",
                player1_faction="Space Marines",
                player2_faction="Orks",
                player1_list_hash="abc123",
                player2_list_hash="def456",
                winner=3,  # Invalid!
            )

    def test_winner_cannot_be_zero(self):
        """Winner cannot be 0."""
        with pytest.raises(ValidationError):
            HistoricalGameResult(
                id="game-001",
                player1_faction="Space Marines",
                player2_faction="Orks",
                player1_list_hash="abc123",
                player2_list_hash="def456",
                winner=0,  # Invalid!
            )

    def test_game_result_has_win_rate(self):
        """HistoricalGameResult should have computed properties."""
        result = HistoricalGameResult(
            id="game-001",
            player1_faction="Space Marines",
            player2_faction="Orks",
            player1_list_hash="abc123",
            player2_list_hash="def456",
            winner=1,
            player1_vp=50,
            player2_vp=30,
        )
        
        assert result.player1_won is True
        assert result.vp_differential == 20


class TestFactionStatisticsModel:
    """Tests for FactionStatistics Pydantic model."""

    def test_valid_stats(self):
        """FactionStatistics should accept valid data."""
        stats = FactionStatistics(
            faction="Space Marines",
            opponent="Orks",
            games=100,
            wins=60,
            losses=40,
            avg_vp_scored=45.5,
            avg_vp_conceded=35.2
        )
        
        assert stats.faction == "Space Marines"
        assert stats.games == 100
        assert stats.wins == 60

    def test_win_rate_computed(self):
        """FactionStatistics should compute win rate."""
        stats = FactionStatistics(
            faction="Space Marines",
            opponent="Orks",
            games=100,
            wins=60,
            losses=40,
            avg_vp_scored=45.5,
            avg_vp_conceded=35.2
        )
        
        assert stats.win_rate == 0.6

    def test_win_rate_zero_games(self):
        """FactionStatistics should handle zero games."""
        stats = FactionStatistics(
            faction="Space Marines",
            opponent="Orks",
            games=0,
            wins=0,
            losses=0,
            avg_vp_scored=0.0,
            avg_vp_conceded=0.0
        )
        
        assert stats.win_rate == 0.0


class TestOpeningBookDBTypedReturns:
    """Tests for OpeningBookDB typed return values."""

    @pytest.mark.asyncio
    async def test_query_matchup_returns_typed_list(self, tmp_path):
        """query_matchup should return list[HistoricalGameResult]."""
        db = OpeningBookDB(db_path=tmp_path / "test.duckdb")
        await db.connect()
        
        try:
            # Index a test game
            await db.index_game(
                game_id="test-001",
                player1_faction="Space Marines",
                player2_faction="Orks",
                player1_list_hash="abc123",
                player2_list_hash="def456",
                winner=1,
                player1_vp=50,
                player2_vp=30
            )
            
            # Query should return typed models
            results = await db.query_matchup("Space Marines", "Orks")
            
            assert isinstance(results, list)
            assert len(results) == 1
            
            # Each result should be a HistoricalGameResult
            result = results[0]
            assert isinstance(result, HistoricalGameResult)
            assert result.player1_faction == "Space Marines"
            assert result.winner == 1
            
        finally:
            await db.close()

    @pytest.mark.asyncio
    async def test_get_matchup_stats_returns_typed_model(self, tmp_path):
        """get_matchup_stats should return Optional[FactionStatistics]."""
        db = OpeningBookDB(db_path=tmp_path / "test.duckdb")
        await db.connect()
        
        try:
            # Index a test game
            await db.index_game(
                game_id="test-001",
                player1_faction="Space Marines",
                player2_faction="Orks",
                player1_list_hash="abc123",
                player2_list_hash="def456",
                winner=1,
                player1_vp=50,
                player2_vp=30
            )
            
            # Stats should return typed model
            stats = await db.get_matchup_stats("Space Marines", "Orks")
            
            assert stats is not None
            assert isinstance(stats, FactionStatistics)
            assert stats.faction == "Space Marines"
            assert stats.opponent == "Orks"
            assert stats.games == 1
            assert stats.wins == 1
            
        finally:
            await db.close()

    @pytest.mark.asyncio
    async def test_get_matchup_stats_returns_none_when_not_found(self, tmp_path):
        """get_matchup_stats should return None when no games exist."""
        db = OpeningBookDB(db_path=tmp_path / "test.duckdb")
        await db.connect()
        
        try:
            stats = await db.get_matchup_stats("Unknown", "Faction")
            assert stats is None
            
        finally:
            await db.close()
