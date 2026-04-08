"""Tests for langgraph-prompt-decomposition-engine - full parity with JS tests."""

import pytest

from prompt_decomposition import decompose as pde_decompose
from prompt_decomposition_engine import (
    DecompositionGraph,
    create_initial_state,
    east_node,
    south_node,
    west_node,
    north_node,
    PerspectiveAnalyzer,
    Universe,
    CeremonyGate,
    GateDecision,
)


# =============================================================================
# DecompositionGraph
# =============================================================================

class TestDecompositionGraphNodes:
    def test_east_node_extracts_intents(self):
        state = create_initial_state("Research the codebase and build a new module.")
        result = east_node(state)
        assert result["directional_analysis"] is not None
        assert result["intent_result"] is not None
        assert result["status"] == "east_complete"

    def test_south_node_builds_dependencies(self):
        state = create_initial_state("Investigate patterns. Create implementation. Test results.")
        updates = east_node(state)
        for k, v in updates.items():
            setattr(state, k, v)
        result = south_node(state)
        assert result["dependency_graph"] is not None
        assert result["execution_order"] is not None

    def test_south_node_handles_missing_east(self):
        state = create_initial_state("test")
        result = south_node(state)
        assert len(result["errors"]) > 0

    def test_west_node_assesses_ceremony(self):
        state = create_initial_state("Build code and deploy immediately.")
        updates = east_node(state)
        for k, v in updates.items():
            setattr(state, k, v)
        result = west_node(state)
        assert result["wheel_enriched"] is not None
        assert isinstance(result["ceremony_required"], bool)

    def test_north_node_builds_action_stack(self):
        state = create_initial_state("Research. Build. Test.")
        for node_fn in [east_node, south_node]:
            updates = node_fn(state)
            for k, v in updates.items():
                setattr(state, k, v)
        result = north_node(state)
        assert result["decomposition"] is not None
        assert result["status"] == "complete"


class TestDecompositionGraphPipeline:
    @pytest.mark.asyncio
    async def test_full_pipeline(self):
        graph = DecompositionGraph()
        state = await graph.invoke(
            "Investigate the existing codebase. Design the architecture. "
            "Build the implementation. Test everything."
        )
        assert state.status == "complete"
        assert state.directional_analysis is not None
        assert state.intent_result is not None
        assert state.decomposition is not None
        assert len(state.decomposition.action_stack) > 0

    @pytest.mark.asyncio
    async def test_detects_ceremony_requirements(self):
        graph = DecompositionGraph()
        state = await graph.invoke("Build code. Deploy code. Ship it. Execute now.")
        assert state.relational_guidance is not None

    @pytest.mark.asyncio
    async def test_halts_at_ceremony_when_enforced(self):
        graph = DecompositionGraph(enforce_ceremony=True)
        state = await graph.invoke("Build code. Ship immediately. Deploy now. Execute.")
        if state.ceremony_required:
            assert state.status == "ceremony_hold"
            assert state.decomposition is None

    @pytest.mark.asyncio
    async def test_preserves_session_id(self):
        graph = DecompositionGraph()
        state = await graph.invoke("Research and build.", session_id="session-123")
        assert state.session_id == "session-123"


# =============================================================================
# PerspectiveAnalyzer
# =============================================================================

class TestPerspectiveAnalyzer:
    def setup_method(self):
        self.analyzer = PerspectiveAnalyzer()

    def test_analyzes_through_three_universes(self):
        result = pde_decompose("Build a new module and test the integration.")
        perspective = self.analyzer.analyze(result["decomposition"])
        assert len(perspective.insights) == 3
        assert perspective.lead_universe is not None
        assert 0 <= perspective.coherence <= 1

    def test_detects_engineer_led_work(self):
        result = pde_decompose(
            "Build the API module. Implement the schema. Deploy to infrastructure. Debug performance."
        )
        perspective = self.analyzer.analyze(result["decomposition"])
        engineer = next(i for i in perspective.insights if i.universe == Universe.ENGINEER)
        assert engineer.confidence > 0

    def test_detects_ceremony_domain(self):
        result = pde_decompose(
            "Design the medicine wheel ceremony protocol for indigenous community governance."
        )
        perspective = self.analyzer.analyze(result["decomposition"])
        ceremony = next(i for i in perspective.insights if i.universe == Universe.CEREMONY)
        assert ceremony.confidence > 0

    def test_flags_missing_ceremony(self):
        result = pde_decompose(
            "Build indigenous knowledge graph. Deploy medicine wheel schema."
        )
        perspective = self.analyzer.analyze(result["decomposition"])
        ceremony = next(i for i in perspective.insights if i.universe == Universe.CEREMONY)
        assert len(ceremony.flags) > 0

    def test_provides_synthesis(self):
        result = pde_decompose("Research. Build. Test. Reflect on purpose.")
        perspective = self.analyzer.analyze(result["decomposition"])
        assert len(perspective.synthesis) > 0


# =============================================================================
# CeremonyGate
# =============================================================================

class TestCeremonyGate:
    def setup_method(self):
        self.gate = CeremonyGate()

    def test_evaluates_balanced_decomposition(self):
        result = pde_decompose(
            "Research the context. Design the architecture. Build the module. Verify the results."
        )
        gate_result = self.gate.evaluate(result["decomposition"])
        assert gate_result.decision in (GateDecision.PROCEED, GateDecision.CAUTION)

    def test_flags_unbalanced(self):
        result = pde_decompose("Build. Ship. Deploy. Code. Execute.")
        gate_result = self.gate.evaluate(result["decomposition"])
        assert len(gate_result.reasons) > 0

    def test_holds_for_indigenous_without_ceremony(self):
        result = pde_decompose("Deploy indigenous ceremony medicine wheel protocol.")
        perspective = PerspectiveAnalyzer().analyze(result["decomposition"])
        gate_result = self.gate.evaluate(result["decomposition"], perspective)
        if gate_result.ceremony_needed:
            assert gate_result.human_review_requested

    def test_provides_relational_score(self):
        result = pde_decompose("Research and build a module.")
        gate_result = self.gate.evaluate(result["decomposition"])
        assert 0 <= gate_result.relational_score <= 1

    def test_can_proceed_returns_bool(self):
        result = pde_decompose("Build a module.")
        assert isinstance(self.gate.can_proceed(result["decomposition"]), bool)

    def test_respects_custom_thresholds(self):
        strict_gate = CeremonyGate(balance_threshold=0.9, coherence_threshold=0.9)
        result = pde_decompose("Build a module.")
        gate_result = strict_gate.evaluate(result["decomposition"])
        assert len(gate_result.reasons) > 0
