# 🌟 UNIFIED MISSION: Narrative Intelligence Stack Integration (2025-12-31)

## Executive Overview

This mission unifies **six interrelated projects** into a cohesive stack:

### Core Stack
1. **Narrative Intelligence Toolkit** (LangGraph) - Narrative analysis & NCP protocol implementation
2. **Agentic Flywheel** (Flowise + MCP) - Dynamic agent coordination & flow management  
3. **Storytelling System** (LangGraph) - Story generation with RAG & ceremonial diary
4. **LangChain Integration** - Langfuse tracing across the entire stack

### Extended Stack (NEW)
5. **ava-langflow** - Universal multi-backend router (Flowise + Langflow + future backends)
6. **Miadi-46 Platform** - GitHub webhook event-driven architecture, ultimate consumer

### The Vision: Three Universes (from Multiverse 3-Act)
- **Engineer World** (Mia) - Technical precision, structural integrity, API schemas
- **Ceremony World** (Ava8) - Indigenous relational protocols, sacred technology
- **Story Engine World** (Miette) - Narrative structure, story beats, plot coherence

Every GitHub webhook becomes a narrative event, processed through all three lenses.

**Status**: Phase 1 COMPLETE, Phase 2 IN PROGRESS
**Session ID**: `364e1265-ec0c-440f-85ed-a1ab388c50f3`

---

## 🏗️ Current State of Components

### 1. **LangGraph: Narrative Intelligence Toolkit** ✅ 100% Phase 1 + Phase 2 Starting
📍 Location: `/workspace/langgraph/libs/narrative-intelligence/`

**What's implemented:**
- ✅ **NCP Schema Models** - Complete Narrative Context Protocol data structures
  - Player, Perspective, StoryBeat, StoryPoint, Moment models
  - State management (CharacterArcState, ThematicAnalysisState, EmotionalClassificationState)
  
- ✅ **Core Nodes**:
  - `NCPLoaderNode` - Load & validate NCP JSON data
  - `NarrativeTraversalNode` - Query narrative graphs with multiple traversal modes
  - `EmotionalBeatClassifierNode` - Classify emotional tones of beats

- ✅ **Narrative Graphs**:
  - `CharacterArcGenerator` - Analyze character development across story
  - `ThematicTensionAnalyzer` - Extract thematic tensions & conflicts
  - **`ThreeUniverseProcessor`** - Process events through all 3 universe lenses
  - **`NarrativeCoherenceEngine`** - Gap identification, coherence scoring, Trinity assessment (NEW!)

- ✅ **Use Cases & Examples** - 5 comprehensive use cases with batch processing, multi-source loading, etc.

- ✅ **Unified State Bridge** (Session 364e1265):
  - `unified_state_bridge.py` - THE CONTRACT for all 6 systems (736 lines)
  - Three-universe types (Engineer/Mia, Ceremony/Ava8, Story-Engine/Miette)
  - NarrativePosition, StoryBeat, CharacterState, ThematicThread
  - Complete JSON/Redis serialization

- ✅ **Redis Integration**:
  - `redis_state.py` - Redis-backed state persistence (701 lines)
  - Beat storage, event analysis caching, routing decision history
  - Mock Redis for development/testing

- ✅ **Checkpoint Integration**:
  - `narrative_checkpointer.py` - LangGraph checkpoint wrapper (607 lines)
  - Narrative-aware metadata extraction
  - Cross-session coherence tracking (for Miadi-46)
  - Act transition and episode boundary detection

- ✅ **Three-Universe Processor**:
  - `three_universe_processor.py` - Full LangGraph graph (930+ lines)
  - Engineer World analysis (Mia - technical intent)
  - Ceremony World analysis (Ava8 - relational intent)
  - Story Engine World analysis (Miette - narrative function)
  - Lead universe determination and coherence scoring
  - Beat creation from webhook events

