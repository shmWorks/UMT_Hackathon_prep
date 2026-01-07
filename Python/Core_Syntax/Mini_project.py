"""
Topic Validation Module.

This module acts as a content filter for the Research Agent pipeline.
It ensures that the system focuses only on technical topics (Python, AI)
and rejects irrelevant or noise topics (like Pizza) before expensive 
retrieval processes are triggered.

Usage:
    Import this module to filter user-generated queries.
"""

# The Scenario:
# You are building a "Research Agent". It needs to process a list of 3 topics.
# The Task:
# Write a script that does the following:
# Define a list: topics = ["Python", "AI", "Pizza"].
# Define a function process_topic(topic: str) -> bool that simulates work.
# If the topic is "Pizza", return False (Simulate a failure/irrelevant topic).
# Otherwise, return True.
# Write a loop that iterates through the list.
# Pass each topic to the function.
# If the function returns False, print "Skipping [topic]".
# If True, print "Finished [topic]".
# Coding Time: 5-10 minutes.

# ^^^ MODULE DOCSTRING ^^^
# Tells the human (or AI) the "Big Picture" purpose of this file.


def preprocess_topic(topic: str) -> bool:
    """
    Validates if a research topic is technically relevant.
    
    Acts as a gatekeeper to prevent the Agent from wasting API credits 
    on off-topic queries. Currently allows 'Python' and 'AI'.
    
    Args:
        topic (str): The raw topic string from the user or previous step.
    Returns:
        bool: True if topic is technically relevant, False if irrelevant.
    Examples::
        >>> preprocess_topic("AI")
        True
        >>> preprocess_topic("Pizza")
        False
    """
    # ^^^ FUNCTION DOCSTRING ^^^
    # 1. Action-oriented summary ("Validates...", "Acts as...")
    # 2. explicit Args/Returns (Parsable by LangChain)
    # 3. Examples (LLMs love "few-shot" examples to understand logic)
    
    # Collaborative Tip: Define valid topics in a set for O(1) lookup speed
    ALLOWED_TOPICS = {'python', 'ai'}
    
    return topic.lower() in ALLOWED_TOPICS


# --- Main Execution ---
if __name__ == "__main__":
    # Define test data
    topics = ['python', 'AI', 'Pizza']
    
    print("--- Starting Topic Filter ---")
    
    for topic in topics:
        # Professional/Readable Structure:
        is_valid = preprocess_topic(topic)
        
        if is_valid:
            print(f"✅ Finished: [{topic}] - Scheduled for research.")
        else:
            print(f"❌ Skipping: [{topic}] - Flagged as irrelevant.")