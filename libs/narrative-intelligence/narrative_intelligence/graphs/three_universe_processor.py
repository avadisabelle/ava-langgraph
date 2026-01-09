"""
Three-Universe Processor Graph

A LangGraph graph that processes events through all three universe lenses:
- Engineer World (Mia) - Technical precision
- Ceremony World (Ava8) - Relational protocols  
- Story Engine World (Miette) - Narrative patterns

This graph takes an event and produces a ThreeUniverseAnalysis with:
- Individual perspectives from each universe
- Lead universe determination
- Coherence score
"""

from typing import Dict, Any, Optional, List, TypedDict, Annotated
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum

# LangGraph imports
try:
    from langgraph.graph import StateGraph, END
    from langchain_core.messages import BaseMessage
    HAS_LANGGRAPH = True
except ImportError:
    HAS_LANGGRAPH = False
    StateGraph = None
    END = None
    BaseMessage = None

# Local imports
from ..schemas.unified_state_bridge import (
    Universe,
    UniversePerspective,
    ThreeUniverseAnalysis,
    NarrativeFunction,
    StoryBeat,
)


class EventType(str, Enum):
    """Types of events that can be processed."""
    GITHUB_PUSH = "github.push"
    GITHUB_ISSUE = "github.issue"
    GITHUB_PR = "github.pull_request"
    GITHUB_COMMENT = "github.comment"
    GITHUB_REVIEW = "github.review"
    USER_INPUT = "user.input"
    AGENT_ACTION = "agent.action"
    SYSTEM_EVENT = "system.event"


@dataclass
class ProcessedEvent:
    """An event ready for three-universe processing."""
    event_id: str
    event_type: EventType
    content: str
    metadata: Dict[str, Any]
    timestamp: datetime
    source: str = "unknown"


class ThreeUniverseState(TypedDict, total=False):
    """State for the three-universe processor graph."""
    # Input
    event: Dict[str, Any]
    event_type: str
    
    # Processing state
    engineer_perspective: Optional[Dict[str, Any]]
    ceremony_perspective: Optional[Dict[str, Any]]
    story_engine_perspective: Optional[Dict[str, Any]]
    
    # Output
    analysis: Optional[Dict[str, Any]]
    lead_universe: Optional[str]
    coherence_score: Optional[float]
    
    # Error handling
    error: Optional[str]


# =============================================================================
# Engineer World (Mia) - The Builder
# =============================================================================

def engineer_intent_keywords() -> Dict[str, List[str]]:
    """Keywords that indicate different engineering intents."""
    return {
        "feature_implementation": ["feat:", "feature", "add", "implement", "create", "new"],
        "bug_fix": ["fix:", "bug", "hotfix", "patch", "resolve", "correct"],
        "refactor": ["refactor", "refact:", "cleanup", "restructure", "reorganize"],
        "documentation": ["docs:", "doc:", "documentation", "readme", "comment"],
        "testing": ["test:", "tests:", "testing", "spec", "coverage"],
        "dependency": ["deps:", "dependency", "upgrade", "update", "bump"],
        "configuration": ["config:", "configure", "settings", "env"],
        "performance": ["perf:", "performance", "optimize", "speed", "cache"],
        "security": ["security", "sec:", "vulnerability", "auth", "permission"],
        "ci_cd": ["ci:", "cd:", "pipeline", "workflow", "build"],
    }


