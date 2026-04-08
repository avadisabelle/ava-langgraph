"""
Tests for NarrativeCheckpointSaver

Tests the integration between LangGraph's checkpoint system and
narrative intelligence state management.
"""

import pytest
from datetime import datetime, timezone
from typing import Dict, Any, Iterator, Optional, Sequence
from dataclasses import dataclass
from collections.abc import AsyncIterator

# Import our modules
from narrative_intelligence.checkpoint.narrative_checkpointer import (
    NarrativeCheckpointSaver,
    NarrativeCheckpointConfig,
    NarrativeCheckpointMetadata,
    create_narrative_checkpoint_metadata,
    HAS_LANGGRAPH,
)
from narrative_intelligence.schemas.unified_state_bridge import (
    UnifiedNarrativeState,
    StoryBeat,
    NarrativePosition,
    NarrativePhase,
    NarrativeFunction,
    Universe,
    ThreeUniverseAnalysis,
    UniversePerspective,
    create_new_narrative_state,
)


# === Mock Classes for Testing Without Full LangGraph ===

class MockCheckpoint:
    """Mock checkpoint for testing."""
    
    def __init__(self, channel_values: Dict[str, Any] = None):
        self._data = {
            "v": 1,
            "id": "test-checkpoint-id",
            "ts": datetime.now(timezone.utc).isoformat(),
            "channel_values": channel_values or {},
            "channel_versions": {},
            "versions_seen": {},
            "updated_channels": None,
        }
    
    def get(self, key: str, default=None):
        return self._data.get(key, default)
    
    def __getitem__(self, key: str):
        return self._data[key]


class MockCheckpointMetadata(dict):
    """Mock checkpoint metadata - dict-like for compatibility."""
    
    def __init__(self, source: str = "loop", step: int = 0):
        super().__init__(source=source, step=step, parents={})


class MockCheckpointTuple:
    """Mock checkpoint tuple."""
    
    def __init__(self, config, checkpoint, metadata, parent_config=None):
        self.config = config
        self.checkpoint = checkpoint
        self.metadata = metadata
        self.parent_config = parent_config
        self.pending_writes = None


class MockBaseSaver:
    """Mock base checkpoint saver for testing."""
    
    def __init__(self):
        self._checkpoints: Dict[str, MockCheckpointTuple] = {}
        self._writes: Dict[str, list] = {}
        self.serde = None  # Mock serializer
    
    @property
    def config_specs(self):
        return []
    
    def get_tuple(self, config):
        thread_id = config.get("configurable", {}).get("thread_id", "default")
        return self._checkpoints.get(thread_id)
    
    def list(self, config, *, filter=None, before=None, limit=None) -> Iterator:
        checkpoints = list(self._checkpoints.values())
        
        # Apply filter
        if filter:
            filtered = []
            for cp in checkpoints:
                matches = True
                for key, value in filter.items():
                    if cp.metadata.get(key) != value:
                        matches = False
                        break
                if matches:
                    filtered.append(cp)
            checkpoints = filtered
        
        # Apply limit
        if limit:
            checkpoints = checkpoints[:limit]
        
        return iter(checkpoints)
    
    def put(self, config, checkpoint, metadata, new_versions):
        thread_id = config.get("configurable", {}).get("thread_id", "default")
        
        # Store metadata as dict for later access
        metadata_dict = dict(metadata) if hasattr(metadata, 'items') else metadata
        
        self._checkpoints[thread_id] = MockCheckpointTuple(
            config=config,
            checkpoint=checkpoint,
            metadata=metadata_dict,
        )
        return config
    
    def put_writes(self, config, writes, task_id, task_path=""):
        thread_id = config.get("configurable", {}).get("thread_id", "default")
        if thread_id not in self._writes:
            self._writes[thread_id] = []
        self._writes[thread_id].extend(writes)
    
    def delete_thread(self, thread_id: str):
        if thread_id in self._checkpoints:
            del self._checkpoints[thread_id]
        if thread_id in self._writes:
            del self._writes[thread_id]
    
    # Async versions
    async def aget_tuple(self, config):
        return self.get_tuple(config)
    
    async def alist(self, config, *, filter=None, before=None, limit=None):
        for item in self.list(config, filter=filter, before=before, limit=limit):
            yield item
    
    async def aput(self, config, checkpoint, metadata, new_versions):
        return self.put(config, checkpoint, metadata, new_versions)
    
    async def aput_writes(self, config, writes, task_id, task_path=""):
        self.put_writes(config, writes, task_id, task_path)
    
    async def adelete_thread(self, thread_id: str):
        self.delete_thread(thread_id)


