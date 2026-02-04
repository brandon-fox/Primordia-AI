"""
Core data models for Primordia.

These models represent game state, units, and moves
for the tactical AI engine.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from typing import Any, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Phase(Enum):
    """Game phases in a turn."""
    COMMAND = auto()
    MOVEMENT = auto()
    SHOOTING = auto()
    CHARGE = auto()
    FIGHT = auto()
    MORALE = auto()


class UnitStatus(Enum):
    """Unit status on the battlefield."""
    ACTIVE = auto()
    DESTROYED = auto()
    FLED = auto()
    IN_RESERVE = auto()


class Unit(BaseModel):
    """A unit on the battlefield."""
    
    id: UUID = Field(default_factory=uuid4)
    name: str
    faction: str
    
    # Stats
    wounds_current: int
    wounds_max: int
    models_current: int
    models_max: int
    
    # Position (abstract grid coordinates)
    position_x: float = 0.0
    position_y: float = 0.0
    
    # State
    status: UnitStatus = UnitStatus.ACTIVE
    has_moved: bool = False
    has_shot: bool = False
    has_charged: bool = False
    has_fought: bool = False
    
    # Metadata
    points_cost: int = 0
    keywords: list[str] = Field(default_factory=list)
    
    @property
    def is_alive(self) -> bool:
        """Check if unit is still active."""
        return self.status == UnitStatus.ACTIVE and self.wounds_current > 0


class Move(BaseModel):
    """A single action in the game."""
    
    id: UUID = Field(default_factory=uuid4)
    
    # Who/what
    unit_id: UUID
    phase: Phase
    action_type: str  # "move", "shoot", "charge", "fight", etc.
    
    # Target (optional)
    target_id: Optional[UUID] = None
    target_position: Optional[tuple[float, float]] = None
    
    # Results
    dice_required: list[int] = Field(default_factory=list)
    expected_damage: float = 0.0
    
    # Metadata
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class MoveRecommendation(BaseModel):
    """A recommended move from the engine."""
    
    move: Move
    
    # Evaluation
    score: float  # Higher is better
    confidence: float = Field(ge=0.0, le=1.0)  # How certain the engine is
    
    # Explanation
    reasoning: str
    key_factors: list[str] = Field(default_factory=list)
    
    # Alternatives considered
    alternatives_count: int = 0


class GameState(BaseModel):
    """The complete state of a game at a point in time."""
    
    id: UUID = Field(default_factory=uuid4)
    
    # Turn tracking
    turn_number: int = 1
    current_phase: Phase = Phase.COMMAND
    active_player: int = 1  # 1 or 2
    
    # Units
    player1_units: list[Unit] = Field(default_factory=list)
    player2_units: list[Unit] = Field(default_factory=list)
    
    # Game info
    mission: str = "unknown"
    deployment_type: str = "unknown"
    
    # Scoring
    player1_vp: int = 0
    player2_vp: int = 0
    
    # Move history
    move_history: list[Move] = Field(default_factory=list)
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    @property
    def all_units(self) -> list[Unit]:
        """Get all units on the battlefield."""
        return self.player1_units + self.player2_units
    
    @property
    def active_units(self) -> list[Unit]:
        """Get all active (non-destroyed) units."""
        return [u for u in self.all_units if u.is_alive]
    
    def get_unit(self, unit_id: UUID) -> Optional[Unit]:
        """Find a unit by ID."""
        for unit in self.all_units:
            if unit.id == unit_id:
                return unit
        return None
