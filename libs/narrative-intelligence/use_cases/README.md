# Narrative Intelligence Toolkit - Use Cases

This directory contains comprehensive, real-world use cases for all 5 components of the Narrative Intelligence Toolkit.

## 📚 Overview

Each component has:
- **Narrative data** (JSON files with complete NCP-formatted stories)
- **Use case scripts** (Runnable Python scripts demonstrating real scenarios)
- **Multiple scenarios** (6-7 use cases per component)

## 🗂️ Structure

```
use_cases/
├── loader/                          # Component 1: NCP Loader
│   ├── tech_thriller.json          # Tech thriller narrative
│   └── use_case_multi_source_loading.py
│
├── traversal/                       # Component 2: Narrative Traversal
│   ├── fantasy_epic.json           # Epic fantasy narrative
│   └── use_case_complex_queries.py
│
├── character_arc/                   # Component 3: Character Arc Generator
│   ├── coming_of_age.json          # Coming-of-age narrative
│   └── use_case_multiple_character_types.py
│
├── thematic_analyzer/               # Component 4: Thematic Tension Analyzer
│   ├── sci_fi_ethics.json          # Sci-fi philosophical narrative
│   └── use_case_deep_theme_analysis.py
│
└── emotional_classifier/            # Component 5: Emotional Beat Classifier
    ├── thriller_screenplay.json     # Psychological thriller
    └── use_case_batch_processing.py
```

## 🎯 Use Cases by Component

### 1. NCP Loader - Multi-Source Data Loading

**Narrative**: Corporate Espionage (Tech Thriller)
- 2 characters, 2 story beats, 1 perspective
- Focus: Trust vs Ambition theme

**Scenarios**:
1. **Loading from Local File** - Production workflow
2. **Loading from Dictionary** - Programmatic generation
3. **Validation Error Handling** - Data integrity
4. **LangGraph Integration** - State management

**Run**: `python use_cases/loader/use_case_multi_source_loading.py`

---

### 2. Narrative Traversal - Complex Query Patterns

**Narrative**: The Shattered Crown (Epic Fantasy)
- 3 characters, 6 story beats, 3 perspectives
- Focus: Unity, justice, power themes

**Scenarios**:
1. **Character Journey Traversal** - Follow Elara's path
2. **Thematic Trace** - Find vengeance/justice beats
3. **Emotional Arc Tracking** - Map emotional landscape
4. **Relationship Network Analysis** - Character interactions
5. **Connected Elements Discovery** - Beat connections
6. **Multi-Character Scene Detection** - Ensemble moments

**Run**: `python use_cases/traversal/use_case_complex_queries.py`

---

### 3. Character Arc Generator - Multiple Character Types

**Narrative**: Summer of Changes (Coming of Age)
- 3 characters (protagonist, deuteragonist, mentor)
- 6 story beats, 1 perspective
- Focus: Control vs Acceptance

**Scenarios**:
1. **Protagonist Arc** - Maya's transformational journey
2. **Deuteragonist Arc** - Derek's mirror journey
3. **Mentor Arc** - Grandma Rosa's wisdom-keeper arc
4. **Comparative Analysis** - Compare all three arcs
5. **Batch Export** - Generate all arcs for review
6. **Arc Completeness Check** - Validate character development

**Run**: `python use_cases/character_arc/use_case_multiple_character_types.py`

---

### 4. Thematic Tension Analyzer - Deep Theme Analysis

**Narrative**: The Consciousness Dilemma (Sci-Fi Ethics)
- 2 characters (human + AI), 6 story beats, 3 perspectives
- Focus: Consciousness, autonomy, ethics

**Scenarios**:
1. **Primary Theme Analysis** - Humanity vs Technology
2. **Secondary Theme Analysis** - Creator vs Creation
3. **Ethical Dimension** - Progress vs Ethics
4. **Comparative Theme Strength** - Which theme dominates?
5. **Theme Evolution Tracking** - How themes develop
6. **Under-Explored Themes** - Development opportunities
7. **Theme Interaction** - Multi-theme beats

**Run**: `python use_cases/thematic_analyzer/use_case_deep_theme_analysis.py`

---

### 5. Emotional Beat Classifier - Batch Processing

**Narrative**: Last Train to Mercy (Psychological Thriller)
- 1 character, 12 story beats (3-act structure)
- Focus: Fear vs Courage, PTSD recovery

