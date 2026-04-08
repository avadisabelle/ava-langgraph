"""
Narrative Intelligence Toolkit

A toolkit for analyzing narratives using the Narrative Context Protocol (NCP) within LangGraph workflows.
"""

__version__ = "0.1.0"

# Core schemas (always available)
from .schemas import (
    NCPData,
    Player,
    Perspective,
    StoryBeat as NCPStoryBeat,  # Alias to avoid confusion with unified_state_bridge.StoryBeat
    StoryPoint,
    Moment,
)

# Unified state bridge (always available, no langgraph dependency)
from .schemas.unified_state_bridge import (
    Universe,
    UniversePerspective,
    ThreeUniverseAnalysis,
    NarrativePhase,
    NarrativeFunction,
    NarrativePosition,
    StoryBeat,
    CharacterState,
    ThematicThread,
    RoutingDecision,
    UnifiedNarrativeState,
    create_new_narrative_state,
    create_beat_from_webhook,
    get_default_characters,
    get_default_themes,
    RedisKeys,
)

# Alias for convenience
create_initial_state = create_new_narrative_state

# LangGraph-dependent imports (optional)
try:
    from .schemas import (
        NCPState,
        CharacterArcState,
        ThematicAnalysisState,
        EmotionalClassificationState,
    )
    
    from .nodes import (
        NCPLoaderNode,
        NarrativeTraversalNode,
        EmotionalBeatClassifierNode,
    )
    from .nodes.narrative_traversal import TraversalMode
    from .nodes.emotional_classifier import EmotionalTone
    
    from .graphs import (
        CharacterArcGenerator,
        ThematicTensionAnalyzer,
        ThreeUniverseProcessor,
        create_three_universe_graph,
        ThreeUniverseState,
        EventType,
        # Coherence Engine (for Editor Anvil)
        NarrativeCoherenceEngine,
        Gap,
        GapType,
        GapSeverity,
        RoutingTarget,
        ComponentScore,
        CoherenceScore,
        TrinityAssessment,
    )
    
    HAS_LANGGRAPH = True
except ImportError:
    HAS_LANGGRAPH = False
    # Set to None so they can be checked
    NCPState = None
    CharacterArcState = None
    ThematicAnalysisState = None
    EmotionalClassificationState = None
    NCPLoaderNode = None
    NarrativeTraversalNode = None
    EmotionalBeatClassifierNode = None
    TraversalMode = None
    EmotionalTone = None
    CharacterArcGenerator = None
    ThematicTensionAnalyzer = None
    ThreeUniverseProcessor = None
    create_three_universe_graph = None
    ThreeUniverseState = None
    EventType = None
    # Coherence Engine
    NarrativeCoherenceEngine = None
    Gap = None
    GapType = None
    GapSeverity = None
    RoutingTarget = None
    ComponentScore = None
    CoherenceScore = None
    TrinityAssessment = None

__all__ = [
    # Version
    "__version__",
    "HAS_LANGGRAPH",
    
    # Core Schemas - NCP Models (always available)
    "NCPData",
    "Player",
    "Perspective",
    "NCPStoryBeat",
    "StoryPoint",
    "Moment",
    
    # Unified State Bridge (always available)
    "Universe",
    "UniversePerspective",
    "ThreeUniverseAnalysis",
    "NarrativePhase",
    "NarrativeFunction",
    "NarrativePosition",
    "StoryBeat",
    "CharacterState",
    "ThematicThread",
    "RoutingDecision",
    "UnifiedNarrativeState",
    "create_new_narrative_state",
    "create_initial_state",  # alias
    "create_beat_from_webhook",
    "get_default_characters",
    "get_default_themes",
    "RedisKeys",
    
    # LangGraph-dependent (may be None)
    "NCPState",
    "CharacterArcState",
    "ThematicAnalysisState",
    "EmotionalClassificationState",
    "NCPLoaderNode",
    "NarrativeTraversalNode",
    "EmotionalBeatClassifierNode",
    "TraversalMode",
    "EmotionalTone",
    "CharacterArcGenerator",
    "ThematicTensionAnalyzer",
    "ThreeUniverseProcessor",
    "create_three_universe_graph",
    "ThreeUniverseState",
    "EventType",
    # Coherence Engine (for Editor Anvil)
    "NarrativeCoherenceEngine",
    "Gap",
    "GapType",
    "GapSeverity",
    "RoutingTarget",
    "ComponentScore",
    "CoherenceScore",
    "TrinityAssessment",
]
