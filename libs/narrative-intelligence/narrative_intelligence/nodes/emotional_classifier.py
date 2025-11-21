"""
🧠 5. Emotional Beat Classifier Node

A LangGraph node that classifies the emotional tone of story beats.
"""

from typing import Optional, List, Dict, Any
from enum import Enum

from ..schemas import StoryBeat, NCPState, EmotionalClassificationState


class EmotionalTone(Enum):
    """Predefined emotional tone categories."""
    DEVASTATING = "Devastating"
    HOPEFUL = "Hopeful"
    TENSE = "Tense"
    JOYFUL = "Joyful"
    MELANCHOLIC = "Melancholic"
    TRIUMPHANT = "Triumphant"
    FEARFUL = "Fearful"
    PEACEFUL = "Peaceful"
    CONFLICTED = "Conflicted"
    RESIGNED = "Resigned"


class EmotionalBeatClassifierNode:
    """
    Classifies the emotional tone of story beats.

    This node enriches the narrative graph with emotional metadata,
    enabling new forms of analysis and visualization.
    """

    def __init__(
        self,
        use_llm: bool = True,
        model_name: Optional[str] = None,
        custom_categories: Optional[List[str]] = None
    ):
        """
        Initialize the Emotional Beat Classifier Node.

        Args:
            use_llm: Whether to use an LLM for classification (requires langchain)
            model_name: Name of the LLM model to use (e.g., "gpt-4", "claude-3")
            custom_categories: Optional list of custom emotional categories
        """
        self.use_llm = use_llm
        self.model_name = model_name
        self.categories = custom_categories or [tone.value for tone in EmotionalTone]

    def classify_beat(
        self,
        storybeat: StoryBeat,
        context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Classify the emotional tone of a story beat.

        Args:
            storybeat: The story beat to classify
            context: Optional additional context for classification

        Returns:
            Dictionary containing classification and confidence score
        """
        # If beat already has emotional_weight, use it as baseline
        if storybeat.emotional_weight:
            return {
                "classification": storybeat.emotional_weight,
                "confidence": 1.0,
                "method": "existing"
            }

        if self.use_llm:
            return self._classify_with_llm(storybeat, context)
        else:
            return self._classify_rule_based(storybeat)

    def _classify_with_llm(
        self,
        storybeat: StoryBeat,
        context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Classify using an LLM.

        Args:
            storybeat: The story beat to classify
            context: Optional additional context

        Returns:
            Classification result with confidence score
        """
        try:
            from langchain_core.messages import HumanMessage, SystemMessage
            from langchain_core.language_models import BaseChatModel
        except ImportError:
            # Fallback to rule-based if LangChain not available
            return self._classify_rule_based(storybeat)

        # Construct the classification prompt
        prompt = self._build_classification_prompt(storybeat, context)

        # For now, return a structured response
        # In actual implementation, you'd call an LLM here
        return {
            "classification": self._classify_rule_based(storybeat)["classification"],
            "confidence": 0.8,
            "method": "llm_placeholder",
            "prompt": prompt
        }

    def _build_classification_prompt(
        self,
        storybeat: StoryBeat,
        context: Optional[str] = None
    ) -> str:
        """
        Build the LLM classification prompt.

        Args:
            storybeat: The story beat to classify
            context: Optional additional context

        Returns:
            Formatted prompt string
        """
        categories_str = ", ".join(self.categories)

        prompt = f"""Classify the emotional tone of this story beat.

Story Beat: {storybeat.title}
Description: {storybeat.description}

Available categories: {categories_str}

Analyze the emotional weight and tone of this beat. Consider:
1. The language and imagery used
2. The actions and events described
3. The overall mood conveyed

Respond with:
1. The most appropriate emotional category
2. A confidence score (0.0-1.0)
3. A brief explanation of your classification

Classification:"""

        if context:
            prompt = f"{prompt}\n\nAdditional Context:\n{context}\n"

        return prompt

    def _classify_rule_based(self, storybeat: StoryBeat) -> Dict[str, Any]:
        """
        Simple rule-based classification using keyword matching.

        Args:
            storybeat: The story beat to classify

        Returns:
            Classification result
        """
        text = f"{storybeat.title} {storybeat.description}".lower()

        # Keyword mappings for emotional tones
        tone_keywords = {
            EmotionalTone.DEVASTATING.value: ["destroy", "loss", "death", "tragedy", "grief", "devastat"],
            EmotionalTone.HOPEFUL.value: ["hope", "bright", "promise", "future", "optimis", "dream"],
            EmotionalTone.TENSE.value: ["tense", "anxious", "nervous", "edge", "suspense", "uncertain"],
            EmotionalTone.JOYFUL.value: ["joy", "happy", "celebrate", "triumph", "delight", "elat"],
            EmotionalTone.MELANCHOLIC.value: ["sad", "melanchol", "wistful", "longing", "regret", "sorrow"],
            EmotionalTone.TRIUMPHANT.value: ["victory", "triumph", "succeed", "conquer", "win", "achieve"],
            EmotionalTone.FEARFUL.value: ["fear", "terror", "dread", "frighten", "horror", "panic"],
            EmotionalTone.PEACEFUL.value: ["peace", "calm", "serene", "tranquil", "quiet", "still"],
            EmotionalTone.CONFLICTED.value: ["conflict", "torn", "struggle", "dilemma", "uncertain", "doubt"],
            EmotionalTone.RESIGNED.value: ["resign", "accept", "inevitable", "surrender", "fate", "give up"],
        }

        # Score each tone based on keyword matches
        scores = {}
        for tone, keywords in tone_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text)
            if score > 0:
                scores[tone] = score

        if scores:
            # Return the tone with highest score
            best_tone = max(scores.items(), key=lambda x: x[1])
            confidence = min(best_tone[1] / 3.0, 1.0)  # Cap at 1.0
            return {
                "classification": best_tone[0],
                "confidence": confidence,
                "method": "rule_based"
            }
        else:
            # Default to neutral/peaceful if no keywords match
            return {
                "classification": EmotionalTone.PEACEFUL.value,
                "confidence": 0.3,
                "method": "rule_based_default"
            }

    def __call__(self, state: EmotionalClassificationState) -> EmotionalClassificationState:
        """
        LangGraph node callable.

        Expects state to contain:
        - ncp_data: Loaded NCP data
        - storybeat_id: ID of the beat to classify

        Args:
            state: Current EmotionalClassificationState

        Returns:
            Updated state with emotional_classification and confidence_score
        """
        if not state.get("ncp_data"):
            return {
                **state,
                "error": "No NCP data loaded. Run NCPLoaderNode first."
            }

        ncp_data = state["ncp_data"]
        storybeat_id = state.get("storybeat_id")

        if not storybeat_id:
            return {
                **state,
                "error": "No storybeat_id provided for classification."
            }

        try:
            storybeat = ncp_data.get_storybeat(storybeat_id)
            if not storybeat:
                return {
                    **state,
                    "error": f"Story beat not found: {storybeat_id}"
                }

            # Get context from metadata if available
            context = state.get("metadata", {}).get("classification_context")

            # Perform classification
            result = self.classify_beat(storybeat, context)

            return {
                **state,
                "emotional_classification": result["classification"],
                "confidence_score": result["confidence"],
                "error": None,
                "metadata": {
                    **state.get("metadata", {}),
                    "classification_method": result["method"]
                }
            }

        except Exception as e:
            return {
                **state,
                "error": f"Classification error: {str(e)}"
            }
