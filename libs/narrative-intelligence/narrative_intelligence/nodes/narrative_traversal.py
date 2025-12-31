"""
🧠 2. Narrative Graph Traversal Node

A versatile LangGraph node for navigating and querying the narrative graph.
"""

from typing import List, Callable, Optional, Set, Any
from enum import Enum

from ..schemas import NCPData, StoryBeat, Player, Perspective, StoryPoint, NCPState


class TraversalMode(Enum):
    """Modes for traversing the narrative graph."""
    PLAYER_JOURNEY = "player_journey"  # Follow a character's story
    THEMATIC_TRACE = "thematic_trace"  # Trace a theme through the narrative
    TEMPORAL_SEQUENCE = "temporal_sequence"  # Follow chronological order
    EMOTIONAL_ARC = "emotional_arc"  # Follow emotional progression


class NarrativeTraversalNode:
    """
    Enables efficient and flexible navigation of the narrative graph.

    This node acts as a "search engine" for the narrative, handling complex
    traversal logic and queries.
    """

    def __init__(self, mode: TraversalMode = TraversalMode.PLAYER_JOURNEY):
        """
        Initialize the Narrative Traversal Node.

        Args:
            mode: The traversal mode to use
        """
        self.mode = mode

    def traverse_player_journey(
        self,
        ncp_data: NCPData,
        player_id: str,
        filter_func: Optional[Callable[[StoryBeat], bool]] = None
    ) -> List[StoryBeat]:
        """
        Traverse all story beats involving a specific player.

        Args:
            ncp_data: The NCP data to traverse
            player_id: ID of the player to follow
            filter_func: Optional function to filter story beats

        Returns:
            List of story beats involving the player
        """
        beats = ncp_data.get_player_storybeats(player_id)

        if filter_func:
            beats = [beat for beat in beats if filter_func(beat)]

        return beats

    def find_thematic_beats(
        self,
        ncp_data: NCPData,
        perspective_id: str,
        search_terms: Optional[List[str]] = None
    ) -> List[StoryBeat]:
        """
        Find story beats that resonate with a specific thematic perspective.

        Args:
            ncp_data: The NCP data to search
            perspective_id: ID of the thematic perspective
            search_terms: Optional list of terms to search for in beat descriptions

        Returns:
            List of thematically relevant story beats
        """
        perspective = ncp_data.get_perspective(perspective_id)
        if not perspective:
            return []

        # If search terms provided, use them
        if search_terms:
            return self._search_beats_by_terms(ncp_data, search_terms)

        # Otherwise, use perspective description and thematic question
        default_terms = []
        if perspective.description:
            default_terms.append(perspective.description.lower())
        if perspective.thematic_question:
            default_terms.append(perspective.thematic_question.lower())
        if perspective.tension:
            # Split tension like "Safety vs Vulnerability" into keywords
            default_terms.extend(perspective.tension.lower().split())

        return self._search_beats_by_terms(ncp_data, default_terms)

    def _search_beats_by_terms(
        self,
        ncp_data: NCPData,
        search_terms: List[str]
    ) -> List[StoryBeat]:
        """
        Search story beats by keyword terms.

        Args:
            ncp_data: The NCP data to search
            search_terms: List of search terms

        Returns:
            List of matching story beats
        """
        matching_beats = []
        seen_ids: Set[str] = set()

        for beat in ncp_data.storybeats:
            if beat.storybeat_id in seen_ids:
                continue

            # Search in title and description
            searchable_text = f"{beat.title} {beat.description}".lower()

            # Check if any search term matches
            if any(term.lower() in searchable_text for term in search_terms):
                matching_beats.append(beat)
                seen_ids.add(beat.storybeat_id)

        return matching_beats

    def get_connected_elements(
        self,
        ncp_data: NCPData,
        storybeat_id: str
    ) -> dict:
        """
        Get all elements connected to a specific story beat.

        Args:
            ncp_data: The NCP data
            storybeat_id: ID of the story beat

        Returns:
            Dictionary containing connected players, storypoints, and moments
        """
        beat = ncp_data.get_storybeat(storybeat_id)
        if not beat:
            return {"players": [], "storypoints": [], "moments": []}

        players = [ncp_data.get_player(pid) for pid in beat.related_players]
        players = [p for p in players if p is not None]

        storypoints = [ncp_data.get_storypoint(spid) for spid in beat.related_storypoints]
        storypoints = [sp for sp in storypoints if sp is not None]

        return {
            "players": players,
            "storypoints": storypoints,
            "moments": beat.moments
        }

    def find_beats_by_emotional_weight(
        self,
        ncp_data: NCPData,
        emotional_weight: str
    ) -> List[StoryBeat]:
        """
        Find all story beats with a specific emotional weight.

        Args:
            ncp_data: The NCP data
            emotional_weight: The emotional weight to search for

        Returns:
            List of matching story beats
        """
        return ncp_data.get_storybeats_by_emotional_weight(emotional_weight)

    def __call__(self, state: NCPState) -> NCPState:
        """
        LangGraph node callable.

        Expects state metadata to contain:
        - 'traversal_mode': The traversal mode to use
        - Mode-specific parameters (player_id, perspective_id, etc.)

        Args:
            state: Current NCPState

        Returns:
            Updated NCPState with traversal results in metadata
        """
        if not state.get("ncp_data"):
            return {
                **state,
                "error": "No NCP data loaded. Run NCPLoaderNode first."
            }

        ncp_data = state["ncp_data"]
        metadata = state.get("metadata", {})

        try:
            mode = metadata.get("traversal_mode", self.mode.value)

            if mode == TraversalMode.PLAYER_JOURNEY.value:
                player_id = metadata.get("player_id")
                if not player_id:
                    raise ValueError("player_id required for PLAYER_JOURNEY mode")
                results = self.traverse_player_journey(ncp_data, player_id)

            elif mode == TraversalMode.THEMATIC_TRACE.value:
                perspective_id = metadata.get("perspective_id")
                search_terms = metadata.get("search_terms")
                if not perspective_id:
                    raise ValueError("perspective_id required for THEMATIC_TRACE mode")
                results = self.find_thematic_beats(ncp_data, perspective_id, search_terms)

            elif mode == TraversalMode.EMOTIONAL_ARC.value:
                emotional_weight = metadata.get("emotional_weight")
                if not emotional_weight:
                    raise ValueError("emotional_weight required for EMOTIONAL_ARC mode")
                results = self.find_beats_by_emotional_weight(ncp_data, emotional_weight)

            else:
                raise ValueError(f"Unsupported traversal mode: {mode}")

            # Store results in metadata
            updated_metadata = {
                **metadata,
                "traversal_results": [beat.dict() for beat in results]
            }

            return {
                **state,
                "metadata": updated_metadata,
                "error": None
            }

        except Exception as e:
            return {
                **state,
                "error": f"Traversal error: {str(e)}"
            }
