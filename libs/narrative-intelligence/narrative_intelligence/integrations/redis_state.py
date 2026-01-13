"""
Redis State Manager for Narrative Intelligence

Provides Redis-backed persistence for the UnifiedNarrativeState,
enabling cross-system state sharing and mid-story resumption.

This integrates with:
- Miadi-46's Redis patterns (webhook event storage)
- ava-langflow's redis_state.py (session state)
- LangGraph checkpointing (for graph state persistence)

Session ID: 364e1265-ec0c-440f-85ed-a1ab388c50f3
Created: 2025-12-31
"""

import json
import logging
from datetime import datetime, timedelta, timezone
from typing import Optional, List, Dict, Any, AsyncIterator
from dataclasses import dataclass
import asyncio

# Try relative import first (for package usage), then absolute (for testing)
try:
    from ..schemas.unified_state_bridge import (
        UnifiedNarrativeState,
        StoryBeat,
        ThreeUniverseAnalysis,
        RoutingDecision,
        NarrativePosition,
        RedisKeys,
        create_new_narrative_state,
    )
except ImportError:
    from narrative_intelligence.schemas.unified_state_bridge import (
        UnifiedNarrativeState,
        StoryBeat,
        ThreeUniverseAnalysis,
        RoutingDecision,
        NarrativePosition,
        RedisKeys,
        create_new_narrative_state,
    )

logger = logging.getLogger(__name__)



@dataclass
class RedisConfig:
    """Configuration for Redis connection"""
    host: str = "localhost"
    port: int = 6379
    db: int = 0
    password: Optional[str] = None
    url: Optional[str] = None  # Alternative: full redis URL
    
    # TTL settings
    state_ttl_hours: int = 168  # 1 week default
    beat_ttl_hours: int = 720   # 30 days default
    event_cache_ttl_hours: int = 24  # 1 day for event analysis cache
    
    # Connection pool
    max_connections: int = 10
    decode_responses: bool = True


