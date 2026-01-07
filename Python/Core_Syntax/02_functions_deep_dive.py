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
   if tools_list is None:
       tools_list = []
   tools_list.append(tool_name)
   return tools_list

print("--- Challenge 1 Output ---")
# Agent A gets a tool
agent_a_tools = safe_add_tool("Search")
print(f"Agent A: {agent_a_tools}")
# Agent B gets a tool... now correctly isolated
agent_b_tools = safe_add_tool("Calculator")
print(f"Agent B: {agent_b_tools}")



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

# add type hints for inputs and outputs(returned back)
def process(d:dict[str,str], q:str) -> list[str]:
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
    """
    Search documents and return titles containing the query string.
    
    Performs a case-sensitive substring search across document content.

    Args:
        docs (dict[str, str]): Dictionary mapping document titles (str) to content (str).
        query (str): Search query string to match within document content.
    
    Returns:
       list[str]: List of document titles containing the query substring.
    
    Example:
        >>> docs = {
        ...     "report": "AI trends 2026",
        ...     "blog": "Python basics"
        ... }
        >>> find_relevant_documents(docs, "AI")
        ['report']
    """
    result = []
    for k, v in docs.items():
        if query in v:
            result.append(k)
    return result


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

def clean(text:str) -> str:
    """
    Strip whitespaces from the input string and convert it to lowercase

    Args:
        text (str): string to clean
    
    Returns:
        str: input string converted to lowercase with leading/trailing whitespaces removed
    """
    return text.strip().lower()

def think(text:str) -> str:
    """
    Prefix the input string with "I think: "

    Args:
        text (str): string to process
    
    Returns:
        str: input string prefixed with "I think: "
    """
    return f"I think: {text}"

def speak(text:str) -> str:
    """
    Wrap the input string in a JSON format {"say": text}

    Args:
        text (str): string to format
    
    Returns:
        str: JSON formatted string with the input text
    """
    return f'{{"say": "{text}"}}'


input_text = "   User Query   "
print(f"before: '{input_text}'")
result = speak(think(clean(input_text)))
print(f"after: {result}")