- ✅ **NarrativeCoherenceEngine** (NEW - Phase 2):
  - `coherence_engine.py` - Gap identification and quality scoring (800+ lines)
  - Gap types: structural, thematic, character, sensory, continuity
  - Coherence scoring: narrative flow, character consistency, pacing, theme saturation, continuity
  - Routing suggestions to appropriate tools (Storyteller, Structurist, Architect, Author)
  - **Trinity Assessment** (Mia/Miette/Ava8 perspectives)
  - Full LangGraph workflow

- ✅ **Working Examples**:
  - `webhook_to_beat_example.py` - Complete webhook → 3-universe → beat pipeline

**Tests**: 124 passing
  - unified_state_bridge: 32 tests
  - redis_state: 15 tests  
  - narrative_checkpointer: 25 tests
  - three_universe_processor: 26 tests
  - coherence_engine: 26 tests (NEW!)

**What's incomplete:**
- ⚠️ **Integration with ava-langflow** - State bridge ready, handler not yet created
- ⚠️ **Langfuse tracing integration** - Ready in LangChain, needs wiring

---

### 2. **LangGraph: Storytelling System** ✅ ~75% Complete
📍 Location: `/src/storytelling/`

**What's implemented:**
- ✅ **Story Generation Engine** - Graph-based with RAG integration
  - 3 Indigenous-inspired prompts (Spiral of Memory, Two-Eyed Seeing, Dream Architect)
  - Session management with checkpoint/resume capability
  - Knowledge base integration with semantic search

- ✅ **COAIA Fusion** - Combines narrative context with ceremonial practices
  - Ceremonial diary for tracking story generation rituals
  - IAIP bridge for relational science integration
  - Context extraction and fusion logic

- ✅ **CLI Interface** - Rich command-line tool with multiple providers
  - Ollama, Google Gemini, OpenRouter support
  - Debug mode with detailed logging

**What's incomplete/superficial:**
- ⚠️ **Narrative Intelligence Toolkit integration** - Uses generic prompts, not NCP-driven analysis
- ⚠️ **Emotional beat classification** - Doesn't analyze generated stories for emotional arcs
- ⚠️ **Character trajectory tracking** - No persistent character state across generations
- ⚠️ **Agentic feedback loop** - Stories generated but not fed back to agents

**Key Files**:
- `graph.py` - Main story generation graph (55KB - comprehensive)
- `coaia_fuse.py` - Narrative + ceremonial integration
- `enhanced_rag.py` - Knowledge base retrieval with semantic search
- `prompts.py` - 29KB of sophisticated narrative prompts

---

### 3. **Flowise + Agentic Flywheel** ⚠️ ~60% Complete
📍 Location: `/workspace/ava-Flowise/` & `/cesaret/src/agentic_flywheel/`

**What's implemented:**
- ✅ **Flow Registry System** - Dynamic Flowise flow management
  - YAML-based flow registry with cascading configuration loading
  - Flow metadata, keywords, intent classification
  
- ✅ **FlowiseManager** - Central abstraction layer
  - Intelligent query routing based on intent classification
  - Dynamic parameter adjustment (temperature, maxOutputTokens)
  - Session ID generation for conversation continuity

- ✅ **MCP Server Integration**
  - `mcp_server.py` - Foundational MCP server exposing Flowise as tools
  - `intelligent_mcp_server.py` - Enhanced with admin layer intelligence
  - Tool registration and resource discovery

- ✅ **Admin Layer** - Flow analysis & configuration sync
  - Database interface for Flowise backend
  - Flow analyzer for capability detection

**What's incomplete/superficial:**
- ❌ **LangGraph integration** - MCP tools not wired to LangGraph nodes
- ❌ **Narrative awareness** - Flows don't understand NCP structures
- ❌ **State management** - Session continuity not connected to narrative state
- ⚠️ **Testing** - Basic functionality works but complex routing untested

**Why it partially failed in cesaret**:
- Flowise backend integration was incomplete (database schema mismatches)
- MCP server specs were drafted but not fully connected to flow execution
- Intent classification too simplistic for narrative domains
- No clear bridge to LangGraph narrative state