# === Fixtures ===

@pytest.fixture
def mock_base_saver():
    """Create a mock base checkpoint saver."""
    return MockBaseSaver()


@pytest.fixture
def narrative_config():
    """Create a narrative checkpoint configuration."""
    return NarrativeCheckpointConfig(
        checkpoint_frequency=1,
        store_full_beats=True,
        max_beats_in_metadata=10,
        enable_cross_session_tracking=True,
        checkpoint_on_act_transition=True,
        checkpoint_on_episode_boundary=True,
    )


@pytest.fixture
def narrative_saver(mock_base_saver, narrative_config):
    """Create a narrative checkpoint saver with mock base."""
    # Patch HAS_LANGGRAPH for testing
    import narrative_intelligence.checkpoint.narrative_checkpointer as module
    original = module.HAS_LANGGRAPH
    module.HAS_LANGGRAPH = True
    
    saver = NarrativeCheckpointSaver(
        base_saver=mock_base_saver,
        config=narrative_config,
        narrative_state_channel="narrative_state",
    )
    
    # Restore
    module.HAS_LANGGRAPH = original
    return saver


@pytest.fixture
def sample_narrative_state():
    """Create a sample UnifiedNarrativeState."""
    state = create_new_narrative_state(
        story_id="test-story",
        session_id="test-session-123",
    )
    state.current_episode_id = "s01e01"
    
    # Add a beat
    beat = StoryBeat(
        id="beat-001",
        sequence=1,
        content="Test webhook event",
        narrative_function=NarrativeFunction.RISING_ACTION,
        act=2,
        source="test",
    )
    state.beats.append(beat)
    
    # Update position
    state.position.act = 2
    state.position.phase = NarrativePhase.CONFRONTATION
    
    return state


# === Tests ===

class TestCreateNarrativeCheckpointMetadata:
    """Tests for create_narrative_checkpoint_metadata function."""
    
    def test_basic_metadata_creation(self):
        """Test creating metadata without narrative state."""
        base = {"source": "loop", "step": 5, "parents": {}}
        
        result = create_narrative_checkpoint_metadata(base)
        
        assert result["source"] == "loop"
        assert result["step"] == 5
        assert result["narrative_checkpoint_type"] == "beat"
    
    def test_metadata_with_narrative_state(self, sample_narrative_state):
        """Test creating metadata with narrative state."""
        base = {"source": "loop", "step": 10}
        
        result = create_narrative_checkpoint_metadata(
            base_metadata=base,
            narrative_state=sample_narrative_state,
            checkpoint_type="beat",
        )
        
        assert result["narrative_session_id"] == "test-session-123"
        assert result["narrative_episode_id"] == "s01e01"
        assert result["narrative_act"] == 2
        assert "confrontation" in result["narrative_phase"].lower()
        assert result["narrative_beat_count"] == 1
    
    def test_metadata_with_webhook_correlation(self, sample_narrative_state):
        """Test metadata includes webhook correlation ID."""
        base = {"source": "input", "step": 0}
        
        result = create_narrative_checkpoint_metadata(
            base_metadata=base,
            narrative_state=sample_narrative_state,
            webhook_correlation_id="gh-webhook-abc123",
        )
        
        assert result["webhook_correlation_id"] == "gh-webhook-abc123"
    
    def test_metadata_checkpoint_types(self, sample_narrative_state):
        """Test different checkpoint types."""
        base = {"source": "loop", "step": 1}
        
        for checkpoint_type in ["beat", "act_transition", "episode_boundary"]:
            result = create_narrative_checkpoint_metadata(
                base_metadata=base,
                narrative_state=sample_narrative_state,
                checkpoint_type=checkpoint_type,
            )
            assert result["narrative_checkpoint_type"] == checkpoint_type


