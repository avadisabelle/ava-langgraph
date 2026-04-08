"""
langgraph-prompt-decomposition-engine

Graph-level orchestration for the Prompt Decomposition Engine (PDE).
Built on top of langchain-prompt-decomposition primitives.

Components:
- DecompositionGraph: State-based graph running EAST→SOUTH→WEST→NORTH
- PerspectiveAnalyzer: Three-universe analysis (Mia/Ava8/Miette)
- CeremonyGate: Relational accountability gating
"""

__version__ = "0.1.0"

from prompt_decomposition_engine.graphs.decomposition_graph import (
    DecompositionState,
    create_initial_state,
    east_node,
    south_node,
    west_node,
    north_node,
    DecompositionGraph,
)

from prompt_decomposition_engine.nodes.perspective_nodes import (
    Universe,
    UNIVERSE_NAMES,
    PerspectiveAnalyzer,
)

from prompt_decomposition_engine.nodes.ceremony_gate import (
    GateDecision,
    CeremonyGate,
)

from prompt_decomposition_engine.graphs.state_graph_factory import (
    create_decomposition_state_graph,
)

# Re-export core primitives for convenience
from prompt_decomposition import (
    Direction,
    DirectionalDecomposer,
    IntentExtractor,
    DependencyMapper,
    ActionStackBuilder,
    MedicineWheelBridge,
    decompose,
    RunnableDecomposer,
    RunnableDirectionalAnalyzer,
    RunnableWheelGate,
)

__all__ = [
    "DecompositionState",
    "create_initial_state",
    "east_node",
    "south_node",
    "west_node",
    "north_node",
    "DecompositionGraph",
    "Universe",
    "UNIVERSE_NAMES",
    "PerspectiveAnalyzer",
    "GateDecision",
    "CeremonyGate",
    "create_decomposition_state_graph",
    "Direction",
    "DirectionalDecomposer",
    "IntentExtractor",
    "DependencyMapper",
    "ActionStackBuilder",
    "MedicineWheelBridge",
    "decompose",
    "RunnableDecomposer",
    "RunnableDirectionalAnalyzer",
    "RunnableWheelGate",
]
