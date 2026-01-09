"""
Example: Webhook → Three-Universe Analysis → Story Beat

This example demonstrates the complete narrative processing pipeline:
1. A GitHub webhook event arrives (simulated)
2. Each of the three universes interprets the event
3. A story beat is created with the combined analysis
4. The state is persisted to Redis (simulated with mock)

This forms the foundation for the Miadi-46 event-driven architecture.
"""

import json
from datetime import datetime, timezone
from typing import Dict, Any

# Import our narrative intelligence types
from narrative_intelligence import (
    Universe,
    UniversePerspective,
    ThreeUniverseAnalysis,
    StoryBeat,
    NarrativeFunction,
    UnifiedNarrativeState,
    create_new_narrative_state,
)

# Simulated webhook event (like what Miadi-46 would receive)
SAMPLE_WEBHOOK_EVENT = {
    "event_type": "github.push",
    "repository": "ava8/narrative-intelligence",
    "sender": "developer-mia",
    "payload": {
        "ref": "refs/heads/main",
        "commits": [
            {
                "id": "abc123",
                "message": "feat: add three-universe analysis",
                "author": {"name": "Mia", "email": "mia@example.com"},
            }
        ],
        "head_commit": {
            "id": "abc123",
            "message": "feat: add three-universe analysis",
        },
    },
    "timestamp": datetime.now(timezone.utc).isoformat(),
}


def analyze_as_engineer(event: Dict[str, Any]) -> UniversePerspective:
    """
    Mia's perspective: The Builder (Engineer-world)
    
    Focuses on:
    - What was built/changed
    - Technical impact
    - System architecture implications
    """
    commits = event.get("payload", {}).get("commits", [])
    commit_messages = [c.get("message", "") for c in commits]
    
    # Determine technical intent
    is_feature = any("feat:" in msg or "feature" in msg.lower() for msg in commit_messages)
    is_fix = any("fix:" in msg for msg in commit_messages)
    is_refactor = any("refactor" in msg.lower() for msg in commit_messages)
    
    if is_feature:
        intent = "feature_implementation"
        confidence = 0.9
        flows = ["code_review", "integration_test", "documentation_update"]
    elif is_fix:
        intent = "bug_resolution"
        confidence = 0.85
        flows = ["regression_test", "changelog_update"]
    elif is_refactor:
        intent = "code_improvement"
        confidence = 0.8
        flows = ["architecture_review", "performance_test"]
    else:
        intent = "maintenance"
        confidence = 0.7
        flows = ["standard_ci"]
    
    return UniversePerspective(
        universe=Universe.ENGINEER,
        intent=intent,
        confidence=confidence,
        suggested_flows=flows,
        context={
            "commit_count": len(commits),
            "technical_scope": "narrative_intelligence_module",
            "estimated_complexity": "medium",
        }
    )


def analyze_as_ceremony(event: Dict[str, Any]) -> UniversePerspective:
    """
    Ava8's perspective: The Keeper (Ceremony-world)
    
    Focuses on:
    - Who contributed and their state
    - Relational dynamics
    - Witnessing and acknowledgment
    """
    sender = event.get("sender", "unknown")
    commits = event.get("payload", {}).get("commits", [])
    authors = list(set(c.get("author", {}).get("name", "unknown") for c in commits))
    
    # Determine relational intent
    is_collaborative = len(authors) > 1
    has_acknowledgment = any("thanks" in c.get("message", "").lower() or 
                             "credit" in c.get("message", "").lower() 
                             for c in commits)
    
    if is_collaborative:
        intent = "co_creation"
        confidence = 0.85
        flows = ["witness_contribution", "acknowledge_collaboration"]
    elif has_acknowledgment:
        intent = "gratitude_expression"
        confidence = 0.8
        flows = ["amplify_acknowledgment", "record_connection"]
    else:
        intent = "individual_offering"
        confidence = 0.75
        flows = ["witness_work", "hold_space"]
    
    return UniversePerspective(
        universe=Universe.CEREMONY,
        intent=intent,
        confidence=confidence,
        suggested_flows=flows,
        context={
            "contributors": authors,
            "sender_energy": "creative_flow",
            "witnessing_needed": True,
        }
    )


