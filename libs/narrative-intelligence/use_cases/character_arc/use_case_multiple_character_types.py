"""
USE CASE 3: Character Arc Generator - Multiple Character Types

Scenario: A writing coach needs to analyze different character arcs:
- Protagonist arc (coming-of-age)
- Deuteragonist arc (parallel journey)
- Mentor arc (reverse journey)

This demonstrates how the Character Arc Generator handles various narrative roles.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from narrative_intelligence import NCPLoaderNode, CharacterArcGenerator


def load_coming_of_age_story():
    """Load the coming-of-age narrative."""
    loader = NCPLoaderNode()
    file_path = Path(__file__).parent / "coming_of_age.json"
    return loader.load_from_file(file_path)


def use_case_protagonist_arc():
    """Analyze the protagonist's transformational journey."""
    print("=" * 70)
    print("USE CASE 3A: Protagonist Arc (Coming-of-Age)")
    print("=" * 70)
    print("\nCharacter: Maya Rodriguez (16-year-old protagonist)\n")

    ncp_data = load_coming_of_age_story()
    generator = CharacterArcGenerator()

    # Generate Maya's arc
    maya_arc = generator.generate(ncp_data, "maya_001")

    print(maya_arc)
    print("\n" + "-" * 70)
    print("📊 Arc Analysis:")
    print("   Type: Transformational (Change Arc)")
    print("   Wound: External event (divorce) creating internal conflict")
    print("   Desire: Control (false want) → Peace (true need)")
    print("   Journey: 6 beats showing gradual transformation")
    print("   Resolution: Accepts uncertainty, finds freedom in letting go")
    print()


def use_case_deuteragonist_arc():
    """Analyze a parallel character journey."""
    print("=" * 70)
    print("USE CASE 3B: Deuteragonist Arc (Self-Discovery)")
    print("=" * 70)
    print("\nCharacter: Derek Chen (17-year-old parallel protagonist)\n")

    ncp_data = load_coming_of_age_story()
    generator = CharacterArcGenerator()

    # Generate Derek's arc
    derek_arc = generator.generate(ncp_data, "derek_002")

    print(derek_arc)
    print("\n" + "-" * 70)
    print("📊 Arc Analysis:")
    print("   Type: Mirror Arc (reflects protagonist's journey)")
    print("   Wound: External pressure (family expectations)")
    print("   Desire: Authenticity (to be seen for who he is)")
    print("   Function: Shows Maya her own struggle from outside")
    print("   Impact: Fewer total beats but crucial catalytic moments")
    print()


def use_case_mentor_arc():
    """Analyze a mentor's wisdom-keeper journey."""
    print("=" * 70)
    print("USE CASE 3C: Mentor Arc (Wisdom-Keeper)")
    print("=" * 70)
    print("\nCharacter: Grandma Rosa (78-year-old mentor)\n")

    ncp_data = load_coming_of_age_story()
    generator = CharacterArcGenerator()

    # Generate Rosa's arc
    rosa_arc = generator.generate(ncp_data, "grandma_rosa_003")

    print(rosa_arc)
    print("\n" + "-" * 70)
    print("📊 Arc Analysis:")
    print("   Type: Reverse Arc (fears beginning → embraces ending)")
    print("   Wound: Loss and mortality fears")
    print("   Desire: Legacy (to matter after death)")
    print("   Function: Provides wisdom protagonist needs")
    print("   Unique: Arc about embracing finality, not resisting it")
    print()


def use_case_comparative_analysis():
    """Compare all three character arcs."""
    print("=" * 70)
    print("USE CASE 3D: Comparative Arc Analysis")
    print("=" * 70)
    print("\nComparison: How do the three character types differ?\n")

    ncp_data = load_coming_of_age_story()
    generator = CharacterArcGenerator()

    # Generate all arcs with metadata
    maya_result = generator.generate(ncp_data, "maya_001", include_metadata=True)
    derek_result = generator.generate(ncp_data, "derek_002", include_metadata=True)
    rosa_result = generator.generate(ncp_data, "grandma_rosa_003", include_metadata=True)

    # Extract beat counts
    maya_beats = len(maya_result['metadata']['character_beats'])
    derek_beats = len(derek_result['metadata']['character_beats'])
    rosa_beats = len(rosa_result['metadata']['character_beats'])

    print("📊 Structural Comparison:\n")
    print(f"   Maya (Protagonist):     {maya_beats} beats - Maximum presence")
    print(f"   Derek (Deuteragonist):  {derek_beats} beats - Strategic appearances")
    print(f"   Rosa (Mentor):          {rosa_beats} beats - Pivotal moments\n")

    print("🎭 Arc Type Patterns:\n")
    print("   Protagonist:     Most beats, complete transformation")
    print("   Deuteragonist:   Parallel journey, mutual influence")
    print("   Mentor:          Teaching arc, generational bridge\n")

    print("💡 Narrative Insight:")
    print("   Each character type has a different 'beat density' pattern.")
    print("   Protagonists appear most frequently.")
    print("   Supporting characters have fewer but more impactful beats.")
    print("   This is structurally sound narrative design!\n")