def analyze_engineer_perspective(state: ThreeUniverseState) -> ThreeUniverseState:
    """
    Mia's perspective: The Builder (Engineer-world)
    
    Focuses on:
    - What was built/changed
    - Technical impact
    - System architecture implications
    - Flow routing for technical actions
    """
    event = state.get("event", {})
    event_type = state.get("event_type", "")
    
    # Extract relevant content
    content = ""
    if "payload" in event:
        payload = event["payload"]
        if "commits" in payload:
            content = " ".join(c.get("message", "") for c in payload["commits"])
        elif "issue" in payload:
            content = payload["issue"].get("title", "") + " " + payload["issue"].get("body", "")
        elif "pull_request" in payload:
            content = payload["pull_request"].get("title", "") + " " + payload["pull_request"].get("body", "")
    elif "content" in event:
        content = event["content"]
    
    content_lower = content.lower()
    
    # Analyze intent based on keywords
    keywords = engineer_intent_keywords()
    intent_scores: Dict[str, float] = {}
    
    for intent, terms in keywords.items():
        score = sum(1 for term in terms if term.lower() in content_lower)
        if score > 0:
            intent_scores[intent] = score / len(terms)
    
    # Determine primary intent
    if intent_scores:
        intent = max(intent_scores, key=intent_scores.get)
        confidence = min(0.95, 0.6 + intent_scores[intent] * 0.4)
    else:
        intent = "maintenance"
        confidence = 0.5
    
    # Map intents to suggested flows
    flow_map = {
        "feature_implementation": ["code_review", "integration_test", "documentation_update"],
        "bug_fix": ["regression_test", "root_cause_analysis", "changelog_update"],
        "refactor": ["architecture_review", "performance_test", "code_quality"],
        "documentation": ["doc_review", "example_validation"],
        "testing": ["coverage_analysis", "test_quality_review"],
        "dependency": ["security_scan", "compatibility_test"],
        "configuration": ["validation_test", "rollback_plan"],
        "performance": ["benchmark", "profiling", "optimization_review"],
        "security": ["security_audit", "penetration_test", "credential_scan"],
        "ci_cd": ["pipeline_validation", "deployment_test"],
        "maintenance": ["standard_ci"],
    }
    
    suggested_flows = flow_map.get(intent, ["standard_ci"])
    
    # Build context
    context = {
        "detected_keywords": [k for k, v in intent_scores.items() if v > 0],
        "content_length": len(content),
        "event_type": event_type,
        "technical_scope": _determine_technical_scope(content, event),
        "estimated_complexity": _estimate_complexity(content, event),
    }
    
    perspective = UniversePerspective(
        universe=Universe.ENGINEER,
        intent=intent,
        confidence=confidence,
        suggested_flows=suggested_flows,
        context=context,
    )
    
    return {**state, "engineer_perspective": perspective.to_dict()}


def _determine_technical_scope(content: str, event: Dict[str, Any]) -> str:
    """Determine the technical scope of the change."""
    content_lower = content.lower()
    
    if any(kw in content_lower for kw in ["api", "endpoint", "route"]):
        return "api_layer"
    if any(kw in content_lower for kw in ["database", "schema", "migration"]):
        return "data_layer"
    if any(kw in content_lower for kw in ["ui", "component", "frontend"]):
        return "presentation_layer"
    if any(kw in content_lower for kw in ["test", "spec"]):
        return "testing"
    if any(kw in content_lower for kw in ["config", "env", "settings"]):
        return "configuration"
    
    return "general"


def _estimate_complexity(content: str, event: Dict[str, Any]) -> str:
    """Estimate the complexity of the change."""
    # Simple heuristics
    if "payload" in event:
        commits = event["payload"].get("commits", [])
        if len(commits) > 5:
            return "high"
        if len(commits) > 2:
            return "medium"
    
    content_length = len(content)
    if content_length > 500:
        return "high"
    if content_length > 100:
        return "medium"
    
    return "low"


# =============================================================================
# Ceremony World (Ava8) - The Keeper
# =============================================================================

def ceremony_intent_keywords() -> Dict[str, List[str]]:
    """Keywords that indicate different ceremonial intents."""
    return {
        "co_creation": ["we", "together", "team", "pair", "collaborate", "co-author"],
        "gratitude_expression": ["thanks", "thank you", "grateful", "appreciate", "credit"],
        "witnessing": ["witness", "observe", "acknowledge", "see", "recognize"],
        "sacred_pause": ["pause", "reflect", "consider", "contemplate", "breathe"],
        "relationship_building": ["connect", "relationship", "community", "support"],
        "healing": ["heal", "restore", "repair", "reconcile", "mend"],
        "celebration": ["celebrate", "milestone", "achievement", "success", "complete"],
        "offering": ["offer", "gift", "contribute", "share", "give"],
    }