class TestNarrativeCheckpointConfig:
    """Tests for NarrativeCheckpointConfig."""
    
    def test_default_config(self):
        """Test default configuration values."""
        config = NarrativeCheckpointConfig()
        
        assert config.checkpoint_frequency == 1
        assert config.store_full_beats is True
        assert config.max_beats_in_metadata == 10
        assert config.enable_cross_session_tracking is True
        assert config.checkpoint_on_act_transition is True
        assert config.checkpoint_on_episode_boundary is True
    
    def test_custom_config(self):
        """Test custom configuration."""
        config = NarrativeCheckpointConfig(
            checkpoint_frequency=5,
            store_full_beats=False,
            max_beats_in_metadata=3,
        )
        
        assert config.checkpoint_frequency == 5
        assert config.store_full_beats is False
        assert config.max_beats_in_metadata == 3


class TestNarrativeCheckpointSaver:
    """Tests for NarrativeCheckpointSaver."""
    
    def test_initialization(self, mock_base_saver, narrative_config):
        """Test saver initialization."""
        import narrative_intelligence.checkpoint.narrative_checkpointer as module
        module.HAS_LANGGRAPH = True
        
        saver = NarrativeCheckpointSaver(
            base_saver=mock_base_saver,
            config=narrative_config,
        )
        
        assert saver._base_saver is mock_base_saver
        assert saver._config is narrative_config
        assert saver._narrative_channel == "narrative_state"
    
    def test_put_checkpoint_basic(self, narrative_saver, mock_base_saver):
        """Test storing a basic checkpoint."""
        config = {"configurable": {"thread_id": "thread-1"}}
        checkpoint = MockCheckpoint()
        metadata = MockCheckpointMetadata(source="loop", step=1)
        new_versions = {}
        
        result = narrative_saver.put(config, checkpoint, metadata, new_versions)
        
        assert result == config
        assert "thread-1" in mock_base_saver._checkpoints
    
    def test_put_checkpoint_with_narrative_state(
        self, narrative_saver, mock_base_saver, sample_narrative_state
    ):
        """Test storing checkpoint with narrative state extracts metadata."""
        config = {"configurable": {"thread_id": "thread-2"}}
        checkpoint = MockCheckpoint(
            channel_values={"narrative_state": sample_narrative_state}
        )
        metadata = MockCheckpointMetadata(source="loop", step=5)
        new_versions = {}
        
        narrative_saver.put(config, checkpoint, metadata, new_versions)
        
        stored = mock_base_saver._checkpoints["thread-2"]
        assert stored.metadata.get("narrative_session_id") == "test-session-123"
        assert stored.metadata.get("narrative_act") == 2
    
    def test_put_checkpoint_with_webhook_correlation(
        self, narrative_saver, mock_base_saver
    ):
        """Test webhook correlation ID is preserved."""
        config = {
            "configurable": {
                "thread_id": "thread-3",
                "webhook_correlation_id": "webhook-xyz",
            }
        }
        checkpoint = MockCheckpoint()
        metadata = MockCheckpointMetadata()
        
        narrative_saver.put(config, checkpoint, metadata, {})
        
        stored = mock_base_saver._checkpoints["thread-3"]
        assert stored.metadata.get("webhook_correlation_id") == "webhook-xyz"
    
    def test_get_tuple(self, narrative_saver, mock_base_saver):
        """Test retrieving a checkpoint tuple."""
        # Store first
        config = {"configurable": {"thread_id": "thread-get"}}
        checkpoint = MockCheckpoint()
        metadata = MockCheckpointMetadata()
        narrative_saver.put(config, checkpoint, metadata, {})
        
        # Retrieve
        result = narrative_saver.get_tuple(config)
        
        assert result is not None
        assert result.config == config
    
    def test_list_checkpoints(self, narrative_saver, mock_base_saver):
        """Test listing checkpoints."""
        # Store multiple
        for i in range(3):
            config = {"configurable": {"thread_id": f"thread-list-{i}"}}
            checkpoint = MockCheckpoint()
            metadata = MockCheckpointMetadata(step=i)
            narrative_saver.put(config, checkpoint, metadata, {})
        
        # List all
        results = list(narrative_saver.list(config=None))
        
        assert len(results) == 3
    
    def test_list_with_limit(self, narrative_saver, mock_base_saver):
        """Test listing with limit."""
        for i in range(5):
            config = {"configurable": {"thread_id": f"thread-limit-{i}"}}
            narrative_saver.put(config, MockCheckpoint(), MockCheckpointMetadata(), {})
        
        results = list(narrative_saver.list(config=None, limit=2))
        
        assert len(results) == 2
    
    def test_delete_thread(self, narrative_saver, mock_base_saver):
        """Test deleting a thread."""
        config = {"configurable": {"thread_id": "thread-delete"}}
        narrative_saver.put(config, MockCheckpoint(), MockCheckpointMetadata(), {})
        
        assert "thread-delete" in mock_base_saver._checkpoints
        
        narrative_saver.delete_thread("thread-delete")
        
        assert "thread-delete" not in mock_base_saver._checkpoints
    
    def test_extract_narrative_state_from_dict(self, narrative_saver):
        """Test extracting narrative state from dict format."""
        state_dict = {
            "story_id": "test-story",
            "session_id": "dict-session",
            "current_episode_id": "s01e01",
            "position": {
                "act": 1,
                "phase": "setup",
            },
            "beats": [],
            "characters": {},
            "themes": {},
            "routing_decisions": [],
        }
        
        checkpoint = MockCheckpoint(channel_values={"narrative_state": state_dict})
        
        result = narrative_saver._extract_narrative_state(checkpoint)
        
        assert result is not None
        assert result.session_id == "dict-session"
    
    def test_extract_narrative_state_from_object(
        self, narrative_saver, sample_narrative_state
    ):
        """Test extracting narrative state from UnifiedNarrativeState object."""
        checkpoint = MockCheckpoint(
            channel_values={"narrative_state": sample_narrative_state}
        )
        
        result = narrative_saver._extract_narrative_state(checkpoint)
        
        assert result is sample_narrative_state


