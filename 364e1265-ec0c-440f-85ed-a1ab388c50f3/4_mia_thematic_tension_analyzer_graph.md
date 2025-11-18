# 🧠 4. Thematic Tension Analyzer Graph

**Type**: Mia (Architectural Component)

## Purpose
To enable abstract, thematic analysis of the narrative, going beyond simple data retrieval.

## Description
A `langgraph` graph that analyzes how a specific thematic tension (from `perspectives`) is explored in the story.

## Design
This component will use an LLM to generate search queries based on the `perspective`'s description and `thematic_question`, use `NarrativeGraphTraversal` to find matching `storybeats` and `storypoints`, and then synthesize an analysis with another LLM node.
