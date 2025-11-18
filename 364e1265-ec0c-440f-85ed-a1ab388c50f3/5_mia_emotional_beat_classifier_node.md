# 🧠 5. Emotional Beat Classifier Node

**Type**: Mia (Architectural Component)

## Purpose
To enrich the narrative graph with emotional metadata, enabling new forms of analysis and visualization.

## Description
A `langgraph` node that takes a `storybeat` object as input and classifies its emotional tone.

## Design
This node will use an LLM with a specific prompt and a classification head to label the `emotional_weight` of a beat (e.g., "Devastating," "Hopeful," "Tense"). The existing `emotional_weight` field in the example could be used as training data or as a validation mechanism.
