"""
🧠 3. Character Arc Generator Graph

A pre-built LangGraph graph that analyzes character development.
"""

from typing import Optional
from langgraph.graph import StateGraph, END

from ..schemas import CharacterArcState
from ..nodes import NCPLoaderNode, NarrativeTraversalNode


class CharacterArcGenerator:
    """
    Generates a summary of a character's arc through the narrative.

    This composite component uses NarrativeTraversalNode to find all relevant
    story beats and story points, then generates a markdown summary of the
    character's journey, referencing their wound, desire, and arc.
    """

    def __init__(self):
        """Initialize the Character Arc Generator graph."""
        self.ncp_loader = NCPLoaderNode()
        self.traversal_node = NarrativeTraversalNode()

    def _gather_character_beats(self, state: CharacterArcState) -> CharacterArcState:
        """
        Gather all story beats involving the character.

        Args:
            state: Current character arc state

        Returns:
            Updated state with character beats in metadata
        """
        if not state.get("ncp_data"):
            return {
                **state,
                "error": "No NCP data loaded"
            }

        ncp_data = state["ncp_data"]
        player_id = state.get("player_id")

        if not player_id:
            return {
                **state,
                "error": "No player_id provided"
            }

        # Get character info
        player = ncp_data.get_player(player_id)
        if not player:
            return {
                **state,
                "error": f"Player not found: {player_id}"
            }

        # Get all story beats for this character
        beats = ncp_data.get_player_storybeats(player_id)

        # Store in metadata
        updated_metadata = {
            **state.get("metadata", {}),
            "player": player.dict(),
            "character_beats": [beat.dict() for beat in beats],
            "traversal_mode": "player_journey"
        }

        return {
            **state,
            "metadata": updated_metadata,
            "error": None
        }

    def _generate_arc_summary(self, state: CharacterArcState) -> CharacterArcState:
        """
        Generate a markdown summary of the character's arc.

        Args:
            state: Current character arc state with gathered beats

        Returns:
            Updated state with character_arc_summary
        """
        metadata = state.get("metadata", {})
        player = metadata.get("player")
        beats = metadata.get("character_beats", [])

        if not player:
            return {
                **state,
                "error": "Player data not found in metadata"
            }

        # Generate the arc summary
        summary = self._build_arc_markdown(player, beats)

        return {
            **state,
            "character_arc_summary": summary,
            "error": None
        }

    def _build_arc_markdown(self, player: dict, beats: list) -> str:
        """
        Build the markdown summary of the character arc.

        Args:
            player: Player/character data
            beats: List of story beats

        Returns:
            Markdown formatted character arc summary
        """
        md = f"# Character Arc: {player['name']}\n\n"

        # Character foundation
        md += "## Character Foundation\n\n"
        if player.get('wound'):
            md += f"**Wound**: {player['wound']}\n\n"
        if player.get('desire'):
            md += f"**Desire**: {player['desire']}\n\n"
        if player.get('arc'):
            md += f"**Arc**: {player['arc']}\n\n"

        # Journey through story beats
        md += "## Journey\n\n"

        if beats:
            for i, beat in enumerate(beats, 1):
                md += f"### {i}. {beat['title']}\n\n"
                md += f"{beat['description']}\n\n"
                if beat.get('emotional_weight'):
                    md += f"*Emotional tone: {beat['emotional_weight']}*\n\n"

                # Add moments if present
                if beat.get('moments'):
                    md += "**Key Moments:**\n"
                    for moment in beat['moments']:
                        md += f"- {moment['description']}\n"
                    md += "\n"
        else:
            md += "*No story beats found for this character.*\n\n"

        # Character transformation
        md += "## Character Transformation\n\n"
        if player.get('arc'):
            md += f"{player['arc']}\n\n"
        else:
            md += "*Character arc to be determined.*\n\n"

        return md

    def build_graph(self) -> StateGraph:
        """
        Build the LangGraph workflow for character arc generation.

        Returns:
            Compiled StateGraph
        """
        workflow = StateGraph(CharacterArcState)

        # Add nodes
        workflow.add_node("gather_beats", self._gather_character_beats)
        workflow.add_node("generate_summary", self._generate_arc_summary)

        # Define edges
        workflow.set_entry_point("gather_beats")
        workflow.add_edge("gather_beats", "generate_summary")
        workflow.add_edge("generate_summary", END)

        return workflow.compile()

    def generate(
        self,
        ncp_data,
        player_id: str,
        include_metadata: bool = False
    ) -> str:
        """
        Generate a character arc summary.

        Args:
            ncp_data: NCPData object
            player_id: ID of the character to analyze
            include_metadata: Whether to return full state with metadata

        Returns:
            Character arc summary as markdown string (or full state if include_metadata=True)
        """
        # Initialize state
        initial_state = {
            "ncp_data": ncp_data,
            "player_id": player_id,
            "messages": [],
            "error": None,
            "metadata": {},
            "character_arc_summary": None
        }

        # Build and run the graph
        graph = self.build_graph()
        result = graph.invoke(initial_state)

        if include_metadata:
            return result
        else:
            return result.get("character_arc_summary", "Error generating arc")
