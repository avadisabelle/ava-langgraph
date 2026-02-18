"""
Decomposition Graph

State-based graph that orchestrates the full PDE pipeline:
1. EAST node: Intent extraction (what is being asked?)
2. SOUTH node: Dependency analysis (what needs to be learned?)
3. WEST node: Ceremony gate (what needs reflection?)
4. NORTH node: Action stack building (what executes?)
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from prompt_decomposition import (
    DirectionalDecomposer,
    IntentExtractor,
    DependencyMapper,
    ActionStackBuilder,
    MedicineWheelBridge,
)
from prompt_decomposition.directional_decomposer import DirectionalAnalysis
from prompt_decomposition.intent_extractor import IntentExtractionResult
from prompt_decomposition.dependency_mapper import DependencyGraph, ExecutionOrder
from prompt_decomposition.action_stack import DecompositionResult
from prompt_decomposition.wheel_bridge import WheelEnrichedAnalysis


@dataclass
class DecompositionState:
    prompt: str
    session_id: str
    directional_analysis: Optional[DirectionalAnalysis] = None
    intent_result: Optional[IntentExtractionResult] = None
    dependency_graph: Optional[DependencyGraph] = None
    execution_order: Optional[ExecutionOrder] = None
    wheel_enriched: Optional[WheelEnrichedAnalysis] = None
    ceremony_required: bool = False
    relational_guidance: List[str] = field(default_factory=list)
    decomposition: Optional[DecompositionResult] = None
    status: str = "pending"
    errors: List[str] = field(default_factory=list)


def create_initial_state(prompt: str, session_id: Optional[str] = None) -> DecompositionState:
    return DecompositionState(
        prompt=prompt,
        session_id=session_id or str(uuid.uuid4()),
    )


def east_node(state: DecompositionState) -> Dict[str, Any]:
    """EAST: Vision — Extract intents and directional analysis."""
    try:
        decomposer = DirectionalDecomposer()
        extractor = IntentExtractor()
        return {
            "directional_analysis": decomposer.decompose(state.prompt),
            "intent_result": extractor.extract(state.prompt),
            "status": "east_complete",
        }
    except Exception as e:
        return {
            "errors": state.errors + [f"EAST: {e}"],
            "status": "east_complete",
        }


def south_node(state: DecompositionState) -> Dict[str, Any]:
    """SOUTH: Analysis — Map dependencies and compute execution order."""
    if not state.intent_result:
        return {
            "errors": state.errors + ["SOUTH: No intent result from EAST"],
            "status": "south_complete",
        }
    try:
        mapper = DependencyMapper()
        graph = mapper.build_graph(state.intent_result.secondary)
        order = mapper.compute_execution_order(graph)
        return {
            "dependency_graph": graph,
            "execution_order": order,
            "status": "south_complete",
        }
    except Exception as e:
        return {
            "errors": state.errors + [f"SOUTH: {e}"],
            "status": "south_complete",
        }


def west_node(state: DecompositionState) -> Dict[str, Any]:
    """WEST: Validation — Check ceremony requirements and relational balance."""
    if not state.directional_analysis:
        return {
            "errors": state.errors + ["WEST: No directional analysis from EAST"],
            "status": "west_complete",
        }
    try:
        bridge = MedicineWheelBridge()
        enriched = bridge.enrich(state.directional_analysis)
        guidance = bridge.get_relational_guidance(state.directional_analysis)
        return {
            "wheel_enriched": enriched,
            "ceremony_required": enriched.ceremony_required,
            "relational_guidance": guidance,
            "status": "ceremony_hold" if enriched.ceremony_required else "west_complete",
        }
    except Exception as e:
        return {
            "errors": state.errors + [f"WEST: {e}"],
            "status": "west_complete",
        }


def north_node(state: DecompositionState) -> Dict[str, Any]:
    """NORTH: Action — Build the final action stack."""
    if not state.directional_analysis or not state.intent_result:
        return {
            "errors": state.errors + ["NORTH: Missing EAST results"],
            "status": "complete",
        }
    try:
        builder = ActionStackBuilder()
        decomposition = builder.build(
            state.directional_analysis,
            state.intent_result,
            state.execution_order,
        )
        return {
            "decomposition": decomposition,
            "status": "complete",
        }
    except Exception as e:
        return {
            "errors": state.errors + [f"NORTH: {e}"],
            "status": "complete",
        }


class DecompositionGraph:
    """Orchestrates EAST→SOUTH→WEST→NORTH pipeline."""

    def __init__(self, enforce_ceremony: bool = False):
        self.enforce_ceremony = enforce_ceremony

    async def invoke(self, prompt: str, session_id: Optional[str] = None) -> DecompositionState:
        state = create_initial_state(prompt, session_id)

        state = self._merge(state, east_node(state))
        state = self._merge(state, south_node(state))
        state = self._merge(state, west_node(state))

        if state.status == "ceremony_hold" and self.enforce_ceremony:
            return state

        state = self._merge(state, north_node(state))
        return state

    async def invoke_east(self, state: DecompositionState) -> DecompositionState:
        return self._merge(state, east_node(state))

    async def invoke_south(self, state: DecompositionState) -> DecompositionState:
        return self._merge(state, south_node(state))

    async def invoke_west(self, state: DecompositionState) -> DecompositionState:
        return self._merge(state, west_node(state))

    async def invoke_north(self, state: DecompositionState) -> DecompositionState:
        return self._merge(state, north_node(state))

    def _merge(self, state: DecompositionState, updates: Dict[str, Any]) -> DecompositionState:
        for key, value in updates.items():
            setattr(state, key, value)
        return state
