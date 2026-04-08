"""
Tests for the Narrative Coherence Engine.

Tests the gap identification, coherence scoring, and Trinity assessment features.
"""

import pytest
from narrative_intelligence import (
    NarrativeCoherenceEngine,
    Gap,
    GapType,
    GapSeverity,
    RoutingTarget,
    ComponentScore,
    CoherenceScore,
    TrinityAssessment,
    StoryBeat,
    CharacterState,
    ThematicThread,
    NarrativeFunction,
)


class TestGapDataclasses:
    """Test the Gap and related dataclasses."""
    
    def test_gap_creation(self):
        """Test creating a Gap object."""
        gap = Gap(
            id="gap_1",
            gap_type=GapType.STRUCTURAL,
            severity=GapSeverity.CRITICAL,
            description="Missing climax beat",
            location={"beat_id": "beat_5"},
            suggested_route=RoutingTarget.STRUCTURIST,
        )
        
        assert gap.id == "gap_1"
        assert gap.gap_type == GapType.STRUCTURAL
        assert gap.severity == GapSeverity.CRITICAL
        assert gap.resolved is False
    
    def test_gap_to_dict(self):
        """Test Gap serialization."""
        gap = Gap(
            id="gap_1",
            gap_type=GapType.CHARACTER,
            severity=GapSeverity.MODERATE,
            description="Character disappears",
            location={"component": "character_consistency_score"},
            suggested_route=RoutingTarget.STORYTELLER,
        )
        
        result = gap.to_dict()
        assert result["type"] == "character"
        assert result["severity"] == "moderate"
        assert result["suggested_route"] == "storyteller"
    
    def test_component_score_creation(self):
        """Test creating a ComponentScore."""
        score = ComponentScore(
            score=75.0,
            status="good",
            issues=["Minor issue"],
            suggestions=["Try this"],
        )
        
        assert score.score == 75.0
        assert score.status == "good"
        assert len(score.issues) == 1
    
    def test_coherence_score_to_dict(self):
        """Test CoherenceScore serialization."""
        score = CoherenceScore(
            overall=80.0,
            narrative_flow=ComponentScore(85.0, "good"),
            character_consistency=ComponentScore(75.0, "good"),
            pacing=ComponentScore(70.0, "warning"),
            theme_saturation=ComponentScore(90.0, "good"),
            continuity=ComponentScore(80.0, "good"),
        )
        
        result = score.to_dict()
        assert result["overall"] == 80.0
        assert result["components"]["narrative_flow"]["score"] == 85.0
        assert "analyzed_at" in result
    
    def test_trinity_assessment_creation(self):
        """Test TrinityAssessment creation."""
        trinity = TrinityAssessment(
            mia="Structure is 85% sound.",
            miette="Emotional arcs resonate well.",
            ava8="Atmosphere needs grounding.",
            priorities=["Fix pacing in Act 2"],
        )
        
        assert "85%" in trinity.mia
        assert "resonate" in trinity.miette
        assert len(trinity.priorities) == 1


