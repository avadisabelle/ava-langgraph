"""
Tests for the Redis State Manager.

Tests cover:
- State persistence and retrieval
- Beat management
- Event analysis caching
- Routing history tracking
- Episode management
- Mock Redis functionality
"""

import pytest
import asyncio
import json
import sys
import importlib.util
from pathlib import Path

# Load unified_state_bridge first
spec = importlib.util.spec_from_file_location(
    "unified_state_bridge",
    Path(__file__).parent.parent / "narrative_intelligence/schemas/unified_state_bridge.py"
)
usb_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(usb_module)

# Load redis_state module
spec2 = importlib.util.spec_from_file_location(
    "redis_state",
    Path(__file__).parent.parent / "narrative_intelligence/integrations/redis_state.py"
)
redis_module = importlib.util.module_from_spec(spec2)
# Inject the usb_module into sys.modules so redis_state can import from it
sys.modules['narrative_intelligence.schemas.unified_state_bridge'] = usb_module
spec2.loader.exec_module(redis_module)

# Import types
Universe = usb_module.Universe
NarrativeFunction = usb_module.NarrativeFunction
NarrativePhase = usb_module.NarrativePhase
UniversePerspective = usb_module.UniversePerspective
ThreeUniverseAnalysis = usb_module.ThreeUniverseAnalysis
NarrativePosition = usb_module.NarrativePosition
StoryBeat = usb_module.StoryBeat
RoutingDecision = usb_module.RoutingDecision
UnifiedNarrativeState = usb_module.UnifiedNarrativeState
create_new_narrative_state = usb_module.create_new_narrative_state

# Import from redis_state
RedisConfig = redis_module.RedisConfig
NarrativeRedisManager = redis_module.NarrativeRedisManager
MockRedis = redis_module.MockRedis


@pytest.fixture
def redis_config():
    """Create a test Redis config"""
    return RedisConfig(
        host="localhost",
        port=6379,
        state_ttl_hours=24,
        beat_ttl_hours=168
    )


@pytest.fixture
def manager(redis_config):
    """Create a manager with mock Redis"""
    mgr = NarrativeRedisManager(redis_config)
    mgr._redis = MockRedis()  # Use mock instead of real connection
    mgr._connected = True
    return mgr


class TestMockRedis:
    """Tests for MockRedis implementation"""
    
    @pytest.mark.asyncio
    async def test_basic_get_set(self):
        """Test basic get/set operations"""
        redis = MockRedis()
        
        await redis.set("key1", "value1")
        result = await redis.get("key1")
        
        assert result == "value1"
    
    @pytest.mark.asyncio
    async def test_setex_with_ttl(self):
        """Test setex with TTL"""
        redis = MockRedis()
        
        await redis.setex("key1", 3600, "value1")
        result = await redis.get("key1")
        
        assert result == "value1"
    
    @pytest.mark.asyncio
    async def test_list_operations(self):
        """Test list push and range"""
        redis = MockRedis()
        
        await redis.rpush("list1", "item1")
        await redis.rpush("list1", "item2")
        await redis.rpush("list1", "item3")
        
        # Get all items
        items = await redis.lrange("list1", 0, -1)
        assert items == ["item1", "item2", "item3"]
        
        # Get last 2
        items = await redis.lrange("list1", -2, -1)
        assert items == ["item2", "item3"]
    
    @pytest.mark.asyncio
    async def test_delete(self):
        """Test key deletion"""
        redis = MockRedis()
        
        await redis.set("key1", "value1")
        await redis.set("key2", "value2")
        
        count = await redis.delete("key1", "key2")
        assert count == 2
        
        result = await redis.get("key1")
        assert result is None


