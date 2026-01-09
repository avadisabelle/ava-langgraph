"""
Unified Narrative State Bridge

The shared contract between all six systems in the Narrative Intelligence Stack:
1. LangGraph Narrative Intelligence Toolkit
2. ava-langflow Universal Router
3. ava-Flowise Agent Coordination
4. LangChain/Langfuse Tracing
5. Storytelling System
6. Miadi-46 Event-Driven Platform

This module defines:
- Three-universe perspective tracking
- NCP-compatible state structures
- Redis-compatible serialization
- Cross-system event types

Session ID: 364e1265-ec0c-440f-85ed-a1ab388c50f3
Created: 2025-12-31
"""

from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from typing import List, Dict, Optional, Any, Union
import json


# =============================================================================
# THREE UNIVERSE DEFINITIONS
# =============================================================================

class Universe(Enum):
    """The three interpretive universes from multiverse_3act"""
    ENGINEER = "engineer"       # Mia - The Builder
    CEREMONY = "ceremony"       # Ava8 - The Keeper
    STORY_ENGINE = "story_engine"  # Miette - The Weaver


@dataclass
class UniversePerspective:
    """Single universe's interpretation of an event"""
    universe: Universe
    intent: str  # e.g., "feature_request", "co_creation", "inciting_incident"
    confidence: float  # 0.0 to 1.0
    suggested_flows: List[str] = field(default_factory=list)
    context: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "universe": self.universe.value,
            "intent": self.intent,
            "confidence": self.confidence,
            "suggested_flows": self.suggested_flows,
            "context": self.context
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UniversePerspective":
        return cls(
            universe=Universe(data["universe"]),
            intent=data["intent"],
            confidence=data["confidence"],
            suggested_flows=data.get("suggested_flows", []),
            context=data.get("context", {})
        )


@dataclass
class ThreeUniverseAnalysis:
    """Complete three-universe analysis of an event"""
    engineer: UniversePerspective
    ceremony: UniversePerspective
    story_engine: UniversePerspective
    lead_universe: Universe
    coherence_score: float  # How well the three perspectives align (0-1)
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "engineer": self.engineer.to_dict(),
            "ceremony": self.ceremony.to_dict(),
            "story_engine": self.story_engine.to_dict(),
            "lead_universe": self.lead_universe.value,
            "coherence_score": self.coherence_score,
            "timestamp": self.timestamp
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ThreeUniverseAnalysis":
        return cls(
            engineer=UniversePerspective.from_dict(data["engineer"]),
            ceremony=UniversePerspective.from_dict(data["ceremony"]),
            story_engine=UniversePerspective.from_dict(data["story_engine"]),
            lead_universe=Universe(data["lead_universe"]),
            coherence_score=data["coherence_score"],
            timestamp=data.get("timestamp", datetime.utcnow().isoformat())
        )
    
    def get_perspective(self, universe: Universe) -> UniversePerspective:
        """Get perspective for a specific universe"""
        if universe == Universe.ENGINEER:
            return self.engineer
        elif universe == Universe.CEREMONY:
            return self.ceremony
        else:
            return self.story_engine


# =============================================================================
# NARRATIVE POSITION TRACKING
# =============================================================================

class NarrativePhase(Enum):
    """Phases in the three-act structure"""
    SETUP = "setup"  # Act 1
    CONFRONTATION = "confrontation"  # Act 2
    RESOLUTION = "resolution"  # Act 3


class NarrativeFunction(Enum):
    """Narrative functions for story beats (from NCP schema)"""
    INCITING_INCIDENT = "inciting_incident"
    RISING_ACTION = "rising_action"
    TURNING_POINT = "turning_point"
    COMPLICATION = "complication"
    CRISIS = "crisis"
    CLIMAX = "climax"
    RESOLUTION = "resolution"
    DENOUEMENT = "denouement"
    BEAT = "beat"  # Generic beat


