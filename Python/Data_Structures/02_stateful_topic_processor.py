"""
PROJECT: Stateful Topic Processor
Goal: Refactor /python/Core_Syntax/Mini_project.py logic to use a professional "State Pattern". 
In Agentic AI, we don't just print results; we accumulate them into a State object
so that the next Agent or Tool can act on them.
"""

def preprocess_topic(topic: str) -> bool:
    """Validates if a topic is technically relevant."""
    ALLOWED_TOPICS = {'python', 'ai'}
    return topic.lower() in ALLOWED_TOPICS

def run_pipeline(topics: list[str]) -> dict:
    # 1. INITIALIZE STATE
    # This is the "Brain" of our pipeline. 
    # Everything that happens is recorded here.
    state = {
        "processed": [],
        "skipped": [],
        "metadata": {
            "total_count": len(topics),
            "success_rate": 0.0
        }
    }

    print("--- Starting Stateful Pipeline ---")

    # 2. PROCESS & UPDATE STATE
    for topic in topics:
        if preprocess_topic(topic):
            print(f"✅ Approved: {topic}")
            state["processed"].append(topic)
        else:
            print(f"❌ Rejected: {topic}")
            state["skipped"].append(topic)

    # 3. CALCULATE FINAL STATE METRICS
    processed_count = len(state["processed"])
    if state["metadata"]["total_count"] > 0:
        state["metadata"]["success_rate"] = (processed_count / state["metadata"]["total_count"]) * 100

    return state

# --- Main Execution ---
if __name__ == "__main__":
    raw_topics = ["Python", "AI", "Pizza", "Machine Learning", "Burgers"]
    
    # Run the system and capture the final state
    final_state = run_pipeline(raw_topics)

    # 4. SUMMARIZE STATE
    print("\n" + "="*30)
    print("PIPELINE SUMMARY")
    print("="*30)
    # Using our map/join pattern for professional output
    print(f"Processed: {', '.join(final_state['processed'])}")
    print(f"Skipped:   {', '.join(final_state['skipped'])}")
    print(f"Success Rate: {final_state['metadata']['success_rate']:.1f}%")
    print("="*30)