def analyze_ceremony_perspective(state: ThreeUniverseState) -> ThreeUniverseState:
    """
    Ava8's perspective: The Keeper (Ceremony-world)
    
    Focuses on:
    - Who contributed and their state
    - Relational dynamics (K'é)
    - Witnessing and acknowledgment
    - Seven-generation awareness
    """
    event = state.get("event", {})
    
    # Extract contributor information
    contributors = _extract_contributors(event)
    
    # Extract content for analysis
    content = _extract_content(event)
    content_lower = content.lower()
    
    # Analyze relational intent
    keywords = ceremony_intent_keywords()
    intent_scores: Dict[str, float] = {}
    
    for intent, terms in keywords.items():
        score = sum(1 for term in terms if term in content_lower)
        if score > 0:
            intent_scores[intent] = score / len(terms)
    
    # Special case: multiple contributors = co_creation
    if len(contributors) > 1:
        intent_scores["co_creation"] = intent_scores.get("co_creation", 0) + 0.5
    
    # Determine primary intent
    if intent_scores:
        intent = max(intent_scores, key=intent_scores.get)
        confidence = min(0.95, 0.5 + intent_scores[intent] * 0.4)
    else:
        intent = "individual_offering"
        confidence = 0.6
    
    # Map intents to ceremonial flows
    flow_map = {
        "co_creation": ["witness_collaboration", "honor_contributions", "amplify_voices"],
        "gratitude_expression": ["amplify_acknowledgment", "record_connection", "reciprocity_check"],
        "witnessing": ["hold_space", "reflect_back", "presence"],
        "sacred_pause": ["create_silence", "contemplation_prompt", "breathing_space"],
        "relationship_building": ["map_connections", "strengthen_ties", "introduce_support"],
        "healing": ["compassion_response", "restoration_path", "forgiveness_space"],
        "celebration": ["amplify_joy", "community_acknowledgment", "gratitude_circle"],
        "offering": ["receive_gracefully", "honor_gift", "share_forward"],
        "individual_offering": ["witness_work", "hold_space", "gentle_acknowledgment"],
    }
    
    suggested_flows = flow_map.get(intent, ["witness_work", "hold_space"])
    
    # Build ceremonial context
    context = {
        "contributors": contributors,
        "is_collaborative": len(contributors) > 1,
        "sender_energy": _assess_energy(content),
        "witnessing_needed": _needs_witnessing(content, event),
        "relationship_depth": _assess_relationship_depth(contributors, event),
        "seven_generation_relevance": _assess_long_term_impact(content, event),
    }
    
    perspective = UniversePerspective(
        universe=Universe.CEREMONY,
        intent=intent,
        confidence=confidence,
        suggested_flows=suggested_flows,
        context=context,
    )
    
    return {**state, "ceremony_perspective": perspective.to_dict()}


def _extract_contributors(event: Dict[str, Any]) -> List[str]:
    """Extract contributor names from event."""
    contributors = []
    
    if "sender" in event:
        contributors.append(event["sender"])
    
    if "payload" in event:
        payload = event["payload"]
        
        # Git commits
        if "commits" in payload:
            for commit in payload["commits"]:
                author = commit.get("author", {}).get("name")
                if author and author not in contributors:
                    contributors.append(author)
        
        # Issue/PR author
        if "issue" in payload:
            author = payload["issue"].get("user", {}).get("login")
            if author and author not in contributors:
                contributors.append(author)
        
        if "pull_request" in payload:
            author = payload["pull_request"].get("user", {}).get("login")
            if author and author not in contributors:
                contributors.append(author)
    
    return contributors if contributors else ["unknown"]


