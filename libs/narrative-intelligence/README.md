# 🧠🌸 LangGraph Narrative Intelligence Toolkit

A toolkit for analyzing narratives using the Narrative Context Protocol (NCP) within LangGraph workflows.

## Overview

This library provides LangGraph nodes and graphs for deep narrative analysis based on the Narrative Context Protocol. It includes both architectural components (Mia's domain) for data processing and analytical capabilities.

## Components

### 🧠 Mia's Architectural Components

1. **NCP Loader Node** - Load and validate NCP JSON data
2. **Narrative Graph Traversal Node** - Navigate and query the narrative graph
3. **Character Arc Generator Graph** - Analyze character development arcs
4. **Thematic Tension Analyzer Graph** - Explore thematic tensions in narratives
5. **Emotional Beat Classifier Node** - Classify emotional tones of story beats

## Installation

```bash
pip install langgraph-narrative-intelligence
```

## Usage

```python
from narrative_intelligence import NCPLoaderNode, CharacterArcGenerator

# Load NCP data
loader = NCPLoaderNode()
state = loader.load("path/to/ncp.json")

# Analyze character arc
arc_generator = CharacterArcGenerator()
character_arc = arc_generator.generate(state, player_id="protagonist_1")
```

## Development

This library is built on LangGraph and follows the Narrative Context Protocol specification.

**Session ID**: `364e1265-ec0c-440f-85ed-a1ab388c50f3`

## License

MIT
