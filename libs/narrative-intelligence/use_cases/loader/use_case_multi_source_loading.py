"""
USE CASE 1: NCP Loader - Multi-Source Data Loading

Scenario: A narrative analysis platform needs to load NCP data from various sources:
- Local JSON files (most common)
- Remote URLs (collaborative storytelling)
- In-memory dictionaries (programmatic generation)

This example demonstrates all three loading methods and validation.
"""

import sys
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from narrative_intelligence import NCPLoaderNode


def use_case_file_loading():
    """Load NCP data from a local JSON file."""
    print("=" * 70)
    print("USE CASE 1A: Loading from Local File")
    print("=" * 70)
    print("\nScenario: Loading a tech thriller narrative from local storage\n")

    loader = NCPLoaderNode(validate=True)

    # Load from file
    file_path = Path(__file__).parent / "tech_thriller.json"
    ncp_data = loader.load_from_file(file_path)

    print(f"✅ Successfully loaded: '{ncp_data.title}'")
    print(f"   Author: {ncp_data.author}")
    print(f"   Genre: {ncp_data.metadata.get('genre')}")
    print(f"   Characters: {len(ncp_data.players)}")
    print(f"   Story Beats: {len(ncp_data.storybeats)}")
    print(f"   Themes: {len(ncp_data.perspectives)}")

    # Demonstrate validation
    print("\n📋 Validation Details:")
    print(f"   - All players have IDs: {all(p.player_id for p in ncp_data.players)}")
    print(f"   - All beats have descriptions: {all(sb.description for sb in ncp_data.storybeats)}")
    print(f"   - Schema version: {ncp_data.version}")

    return ncp_data


def use_case_dict_loading():
    """Load NCP data from an in-memory dictionary."""
    print("\n" + "=" * 70)
    print("USE CASE 1B: Loading from Dictionary (Programmatic Generation)")
    print("=" * 70)
    print("\nScenario: Dynamically generating a micro-narrative in code\n")

    loader = NCPLoaderNode(validate=True)

    # Create narrative programmatically
    narrative_dict = {
        "title": "The Decision",
        "author": "Generated Example",
        "version": "1.0",
        "players": [
            {
                "player_id": "hero_001",
                "name": "The Hero",
                "wound": "Failed to save someone important",
                "desire": "Redemption through sacrifice",
                "arc": "Learns that redemption comes from living, not dying",
                "role": "protagonist",
                "metadata": {}
            }
        ],
        "perspectives": [
            {
                "perspective_id": "sacrifice_survival",
                "name": "Sacrifice vs Survival",
                "description": "The tension between self-sacrifice and self-preservation",
                "thematic_question": "Is dying for others the only form of redemption?",
                "tension": "Sacrifice vs Survival",
                "metadata": {}
            }
        ],
        "storybeats": [
            {
                "storybeat_id": "beat_001",
                "title": "The Choice",
                "description": "The hero faces a moment where they can save others by sacrificing themselves.",
                "emotional_weight": "Tense",
                "moments": [],
                "related_players": ["hero_001"],
                "related_storypoints": [],
                "metadata": {}
            }
        ],
        "storypoints": [],
        "metadata": {"generated": True, "genre": "Moral Dilemma"}
    }

    ncp_data = loader.load_from_dict(narrative_dict)

    print(f"✅ Successfully created: '{ncp_data.title}'")
    print(f"   Programmatically generated: {ncp_data.metadata.get('generated')}")
    print(f"   Character: {ncp_data.players[0].name}")
    print(f"   Core conflict: {ncp_data.perspectives[0].tension}")

    return ncp_data


def use_case_validation_error():
    """Demonstrate validation error handling."""
    print("\n" + "=" * 70)
    print("USE CASE 1C: Validation Error Handling")
    print("=" * 70)
    print("\nScenario: Attempting to load malformed NCP data\n")

    loader = NCPLoaderNode(validate=True)

    # Invalid data (missing required fields)
    invalid_data = {
        "title": "Incomplete Story",
        # Missing required 'version' field
        "players": [
            {
                "player_id": "char_001",
                # Missing required 'name' field
                "wound": "Something bad happened"
            }
        ]
    }

    try:
        ncp_data = loader.load_from_dict(invalid_data)
        print("❌ Should have raised validation error!")
    except Exception as e:
        print(f"✅ Validation correctly caught errors:")
        print(f"   Error type: {type(e).__name__}")
        print(f"   Details: {str(e)[:200]}...")
        print("\n💡 Validation ensures data integrity before analysis begins")


def use_case_integration_langgraph():
    """Demonstrate using NCP Loader in a LangGraph workflow."""
    print("\n" + "=" * 70)
    print("USE CASE 1D: Integration with LangGraph State")
    print("=" * 70)
    print("\nScenario: Using NCPLoader as a node in a LangGraph workflow\n")

    from narrative_intelligence import NCPLoaderNode

    loader_node = NCPLoaderNode()

    # Simulate LangGraph state
    state = {
        "ncp_data": None,
        "error": None,
        "messages": [],
        "metadata": {
            "ncp_file_path": str(Path(__file__).parent / "tech_thriller.json")
        }
    }

    # Call node (as LangGraph would)
    result_state = loader_node(state)

    print("✅ LangGraph Integration:")
    print(f"   State updated: {result_state['ncp_data'] is not None}")
    print(f"   No errors: {result_state['error'] is None}")
    print(f"   Narrative loaded: {result_state['ncp_data'].title}")
    print(f"   Ready for downstream nodes: ✓")

    return result_state


def main():
    print("\n🎬 NCP LOADER - MULTI-SOURCE DATA LOADING USE CASES\n")

    # Run all use cases
    use_case_file_loading()
    use_case_dict_loading()
    use_case_validation_error()
    use_case_integration_langgraph()

    print("\n" + "=" * 70)
    print("📊 SUMMARY")
    print("=" * 70)
    print("\n✅ All loading methods demonstrated:")
    print("   1. File loading - For production narratives")
    print("   2. Dictionary loading - For programmatic generation")
    print("   3. Validation - Ensures data integrity")
    print("   4. LangGraph integration - Ready for workflows")
    print("\n💡 The NCP Loader is the foundation for all narrative analysis")
    print()


if __name__ == "__main__":
    main()