def _extract_content(event: Dict[str, Any]) -> str:
    """Extract text content from event."""
    if "content" in event:
        return event["content"]
    
    if "payload" in event:
        payload = event["payload"]
        parts = []
        
        if "commits" in payload:
            parts.extend(c.get("message", "") for c in payload["commits"])
        if "issue" in payload:
            parts.append(payload["issue"].get("title", ""))
            parts.append(payload["issue"].get("body", ""))
        if "pull_request" in payload:
            parts.append(payload["pull_request"].get("title", ""))
            parts.append(payload["pull_request"].get("body", ""))
        if "comment" in payload:
            parts.append(payload["comment"].get("body", ""))
        
        return " ".join(filter(None, parts))
    
    return ""


def _assess_energy(content: str) -> str:
    """Assess the energy/tone of the content."""
    content_lower = content.lower()
    
    if any(word in content_lower for word in ["urgent", "critical", "asap", "emergency"]):
        return "urgent_flow"
    if any(word in content_lower for word in ["excited", "happy", "great", "awesome"]):
        return "joyful_flow"
    if any(word in content_lower for word in ["stuck", "blocked", "help", "issue"]):
        return "seeking_support"
    if any(word in content_lower for word in ["thoughtful", "consider", "reflect"]):
        return "contemplative_flow"
    
    return "steady_flow"


def _needs_witnessing(content: str, event: Dict[str, Any]) -> bool:
    """Determine if this event needs explicit witnessing."""
    # New contributors need witnessing
    contributors = _extract_contributors(event)
    # First contribution detection would need history - assume yes for now
    
    # Vulnerable sharing needs witnessing
    content_lower = content.lower()
    if any(word in content_lower for word in ["first", "new", "trying", "learning", "help"]):
        return True
    
    # Significant achievements need witnessing
    if any(word in content_lower for word in ["complete", "achieve", "milestone", "done"]):
        return True
    
    return False


def _assess_relationship_depth(contributors: List[str], event: Dict[str, Any]) -> str:
    """Assess the depth of relationship (would use history in production)."""
    if len(contributors) > 2:
        return "community"
    if len(contributors) > 1:
        return "pair"
    return "individual"


def _assess_long_term_impact(content: str, event: Dict[str, Any]) -> float:
    """Assess the seven-generation relevance (long-term impact)."""
    content_lower = content.lower()
    
    score = 0.3  # Base score
    
    # Infrastructure changes have long-term impact
    if any(word in content_lower for word in ["architecture", "foundation", "core", "framework"]):
        score += 0.3
    
    # Documentation affects future generations
    if any(word in content_lower for word in ["document", "guide", "tutorial", "example"]):
        score += 0.2
    
    # Breaking changes affect the future
    if any(word in content_lower for word in ["breaking", "migration", "deprecate"]):
        score += 0.2
    
    return min(1.0, score)


# =============================================================================
# Story Engine World (Miette) - The Weaver
# =============================================================================

def story_engine_intent_keywords() -> Dict[str, List[str]]:
    """Keywords that indicate different narrative functions."""
    return {
        "inciting_incident": ["init", "start", "begin", "new", "first", "introduce"],
        "rising_action": ["add", "implement", "build", "develop", "progress", "continue"],
        "turning_point": ["feat:", "major", "significant", "pivot", "change", "transform"],
        "complication": ["issue", "problem", "bug", "error", "conflict", "challenge"],
        "crisis": ["critical", "urgent", "breaking", "emergency", "blocker"],
        "climax": ["complete", "finish", "final", "release", "launch", "deploy"],
        "resolution": ["fix", "resolve", "close", "merge", "done"],
        "denouement": ["cleanup", "refactor", "optimize", "polish", "improve"],
    }


