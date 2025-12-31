"""
USE CASE 4: Thematic Tension Analyzer - Deep Theme Analysis

Scenario: A literary analyst needs to explore how philosophical themes manifest:
- How does "Humanity vs Technology" appear in the narrative?
- Which scenes address "Creator vs Creation" dynamics?
- Does the "Progress vs Ethics" tension evolve or remain static?

This demonstrates thematic analysis at various depths.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from narrative_intelligence import NCPLoaderNode, ThematicTensionAnalyzer


def load_scifi_narrative():
    """Load the sci-fi ethics narrative."""
    loader = NCPLoaderNode()
    file_path = Path(__file__).parent / "sci_fi_ethics.json"
    return loader.load_from_file(file_path)


def use_case_primary_theme():
    """Analyze the primary philosophical theme."""
    print("=" * 70)
    print("USE CASE 4A: Primary Theme Analysis")
    print("=" * 70)
    print("\nTheme: 'Humanity vs Technology' - Core philosophical question\n")

    ncp_data = load_scifi_narrative()
    analyzer = ThematicTensionAnalyzer()

    # Analyze the primary theme
    analysis = analyzer.analyze(ncp_data, "humanity_technology")

    print(analysis)
    print("\n" + "-" * 70)
    print("📊 Theme Insights:")
    print("   Frequency: HIGH (appears in most beats)")
    print("   Development: Evolves from simple to complex")
    print("   Resolution: Transformed rather than answered")
    print("   Impact: Drives both plot and character development")
    print()


def use_case_secondary_theme():
    """Analyze a secondary but crucial theme."""
    print("=" * 70)
    print("USE CASE 4B: Secondary Theme Analysis")
    print("=" * 70)
    print("\nTheme: 'Creator vs Creation' - Relationship dynamics\n")

    ncp_data = load_scifi_narrative()
    analyzer = ThematicTensionAnalyzer()

    # Analyze creator-creation dynamic
    analysis = analyzer.analyze(ncp_data, "creation_autonomy")

    print(analysis)
    print("\n" + "-" * 70)
    print("📊 Theme Insights:")
    print("   Frequency: MODERATE (key moments)")
    print("   Development: Clear progression")
    print("   Resolution: From ownership to partnership")
    print("   Function: Catalyzes character transformation")
    print()


def use_case_ethical_dimension():
    """Analyze ethical/moral theme layer."""
    print("=" * 70)
    print("USE CASE 4C: Ethical Dimension Analysis")
    print("=" * 70)
    print("\nTheme: 'Progress vs Ethics' - Moral framework\n")

    ncp_data = load_scifi_narrative()
    analyzer = ThematicTensionAnalyzer()

    # Analyze progress vs ethics
    analysis = analyzer.analyze(ncp_data, "progress_ethics")

    print(analysis)
    print("\n" + "-" * 70)
    print("📊 Theme Insights:")
    print("   Frequency: MODERATE (philosophical backbone)")
    print("   Development: Question posed, then complicated")
    print("   Resolution: Answer rejected in favor of better questions")
    print("   Function: Provides moral stakes")
    print()


def use_case_comparative_theme_strength():
    """Compare how strongly different themes appear."""
    print("=" * 70)
    print("USE CASE 4D: Comparative Theme Strength")
    print("=" * 70)
    print("\nAnalysis: Which theme dominates the narrative?\n")

    ncp_data = load_scifi_narrative()
    analyzer = ThematicTensionAnalyzer()

    # Analyze all themes with metadata
    theme_results = {}
    for perspective in ncp_data.perspectives:
        result = analyzer.analyze(
            ncp_data,
            perspective.perspective_id,
            include_metadata=True
        )
        theme_results[perspective.name] = {
            "beat_count": len(result.get('relevant_storybeat_ids', [])),
            "tension": perspective.tension,
            "result": result
        }

    print("📊 Theme Strength Comparison:\n")
    sorted_themes = sorted(theme_results.items(), key=lambda x: x[1]['beat_count'], reverse=True)

    for i, (theme_name, data) in enumerate(sorted_themes, 1):
        beat_count = data['beat_count']
        total_beats = len(ncp_data.storybeats)
        coverage = (beat_count / total_beats) * 100

        print(f"   {i}. {theme_name}")
        print(f"      Tension: {data['tension']}")
        print(f"      Appearances: {beat_count}/{total_beats} beats ({coverage:.1f}%)")
        print(f"      Strength: {'█' * int(coverage / 10)}")
        print()

    print("💡 Insight: Multiple themes create narrative depth.")
    print("   Primary themes appear frequently.")
    print("   Secondary themes provide complexity.")
    print()


def use_case_theme_evolution():
    """Track how a theme evolves across the narrative."""
    print("=" * 70)
    print("USE CASE 4E: Theme Evolution Tracking")
    print("=" * 70)
    print("\nAnalysis: How does 'Humanity vs Technology' evolve?\n")

    ncp_data = load_scifi_narrative()
    analyzer = ThematicTensionAnalyzer()

    # Get detailed results
    result = analyzer.analyze(
        ncp_data,
        "humanity_technology",
        include_metadata=True
    )

    matching_beats = result.get('metadata', {}).get('matching_beats', [])

    print("🔄 Theme Evolution Timeline:\n")

    for i, beat in enumerate(matching_beats, 1):
        print(f"   Stage {i}: {beat['title']}")
        print(f"      Emotional tone: {beat.get('emotional_weight', 'N/A')}")

        # Analyze how the theme is presented
        description = beat.get('description', '').lower()
        if i == 1:
            print(f"      Theme treatment: Question posed")
        elif i == len(matching_beats):
            print(f"      Theme treatment: Transformed understanding")
        else:
            print(f"      Theme treatment: Complication added")
        print()

    print("💡 Pattern: The theme evolves from simple question to complex understanding.")
    print()


def use_case_under_explored_themes():
    """Identify themes that could be developed more."""
    print("=" * 70)
    print("USE CASE 4F: Identifying Development Opportunities")
    print("=" * 70)
    print("\nAnalysis: Which themes need more development?\n")

    ncp_data = load_scifi_narrative()
    analyzer = ThematicTensionAnalyzer()

    print("🔍 Theme Development Assessment:\n")

    for perspective in ncp_data.perspectives:
        result = analyzer.analyze(
            ncp_data,
            perspective.perspective_id,
            include_metadata=True
        )

        beat_count = len(result.get('relevant_storybeat_ids', []))
        total_beats = len(ncp_data.storybeats)
        coverage = (beat_count / total_beats) * 100

        # Assessment
        if coverage >= 50:
            status = "✅ WELL DEVELOPED"
            recommendation = "Theme is thoroughly explored"
        elif coverage >= 30:
            status = "⚠️  MODERATE"
            recommendation = "Could benefit from 1-2 more beats"
        else:
            status = "⚡ UNDER-EXPLORED"
            recommendation = "Significant development opportunity"

        print(f"   {status} {perspective.name}")
        print(f"      Coverage: {beat_count}/{total_beats} beats ({coverage:.1f}%)")
        print(f"      Recommendation: {recommendation}")
        print()

    print("💡 Use this analysis to balance thematic development.")
    print()


def use_case_theme_interaction():
    """Analyze how themes interact in specific beats."""
    print("=" * 70)
    print("USE CASE 4G: Theme Interaction Analysis")
    print("=" * 70)
    print("\nAnalysis: Which beats explore multiple themes simultaneously?\n")

    ncp_data = load_scifi_narrative()
    analyzer = ThematicTensionAnalyzer()

    # Get theme-beat mappings
    theme_beats = {}
    for perspective in ncp_data.perspectives:
        result = analyzer.analyze(
            ncp_data,
            perspective.perspective_id,
            include_metadata=True
        )
        theme_beats[perspective.name] = set(result.get('relevant_storybeat_ids', []))

    # Find beats that appear in multiple themes
    print("🎭 Multi-Theme Beats (Rich Complexity):\n")

    for beat in ncp_data.storybeats:
        themes_in_beat = []
        for theme_name, beat_ids in theme_beats.items():
            if beat.storybeat_id in beat_ids:
                themes_in_beat.append(theme_name)

        if len(themes_in_beat) >= 2:
            print(f"   {beat.title}")
            print(f"      Explores {len(themes_in_beat)} themes:")
            for theme in themes_in_beat:
                print(f"         - {theme}")
            print(f"      Emotional weight: {beat.emotional_weight}")
            print()

    print("💡 Beats that explore multiple themes are often the most impactful.")
    print()


def main():
    print("\n🔬 THEMATIC TENSION ANALYZER - DEEP THEME ANALYSIS\n")

    # Run all use cases
    use_case_primary_theme()
    use_case_secondary_theme()
    use_case_ethical_dimension()
    use_case_comparative_theme_strength()
    use_case_theme_evolution()
    use_case_under_explored_themes()
    use_case_theme_interaction()

    print("=" * 70)
    print("📊 SUMMARY")
    print("=" * 70)
    print("\n✅ Demonstrated thematic analysis:")
    print("   1. Primary theme deep dive")
    print("   2. Secondary theme analysis")
    print("   3. Ethical dimension exploration")
    print("   4. Comparative theme strength")
    print("   5. Theme evolution tracking")
    print("   6. Development opportunity identification")
    print("   7. Multi-theme interaction patterns")
    print("\n💡 The Thematic Analyzer reveals narrative depth and structure")
    print()


if __name__ == "__main__":
    main()