---

### 4. **LangChain: Langfuse Tracing** ✅ ~85% Complete
📍 Location: `/workspace/langchain/`

**What's implemented:**
- ✅ **Langfuse Handler** - Full integration for LangChain callbacks
  - Trace creation, span management, custom events
  - Metadata tracking and cost calculation
  
- ✅ **Environment Setup** - Integration in launch scripts
  - Langfuse API key configuration
  - Base URL and project settings

**What's incomplete:**
- ❌ **Multi-stack tracing** - Doesn't trace across LangGraph → Flowise → LangChain
- ❌ **Narrative event recording** - No NCP-specific events in traces
- ⚠️ **Real-time visualization** - Traces generated but not connected to story progress

---

### 5. **ava-langflow: Universal Multi-Backend Router** ✅ ~70% Complete (NEW)
📍 Location: `/workspace/ava-langflow/`

**What's implemented:**
- ✅ **Universal Backend Abstraction** - Flowise + Langflow + extensible
  - `routing/router.py` - Intelligent backend selection (15KB comprehensive)
  - Performance tracking with historical metrics
  - Health-based routing decisions

- ✅ **Langfuse Creative Archaeology Tracer** (27KB!)
  - Decorator-based tracing (`@trace_mcp_tool`)
  - Structured observations for decision points
  - Performance and quality scoring
  - Fail-safe design (tracing never breaks tools)

- ✅ **Redis State Integration**
  - `integrations/redis_state.py` - Session state persistence
  - Cross-request state management
  - Integration with Miadi-46 Redis patterns

- ✅ **Cross-Instance Coordination**
  - Platform consolidation plan documented
  - Integration with all 4 forks (langchain, langgraph, ava-Flowise)

**What's incomplete:**
- ⚠️ **Narrative-aware routing** - Routes based on intent, not story position
- ⚠️ **Three-universe processing** - Single-lens currently (Engineer World)
- ⚠️ **Webhook event consumption** - Not yet integrated with Miadi-46

**Key Files**:
- `src/agentic_flywheel/routing/router.py` - Universal query router
- `src/agentic_flywheel/integrations/langfuse_tracer.py` - Creative archaeology
- `src/agentic_flywheel/integrations/redis_state.py` - State persistence
- `CROSS_INSTANCE_COORDINATION.md` - Platform integration plan

---

### 6. **Miadi-46: GitHub Webhook Event-Driven Platform** ✅ ~80% Complete (NEW)
📍 Location: `/src/Miadi-46/`

**What's implemented:**
- ✅ **Webhook ETL Pipeline**
  - GitHub webhook receiver (`app/api/hooks/`)
  - Event transformation to agent-friendly format
  - Redis storage with structured keys
  - Queue-based processing

- ✅ **Local Hook System** (analogous to `.git/hooks/`)
  - `.github-hooks/issues` - Triggered on issue events
  - `.github-hooks/push` - Triggered on push events
  - Environment variables passed to hooks (WEBHOOK_EVENT_TYPE, etc.)
  - Stdin payload for full context

- ✅ **Live Story Monitor API**
  - `app/api/live-story-monitor/` - Real-time narrative interfaces
  - Scene streaming, archive management
  - Context stream for narrative state

- ✅ **Multiverse 3-Act Narrative Framework** 
  - Episodes with NCP structure (`episodes/s01e01-pilot.ncp.json`)
  - Three-universe perspective system
  - Character archetypes (Mia/Builder, Ava8/Keeper, Miette/Weaver)
  - Full NCP schema in `schema/ncp-schema.json`

- ✅ **Session Management**
  - Multi-agent session tracking
  - NewSessionUUID handler
  - Cross-session coherence

**What's incomplete:**
- ⚠️ **NCP analysis pipeline** - Schema defined but not applied to new events
- ⚠️ **Three-universe validation** - Single-lens processing currently
- ⚠️ **Ceremonial protocol implementation** - Framework documented, not operationalized
- ⚠️ **Story Engine integration** - Not connected to storytelling system