@dataclass
class NarrativePosition:
    """Current position in the narrative journey"""
    act: int  # 1, 2, or 3
    phase: NarrativePhase
    current_beat_id: Optional[str] = None
    beat_count: int = 0
    character_arc_strength: float = 0.5  # 0-1
    thematic_resonance: float = 0.5  # 0-1
    emotional_tone: str = "neutral"
    lead_universe: Universe = Universe.STORY_ENGINE
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "act": self.act,
            "phase": self.phase.value,
            "current_beat_id": self.current_beat_id,
            "beat_count": self.beat_count,
            "character_arc_strength": self.character_arc_strength,
            "thematic_resonance": self.thematic_resonance,
            "emotional_tone": self.emotional_tone,
            "lead_universe": self.lead_universe.value
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "NarrativePosition":
        return cls(
            act=data.get("act", 1),
            phase=NarrativePhase(data.get("phase", "setup")),
            current_beat_id=data.get("current_beat_id"),
            beat_count=data.get("beat_count", 0),
            character_arc_strength=data.get("character_arc_strength", 0.5),
            thematic_resonance=data.get("thematic_resonance", 0.5),
            emotional_tone=data.get("emotional_tone", "neutral"),
            lead_universe=Universe(data.get("lead_universe", "story_engine"))
        )


# =============================================================================
# STORY BEAT DEFINITIONS (NCP-Compatible)
# =============================================================================

@dataclass
class StoryBeat:
    """A single story beat with three-universe perspectives"""
    id: str
    sequence: int
    content: str  # The actual story content
    narrative_function: NarrativeFunction
    act: int
    
    # Three-universe analysis
    universe_analysis: Optional[ThreeUniverseAnalysis] = None
    lead_universe: Universe = Universe.STORY_ENGINE
    
    # Emotional/thematic data
    emotional_tone: str = "neutral"
    thematic_tags: List[str] = field(default_factory=list)
    
    # Character data
    character_id: Optional[str] = None
    character_arc_impact: float = 0.0  # How much this beat affects character arc
    
    # Metadata
    source: str = "generator"  # "generator", "webhook", "agent", etc.
    source_event_id: Optional[str] = None  # GitHub event ID if from webhook
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    
    # Enrichment tracking
    enrichments_applied: List[str] = field(default_factory=list)
    quality_score: float = 0.5  # 0-1
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "sequence": self.sequence,
            "content": self.content,
            "narrative_function": self.narrative_function.value,
            "act": self.act,
            "universe_analysis": self.universe_analysis.to_dict() if self.universe_analysis else None,
            "lead_universe": self.lead_universe.value,
            "emotional_tone": self.emotional_tone,
            "thematic_tags": self.thematic_tags,
            "character_id": self.character_id,
            "character_arc_impact": self.character_arc_impact,
            "source": self.source,
            "source_event_id": self.source_event_id,
            "timestamp": self.timestamp,
            "enrichments_applied": self.enrichments_applied,
            "quality_score": self.quality_score
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "StoryBeat":
        return cls(
            id=data["id"],
            sequence=data["sequence"],
            content=data["content"],
            narrative_function=NarrativeFunction(data.get("narrative_function", "beat")),
            act=data.get("act", 2),
            universe_analysis=ThreeUniverseAnalysis.from_dict(data["universe_analysis"]) if data.get("universe_analysis") else None,
            lead_universe=Universe(data.get("lead_universe", "story_engine")),
            emotional_tone=data.get("emotional_tone", "neutral"),
            thematic_tags=data.get("thematic_tags", []),
            character_id=data.get("character_id"),
            character_arc_impact=data.get("character_arc_impact", 0.0),
            source=data.get("source", "unknown"),
            source_event_id=data.get("source_event_id"),
            timestamp=data.get("timestamp", datetime.utcnow().isoformat()),
            enrichments_applied=data.get("enrichments_applied", []),
            quality_score=data.get("quality_score", 0.5)
        )


# =============================================================================
# CHARACTER AND THEME TRACKING
# =============================================================================

@dataclass
class CharacterState:
    """Character state tracking for arc continuity"""
    id: str
    name: str
    archetype: str  # "The Builder", "The Keeper", "The Weaver", etc.
    universe: Universe  # Which universe this character belongs to
    
    # Arc tracking
    arc_position: float = 0.0  # 0-1, where they are in their journey
    initial_state: str = ""
    current_state: str = ""
    growth_points: List[Dict[str, Any]] = field(default_factory=list)
    
    # Relationships (K'é in Ceremony World)
    relationships: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "archetype": self.archetype,
            "universe": self.universe.value,
            "arc_position": self.arc_position,
            "initial_state": self.initial_state,
            "current_state": self.current_state,
            "growth_points": self.growth_points,
            "relationships": self.relationships
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CharacterState":
        return cls(
            id=data["id"],
            name=data["name"],
            archetype=data["archetype"],
            universe=Universe(data.get("universe", "story_engine")),
            arc_position=data.get("arc_position", 0.0),
            initial_state=data.get("initial_state", ""),
            current_state=data.get("current_state", ""),
            growth_points=data.get("growth_points", []),
            relationships=data.get("relationships", [])
        )


