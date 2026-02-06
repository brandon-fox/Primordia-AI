"""Game state encoding for neural network input.

Provides normalized vector representations of game states
suitable for ML model consumption.
"""

from dataclasses import dataclass
from typing import Sequence

import numpy as np
from numpy.typing import NDArray

from primordia.models import GameState, Phase, Unit, UnitStatus


# Encoding constants
MAX_UNITS_PER_PLAYER = 20
UNIT_FEATURE_DIM = 12
GLOBAL_FEATURE_DIM = 8
BOARD_SIZE = 60.0  # Inches, for normalization


@dataclass
class EncodedState:
    """Encoded representation of a game state."""
    
    global_features: NDArray[np.float32]  # Shape: (GLOBAL_FEATURE_DIM,)
    player1_units: NDArray[np.float32]    # Shape: (MAX_UNITS, UNIT_FEATURE_DIM)
    player2_units: NDArray[np.float32]    # Shape: (MAX_UNITS, UNIT_FEATURE_DIM)
    unit_mask_p1: NDArray[np.bool_]       # Shape: (MAX_UNITS,)
    unit_mask_p2: NDArray[np.bool_]       # Shape: (MAX_UNITS,)
    
    @property
    def flat(self) -> NDArray[np.float32]:
        """Flatten to single vector for simple MLPs."""
        return np.concatenate([
            self.global_features,
            self.player1_units.flatten(),
            self.player2_units.flatten(),
        ])
    
    @property
    def total_dim(self) -> int:
        """Total dimension of flat encoding."""
        return (
            GLOBAL_FEATURE_DIM +
            2 * MAX_UNITS_PER_PLAYER * UNIT_FEATURE_DIM
        )


class GameStateEncoder:
    """Encodes game states into normalized vectors for ML models."""
    
    def __init__(
        self,
        max_units: int = MAX_UNITS_PER_PLAYER,
        board_size: float = BOARD_SIZE,
    ) -> None:
        """Initialize encoder with configuration.
        
        Args:
            max_units: Maximum units per player to encode.
            board_size: Board size in inches for position normalization.
        """
        self.max_units = max_units
        self.board_size = board_size
    
    def encode(self, state: GameState) -> EncodedState:
        """Encode a game state into normalized vectors.
        
        Args:
            state: The game state to encode.
            
        Returns:
            EncodedState with normalized feature vectors.
        """
        return EncodedState(
            global_features=self._encode_global(state),
            player1_units=self._encode_units(state.player1_units),
            player2_units=self._encode_units(state.player2_units),
            unit_mask_p1=self._create_mask(state.player1_units),
            unit_mask_p2=self._create_mask(state.player2_units),
        )
    
    def _encode_global(self, state: GameState) -> NDArray[np.float32]:
        """Encode global game state features."""
        features = np.zeros(GLOBAL_FEATURE_DIM, dtype=np.float32)
        
        # Turn number (normalized, cap at 5)
        features[0] = min(state.turn_number / 5.0, 1.0)
        
        # Phase (one-hot, using 6 slots for 6 phases)
        phase_idx = list(Phase).index(state.current_phase)
        features[1] = phase_idx / 5.0  # Normalized phase
        
        # Active player (0 or 1)
        features[2] = float(state.active_player - 1)
        
        # Victory points (normalized, cap at 100)
        features[3] = min(state.player1_vp / 100.0, 1.0)
        features[4] = min(state.player2_vp / 100.0, 1.0)
        
        # VP difference (centered at 0.5)
        vp_diff = state.player1_vp - state.player2_vp
        features[5] = 0.5 + np.clip(vp_diff / 100.0, -0.5, 0.5)
        
        # Unit counts (normalized)
        p1_active = sum(1 for u in state.player1_units if u.is_alive)
        p2_active = sum(1 for u in state.player2_units if u.is_alive)
        features[6] = min(p1_active / self.max_units, 1.0)
        features[7] = min(p2_active / self.max_units, 1.0)
        
        return features
    
    def _encode_units(self, units: Sequence[Unit]) -> NDArray[np.float32]:
        """Encode a list of units to fixed-size matrix."""
        encoded = np.zeros(
            (self.max_units, UNIT_FEATURE_DIM),
            dtype=np.float32
        )
        
        for i, unit in enumerate(units[:self.max_units]):
            encoded[i] = self._encode_unit(unit)
        
        return encoded
    
    def _encode_unit(self, unit: Unit) -> NDArray[np.float32]:
        """Encode a single unit to feature vector."""
        features = np.zeros(UNIT_FEATURE_DIM, dtype=np.float32)
        
        # Position (normalized to 0-1)
        features[0] = np.clip(unit.position_x / self.board_size, 0, 1)
        features[1] = np.clip(unit.position_y / self.board_size, 0, 1)
        
        # Health (current/max wounds ratio)
        features[2] = unit.wounds_current / max(unit.wounds_max, 1)
        
        # Model count (current/max ratio)
        features[3] = unit.models_current / max(unit.models_max, 1)
        
        # Points (normalized, assuming 500 max per unit)
        features[4] = min(unit.points_cost / 500.0, 1.0)
        
        # Status (one-hot encoding, 4 states)
        status_idx = list(UnitStatus).index(unit.status)
        features[5] = float(status_idx == 0)  # ACTIVE
        features[6] = float(status_idx == 1)  # DESTROYED
        features[7] = float(status_idx == 2)  # FLED
        features[8] = float(status_idx == 3)  # IN_RESERVE
        
        # Action flags
        features[9] = float(unit.has_moved)
        features[10] = float(unit.has_shot)
        features[11] = float(unit.has_charged or unit.has_fought)
        
        return features
    
    def _create_mask(self, units: Sequence[Unit]) -> NDArray[np.bool_]:
        """Create attention mask for valid units."""
        mask = np.zeros(self.max_units, dtype=np.bool_)
        mask[:min(len(units), self.max_units)] = True
        return mask
    
    @staticmethod
    def feature_names() -> list[str]:
        """Get human-readable names for unit features."""
        return [
            "position_x",
            "position_y",
            "wounds_ratio",
            "models_ratio",
            "points_norm",
            "status_active",
            "status_destroyed",
            "status_fled",
            "status_reserve",
            "has_moved",
            "has_shot",
            "has_fought",
        ]
    
    @staticmethod
    def global_feature_names() -> list[str]:
        """Get human-readable names for global features."""
        return [
            "turn_progress",
            "phase_norm",
            "active_player",
            "p1_vp_norm",
            "p2_vp_norm",
            "vp_diff_centered",
            "p1_units_active",
            "p2_units_active",
        ]
