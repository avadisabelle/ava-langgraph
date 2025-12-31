"""
USE CASE 5: Emotional Beat Classifier - Batch Processing & Visualization

Scenario: A screenplay analyst needs to map the emotional journey:
- Classify emotions for all beats efficiently
- Create an emotional landscape visualization
- Identify emotional rhythm patterns
- Compare emotional arcs across acts

This demonstrates batch processing and emotional analysis.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from narrative_intelligence import NCPLoaderNode, EmotionalBeatClassifierNode


def load_thriller_screenplay():
    """Load the thriller screenplay."""
    loader = NCPLoaderNode()
    file_path = Path(__file__).parent / "thriller_screenplay.json"
    return loader.load_from_file(file_path)


def use_case_batch_classification():
    """Classify all beats in one workflow."""
    print("=" * 70)
    print("USE CASE 5A: Batch Emotional Classification")
    print("=" * 70)
    print("\nScenario: Classify all 12 beats in the screenplay\n")

    ncp_data = load_thriller_screenplay()
    classifier = EmotionalBeatClassifierNode(use_llm=False)

    # Batch classify all beats
    results = []
    for beat in ncp_data.storybeats:
        result = classifier.classify_beat(beat)
        results.append({
            "title": beat.title,
            "classification": result["classification"],
            "confidence": result["confidence"],
            "method": result["method"]
        })

    print("✅ Classified all beats:\n")
    for i, result in enumerate(results, 1):
        conf_bar = "█" * int(result["confidence"] * 10)
        print(f"   {i:2d}. {result['title']}")
        print(f"       Emotion: {result['classification']:15s} Confidence: {conf_bar} {result['confidence']:.2f}")
    print()

    return results


def use_case_emotional_landscape():
    """Create an emotional journey visualization."""
    print("=" * 70)
    print("USE CASE 5B: Emotional Landscape Visualization")
    print("=" * 70)
    print("\nScenario: Map the emotional journey of the screenplay\n")

    ncp_data = load_thriller_screenplay()
    classifier = EmotionalBeatClassifierNode(use_llm=False)

    # Define emotional intensity scores (for visualization)
    intensity_map = {
        "Peaceful": 1,
        "Hopeful": 2,
        "Melancholic": 3,
        "Conflicted": 4,
        "Tense": 5,
        "Fearful": 6,
        "Devastating": 7,
        "Triumphant": 3,  # Positive but intense
        "Joyful": 2,
    }

    # Classify and map
    emotional_journey = []
    for i, beat in enumerate(ncp_data.storybeats):
        result = classifier.classify_beat(beat)
        intensity = intensity_map.get(result["classification"], 4)
        emotional_journey.append({
            "sequence": i + 1,
            "title": beat.title,
            "emotion": result["classification"],
            "intensity": intensity,
            "act": beat.metadata.get("act", 1)
        })

    # Visualize
    print("📊 Emotional Intensity Journey:\n")
    print("    1 (Low) ─────────────────────────────────────── 7 (High)\n")

    for beat in emotional_journey:
        # Create visual bar
        bar = "█" * beat["intensity"]
        space = " " * (7 - beat["intensity"])
        act_marker = f"[Act {beat['act']}]"

        print(f"   {beat['sequence']:2d}. {act_marker} {bar}{space} {beat['emotion']:15s} - {beat['title']}")

    print("\n💡 Emotional Arc Analysis:")
    print(f"   Act 1: Gradual tension build (beats 1-3)")
    print(f"   Act 2: Escalating crisis (beats 4-8)")
    print(f"   Act 3: Resolution journey (beats 9-12)")
    print()


def use_case_act_structure_analysis():
    """Analyze emotional patterns by act."""
    print("=" * 70)
    print("USE CASE 5C: Three-Act Emotional Structure")
    print("=" * 70)
    print("\nScenario: Compare emotional tones across acts\n")

    ncp_data = load_thriller_screenplay()
    classifier = EmotionalBeatClassifierNode(use_llm=False)

    # Group by act
    act_emotions = {1: [], 2: [], 3: []}

    for beat in ncp_data.storybeats:
        result = classifier.classify_beat(beat)
        act = beat.metadata.get("act", 1)
        act_emotions[act].append(result["classification"])

    # Analyze each act
    print("🎬 Act-by-Act Emotional Analysis:\n")

    for act_num in [1, 2, 3]:
        emotions = act_emotions[act_num]
        print(f"   ACT {act_num}:")
        print(f"      Beat count: {len(emotions)}")

        # Count emotion types
        emotion_counts = {}
        for emotion in emotions:
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1

        print(f"      Dominant emotions:")
        for emotion, count in sorted(emotion_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"         - {emotion}: {count} beat(s)")

        # Determine act character
        if act_num == 1:
            print(f"      Character: Setup (building tension)")
        elif act_num == 2:
            print(f"      Character: Confrontation (maximum pressure)")
        else:
            print(f"      Character: Resolution (release and transformation)")
        print()

    print("💡 This follows classic thriller structure perfectly!")
    print()


def use_case_emotional_rhythm():
    """Identify pacing patterns in emotional beats."""
    print("=" * 70)
    print("USE CASE 5D: Emotional Rhythm & Pacing")
    print("=" * 70)
    print("\nScenario: Analyze the rhythm of emotional beats\n")

    ncp_data = load_thriller_screenplay()
    classifier = EmotionalBeatClassifierNode(use_llm=False)

    # Classify with intensity scores
    high_intensity = ["Devastating", "Fearful", "Tense"]
    low_intensity = ["Peaceful", "Hopeful", "Joyful"]
    medium_intensity = ["Melancholic", "Conflicted", "Triumphant"]

    rhythm = []
    for i, beat in enumerate(ncp_data.storybeats):
        result = classifier.classify_beat(beat)
        emotion = result["classification"]

        if emotion in high_intensity:
            level = "HIGH"
        elif emotion in low_intensity:
            level = "LOW"
        else:
            level = "MED"

        rhythm.append(level)

    # Display rhythm
    print("🎵 Emotional Pacing Rhythm:\n")
    print("   " + " → ".join(rhythm))
    print()

    # Analyze patterns
    print("📊 Rhythm Analysis:\n")

    # Count consecutive highs
    max_consecutive = 0
    current_consecutive = 0
    for level in rhythm:
        if level == "HIGH":
            current_consecutive += 1
            max_consecutive = max(max_consecutive, current_consecutive)
        else:
            current_consecutive = 0

    print(f"   Longest high-intensity sequence: {max_consecutive} beats")

    # Check for relief beats
    relief_count = sum(1 for i, level in enumerate(rhythm[:-1]) if level == "HIGH" and rhythm[i+1] != "HIGH")
    print(f"   Relief moments after intensity: {relief_count}")

    print(f"\n💡 Pacing Insight:")
    if max_consecutive >= 4:
        print(f"   ⚠️  Caution: {max_consecutive} consecutive high-intensity beats")
        print(f"      Consider adding a breather moment")
    else:
        print(f"   ✅ Good pacing: Intensity varied appropriately")
    print()


def use_case_emotional_progression():
    """Track how a specific emotion evolves."""
    print("=" * 70)
    print("USE CASE 5E: Emotional Progression Tracking")
    print("=" * 70)
    print("\nScenario: How does 'fear' manifest across the narrative?\n")

    ncp_data = load_thriller_screenplay()
    classifier = EmotionalBeatClassifierNode(use_llm=False)

    # Track fear-related emotions
    fear_family = ["Fearful", "Tense", "Devastating"]
    fear_beats = []

    for beat in ncp_data.storybeats:
        result = classifier.classify_beat(beat)
        if result["classification"] in fear_family:
            fear_beats.append({
                "title": beat.title,
                "emotion": result["classification"],
                "description": beat.description[:80] + "..."
            })

    print(f"😨 Fear Progression ({len(fear_beats)} beats):\n")

    for i, beat in enumerate(fear_beats, 1):
        print(f"   {i}. {beat['title']}")
        print(f"      Type: {beat['emotion']}")
        print(f"      Context: {beat['description']}")
        print()

    print("💡 Fear Evolution:")
    print("   Starts: External threat (Tense)")
    print("   Escalates: Internal paralysis (Fearful)")
    print("   Peaks: Consequences realized (Devastating)")
    print("   This tracks the protagonist's journey authentically")
    print()


def use_case_confidence_analysis():
    """Analyze classification confidence scores."""
    print("=" * 70)
    print("USE CASE 5F: Classification Confidence Analysis")
    print("=" * 70)
    print("\nScenario: Which classifications are most reliable?\n")

    ncp_data = load_thriller_screenplay()
    classifier = EmotionalBeatClassifierNode(use_llm=False)

    # Classify with confidence tracking
    high_confidence = []
    low_confidence = []

    for beat in ncp_data.storybeats:
        result = classifier.classify_beat(beat)
        if result["confidence"] >= 0.7:
            high_confidence.append((beat.title, result["classification"], result["confidence"]))
        else:
            low_confidence.append((beat.title, result["classification"], result["confidence"]))

    print(f"✅ High Confidence Classifications ({len(high_confidence)}):\n")
    for title, emotion, conf in high_confidence:
        print(f"   • {emotion:15s} ({conf:.2f}) - {title}")

    print(f"\n⚠️  Lower Confidence Classifications ({len(low_confidence)}):\n")
    for title, emotion, conf in low_confidence:
        print(f"   • {emotion:15s} ({conf:.2f}) - {title}")
        print(f"     → Consider LLM classification for better accuracy")

    print(f"\n💡 Confidence Insights:")
    print(f"   High confidence: {len(high_confidence)}/{len(ncp_data.storybeats)} beats")
    print(f"   For production use, run LLM classification on lower-confidence beats")
    print()


def use_case_export_emotional_data():
    """Export emotional data for visualization tools."""
    print("=" * 70)
    print("USE CASE 5G: Export for Visualization Tools")
    print("=" * 70)
    print("\nScenario: Prepare data for external charting tools\n")

    ncp_data = load_thriller_screenplay()
    classifier = EmotionalBeatClassifierNode(use_llm=False)

    # Generate export data
    export_data = []
    for i, beat in enumerate(ncp_data.storybeats, 1):
        result = classifier.classify_beat(beat)
        export_data.append({
            "sequence": i,
            "title": beat.title,
            "emotion": result["classification"],
            "confidence": result["confidence"],
            "act": beat.metadata.get("act", 1),
            "method": result["method"]
        })

    # Simulate CSV export
    print("📁 Export Format (CSV):\n")
    print("   sequence,title,emotion,confidence,act")
    for data in export_data[:5]:  # Show first 5
        print(f"   {data['sequence']},\"{data['title']}\",{data['emotion']},{data['confidence']:.2f},{data['act']}")
    print(f"   ... ({len(export_data)} total rows)")

    print("\n💡 This data can be imported into:")
    print("   - Excel / Google Sheets (for charts)")
    print("   - D3.js / Chart.js (for web visualization)")
    print("   - Tableau / Power BI (for analytics)")
    print("   - Custom dashboards")
    print()


def main():
    print("\n🎭 EMOTIONAL BEAT CLASSIFIER - BATCH PROCESSING\n")

    # Run all use cases
    use_case_batch_classification()
    use_case_emotional_landscape()
    use_case_act_structure_analysis()
    use_case_emotional_rhythm()
    use_case_emotional_progression()
    use_case_confidence_analysis()
    use_case_export_emotional_data()

    print("=" * 70)
    print("📊 SUMMARY")
    print("=" * 70)
    print("\n✅ Demonstrated emotional analysis:")
    print("   1. Batch classification of all beats")
    print("   2. Emotional landscape visualization")
    print("   3. Act structure analysis")
    print("   4. Rhythm and pacing patterns")
    print("   5. Emotional progression tracking")
    print("   6. Confidence score analysis")
    print("   7. Export for visualization tools")
    print("\n💡 The Classifier maps the emotional heartbeat of narratives")
    print()


if __name__ == "__main__":
    main()
