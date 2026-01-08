"""
PHASE 1 (Part 2): CONTROL FLOW - The Looping Brain
Goal: Master nested loops, break/continue, and agent life-cycles.

------------------------------------------------------------------
EXERCISE 1: The Retry Loop
------------------------------------------------------------------
Agents often need to retry failed API calls.
Read this loop. Under what conditions does it print "Gave up"?

"""

import random

def mock_api_call():
    # Simulates an API that fails 80% of the time
    if random.random() < 0.8:
        raise ConnectionError("Fail")
    return "Success"

print("--- Exercise 1: Retry Loop ---")
max_retries = 3
attempt = 0

while attempt < max_retries:
    try:
        print(f"Attempt {attempt + 1}...")
        result = mock_api_call()
        print(f"Got: {result}")
        break # <--- Why is this here?
    except ConnectionError:
        print("Error, retrying...")
        attempt += 1
else:
    # <--- The 'else' block on a while loop is rare but useful.
    # It runs ONLY if the loop completed NORMALLY (did not break).
    print("Gave up after all retries.")

# CHALLENGE 1: 
# 1. Run this a few times.
# 2. Modify it to use a 'for' loop with 'range(max_retries)' instead of 'while'.


"""------------------------------------------------------------------
EXERCISE 2: The Agent Decision Tree
------------------------------------------------------------------
An agent often loops until it decides it is "DONE".
"""

def run_agent_turn(turn_n):
    # Simulates agent thinking
    # Turn 3 is always the "DONE" turn for this demo
    if turn_n == 3:
        return {"action": "FINISH", "content": "Here is the answer."}
    return {"action": "SEARCH", "query": "python loops"}

print("\n--- Exercise 2: Agent Loop ---")
turn = 0
while True:
    turn += 1
    decision = run_agent_turn(turn)
    
    print(f"Turn {turn}: Agent decided to {decision['action']}")
    
    if decision['action'] == "FINISH":
        print(f"Final Answer: {decision['content']}")
        # STOP THE LOOP HERE
        break # <--- REPLACE 'pass' with the correct keyword
    
    if turn > 10:
        print("Emergency Stop: Too many turns!")
        break

# CHALLENGE 2:
# Replace 'pass' with 'break'.
# What happens if you accidentally used 'continue'? predict first.
