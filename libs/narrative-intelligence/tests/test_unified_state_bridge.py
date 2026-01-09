"""
Tests for the Unified State Bridge.

Tests cover:
- Three-universe data structures
- State serialization/deserialization
- Factory functions
- State modification methods
- Redis key helpers
"""

import pytest
import json
import sys
import importlib.util
from datetime import datetime
from pathlib import Path

# Load the module directly to avoid langgraph dependency
spec = importlib.util.spec_from_file_location(
    "unified_state_bridge",
    Path(__file__).parent.parent / "narrative_intelligence/schemas/unified_state_bridge.py"
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

# Import from loaded module
Universe = module.Universe
NarrativePhase = module.NarrativePhase
NarrativeFunction = module.NarrativeFunction
UniversePerspective = module.UniversePerspective
ThreeUniverseAnalysis = module.ThreeUniverseAnalysis
NarrativePosition = module.NarrativePosition
StoryBeat = module.StoryBeat
CharacterState = module.CharacterState
ThematicThread = module.ThematicThread
RoutingDecision = module.RoutingDecision
UnifiedNarrativeState = module.UnifiedNarrativeState
create_new_narrative_state = module.create_new_narrative_state
create_beat_from_webhook = module.create_beat_from_webhook
get_default_characters = module.get_default_characters
get_default_themes = module.get_default_themes
RedisKeys = module.RedisKeys


class TestUniverse:
    """Tests for Universe enum"""
    
    def test_universe_values(self):
        """Test universe enum values"""
        assert Universe.ENGINEER.value == "engineer"
        assert Universe.CEREMONY.value == "ceremony"
        assert Universe.STORY_ENGINE.value == "story_engine"
    
    def test_universe_from_string(self):
        """Test creating universe from string"""
        assert Universe("engineer") == Universe.ENGINEER
        assert Universe("ceremony") == Universe.CEREMONY
        assert Universe("story_engine") == Universe.STORY_ENGINE


class TestUniversePerspective:
    """Tests for UniversePerspective"""
    
    def test_create_perspective(self):
        """Test creating a universe perspective"""
        perspective = UniversePerspective(
            universe=Universe.ENGINEER,
            intent="feature_request",
            confidence=0.85,
            suggested_flows=["tech_analyzer", "spec_writer"],
            context={"priority": "HIGH"}
        )
        
        assert perspective.universe == Universe.ENGINEER
        assert perspective.intent == "feature_request"
        assert perspective.confidence == 0.85
        assert "tech_analyzer" in perspective.suggested_flows
        assert perspective.context["priority"] == "HIGH"
    
    def test_perspective_serialization(self):
        """Test serialization round-trip"""
        original = UniversePerspective(
            universe=Universe.CEREMONY,
            intent="co_creation",
            confidence=0.7,
            suggested_flows=["sacred_pause"],
            context={"ke_relationships": ["developer", "user"]}
        )
        
        data = original.to_dict()
        restored = UniversePerspective.from_dict(data)
        
        assert restored.universe == original.universe
        assert restored.intent == original.intent
        assert restored.confidence == original.confidence
        assert restored.suggested_flows == original.suggested_flows
        assert restored.context == original.context


class TestThreeUniverseAnalysis:
    """Tests for ThreeUniverseAnalysis"""
    
    def test_create_analysis(self):
        """Test creating three-universe analysis"""
        engineer = UniversePerspective(Universe.ENGINEER, "feature_request", 0.8)
        ceremony = UniversePerspective(Universe.CEREMONY, "co_creation", 0.7)
        story = UniversePerspective(Universe.STORY_ENGINE, "inciting_incident", 0.95)
        
        analysis = ThreeUniverseAnalysis(
            engineer=engineer,
            ceremony=ceremony,
            story_engine=story,
            lead_universe=Universe.STORY_ENGINE,
            coherence_score=0.88
        )
        
        assert analysis.lead_universe == Universe.STORY_ENGINE
        assert analysis.coherence_score == 0.88
        assert analysis.engineer.intent == "feature_request"
    
    def test_get_perspective(self):
        """Test getting perspective by universe"""
        engineer = UniversePerspective(Universe.ENGINEER, "tech", 0.8)
        ceremony = UniversePerspective(Universe.CEREMONY, "relational", 0.7)
        story = UniversePerspective(Universe.STORY_ENGINE, "narrative", 0.9)
        
        analysis = ThreeUniverseAnalysis(
            engineer=engineer,
            ceremony=ceremony,
            story_engine=story,
            lead_universe=Universe.STORY_ENGINE,
            coherence_score=0.85
        )
        
        assert analysis.get_perspective(Universe.ENGINEER).intent == "tech"
        assert analysis.get_perspective(Universe.CEREMONY).intent == "relational"
        assert analysis.get_perspective(Universe.STORY_ENGINE).intent == "narrative"
    
    def test_analysis_serialization(self):
        """Test serialization round-trip"""
        engineer = UniversePerspective(Universe.ENGINEER, "feature", 0.8)
        ceremony = UniversePerspective(Universe.CEREMONY, "sacred", 0.7)
        story = UniversePerspective(Universe.STORY_ENGINE, "inciting", 0.95)
        
        original = ThreeUniverseAnalysis(
            engineer=engineer,
            ceremony=ceremony,
            story_engine=story,
            lead_universe=Universe.STORY_ENGINE,
            coherence_score=0.88
        )
        
        data = original.to_dict()
        json_str = json.dumps(data)
        restored_data = json.loads(json_str)
        restored = ThreeUniverseAnalysis.from_dict(restored_data)
        
        assert restored.lead_universe == original.lead_universe
        assert restored.coherence_score == original.coherence_score
        assert restored.engineer.intent == original.engineer.intent


class TestNarrativePosition:
    """Tests for NarrativePosition"""
    
    def test_default_position(self):
        """Test default position is Act 1 setup"""
        position = NarrativePosition(act=1, phase=NarrativePhase.SETUP)
        
        assert position.act == 1
        assert position.phase == NarrativePhase.SETUP
        assert position.beat_count == 0
        assert position.character_arc_strength == 0.5
    
    def test_position_serialization(self):
        """Test serialization round-trip"""
        original = NarrativePosition(
            act=2,
            phase=NarrativePhase.CONFRONTATION,
            current_beat_id="beat_5",
            beat_count=5,
            character_arc_strength=0.7,
            emotional_tone="tense",
            lead_universe=Universe.ENGINEER
        )
        
        data = original.to_dict()
        restored = NarrativePosition.from_dict(data)
        
        assert restored.act == original.act
        assert restored.phase == original.phase
        assert restored.current_beat_id == original.current_beat_id
        assert restored.lead_universe == original.lead_universe


class TestStoryBeat:
    """Tests for StoryBeat"""
    
    def test_create_beat(self):
        """Test creating a story beat"""
        beat = StoryBeat(
            id="beat_1",
            sequence=1,
            content="The hero discovers the ancient artifact.",
            narrative_function=NarrativeFunction.INCITING_INCIDENT,
            act=1,
            emotional_tone="discovery",
            thematic_tags=["destiny", "discovery"]
        )
        
        assert beat.id == "beat_1"
        assert beat.narrative_function == NarrativeFunction.INCITING_INCIDENT
        assert beat.emotional_tone == "discovery"
        assert "destiny" in beat.thematic_tags
    
    def test_beat_with_universe_analysis(self):
        """Test beat with three-universe analysis"""
        engineer = UniversePerspective(Universe.ENGINEER, "spec_created", 0.9)
        ceremony = UniversePerspective(Universe.CEREMONY, "intention_set", 0.8)
        story = UniversePerspective(Universe.STORY_ENGINE, "inciting_incident", 0.95)
        
        analysis = ThreeUniverseAnalysis(
            engineer=engineer,
            ceremony=ceremony,
            story_engine=story,
            lead_universe=Universe.STORY_ENGINE,
            coherence_score=0.9
        )
        
        beat = StoryBeat(
            id="beat_webhook_110",
            sequence=1,
            content="Issue #110: Live Story Monitor",
            narrative_function=NarrativeFunction.INCITING_INCIDENT,
            act=1,
            universe_analysis=analysis,
            lead_universe=Universe.STORY_ENGINE,
            source="webhook",
            source_event_id="github:110"
        )
        
        assert beat.universe_analysis is not None
        assert beat.universe_analysis.lead_universe == Universe.STORY_ENGINE
        assert beat.source == "webhook"
    
    def test_beat_serialization(self):
        """Test serialization round-trip"""
        original = StoryBeat(
            id="beat_test",
            sequence=5,
            content="Test content",
            narrative_function=NarrativeFunction.RISING_ACTION,
            act=2,
            emotional_tone="tense",
            character_id="protagonist_1",
            quality_score=0.85
        )
        
        data = original.to_dict()
        json_str = json.dumps(data)
        restored_data = json.loads(json_str)
        restored = StoryBeat.from_dict(restored_data)
        
        assert restored.id == original.id
        assert restored.content == original.content
        assert restored.quality_score == original.quality_score


class TestCharacterState:
    """Tests for CharacterState"""
    
    def test_create_character(self):
        """Test creating a character state"""
        character = CharacterState(
            id="mia_1",
            name="Mia",
            archetype="The Builder",
            universe=Universe.ENGINEER,
            initial_state="Focused on technical precision",
            current_state="Focused on technical precision"
        )
        
        assert character.name == "Mia"
        assert character.archetype == "The Builder"
        assert character.universe == Universe.ENGINEER
    
    def test_character_arc_position(self):
        """Test character arc tracking"""
        character = CharacterState(
            id="test_char",
            name="Test",
            archetype="Hero",
            universe=Universe.STORY_ENGINE,
            arc_position=0.3
        )
        
        assert character.arc_position == 0.3
        
        # Simulate arc progression
        character.arc_position = min(1.0, character.arc_position + 0.2)
        assert character.arc_position == 0.5


class TestUnifiedNarrativeState:
    """Tests for UnifiedNarrativeState"""
    
    def test_create_state(self):
        """Test creating unified state"""
        state = UnifiedNarrativeState(
            story_id="story_123",
            session_id="session_456"
        )
        
        assert state.story_id == "story_123"
        assert state.session_id == "session_456"
        assert state.position.act == 1
        assert state.position.phase == NarrativePhase.SETUP
        assert len(state.beats) == 0
    
    def test_add_beat(self):
        """Test adding beats to state"""
        state = UnifiedNarrativeState(
            story_id="story_123",
            session_id="session_456"
        )
        
        beat = StoryBeat(
            id="beat_1",
            sequence=1,
            content="First beat",
            narrative_function=NarrativeFunction.INCITING_INCIDENT,
            act=1
        )
        
        state.add_beat(beat)
        
        assert len(state.beats) == 1
        assert state.position.beat_count == 1
        assert state.position.current_beat_id == "beat_1"
    
    def test_state_serialization(self):
        """Test full state serialization"""
        state = create_new_narrative_state(
            story_id="story_test",
            session_id="session_test"
        )
        
        # Add a beat
        beat = StoryBeat(
            id="beat_1",
            sequence=1,
            content="Test beat",
            narrative_function=NarrativeFunction.INCITING_INCIDENT,
            act=1
        )
        state.add_beat(beat)
        
        # Serialize
        json_str = state.to_json()
        
        # Deserialize
        restored = UnifiedNarrativeState.from_json(json_str)
        
        assert restored.story_id == state.story_id
        assert restored.session_id == state.session_id
        assert len(restored.beats) == len(state.beats)
        assert len(restored.characters) == len(state.characters)
        assert len(restored.themes) == len(state.themes)
    
    def test_get_last_n_beats(self):
        """Test getting recent beats"""
        state = UnifiedNarrativeState(
            story_id="story_123",
            session_id="session_456"
        )
        
        # Add 10 beats
        for i in range(10):
            beat = StoryBeat(
                id=f"beat_{i}",
                sequence=i,
                content=f"Beat {i}",
                narrative_function=NarrativeFunction.BEAT,
                act=2
            )
            state.add_beat(beat)
        
        # Get last 3
        last_beats = state.get_last_n_beats(3)
        
        assert len(last_beats) == 3
        assert last_beats[-1].id == "beat_9"


class TestFactoryFunctions:
    """Tests for factory functions"""
    
    def test_create_new_narrative_state_with_defaults(self):
        """Test creating state with default characters and themes"""
        state = create_new_narrative_state(
            story_id="test_story",
            session_id="test_session"
        )
        
        # Check characters
        assert "the-builder" in state.characters
        assert "the-keeper" in state.characters
        assert "the-weaver" in state.characters
        assert state.characters["the-builder"].name == "Mia"
        assert state.characters["the-keeper"].name == "Ava8"
        assert state.characters["the-weaver"].name == "Miette"
        
        # Check themes
        assert "integration" in state.themes
        assert "collaboration" in state.themes
        assert "coherence" in state.themes
    
    def test_create_new_narrative_state_without_defaults(self):
        """Test creating state without defaults"""
        state = create_new_narrative_state(
            story_id="test_story",
            session_id="test_session",
            include_default_characters=False,
            include_default_themes=False
        )
        
        assert len(state.characters) == 0
        assert len(state.themes) == 0
    
    def test_get_default_characters(self):
        """Test default character archetypes"""
        characters = get_default_characters()
        
        assert len(characters) == 3
        
        # Check Mia (Engineer)
        mia = characters["the-builder"]
        assert mia.name == "Mia"
        assert mia.archetype == "The Builder"
        assert mia.universe == Universe.ENGINEER
        
        # Check Ava8 (Ceremony)
        ava = characters["the-keeper"]
        assert ava.name == "Ava8"
        assert ava.archetype == "The Keeper"
        assert ava.universe == Universe.CEREMONY
        
        # Check Miette (Story Engine)
        miette = characters["the-weaver"]
        assert miette.name == "Miette"
        assert miette.archetype == "The Weaver"
        assert miette.universe == Universe.STORY_ENGINE
    
    def test_create_beat_from_webhook(self):
        """Test creating beat from webhook event"""
        # Create analysis
        engineer = UniversePerspective(Universe.ENGINEER, "feature_request", 0.8)
        ceremony = UniversePerspective(Universe.CEREMONY, "co_creation", 0.7)
        story = UniversePerspective(
            Universe.STORY_ENGINE, 
            "inciting_incident", 
            0.95,
            context={"act": 1}
        )
        
        analysis = ThreeUniverseAnalysis(
            engineer=engineer,
            ceremony=ceremony,
            story_engine=story,
            lead_universe=Universe.STORY_ENGINE,
            coherence_score=0.88
        )
        
        # Create beat
        beat = create_beat_from_webhook(
            event_id="github:issues:110",
            content="Issue #110: Live Story Monitor",
            universe_analysis=analysis,
            sequence=1
        )
        
        assert beat.id == "beat_github:issues:110"
        assert beat.source == "webhook"
        assert beat.source_event_id == "github:issues:110"
        assert beat.narrative_function == NarrativeFunction.INCITING_INCIDENT
        assert beat.lead_universe == Universe.STORY_ENGINE


class TestRedisKeys:
    """Tests for Redis key helpers"""
    
    def test_state_key(self):
        """Test state key generation"""
        key = RedisKeys.state("session_123")
        assert key == "ncp:state:session_123"
    
    def test_current_state_key(self):
        """Test current state key"""
        key = RedisKeys.current_state()
        assert key == "ncp:state:current"
    
    def test_beats_key(self):
        """Test beats list key"""
        key = RedisKeys.beats("session_123")
        assert key == "ncp:beats:session_123"
    
    def test_beat_key(self):
        """Test individual beat key"""
        key = RedisKeys.beat("beat_456")
        assert key == "ncp:beat:beat_456"
    
    def test_event_analysis_key(self):
        """Test event analysis cache key"""
        key = RedisKeys.event_analysis("github:110")
        assert key == "ncp:event:github:110"
    
    def test_routing_history_key(self):
        """Test routing history key"""
        key = RedisKeys.routing_history("session_123")
        assert key == "ncp:routing:session_123"
    
    def test_episode_key(self):
        """Test episode key"""
        key = RedisKeys.episode("s01e07")
        assert key == "ncp:episode:s01e07"


class TestEpisodeManagement:
    """Tests for episode-related state management"""
    
    def test_should_create_new_episode_by_count(self):
        """Test episode boundary detection by beat count"""
        state = UnifiedNarrativeState(
            story_id="test",
            session_id="test"
        )
        
        # Add 12 beats (threshold for new episode)
        for i in range(12):
            beat = StoryBeat(
                id=f"beat_{i}",
                sequence=i,
                content=f"Beat {i}",
                narrative_function=NarrativeFunction.BEAT,
                act=2
            )
            state.add_beat(beat)
        
        assert state.should_create_new_episode() == True
    
    def test_should_create_new_episode_by_resolution(self):
        """Test episode boundary detection by resolution beat"""
        state = UnifiedNarrativeState(
            story_id="test",
            session_id="test"
        )
        
        # Add resolution beat
        beat = StoryBeat(
            id="beat_resolution",
            sequence=1,
            content="The story concludes",
            narrative_function=NarrativeFunction.RESOLUTION,
            act=3
        )
        state.add_beat(beat)
        
        assert state.should_create_new_episode() == True
    
    def test_start_new_episode(self):
        """Test starting new episode"""
        state = UnifiedNarrativeState(
            story_id="test",
            session_id="test"
        )
        
        # Add some beats
        for i in range(5):
            state.add_beat(StoryBeat(
                id=f"beat_{i}",
                sequence=i,
                content=f"Beat {i}",
                narrative_function=NarrativeFunction.BEAT,
                act=2
            ))
        
        # Start new episode
        state.start_new_episode("s01e02")
        
        assert state.current_episode_id == "s01e02"
        assert state.episode_beats_count == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
