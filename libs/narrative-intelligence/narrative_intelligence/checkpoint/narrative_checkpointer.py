"""
NarrativeCheckpointSaver - LangGraph Checkpoint Integration

Extends LangGraph's checkpoint system to support narrative state persistence.
This allows three-universe analysis and story beats to be preserved across
graph executions and sessions.

Key Features:
- Wraps existing checkpointers (SQLite, Postgres, Memory)
- Adds narrative metadata extraction
- Tracks story beats in checkpoint metadata
- Supports cross-session narrative continuity (Miadi-46 requirement)
"""

from __future__ import annotations

import json
from collections.abc import AsyncIterator, Iterator, Sequence
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, TypedDict, TYPE_CHECKING

# Make langchain_core import optional
try:
    from langchain_core.runnables import RunnableConfig
    HAS_LANGCHAIN_CORE = True
except ImportError:
    HAS_LANGCHAIN_CORE = False
    # Create stub type for development without langchain_core
    RunnableConfig = Dict[str, Any]

# Import from langgraph checkpoint base
try:
    from langgraph.checkpoint.base import (
        BaseCheckpointSaver,
        Checkpoint,
        CheckpointMetadata,
        CheckpointTuple,
        ChannelVersions,
    )
    HAS_LANGGRAPH = True
except ImportError:
    HAS_LANGGRAPH = False
    # Create stub types for development without langgraph
    from typing import Generic, TypeVar
    V = TypeVar("V")
    class BaseCheckpointSaver(Generic[V]):
        """Stub base class for development without langgraph."""
        serde = None
        def __init__(self, *, serde=None):
            self.serde = serde
        @property
        def config_specs(self):
            return []
    Checkpoint = dict
    CheckpointMetadata = dict
    CheckpointTuple = tuple
    ChannelVersions = dict

# Import our unified state types
from narrative_intelligence.schemas.unified_state_bridge import (
    UnifiedNarrativeState,
    StoryBeat,
    NarrativePosition,
    Universe,
    ThreeUniverseAnalysis,
)


class NarrativeCheckpointMetadata(TypedDict, total=False):
    """Extended metadata for narrative-aware checkpoints.
    
    This extends LangGraph's CheckpointMetadata with narrative-specific
    fields that enable cross-session coherence and three-universe tracking.
    """
    # Standard checkpoint metadata
    source: str
    step: int
    parents: Dict[str, str]
    
    # Narrative-specific metadata
    narrative_session_id: str
    narrative_episode_id: str
    narrative_act: int
    narrative_phase: str
    narrative_beat_count: int
    narrative_lead_universe: str
    narrative_coherence: float
    narrative_themes: List[str]
    narrative_checkpoint_type: str  # "beat", "episode_boundary", "act_transition"
    
    # Cross-session tracking (for Miadi-46 webhook continuity)
    related_sessions: List[str]
    webhook_correlation_id: Optional[str]


def create_narrative_checkpoint_metadata(
    base_metadata: CheckpointMetadata,
    narrative_state: Optional[UnifiedNarrativeState] = None,
    checkpoint_type: str = "beat",
    webhook_correlation_id: Optional[str] = None,
) -> NarrativeCheckpointMetadata:
    """Create extended checkpoint metadata with narrative information.
    
    Args:
        base_metadata: Standard LangGraph checkpoint metadata
        narrative_state: Current narrative state (if available)
        checkpoint_type: Type of narrative checkpoint
        webhook_correlation_id: For tracking webhook-initiated chains
        
    Returns:
        Extended metadata including narrative context
    """
    extended = NarrativeCheckpointMetadata(**base_metadata)
    extended["narrative_checkpoint_type"] = checkpoint_type
    
    if webhook_correlation_id:
        extended["webhook_correlation_id"] = webhook_correlation_id
    
    if narrative_state:
        extended["narrative_session_id"] = narrative_state.session_id
        extended["narrative_episode_id"] = narrative_state.current_episode_id
        
        # Use position attribute (the actual field name)
        position = narrative_state.position
        extended["narrative_act"] = position.act
        extended["narrative_phase"] = position.phase.value if hasattr(position.phase, 'value') else str(position.phase)
        extended["narrative_beat_count"] = len(narrative_state.beats)
        
        # Track themes
        extended["narrative_themes"] = list(narrative_state.themes.keys())
        
        # Track related sessions for cross-session coherence (empty list if not set)
        extended["related_sessions"] = []
        
        # Get lead universe from latest analysis if available
        if narrative_state.beats:
            latest_beat = narrative_state.beats[-1]
            if latest_beat.universe_analysis:
                analysis = latest_beat.universe_analysis
                extended["narrative_lead_universe"] = analysis.lead_universe.value
                extended["narrative_coherence"] = analysis.coherence_score
    
    return extended