def analyze_story_engine_perspective(state: ThreeUniverseState) -> ThreeUniverseState:
    """
    Miette's perspective: The Weaver (Story-engine-world)
    
    Focuses on:
    - Narrative position (which act/phase)
    - Dramatic function
    - Story arc progression
    - Character development
    """
    event = state.get("event", {})
    content = _extract_content(event)
    content_lower = content.lower()
    
    # Analyze narrative function
    keywords = story_engine_intent_keywords()
    intent_scores: Dict[str, float] = {}
    
    for intent, terms in keywords.items():
        score = sum(1 for term in terms if term in content_lower)
        if score > 0:
            intent_scores[intent] = score / len(terms)
    
    # Determine primary intent
    if intent_scores:
        intent = max(intent_scores, key=intent_scores.get)
        confidence = min(0.95, 0.55 + intent_scores[intent] * 0.4)
    else:
        intent = "rising_action"
        confidence = 0.5
    
    # Map intent to act
    act_map = {
        "inciting_incident": 1,
        "rising_action": 2,
        "turning_point": 2,
        "complication": 2,
        "crisis": 2,
        "climax": 3,
        "resolution": 3,
        "denouement": 3,
    }
    act = act_map.get(intent, 2)
    
    # Map intent to narrative function enum
    function_map = {
        "inciting_incident": "inciting_incident",
        "rising_action": "rising_action",
        "turning_point": "turning_point",
        "complication": "complication",
        "crisis": "crisis",
        "climax": "climax",
        "resolution": "resolution",
        "denouement": "denouement",
    }
    narrative_function = function_map.get(intent, "beat")
    
    # Suggested flows for story engine
    flow_map = {
        "inciting_incident": ["establish_stakes", "introduce_characters", "set_tone"],
        "rising_action": ["advance_narrative", "develop_characters", "build_tension"],
        "turning_point": ["mark_pivot", "shift_perspective", "update_arc"],
        "complication": ["deepen_conflict", "raise_stakes", "add_obstacle"],
        "crisis": ["peak_tension", "force_decision", "approach_climax"],
        "climax": ["resolve_main_conflict", "character_transformation", "theme_revelation"],
        "resolution": ["tie_loose_ends", "show_consequences", "new_equilibrium"],
        "denouement": ["reflect_journey", "hint_future", "final_image"],
    }
    
    suggested_flows = flow_map.get(intent, ["advance_narrative", "update_arc_position"])
    
    # Calculate dramatic tension
    dramatic_tension = _calculate_dramatic_tension(intent, content)
    
    # Build story context
    context = {
        "act": act,
        "narrative_function": narrative_function,
        "dramatic_tension": dramatic_tension,
        "suggested_next_beat": _suggest_next_beat(intent),
        "character_impact": _assess_character_impact(content),
        "theme_resonance": _assess_theme_resonance(content),
        "pacing_suggestion": _suggest_pacing(intent, dramatic_tension),
    }
    
    perspective = UniversePerspective(
        universe=Universe.STORY_ENGINE,
        intent=intent,
        confidence=confidence,
        suggested_flows=suggested_flows,
        context=context,
    )
    
    return {**state, "story_engine_perspective": perspective.to_dict()}


def _calculate_dramatic_tension(intent: str, content: str) -> float:
    """Calculate the dramatic tension level (0.0 - 1.0)."""
    base_tension = {
        "inciting_incident": 0.4,
        "rising_action": 0.5,
        "turning_point": 0.7,
        "complication": 0.6,
        "crisis": 0.9,
        "climax": 1.0,
        "resolution": 0.4,
        "denouement": 0.2,
    }
    
    tension = base_tension.get(intent, 0.5)
    
    # Adjust based on content intensity
    content_lower = content.lower()
    if any(word in content_lower for word in ["urgent", "critical", "breaking"]):
        tension = min(1.0, tension + 0.2)
    if any(word in content_lower for word in ["minor", "small", "trivial"]):
        tension = max(0.1, tension - 0.2)
    
    return round(tension, 2)