class NarrativeRedisManager:
    """
    Redis-backed state management for narrative intelligence.
    
    Responsibilities:
    - Store and retrieve UnifiedNarrativeState
    - Manage story beat persistence
    - Cache three-universe analysis results
    - Track routing decision history
    - Enable cross-system state sharing
    
    Usage:
        async with NarrativeRedisManager(config) as manager:
            # Get or create state
            state = await manager.get_or_create_state("story_123", "session_456")
            
            # Add a beat
            await manager.add_beat(beat)
            
            # Get current state
            state = await manager.get_state("session_456")
    """
    
    def __init__(self, config: Optional[RedisConfig] = None):
        self.config = config or RedisConfig()
        self._redis = None
        self._connected = False
    
    async def __aenter__(self):
        await self.connect()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.disconnect()
    
    async def connect(self) -> None:
        """Establish Redis connection"""
        try:
            # Try to import redis async
            try:
                import redis.asyncio as aioredis
            except ImportError:
                import aioredis  # Fallback for older redis versions
            
            if self.config.url:
                self._redis = await aioredis.from_url(
                    self.config.url,
                    decode_responses=self.config.decode_responses
                )
            else:
                self._redis = await aioredis.from_url(
                    f"redis://{self.config.host}:{self.config.port}/{self.config.db}",
                    password=self.config.password,
                    decode_responses=self.config.decode_responses
                )
            
            # Test connection
            await self._redis.ping()
            self._connected = True
            logger.info("Connected to Redis for narrative state management")
            
        except ImportError:
            logger.warning("Redis async library not available, using mock mode")
            self._redis = MockRedis()
            self._connected = True
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            # Use mock for development/testing
            self._redis = MockRedis()
            self._connected = True
    
    async def disconnect(self) -> None:
        """Close Redis connection"""
        if self._redis and hasattr(self._redis, 'close'):
            await self._redis.close()
        self._connected = False
    
    # =========================================================================
    # State Management
    # =========================================================================
    
    async def get_state(self, session_id: str) -> Optional[UnifiedNarrativeState]:
        """
        Retrieve narrative state for a session.
        
        Args:
            session_id: Session identifier
            
        Returns:
            UnifiedNarrativeState if exists, None otherwise
        """
        key = RedisKeys.state(session_id)
        data = await self._redis.get(key)
        
        if data:
            try:
                return UnifiedNarrativeState.from_json(data)
            except Exception as e:
                logger.error(f"Failed to deserialize state for {session_id}: {e}")
                return None
        return None
    
    async def get_or_create_state(
        self,
        story_id: str,
        session_id: str,
        include_default_characters: bool = True,
        include_default_themes: bool = True
    ) -> UnifiedNarrativeState:
        """
        Get existing state or create new one.
        
        Args:
            story_id: Story identifier
            session_id: Session identifier
            include_default_characters: Add Mia, Ava8, Miette
            include_default_themes: Add default thematic threads
            
        Returns:
            UnifiedNarrativeState (existing or new)
        """
        existing = await self.get_state(session_id)
        if existing:
            return existing
        
        # Create new state
        state = create_new_narrative_state(
            story_id=story_id,
            session_id=session_id,
            include_default_characters=include_default_characters,
            include_default_themes=include_default_themes
        )
        
        # Save it
        await self.save_state(state)
        
        return state
    
    async def save_state(self, state: UnifiedNarrativeState) -> bool:
        """
        Save narrative state to Redis.
        
        Args:
            state: State to save
            
        Returns:
            True if successful
        """
        try:
            key = RedisKeys.state(state.session_id)
            state.updated_at = datetime.now(timezone.utc).isoformat()
            
            ttl_seconds = self.config.state_ttl_hours * 3600
            await self._redis.setex(key, ttl_seconds, state.to_json())
            
            # Also update "current" pointer if this is the active state
            await self._redis.set(RedisKeys.current_state(), state.session_id)
            
            logger.debug(f"Saved narrative state for session {state.session_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save state: {e}")
            return False
    
    async def get_current_session_id(self) -> Optional[str]:
        """Get the ID of the currently active session"""
        return await self._redis.get(RedisKeys.current_state())
    
    async def set_current_session(self, session_id: str) -> None:
        """Set the currently active session"""
        await self._redis.set(RedisKeys.current_state(), session_id)
    
    # =========================================================================
    # Beat Management
    # =========================================================================
    
    async def add_beat(
        self,
        session_id: str,
        beat: StoryBeat
    ) -> bool:
        """
        Add a story beat to the session.
        
        This:
        1. Stores the beat individually (for fast lookup)
        2. Adds to session's beat list
        3. Updates the session state
        
        Args:
            session_id: Session identifier
            beat: StoryBeat to add
            
        Returns:
            True if successful
        """
        try:
            # Store individual beat
            beat_key = RedisKeys.beat(beat.id)
            ttl_seconds = self.config.beat_ttl_hours * 3600
            await self._redis.setex(beat_key, ttl_seconds, json.dumps(beat.to_dict()))
            
            # Add to session's beat list
            beats_key = RedisKeys.beats(session_id)
            await self._redis.rpush(beats_key, beat.id)
            await self._redis.expire(beats_key, ttl_seconds)
            
            # Update state
            state = await self.get_state(session_id)
            if state:
                state.add_beat(beat)
                await self.save_state(state)
            
            logger.debug(f"Added beat {beat.id} to session {session_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to add beat: {e}")
            return False
    
    async def get_beat(self, beat_id: str) -> Optional[StoryBeat]:
        """
        Retrieve a specific beat by ID.
        
        Args:
            beat_id: Beat identifier
            
        Returns:
            StoryBeat if exists
        """
        key = RedisKeys.beat(beat_id)
        data = await self._redis.get(key)
        
        if data:
            try:
                return StoryBeat.from_dict(json.loads(data))
            except Exception as e:
                logger.error(f"Failed to deserialize beat {beat_id}: {e}")
                return None
        return None
    
    async def get_recent_beats(
        self,
        session_id: str,
        count: int = 10
    ) -> List[StoryBeat]:
        """
        Get the most recent beats for a session.
        
        Args:
            session_id: Session identifier
            count: Number of beats to retrieve
            
        Returns:
            List of StoryBeat objects (most recent first)
        """
        beats_key = RedisKeys.beats(session_id)
        beat_ids = await self._redis.lrange(beats_key, -count, -1)
        
        beats = []
        for beat_id in reversed(beat_ids):  # Most recent first
            beat = await self.get_beat(beat_id)
            if beat:
                beats.append(beat)
        
        return beats
    
    # =========================================================================
    # Event Analysis Caching
    # =========================================================================
    
    async def cache_event_analysis(
        self,
        event_id: str,
        analysis: ThreeUniverseAnalysis
    ) -> bool:
        """
        Cache three-universe analysis for a webhook event.
        
        This prevents re-analyzing the same event.
        
        Args:
            event_id: GitHub event ID
            analysis: Analysis result
            
        Returns:
            True if successful
        """
        try:
            key = RedisKeys.event_analysis(event_id)
            ttl_seconds = self.config.event_cache_ttl_hours * 3600
            await self._redis.setex(key, ttl_seconds, json.dumps(analysis.to_dict()))
            return True
        except Exception as e:
            logger.error(f"Failed to cache event analysis: {e}")
            return False
    
    async def get_cached_analysis(
        self,
        event_id: str
    ) -> Optional[ThreeUniverseAnalysis]:
        """
        Retrieve cached analysis for an event.
        
        Args:
            event_id: GitHub event ID
            
        Returns:
            ThreeUniverseAnalysis if cached
        """
        key = RedisKeys.event_analysis(event_id)
        data = await self._redis.get(key)
        
        if data:
            try:
                return ThreeUniverseAnalysis.from_dict(json.loads(data))
            except Exception as e:
                logger.error(f"Failed to deserialize analysis for {event_id}: {e}")
                return None
        return None
    
    # =========================================================================
    # Routing History
    # =========================================================================
    
    async def record_routing_decision(
        self,
        session_id: str,
        decision: RoutingDecision
    ) -> bool:
        """
        Record a routing decision for learning and tracing.
        
        Args:
            session_id: Session identifier
            decision: RoutingDecision to record
            
        Returns:
            True if successful
        """
        try:
            key = RedisKeys.routing_history(session_id)
            await self._redis.rpush(key, json.dumps(decision.to_dict()))
            
            # Keep only last 100 decisions per session
            await self._redis.ltrim(key, -100, -1)
            
            # Update state
            state = await self.get_state(session_id)
            if state:
                state.add_routing_decision(decision)
                await self.save_state(state)
            
            return True
        except Exception as e:
            logger.error(f"Failed to record routing decision: {e}")
            return False
    
    async def get_routing_history(
        self,
        session_id: str,
        count: int = 50
    ) -> List[RoutingDecision]:
        """
        Get recent routing decisions for a session.
        
        Args:
            session_id: Session identifier
            count: Number of decisions to retrieve
            
        Returns:
            List of RoutingDecision objects
        """
        key = RedisKeys.routing_history(session_id)
        data_list = await self._redis.lrange(key, -count, -1)
        
        decisions = []
        for data in data_list:
            try:
                decisions.append(RoutingDecision.from_dict(json.loads(data)))
            except Exception as e:
                logger.warning(f"Failed to deserialize routing decision: {e}")
        
        return decisions
    
    # =========================================================================
    # Episode Management
    # =========================================================================
    
    async def start_new_episode(
        self,
        session_id: str,
        episode_id: str
    ) -> bool:
        """
        Mark the start of a new episode.
        
        Args:
            session_id: Session identifier
            episode_id: New episode identifier
            
        Returns:
            True if successful
        """
        state = await self.get_state(session_id)
        if state:
            state.start_new_episode(episode_id)
            return await self.save_state(state)
        return False
    
    async def get_episode_beats(
        self,
        episode_id: str
    ) -> List[StoryBeat]:
        """
        Get all beats for an episode.
        
        Args:
            episode_id: Episode identifier
            
        Returns:
            List of StoryBeat objects
        """
        key = RedisKeys.episode(episode_id)
        data = await self._redis.get(key)
        
        if data:
            try:
                episode_data = json.loads(data)
                beat_ids = episode_data.get("beat_ids", [])
                beats = []
                for beat_id in beat_ids:
                    beat = await self.get_beat(beat_id)
                    if beat:
                        beats.append(beat)
                return beats
            except Exception as e:
                logger.error(f"Failed to get episode beats: {e}")
                return []
        return []
    
    # =========================================================================
    # Utility Methods
    # =========================================================================
    
    async def list_sessions(self, pattern: str = "ncp:state:*") -> List[str]:
        """
        List all session IDs matching pattern.
        
        Args:
            pattern: Redis key pattern
            
        Returns:
            List of session IDs
        """
        keys = await self._redis.keys(pattern)
        return [k.replace("ncp:state:", "") for k in keys if k != "ncp:state:current"]
    
    async def delete_session(self, session_id: str) -> bool:
        """
        Delete all data for a session.
        
        Args:
            session_id: Session to delete
            
        Returns:
            True if successful
        """
        try:
            # Get beat IDs first
            beats_key = RedisKeys.beats(session_id)
            beat_ids = await self._redis.lrange(beats_key, 0, -1)
            
            # Delete beats
            for beat_id in beat_ids:
                await self._redis.delete(RedisKeys.beat(beat_id))
            
            # Delete session keys
            await self._redis.delete(
                RedisKeys.state(session_id),
                RedisKeys.beats(session_id),
                RedisKeys.routing_history(session_id)
            )
            
            logger.info(f"Deleted session {session_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete session: {e}")
            return False
    
    async def health_check(self) -> Dict[str, Any]:
        """
        Check Redis connection health.
        
        Returns:
            Dict with health status
        """
        try:
            start = datetime.now(timezone.utc)
            await self._redis.ping()
            latency = (datetime.now(timezone.utc) - start).total_seconds() * 1000
            
            return {
                "status": "healthy",
                "connected": self._connected,
                "latency_ms": latency,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "connected": self._connected,
                "error": str(e),
                "timestamp": datetime.now(timezone.utc).isoformat()
            }


