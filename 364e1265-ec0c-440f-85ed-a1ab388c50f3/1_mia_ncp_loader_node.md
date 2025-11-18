# 🧠 1. NCP Loader Node

**Type**: Mia (Architectural Component)

## Purpose
To load and validate the Narrative Context Protocol (NCP) data, preparing it for analysis within a `langgraph` workflow.

## Description
A `langgraph` node that takes a file path or URL to an NCP JSON file as input, reads, parses, and validates it against the NCP schema, and outputs a structured `StateGraph` object.

## Design
This will be the entry point for any NCP analysis graph. It ensures data integrity from the start. The node's state will contain the parsed NCP data, which will be passed to downstream nodes.