def _suggest_next_beat(current_intent: str) -> str:
    """Suggest what narrative beat should come next."""
    next_beat_map = {
        "inciting_incident": "rising_action",
        "rising_action": "complication",
        "turning_point": "rising_action",
        "complication": "crisis",
        "crisis": "climax",
        "climax": "resolution",
        "resolution": "denouement",
        "denouement": "inciting_incident",  # New cycle
    }
    return next_beat_map.get(current_intent, "rising_action")


def _assess_character_impact(content: str) -> str:
    """Assess how this event impacts character development."""
    content_lower = content.lower()
    
    if any(word in content_lower for word in ["transform", "change", "grow", "learn"]):
        return "transformative"
    if any(word in content_lower for word in ["challenge", "struggle", "overcome"]):
        return "character_testing"
    if any(word in content_lower for word in ["connect", "relationship", "team"]):
        return "relational"
    
    return "incremental"


def _assess_theme_resonance(content: str) -> str:
    """Assess which themes resonate in this content."""
    content_lower = content.lower()
    
    themes = []
    if any(word in content_lower for word in ["together", "team", "collaborate"]):
        themes.append("collaboration")
    if any(word in content_lower for word in ["integrate", "connect", "bridge"]):
        themes.append("integration")
    if any(word in content_lower for word in ["coherent", "consistent", "unified"]):
        themes.append("coherence")
    if any(word in content_lower for word in ["transform", "change", "evolve"]):
        themes.append("transformation")
    
    return ", ".join(themes) if themes else "development"


def _suggest_pacing(intent: str, tension: float) -> str:
    """Suggest narrative pacing based on intent and tension."""
    if tension > 0.8:
        return "accelerate"
    if tension < 0.3:
        return "breathe"
    if intent in ["inciting_incident", "climax"]:
        return "emphasize"
    return "steady"


# =============================================================================
# Synthesis - Combining All Three Perspectives
# =============================================================================

def synthesize_perspectives(state: ThreeUniverseState) -> ThreeUniverseState:
    """
    Combine all three universe perspectives into a unified analysis.
    
    Determines:
    - Lead universe (who should drive the response)
    - Coherence score (how well the perspectives align)
    """
    engineer = state.get("engineer_perspective", {})
    ceremony = state.get("ceremony_perspective", {})
    story_engine = state.get("story_engine_perspective", {})
    
    if not all([engineer, ceremony, story_engine]):
        return {
            **state,
            "error": "Missing one or more perspectives",
        }
    
    # Create perspective objects
    engineer_p = UniversePerspective.from_dict(engineer)
    ceremony_p = UniversePerspective.from_dict(ceremony)
    story_engine_p = UniversePerspective.from_dict(story_engine)
    
    # Determine lead universe based on confidence and special conditions
    lead = _determine_lead_universe(engineer_p, ceremony_p, story_engine_p)
    
    # Calculate coherence
    coherence = _calculate_coherence(engineer_p, ceremony_p, story_engine_p)
    
    # Build the analysis
    analysis = ThreeUniverseAnalysis(
        engineer=engineer_p,
        ceremony=ceremony_p,
        story_engine=story_engine_p,
        lead_universe=lead,
        coherence_score=coherence,
    )
    
    return {
        **state,
        "analysis": analysis.to_dict(),
        "lead_universe": lead.value,
        "coherence_score": coherence,
    }


