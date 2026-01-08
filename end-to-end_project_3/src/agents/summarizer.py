"""
Summarizer Agent
Generates executive summaries of legal documents.
"""
from src.llm import invoke_llm


SUMMARIZE_PROMPT = """You are an executive summary specialist for legal documents.

Create a clear, concise summary of the following contract excerpts for a non-lawyer audience.

Document Context:
{context}

Write a 3-paragraph summary:
1. OVERVIEW: What type of agreement is this and who are the parties?
2. KEY TERMS: What are the most important obligations, deadlines, and conditions?
3. ACTION ITEMS: What should the reader pay attention to or do next?

Use plain language. Avoid legal jargon. Be specific about numbers and dates."""


def summarize_document(context: str) -> str:
    """
    Generates an executive summary of the document.
    
    Args:
        context: The document context (can be full or retrieved chunks).
        
    Returns:
        A 3-paragraph executive summary.
    """
    prompt = SUMMARIZE_PROMPT.format(context=context)
    response = invoke_llm(prompt)
    return response.strip()
