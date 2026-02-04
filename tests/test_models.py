"""
Unit tests for Primordia models and evaluation.
"""

import pytest
from uuid import uuid4

from primordia.models import (
    GameState,
    Move,
    MoveRecommendation,
    Phase,
    Unit,
    UnitStatus,
)
from primordia.evaluation import HeuristicEvaluator, PositionEvaluation


class TestUnit:
    """Tests for Unit model."""

    def test_unit_creation(self):
        """Unit should be creatable with required fields."""
        unit = Unit(
            name="Space Marine Squad",
            faction="Space Marines",
            wounds_current=10,
            wounds_max=10,
            models_current=5,
            models_max=5
        )
        
        assert unit.name == "Space Marine Squad"
        assert unit.is_alive

    def test_unit_is_alive_with_wounds(self):
        """Unit with wounds should be alive."""
        unit = Unit(
            name="Test",
            faction="Test",
            wounds_current=5,
            wounds_max=10,
            models_current=3,
            models_max=5
        )
        
        assert unit.is_alive

    def test_unit_dead_with_zero_wounds(self):
        """Unit with zero wounds should not be alive."""
        unit = Unit(
            name="Test",
            faction="Test",
            wounds_current=0,
            wounds_max=10,
            models_current=0,
            models_max=5
        )
        
        assert not unit.is_alive

    def test_unit_dead_when_destroyed(self):
        """Unit with DESTROYED status should not be alive."""
        unit = Unit(
            name="Test",
            faction="Test",
            wounds_current=10,
            wounds_max=10,
            models_current=5,
            models_max=5,
            status=UnitStatus.DESTROYED
        )
        
        assert not unit.is_alive


class TestGameState:
    """Tests for GameState model."""

    def test_game_state_defaults(self):
        """GameState should have sensible defaults."""
        state = GameState()
        
        assert state.turn_number == 1
        assert state.current_phase == Phase.COMMAND
        assert state.active_player == 1
        assert len(state.player1_units) == 0
        assert len(state.player2_units) == 0

    def test_all_units(self):
        """all_units should return both players' units."""
        unit1 = Unit(name="U1", faction="F1", wounds_current=1, wounds_max=1, models_current=1, models_max=1)
        unit2 = Unit(name="U2", faction="F2", wounds_current=1, wounds_max=1, models_current=1, models_max=1)
        
        state = GameState(
            player1_units=[unit1],
            player2_units=[unit2]
        )
        
        assert len(state.all_units) == 2

    def test_get_unit_by_id(self):
        """get_unit should find unit by ID."""
        unit = Unit(name="Test", faction="Test", wounds_current=1, wounds_max=1, models_current=1, models_max=1)
        state = GameState(player1_units=[unit])
        
        found = state.get_unit(unit.id)
        
        assert found is not None
        assert found.id == unit.id

    def test_get_unit_not_found(self):
        """get_unit should return None for unknown ID."""
        state = GameState()
        
        found = state.get_unit(uuid4())
        
        assert found is None


class TestHeuristicEvaluator:
    """Tests for HeuristicEvaluator."""

    def test_equal_position(self):
        """Equal position should evaluate near 0."""
        unit1 = Unit(name="U1", faction="F1", wounds_current=10, wounds_max=10, models_current=5, models_max=5, points_cost=100)
        unit2 = Unit(name="U2", faction="F2", wounds_current=10, wounds_max=10, models_current=5, models_max=5, points_cost=100)
        
        state = GameState(
            player1_units=[unit1],
            player2_units=[unit2]
        )
        
        evaluator = HeuristicEvaluator()
        result = evaluator.evaluate(state)
        
        assert -0.2 < result.player_advantage < 0.2

    def test_player1_advantage(self):
        """Player 1 with more material should have advantage."""
        unit1 = Unit(name="U1", faction="F1", wounds_current=10, wounds_max=10, models_current=5, models_max=5, points_cost=200)
        unit2 = Unit(name="U2", faction="F2", wounds_current=5, wounds_max=10, models_current=2, models_max=5, points_cost=50)
        
        state = GameState(
            player1_units=[unit1],
            player2_units=[unit2]
        )
        
        evaluator = HeuristicEvaluator()
        result = evaluator.evaluate(state)
        
        assert result.player_advantage > 0

    def test_evaluation_has_confidence(self):
        """Evaluation should include confidence score."""
        state = GameState()
        
        evaluator = HeuristicEvaluator()
        result = evaluator.evaluate(state)
        
        assert 0.0 <= result.confidence <= 1.0

    def test_vp_advantage(self):
        """VP lead should affect evaluation."""
        state = GameState(
            player1_vp=10,
            player2_vp=0
        )
        
        evaluator = HeuristicEvaluator()
        result = evaluator.evaluate(state)
        
        assert result.player_advantage > 0
        assert "VP" in str(result.key_factors)


class TestPositionEvaluation:
    """Tests for PositionEvaluation model."""

    def test_explain(self):
        """explain() should return readable string."""
        eval = PositionEvaluation(
            player_advantage=0.5,
            win_probability=0.75,
            key_factors=["Material advantage"]
        )
        
        explanation = eval.explain()
        
        assert "advantage" in explanation.lower()


class TestMoveRecommendation:
    """Tests for MoveRecommendation model."""

    def test_recommendation_creation(self):
        """MoveRecommendation should be creatable."""
        move = Move(
            unit_id=uuid4(),
            phase=Phase.MOVEMENT,
            action_type="move"
        )
        
        rec = MoveRecommendation(
            move=move,
            score=0.8,
            confidence=0.9,
            reasoning="Best move available"
        )
        
        assert rec.score == 0.8
        assert rec.confidence == 0.9
