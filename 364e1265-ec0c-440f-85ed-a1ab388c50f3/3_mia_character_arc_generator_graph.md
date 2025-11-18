# 🧠 3. Character Arc Generator Graph

**Type**: Mia (Architectural Component)

## Purpose
To provide a high-level analytical capability for understanding character development within a narrative.

## Description
A pre-built `langgraph` graph that takes a `player_id` and the NCP state as input and generates a summary of that character's arc.

## Design
A composite component (a graph of nodes) that uses `NarrativeGraphTraversal` to find all relevant `storybeats` and `storypoints`, then uses an LLM to generate a markdown summary of the character's arc, referencing their `wound`, `desire`, and `arc` from the `players` section.