def _determine_lead_universe(
    engineer: UniversePerspective,
    ceremony: UniversePerspective,
    story_engine: UniversePerspective,
) -> Universe:
    """
    Determine which universe should lead the response.
    
    Priority logic:
    1. CEREMONY leads if: new contributor, sacred pause needed, relational obligation
    2. STORY_ENGINE leads if: narrative coherence critical, character arc in focus
    3. ENGINEER leads if: technical precision critical, schema validation required
    4. Otherwise: highest confidence wins
    """
    # Check ceremony priority conditions
    ceremony_context = ceremony.context
    if ceremony_context.get("witnessing_needed"):
        return Universe.CEREMONY
    if ceremony_context.get("is_collaborative"):
        # Collaborative work honors the ceremony world
        return Universe.CEREMONY
    
    # Check story engine priority conditions
    story_context = story_engine.context
    if story_context.get("dramatic_tension", 0) > 0.8:
        # High drama moments are led by story engine
        return Universe.STORY_ENGINE
    if story_context.get("narrative_function") in ["climax", "turning_point"]:
        return Universe.STORY_ENGINE
    
    # Check engineer priority conditions
    engineer_context = engineer.context
    if engineer_context.get("estimated_complexity") == "high":
        return Universe.ENGINEER
    if engineer.intent in ["security", "bug_fix"]:
        # Technical urgency
        return Universe.ENGINEER
    
    # Default: highest confidence
    perspectives = [
        (engineer, Universe.ENGINEER),
        (ceremony, Universe.CEREMONY),
        (story_engine, Universe.STORY_ENGINE),
    ]
    
    return max(perspectives, key=lambda x: x[0].confidence)[1]


def _calculate_coherence(
    engineer: UniversePerspective,
    ceremony: UniversePerspective,
    story_engine: UniversePerspective,
) -> float:
    """
    Calculate how well the three perspectives align.
    
    Higher coherence means the perspectives are complementary.
    Lower coherence might indicate conflicting interpretations.
    """
    # Base: average confidence
    avg_confidence = (engineer.confidence + ceremony.confidence + story_engine.confidence) / 3
    
    # Bonus for alignment
    bonus = 0.0
    
    # If all suggest similar urgency
    engineer_urgent = engineer.intent in ["security", "bug_fix", "performance"]
    ceremony_urgent = ceremony.context.get("sender_energy") == "urgent_flow"
    story_urgent = story_engine.context.get("dramatic_tension", 0) > 0.7
    
    if sum([engineer_urgent, ceremony_urgent, story_urgent]) >= 2:
        bonus += 0.1  # Aligned on urgency
    
    # Penalty for very different confidences (might indicate conflict)
    confidence_spread = max(engineer.confidence, ceremony.confidence, story_engine.confidence) - \
                       min(engineer.confidence, ceremony.confidence, story_engine.confidence)
    
    penalty = confidence_spread * 0.2
    
    coherence = avg_confidence + bonus - penalty
    return round(max(0.0, min(1.0, coherence)), 2)


# =============================================================================
# Graph Definition
# =============================================================================

def create_three_universe_graph() -> "StateGraph":
    """
    Create the three-universe processor graph.
    
    Graph structure:
    
    START → engineer → ceremony → story_engine → synthesize → END
    
    All perspectives are computed, then synthesized.
    """
    if not HAS_LANGGRAPH:
        raise ImportError("LangGraph is required for graph creation. Install with: pip install langgraph")
    
    # Build the graph
    workflow = StateGraph(ThreeUniverseState)
    
    # Add nodes
    workflow.add_node("engineer", analyze_engineer_perspective)
    workflow.add_node("ceremony", analyze_ceremony_perspective)
    workflow.add_node("story_engine", analyze_story_engine_perspective)
    workflow.add_node("synthesize", synthesize_perspectives)
    
    # Define the flow
    workflow.set_entry_point("engineer")
    workflow.add_edge("engineer", "ceremony")
    workflow.add_edge("ceremony", "story_engine")
    workflow.add_edge("story_engine", "synthesize")
    workflow.add_edge("synthesize", END)
    
    return workflow.compile()


