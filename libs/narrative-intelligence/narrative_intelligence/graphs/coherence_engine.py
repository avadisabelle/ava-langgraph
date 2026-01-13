"""
🧠 Narrative Coherence Engine

A LangGraph graph that analyzes narrative coherence and identifies gaps.
This is a core dependency for the Editor Anvil app.

Features:
- Gap identification (structural, thematic, character, sensory, continuity)
- Coherence scoring across multiple dimensions
- Enrichment routing suggestions
- Trinity perspective integration (Mia/Miette/Ava8)
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Literal
from enum import Enum
from datetime import datetime, timezone
from langgraph.graph import StateGraph, END

from ..schemas.unified_state_bridge import (
    StoryBeat,
    CharacterState,
    ThematicThread,
    Universe,
    UniversePerspective,
)


class GapType(Enum):
    """Types of narrative gaps that can be identified."""
    STRUCTURAL = "structural"      # Missing beats, incomplete arcs
    THEMATIC = "thematic"          # Promised themes underdelivered
    CHARACTER = "character"        # Traits mentioned but not demonstrated
    SENSORY = "sensory"           # Scenes lacking grounding detail
    CONTINUITY = "continuity"     # Timeline/detail inconsistencies


class GapSeverity(Enum):
    """Severity levels for identified gaps."""
    CRITICAL = "critical"   # Must fix before publication
    MODERATE = "moderate"   # Should address in next pass
    MINOR = "minor"        # Nice to have, low priority


class RoutingTarget(Enum):
    """Where to route gaps for remediation."""
    STORYTELLER = "storyteller"   # Needs prose refinement
    STRUCTURIST = "structurist"   # Needs structural repair
    ARCHITECT = "architect"       # Schema inconsistency
    AUTHOR = "author"            # Human decision required


@dataclass
class Gap:
    """A narrative gap identified in the story."""
    id: str
    gap_type: GapType
    severity: GapSeverity
    description: str
    location: Dict[str, Any]  # beat_id, chapter_id, position
    suggested_route: RoutingTarget
    resolved: bool = False
    resolution: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "type": self.gap_type.value,
            "severity": self.severity.value,
            "description": self.description,
            "location": self.location,
            "suggested_route": self.suggested_route.value,
            "resolved": self.resolved,
            "resolution": self.resolution,
        }


@dataclass
class ComponentScore:
    """Score for a single coherence component."""
    score: float  # 0-100
    status: Literal["good", "warning", "critical"]
    issues: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "score": self.score,
            "status": self.status,
            "issues": self.issues,
            "suggestions": self.suggestions,
        }


@dataclass
class CoherenceScore:
    """Complete coherence score for a narrative."""
    overall: float
    narrative_flow: ComponentScore
    character_consistency: ComponentScore
    pacing: ComponentScore
    theme_saturation: ComponentScore
    continuity: ComponentScore
    analyzed_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "overall": self.overall,
            "components": {
                "narrative_flow": self.narrative_flow.to_dict(),
                "character_consistency": self.character_consistency.to_dict(),
                "pacing": self.pacing.to_dict(),
                "theme_saturation": self.theme_saturation.to_dict(),
                "continuity": self.continuity.to_dict(),
            },
            "analyzed_at": self.analyzed_at,
        }


@dataclass
class TrinityAssessment:
    """Assessment from three narrative perspectives (Mia/Miette/Ava8)."""
    mia: str      # Structural quality (🧠 logical, analytical)
    miette: str   # Emotional effectiveness (🌸 feeling, resonance)
    ava8: str     # Atmospheric/sensory (🎨 visual, immersive)
    priorities: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "mia": self.mia,
            "miette": self.miette,
            "ava8": self.ava8,
            "priorities": self.priorities,
        }


# Type alias for the coherence engine state
CoherenceEngineState = Dict[str, Any]


class NarrativeCoherenceEngine:
    """
    Analyzes narrative coherence and identifies gaps.
    
    This is a core component for the Editor Anvil app, providing:
    - Comprehensive coherence scoring across 5 dimensions
    - Gap identification with severity and routing
    - Trinity perspective assessment (Mia/Miette/Ava8)
    - Actionable improvement suggestions
    
    Usage:
        engine = NarrativeCoherenceEngine()
        result = engine.analyze(beats, characters, themes)
        
        # Access scores
        print(f"Overall coherence: {result.coherence_score.overall}")
        
        # Access gaps
        for gap in result.gaps:
            print(f"Gap: {gap.description} ({gap.severity.value})")
        
        # Access Trinity assessment
        print(f"Mia says: {result.trinity_assessment.mia}")
    """
    
    def __init__(self, strict_mode: bool = False):
        """
        Initialize the Narrative Coherence Engine.
        
        Args:
            strict_mode: If True, apply stricter scoring thresholds
        """
        self.strict_mode = strict_mode
        self._gap_counter = 0
    
    def _generate_gap_id(self) -> str:
        """Generate a unique gap ID."""
        self._gap_counter += 1
        return f"gap_{self._gap_counter}"
    
    def _analyze_narrative_flow(
        self,
        state: CoherenceEngineState
    ) -> CoherenceEngineState:
        """
        Analyze narrative flow - how smoothly the story progresses.
        
        Checks:
        - Beat transitions (jarring vs smooth)
        - Logical causality between beats
        - Pacing consistency
        """
        beats: List[StoryBeat] = state.get("beats", [])
        issues = []
        suggestions = []
        
        if len(beats) < 2:
            score = 50.0
            issues.append("Too few beats to assess flow")
            suggestions.append("Add more story beats to establish narrative rhythm")
        else:
            # Check for logical function progression
            functions = [b.narrative_function.value for b in beats]
            
            # Penalize if no setup before confrontation
            has_proper_structure = False
            for i, func in enumerate(functions):
                if func in ["setup", "introduction", "discovery"]:
                    has_proper_structure = True
                    break
                elif func in ["confrontation", "crisis", "climax"]:
                    if not has_proper_structure:
                        issues.append(f"Beat {i+1} escalates without proper setup")
                        has_proper_structure = True  # Only report once
            
            # Check emotional continuity
            prev_tone = None
            jarring_transitions = 0
            for i, beat in enumerate(beats):
                if prev_tone and beat.emotional_tone:
                    # Simple check: devastation followed by joy is jarring
                    jarring_pairs = [
                        ("devastating", "joyful"),
                        ("fearful", "peaceful"),
                        ("triumphant", "devastating"),
                    ]
                    for p1, p2 in jarring_pairs:
                        if (p1 in prev_tone.lower() and p2 in beat.emotional_tone.lower()) or \
                           (p2 in prev_tone.lower() and p1 in beat.emotional_tone.lower()):
                            jarring_transitions += 1
                            issues.append(f"Jarring emotional transition at Beat {i+1}")
                prev_tone = beat.emotional_tone
            
            # Calculate score
            base_score = 85.0
            base_score -= jarring_transitions * 10
            base_score -= len([i for i in issues if "without proper setup" in i]) * 15
            
            score = max(0.0, min(100.0, base_score))
            
            if jarring_transitions > 0:
                suggestions.append("Add transitional beats to smooth emotional shifts")
            if not has_proper_structure:
                suggestions.append("Consider adding setup beats before major confrontations")
        
        # Determine status
        if score >= 70:
            status = "good"
        elif score >= 50:
            status = "warning"
        else:
            status = "critical"
        
        state["narrative_flow_score"] = ComponentScore(
            score=score,
            status=status,
            issues=issues,
            suggestions=suggestions
        )
        
        return state
    
    def _analyze_character_consistency(
        self,
        state: CoherenceEngineState
    ) -> CoherenceEngineState:
        """
        Analyze character consistency across the narrative.
        
        Checks:
        - Character voice consistency
        - Arc progression logic
        - Relationship evolution coherence
        """
        beats: List[StoryBeat] = state.get("beats", [])
        characters: List[CharacterState] = state.get("characters", [])
        issues = []
        suggestions = []
        
        if not characters:
            score = 50.0
            issues.append("No character data provided")
            suggestions.append("Define character states to enable consistency analysis")
        else:
            # Track character appearances across beats
            character_beats: Dict[str, List[int]] = {c.id: [] for c in characters}
            
            for i, beat in enumerate(beats):
                if hasattr(beat, 'characters') and beat.characters:
                    for char_id in beat.characters:
                        if char_id in character_beats:
                            character_beats[char_id].append(i)
            
            # Check for characters with large gaps
            for char_id, appearances in character_beats.items():
                if len(appearances) >= 2:
                    for i in range(1, len(appearances)):
                        gap = appearances[i] - appearances[i-1]
                        if gap > 5:  # More than 5 beats between appearances
                            char = next((c for c in characters if c.id == char_id), None)
                            name = char.name if char else char_id
                            issues.append(f"Character '{name}' disappears for {gap} beats")
                            suggestions.append(f"Consider adding '{name}' to beats between {appearances[i-1]+1} and {appearances[i]+1}")
            
            # Check arc progression
            for char in characters:
                if hasattr(char, 'arc_position'):
                    if char.arc_position < 0.1 and len(beats) > 5:
                        issues.append(f"Character '{char.name}' has minimal arc progression")
            
            # Calculate score based on issues
            base_score = 90.0
            base_score -= len([i for i in issues if "disappears" in i]) * 8
            base_score -= len([i for i in issues if "minimal arc" in i]) * 12
            
            score = max(0.0, min(100.0, base_score))
        
        # Determine status
        if score >= 70:
            status = "good"
        elif score >= 50:
            status = "warning"
        else:
            status = "critical"
        
        state["character_consistency_score"] = ComponentScore(
            score=score,
            status=status,
            issues=issues,
            suggestions=suggestions
        )
        
        return state
    
    def _analyze_pacing(
        self,
        state: CoherenceEngineState
    ) -> CoherenceEngineState:
        """
        Analyze narrative pacing.
        
        Checks:
        - Tension/relief distribution
        - Beat density per section
        - Climax positioning
        """
        beats: List[StoryBeat] = state.get("beats", [])
        issues = []
        suggestions = []
        
        if len(beats) < 3:
            score = 50.0
            issues.append("Too few beats to assess pacing")
            suggestions.append("Add more beats to establish proper pacing rhythm")
        else:
            # Analyze function distribution
            functions = [b.narrative_function.value for b in beats]
            
            # Check for climax positioning (should be in last third)
            climax_positions = [i for i, f in enumerate(functions) if "climax" in f.lower()]
            
            if not climax_positions:
                issues.append("No climax beat identified")
                suggestions.append("Ensure at least one beat has a climax function")
            else:
                # Check if climax is too early
                last_climax = climax_positions[-1]
                total = len(beats)
                if last_climax < total * 0.5:
                    issues.append("Climax occurs too early in the narrative")
                    suggestions.append("Move climax to later in the story or add post-climax resolution beats")
            
            # Check for consecutive high-tension beats
            high_tension_funcs = ["confrontation", "crisis", "climax", "revelation"]
            consecutive_high = 0
            max_consecutive = 0
            
            for func in functions:
                if any(ht in func.lower() for ht in high_tension_funcs):
                    consecutive_high += 1
                    max_consecutive = max(max_consecutive, consecutive_high)
                else:
                    consecutive_high = 0
            
            if max_consecutive > 3:
                issues.append(f"Found {max_consecutive} consecutive high-tension beats")
                suggestions.append("Add breathing room with quieter beats between intense moments")
            
            # Calculate score
            base_score = 85.0
            if not climax_positions:
                base_score -= 20
            elif climax_positions[-1] < len(beats) * 0.5:
                base_score -= 15
            base_score -= min(20, max_consecutive * 5)
            
            score = max(0.0, min(100.0, base_score))
        
        # Determine status
        if score >= 70:
            status = "good"
        elif score >= 50:
            status = "warning"
        else:
            status = "critical"
        
        state["pacing_score"] = ComponentScore(
            score=score,
            status=status,
            issues=issues,
            suggestions=suggestions
        )
        
        return state
    
    def _analyze_theme_saturation(
        self,
        state: CoherenceEngineState
    ) -> CoherenceEngineState:
        """
        Analyze how well themes permeate the narrative.
        
        Checks:
        - Theme presence across beats
        - Theme introduction and payoff
        - Theme strength consistency
        """
        beats: List[StoryBeat] = state.get("beats", [])
        themes: List[ThematicThread] = state.get("themes", [])
        issues = []
        suggestions = []
        
        if not themes:
            score = 50.0
            issues.append("No themes defined")
            suggestions.append("Define thematic threads to enable saturation analysis")
        else:
            # Track theme presence
            theme_coverage: Dict[str, float] = {}
            
            for theme in themes:
                # Calculate theme presence across beats
                beats_with_theme = 0
                for beat in beats:
                    if hasattr(beat, 'themes') and beat.themes:
                        if theme.id in beat.themes:
                            beats_with_theme += 1
                
                coverage = beats_with_theme / max(len(beats), 1)
                theme_coverage[theme.name] = coverage
                
                # Check for underdeveloped themes
                if coverage < 0.2 and theme.strength > 0.5:
                    issues.append(f"Theme '{theme.name}' is important but appears rarely")
                    suggestions.append(f"Weave '{theme.name}' into more beats to fulfill its promise")
                
                # Check for theme that appears but never pays off
                if coverage > 0.3 and theme.strength < 0.3:
                    issues.append(f"Theme '{theme.name}' appears often but lacks impact")
                    suggestions.append(f"Strengthen the thematic weight of '{theme.name}' in key beats")
            
            # Calculate average coverage
            avg_coverage = sum(theme_coverage.values()) / max(len(theme_coverage), 1)
            
            # Score based on coverage and issues
            base_score = min(100.0, avg_coverage * 100 + 20)  # Base on coverage + buffer
            base_score -= len([i for i in issues if "rarely" in i]) * 10
            base_score -= len([i for i in issues if "lacks impact" in i]) * 8
            
            score = max(0.0, min(100.0, base_score))
        
        # Determine status
        if score >= 70:
            status = "good"
        elif score >= 50:
            status = "warning"
        else:
            status = "critical"
        
        state["theme_saturation_score"] = ComponentScore(
            score=score,
            status=status,
            issues=issues,
            suggestions=suggestions
        )
        
        return state
    
    def _analyze_continuity(
        self,
        state: CoherenceEngineState
    ) -> CoherenceEngineState:
        """
        Analyze narrative continuity.
        
        Checks:
        - Timeline consistency
        - Detail consistency across beats
        - Setting/location coherence
        """
        beats: List[StoryBeat] = state.get("beats", [])
        issues = []
        suggestions = []
        
        if len(beats) < 2:
            score = 70.0  # Default to passing if not enough to analyze
            issues.append("Too few beats for continuity analysis")
        else:
            # Check sequence ordering
            sequences = [b.sequence for b in beats]
            if sequences != sorted(sequences):
                issues.append("Beat sequences are not in order")
                suggestions.append("Reorder beats to ensure logical sequence progression")
            
            # Check for duplicate sequences
            if len(sequences) != len(set(sequences)):
                issues.append("Duplicate beat sequence numbers found")
                suggestions.append("Ensure each beat has a unique sequence number")
            
            # Check for gaps in sequence
            expected = set(range(1, max(sequences) + 1))
            actual = set(sequences)
            missing = expected - actual
            if missing and len(missing) <= 3:  # Small gaps are issues
                issues.append(f"Missing beat sequences: {sorted(missing)}")
                suggestions.append("Fill in missing beat sequences or renumber")
            
            # Check episode consistency
            episodes = [b.episode_id for b in beats if hasattr(b, 'episode_id') and b.episode_id]
            if episodes:
                unique_episodes = list(dict.fromkeys(episodes))  # Preserve order
                # Check if episodes jump around
                episode_changes = 0
                prev_ep = None
                for ep in episodes:
                    if prev_ep and ep != prev_ep:
                        episode_changes += 1
                    prev_ep = ep
                
                if episode_changes > len(unique_episodes):
                    issues.append("Episode assignments jump around inconsistently")
                    suggestions.append("Group beats by episode more cleanly")
            
            # Calculate score
            base_score = 90.0
            base_score -= len([i for i in issues if "not in order" in i]) * 20
            base_score -= len([i for i in issues if "Duplicate" in i]) * 15
            base_score -= len([i for i in issues if "Missing" in i]) * 5
            base_score -= len([i for i in issues if "jump around" in i]) * 10
            
            score = max(0.0, min(100.0, base_score))
        
        # Determine status
        if score >= 70:
            status = "good"
        elif score >= 50:
            status = "warning"
        else:
            status = "critical"
        
        state["continuity_score"] = ComponentScore(
            score=score,
            status=status,
            issues=issues,
            suggestions=suggestions
        )
        
        return state
    
    def _calculate_overall_score(
        self,
        state: CoherenceEngineState
    ) -> CoherenceEngineState:
        """Calculate the overall coherence score from components."""
        components = [
            state.get("narrative_flow_score"),
            state.get("character_consistency_score"),
            state.get("pacing_score"),
            state.get("theme_saturation_score"),
            state.get("continuity_score"),
        ]
        
        valid_scores = [c.score for c in components if c is not None]
        
        if valid_scores:
            # Weighted average (narrative flow and character consistency weighted higher)
            weights = [1.2, 1.2, 1.0, 1.0, 0.8]  # Matches component order
            weighted_sum = sum(s * w for s, w in zip(valid_scores, weights))
            total_weight = sum(weights[:len(valid_scores)])
            overall = weighted_sum / total_weight
        else:
            overall = 50.0
        
        state["overall_score"] = overall
        
        return state
    
    def _identify_gaps(
        self,
        state: CoherenceEngineState
    ) -> CoherenceEngineState:
        """
        Identify narrative gaps from component analyses.
        
        Creates Gap objects with severity and routing suggestions.
        """
        gaps: List[Gap] = []
        
        # Extract issues from each component
        component_mappings = [
            ("narrative_flow_score", GapType.STRUCTURAL),
            ("character_consistency_score", GapType.CHARACTER),
            ("pacing_score", GapType.STRUCTURAL),
            ("theme_saturation_score", GapType.THEMATIC),
            ("continuity_score", GapType.CONTINUITY),
        ]
        
        for component_key, gap_type in component_mappings:
            component = state.get(component_key)
            if component and component.issues:
                for issue in component.issues:
                    # Determine severity
                    if component.status == "critical":
                        severity = GapSeverity.CRITICAL
                    elif "rarely" in issue or "disappears" in issue:
                        severity = GapSeverity.MODERATE
                    else:
                        severity = GapSeverity.MINOR
                    
                    # Determine routing
                    if gap_type == GapType.STRUCTURAL:
                        route = RoutingTarget.STRUCTURIST
                    elif gap_type == GapType.CHARACTER:
                        route = RoutingTarget.STORYTELLER
                    elif gap_type == GapType.THEMATIC:
                        route = RoutingTarget.STRUCTURIST
                    elif gap_type == GapType.SENSORY:
                        route = RoutingTarget.STORYTELLER
                    else:  # CONTINUITY
                        route = RoutingTarget.AUTHOR
                    
                    gaps.append(Gap(
                        id=self._generate_gap_id(),
                        gap_type=gap_type,
                        severity=severity,
                        description=issue,
                        location={"component": component_key},
                        suggested_route=route,
                    ))
        
        # Sort by severity (critical first)
        severity_order = {GapSeverity.CRITICAL: 0, GapSeverity.MODERATE: 1, GapSeverity.MINOR: 2}
        gaps.sort(key=lambda g: severity_order[g.severity])
        
        state["gaps"] = gaps
        
        return state
    
    def _generate_trinity_assessment(
        self,
        state: CoherenceEngineState
    ) -> CoherenceEngineState:
        """
        Generate Trinity perspective assessment (Mia/Miette/Ava8).
        
        Each persona provides feedback aligned with their perspective:
        - Mia 🧠: Structural/logical analysis
        - Miette 🌸: Emotional/resonance analysis
        - Ava8 🎨: Atmospheric/sensory analysis
        """
        overall = state.get("overall_score", 50.0)
        gaps = state.get("gaps", [])
        
        # Component scores
        flow = state.get("narrative_flow_score")
        character = state.get("character_consistency_score")
        pacing = state.get("pacing_score")
        theme = state.get("theme_saturation_score")
        continuity = state.get("continuity_score")
        
        # Build Mia's assessment (structural)
        mia_parts = []
        if flow:
            mia_parts.append(f"Structure is {flow.score:.0f}% sound.")
            if flow.issues:
                mia_parts.append(f"Key structural gap: {flow.issues[0]}")
        if pacing:
            if pacing.score < 70:
                mia_parts.append(f"Pacing needs attention ({pacing.score:.0f}%).")
                if pacing.suggestions:
                    mia_parts.append(pacing.suggestions[0])
        if continuity:
            if continuity.score < 80:
                mia_parts.append(f"Continuity has {len(continuity.issues)} issues to address.")
        
        mia = " ".join(mia_parts) if mia_parts else "Structure analysis unavailable."
        
        # Build Miette's assessment (emotional)
        miette_parts = []
        if character:
            if character.score >= 80:
                miette_parts.append("Character arcs are resonating well.")
            else:
                miette_parts.append(f"Character consistency is {character.score:.0f}%.")
                if character.issues:
                    miette_parts.append(f"The emotional gap: {character.issues[0]}")
        if theme:
            if theme.score >= 70:
                miette_parts.append("Themes are landing with emotional weight.")
            else:
                miette_parts.append("Themes need stronger emotional anchoring.")
        if flow and flow.issues:
            jarring = [i for i in flow.issues if "Jarring" in i]
            if jarring:
                miette_parts.append("Emotional transitions feel abrupt in places.")
        
        miette = " ".join(miette_parts) if miette_parts else "Emotional analysis unavailable."
        
        # Build Ava8's assessment (atmospheric)
        ava8_parts = []
        sensory_gaps = [g for g in gaps if g.gap_type == GapType.SENSORY]
        if sensory_gaps:
            ava8_parts.append(f"Found {len(sensory_gaps)} sensory gaps to address.")
        
        if pacing and pacing.score >= 70:
            ava8_parts.append("Atmospheric rhythm feels balanced.")
        else:
            ava8_parts.append("Atmosphere could use more grounding moments.")
        
        # Check for consecutive high-tension (affects atmosphere)
        if pacing and any("consecutive high-tension" in i for i in pacing.issues):
            ava8_parts.append("The dense tension sections may benefit from visual breathing room.")
        
        ava8 = " ".join(ava8_parts) if ava8_parts else "Atmospheric analysis unavailable."
        
        # Determine priorities
        priorities = []
        critical_gaps = [g for g in gaps if g.severity == GapSeverity.CRITICAL]
        if critical_gaps:
            priorities.extend([g.description for g in critical_gaps[:3]])
        else:
            moderate_gaps = [g for g in gaps if g.severity == GapSeverity.MODERATE]
            if moderate_gaps:
                priorities.extend([g.description for g in moderate_gaps[:3]])
        
        if not priorities:
            priorities.append("Minor polish items only - narrative is coherent")
        
        state["trinity_assessment"] = TrinityAssessment(
            mia=mia,
            miette=miette,
            ava8=ava8,
            priorities=priorities
        )
        
        return state
    
    def _build_coherence_result(
        self,
        state: CoherenceEngineState
    ) -> CoherenceEngineState:
        """Build the final coherence result object."""
        state["coherence_score"] = CoherenceScore(
            overall=state.get("overall_score", 50.0),
            narrative_flow=state.get("narrative_flow_score", ComponentScore(50, "warning")),
            character_consistency=state.get("character_consistency_score", ComponentScore(50, "warning")),
            pacing=state.get("pacing_score", ComponentScore(50, "warning")),
            theme_saturation=state.get("theme_saturation_score", ComponentScore(50, "warning")),
            continuity=state.get("continuity_score", ComponentScore(50, "warning")),
        )
        
        return state
    
    def build_graph(self) -> StateGraph:
        """
        Build the LangGraph workflow for coherence analysis.
        
        Flow:
        1. Analyze narrative flow
        2. Analyze character consistency
        3. Analyze pacing
        4. Analyze theme saturation
        5. Analyze continuity
        6. Calculate overall score
        7. Identify gaps
        8. Generate Trinity assessment
        9. Build final result
        
        Returns:
            Compiled StateGraph
        """
        workflow = StateGraph(CoherenceEngineState)
        
        # Add nodes
        workflow.add_node("analyze_flow", self._analyze_narrative_flow)
        workflow.add_node("analyze_character", self._analyze_character_consistency)
        workflow.add_node("analyze_pacing", self._analyze_pacing)
        workflow.add_node("analyze_theme", self._analyze_theme_saturation)
        workflow.add_node("analyze_continuity", self._analyze_continuity)
        workflow.add_node("calculate_overall", self._calculate_overall_score)
        workflow.add_node("identify_gaps", self._identify_gaps)
        workflow.add_node("trinity_assessment", self._generate_trinity_assessment)
        workflow.add_node("build_result", self._build_coherence_result)
        
        # Define edges (sequential analysis)
        workflow.set_entry_point("analyze_flow")
        workflow.add_edge("analyze_flow", "analyze_character")
        workflow.add_edge("analyze_character", "analyze_pacing")
        workflow.add_edge("analyze_pacing", "analyze_theme")
        workflow.add_edge("analyze_theme", "analyze_continuity")
        workflow.add_edge("analyze_continuity", "calculate_overall")
        workflow.add_edge("calculate_overall", "identify_gaps")
        workflow.add_edge("identify_gaps", "trinity_assessment")
        workflow.add_edge("trinity_assessment", "build_result")
        workflow.add_edge("build_result", END)
        
        return workflow.compile()
    
    def analyze(
        self,
        beats: List[StoryBeat],
        characters: Optional[List[CharacterState]] = None,
        themes: Optional[List[ThematicThread]] = None,
        include_metadata: bool = False
    ) -> Dict[str, Any]:
        """
        Analyze narrative coherence.
        
        Args:
            beats: List of story beats to analyze
            characters: Optional list of character states
            themes: Optional list of thematic threads
            include_metadata: Whether to include full analysis state
        
        Returns:
            Dictionary with coherence_score, gaps, and trinity_assessment
        """
        # Initialize state
        initial_state: CoherenceEngineState = {
            "beats": beats,
            "characters": characters or [],
            "themes": themes or [],
        }
        
        # Build and run graph
        graph = self.build_graph()
        result = graph.invoke(initial_state)
        
        if include_metadata:
            return result
        else:
            return {
                "coherence_score": result.get("coherence_score"),
                "gaps": result.get("gaps", []),
                "trinity_assessment": result.get("trinity_assessment"),
            }
    
    def get_routing_suggestions(
        self,
        gaps: List[Gap]
    ) -> Dict[str, List[Gap]]:
        """
        Group gaps by their routing target.
        
        Args:
            gaps: List of identified gaps
        
        Returns:
            Dictionary mapping routing target to list of gaps
        """
        routing: Dict[str, List[Gap]] = {target.value: [] for target in RoutingTarget}
        
        for gap in gaps:
            routing[gap.suggested_route.value].append(gap)
        
        return routing