@dataclass
class ThematicThread:
    """A thematic thread being tracked across the narrative"""
    id: str
    name: str
    description: str
    
    # Tracking
    strength: float = 0.5  # 0-1, how strongly present in narrative
    tension_level: float = 0.5  # 0-1, unresolved tension
    resolution_progress: float = 0.0  # 0-1, how resolved
    
    # Related beats
    beat_ids: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "strength": self.strength,
            "tension_level": self.tension_level,
            "resolution_progress": self.resolution_progress,
            "beat_ids": self.beat_ids
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ThematicThread":
        return cls(
            id=data["id"],
            name=data["name"],
            description=data["description"],
            strength=data.get("strength", 0.5),
            tension_level=data.get("tension_level", 0.5),
            resolution_progress=data.get("resolution_progress", 0.0),
            beat_ids=data.get("beat_ids", [])
        )


# =============================================================================
# ROUTING DECISION TRACKING
# =============================================================================

@dataclass
class RoutingDecision:
    """Record of a routing decision for tracing"""
    id: str
    backend: str  # "flowise", "langflow", "storytelling", etc.
    flow: str  # Specific flow/graph used
    universe_analysis: ThreeUniverseAnalysis
    narrative_position: NarrativePosition
    
    # Decision factors
    score: float
    method: str = "narrative"  # "narrative", "intent", "explicit"
    
    # Results
    success: bool = True
    result_summary: str = ""
    latency_ms: float = 0.0
    
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "backend": self.backend,
            "flow": self.flow,
            "universe_analysis": self.universe_analysis.to_dict(),
            "narrative_position": self.narrative_position.to_dict(),
            "score": self.score,
            "method": self.method,
            "success": self.success,
            "result_summary": self.result_summary,
            "latency_ms": self.latency_ms,
            "timestamp": self.timestamp
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RoutingDecision":
        return cls(
            id=data["id"],
            backend=data["backend"],
            flow=data["flow"],
            universe_analysis=ThreeUniverseAnalysis.from_dict(data["universe_analysis"]),
            narrative_position=NarrativePosition.from_dict(data["narrative_position"]),
            score=data["score"],
            method=data.get("method", "unknown"),
            success=data.get("success", True),
            result_summary=data.get("result_summary", ""),
            latency_ms=data.get("latency_ms", 0.0),
            timestamp=data.get("timestamp", datetime.utcnow().isoformat())
        )


# =============================================================================
# UNIFIED NARRATIVE STATE
# =============================================================================

