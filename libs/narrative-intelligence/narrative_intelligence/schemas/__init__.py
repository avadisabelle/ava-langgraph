"""Schema definitions for the Narrative Context Protocol (NCP)."""

from .ncp import (
    NCPData,
    Player,
    Perspective,
    StoryBeat,
    StoryPoint,
    Moment,
)
from .state import (
    NCPState,
    CharacterArcState,
    ThematicAnalysisState,
    EmotionalClassificationState,
)
from .unified_state_bridge import (
    # Enums
    Universe,
    NarrativePhase,
    NarrativeFunction,
    # Three Universe Types
    UniversePerspective,
    ThreeUniverseAnalysis,
    # Narrative Types
    NarrativePosition,
    StoryBeat as UnifiedStoryBeat,  # Alias to avoid conflict
    CharacterState,
    ThematicThread,
    RoutingDecision,
    # Main State
    UnifiedNarrativeState,
    # Factory Functions
    create_new_narrative_state,
    create_beat_from_webhook,
    get_default_characters,
    get_default_themes,
    # Redis Helpers
    RedisKeys,
)

__all__ = [
    # NCP Models (original)
    "NCPData",
    "Player",
    "Perspective",
    "StoryBeat",
    "StoryPoint",
    "Moment",
    # State Models (original)
    "NCPState",
    "CharacterArcState",
    "ThematicAnalysisState",
    "EmotionalClassificationState",
    # Unified State Bridge (NEW)
    "Universe",
    "NarrativePhase",
    "NarrativeFunction",
    "UniversePerspective",
    "ThreeUniverseAnalysis",
    "NarrativePosition",
    "UnifiedStoryBeat",
    "CharacterState",
    "ThematicThread",
    "RoutingDecision",
    "UnifiedNarrativeState",
    "create_new_narrative_state",
    "create_beat_from_webhook",
    "get_default_characters",
    "get_default_themes",
    "RedisKeys",
]
