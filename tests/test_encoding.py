"""Tests for game state encoding."""

import numpy as np
import pytest

from primordia.encoding import (
    EncodedState,
    GameStateEncoder,
    GLOBAL_FEATURE_DIM,
    MAX_UNITS_PER_PLAYER,
    UNIT_FEATURE_DIM,
)
from primordia.models import GameState, Phase, Unit, UnitStatus


@pytest.fixture
def sample_unit() -> Unit:
    """Create a sample unit for testing."""
    return Unit(
        name="Space Marines",
        faction="Imperium",
        wounds_current=10,
        wounds_max=12,
        models_current=5,
        models_max=5,
        position_x=24.0,
        position_y=18.0,
        points_cost=200,
    )


@pytest.fixture
def sample_game_state(sample_unit: Unit) -> GameState:
    """Create a sample game state for testing."""
    return GameState(
        turn_number=2,
        current_phase=Phase.MOVEMENT,
        active_player=1,
        player1_units=[sample_unit],
        player2_units=[],
        player1_vp=15,
        player2_vp=10,
    )


class TestGameStateEncoder:
    """Tests for GameStateEncoder class."""
    
    def test_encoder_initialization(self) -> None:
        """Test encoder initializes with correct defaults."""
        encoder = GameStateEncoder()
        assert encoder.max_units == MAX_UNITS_PER_PLAYER
        assert encoder.board_size == 60.0
    
    def test_custom_initialization(self) -> None:
        """Test encoder with custom parameters."""
        encoder = GameStateEncoder(max_units=10, board_size=44.0)
        assert encoder.max_units == 10
        assert encoder.board_size == 44.0
    
    def test_encode_returns_encoded_state(self, sample_game_state: GameState) -> None:
        """Test encode returns EncodedState with correct shapes."""
        encoder = GameStateEncoder()
        result = encoder.encode(sample_game_state)
        
        assert isinstance(result, EncodedState)
        assert result.global_features.shape == (GLOBAL_FEATURE_DIM,)
        assert result.player1_units.shape == (MAX_UNITS_PER_PLAYER, UNIT_FEATURE_DIM)
        assert result.player2_units.shape == (MAX_UNITS_PER_PLAYER, UNIT_FEATURE_DIM)
        assert result.unit_mask_p1.shape == (MAX_UNITS_PER_PLAYER,)
        assert result.unit_mask_p2.shape == (MAX_UNITS_PER_PLAYER,)
    
    def test_global_features_normalized(self, sample_game_state: GameState) -> None:
        """Test that global features are in [0, 1] range."""
        encoder = GameStateEncoder()
        result = encoder.encode(sample_game_state)
        
        assert np.all(result.global_features >= 0.0)
        assert np.all(result.global_features <= 1.0)
    
    def test_unit_features_normalized(self, sample_game_state: GameState) -> None:
        """Test that unit features are in [0, 1] range."""
        encoder = GameStateEncoder()
        result = encoder.encode(sample_game_state)
        
        # Check only first unit (others are zero-padded)
        first_unit = result.player1_units[0]
        assert np.all(first_unit >= 0.0)
        assert np.all(first_unit <= 1.0)
    
    def test_unit_mask_correctness(self, sample_game_state: GameState) -> None:
        """Test that unit masks correctly identify valid units."""
        encoder = GameStateEncoder()
        result = encoder.encode(sample_game_state)
        
        # Player 1 has 1 unit
        assert result.unit_mask_p1[0] == True
        assert result.unit_mask_p1[1] == False
        
        # Player 2 has no units
        assert np.all(result.unit_mask_p2 == False)
    
    def test_position_encoding(self, sample_unit: Unit) -> None:
        """Test unit position is correctly normalized."""
        encoder = GameStateEncoder(board_size=60.0)
        features = encoder._encode_unit(sample_unit)
        
        # Position (24, 18) / 60 = (0.4, 0.3)
        assert features[0] == pytest.approx(0.4)
        assert features[1] == pytest.approx(0.3)
    
    def test_wounds_ratio_encoding(self, sample_unit: Unit) -> None:
        """Test wounds ratio is correctly calculated."""
        encoder = GameStateEncoder()
        features = encoder._encode_unit(sample_unit)
        
        # 10/12 wounds = 0.833...
        assert features[2] == pytest.approx(10.0 / 12.0)
    
    def test_status_one_hot_encoding(self) -> None:
        """Test unit status is one-hot encoded."""
        encoder = GameStateEncoder()
        
        # Active unit
        active_unit = Unit(
            name="Test", faction="Test",
            wounds_current=5, wounds_max=5,
            models_current=1, models_max=1,
            status=UnitStatus.ACTIVE,
        )
        features = encoder._encode_unit(active_unit)
        assert features[5] == 1.0  # ACTIVE
        assert features[6] == 0.0  # DESTROYED
        
        # Destroyed unit
        destroyed_unit = Unit(
            name="Test", faction="Test",
            wounds_current=0, wounds_max=5,
            models_current=0, models_max=1,
            status=UnitStatus.DESTROYED,
        )
        features = encoder._encode_unit(destroyed_unit)
        assert features[5] == 0.0  # ACTIVE
        assert features[6] == 1.0  # DESTROYED
    
    def test_flat_encoding(self, sample_game_state: GameState) -> None:
        """Test flat encoding produces correct dimension."""
        encoder = GameStateEncoder()
        result = encoder.encode(sample_game_state)
        
        expected_dim = (
            GLOBAL_FEATURE_DIM +
            2 * MAX_UNITS_PER_PLAYER * UNIT_FEATURE_DIM
        )
        assert result.flat.shape == (expected_dim,)
        assert result.total_dim == expected_dim
    
    def test_feature_names(self) -> None:
        """Test feature name methods return correct counts."""
        assert len(GameStateEncoder.feature_names()) == UNIT_FEATURE_DIM
        assert len(GameStateEncoder.global_feature_names()) == GLOBAL_FEATURE_DIM
    
    def test_empty_state_encoding(self) -> None:
        """Test encoding an empty game state."""
        encoder = GameStateEncoder()
        empty_state = GameState(
            turn_number=1,
            current_phase=Phase.COMMAND,
            active_player=1,
        )
        result = encoder.encode(empty_state)
        
        # Should not raise, all units should be zero
        assert np.all(result.player1_units == 0.0)
        assert np.all(result.player2_units == 0.0)
        assert np.all(result.unit_mask_p1 == False)
        assert np.all(result.unit_mask_p2 == False)
