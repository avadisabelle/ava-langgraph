"""
Example usage of the Narrative Intelligence Toolkit.

This script demonstrates how to use all 5 core components to analyze a narrative.
"""

from pathlib import Path
from narrative_intelligence import (
    NCPLoaderNode,
    NarrativeTraversalNode,
    CharacterArcGenerator,
    ThematicTensionAnalyzer,
    EmotionalBeatClassifierNode,
)


def main():
    print("🧠🌸 Narrative Intelligence Toolkit - Usage Example\n")
    print("=" * 60)

    # Path to sample narrative
    sample_file = Path(__file__).parent / "sample_narrative.json"

    # ===================================================================
    # Component 1: Load NCP Data
    # ===================================================================
    print("\n1️⃣  Loading NCP data...\n")

    loader = NCPLoaderNode()
    ncp_data = loader.load_from_file(sample_file)

    print(f"✓ Loaded narrative: '{ncp_data.title}'")
    print(f"  - {len(ncp_data.players)} characters")
    print(f"  - {len(ncp_data.storybeats)} story beats")
    print(f"  - {len(ncp_data.perspectives)} thematic perspectives")

    # ===================================================================
    # Component 2: Narrative Traversal
    # ===================================================================
    print("\n2️⃣  Traversing narrative graph...\n")

    traversal = NarrativeTraversalNode()

    # Find all beats involving Sarah
    sarah_beats = traversal.traverse_player_journey(ncp_data, "sarah_001")
    print(f"✓ Found {len(sarah_beats)} story beats involving Sarah")

    # Find beats exploring safety vs vulnerability
    safety_beats = traversal.find_thematic_beats(ncp_data, "safety_vulnerability")
    print(f"✓ Found {len(safety_beats)} beats exploring 'Safety vs Vulnerability'")

    # ===================================================================
    # Component 3: Character Arc Generator
    # ===================================================================
    print("\n3️⃣  Generating character arc...\n")

    arc_generator = CharacterArcGenerator()
    sarah_arc = arc_generator.generate(ncp_data, "sarah_001")

    print("✓ Generated character arc for Sarah:\n")
    print("-" * 60)
    print(sarah_arc)
    print("-" * 60)

    # ===================================================================
    # Component 4: Thematic Tension Analyzer
    # ===================================================================
    print("\n4️⃣  Analyzing thematic tensions...\n")

    analyzer = ThematicTensionAnalyzer()
    thematic_analysis = analyzer.analyze(ncp_data, "safety_vulnerability")

    print("✓ Generated thematic analysis:\n")
    print("-" * 60)
    print(thematic_analysis)
    print("-" * 60)

    # ===================================================================
    # Component 5: Emotional Beat Classifier
    # ===================================================================
    print("\n5️⃣  Classifying emotional beats...\n")

    classifier = EmotionalBeatClassifierNode(use_llm=False)  # Using rule-based for demo

    print("Emotional classifications:\n")
    for beat in ncp_data.storybeats:
        result = classifier.classify_beat(beat)
        print(f"  - {beat.title}")
        print(f"    Classification: {result['classification']}")
        print(f"    Confidence: {result['confidence']:.2f}")
        print(f"    Method: {result['method']}\n")

    # ===================================================================
    # Summary
    # ===================================================================
    print("\n" + "=" * 60)
    print("🎉 All components successfully demonstrated!")
    print("=" * 60 + "\n")

    print("What you can do with this toolkit:")
    print("  • Load and validate NCP narrative data")
    print("  • Navigate narrative graphs by character, theme, or emotion")
    print("  • Generate character arc summaries with markdown output")
    print("  • Analyze how themes manifest throughout the story")
    print("  • Classify emotional tones of story beats")
    print()
    print("Next steps:")
    print("  • Integrate with LangFlow for visual components")
    print("  • Add LLM support for advanced analysis")
    print("  • Create custom analysis workflows")
    print()


if __name__ == "__main__":
    main()
