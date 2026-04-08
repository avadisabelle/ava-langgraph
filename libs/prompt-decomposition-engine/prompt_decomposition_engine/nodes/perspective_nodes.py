"""
Perspective Nodes

Three-universe perspective analysis of decomposed prompts:
- Mia (Engineer): Technical feasibility, dependencies, architecture
- Ava8 (Ceremony): Relational accountability, protocol, governance
- Miette (Story Engine): Narrative coherence, emotional arc, meaning
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List

from prompt_decomposition.directional_decomposer import Direction
from prompt_decomposition.action_stack import DecompositionResult


class Universe(str, Enum):
    ENGINEER = "engineer"
    CEREMONY = "ceremony"
    STORY_ENGINE = "story_engine"


UNIVERSE_NAMES: Dict[Universe, str] = {
    Universe.ENGINEER: "Mia (Engineer)",
    Universe.CEREMONY: "Ava8 (Ceremony)",
    Universe.STORY_ENGINE: "Miette (Story Engine)",
}

UNIVERSE_KEYWORDS: Dict[Universe, List[str]] = {
    Universe.ENGINEER: [
        "build", "implement", "deploy", "code", "architecture", "pattern",
        "package", "module", "test", "dependency", "api", "schema",
        "performance", "scale", "infrastructure", "debug", "refactor",
    ],
    Universe.CEREMONY: [
        "ceremony", "protocol", "relational", "accountability", "indigenous",
        "medicine", "wheel", "consent", "elder", "community", "land",
        "dream", "vision", "spiritual", "emotional", "respect", "reciprocity",
        "ocap", "governance", "sovereign",
    ],
    Universe.STORY_ENGINE: [
        "narrative", "story", "beat", "arc", "character", "theme",
        "tension", "resolution", "climax", "meaning", "emotional",
        "journey", "transformation", "coherence", "voice", "episode",
    ],
}


@dataclass
class PerspectiveInsight:
    universe: Universe
    observation: str
    relevant_actions: List[str]
    confidence: float
    flags: List[str]


@dataclass
class ThreeUniversePerspective:
    id: str
    timestamp: str
    decomposition_id: str
    insights: List[PerspectiveInsight]
    lead_universe: Universe
    coherence: float
    synthesis: str


class PerspectiveAnalyzer:
    """Analyzes decompositions through three universe lenses."""

    def analyze(self, decomposition: DecompositionResult) -> ThreeUniversePerspective:
        perspective_id = str(uuid.uuid4())
        insights = [
            self._analyze_from_universe(u, decomposition)
            for u in Universe
        ]

        sorted_insights = sorted(insights, key=lambda i: i.confidence, reverse=True)
        lead_universe = sorted_insights[0].universe
        coherence = self._calculate_coherence(insights, decomposition)
        synthesis = self._synthesize(insights, decomposition)

        return ThreeUniversePerspective(
            id=perspective_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            decomposition_id=decomposition.id,
            insights=insights,
            lead_universe=lead_universe,
            coherence=coherence,
            synthesis=synthesis,
        )

    def _analyze_from_universe(
        self, universe: Universe, decomposition: DecompositionResult
    ) -> PerspectiveInsight:
        keywords = UNIVERSE_KEYWORDS[universe]
        prompt_lower = decomposition.prompt.lower()
        flags: List[str] = []
        relevant_actions: List[str] = []

        keyword_hits = sum(1 for kw in keywords if kw in prompt_lower)
        confidence = min(keyword_hits / 5.0, 1.0)

        for action in decomposition.action_stack:
            action_lower = action.text.lower()
            if any(kw in action_lower for kw in keywords):
                relevant_actions.append(action.id)

        if universe == Universe.ENGINEER:
            has_tests = any(a.direction == Direction.WEST for a in decomposition.action_stack)
            has_deps = any(s.dependency is not None for s in decomposition.secondary)
            observation = (
                f"Technical scope: {len(decomposition.action_stack)} actions, "
                f"{'with' if has_deps else 'no'} dependency chain."
            )
            if not has_tests:
                flags.append("No validation/test actions detected")
            if decomposition.balance < 0.3:
                flags.append("Unbalanced — may need architectural review")

        elif universe == Universe.CEREMONY:
            has_west = len(decomposition.directions.get("west", [])) > 0
            has_east = len(decomposition.directions.get("east", [])) > 0
            observation = (
                f"Relational coverage: EAST(vision)={len(decomposition.directions.get('east', []))}, "
                f"WEST(ceremony)={len(decomposition.directions.get('west', []))} insights."
            )
            if not has_west:
                flags.append("⚠️ No ceremonial/reflective dimension — pause recommended")
            if not has_east:
                flags.append("Vision unclear — who does this serve?")
            if "indigenous" in prompt_lower and not has_west:
                flags.append("🛑 Indigenous domain work without ceremony context")

        else:  # STORY_ENGINE
            has_arc = len(decomposition.action_stack) > 3
            observation = (
                f"Narrative shape: {len(decomposition.action_stack)}-step journey, "
                f"{decomposition.lead_direction.value} led."
            )
            if not has_arc:
                flags.append("Very short arc — may lack narrative depth")
            if len(decomposition.neglected_directions) > 1:
                flags.append(
                    f"Neglected perspectives: {', '.join(d.value for d in decomposition.neglected_directions)}"
                )

        return PerspectiveInsight(
            universe=universe,
            observation=observation,
            relevant_actions=relevant_actions,
            confidence=confidence,
            flags=flags,
        )

    def _calculate_coherence(
        self, insights: List[PerspectiveInsight], decomposition: DecompositionResult
    ) -> float:
        all_flags = [f for i in insights for f in i.flags]
        unique_flags = len(set(all_flags))
        flag_coherence = 1.0 if unique_flags == 0 else max(0.0, 1.0 - unique_flags / 10.0)
        return flag_coherence * 0.6 + decomposition.balance * 0.4

    def _synthesize(
        self, insights: List[PerspectiveInsight], decomposition: DecompositionResult
    ) -> str:
        flags = [f for i in insights for f in i.flags]
        if any("🛑" in f for f in flags):
            return "HOLD: Critical flags raised — ceremony or protocol review required before proceeding."
        if any("⚠️" in f for f in flags):
            warnings = sum(1 for f in flags if "⚠️" in f)
            return f"CAUTION: {warnings} warning(s) raised. Consider addressing before execution."
        if decomposition.balance > 0.5:
            return "PROCEED: Well-balanced decomposition across all perspectives."
        return f"REVIEW: Decomposition is {decomposition.lead_direction.value}-heavy. Consider broadening perspective."