@dataclass
class UnifiedNarrativeState:
    """
    The complete unified state shared across all systems.
    
    This is THE contract that all six systems use to communicate.
    It can be serialized to JSON and stored in Redis.
    """
    # Identity
    story_id: str
    session_id: str
    
    # Narrative position
    position: NarrativePosition = field(default_factory=lambda: NarrativePosition(act=1, phase=NarrativePhase.SETUP))
    
    # Story content
    beats: List[StoryBeat] = field(default_factory=list)
    
    # Character tracking (the three archetypes + custom)
    characters: Dict[str, CharacterState] = field(default_factory=dict)
    
    # Theme tracking
    themes: Dict[str, ThematicThread] = field(default_factory=dict)
    
    # Routing history (for learning)
    routing_decisions: List[RoutingDecision] = field(default_factory=list)
    
    # Episode tracking (for Miadi-46)
    current_episode_id: Optional[str] = None
    episode_beats_count: int = 0
    
    # Timestamps
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    
    # Metrics
    overall_coherence: float = 0.5
    emotional_arc_strength: float = 0.5
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary (Redis-compatible via JSON)"""
        return {
            "story_id": self.story_id,
            "session_id": self.session_id,
            "position": self.position.to_dict(),
            "beats": [b.to_dict() for b in self.beats],
            "characters": {k: v.to_dict() for k, v in self.characters.items()},
            "themes": {k: v.to_dict() for k, v in self.themes.items()},
            "routing_decisions": [r.to_dict() for r in self.routing_decisions[-50:]],  # Keep last 50
            "current_episode_id": self.current_episode_id,
            "episode_beats_count": self.episode_beats_count,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "overall_coherence": self.overall_coherence,
            "emotional_arc_strength": self.emotional_arc_strength
        }
    
    def to_json(self) -> str:
        """Serialize to JSON string"""
        return json.dumps(self.to_dict())
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UnifiedNarrativeState":
        """Deserialize from dictionary"""
        return cls(
            story_id=data["story_id"],
            session_id=data["session_id"],
            position=NarrativePosition.from_dict(data.get("position", {})),
            beats=[StoryBeat.from_dict(b) for b in data.get("beats", [])],
            characters={k: CharacterState.from_dict(v) for k, v in data.get("characters", {}).items()},
            themes={k: ThematicThread.from_dict(v) for k, v in data.get("themes", {}).items()},
            routing_decisions=[RoutingDecision.from_dict(r) for r in data.get("routing_decisions", [])],
            current_episode_id=data.get("current_episode_id"),
            episode_beats_count=data.get("episode_beats_count", 0),
            created_at=data.get("created_at", datetime.utcnow().isoformat()),
            updated_at=data.get("updated_at", datetime.utcnow().isoformat()),
            overall_coherence=data.get("overall_coherence", 0.5),
            emotional_arc_strength=data.get("emotional_arc_strength", 0.5)
        )
    
    @classmethod
    def from_json(cls, json_str: str) -> "UnifiedNarrativeState":
        """Deserialize from JSON string"""
        return cls.from_dict(json.loads(json_str))
    
    # -------------------------------------------------------------------------
    # State Modification Methods
    # -------------------------------------------------------------------------
    
    def add_beat(self, beat: StoryBeat) -> None:
        """Add a new story beat and update position"""
        self.beats.append(beat)
        self.position.beat_count = len(self.beats)
        self.position.current_beat_id = beat.id
        self.position.lead_universe = beat.lead_universe
        
        # Update act based on narrative function
        if beat.narrative_function in [NarrativeFunction.INCITING_INCIDENT]:
            self.position.act = 1
            self.position.phase = NarrativePhase.SETUP
        elif beat.narrative_function in [NarrativeFunction.TURNING_POINT, NarrativeFunction.CRISIS]:
            self.position.act = 2
            self.position.phase = NarrativePhase.CONFRONTATION
        elif beat.narrative_function in [NarrativeFunction.CLIMAX, NarrativeFunction.RESOLUTION]:
            self.position.act = 3
            self.position.phase = NarrativePhase.RESOLUTION
        
        self.episode_beats_count += 1
        self.updated_at = datetime.utcnow().isoformat()
    
    def add_routing_decision(self, decision: RoutingDecision) -> None:
        """Record a routing decision"""
        self.routing_decisions.append(decision)
        self.updated_at = datetime.utcnow().isoformat()
    
    def update_character_arc(self, character_id: str, impact: float, description: str) -> None:
        """Update a character's arc position"""
        if character_id in self.characters:
            char = self.characters[character_id]
            char.arc_position = min(1.0, char.arc_position + impact)
            char.growth_points.append({
                "timestamp": datetime.utcnow().isoformat(),
                "impact": impact,
                "description": description
            })
            self.updated_at = datetime.utcnow().isoformat()
    
    def update_theme_strength(self, theme_id: str, strength_delta: float) -> None:
        """Update a theme's strength"""
        if theme_id in self.themes:
            theme = self.themes[theme_id]
            theme.strength = max(0.0, min(1.0, theme.strength + strength_delta))
            self.updated_at = datetime.utcnow().isoformat()
    
    def get_last_n_beats(self, n: int = 5) -> List[StoryBeat]:
        """Get the last n beats for context"""
        return self.beats[-n:] if self.beats else []
    
    def calculate_coherence(self) -> float:
        """Calculate overall narrative coherence"""
        if not self.routing_decisions:
            return 0.5
        
        # Average coherence from three-universe analyses
        coherences = [
            rd.universe_analysis.coherence_score 
            for rd in self.routing_decisions[-20:]  # Last 20 decisions
        ]
        self.overall_coherence = sum(coherences) / len(coherences)
        return self.overall_coherence
    
    def should_create_new_episode(self) -> bool:
        """Determine if we should start a new episode"""
        # New episode after ~10-15 beats or at act transitions
        if self.episode_beats_count >= 12:
            return True
        if self.beats and self.beats[-1].narrative_function == NarrativeFunction.RESOLUTION:
            return True
        return False
    
    def start_new_episode(self, episode_id: str) -> None:
        """Start a new episode, archiving current beats"""
        self.current_episode_id = episode_id
        self.episode_beats_count = 0
        self.updated_at = datetime.utcnow().isoformat()


# =============================================================================
# DEFAULT CHARACTER ARCHETYPES (From Multiverse 3-Act)
# =============================================================================