**Key Files**:
- `stories/multiverse_3act_2512012121/` - Complete multiverse framework
- `stories/multiverse_3act_2512012121/schema/ncp-schema.json` - NCP definition
- `WEBHOOK_HOOKS.md` - Hook system documentation
- `.github-hooks/` - Executable hook scripts

---

## 🎯 THE INTEGRATION MISSION: What Needs to Be Built

### **The Three-Universe Event Flow** (NEW VISION)

Every GitHub webhook flows through three interpretive lenses:

```
┌──────────────────────────────────────────────────────────────────────────┐
│                     GitHub Webhook Event                                 │
│  (Issue opened, PR created, Push, Comment, etc.)                        │
└────────────────────────────────┬─────────────────────────────────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │     Miadi-46 ETL        │
                    │   (Webhook receiver)    │
                    └────────────┬────────────┘
                                 │
         ┌───────────────────────┼───────────────────────┐
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐
│  ENGINEER WORLD │   │  CEREMONY WORLD │   │ STORY ENGINE    │
│     (Mia)       │   │     (Ava8)      │   │    (Miette)     │
│                 │   │                 │   │                 │
│ - Technical     │   │ - Relational    │   │ - Narrative     │
│   schema        │   │   accountability│   │   function      │
│ - API structure │   │ - Sacred pause  │   │ - Act position  │
│ - Build status  │   │ - K'é mapping   │   │ - Character arc │
│ - Flow routing  │   │ - 7-generation  │   │ - Plot coherence│
└────────┬────────┘   └────────┬────────┘   └────────┬────────┘
         │                     │                     │
         └─────────────────────┼─────────────────────┘
                               │
                    ┌──────────▼──────────┐
                    │  Unified Narrative  │
                    │       State         │
                    │ (NCP + All 3 views) │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
     ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
     │  ava-lang   │  │  Narrative  │  │ Storytelling│
     │   flow      │  │Intelligence │  │   System    │
     │  (Router)   │  │  (Analysis) │  │ (Generator) │
     └─────────────┘  └─────────────┘  └─────────────┘
              │                │                │
              └────────────────┼────────────────┘
                               │
                    ┌──────────▼──────────┐
                    │    Langfuse Trace   │
                    │ (Complete journey)  │
                    └─────────────────────┘
```

### **Phase 1: Unified State Bridge** (Priority 1 - Foundation)
**Goal**: Make all six systems aware of each other's state

```
┌───────────────────────────────────────────────────────────────┐
│               Unified Narrative State Bridge                  │
│     (NCP + Story State + 3-Universe + Webhook Events)        │
└──────────────────────────────┬────────────────────────────────┘
                               │
    ┌──────────┬───────────┬───┴───┬───────────┬───────────┐
    │          │           │       │           │           │
┌───▼──┐  ┌───▼───┐  ┌────▼──┐  ┌─▼──┐  ┌────▼────┐  ┌───▼───┐
│Story │  │  NCP  │  │ Agent │  │Trace│ │ava-lang │  │Miadi  │
│Graph │  │ Anal  │  │ Flow  │  │ Log │ │  flow   │  │ -46   │
└──────┘  └───────┘  └───────┘  └────┘  └─────────┘  └───────┘
```

**Deliverables**:
1. **Shared State Model** (`unified_state_bridge.py`)
   - Extends NCP data with agent flow metadata
   - Tracks story generation + agent decisions + analytical insights
   - **NEW**: Includes 3-universe perspective tracking
   - **NEW**: Integrates with Redis for Miadi-46 compatibility
   - Serializable for checkpointing

2. **Webhook Event Integration** (NEW)
   - Bridge GitHub webhooks to narrative events
   - Transform `issues.opened` → `StoryBeat` with perspective metadata
   - Track which universe(s) processed each event
   - Example: Issue #110 = Inciting Incident in Story Engine World