class TestNarrativeCoherenceEngine:
    """Test the NarrativeCoherenceEngine."""
    
    @pytest.fixture
    def engine(self):
        """Create an engine instance."""
        return NarrativeCoherenceEngine()
    
    @pytest.fixture
    def sample_beats(self):
        """Create sample story beats for testing."""
        return [
            StoryBeat(
                id="beat_1",
                sequence=1,
                content="The hero discovers a mysterious artifact",
                narrative_function=NarrativeFunction.INCITING_INCIDENT,
                act=1,
                emotional_tone="intriguing",
            ),
            StoryBeat(
                id="beat_2",
                sequence=2,
                content="First confrontation with the antagonist",
                narrative_function=NarrativeFunction.RISING_ACTION,
                act=1,
                emotional_tone="tense",
            ),
            StoryBeat(
                id="beat_3",
                sequence=3,
                content="The hero faces a crisis of faith",
                narrative_function=NarrativeFunction.CRISIS,
                act=2,
                emotional_tone="fearful",
            ),
            StoryBeat(
                id="beat_4",
                sequence=4,
                content="The climactic battle",
                narrative_function=NarrativeFunction.CLIMAX,
                act=3,
                emotional_tone="triumphant",
            ),
            StoryBeat(
                id="beat_5",
                sequence=5,
                content="Peace returns to the land",
                narrative_function=NarrativeFunction.RESOLUTION,
                act=3,
                emotional_tone="peaceful",
            ),
        ]
    
    @pytest.fixture
    def sample_characters(self):
        """Create sample characters for testing."""
        from narrative_intelligence import Universe
        return [
            CharacterState(
                id="hero",
                name="Elena",
                archetype="protagonist",
                universe=Universe.STORY_ENGINE,
                arc_position=0.5,
            ),
            CharacterState(
                id="villain",
                name="Marcus",
                archetype="antagonist",
                universe=Universe.STORY_ENGINE,
                arc_position=0.4,
            ),
        ]
    
    @pytest.fixture
    def sample_themes(self):
        """Create sample themes for testing."""
        return [
            ThematicThread(
                id="theme_1",
                name="Redemption",
                description="The journey toward redemption",
                strength=0.7,
            ),
            ThematicThread(
                id="theme_2",
                name="Trust",
                description="The building of trust",
                strength=0.5,
            ),
        ]
    
    def test_engine_initialization(self, engine):
        """Test engine creates properly."""
        assert engine is not None
        assert engine.strict_mode is False
    
    def test_engine_with_strict_mode(self):
        """Test engine in strict mode."""
        engine = NarrativeCoherenceEngine(strict_mode=True)
        assert engine.strict_mode is True
    
    def test_analyze_basic(self, engine, sample_beats):
        """Test basic analysis with just beats."""
        result = engine.analyze(sample_beats)
        
        assert "coherence_score" in result
        assert "gaps" in result
        assert "trinity_assessment" in result
        
        # Overall score should be reasonable for well-structured beats
        assert result["coherence_score"].overall >= 50.0
    
    def test_analyze_with_characters(self, engine, sample_beats, sample_characters):
        """Test analysis with beats and characters."""
        result = engine.analyze(sample_beats, characters=sample_characters)
        
        score = result["coherence_score"]
        assert score.character_consistency.score >= 50.0
    
    def test_analyze_with_themes(self, engine, sample_beats, sample_themes):
        """Test analysis with beats and themes."""
        result = engine.analyze(sample_beats, themes=sample_themes)
        
        score = result["coherence_score"]
        assert score.theme_saturation is not None
    
    def test_analyze_full(self, engine, sample_beats, sample_characters, sample_themes):
        """Test full analysis with all components."""
        result = engine.analyze(
            sample_beats,
            characters=sample_characters,
            themes=sample_themes
        )
        
        score = result["coherence_score"]
        assert score.overall >= 0.0
        assert score.overall <= 100.0
        
        # All components should have scores
        assert score.narrative_flow.score is not None
        assert score.character_consistency.score is not None
        assert score.pacing.score is not None
        assert score.theme_saturation.score is not None
        assert score.continuity.score is not None
    
    def test_analyze_includes_metadata(self, engine, sample_beats):
        """Test analysis with metadata included."""
        result = engine.analyze(sample_beats, include_metadata=True)
        
        # Should include all internal state keys
        assert "beats" in result
        assert "narrative_flow_score" in result
        assert "overall_score" in result
    
    def test_gap_identification_missing_setup(self, engine):
        """Test that missing setup beats are detected."""
        # Beats that jump straight to confrontation
        beats = [
            StoryBeat(
                id="beat_1",
                sequence=1,
                content="Intense battle",
                narrative_function=NarrativeFunction.CRISIS,
                act=2,
                emotional_tone="tense",
            ),
            StoryBeat(
                id="beat_2",
                sequence=2,
                content="Crisis point",
                narrative_function=NarrativeFunction.CRISIS,
                act=2,
                emotional_tone="fearful",
            ),
        ]
        
        result = engine.analyze(beats)
        
        # Should have low flow score due to missing setup
        assert result["coherence_score"].narrative_flow.score < 85.0
    
    def test_gap_identification_no_climax(self, engine):
        """Test that missing climax is detected."""
        # Beats without a climax
        beats = [
            StoryBeat(
                id="beat_1",
                sequence=1,
                content="Introduction",
                narrative_function=NarrativeFunction.INCITING_INCIDENT,
                act=1,
                emotional_tone="calm",
            ),
            StoryBeat(
                id="beat_2",
                sequence=2,
                content="Some development",
                narrative_function=NarrativeFunction.RISING_ACTION,
                act=1,
                emotional_tone="neutral",
            ),
            StoryBeat(
                id="beat_3",
                sequence=3,
                content="Resolution without climax",
                narrative_function=NarrativeFunction.RESOLUTION,
                act=3,
                emotional_tone="peaceful",
            ),
        ]
        
        result = engine.analyze(beats)
        
        # Pacing score should reflect missing climax
        pacing = result["coherence_score"].pacing
        assert any("climax" in issue.lower() for issue in pacing.issues)
    
    def test_trinity_assessment_generated(self, engine, sample_beats):
        """Test that Trinity assessment is generated."""
        result = engine.analyze(sample_beats)
        
        trinity = result["trinity_assessment"]
        assert trinity.mia is not None
        assert trinity.miette is not None
        assert trinity.ava8 is not None
        assert len(trinity.priorities) >= 0
    
    def test_routing_suggestions(self, engine, sample_beats):
        """Test gap routing suggestions."""
        result = engine.analyze(sample_beats)
        gaps = result["gaps"]
        
        if gaps:
            routing = engine.get_routing_suggestions(gaps)
            
            # Should have keys for all routing targets
            assert "storyteller" in routing
            assert "structurist" in routing
            assert "architect" in routing
            assert "author" in routing


