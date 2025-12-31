# Narrative Intelligence Toolkit - Examples

This directory contains examples demonstrating how to use the Narrative Intelligence Toolkit.

## Files

- **`sample_narrative.json`** - An example NCP-formatted narrative about Sarah's journey to find belonging
- **`usage_example.py`** - Demonstrates all 5 core components

## Running the Example

```bash
cd libs/narrative-intelligence/examples
python usage_example.py
```

## What the Example Demonstrates

### 1. NCP Loader Node
Loads and validates the sample narrative JSON file.

### 2. Narrative Traversal Node
- Finds all story beats involving a specific character
- Searches for beats exploring a specific theme

### 3. Character Arc Generator
Generates a complete markdown summary of Sarah's character arc, including:
- Character foundation (wound, desire, arc)
- Journey through story beats
- Character transformation

### 4. Thematic Tension Analyzer
Analyzes how "Safety vs Vulnerability" manifests in the narrative:
- Generates search queries from the perspective
- Finds all relevant story beats
- Synthesizes thematic insights

### 5. Emotional Beat Classifier
Classifies the emotional tone of each story beat using:
- Rule-based keyword matching
- Confidence scoring
- Extensible for LLM-based classification

## Sample Output

The example will generate:
- Character arc markdown document
- Thematic analysis report
- Emotional classifications for all beats

## Next Steps

After running the example, you can:
1. Modify `sample_narrative.json` to create your own narratives
2. Experiment with different characters and themes
3. Integrate with LangFlow for visual components
4. Add LLM support for more sophisticated analysis
