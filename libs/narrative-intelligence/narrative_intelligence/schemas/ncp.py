"""
Pydantic models for the Narrative Context Protocol (NCP).

These models define the structure of narrative data following the NCP specification.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class Moment(BaseModel):
    """A specific moment or event within a story beat."""
    moment_id: str = Field(..., description="Unique identifier for the moment")
    description: str = Field(..., description="Description of the moment")
    timestamp: Optional[str] = Field(None, description="When this moment occurs in the narrative")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class StoryPoint(BaseModel):
    """A key story point or plot point in the narrative."""
    storypoint_id: str = Field(..., description="Unique identifier for the story point")
    title: str = Field(..., description="Title or name of the story point")
    description: str = Field(..., description="Description of the story point")
    type: Optional[str] = Field(None, description="Type of story point (e.g., 'inciting_incident', 'climax')")
    related_players: List[str] = Field(default_factory=list, description="Player IDs involved in this story point")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class StoryBeat(BaseModel):
    """A story beat representing a unit of narrative progression."""
    storybeat_id: str = Field(..., description="Unique identifier for the story beat")
    title: str = Field(..., description="Title or name of the story beat")
    description: str = Field(..., description="Description of the story beat")
    emotional_weight: Optional[str] = Field(None, description="Emotional tone (e.g., 'Devastating', 'Hopeful', 'Tense')")
    moments: List[Moment] = Field(default_factory=list, description="Moments within this story beat")
    related_players: List[str] = Field(default_factory=list, description="Player IDs involved in this beat")
    related_storypoints: List[str] = Field(default_factory=list, description="Story point IDs related to this beat")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class Player(BaseModel):
    """A character or entity in the narrative."""
    player_id: str = Field(..., description="Unique identifier for the player/character")
    name: str = Field(..., description="Name of the character")
    wound: Optional[str] = Field(None, description="The character's wound or trauma")
    desire: Optional[str] = Field(None, description="The character's primary desire or goal")
    arc: Optional[str] = Field(None, description="Description of the character's arc or transformation")
    role: Optional[str] = Field(None, description="Role in the story (e.g., 'protagonist', 'antagonist')")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class Perspective(BaseModel):
    """A thematic perspective or lens through which to view the narrative."""
    perspective_id: str = Field(..., description="Unique identifier for the perspective")
    name: str = Field(..., description="Name of the perspective")
    description: str = Field(..., description="Description of this thematic perspective")
    thematic_question: Optional[str] = Field(None, description="The central question this perspective explores")
    tension: Optional[str] = Field(None, description="The tension or conflict (e.g., 'Safety vs Vulnerability')")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class NCPData(BaseModel):
    """Complete Narrative Context Protocol data structure."""
    title: str = Field(..., description="Title of the narrative")
    author: Optional[str] = Field(None, description="Author of the narrative")
    version: str = Field(default="1.0", description="NCP schema version")

    players: List[Player] = Field(default_factory=list, description="Characters in the narrative")
    perspectives: List[Perspective] = Field(default_factory=list, description="Thematic perspectives")
    storybeats: List[StoryBeat] = Field(default_factory=list, description="Story beats")
    storypoints: List[StoryPoint] = Field(default_factory=list, description="Story points")

    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional narrative metadata")

    def get_player(self, player_id: str) -> Optional[Player]:
        """Get a player by ID."""
        return next((p for p in self.players if p.player_id == player_id), None)

    def get_perspective(self, perspective_id: str) -> Optional[Perspective]:
        """Get a perspective by ID."""
        return next((p for p in self.perspectives if p.perspective_id == perspective_id), None)

    def get_storybeat(self, storybeat_id: str) -> Optional[StoryBeat]:
        """Get a story beat by ID."""
        return next((sb for sb in self.storybeats if sb.storybeat_id == storybeat_id), None)

    def get_storypoint(self, storypoint_id: str) -> Optional[StoryPoint]:
        """Get a story point by ID."""
        return next((sp for sp in self.storypoints if sp.storypoint_id == storypoint_id), None)

    def get_player_storybeats(self, player_id: str) -> List[StoryBeat]:
        """Get all story beats involving a specific player."""
        return [sb for sb in self.storybeats if player_id in sb.related_players]

    def get_storybeats_by_emotional_weight(self, emotional_weight: str) -> List[StoryBeat]:
        """Get all story beats with a specific emotional weight."""
        return [sb for sb in self.storybeats if sb.emotional_weight == emotional_weight]
