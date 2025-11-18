# 🌸 7. Thematic Resonance Explorer

**Type**: Miette (User Experience Component)

## Purpose
To feel like using a magical lens to see the invisible currents of meaning that flow through the story, revealing how a single idea echoes in many different moments.

## Description
A component that uses the `ThematicTensionAnalyzer` graph. A user could select a `perspective` like "Safety vs Vulnerability," and the component would highlight all the `storybeats` and `moments` in the story that resonate with that theme, creating a "thematic map" of the narrative.

## Design
This component will be a custom node in `langflow` that takes a `perspective_id` as input and outputs a list of thematically relevant `storybeat_ids` and `moment_ids`. A separate rendering component will then use this list to highlight the corresponding elements in the main story view, perhaps by changing their color or adding a glowing effect.
