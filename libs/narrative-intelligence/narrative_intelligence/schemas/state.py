"""State schemas for LangGraph workflows."""

from typing import Optional, List, Dict, Any, Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from .ncp import NCPData


class NCPState(TypedDict):
    """State for NCP-based LangGraph workflows."""
    ncp_data: Optional[NCPData]
    """The loaded NCP data"""

    messages: Annotated[List[Dict[str, Any]], add_messages]
    """Messages for LLM interaction"""

    error: Optional[str]
    """Error message if any"""

    metadata: Dict[str, Any]
    """Additional workflow metadata"""


class CharacterArcState(NCPState):
    """State for character arc generation workflow."""
    player_id: str
    """ID of the character to analyze"""

    character_arc_summary: Optional[str]
    """Generated summary of the character's arc"""


class ThematicAnalysisState(NCPState):
    """State for thematic tension analysis workflow."""
    perspective_id: str
    """ID of the perspective/theme to analyze"""

    relevant_storybeat_ids: List[str]
    """Story beat IDs relevant to this theme"""

    thematic_analysis: Optional[str]
    """Generated thematic analysis"""


class EmotionalClassificationState(NCPState):
    """State for emotional beat classification workflow."""
    storybeat_id: str
    """ID of the story beat to classify"""

    emotional_classification: Optional[str]
    """Classified emotional tone"""

    confidence_score: Optional[float]
    """Confidence score of the classification"""