3. **Checkpoint Integration**
   - Use LangGraph checkpoint saver to persist narrative state
   - **NEW**: Redis-backed for Miadi-46 compatibility
   - Enable mid-story intervention by agents
   - Resume narratives with full context recovery

4. **Three-Universe Event Classifier** (NEW)
   - Each event gets 3 interpretations (Engineer, Ceremony, Story)
   - Classify which universe should "lead" response
   - Track cross-universe coherence

### **Phase 2: Narrative-Aware Agents** (Priority 2 - Intelligence)
**Goal**: Make agents (Flowise, Langflow) understand and respect narrative structure

**Deliverables**:
1. **Narrative Intent Classification** (`narrative_intent_classifier.py`)
   - Move beyond keywords to NCP-aware intent
   - Example: "Is this agent adding tension or resolution?"
   - Route flows based on narrative position (setup, crisis, resolution)
   - **NEW**: Classify intent per-universe (Mia sees technical, Miette sees story)

2. **Context Injection for Flows**
   - Inject current narrative state into Flowise/Langflow queries
   - Example: "Given this character's arc so far, suggest next dialogue"
   - Personality-aware response generation
   - **NEW**: Include universe-specific context (which lens is active?)

3. **Story-Responsive Flow Registry** (ava-langflow integration)
   - Dynamic flow activation based on story needs
   - Example: If character needs antagonist challenge → activate conflict resolver flow
   - If emotional beat needed → activate emotional deepener flow
   - **NEW**: Route to appropriate backend (Flowise vs Langflow) based on capability

### **Phase 3: Story Intelligence Loop** (Priority 3 - Integration)
**Goal**: Close the loop - stories learn from agent analysis

**Deliverables**:
1. **Analytical Feedback Loop**
   ```
   Story Generated → NCP Analysis → Gaps Identified → 
   Agent Routes to Specialist Flow → Enriched Story → Updated Analysis
   ```

2. **Emotional Beat Optimization**
   - Classifier identifies weak emotional moments
   - Routes to sentiment enhancer flow
   - Regenerates scene with stronger emotional resonance

3. **Character Arc Coherence Checker**
   - Analyzes character development across generated story
   - Routes to character consistency checker when inconsistencies found
   - Suggests dialogue/action modifications for arc alignment

### **Phase 4: Unified Tracing** (Priority 4 - Observability)
**Goal**: Complete end-to-end visibility across the stack

**Deliverables**:
1. **Instrumentation**
   - NCP analysis events logged to Langfuse
   - Flowise/Langflow execution traced with span nesting
   - Story generation traced with emotional beat markers
   - **NEW**: Webhook events traced from GitHub → processing → response

2. **Narrative Trace Format**
   - Custom Langfuse event types for narrative concepts
   - Character perspective spans
   - Theme tension tracking in trace hierarchy
   - **NEW**: Three-universe decision spans (which universe led?)

3. **Live Story Monitor** (connects to Miadi-46)
   - Real-time trace viewer showing narrative generation
   - Visual representation of character arcs, themes, emotional beats
   - Agent decisions overlaid on story progress
   - **NEW**: Webhook event stream visualization

---

### **Phase 5: Event-Driven Integration** (Priority 5 - Platform) (NEW)
**Goal**: Connect the Narrative Intelligence Stack to Miadi-46's webhook architecture

**Deliverables**:
1. **Webhook → Narrative Event Bridge**
   - Transform GitHub events into narrative beats
   - Apply three-universe classification
   - Store in Redis with NCP structure
   - Trigger appropriate storytelling flows

2. **GitHub Hook Enhancement** (`.github-hooks/`)
   - Enhanced hooks that invoke narrative analysis
   - Example: `issues` hook → Creates StoryBeat + triggers arc analysis
   - Pass context through environment variables + stdin

3. **Live Story Monitor API Integration**
   - Connect `/api/live-story-monitor/` to unified state
   - Stream narrative events in real-time
   - Archive completed story arcs

4. **Episode Generation Pipeline**
   - From webhook events → S01E0X episodes
   - Auto-generate NCP JSON from event sequences
   - Apply multiverse 3-act structure