class TestNarrativeQueryMethods:
    """Tests for narrative-specific query methods."""
    
    def test_list_by_narrative_session(self, narrative_saver, mock_base_saver):
        """Test filtering by narrative session."""
        # Store checkpoints with different sessions
        for i, session in enumerate(["session-a", "session-a", "session-b"]):
            config = {"configurable": {"thread_id": f"thread-sess-{i}"}}
            state = create_new_narrative_state(story_id="test-story", session_id=session)
            checkpoint = MockCheckpoint(channel_values={"narrative_state": state})
            narrative_saver.put(config, checkpoint, MockCheckpointMetadata(), {})
        
        results = list(narrative_saver.list_by_narrative_session("session-a"))
        
        assert len(results) == 2
    
    def test_list_by_episode(self, narrative_saver, mock_base_saver):
        """Test filtering by episode."""
        for i, episode in enumerate(["s01e01", "s01e02", "s01e01"]):
            config = {"configurable": {"thread_id": f"thread-ep-{i}"}}
            state = create_new_narrative_state(
                story_id="test-story",
                session_id=f"session-{i}",
            )
            state.current_episode_id = episode
            checkpoint = MockCheckpoint(channel_values={"narrative_state": state})
            narrative_saver.put(config, checkpoint, MockCheckpointMetadata(), {})
        
        results = list(narrative_saver.list_by_episode("s01e01"))
        
        assert len(results) == 2
    
    def test_list_by_webhook_correlation(self, narrative_saver, mock_base_saver):
        """Test filtering by webhook correlation ID."""
        # Store with different correlations
        for i, corr_id in enumerate(["corr-1", "corr-1", "corr-2"]):
            config = {
                "configurable": {
                    "thread_id": f"thread-corr-{i}",
                    "webhook_correlation_id": corr_id,
                }
            }
            narrative_saver.put(config, MockCheckpoint(), MockCheckpointMetadata(), {})
        
        results = list(narrative_saver.list_by_webhook_correlation("corr-1"))
        
        assert len(results) == 2
    
    def test_get_narrative_history(self, narrative_saver, mock_base_saver):
        """Test getting narrative history."""
        # Store checkpoints with progression
        for i in range(3):
            config = {"configurable": {"thread_id": f"thread-hist-{i}"}}
            state = create_new_narrative_state(story_id="test-story", session_id="history-session")
            state.position.act = i + 1
            # Add some beats
            for j in range(i * 5):
                beat = StoryBeat(
                    id=f"beat-{i}-{j}",
                    sequence=j,
                    content=f"Beat {j}",
                    narrative_function=NarrativeFunction.RISING_ACTION,
                    act=i + 1,
                )
                state.beats.append(beat)
            checkpoint = MockCheckpoint(channel_values={"narrative_state": state})
            metadata = MockCheckpointMetadata(step=i)
            narrative_saver.put(config, checkpoint, metadata, {})
        
        history = narrative_saver.get_narrative_history(
            config=None,
            max_checkpoints=10,
        )
        
        assert len(history) == 3
        # Check history entries have expected fields
        for entry in history:
            assert "checkpoint_id" in entry
            assert "timestamp" in entry
            assert "narrative_act" in entry


