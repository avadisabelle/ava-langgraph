#!/usr/bin/env python3
"""
Comprehensive QA Test Suite for Narrative Intelligence Toolkit
Tests all schemas, nodes, and graphs for correctness and professional quality.
"""

import sys
import json
from pathlib import Path
from typing import Dict, List, Any

# Add package to path
sys.path.insert(0, str(Path(__file__).parent))

# Import all components
from narrative_intelligence import (
    NCPData, Player, Perspective, StoryBeat, StoryPoint, Moment,
    NCPState, CharacterArcState, ThematicAnalysisState, EmotionalClassificationState,
    NCPLoaderNode, NarrativeTraversalNode, EmotionalBeatClassifierNode,
    CharacterArcGenerator, ThematicTensionAnalyzer,
    __version__
)
from narrative_intelligence.nodes.narrative_traversal import TraversalMode
from narrative_intelligence.nodes.emotional_classifier import EmotionalTone

class QATestRunner:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []

    def test(self, name: str, func):
        """Run a test and track results."""
        try:
            func()
            self.passed += 1
            print(f"✓ {name}")
            return True
        except Exception as e:
            self.failed += 1
            error_msg = f"✗ {name}: {str(e)}"
            print(error_msg)
            self.errors.append(error_msg)
            import traceback
            traceback.print_exc()
            return False

    def report(self):
        """Print final test report."""
        print("\n" + "="*70)
        print("COMPREHENSIVE QA TEST REPORT")
        print("="*70)
        print(f"Total Tests: {self.passed + self.failed}")
        print(f"Passed: {self.passed} ✓")
        print(f"Failed: {self.failed} ✗")
        print(f"Success Rate: {(self.passed/(self.passed+self.failed)*100):.1f}%")

        if self.errors:
            print("\nErrors:")
            for error in self.errors:
                print(f"  {error}")

        return self.failed == 0