---

## 📂 File Structure & Implementation Plan

```
/workspace/langgraph/
├── libs/
│   ├── narrative-intelligence/
│   │   ├── narrative_intelligence/
│   │   │   ├── nodes/
│   │   │   │   ├── ncp_loader.py ✅
│   │   │   │   ├── narrative_traversal.py ✅
│   │   │   │   ├── emotional_classifier.py ✅
│   │   │   │   ├── narrative_intent_classifier.py 🔴 NEW
│   │   │   │   └── webhook_event_processor.py 🔴 NEW (Phase 5)
│   │   │   ├── graphs/
│   │   │   │   ├── character_arc.py ✅
│   │   │   │   ├── thematic_analyzer.py ✅
│   │   │   │   ├── unified_narrative_graph.py 🔴 NEW
│   │   │   │   └── three_universe_processor.py 🔴 NEW
│   │   │   └── schemas/
│   │   │       ├── ncp.py ✅
│   │   │       ├── state.py ✅
│   │   │       ├── unified_state_bridge.py 🔴 NEW
│   │   │       └── universe_perspective.py 🔴 NEW
│   │   └── pyproject.toml
│   └── storytelling-integration/
│       ├── narrative_aware_story_graph.py 🔴 NEW
│       ├── emotional_feedback_loop.py 🔴 NEW
│       └── agentic_enrichment.py 🔴 NEW
│
├── integrations/
│   ├── flowise_narrative_bridge.py 🔴 NEW
│   ├── langflow_narrative_bridge.py 🔴 NEW (for ava-langflow)
│   ├── langfuse_narrative_tracer.py 🔴 NEW
│   ├── checkpoint_narrative_state.py 🔴 NEW
│   ├── redis_state_bridge.py 🔴 NEW (Miadi-46 compatibility)
│   └── miadi_webhook_bridge.py 🔴 NEW (Phase 5)
│
└── examples/
    ├── unified_narrative_story_flow.py 🔴 NEW
    └── webhook_to_episode.py 🔴 NEW (Phase 5)

/workspace/ava-langflow/
├── src/agentic_flywheel/
│   ├── routing/
│   │   ├── router.py ✅
│   │   └── narrative_router.py 🔴 NEW (narrative-aware routing)
│   ├── integrations/
│   │   ├── langfuse_tracer.py ✅
│   │   ├── redis_state.py ✅
│   │   └── narrative_state_bridge.py 🔴 NEW
│   ├── narrative_intent_classifier.py 🔴 NEW
│   ├── ncp_context_injector.py 🔴 NEW
│   └── three_universe_handler.py 🔴 NEW
└── MISSION_251231.md 🔴 NEW

/workspace/langchain/
├── integrations/
│   └── narrative_langfuse_handler.py 🔴 NEW
│       └── Langfuse integration for narrative events

/workspace/ava-Flowise/
├── agentic_flywheel/
│   ├── narrative_flow_router.py 🔴 NEW
│   ├── ncp_context_injector.py 🔴 NEW
│   └── flow_registry.yaml (update)

/src/storytelling/
├── storytelling/
│   ├── narrative_intelligence_integration.py 🔴 NEW
│   ├── emotional_beat_enricher.py 🔴 NEW
│   ├── character_arc_tracker.py 🔴 NEW
│   ├── analytical_feedback_loop.py 🔴 NEW
│   └── graph.py (enhance existing)
└── MISSION_251231.md ✅

/src/Miadi-46/
├── .github-hooks/
│   ├── issues (enhance) 🔴 UPDATE
│   ├── push (enhance) 🔴 UPDATE
│   └── narrative_processor.sh 🔴 NEW
├── app/api/
│   ├── narrative-bridge/ 🔴 NEW
│   │   └── route.ts (receive narrative state from stack)
│   └── live-story-monitor/ ✅ (connect to unified state)
├── stories/multiverse_3act_2512012121/
│   ├── schema/ncp-schema.json ✅
│   ├── episodes/ ✅
│   └── auto-generator/ 🔴 NEW (webhook → episode pipeline)
└── MISSION_251231.md 🔴 NEW
```
│   │   │   │   ├── narrative_traversal.py ✅
│   │   │   │   ├── emotional_classifier.py ✅
│   │   │   │   └── narrative_intent_classifier.py 🔴 NEW
│   │   │   ├── graphs/
│   │   │   │   ├── character_arc.py ✅
│   │   │   │   ├── thematic_analyzer.py ✅
│   │   │   │   └── unified_narrative_graph.py 🔴 NEW
│   │   │   └── schemas/
│   │   │       ├── ncp.py ✅
│   │   │       ├── state.py ✅
│   │   │       └── unified_state_bridge.py 🔴 NEW
│   │   └── pyproject.toml
│   └── storytelling-integration/
│       ├── narrative_aware_story_graph.py 🔴 NEW
│       ├── emotional_feedback_loop.py 🔴 NEW
│       └── agentic_enrichment.py 🔴 NEW
│
├── integrations/
│   ├── flowise_narrative_bridge.py 🔴 NEW
│   │   └── Connects Flowise flows to NCP state
│   ├── langfuse_narrative_tracer.py 🔴 NEW
│   │   └── Custom narrative events in traces
│   └── checkpoint_narrative_state.py 🔴 NEW
│       └── Persistent narrative checkpointing
│
└── examples/
    └── unified_narrative_story_flow.py 🔴 NEW
        └── End-to-end example: NCP → Story → Analysis → Agent Enrichment

