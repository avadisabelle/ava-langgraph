"""
Integrations for Narrative Intelligence Toolkit.

This module provides integration with external systems:
- Redis state management
- LangGraph checkpointing (coming soon)
- Langfuse tracing (coming soon)
- Flowise/Langflow bridges (coming soon)
"""

from .redis_state import (
    RedisConfig,
    NarrativeRedisManager,
    MockRedis,
    get_narrative_manager,
)

__all__ = [
    # Redis State Management
    "RedisConfig",
    "NarrativeRedisManager",
    "MockRedis",
    "get_narrative_manager",
]