class TestAsyncMethods:
    """Tests for async checkpoint methods."""
    
    @pytest.mark.asyncio
    async def test_async_put_and_get(self, narrative_saver, mock_base_saver):
        """Test async put and get."""
        config = {"configurable": {"thread_id": "async-thread"}}
        checkpoint = MockCheckpoint()
        metadata = MockCheckpointMetadata()
        
        await narrative_saver.aput(config, checkpoint, metadata, {})
        
        result = await narrative_saver.aget_tuple(config)
        
        assert result is not None
    
    @pytest.mark.asyncio
    async def test_async_list(self, narrative_saver, mock_base_saver):
        """Test async list."""
        # Store some checkpoints
        for i in range(2):
            config = {"configurable": {"thread_id": f"async-list-{i}"}}
            await narrative_saver.aput(
                config, MockCheckpoint(), MockCheckpointMetadata(), {}
            )
        
        results = []
        async for item in narrative_saver.alist(config=None):
            results.append(item)
        
        assert len(results) == 2
    
    @pytest.mark.asyncio
    async def test_async_delete(self, narrative_saver, mock_base_saver):
        """Test async delete."""
        config = {"configurable": {"thread_id": "async-delete"}}
        await narrative_saver.aput(config, MockCheckpoint(), MockCheckpointMetadata(), {})
        
        await narrative_saver.adelete_thread("async-delete")
        
        result = await narrative_saver.aget_tuple(config)
        assert result is None


class TestCheckpointTypeDetection:
    """Tests for checkpoint type detection logic."""
    
    def test_detects_act_transition(self, narrative_saver):
        """Test detection of act transitions."""
        # First checkpoint at act 1
        state1 = create_new_narrative_state(story_id="test-story", session_id="act-test")
        state1.position.act = 1
        
        should, type_ = narrative_saver._should_create_narrative_checkpoint(
            state1, MockCheckpointMetadata()
        )
        assert should is True
        # First call doesn't detect transition (sets baseline)
        
        # Second checkpoint at act 2
        state2 = create_new_narrative_state(story_id="test-story", session_id="act-test")
        state2.position.act = 2
        
        should, type_ = narrative_saver._should_create_narrative_checkpoint(
            state2, MockCheckpointMetadata()
        )
        assert should is True
        assert type_ == "act_transition"
    
    def test_detects_episode_boundary(self, narrative_saver):
        """Test detection of episode boundaries."""
        # Set initial episode
        state1 = create_new_narrative_state(story_id="test-story", session_id="ep-test")
        state1.current_episode_id = "s01e01"
        narrative_saver._should_create_narrative_checkpoint(
            state1, MockCheckpointMetadata()
        )
        
        # New episode
        state2 = create_new_narrative_state(story_id="test-story", session_id="ep-test")
        state2.current_episode_id = "s01e02"
        
        should, type_ = narrative_saver._should_create_narrative_checkpoint(
            state2, MockCheckpointMetadata()
        )
        assert should is True
        assert type_ == "episode_boundary"
