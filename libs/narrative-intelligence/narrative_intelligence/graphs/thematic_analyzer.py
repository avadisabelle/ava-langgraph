"""
🧠 4. Thematic Tension Analyzer Graph

A LangGraph graph that analyzes how thematic tensions are explored in the narrative.
"""

from typing import List, Optional
from langgraph.graph import StateGraph, END

from ..schemas import ThematicAnalysisState
from ..nodes import NarrativeTraversalNode, NCPLoaderNode


class ThematicTensionAnalyzer:
    """
    Analyzes how a specific thematic tension is explored throughout the story.

    This component uses traversal to find matching story beats and moments,
    then synthesizes an analysis of how the theme manifests in the narrative.
    """

    def __init__(self):
        """Initialize the Thematic Tension Analyzer graph."""
        self.traversal_node = NarrativeTraversalNode()

    def _generate_search_queries(self, state: ThematicAnalysisState) -> ThematicAnalysisState:
        """
        Generate search queries based on the perspective.

        Args:
            state: Current thematic analysis state

        Returns:
            Updated state with search queries in metadata
        """
        if not state.get("ncp_data"):
            return {
                **state,
                "error": "No NCP data loaded"
            }

        ncp_data = state["ncp_data"]
        perspective_id = state.get("perspective_id")

        if not perspective_id:
            return {
                **state,
                "error": "No perspective_id provided"
            }

        # Get perspective info
        perspective = ncp_data.get_perspective(perspective_id)
        if not perspective:
            return {
                **state,
                "error": f"Perspective not found: {perspective_id}"
            }

        # Generate search terms from perspective
        search_terms = []

        if perspective.description:
            search_terms.extend(perspective.description.lower().split())

        if perspective.thematic_question:
            # Extract key words from the thematic question
            question_words = perspective.thematic_question.lower().split()
            # Filter out common question words
            stopwords = {'what', 'how', 'why', 'when', 'where', 'who', 'is', 'are', 'the', 'a', 'an', 'does', 'do'}
            search_terms.extend([word for word in question_words if word not in stopwords])

        if perspective.tension:
            # Split tension like "Safety vs Vulnerability" into keywords
            tension_words = perspective.tension.replace(" vs ", " ").replace(" vs. ", " ").split()
            search_terms.extend([word.lower() for word in tension_words])

        # Remove duplicates while preserving order
        search_terms = list(dict.fromkeys(search_terms))

        # Store in metadata
        updated_metadata = {
            **state.get("metadata", {}),
            "perspective": perspective.dict(),
            "search_terms": search_terms,
            "traversal_mode": "thematic_trace"
        }

        return {
            **state,
            "metadata": updated_metadata,
            "error": None
        }

    def _find_thematic_beats(self, state: ThematicAnalysisState) -> ThematicAnalysisState:
        """
        Find story beats that match the thematic search.

        Args:
            state: Current thematic analysis state

        Returns:
            Updated state with relevant_storybeat_ids
        """
        if not state.get("ncp_data"):
            return {
                **state,
                "error": "No NCP data loaded"
            }

        ncp_data = state["ncp_data"]
        metadata = state.get("metadata", {})
        search_terms = metadata.get("search_terms", [])
        perspective_id = state.get("perspective_id")

        if not perspective_id:
            return {
                **state,
                "error": "No perspective_id provided"
            }

        # Use traversal node to find matching beats
        matching_beats = self.traversal_node.find_thematic_beats(
            ncp_data,
            perspective_id,
            search_terms
        )

        # Extract IDs
        relevant_ids = [beat.storybeat_id for beat in matching_beats]

        # Store detailed beat information in metadata
        updated_metadata = {
            **metadata,
            "matching_beats": [beat.dict() for beat in matching_beats]
        }

        return {
            **state,
            "relevant_storybeat_ids": relevant_ids,
            "metadata": updated_metadata,
            "error": None
        }

    def _synthesize_analysis(self, state: ThematicAnalysisState) -> ThematicAnalysisState:
        """
        Synthesize the thematic analysis.

        Args:
            state: Current thematic analysis state

        Returns:
            Updated state with thematic_analysis
        """
        metadata = state.get("metadata", {})
        perspective = metadata.get("perspective")
        matching_beats = metadata.get("matching_beats", [])

        if not perspective:
            return {
                **state,
                "error": "Perspective data not found in metadata"
            }

        # Generate the analysis
        analysis = self._build_thematic_analysis_markdown(perspective, matching_beats)

        return {
            **state,
            "thematic_analysis": analysis,
            "error": None
        }

    def _build_thematic_analysis_markdown(self, perspective: dict, beats: list) -> str:
        """
        Build the markdown analysis of the thematic tension.

        Args:
            perspective: Perspective/theme data
            beats: List of matching story beats

        Returns:
            Markdown formatted thematic analysis
        """
        md = f"# Thematic Analysis: {perspective['name']}\n\n"

        # Perspective overview
        md += "## Thematic Lens\n\n"
        if perspective.get('description'):
            md += f"{perspective['description']}\n\n"
        if perspective.get('tension'):
            md += f"**Core Tension**: {perspective['tension']}\n\n"
        if perspective.get('thematic_question'):
            md += f"**Thematic Question**: {perspective['thematic_question']}\n\n"

        # Analysis of how theme manifests
        md += "## How This Theme Manifests in the Narrative\n\n"

        if beats:
            md += f"Found **{len(beats)}** story beats that explore this theme:\n\n"

            for i, beat in enumerate(beats, 1):
                md += f"### {i}. {beat['title']}\n\n"
                md += f"{beat['description']}\n\n"

                if beat.get('emotional_weight'):
                    md += f"*Emotional resonance: {beat['emotional_weight']}*\n\n"

                # Analyze thematic relevance
                md += "**Thematic Relevance**: "
                if perspective.get('tension'):
                    md += f"This beat explores the tension between {perspective['tension']} through "
                    md += "the choices and conflicts presented.\n\n"
                else:
                    md += "This beat resonates with the central thematic question.\n\n"

        else:
            md += "*No story beats found that explicitly explore this theme. "
            md += "This could indicate an area for narrative development.*\n\n"

        # Thematic synthesis
        md += "## Thematic Synthesis\n\n"
        if len(beats) > 0:
            md += f"This theme appears {len(beats)} times throughout the narrative, "
            md += "indicating its significance to the overall story. "

            if len(beats) >= 5:
                md += "The frequency suggests this is a **major thematic pillar** of the narrative.\n\n"
            elif len(beats) >= 3:
                md += "This theme receives **moderate exploration** in the story.\n\n"
            else:
                md += "This theme is **lightly touched upon** and could be developed further.\n\n"
        else:
            md += "This theme does not appear explicitly in the current narrative beats. "
            md += "Consider whether this represents a missed opportunity for thematic depth.\n\n"

        return md

    def build_graph(self) -> StateGraph:
        """
        Build the LangGraph workflow for thematic tension analysis.

        Returns:
            Compiled StateGraph
        """
        workflow = StateGraph(ThematicAnalysisState)

        # Add nodes
        workflow.add_node("generate_queries", self._generate_search_queries)
        workflow.add_node("find_beats", self._find_thematic_beats)
        workflow.add_node("synthesize", self._synthesize_analysis)

        # Define edges
        workflow.set_entry_point("generate_queries")
        workflow.add_edge("generate_queries", "find_beats")
        workflow.add_edge("find_beats", "synthesize")
        workflow.add_edge("synthesize", END)

        return workflow.compile()

    def analyze(
        self,
        ncp_data,
        perspective_id: str,
        include_metadata: bool = False
    ) -> str:
        """
        Analyze how a thematic tension is explored in the narrative.

        Args:
            ncp_data: NCPData object
            perspective_id: ID of the perspective/theme to analyze
            include_metadata: Whether to return full state with metadata

        Returns:
            Thematic analysis as markdown string (or full state if include_metadata=True)
        """
        # Initialize state
        initial_state = {
            "ncp_data": ncp_data,
            "perspective_id": perspective_id,
            "relevant_storybeat_ids": [],
            "messages": [],
            "error": None,
            "metadata": {},
            "thematic_analysis": None
        }

        # Build and run the graph
        graph = self.build_graph()
        result = graph.invoke(initial_state)

        if include_metadata:
            return result
        else:
            return result.get("thematic_analysis", "Error generating analysis")