class TestNarrativeFlowAnalysis:
    """Test narrative flow analysis specifically."""
    
    @pytest.fixture
    def engine(self):
        return NarrativeCoherenceEngine()
    
    def test_jarring_emotional_transition(self, engine):
        """Test detection of jarring emotional transitions."""
        beats = [
            StoryBeat(
                id="beat_1",
                sequence=1,
                content="Devastation",
                narrative_function=NarrativeFunction.CRISIS,
                act=2,
                emotional_tone="devastating",
            ),
            StoryBeat(
                id="beat_2",
                sequence=2,
                content="Sudden joy",
                narrative_function=NarrativeFunction.RESOLUTION,
                act=3,
                emotional_tone="joyful",
            ),
        ]
        
        result = engine.analyze(beats)
        flow = result["coherence_score"].narrative_flow
        
        # Should detect jarring transition
        assert any("jarring" in issue.lower() for issue in flow.issues) or flow.score < 85


class TestCharacterConsistencyAnalysis:
    """Test character consistency analysis."""
    
    @pytest.fixture
    def engine(self):
        return NarrativeCoherenceEngine()
    
    def test_empty_characters_handled(self, engine):
        """Test analysis with no characters."""
        beats = [
            StoryBeat(
                id="beat_1",
                sequence=1,
                content="Action",
                narrative_function=NarrativeFunction.INCITING_INCIDENT,
                act=1,
            ),
        ]
        
        result = engine.analyze(beats, characters=[])
        
        # Should still work but note the issue
        score = result["coherence_score"].character_consistency
        assert score.score == 50.0  # Default when no characters