class ThreeUniverseProcessor:
    """
    High-level interface for three-universe event processing.
    
    Usage:
        processor = ThreeUniverseProcessor()
        result = processor.process(event)
        print(result.lead_universe)  # "ceremony"
    """
    
    def __init__(self):
        """Initialize the processor with the compiled graph."""
        self._graph = None
    
    @property
    def graph(self):
        """Lazy-load the graph."""
        if self._graph is None:
            self._graph = create_three_universe_graph()
        return self._graph
    
    def process(self, event: Dict[str, Any], event_type: str = "unknown") -> ThreeUniverseAnalysis:
        """
        Process an event through all three universes.
        
        Args:
            event: The event data (webhook payload, user input, etc.)
            event_type: Type of event (e.g., "github.push", "user.input")
        
        Returns:
            ThreeUniverseAnalysis with all perspectives and synthesis
        """
        # Run the graph
        result = self.graph.invoke({
            "event": event,
            "event_type": event_type,
        })
        
        # Check for errors
        if result.get("error"):
            raise ValueError(f"Processing error: {result['error']}")
        
        # Return the analysis
        analysis_dict = result.get("analysis", {})
        return ThreeUniverseAnalysis.from_dict(analysis_dict)
    
    def process_webhook(self, webhook_payload: Dict[str, Any]) -> ThreeUniverseAnalysis:
        """
        Convenience method for processing GitHub webhooks.
        
        Args:
            webhook_payload: Raw webhook payload from GitHub
        
        Returns:
            ThreeUniverseAnalysis
        """
        # Determine event type from webhook
        event_type = "github.push"  # Default
        
        if "issue" in webhook_payload.get("payload", {}):
            event_type = "github.issue"
        elif "pull_request" in webhook_payload.get("payload", {}):
            event_type = "github.pull_request"
        elif "comment" in webhook_payload.get("payload", {}):
            event_type = "github.comment"
        
        return self.process(webhook_payload, event_type)
    
    def create_beat_from_analysis(
        self,
        event: Dict[str, Any],
        analysis: ThreeUniverseAnalysis,
        sequence: int,
    ) -> StoryBeat:
        """
        Create a story beat from event and analysis.
        
        Args:
            event: The original event
            analysis: The three-universe analysis
            sequence: Beat sequence number
        
        Returns:
            StoryBeat ready for storage
        """
        # Map story engine intent to NarrativeFunction
        function_map = {
            "inciting_incident": NarrativeFunction.INCITING_INCIDENT,
            "rising_action": NarrativeFunction.RISING_ACTION,
            "turning_point": NarrativeFunction.TURNING_POINT,
            "complication": NarrativeFunction.COMPLICATION,
            "crisis": NarrativeFunction.CRISIS,
            "climax": NarrativeFunction.CLIMAX,
            "resolution": NarrativeFunction.RESOLUTION,
            "denouement": NarrativeFunction.DENOUEMENT,
        }
        
        story_intent = analysis.story_engine.intent
        narrative_func = function_map.get(story_intent, NarrativeFunction.BEAT)
        
        # Extract act
        act = analysis.story_engine.context.get("act", 2)
        
        # Build content
        content = _extract_content(event)
        if not content:
            content = str(event.get("event_type", "event"))
        
        # Generate beat ID
        timestamp = datetime.now(timezone.utc).isoformat()
        beat_id = f"beat_{timestamp}"
        
        # Source event ID
        source_event_id = None
        if "payload" in event:
            if "head_commit" in event["payload"]:
                source_event_id = event["payload"]["head_commit"].get("id")
            elif "issue" in event["payload"]:
                source_event_id = str(event["payload"]["issue"].get("id"))
            elif "pull_request" in event["payload"]:
                source_event_id = str(event["payload"]["pull_request"].get("id"))
        
        return StoryBeat(
            id=beat_id,
            sequence=sequence,
            content=content[:500] if content else "Event processed",  # Truncate long content
            narrative_function=narrative_func,
            act=act,
            universe_analysis=analysis,
            lead_universe=analysis.lead_universe,
            source="webhook" if "github" in event.get("event_type", "") else "event",
            source_event_id=source_event_id,
        )


# =============================================================================
# Module exports
# =============================================================================

__all__ = [
    "EventType",
    "ProcessedEvent",
    "ThreeUniverseState",
    "ThreeUniverseProcessor",
    "create_three_universe_graph",
    "analyze_engineer_perspective",
    "analyze_ceremony_perspective",
    "analyze_story_engine_perspective",
    "synthesize_perspectives",
]
