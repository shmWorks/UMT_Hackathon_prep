"""
PHASE 1 (Part 1): FUNCTIONS - Deep Dive
Goal: Internalize function contracts, type hints, and the "Mutable Default" trap.

------------------------------------------------------------------
EXERCISE 1: The Mutable Default Trap (CRITICAL)
------------------------------------------------------------------
Predict what happens when you run this code.
Do not run it yet. Read, Think, Predict.
"""

def unsafe_add_tool(tool_name, tools_list=[]):
    """Adds a tool to the agent's toolbox."""
    tools_list.append(tool_name)
    return tools_list

print("--- Exercise 1 Output ---")
# Agent A gets a tool
agent_a_tools = unsafe_add_tool("Search")
print(f"Agent A: {agent_a_tools}")

# Agent B gets a tool... but wait?
agent_b_tools = unsafe_add_tool("Calculator")
print(f"Agent B: {agent_b_tools}")

# CHALLENGE 1: Fix the function above so Agent B doesn't inherit Agent A's tools.
# (Write your fix below)
def safe_add_tool(tool_name, tools_list=None):
    pass # <--- IMPLEMENT THIS


"""------------------------------------------------------------------
EXERCISE 2: Type Hints & Signatures
------------------------------------------------------------------
Agents rely on strict contracts. 
Refactor this "mystery function" into a clean, type-hinted function.
"""

def process(d, q):
    # d is a dictionary of documents (title -> content)
    # q is a search query string
    # Returns a list of matching titles
    r = []
    for k, v in d.items():
        if q in v:
            r.append(k)
    return r

# CHALLENGE 2: Rewrite 'process' as 'find_relevant_documents'
# Use type hints: dict[str, str], str, list[str]
# Add a docstring.

def find_relevant_documents(docs: dict[str, str], query: str) -> list[str]:
    pass # <--- IMPLEMENT THIS


"""------------------------------------------------------------------
EXERCISE 3: Function Composition (The "Chain")
------------------------------------------------------------------
Agents are chains of functions. 
clean_input -> think -> format_output

1. clean(text) -> strips whitespace, lowercases
2. think(text) -> adds "I think: " prefix
3. speak(text) -> wraps in JSON format {"say": text}

Write these 3 tiny functions and chain them.
"""

# CHALLENGE 3: Implement the chain
# input_text = "   User Query   "
# result = speak(think(clean(input_text)))
# print(result)

def agent(messages=[]):
    messages.append("hello")
    return messages

print(agent())
print(agent())


