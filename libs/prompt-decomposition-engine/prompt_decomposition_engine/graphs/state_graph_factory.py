"""
LangGraph StateGraph Factory for PDE.

Creates a proper LangGraph StateGraph that can be compiled and used
as a subgraph in larger graph workflows.

Requires langgraph as a dependency.

Usage:
    from prompt_decomposition_engine.graphs.state_graph_factory import create_decomposition_state_graph

    graph = create_decomposition_state_graph()
    compiled = graph.compile()
    result = compiled.invoke({"prompt": "Build a knowledge graph..."})
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from prompt_decomposition_engine.graphs.decomposition_graph import (
    east_node,
    south_node,
    west_node,
    north_node,
)


def create_decomposition_state_graph(
    *,
    enforce_ceremony: bool = False,
) -> Any:
    """
    Create a LangGraph StateGraph for the PDE pipeline.

    The graph follows EAST → SOUTH → WEST → (ceremony check) → NORTH.

    Args:
        enforce_ceremony: If True, halt at ceremony_hold instead of continuing.

    Returns:
        A configured StateGraph ready to be compiled.

    Raises:
        ImportError: If langgraph is not installed.
    """
    try:
        from langgraph.graph import StateGraph, END, START
    except ImportError:
        raise ImportError(
            "create_decomposition_state_graph requires langgraph. "
            "Install it with: pip install langgraph"
        )

    from typing import TypedDict, List

    class PDEState(TypedDict, total=False):
        prompt: str
        session_id: str
        directional_analysis: Any
        intent_result: Any
        dependency_graph: Any
        execution_order: Any
        wheel_enriched: Any
        ceremony_required: bool
        relational_guidance: List[str]
        decomposition: Any
        status: str
        errors: List[str]

    graph = StateGraph(PDEState)

    graph.add_node("east", east_node)
    graph.add_node("south", south_node)
    graph.add_node("west", west_node)
    graph.add_node("north", north_node)

    graph.add_edge(START, "east")
    graph.add_edge("east", "south")
    graph.add_edge("south", "west")

    def ceremony_router(state: PDEState) -> str:
        if state.get("status") == "ceremony_hold" and enforce_ceremony:
            return END
        return "north"

    graph.add_conditional_edges("west", ceremony_router)
    graph.add_edge("north", END)

    return graph
