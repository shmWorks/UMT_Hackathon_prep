"""
PHASE 2: Data Structures Mastery for Agentic AI
Goal: Handle deeply nested JSON, context windows, and immutable keys.

------------------------------------------------------------------
EXERCISE 1: The "Nested State" Nightmare
------------------------------------------------------------------
Agents use nested dicts. Accessing them safely is critical.
LLMs often skip keys or return nulls.
"""

# A complex, messy state from an LLM run
agent_state = {
    "session_id": "123",
    "memory": {
        "short_term": ["Hi", "Hello"],
        # "long_term": MISSING!
    },
    "tools_output": [
        None, # Failed tool
        {"tool": "search", "result": "Python 3.12"},
        {"tool": "search", "result": None}
    ]
}

def get_last_search_result(state):
    # CHALLENGE 1: 
    # Extract the 'result' of the LAST successful 'search' tool usage.
    # Rules:
    # 1. Handle missing keys gracefully.
    # 2. Iterate backwards.
    # 3. Ignore None items in the list.
    # 4. Return "No result" if nothing found.
    pass # <--- IMPLEMENT THIS

print("--- Exercise 1: Nested Extraction ---")
# print(get_last_search_result(agent_state))

"""
------------------------------------------------------------------
EXERCISE 2: Comprehensions (The "Filter" Engine)
------------------------------------------------------------------
You have a list of tool outputs. Some are errors/empty.
Clean them in ONE line.
"""

raw_logs = [
    {"id": 1, "status": "success", "data": "A"},
    {"id": 2, "status": "failed", "data": "Err"},
    {"id": 3, "status": "success", "data": ""}, # Empty data
    {"id": 4, "status": "pending", "data": "C"}
]

# CHALLENGE 2:
# Create a Dict where key=id and value=data.
# ONLY include items where status is 'success' AND data is not empty.
# Use a DICTIONARY COMPREHENSION.

clean_data = {} # <--- IMPLEMENT THIS

print("\n--- Exercise 2: Comprehensions ---")
print(f"Clean Logs: {clean_data}")


"""
------------------------------------------------------------------
EXERCISE 3: Smart Merging (The State Updater)
------------------------------------------------------------------
You have a 'default_config' and a 'user_override'.
The user override should partial-update the config.
Note: .update() is shallow! We want a simple overwrite for now.
"""

default_config = {"model": "gpt-4", "temp": 0.7, "retries": 3}
user_override = {"temp": 0.1, "verbose": True}

# CHALLENGE 3: 
# Create 'final_config' that has all defaults, but with user overrides applied.
# Use the Dictionary Merge Operator '|' (Python 3.9+) or {**d1, **d2}

final_config = {} # <--- IMPLEMENT THIS

print("\n--- Exercise 3: Config Merging ---")
print(f"Final Config: {final_config}")


"""
------------------------------------------------------------------
EXERCISE 4: Immutable Keys (The "Cache" Pattern)
------------------------------------------------------------------
You want to cache API calls. dict keys must be immutable.
Values can be anything.
"""

# We want to cache: func="search", query="python" -> Result
api_cache = {}

def mock_search(query):
    # This represents an expensive tool
    return f"Results for {query}"

# CHALLENGE 4:
# 1. Create a key from ("search", "agentic ai")
# 2. Check if key is in api_cache.
# 3. If not, run mock_search and store it.
# 4. Print the cache.

print("\n--- Exercise 4: Tuple Keys ---")
# Write your caching logic here...