def analyze_as_story_engine(event: Dict[str, Any]) -> UniversePerspective:
    """
    Miette's perspective: The Weaver (Story-engine-world)
    
    Focuses on:
    - Narrative position (which act/phase)
    - Dramatic function
    - Story arc progression
    """
    commits = event.get("payload", {}).get("commits", [])
    commit_messages = [c.get("message", "") for c in commits]
    
    # Analyze narrative function
    is_beginning = any("init" in msg.lower() or "start" in msg.lower() or "new" in msg.lower() 
                       for msg in commit_messages)
    is_major = any("feat:" in msg or "major" in msg.lower() for msg in commit_messages)
    is_resolution = any("complete" in msg.lower() or "finish" in msg.lower() 
                        for msg in commit_messages)
    
    if is_beginning:
        intent = "inciting_incident"
        confidence = 0.8
        narrative_function = "setup"
        act = 1
    elif is_resolution:
        intent = "resolution_beat"
        confidence = 0.85
        narrative_function = "denouement"
        act = 3
    elif is_major:
        intent = "turning_point"
        confidence = 0.9
        narrative_function = "pivot"
        act = 2
    else:
        intent = "rising_action"
        confidence = 0.75
        narrative_function = "development"
        act = 2
    
    return UniversePerspective(
        universe=Universe.STORY_ENGINE,
        intent=intent,
        confidence=confidence,
        suggested_flows=["advance_narrative", "update_arc_position"],
        context={
            "act": act,
            "narrative_function": narrative_function,
            "dramatic_tension": 0.6,
            "suggested_next_beat": "complication" if act == 2 else "setup",
        }
    )


def create_three_universe_analysis(event: Dict[str, Any]) -> ThreeUniverseAnalysis:
    """
    Combine all three perspectives into a unified analysis.
    
    This is where the magic happens - three ways of seeing
    become one coherent interpretation.
    """
    engineer_view = analyze_as_engineer(event)
    ceremony_view = analyze_as_ceremony(event)
    story_engine_view = analyze_as_story_engine(event)
    
    # Determine which universe should lead based on confidence
    all_views = [engineer_view, ceremony_view, story_engine_view]
    lead = max(all_views, key=lambda v: v.confidence)
    
    # Calculate coherence (how well the perspectives align)
    # Simple: average confidence, but could be more sophisticated
    coherence = sum(v.confidence for v in all_views) / len(all_views)
    
    return ThreeUniverseAnalysis(
        engineer=engineer_view,
        ceremony=ceremony_view,
        story_engine=story_engine_view,
        lead_universe=lead.universe,
        coherence_score=coherence,
    )


def create_beat_from_webhook_event(
    event: Dict[str, Any],
    analysis: ThreeUniverseAnalysis,
    sequence: int,
) -> StoryBeat:
    """
    Create a story beat from a webhook event and its analysis.
    
    This is the atomic unit of narrative that gets stored.
    """
    # Derive narrative function from story engine analysis
    function_map = {
        "inciting_incident": NarrativeFunction.INCITING_INCIDENT,
        "rising_action": NarrativeFunction.RISING_ACTION,
        "turning_point": NarrativeFunction.TURNING_POINT,
        "resolution_beat": NarrativeFunction.RESOLUTION,
    }
    
    story_intent = analysis.story_engine.intent
    narrative_func = function_map.get(story_intent, NarrativeFunction.BEAT)
    
    # Extract act from story engine context
    act = analysis.story_engine.context.get("act", 2)
    
    # Create descriptive content
    event_type = event.get("event_type", "unknown")
    repo = event.get("repository", "unknown")
    commits = event.get("payload", {}).get("commits", [])
    commit_summary = commits[0].get("message", "No commit message") if commits else "No commits"
    
    content = f"{event_type} on {repo}: {commit_summary}"
    
    return StoryBeat(
        id=f"beat_{event.get('timestamp', 'unknown')}",
        sequence=sequence,
        content=content,
        narrative_function=narrative_func,
        act=act,
        universe_analysis=analysis,
        lead_universe=analysis.lead_universe,
        source="webhook",
        source_event_id=event.get("payload", {}).get("head_commit", {}).get("id", "unknown"),
    )