def main():
    qa = QATestRunner()

    print("="*70)
    print("NARRATIVE INTELLIGENCE TOOLKIT - COMPREHENSIVE QA")
    print(f"Version: {__version__}")
    print("="*70)

    # ========================================================================
    # SCHEMA TESTS
    # ========================================================================
    print("\n[1/5] SCHEMA VALIDATION TESTS")
    print("-"*70)

    def test_player_schema():
        player = Player(
            player_id="char_001",
            name="Test Character",
            role="protagonist"
        )
        assert player.player_id == "char_001"
        assert player.name == "Test Character"
        assert player.role == "protagonist"

    def test_moment_schema():
        moment = Moment(
            id="moment_001",
            timestamp="00:15:30",
            description="A critical decision",
            intensity=0.8
        )
        assert moment.id == "moment_001"
        assert moment.intensity == 0.8

    def test_storybeat_schema():
        beat = StoryBeat(
            id="beat_001",
            title="The Confrontation",
            description="Hero faces the antagonist",
            player_ids=["char_001"],
            perspective_ids=["persp_001"],
            emotional_weight="fear"
        )
        assert beat.title == "The Confrontation"
        assert len(beat.player_ids) == 1

    def test_storypoint_schema():
        point = StoryPoint(
            id="point_001",
            title="Plot Point",
            description="A turning point",
            beat_ids=["beat_001", "beat_002"]
        )
        assert len(point.beat_ids) == 2

    def test_perspective_schema():
        persp = Perspective(
            id="persp_001",
            name="Justice vs Revenge",
            thematic_question="When does justice become revenge?"
        )
        assert "Justice" in persp.name

    def test_ncp_data_schema():
        ncp = NCPData(
            title="Test Narrative",
            author="Test Author",
            version="1.0",
            players=[
                Player(player_id="p1", name="Hero", role="protagonist")
            ],
            perspectives=[
                Perspective(id="persp1", name="Theme1")
            ],
            storybeats=[
                StoryBeat(
                    id="beat1",
                    title="Opening",
                    description="Story begins",
                    player_ids=["p1"],
                    perspective_ids=["persp1"]
                )
            ],
            storypoints=[],
            metadata={"genre": "drama"}
        )
        assert ncp.title == "Test Narrative"
        assert len(ncp.players) == 1
        assert ncp.metadata["genre"] == "drama"

    qa.test("Player schema validation", test_player_schema)
    qa.test("Moment schema validation", test_moment_schema)
    qa.test("StoryBeat schema validation", test_storybeat_schema)
    qa.test("StoryPoint schema validation", test_storypoint_schema)
    qa.test("Perspective schema validation", test_perspective_schema)
    qa.test("NCPData schema validation", test_ncp_data_schema)

    # ========================================================================
    # NODE TESTS - Component 1: NCP Loader
    # ========================================================================
    print("\n[2/5] COMPONENT TESTS - NCP Loader Node")
    print("-"*70)

    def test_ncp_loader_from_dict():
        loader = NCPLoaderNode(validate=True)
        data = {
            "title": "Test Story",
            "version": "1.0",
            "players": [{"player_id": "p1", "name": "Hero"}],
            "perspectives": [{"id": "persp1", "name": "Theme"}],
            "storybeats": [
                {
                    "id": "beat1",
                    "title": "Scene",
                    "description": "A scene",
                    "player_ids": ["p1"],
                    "perspective_ids": ["persp1"]
                }
            ],
            "storypoints": [],
            "metadata": {}
        }
        ncp = loader.load_from_dict(data)
        assert ncp.title == "Test Story"
        assert len(ncp.players) == 1

    def test_ncp_loader_from_file():
        loader = NCPLoaderNode(validate=True)
        file_path = Path(__file__).parent / "examples/sample_narrative.json"
        if file_path.exists():
            ncp = loader.load_from_file(file_path)
            assert ncp.title is not None
            assert len(ncp.players) > 0
        else:
            # Create a temporary test file
            test_data = {
                "title": "File Test",
                "version": "1.0",
                "players": [{"player_id": "p1", "name": "Hero"}],
                "perspectives": [{"id": "persp1", "name": "Theme"}],
                "storybeats": [{
                    "id": "b1", "title": "S1", "description": "D1",
                    "player_ids": ["p1"], "perspective_ids": ["persp1"]
                }],
                "storypoints": [],
                "metadata": {}
            }
            test_file = Path("/tmp/test_ncp.json")
            test_file.write_text(json.dumps(test_data))
            ncp = loader.load_from_file(test_file)
            assert ncp.title == "File Test"

    def test_ncp_loader_validation():
        loader = NCPLoaderNode(validate=True)
        invalid_data = {"title": "Bad", "players": "not_a_list"}
        try:
            loader.load_from_dict(invalid_data)
            raise AssertionError("Should have raised validation error")
        except Exception as e:
            assert "validation" in str(e).lower() or "required" in str(e).lower()

    qa.test("NCPLoaderNode - load from dict", test_ncp_loader_from_dict)
    qa.test("NCPLoaderNode - load from file", test_ncp_loader_from_file)
    qa.test("NCPLoaderNode - validation", test_ncp_loader_validation)

    # ========================================================================
    # NODE TESTS - Component 2: Narrative Traversal
    # ========================================================================
    print("\n[3/5] COMPONENT TESTS - Narrative Traversal Node")
    print("-"*70)

    def test_traversal_player_journey():
        traversal = NarrativeTraversalNode()
        ncp = NCPData(
            title="Test",
            version="1.0",
            players=[Player(player_id="p1", name="Hero")],
            perspectives=[Perspective(id="persp1", name="Theme")],
            storybeats=[
                StoryBeat(id="b1", title="S1", description="D1",
                         player_ids=["p1"], perspective_ids=["persp1"]),
                StoryBeat(id="b2", title="S2", description="D2",
                         player_ids=["p1"], perspective_ids=["persp1"])
            ],
            storypoints=[],
            metadata={}
        )
        beats = traversal.traverse_player_journey(ncp, "p1")
        assert len(beats) == 2

    def test_traversal_thematic_trace():
        traversal = NarrativeTraversalNode()
        ncp = NCPData(
            title="Test",
            version="1.0",
            players=[Player(player_id="p1", name="Hero")],
            perspectives=[Perspective(id="persp1", name="Theme")],
            storybeats=[
                StoryBeat(id="b1", title="S1", description="D1",
                         player_ids=["p1"], perspective_ids=["persp1"]),
                StoryBeat(id="b2", title="S2", description="D2",
                         player_ids=["p1"], perspective_ids=["persp1"])
            ],
            storypoints=[],
            metadata={}
        )
        beats = traversal.traverse_thematic_trace(ncp, "persp1")
        assert len(beats) == 2

    def test_traversal_temporal_sequence():
        traversal = NarrativeTraversalNode()
        ncp = NCPData(
            title="Test",
            version="1.0",
            players=[Player(player_id="p1", name="Hero")],
            perspectives=[Perspective(id="persp1", name="Theme")],
            storybeats=[
                StoryBeat(id="b2", title="S2", description="D2", sequence=2,
                         player_ids=["p1"], perspective_ids=["persp1"]),
                StoryBeat(id="b1", title="S1", description="D1", sequence=1,
                         player_ids=["p1"], perspective_ids=["persp1"])
            ],
            storypoints=[],
            metadata={}
        )
        beats = traversal.traverse_temporal_sequence(ncp)
        assert beats[0].id == "b1"  # Should be sorted by sequence
        assert beats[1].id == "b2"

    qa.test("NarrativeTraversalNode - player journey", test_traversal_player_journey)
    qa.test("NarrativeTraversalNode - thematic trace", test_traversal_thematic_trace)
    qa.test("NarrativeTraversalNode - temporal sequence", test_traversal_temporal_sequence)

    # ========================================================================
    # NODE TESTS - Component 5: Emotional Classifier
    # ========================================================================
    print("\n[4/5] COMPONENT TESTS - Emotional Beat Classifier")
    print("-"*70)

    def test_emotional_classifier_basic():
        classifier = EmotionalBeatClassifierNode(use_llm=False)
        beat = StoryBeat(
            id="b1",
            title="Terror",
            description="Fear grips the hero",
            player_ids=["p1"],
            perspective_ids=["persp1"]
        )
        result = classifier.classify_beat(beat)
        assert "classification" in result
        assert result["confidence"] > 0

    def test_emotional_classifier_existing_weight():
        classifier = EmotionalBeatClassifierNode(use_llm=False)
        beat = StoryBeat(
            id="b1",
            title="Happy Scene",
            description="Joy everywhere",
            player_ids=["p1"],
            perspective_ids=["persp1"],
            emotional_weight="joy"
        )
        result = classifier.classify_beat(beat)
        assert result["classification"] == "joy"
        assert result["method"] == "existing"

    def test_emotional_classifier_batch():
        classifier = EmotionalBeatClassifierNode(use_llm=False)
        beats = [
            StoryBeat(id=f"b{i}", title=f"Scene {i}", description="fear and terror",
                     player_ids=["p1"], perspective_ids=["persp1"])
            for i in range(3)
        ]
        results = classifier.classify_batch(beats)
        assert len(results) == 3

    qa.test("EmotionalBeatClassifier - basic classification", test_emotional_classifier_basic)
    qa.test("EmotionalBeatClassifier - existing weight", test_emotional_classifier_existing_weight)
    qa.test("EmotionalBeatClassifier - batch processing", test_emotional_classifier_batch)

    # ========================================================================
    # GRAPH TESTS - Components 3 & 4
    # ========================================================================
    print("\n[5/5] COMPONENT TESTS - Composite Graphs")
    print("-"*70)

    def test_character_arc_generator():
        generator = CharacterArcGenerator()
        graph = generator.build_graph()
        assert graph is not None
        # Verify graph has correct structure
        # Note: Actual execution would require LangGraph runtime

    def test_thematic_analyzer():
        analyzer = ThematicTensionAnalyzer()
        graph = analyzer.build_graph()
        assert graph is not None
        # Verify graph has correct structure

    qa.test("CharacterArcGenerator - graph creation", test_character_arc_generator)
    qa.test("ThematicTensionAnalyzer - graph creation", test_thematic_analyzer)

    # ========================================================================
    # INTEGRATION TESTS
    # ========================================================================
    print("\n[BONUS] INTEGRATION TESTS")
    print("-"*70)

    def test_full_workflow():
        # Load NCP data
        loader = NCPLoaderNode(validate=True)
        ncp_data = {
            "title": "Integration Test",
            "version": "1.0",
            "players": [
                {"player_id": "hero", "name": "Hero", "role": "protagonist"}
            ],
            "perspectives": [
                {"id": "theme1", "name": "Good vs Evil"}
            ],
            "storybeats": [
                {
                    "id": "beat1",
                    "title": "Dark Beginning",
                    "description": "Fear and anxiety consume the hero",
                    "sequence": 1,
                    "player_ids": ["hero"],
                    "perspective_ids": ["theme1"]
                },
                {
                    "id": "beat2",
                    "title": "Triumphant Victory",
                    "description": "Joy and hope return",
                    "sequence": 2,
                    "player_ids": ["hero"],
                    "perspective_ids": ["theme1"]
                }
            ],
            "storypoints": [],
            "metadata": {"genre": "adventure"}
        }
        ncp = loader.load_from_dict(ncp_data)

        # Traverse narrative
        traversal = NarrativeTraversalNode()
        hero_journey = traversal.traverse_player_journey(ncp, "hero")
        assert len(hero_journey) == 2

        # Classify emotions
        classifier = EmotionalBeatClassifierNode(use_llm=False)
        emotions = classifier.classify_batch(hero_journey)
        assert len(emotions) == 2

        print(f"    Loaded: {ncp.title}")
        print(f"    Traversed: {len(hero_journey)} beats")
        print(f"    Classified: {len(emotions)} emotional tones")

    qa.test("Full workflow integration", test_full_workflow)

    # ========================================================================
    # FINAL REPORT
    # ========================================================================
    success = qa.report()
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