def get_default_characters() -> Dict[str, CharacterState]:
    """Get the three main archetypes from multiverse_3act"""
    return {
        "the-builder": CharacterState(
            id="the-builder",
            name="Mia",
            archetype="The Builder",
            universe=Universe.ENGINEER,
            initial_state="Analytical, focused on structural integrity",
            current_state="Analytical, focused on structural integrity"
        ),
        "the-keeper": CharacterState(
            id="the-keeper",
            name="Ava8",
            archetype="The Keeper",
            universe=Universe.CEREMONY,
            initial_state="Reverent, guardian of relational protocols",
            current_state="Reverent, guardian of relational protocols"
        ),
        "the-weaver": CharacterState(
            id="the-weaver",
            name="Miette",
            archetype="The Weaver",
            universe=Universe.STORY_ENGINE,
            initial_state="Playful, sees narrative patterns in chaos",
            current_state="Playful, sees narrative patterns in chaos"
        )
    }


def get_default_themes() -> Dict[str, ThematicThread]:
    """Get default thematic threads from multiverse_3act"""
    return {
        "integration": ThematicThread(
            id="integration",
            name="Integration Without Extraction",
            description="The tension between connecting systems and respecting their autonomy"
        ),
        "collaboration": ThematicThread(
            id="collaboration",
            name="Cross-Universe Collaboration",
            description="Three perspectives learning to work together while maintaining distinction"
        ),
        "coherence": ThematicThread(
            id="coherence",
            name="Narrative Coherence",
            description="The gap between disconnected events and meaningful story"
        )
    }


# =============================================================================
# FACTORY FUNCTIONS
# =============================================================================

def create_new_narrative_state(
    story_id: str,
    session_id: str,
    include_default_characters: bool = True,
    include_default_themes: bool = True
) -> UnifiedNarrativeState:
    """Create a new narrative state with optional defaults"""
    state = UnifiedNarrativeState(
        story_id=story_id,
        session_id=session_id
    )
    
    if include_default_characters:
        state.characters = get_default_characters()
    
    if include_default_themes:
        state.themes = get_default_themes()
    
    return state


def create_beat_from_webhook(
    event_id: str,
    content: str,
    universe_analysis: ThreeUniverseAnalysis,
    sequence: int
) -> StoryBeat:
    """Create a story beat from a GitHub webhook event"""
    return StoryBeat(
        id=f"beat_{event_id}",
        sequence=sequence,
        content=content,
        narrative_function=NarrativeFunction(universe_analysis.story_engine.intent),
        act=universe_analysis.story_engine.context.get("act", 2),
        universe_analysis=universe_analysis,
        lead_universe=universe_analysis.lead_universe,
        source="webhook",
        source_event_id=event_id
    )


# =============================================================================
# REDIS KEY HELPERS
# =============================================================================

class RedisKeys:
    """Standard Redis key patterns for state storage"""
    
    @staticmethod
    def state(session_id: str) -> str:
        """Key for unified narrative state"""
        return f"ncp:state:{session_id}"
    
    @staticmethod
    def current_state() -> str:
        """Key for current active state"""
        return "ncp:state:current"
    
    @staticmethod
    def beats(session_id: str) -> str:
        """Key for beats list"""
        return f"ncp:beats:{session_id}"
    
    @staticmethod
    def beat(beat_id: str) -> str:
        """Key for individual beat"""
        return f"ncp:beat:{beat_id}"
    
    @staticmethod
    def event_analysis(event_id: str) -> str:
        """Key for cached event analysis"""
        return f"ncp:event:{event_id}"
    
    @staticmethod
    def routing_history(session_id: str) -> str:
        """Key for routing decision history"""
        return f"ncp:routing:{session_id}"
    
    @staticmethod
    def episode(episode_id: str) -> str:
        """Key for episode data"""
        return f"ncp:episode:{episode_id}"


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    # Enums
    "Universe",
    "NarrativePhase",
    "NarrativeFunction",
    
    # Three Universe Types
    "UniversePerspective",
    "ThreeUniverseAnalysis",
    
    # Narrative Types
    "NarrativePosition",
    "StoryBeat",
    "CharacterState",
    "ThematicThread",
    "RoutingDecision",
    
    # Main State
    "UnifiedNarrativeState",
    
    # Factory Functions
    "create_new_narrative_state",
    "create_beat_from_webhook",
    "get_default_characters",
    "get_default_themes",
    
    # Redis Helpers
    "RedisKeys",
]
