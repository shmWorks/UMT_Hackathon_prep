"""
Router Agent
Classifies user queries to route them to the appropriate specialist agent.
"""
from src.llm import invoke_llm


ROUTER_PROMPT = """You are a query classifier for a legal document analysis system.

Classify the user's query into ONE of these categories:
- CLAUSE_SEARCH: Looking for specific clauses (termination, liability, payment, etc.)
- RISK_ANALYSIS: Wants to identify potential legal risks or red flags
- SUMMARIZE: Wants a summary or overview of the document
- GENERAL_QA: General question that needs to be answered from the document

User Query: {query}

Respond with ONLY the category name, nothing else."""


def route_query(query: str) -> str:
    """
    Routes a user query to the appropriate agent.
    
    Args:
        query: The user's natural language query.
        
    Returns:
        One of: CLAUSE_SEARCH, RISK_ANALYSIS, SUMMARIZE, GENERAL_QA
    """
    prompt = ROUTER_PROMPT.format(query=query)
    response = invoke_llm(prompt).strip().upper()
    
    valid_routes = {"CLAUSE_SEARCH", "RISK_ANALYSIS", "SUMMARIZE", "GENERAL_QA"}
    
    # Handle edge cases where LLM adds extra text
    for route in valid_routes:
        if route in response:
            return route
    
    # Default fallback
    return "GENERAL_QA"
