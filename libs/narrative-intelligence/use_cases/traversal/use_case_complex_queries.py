"""
USE CASE 2: Narrative Traversal - Complex Query Patterns

Scenario: A story analytics dashboard needs to answer complex questions about narratives:
- Which scenes involve multiple characters?
- How does a theme evolve across the story?
- What's the emotional journey of a character?
- Which beats connect specific story points?

This demonstrates the versatility of the Narrative Traversal Node.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from narrative_intelligence import NCPLoaderNode, NarrativeTraversalNode, TraversalMode


def load_fantasy_narrative():
    """Load the fantasy epic for analysis."""
    loader = NCPLoaderNode()
    file_path = Path(__file__).parent / "fantasy_epic.json"
    return loader.load_from_file(file_path)


def use_case_character_journey():
    """Query: Show me all scenes involving a specific character."""
    print("=" * 70)
    print("USE CASE 2A: Character Journey Traversal")
    print("=" * 70)
    print("\nQuery: 'Show me all beats in Elara's journey'\n")

    ncp_data = load_fantasy_narrative()
    traversal = NarrativeTraversalNode(mode=TraversalMode.PLAYER_JOURNEY)

    # Get all beats involving Elara
    elara_beats = traversal.traverse_player_journey(ncp_data, "elara_001")

    print(f"✅ Found {len(elara_beats)} beats in Elara's journey:\n")
    for i, beat in enumerate(elara_beats, 1):
        print(f"   {i}. {beat.title}")
        print(f"      Emotion: {beat.emotional_weight}")
        print(f"      Other characters: {len(beat.related_players) - 1}")
        print()

    # Filtered query: Only solo scenes
    solo_beats = traversal.traverse_player_journey(
        ncp_data,
        "elara_001",
        filter_func=lambda b: len(b.related_players) == 1
    )

    print(f"🎯 Filtered: {len(solo_beats)} beats where Elara is alone:")
    for beat in solo_beats:
        print(f"   - {beat.title}")
    print()


def use_case_thematic_exploration():
    """Query: How does the theme of 'justice' manifest in the story?"""
    print("=" * 70)
    print("USE CASE 2B: Thematic Trace Traversal")
    print("=" * 70)
    print("\nQuery: 'Find all beats exploring Vengeance vs Justice'\n")

    ncp_data = load_fantasy_narrative()
    traversal = NarrativeTraversalNode(mode=TraversalMode.THEMATIC_TRACE)

    # Find beats related to vengeance vs justice theme
    justice_beats = traversal.find_thematic_beats(ncp_data, "vengeance_justice")

    print(f"✅ Found {len(justice_beats)} beats exploring this theme:\n")
    for beat in justice_beats:
        print(f"   • {beat.title}")
        print(f"     Description: {beat.description[:80]}...")
        print(f"     Emotional weight: {beat.emotional_weight}")
        print()

    # Custom search terms
    print("🔍 Custom Search: Beats mentioning 'revenge' or 'mercy':\n")
    custom_beats = traversal.find_thematic_beats(
        ncp_data,
        "vengeance_justice",
        search_terms=["revenge", "mercy", "justice", "vengeance"]
    )

    for beat in custom_beats:
        print(f"   - {beat.title}")
    print()


def use_case_emotional_arc_tracking():
    """Query: Show the emotional progression of the story."""
    print("=" * 70)
    print("USE CASE 2C: Emotional Arc Traversal")
    print("=" * 70)
    print("\nQuery: 'What's the emotional landscape of this story?'\n")

    ncp_data = load_fantasy_narrative()
    traversal = NarrativeTraversalNode(mode=TraversalMode.EMOTIONAL_ARC)

    # Track different emotional tones
    emotions = ["Tense", "Hopeful", "Devastating", "Triumphant", "Conflicted"]

    print("📊 Emotional Distribution:\n")
    for emotion in emotions:
        beats = traversal.find_beats_by_emotional_weight(ncp_data, emotion)
        if beats:
            print(f"   {emotion}: {len(beats)} beat(s)")
            for beat in beats:
                print(f"      - {beat.title}")
    print()


def use_case_relationship_mapping():
    """Query: Which characters interact most?"""
    print("=" * 70)
    print("USE CASE 2D: Relationship Network Analysis")
    print("=" * 70)
    print("\nQuery: 'Map character interactions across the story'\n")

    ncp_data = load_fantasy_narrative()
    traversal = NarrativeTraversalNode()

    # Build relationship map
    relationships = {}
    for player in ncp_data.players:
        player_beats = traversal.traverse_player_journey(ncp_data, player.player_id)

        # Find co-occurrences
        co_stars = set()
        for beat in player_beats:
            for other_id in beat.related_players:
                if other_id != player.player_id:
                    co_stars.add(other_id)

        relationships[player.name] = {
            "total_beats": len(player_beats),
            "works_with": [ncp_data.get_player(pid).name for pid in co_stars]
        }

    print("👥 Character Interaction Matrix:\n")
    for char_name, data in relationships.items():
        print(f"   {char_name}:")
        print(f"      Appears in: {data['total_beats']} beats")
        print(f"      Interacts with: {', '.join(data['works_with']) if data['works_with'] else 'Solo journey'}")
        print()


def use_case_connected_elements():
    """Query: What elements connect to a specific beat?"""
    print("=" * 70)
    print("USE CASE 2E: Connected Elements Discovery")
    print("=" * 70)
    print("\nQuery: 'Show me everything connected to The Choice of Mercy beat'\n")

    ncp_data = load_fantasy_narrative()
    traversal = NarrativeTraversalNode()

    # Get all connected elements
    connections = traversal.get_connected_elements(ncp_data, "sb_005")

    print("🔗 Connected Elements:\n")
    print(f"   Players involved: {len(connections['players'])}")
    for player in connections['players']:
        print(f"      - {player.name} ({player.role})")

    print(f"\n   Story points: {len(connections['storypoints'])}")
    for sp in connections['storypoints']:
        print(f"      - {sp.title} ({sp.type})")

    print(f"\n   Moments: {len(connections['moments'])}")
    for moment in connections['moments']:
        print(f"      - {moment.description}")
    print()


def use_case_multi_character_scenes():
    """Query: Find all ensemble scenes."""
    print("=" * 70)
    print("USE CASE 2F: Multi-Character Scene Detection")
    print("=" * 70)
    print("\nQuery: 'Find all beats where all three main characters appear'\n")

    ncp_data = load_fantasy_narrative()

    main_cast = ["elara_001", "thorne_002", "lysandra_003"]
    ensemble_beats = []

    for beat in ncp_data.storybeats:
        if all(char_id in beat.related_players for char_id in main_cast):
            ensemble_beats.append(beat)

    print(f"✅ Found {len(ensemble_beats)} ensemble scenes:\n")
    for beat in ensemble_beats:
        print(f"   • {beat.title}")
        print(f"     Emotional weight: {beat.emotional_weight}")
        print(f"     All {len(beat.related_players)} characters present")
        print()


def main():
    print("\n⚔️ NARRATIVE TRAVERSAL - COMPLEX QUERY PATTERNS\n")

    # Run all use cases
    use_case_character_journey()
    use_case_thematic_exploration()
    use_case_emotional_arc_tracking()
    use_case_relationship_mapping()
    use_case_connected_elements()
    use_case_multi_character_scenes()

    print("=" * 70)
    print("📊 SUMMARY")
    print("=" * 70)
    print("\n✅ Demonstrated query capabilities:")
    print("   1. Character journey tracking")
    print("   2. Thematic exploration with custom search")
    print("   3. Emotional arc analysis")
    print("   4. Relationship network mapping")
    print("   5. Connected elements discovery")
    print("   6. Multi-character scene detection")
    print("\n💡 The Traversal Node answers complex narrative questions efficiently")
    print()


if __name__ == "__main__":
    main()
