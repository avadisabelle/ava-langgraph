# 🌸 8. Emotional Landscape Visualizer

**Type**: Miette (User Experience Component)

## Purpose
To be like seeing the story's EKG, feeling its heartbeat, and understanding the rhythm of its emotional life.

## Description
A component that runs the `EmotionalBeatClassifier` on all the `storybeats` and then generates a visual "emotional landscape" of the story—a graph showing the journey from devastation to hope, from tension to relief.

## Design
This component will be a `langflow` custom node that triggers a batch process (running the `EmotionalBeatClassifier` `langgraph` on all `storybeats`). The output will be a data structure (e.g., a JSON array) containing the emotional classifications for each beat. A separate UI component (e.g., a chart or a timeline) will then render this data, showing the emotional ebb and flow of the story over time.