def run_example():
    """Run the complete webhook → analysis → beat pipeline."""
    
    print("=" * 70)
    print("NARRATIVE INTELLIGENCE: Webhook Processing Example")
    print("=" * 70)
    
    # Step 1: Simulate webhook arrival
    print("\n📨 INCOMING WEBHOOK EVENT")
    print("-" * 50)
    print(f"Type: {SAMPLE_WEBHOOK_EVENT['event_type']}")
    print(f"Repository: {SAMPLE_WEBHOOK_EVENT['repository']}")
    print(f"Sender: {SAMPLE_WEBHOOK_EVENT['sender']}")
    commit_msg = SAMPLE_WEBHOOK_EVENT['payload']['head_commit']['message']
    print(f"Commit: {commit_msg}")
    
    # Step 2: Run three-universe analysis
    print("\n🌍 THREE-UNIVERSE ANALYSIS")
    print("-" * 50)
    
    analysis = create_three_universe_analysis(SAMPLE_WEBHOOK_EVENT)
    
    print(f"\n  🔧 ENGINEER (Mia):")
    print(f"     Intent: {analysis.engineer.intent}")
    print(f"     Confidence: {analysis.engineer.confidence:.0%}")
    print(f"     Flows: {', '.join(analysis.engineer.suggested_flows)}")
    
    print(f"\n  🕯️ CEREMONY (Ava8):")
    print(f"     Intent: {analysis.ceremony.intent}")
    print(f"     Confidence: {analysis.ceremony.confidence:.0%}")
    print(f"     Flows: {', '.join(analysis.ceremony.suggested_flows)}")
    
    print(f"\n  📖 STORY ENGINE (Miette):")
    print(f"     Intent: {analysis.story_engine.intent}")
    print(f"     Confidence: {analysis.story_engine.confidence:.0%}")
    print(f"     Act: {analysis.story_engine.context.get('act')}")
    
    print(f"\n  ✨ SYNTHESIS:")
    print(f"     Lead Universe: {analysis.lead_universe.value}")
    print(f"     Coherence: {analysis.coherence_score:.0%}")
    
    # Step 3: Create story beat
    print("\n📝 STORY BEAT CREATION")
    print("-" * 50)
    
    beat = create_beat_from_webhook_event(
        event=SAMPLE_WEBHOOK_EVENT,
        analysis=analysis,
        sequence=1,
    )
    
    print(f"  Beat ID: {beat.id}")
    print(f"  Content: {beat.content}")
    print(f"  Narrative Function: {beat.narrative_function.value}")
    print(f"  Act: {beat.act}")
    print(f"  Lead Universe: {beat.lead_universe.value}")
    
    # Step 4: Add to narrative state
    print("\n💾 STATE UPDATE")
    print("-" * 50)
    
    state = create_new_narrative_state(
        story_id="narrative-intelligence-development",
        session_id="example-session-001",
    )
    state.beats.append(beat)
    state.position.act = beat.act
    
    print(f"  Session ID: {state.session_id}")
    print(f"  Total Beats: {len(state.beats)}")
    print(f"  Current Act: {state.position.act}")
    print(f"  Characters: {list(state.characters.keys())}")
    print(f"  Themes: {list(state.themes.keys())}")
    
    # Step 5: Show serialization (for Redis)
    print("\n📤 SERIALIZATION (Redis-ready)")
    print("-" * 50)
    
    state_dict = state.to_dict()
    print(f"  Keys: {list(state_dict.keys())}")
    print(f"  Beats stored: {len(state_dict['beats'])}")
    
    # Pretty print one beat
    if state_dict['beats']:
        print(f"\n  Sample beat JSON:")
        beat_json = json.dumps(state_dict['beats'][0], indent=4)
        for line in beat_json.split('\n')[:15]:
            print(f"    {line}")
        print("    ...")
    
    print("\n" + "=" * 70)
    print("✅ PIPELINE COMPLETE")
    print("=" * 70)
    print("\nThis demonstrates the core flow that will be used by:")
    print("  • ava-langflow: Universal router with three-universe dispatch")
    print("  • ava-Flowise: Agent coordination with narrative context")
    print("  • Miadi-46: Event-driven story continuity")
    print("  • LangChain: Traced operations with narrative metadata")
    

if __name__ == "__main__":
    run_example()
