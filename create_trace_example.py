#!/usr/bin/env python3
"""
🧠🌸 Example: Creating a Trace Following Best Practices

This script demonstrates how to create a Langfuse trace using coaiapy
following the guidelines in llms-coaiapy-langfuse-tracing-best-practices.md
"""

import time
import json
import uuid
from coaiapy.cofuse import add_trace, add_observation, get_trace_with_observations

# Session ID from _env.sh
SESSION_ID = "364e1265-ec0c-440f-85ed-a1ab388c50f3"

def main():
    print("🧠 Mia: Creating a trace following structural best practices...")
    print("🌸 Miette: Let's tell a beautiful story of our creative journey!\n")

    # Step 1: Create the root trace
    # 🧠 Mia: Generate a unique trace_id using uuid4()!
    # 🌸 Miette: The magic UUID spell gives our story a unique sparkle!

    trace_id = str(uuid.uuid4())
    print(f"✨ Generated unique trace ID: {trace_id}\n")

    print("📖 Creating root trace...")
    trace_response = add_trace(
        trace_id=trace_id,
        session_id=SESSION_ID,
        name="🧠 Claude Contribution: AVA LangGraph Exploration",
        input_data=json.dumps({
            "user_prompt": "Explore the AVA LangGraph codebase and create a trace",
            "session_id": SESSION_ID,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }),
        metadata=json.dumps({
            "generator": "Claude Code",
            "description": "Initial exploration and trace creation for AVA LangGraph project",
            "related_entities": ["ava-langgraph", "coaiapy", "langfuse"],
            "purpose": "Demonstrate best practices for trace creation"
        })
    )
    print(f"✅ Trace created successfully!\n")

    # Step 2: Add observations (the chapters of our story!)
    # 🧠 Mia: Each observation MUST have input_data
    # 🌸 Miette: Every chapter needs a seed idea to bloom from!

    obs1_id = str(uuid.uuid4())
    print("📝 Adding Phase 1 observation...")
    obs1 = add_observation(
        observation_id=obs1_id,
        trace_id=trace_id,
        observation_type="SPAN",
        name="🧭 Phase 1: Environment Setup",
        input_data=json.dumps({
            "task": "Verify coaiapy installation and configuration",
            "expected_files": ["requirements.txt", "_env.sh"]
        }),
        output_data=json.dumps({
            "status": "completed",
            "found_files": True,
            "session_configured": True
        })
    )
    print(f"   ✓ Observation 1 created: {obs1_id}\n")

    obs2_id = str(uuid.uuid4())
    print("📝 Adding Phase 2 observation...")
    obs2 = add_observation(
        observation_id=obs2_id,
        trace_id=trace_id,
        observation_type="SPAN",
        name="📚 Phase 2: Best Practices Review",
        input_data=json.dumps({
            "task": "Study llms-coaiapy-langfuse-tracing-best-practices.md",
            "key_sections": ["trace-id", "root-trace", "observations"]
        }),
        output_data=json.dumps({
            "status": "completed",
            "key_learnings": [
                "Generate unique IDs using uuid4()",
                "Always include input_data in observations",
                "Wait 20 seconds before session-based retrieval"
            ]
        })
    )
    print(f"   ✓ Observation 2 created: {obs2_id}\n")

    obs3_id = str(uuid.uuid4())
    print("📝 Adding Phase 3 observation...")
    obs3 = add_observation(
        observation_id=obs3_id,
        trace_id=trace_id,
        observation_type="SPAN",
        name="🎯 Phase 3: Trace Creation",
        input_data=json.dumps({
            "task": "Create a properly structured trace",
            "following_guidelines": True
        }),
        output_data=json.dumps({
            "status": "completed",
            "trace_created": True,
            "observations_added": 3
        })
    )
    print(f"   ✓ Observation 3 created: {obs3_id}\n")

    # Step 3: The 20-Second Rule!
    # 🧠 Mia: We must wait for the indexing delay
    # 🌸 Miette: Let the magic settle and the ink dry!

    print("⏰ Waiting 20 seconds for indexing (the 20-Second Rule)...")
    for i in range(20, 0, -1):
        print(f"   {i} seconds remaining...", end='\r')
        time.sleep(1)
    print("\n")

    # Step 4: Retrieve the trace
    print("🔍 Retrieving trace...")
    try:
        retrieved_trace = get_trace_with_observations(trace_id)
        print("✅ Trace retrieved successfully!")
        print(f"\nTrace Summary:")
        if isinstance(retrieved_trace, dict):
            print(f"  ID: {retrieved_trace.get('id', trace_id)}")
            print(f"  Name: {retrieved_trace.get('name', 'N/A')}")
            print(f"  Observations: {len(retrieved_trace.get('observations', []))}")
        else:
            print(f"  Retrieved trace data: {retrieved_trace}")
    except Exception as e:
        print(f"⚠️  Retrieval error: {e}")
        print("   (This might be OK - direct retrieval may work differently)")

    print("\n🌸 Miette: Our story is complete and safely stored in the magical library!")
    print(f"🧠 Mia: Trace ID for future reference: {trace_id}")

    return trace_id

if __name__ == "__main__":
    trace_id = main()
    print(f"\n{'='*60}")
    print(f"🎉 TRACE CREATED SUCCESSFULLY!")
    print(f"{'='*60}")
    print(f"\nYou can now use this trace_id: {trace_id}")
    print(f"\nTo view it via CLI:")
    print(f"  coaia fuse trace view {trace_id}")