class TestNarrativeRedisManager:
    """Tests for NarrativeRedisManager"""
    
    @pytest.mark.asyncio
    async def test_get_or_create_state(self, manager):
        """Test getting or creating state"""
        state = await manager.get_or_create_state(
            story_id="story_123",
            session_id="session_456"
        )
        
        assert state.story_id == "story_123"
        assert state.session_id == "session_456"
        assert "the-builder" in state.characters  # Default characters included
    
    @pytest.mark.asyncio
    async def test_save_and_retrieve_state(self, manager):
        """Test saving and retrieving state"""
        # Create state
        original = create_new_narrative_state(
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
        original.add_beat(beat)
        
        # Save
        success = await manager.save_state(original)
        assert success is True
        
        # Retrieve
        retrieved = await manager.get_state("session_test")
        assert retrieved is not None
        assert retrieved.story_id == original.story_id
        assert len(retrieved.beats) == 1
    
    @pytest.mark.asyncio
    async def test_add_beat(self, manager):
        """Test adding beats via manager"""
        # First create a state
        await manager.get_or_create_state(
            story_id="story_test",
            session_id="session_beat_test"
        )
        
        # Add a beat
        beat = StoryBeat(
            id="beat_via_manager",
            sequence=1,
            content="Beat added via manager",
            narrative_function=NarrativeFunction.RISING_ACTION,
            act=2
        )
        
        success = await manager.add_beat("session_beat_test", beat)
        assert success is True
        
        # Verify beat was added to state
        state = await manager.get_state("session_beat_test")
        assert len(state.beats) == 1
        assert state.beats[0].id == "beat_via_manager"
    
    @pytest.mark.asyncio
    async def test_get_beat(self, manager):
        """Test retrieving individual beat"""
        # Create state and add beat
        await manager.get_or_create_state(
            story_id="story_test",
            session_id="session_get_beat"
        )
        
        beat = StoryBeat(
            id="beat_to_get",
            sequence=1,
            content="Retrievable beat",
            narrative_function=NarrativeFunction.BEAT,
            act=2
        )
        
        await manager.add_beat("session_get_beat", beat)
        
        # Retrieve beat directly
        retrieved = await manager.get_beat("beat_to_get")
        assert retrieved is not None
        assert retrieved.content == "Retrievable beat"
    
    @pytest.mark.asyncio
    async def test_cache_event_analysis(self, manager):
        """Test caching three-universe analysis"""
        # Create analysis
        engineer = UniversePerspective(Universe.ENGINEER, "feature", 0.8)
        ceremony = UniversePerspective(Universe.CEREMONY, "sacred", 0.7)
        story = UniversePerspective(Universe.STORY_ENGINE, "inciting", 0.95)
        
        analysis = ThreeUniverseAnalysis(
            engineer=engineer,
            ceremony=ceremony,
            story_engine=story,
            lead_universe=Universe.STORY_ENGINE,
            coherence_score=0.88
        )
        
        # Cache it
        success = await manager.cache_event_analysis("github:110", analysis)
        assert success is True
        
        # Retrieve it
        cached = await manager.get_cached_analysis("github:110")
        assert cached is not None
        assert cached.lead_universe == Universe.STORY_ENGINE
        assert cached.coherence_score == 0.88
    
    @pytest.mark.asyncio
    async def test_get_recent_beats(self, manager):
        """Test getting recent beats"""
        # Create state
        await manager.get_or_create_state(
            story_id="story_test",
            session_id="session_recent"
        )
        
        # Add multiple beats
        for i in range(5):
            beat = StoryBeat(
                id=f"beat_{i}",
                sequence=i,
                content=f"Beat {i}",
                narrative_function=NarrativeFunction.BEAT,
                act=2
            )
            await manager.add_beat("session_recent", beat)
        
        # Get last 3
        recent = await manager.get_recent_beats("session_recent", count=3)
        
        assert len(recent) == 3
        assert recent[0].id == "beat_4"  # Most recent first
    
    @pytest.mark.asyncio
    async def test_record_routing_decision(self, manager):
        """Test recording routing decisions"""
        # Create state
        await manager.get_or_create_state(
            story_id="story_test",
            session_id="session_routing"
        )
        
        # Create analysis
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
        
        position = NarrativePosition(act=2, phase=NarrativePhase.CONFRONTATION)
        
        decision = RoutingDecision(
            id="decision_1",
            backend="flowise",
            flow="character_deepener",
            universe_analysis=analysis,
            narrative_position=position,
            score=0.92,
            method="narrative"
        )
        
        success = await manager.record_routing_decision("session_routing", decision)
        assert success is True
        
        # Retrieve history
        history = await manager.get_routing_history("session_routing")
        assert len(history) == 1
        assert history[0].backend == "flowise"
    
    @pytest.mark.asyncio
    async def test_start_new_episode(self, manager):
        """Test starting new episode"""
        # Create state with some beats
        await manager.get_or_create_state(
            story_id="story_test",
            session_id="session_episode"
        )
        
        for i in range(5):
            beat = StoryBeat(
                id=f"beat_{i}",
                sequence=i,
                content=f"Beat {i}",
                narrative_function=NarrativeFunction.BEAT,
                act=2
            )
            await manager.add_beat("session_episode", beat)
        
        # Start new episode
        success = await manager.start_new_episode("session_episode", "s01e02")
        assert success is True
        
        # Verify
        state = await manager.get_state("session_episode")
        assert state.current_episode_id == "s01e02"
        assert state.episode_beats_count == 0
    
    @pytest.mark.asyncio
    async def test_health_check(self, manager):
        """Test health check"""
        health = await manager.health_check()
        
        assert health["status"] == "healthy"
        assert health["connected"] is True
        assert "latency_ms" in health
    
    @pytest.mark.asyncio
    async def test_delete_session(self, manager):
        """Test session deletion"""
        # Create state with beats
        await manager.get_or_create_state(
            story_id="story_delete",
            session_id="session_to_delete"
        )
        
        beat = StoryBeat(
            id="beat_delete",
            sequence=1,
            content="To be deleted",
            narrative_function=NarrativeFunction.BEAT,
            act=2
        )
        await manager.add_beat("session_to_delete", beat)
        
        # Verify it exists
        state = await manager.get_state("session_to_delete")
        assert state is not None
        
        # Delete
        success = await manager.delete_session("session_to_delete")
        assert success is True
        
        # Verify it's gone
        state = await manager.get_state("session_to_delete")
        assert state is None


class TestIntegrationScenario:
    """Integration tests simulating real workflow"""
    
    @pytest.mark.asyncio
    async def test_webhook_to_beat_flow(self, manager):
        """Test complete flow: webhook event → three-universe analysis → story beat"""
        session_id = "session_webhook_flow"
        
        # 1. Create initial state
        state = await manager.get_or_create_state(
            story_id="multiverse_live_story",
            session_id=session_id
        )
        
        # 2. Simulate webhook event analysis
        engineer = UniversePerspective(
            Universe.ENGINEER,
            "feature_request",
            0.8,
            suggested_flows=["tech_analyzer"],
            context={"priority": "HIGH"}
        )
        ceremony = UniversePerspective(
            Universe.CEREMONY,
            "co_creation",
            0.7,
            suggested_flows=["relational_audit"],
            context={"seven_generation_impact": "HIGH"}
        )
        story = UniversePerspective(
            Universe.STORY_ENGINE,
            "inciting_incident",
            0.95,
            suggested_flows=["narrative_analyzer"],
            context={"act": 1, "throughline": "Three worlds must learn to see together"}
        )
        
        analysis = ThreeUniverseAnalysis(
            engineer=engineer,
            ceremony=ceremony,
            story_engine=story,
            lead_universe=Universe.STORY_ENGINE,
            coherence_score=0.88
        )
        
        # Cache the analysis
        await manager.cache_event_analysis("github:issue:110", analysis)
        
        # 3. Create story beat from webhook
        beat = StoryBeat(
            id="beat_github_110",
            sequence=1,
            content="Issue #110: Live Story Monitor feature request",
            narrative_function=NarrativeFunction.INCITING_INCIDENT,
            act=1,
            universe_analysis=analysis,
            lead_universe=Universe.STORY_ENGINE,
            source="webhook",
            source_event_id="github:issue:110"
        )
        
        await manager.add_beat(session_id, beat)
        
        # 4. Record routing decision
        position = NarrativePosition(act=1, phase=NarrativePhase.SETUP)
        decision = RoutingDecision(
            id="routing_110",
            backend="langflow",
            flow="narrative_analyzer",
            universe_analysis=analysis,
            narrative_position=position,
            score=0.95,
            method="narrative",
            success=True
        )
        
        await manager.record_routing_decision(session_id, decision)
        
        # 5. Verify complete state
        final_state = await manager.get_state(session_id)
        
        assert len(final_state.beats) == 1
        assert final_state.beats[0].source == "webhook"
        assert final_state.beats[0].universe_analysis.lead_universe == Universe.STORY_ENGINE
        assert len(final_state.routing_decisions) == 1
        assert final_state.routing_decisions[0].flow == "narrative_analyzer"
        
        # 6. Verify cached analysis
        cached = await manager.get_cached_analysis("github:issue:110")
        assert cached.coherence_score == 0.88


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