class TestPacingAnalysis:
    """Test pacing analysis."""
    
    @pytest.fixture
    def engine(self):
        return NarrativeCoherenceEngine()
    
    def test_consecutive_high_tension(self, engine):
        """Test detection of too many consecutive high-tension beats."""
        beats = [
            StoryBeat(
                id=f"beat_{i}",
                sequence=i,
                content=f"Intense moment {i}",
                narrative_function=NarrativeFunction.CRISIS,
                act=2,
            )
            for i in range(1, 6)
        ]
        
        result = engine.analyze(beats)
        pacing = result["coherence_score"].pacing
        
        # Should note the consecutive tension
        assert pacing.score < 85 or any("consecutive" in issue.lower() for issue in pacing.issues)


class TestContinuityAnalysis:
    """Test continuity analysis."""
    
    @pytest.fixture
    def engine(self):
        return NarrativeCoherenceEngine()
    
    def test_duplicate_sequences_detected(self, engine):
        """Test detection of duplicate sequence numbers."""
        beats = [
            StoryBeat(id="beat_1", sequence=1, content="First", narrative_function=NarrativeFunction.BEAT, act=1),
            StoryBeat(id="beat_2", sequence=1, content="Duplicate sequence", narrative_function=NarrativeFunction.BEAT, act=1),  # Duplicate!
            StoryBeat(id="beat_3", sequence=2, content="Third", narrative_function=NarrativeFunction.BEAT, act=1),
        ]
        
        result = engine.analyze(beats)
        continuity = result["coherence_score"].continuity
        
        # Should detect duplicate
        assert any("duplicate" in issue.lower() for issue in continuity.issues)
    
    def test_out_of_order_sequences(self, engine):
        """Test detection of out-of-order sequences."""
        beats = [
            StoryBeat(id="beat_1", sequence=3, content="Should be third", narrative_function=NarrativeFunction.BEAT, act=1),
            StoryBeat(id="beat_2", sequence=1, content="Should be first", narrative_function=NarrativeFunction.BEAT, act=1),
            StoryBeat(id="beat_3", sequence=2, content="Should be second", narrative_function=NarrativeFunction.BEAT, act=1),
        ]
        
        result = engine.analyze(beats)
        continuity = result["coherence_score"].continuity
        
        # Should detect ordering issue
        assert any("order" in issue.lower() for issue in continuity.issues)


class TestGapTypes:
    """Test all gap type enumerations."""
    
    def test_all_gap_types_exist(self):
        """Verify all expected gap types exist."""
        assert GapType.STRUCTURAL.value == "structural"
        assert GapType.THEMATIC.value == "thematic"
        assert GapType.CHARACTER.value == "character"
        assert GapType.SENSORY.value == "sensory"
        assert GapType.CONTINUITY.value == "continuity"
    
    def test_all_severities_exist(self):
        """Verify all expected severities exist."""
        assert GapSeverity.CRITICAL.value == "critical"
        assert GapSeverity.MODERATE.value == "moderate"
        assert GapSeverity.MINOR.value == "minor"
    
    def test_all_routing_targets_exist(self):
        """Verify all expected routing targets exist."""
        assert RoutingTarget.STORYTELLER.value == "storyteller"
        assert RoutingTarget.STRUCTURIST.value == "structurist"
        assert RoutingTarget.ARCHITECT.value == "architect"
        assert RoutingTarget.AUTHOR.value == "author"


class TestGraphExecution:
    """Test the LangGraph workflow execution."""
    
    @pytest.fixture
    def engine(self):
        return NarrativeCoherenceEngine()
    
    def test_graph_builds(self, engine):
        """Test that the graph builds successfully."""
        graph = engine.build_graph()
        assert graph is not None
    
    def test_graph_can_invoke(self, engine):
        """Test that the graph can be invoked."""
        beats = [
            StoryBeat(id="beat_1", sequence=1, content="Test beat", narrative_function=NarrativeFunction.BEAT, act=1),
        ]
        
        result = engine.analyze(beats)
        assert result is not None
        assert "coherence_score" in result