/workspace/langchain/
├── integrations/
│   └── narrative_langfuse_handler.py 🔴 NEW
│       └── Langfuse integration for narrative events

/workspace/ava-Flowise/
├── agentic_flywheel/
│   ├── narrative_flow_router.py 🔴 NEW
│   │   └── Narrative-aware flow selection
│   ├── ncp_context_injector.py 🔴 NEW
│   │   └── Embed NCP state in Flowise queries
│   └── flow_registry.yaml (update)
│       └── Add narrative-driven flow triggers

/src/storytelling/
├── storytelling/
│   ├── narrative_intelligence_integration.py 🔴 NEW
│   │   └── Feed story output to NCP analyzer
│   ├── emotional_beat_enricher.py 🔴 NEW
│   │   └── Use classifier to strengthen beats
│   └── graph.py (enhance existing)
│       └── Add analytical feedback loop
```

---

## 🚀 Implementation Roadmap

### **Sprint 1: Foundation (Days 1-3)**
- [ ] Create `unified_state_bridge.py` - Shared narrative state model
- [ ] Implement checkpoint integration for narrative persistence
- [ ] Wire `NCPLoaderNode` into story generation graph
- [ ] Add Langfuse instrumentation to storytelling graph

### **Sprint 2: Intelligence (Days 4-7)**
- [ ] Build `narrative_intent_classifier.py` - NCP-aware routing
- [ ] Create `narrative_aware_story_graph.py` - Unified orchestration
- [ ] Implement context injection for Flowise flows
- [ ] Test emotional beat classification on generated stories

### **Sprint 3: Integration (Days 8-10)**
- [ ] Build analytical feedback loop in storytelling system
- [ ] Create Flowise narrative flow router
- [ ] Implement story enrichment based on analytical insights
- [ ] End-to-end test: Generate → Analyze → Enrich → Trace

### **Sprint 4: Observability & Polish (Days 11-14)**
- [ ] Complete Langfuse instrumentation across all systems
- [ ] Create narrative trace format with custom event types
- [ ] Build live story monitor visualization
- [ ] Documentation, examples, and deployment guides

---

## 🔗 Key Integration Points

### **1. LangGraph ↔ Flowise Connection**
```python
# In unified orchestration:
1. Story generation produces story beats
2. Each beat classified for emotional tone
3. Intent classifier determines if enrichment needed
4. If yes: Narrative context injected into Flowise flow
5. Flow returns enriched dialogue/action
6. Updated beat added back to story
7. Cycle repeats for next beat
```

### **2. Narrative Analysis ↔ Story Generation Feedback**
```python
# In feedback loop:
1. Generated story passed to NCP analyzer
2. Character arcs extracted
3. Thematic tensions identified
4. Emotional beats classified
5. Gaps identified (weak emotional moments, arc inconsistencies)
6. Gap information routed back to story generator
7. Specific prompts injected to address gaps
8. Next iteration incorporates improvements
```

### **3. All Systems → Langfuse Tracing**
```python
# Unified tracing:
- Story generation spans with beat markers
- NCP analysis spans with graph traversals
- Flowise flow execution spans with intent classification
- Checkpoint spans for state saves
- All connected in parent-child hierarchy
```

---

## 🎓 Design Principles

1. **Narrative-First**: All agent decisions should consider narrative coherence
2. **State Transparency**: Narrative state always accessible to all components
3. **Composable Graphs**: Nodes reusable across story generation and analysis
4. **Feedback Loops**: Analysis insights drive generation improvements
5. **Observable**: Every decision traceable in Langfuse

---

## 📋 Success Criteria

- [ ] Story generation produces complete NCP-structured narratives
- [ ] Emotional beat analysis detects genuine narrative moments (accuracy > 80%)
- [ ] Flowise flows understand narrative context and adapt responses
- [ ] Analytical insights improve story quality (measured via coherence metrics)
- [ ] Checkpoint system allows resuming mid-story with full context
- [ ] Langfuse traces show complete story generation decision tree
- [ ] End-to-end example demonstrates all four components working together

---

## 💡 Next Immediate Actions

1. **This Session** (Claude instance):
   - [ ] Create `unified_state_bridge.py` - Start Phase 1
   - [ ] Review LangGraph checkpoint options
   - [ ] Design unified state serialization format

2. **Delegate to Next Instance**:
   - [ ] Implement checkpoint integration
   - [ ] Wire NCP analyzer into story generation
   - [ ] Start Phase 2 intelligence work

3. **Parallel Tracks** (if resources available):
   - [ ] Begin Flowise integration testing
   - [ ] Set up Langfuse instrumentation skeleton
   - [ ] Create example narratives for testing

---

## 📝 Context for Delegated Instances

When delegating work:
1. Start with Phase 1 (foundation) - it unblocks everything else
2. Use the state bridge as the integration contract
3. Each component is mostly complete - focus on interconnection
4. The Agentic Flywheel work failed because it tried to route without understanding narrative
5. Success = making agents narrative-aware, not just technically capable
6. All tracing goes through Langfuse - instrument as you build

---

## 📚 Key References

- **NCP Protocol**: Defined in `/workspace/langgraph/libs/narrative-intelligence/narrative_intelligence/schemas/ncp.py`
- **Story Generation**: `/src/storytelling/storytelling/graph.py` (55KB - comprehensive)
- **Agentic Flywheel Spec**: `/workspace/ava-Flowise/` and `/cesaret/src/agentic_flywheel/`
- **Existing QA**: `/workspace/langgraph/libs/narrative-intelligence/QA_REPORT.md`
- **Langfuse Integration**: `/workspace/langchain/` (ready to extend)

---

## 🌈 Vision

**The Goal**: A system where stories don't just get written—they get *understood*, *refined*, and *enriched* by intelligent agents working in concert with narrative analysis. Each story becomes a data point for improving the next. Each agent decision considers narrative coherence. Every moment is traceable. The system learns what makes stories resonate.

**The Stack**: LangGraph (core narrative logic) + Flowise (specialized agent capabilities) + LangChain (unified tracing) = **Narrative Intelligence at Scale**

---

**Last Updated**: 2025-12-31
**Status**: Architectural blueprint complete, implementation ready
**Complexity**: High - requires deep understanding of narrative, agents, and state management
**Estimated Effort**: 40-60 developer-hours for full implementation