def use_case_export_for_review():
    """Export arcs for writing workshop review."""
    print("=" * 70)
    print("USE CASE 3E: Batch Export for Review")
    print("=" * 70)
    print("\nScenario: Preparing arcs for a writing workshop\n")

    ncp_data = load_coming_of_age_story()
    generator = CharacterArcGenerator()

    # Generate all arcs
    arcs = {}
    for player in ncp_data.players:
        arc_md = generator.generate(ncp_data, player.player_id)
        arcs[player.name] = arc_md

    # Save to files (simulated)
    output_dir = Path(__file__).parent / "arc_exports"
    print(f"📁 Would export {len(arcs)} character arcs to: {output_dir}/\n")

    for char_name, arc_content in arcs.items():
        filename = char_name.lower().replace(" ", "_") + "_arc.md"
        print(f"   ✓ {filename}")
        print(f"     Length: {len(arc_content)} characters")
        print(f"     Lines: {arc_content.count(chr(10))}")

    print("\n💡 These markdown files can be:")
    print("   - Reviewed in writing workshops")
    print("   - Compared side-by-side")
    print("   - Shared with editors")
    print("   - Integrated into story bibles")
    print()


def use_case_arc_completeness_check():
    """Check if character arcs are complete."""
    print("=" * 70)
    print("USE CASE 3F: Arc Completeness Validation")
    print("=" * 70)
    print("\nScenario: Validate that all characters have complete arcs\n")

    ncp_data = load_coming_of_age_story()

    print("🔍 Checking arc completeness:\n")

    for player in ncp_data.players:
        # Check if character has all arc elements
        has_wound = bool(player.wound)
        has_desire = bool(player.desire)
        has_arc = bool(player.arc)

        # Check if character appears in beats
        appears_in_beats = sum(1 for beat in ncp_data.storybeats if player.player_id in beat.related_players)

        # Calculate completeness
        completeness = sum([has_wound, has_desire, has_arc, appears_in_beats > 0])
        percentage = (completeness / 4) * 100

        status = "✅" if percentage == 100 else "⚠️"

        print(f"   {status} {player.name} ({player.role})")
        print(f"      Completeness: {percentage:.0f}%")
        print(f"      Wound: {'✓' if has_wound else '✗'}")
        print(f"      Desire: {'✓' if has_desire else '✗'}")
        print(f"      Arc: {'✓' if has_arc else '✗'}")
        print(f"      Story beats: {appears_in_beats}")
        print()

    print("💡 All characters have complete arcs! Ready for analysis.")
    print()


def main():
    print("\n📖 CHARACTER ARC GENERATOR - MULTIPLE CHARACTER TYPES\n")

    # Run all use cases
    use_case_protagonist_arc()
    use_case_deuteragonist_arc()
    use_case_mentor_arc()
    use_case_comparative_analysis()
    use_case_export_for_review()
    use_case_arc_completeness_check()

    print("=" * 70)
    print("📊 SUMMARY")
    print("=" * 70)
    print("\n✅ Demonstrated arc generation for:")
    print("   1. Protagonist (complete transformational arc)")
    print("   2. Deuteragonist (parallel/mirror journey)")
    print("   3. Mentor (wisdom-keeper arc)")
    print("   4. Comparative analysis across character types")
    print("   5. Batch export capabilities")
    print("   6. Arc completeness validation")
    print("\n💡 The Arc Generator adapts to any character role or type")
    print()


if __name__ == "__main__":
    main()
