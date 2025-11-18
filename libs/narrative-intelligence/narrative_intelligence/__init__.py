"""
>à<8 Narrative Intelligence Toolkit

A toolkit for analyzing narratives using the Narrative Context Protocol (NCP) within LangGraph workflows.
"""

__version__ = "0.1.0"

# Schemas
from .schemas import (
    NCPData,
    Player,
    Perspective,
    StoryBeat,
    StoryPoint,
    Moment,
    NCPState,
    CharacterArcState,
    ThematicAnalysisState,
    EmotionalClassificationState,
)

# Nodes
from .nodes import (
    NCPLoaderNode,
    NarrativeTraversalNode,
    EmotionalBeatClassifierNode,
)

# Graphs
from .graphs import (
    CharacterArcGenerator,
    ThematicTensionAnalyzer,
)

__all__ = [
    # Version
    "__version__",

    # Schemas - NCP Models
    "NCPData",
    "Player",
    "Perspective",
    "StoryBeat",
    "StoryPoint",
    "Moment",

    # Schemas - State Models
    "NCPState",
    "CharacterArcState",
    "ThematicAnalysisState",
    "EmotionalClassificationState",

    # Nodes
    "NCPLoaderNode",
    "NarrativeTraversalNode",
    "EmotionalBeatClassifierNode",

    # Graphs
    "CharacterArcGenerator",
    "ThematicTensionAnalyzer",
]
