"""
Clause Analyzer Agent
Extracts and structures specific clause types from legal documents.
"""
from pydantic import BaseModel
from src.llm import invoke_llm


class ClauseInfo(BaseModel):
    """Structured representation of an extracted clause."""
    clause_type: str
    summary: str
    key_terms: list[str]
    page_reference: str


CLAUSE_PROMPT = """You are a legal clause extraction specialist.

Given the following document excerpts, extract information about {clause_type} clauses.

Document Context:
{context}

Provide your analysis in this exact format:
CLAUSE_TYPE: {clause_type}
SUMMARY: [1-2 sentence summary of the clause]
KEY_TERMS: [comma-separated list of key terms, numbers, or conditions]
PAGE_REFERENCE: [page numbers where this clause appears]

If the clause type is not found, respond with:
CLAUSE_TYPE: {clause_type}
SUMMARY: Not found in the provided document sections.
KEY_TERMS: N/A
PAGE_REFERENCE: N/A
"""


def analyze_clause(context: str, clause_type: str) -> ClauseInfo:
    """
    Analyzes document context to extract specific clause information.
    
    Args:
        context: The document context from retrieval.
        clause_type: Type of clause to find (e.g., "termination", "liability").
        
    Returns:
        ClauseInfo object with structured clause data.
    """
    prompt = CLAUSE_PROMPT.format(context=context, clause_type=clause_type)
    response = invoke_llm(prompt)
    
    # Parse the structured response
    lines = response.strip().split("\n")
    parsed = {}
    
    for line in lines:
        if ":" in line:
            key, value = line.split(":", 1)
            parsed[key.strip().upper()] = value.strip()
    
    return ClauseInfo(
        clause_type=parsed.get("CLAUSE_TYPE", clause_type),
        summary=parsed.get("SUMMARY", "Unable to extract"),
        key_terms=[t.strip() for t in parsed.get("KEY_TERMS", "").split(",") if t.strip()],
        page_reference=parsed.get("PAGE_REFERENCE", "Unknown")
    )