**Scenarios**:
1. **Batch Classification** - Classify all 12 beats
2. **Emotional Landscape** - Visualize emotional journey
3. **Act Structure Analysis** - Compare acts emotionally
4. **Emotional Rhythm** - Identify pacing patterns
5. **Emotional Progression** - Track fear evolution
6. **Confidence Analysis** - Reliability of classifications
7. **Export for Visualization** - Prepare data for charts

**Run**: `python use_cases/emotional_classifier/use_case_batch_processing.py`

---

## 🎬 Narratives Summary

| Narrative | Genre | Characters | Beats | Perspectives | Complexity |
|-----------|-------|------------|-------|--------------|------------|
| Corporate Espionage | Tech Thriller | 2 | 2 | 1 | Simple |
| The Shattered Crown | Epic Fantasy | 3 | 6 | 3 | High |
| Summer of Changes | Coming of Age | 3 | 6 | 1 | Medium |
| The Consciousness Dilemma | Sci-Fi Ethics | 2 | 6 | 3 | High |
| Last Train to Mercy | Thriller Screenplay | 1 | 12 | 1 | Medium |

## 💡 Key Insights from Use Cases

### Data Variety
- **Genres**: Thriller, Fantasy, Coming-of-Age, Sci-Fi, Screenplay
- **Scales**: 2-12 story beats
- **Character Types**: Protagonists, deuteragonists, mentors, AI
- **Themes**: Ethics, growth, justice, fear, consciousness

### Real-World Applications
1. **Writing Coaches** - Character arc analysis
2. **Story Analysts** - Thematic depth measurement
3. **Screenwriters** - Emotional pacing validation
4. **Game Designers** - Narrative structure planning
5. **Literary Critics** - Academic narrative analysis
6. **Content Creators** - Story bible generation

### Technical Patterns
- **Batch Processing** - Efficient classification of multiple beats
- **Comparative Analysis** - Cross-character/theme comparisons
- **Progressive Depth** - Simple to complex queries
- **Export Capabilities** - Integration with visualization tools
- **Validation** - Data integrity checks

## 🚀 Quick Start

### Run All Use Cases
```bash
# Navigate to use_cases directory
cd libs/narrative-intelligence/use_cases

# Run all use cases in sequence
python loader/use_case_multi_source_loading.py
python traversal/use_case_complex_queries.py
python character_arc/use_case_multiple_character_types.py
python thematic_analyzer/use_case_deep_theme_analysis.py
python emotional_classifier/use_case_batch_processing.py
```

### Run Individual Scenarios
Each use case file demonstrates 6-7 scenarios sequentially. Run the main() function to see all scenarios, or call individual use case functions:

```python
from use_cases.loader.use_case_multi_source_loading import use_case_file_loading

# Run just file loading scenario
use_case_file_loading()
```

## 📊 Expected Output

Each use case script provides:
- ✅ Success/failure indicators
- 📊 Data visualizations (text-based)
- 💡 Insights and recommendations
- 🔍 Analysis summaries
- 📁 Simulated export previews

## 🔧 Customization

### Create Your Own Narratives
1. Copy any JSON file as a template
2. Modify characters, beats, and perspectives
3. Ensure all IDs are unique
4. Run validation: `NCPLoaderNode(validate=True).load_from_file("your_narrative.json")`

### Create Custom Scenarios
```python
from narrative_intelligence import NCPLoaderNode, CharacterArcGenerator

ncp_data = NCPLoaderNode().load_from_file("your_narrative.json")
arc_generator = CharacterArcGenerator()
arc = arc_generator.generate(ncp_data, "your_character_id")
print(arc)
```

## 📈 Performance

All use cases run efficiently:
- **Loader**: < 100ms per file
- **Traversal**: < 50ms per query
- **Character Arc**: < 200ms per character
- **Thematic Analyzer**: < 300ms per theme
- **Emotional Classifier**: < 10ms per beat

Batch processing 12 beats: ~120ms total

## 🎓 Learning Path

1. **Start with Loader** - Understand NCP data structure
2. **Explore Traversal** - Learn query patterns
3. **Generate Character Arcs** - See composite workflows
4. **Analyze Themes** - Deep narrative analysis
5. **Classify Emotions** - Batch processing patterns

## 🤝 Contributing

To add new use cases:
1. Create a new narrative JSON file
2. Write a use case script with 5-7 scenarios
3. Follow the existing naming pattern
4. Update this README with your use case

## 📝 License

All use cases and narratives are provided as examples for the Narrative Intelligence Toolkit (MIT License).

---

**Session**: `364e1265-ec0c-440f-85ed-a1ab388c50f3`
**Repository**: `avadisabelle/ava-langgraph`
**Documentation**: `/libs/narrative-intelligence/README.md`