class MockRedis:
    """
    Mock Redis for development/testing without real Redis.
    
    Stores data in memory, mimics async Redis API.
    """
    
    def __init__(self):
        self._data: Dict[str, Any] = {}
        self._lists: Dict[str, List[str]] = {}
        self._expiry: Dict[str, datetime] = {}
    
    async def ping(self) -> str:
        return "PONG"
    
    async def get(self, key: str) -> Optional[str]:
        self._check_expiry(key)
        return self._data.get(key)
    
    async def set(self, key: str, value: str) -> bool:
        self._data[key] = value
        return True
    
    async def setex(self, key: str, ttl_seconds: int, value: str) -> bool:
        self._data[key] = value
        self._expiry[key] = datetime.now(timezone.utc) + timedelta(seconds=ttl_seconds)
        return True
    
    async def delete(self, *keys: str) -> int:
        count = 0
        for key in keys:
            if key in self._data:
                del self._data[key]
                count += 1
            if key in self._lists:
                del self._lists[key]
                count += 1
        return count
    
    async def keys(self, pattern: str) -> List[str]:
        import fnmatch
        pattern = pattern.replace("*", ".*")
        return [k for k in self._data.keys() if fnmatch.fnmatch(k, pattern)]
    
    async def rpush(self, key: str, value: str) -> int:
        if key not in self._lists:
            self._lists[key] = []
        self._lists[key].append(value)
        return len(self._lists[key])
    
    async def lrange(self, key: str, start: int, end: int) -> List[str]:
        if key not in self._lists:
            return []
        lst = self._lists[key]
        if end == -1:
            end = len(lst)
        else:
            end = end + 1
        return lst[start:end]
    
    async def ltrim(self, key: str, start: int, end: int) -> bool:
        if key in self._lists:
            lst = self._lists[key]
            if end == -1:
                end = len(lst)
            else:
                end = end + 1
            self._lists[key] = lst[start:end]
        return True
    
    async def expire(self, key: str, ttl_seconds: int) -> bool:
        self._expiry[key] = datetime.now(timezone.utc) + timedelta(seconds=ttl_seconds)
        return True
    
    async def close(self):
        pass
    
    def _check_expiry(self, key: str) -> None:
        if key in self._expiry and datetime.now(timezone.utc) > self._expiry[key]:
            self._data.pop(key, None)
            self._lists.pop(key, None)
            self._expiry.pop(key, None)


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================

async def get_narrative_manager(
    redis_url: Optional[str] = None
) -> NarrativeRedisManager:
    """
    Get a configured narrative Redis manager.
    
    Args:
        redis_url: Optional Redis URL (uses localhost if not provided)
        
    Returns:
        Connected NarrativeRedisManager
    """
    config = RedisConfig(url=redis_url) if redis_url else RedisConfig()
    manager = NarrativeRedisManager(config)
    await manager.connect()
    return manager


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    "RedisConfig",
    "NarrativeRedisManager",
    "MockRedis",
    "get_narrative_manager",
]