@dataclass
class NarrativeCheckpointConfig:
    """Configuration for narrative checkpoint behavior."""
    
    # How often to create narrative checkpoints (in beats)
    checkpoint_frequency: int = 1
    
    # Whether to store full beat content or just references
    store_full_beats: bool = True
    
    # Maximum beats to include in checkpoint metadata
    max_beats_in_metadata: int = 10
    
    # Whether to track cross-session relationships
    enable_cross_session_tracking: bool = True
    
    # Checkpoint on act transitions
    checkpoint_on_act_transition: bool = True
    
    # Checkpoint on episode boundaries
    checkpoint_on_episode_boundary: bool = True


class NarrativeCheckpointSaver(BaseCheckpointSaver[int]):
    """Checkpoint saver with narrative intelligence support.
    
    Wraps an existing checkpoint saver to add narrative-aware metadata
    and state extraction. This enables:
    
    1. Narrative continuity across graph executions
    2. Three-universe analysis preservation
    3. Cross-session coherence (for Miadi-46 webhooks)
    4. Story beat history tracking
    
    Usage:
        from langgraph.checkpoint.sqlite import SqliteSaver
        from narrative_intelligence.checkpoint import NarrativeCheckpointSaver
        
        # Wrap existing saver
        base_saver = SqliteSaver.from_conn_string("narratives.db")
        saver = NarrativeCheckpointSaver(base_saver)
        
        # Use with StateGraph
        graph = StateGraph(NarrativeState)
        compiled = graph.compile(checkpointer=saver)
    """
    
    def __init__(
        self,
        base_saver: BaseCheckpointSaver,
        config: Optional[NarrativeCheckpointConfig] = None,
        narrative_state_channel: str = "narrative_state",
    ):
        """Initialize the narrative checkpoint saver.
        
        Args:
            base_saver: The underlying checkpoint saver (SQLite, Postgres, etc.)
            config: Configuration for narrative checkpoint behavior
            narrative_state_channel: Name of the channel containing UnifiedNarrativeState
        """
        if not HAS_LANGGRAPH:
            raise ImportError(
                "langgraph is required for NarrativeCheckpointSaver. "
                "Install with: pip install langgraph"
            )
        
        super().__init__(serde=base_saver.serde)
        self._base_saver = base_saver
        self._config = config or NarrativeCheckpointConfig()
        self._narrative_channel = narrative_state_channel
        self._beat_counter = 0
        self._last_act = 1
        self._last_episode: Optional[str] = None
    
    @property
    def config_specs(self) -> list:
        """Include base saver's config specs."""
        return self._base_saver.config_specs
    
    def _extract_narrative_state(
        self, checkpoint: Checkpoint
    ) -> Optional[UnifiedNarrativeState]:
        """Extract UnifiedNarrativeState from checkpoint channel values."""
        channel_values = checkpoint.get("channel_values", {})
        
        # Try to find narrative state in channels
        narrative_data = channel_values.get(self._narrative_channel)
        
        if narrative_data is None:
            return None
        
        # If it's already a UnifiedNarrativeState, return it
        if isinstance(narrative_data, UnifiedNarrativeState):
            return narrative_data
        
        # If it's a dict, try to deserialize
        if isinstance(narrative_data, dict):
            try:
                return UnifiedNarrativeState.from_dict(narrative_data)
            except (KeyError, TypeError, ValueError):
                return None
        
        return None
    
    def _should_create_narrative_checkpoint(
        self,
        narrative_state: Optional[UnifiedNarrativeState],
        metadata: CheckpointMetadata,
    ) -> tuple[bool, str]:
        """Determine if a narrative checkpoint should be created.
        
        Returns:
            Tuple of (should_checkpoint, checkpoint_type)
        """
        if narrative_state is None:
            return True, "beat"  # Always checkpoint, even without narrative state
        
        position = narrative_state.position
        
        # Check for act transition
        if self._config.checkpoint_on_act_transition:
            if position.act != self._last_act:
                self._last_act = position.act
                return True, "act_transition"
        
        # Check for episode boundary
        if self._config.checkpoint_on_episode_boundary:
            if narrative_state.current_episode_id != self._last_episode:
                self._last_episode = narrative_state.current_episode_id
                return True, "episode_boundary"
        
        # Check beat frequency
        self._beat_counter += 1
        if self._beat_counter >= self._config.checkpoint_frequency:
            self._beat_counter = 0
            return True, "beat"
        
        return True, "beat"  # Default: always checkpoint
    
    def _enhance_metadata(
        self,
        metadata: CheckpointMetadata,
        checkpoint: Checkpoint,
        webhook_correlation_id: Optional[str] = None,
    ) -> NarrativeCheckpointMetadata:
        """Enhance metadata with narrative information."""
        narrative_state = self._extract_narrative_state(checkpoint)
        should_checkpoint, checkpoint_type = self._should_create_narrative_checkpoint(
            narrative_state, metadata
        )
        
        return create_narrative_checkpoint_metadata(
            base_metadata=metadata,
            narrative_state=narrative_state,
            checkpoint_type=checkpoint_type,
            webhook_correlation_id=webhook_correlation_id,
        )
    
    # === Synchronous Methods ===
    
    def get_tuple(self, config: RunnableConfig) -> Optional[CheckpointTuple]:
        """Get checkpoint tuple from base saver."""
        return self._base_saver.get_tuple(config)
    
    def list(
        self,
        config: Optional[RunnableConfig],
        *,
        filter: Optional[Dict[str, Any]] = None,
        before: Optional[RunnableConfig] = None,
        limit: Optional[int] = None,
    ) -> Iterator[CheckpointTuple]:
        """List checkpoints from base saver."""
        return self._base_saver.list(config, filter=filter, before=before, limit=limit)
    
    def put(
        self,
        config: RunnableConfig,
        checkpoint: Checkpoint,
        metadata: CheckpointMetadata,
        new_versions: ChannelVersions,
    ) -> RunnableConfig:
        """Store checkpoint with enhanced narrative metadata."""
        # Extract webhook correlation from config if present
        webhook_correlation_id = config.get("configurable", {}).get(
            "webhook_correlation_id"
        )
        
        # Enhance metadata with narrative information
        enhanced_metadata = self._enhance_metadata(
            metadata, checkpoint, webhook_correlation_id
        )
        
        # Store with base saver
        return self._base_saver.put(config, checkpoint, enhanced_metadata, new_versions)
    
    def put_writes(
        self,
        config: RunnableConfig,
        writes: Sequence[tuple[str, Any]],
        task_id: str,
        task_path: str = "",
    ) -> None:
        """Store writes with base saver."""
        return self._base_saver.put_writes(config, writes, task_id, task_path)
    
    def delete_thread(self, thread_id: str) -> None:
        """Delete thread from base saver."""
        return self._base_saver.delete_thread(thread_id)
    
    # === Async Methods ===
    
    async def aget_tuple(self, config: RunnableConfig) -> Optional[CheckpointTuple]:
        """Async get checkpoint tuple."""
        return await self._base_saver.aget_tuple(config)
    
    async def alist(
        self,
        config: Optional[RunnableConfig],
        *,
        filter: Optional[Dict[str, Any]] = None,
        before: Optional[RunnableConfig] = None,
        limit: Optional[int] = None,
    ) -> AsyncIterator[CheckpointTuple]:
        """Async list checkpoints."""
        async for item in self._base_saver.alist(
            config, filter=filter, before=before, limit=limit
        ):
            yield item
    
    async def aput(
        self,
        config: RunnableConfig,
        checkpoint: Checkpoint,
        metadata: CheckpointMetadata,
        new_versions: ChannelVersions,
    ) -> RunnableConfig:
        """Async store checkpoint with enhanced narrative metadata."""
        webhook_correlation_id = config.get("configurable", {}).get(
            "webhook_correlation_id"
        )
        
        enhanced_metadata = self._enhance_metadata(
            metadata, checkpoint, webhook_correlation_id
        )
        
        return await self._base_saver.aput(
            config, checkpoint, enhanced_metadata, new_versions
        )
    
    async def aput_writes(
        self,
        config: RunnableConfig,
        writes: Sequence[tuple[str, Any]],
        task_id: str,
        task_path: str = "",
    ) -> None:
        """Async store writes."""
        return await self._base_saver.aput_writes(config, writes, task_id, task_path)
    
    async def adelete_thread(self, thread_id: str) -> None:
        """Async delete thread."""
        return await self._base_saver.adelete_thread(thread_id)
    
    # === Narrative-Specific Query Methods ===
    
    def list_by_narrative_session(
        self,
        session_id: str,
        limit: Optional[int] = None,
    ) -> Iterator[CheckpointTuple]:
        """List checkpoints belonging to a narrative session.
        
        Args:
            session_id: The narrative session ID to filter by
            limit: Maximum number of checkpoints to return
            
        Returns:
            Iterator of checkpoint tuples for the session
        """
        return self.list(
            config=None,
            filter={"narrative_session_id": session_id},
            limit=limit,
        )
    
    def list_by_episode(
        self,
        episode_id: str,
        limit: Optional[int] = None,
    ) -> Iterator[CheckpointTuple]:
        """List checkpoints belonging to an episode.
        
        Args:
            episode_id: The episode ID to filter by
            limit: Maximum number of checkpoints to return
            
        Returns:
            Iterator of checkpoint tuples for the episode
        """
        return self.list(
            config=None,
            filter={"narrative_episode_id": episode_id},
            limit=limit,
        )
    
    def list_act_transitions(
        self,
        session_id: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> Iterator[CheckpointTuple]:
        """List checkpoints that represent act transitions.
        
        Useful for navigating to major story points.
        
        Args:
            session_id: Optional session ID to filter by
            limit: Maximum number of checkpoints to return
            
        Returns:
            Iterator of act transition checkpoint tuples
        """
        filter_dict: Dict[str, Any] = {"narrative_checkpoint_type": "act_transition"}
        if session_id:
            filter_dict["narrative_session_id"] = session_id
        
        return self.list(config=None, filter=filter_dict, limit=limit)
    
    def list_by_webhook_correlation(
        self,
        correlation_id: str,
        limit: Optional[int] = None,
    ) -> Iterator[CheckpointTuple]:
        """List checkpoints triggered by a webhook correlation ID.
        
        For Miadi-46 cross-session coherence tracking.
        
        Args:
            correlation_id: The webhook correlation ID
            limit: Maximum number of checkpoints to return
            
        Returns:
            Iterator of checkpoint tuples for the correlation
        """
        return self.list(
            config=None,
            filter={"webhook_correlation_id": correlation_id},
            limit=limit,
        )
    
    def get_narrative_history(
        self,
        config: RunnableConfig,
        max_checkpoints: int = 50,
    ) -> List[Dict[str, Any]]:
        """Get narrative history from checkpoints.
        
        Returns a list of narrative snapshots showing the progression
        of the story through checkpoints.
        
        Args:
            config: Configuration for filtering checkpoints
            max_checkpoints: Maximum number of checkpoints to include
            
        Returns:
            List of narrative history entries
        """
        history = []
        
        for i, checkpoint_tuple in enumerate(self.list(config, limit=max_checkpoints)):
            if i >= max_checkpoints:
                break
            
            metadata = checkpoint_tuple.metadata
            entry = {
                "checkpoint_id": checkpoint_tuple.checkpoint.get("id"),
                "timestamp": checkpoint_tuple.checkpoint.get("ts"),
                "step": metadata.get("step"),
                "narrative_act": metadata.get("narrative_act"),
                "narrative_phase": metadata.get("narrative_phase"),
                "narrative_beat_count": metadata.get("narrative_beat_count"),
                "narrative_lead_universe": metadata.get("narrative_lead_universe"),
                "narrative_coherence": metadata.get("narrative_coherence"),
                "checkpoint_type": metadata.get("narrative_checkpoint_type"),
            }
            history.append(entry)
        
        return history


# === Factory Functions ===

def create_sqlite_narrative_saver(
    db_path: str = ":memory:",
    config: Optional[NarrativeCheckpointConfig] = None,
) -> NarrativeCheckpointSaver:
    """Create a narrative checkpoint saver backed by SQLite.
    
    Args:
        db_path: Path to SQLite database file, or ":memory:" for in-memory
        config: Narrative checkpoint configuration
        
    Returns:
        Configured NarrativeCheckpointSaver
    """
    try:
        from langgraph.checkpoint.sqlite import SqliteSaver
        base_saver = SqliteSaver.from_conn_string(db_path)
        return NarrativeCheckpointSaver(base_saver, config=config)
    except ImportError as e:
        raise ImportError(
            "langgraph-checkpoint-sqlite is required. "
            "Install with: pip install langgraph-checkpoint-sqlite"
        ) from e


def create_postgres_narrative_saver(
    conn_string: str,
    config: Optional[NarrativeCheckpointConfig] = None,
) -> NarrativeCheckpointSaver:
    """Create a narrative checkpoint saver backed by PostgreSQL.
    
    Args:
        conn_string: PostgreSQL connection string
        config: Narrative checkpoint configuration
        
    Returns:
        Configured NarrativeCheckpointSaver
    """
    try:
        from langgraph.checkpoint.postgres import PostgresSaver
        base_saver = PostgresSaver.from_conn_string(conn_string)
        return NarrativeCheckpointSaver(base_saver, config=config)
    except ImportError as e:
        raise ImportError(
            "langgraph-checkpoint-postgres is required. "
            "Install with: pip install langgraph-checkpoint-postgres"
        ) from e


def create_memory_narrative_saver(
    config: Optional[NarrativeCheckpointConfig] = None,
) -> NarrativeCheckpointSaver:
    """Create a narrative checkpoint saver backed by in-memory storage.
    
    Useful for testing and development.
    
    Args:
        config: Narrative checkpoint configuration
        
    Returns:
        Configured NarrativeCheckpointSaver
    """
    try:
        from langgraph.checkpoint.memory import MemorySaver
        base_saver = MemorySaver()
        return NarrativeCheckpointSaver(base_saver, config=config)
    except ImportError as e:
        raise ImportError(
            "langgraph is required. Install with: pip install langgraph"
        ) from e
