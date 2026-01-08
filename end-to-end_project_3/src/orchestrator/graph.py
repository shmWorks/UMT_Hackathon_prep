"""
LangGraph Orchestrator
Coordinates multiple agents using a state graph for conditional routing.
"""
from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END

from src.agents import (
    route_query,
    retrieve_chunks,
    format_context,
    analyze_clause,
    assess_risks,
    summarize_document
)
from src.vectorstore import ChromaStore
from src.llm import invoke_llm


# === State Definition ===
class AgentState(TypedDict):
    """State passed between nodes in the graph."""
    query: str
    route: str
    context: str
    response: str
    citations: list[str]


# === Node Functions ===

def router_node(state: AgentState) -> AgentState:
    """Classifies the query and determines the route."""
    route = route_query(state["query"])
    return {"route": route}


def retriever_node(state: AgentState) -> AgentState:
    """Retrieves relevant chunks from the vector store."""
    store = ChromaStore()
    results = retrieve_chunks(state["query"], store=store)
    context = format_context(results)
    citations = [r.to_citation() for r in results]
    return {"context": context, "citations": citations}


def clause_search_node(state: AgentState) -> AgentState:
    """Handles clause search queries."""
    # Extract clause type from query (simplified)
    query_lower = state["query"].lower()
    clause_type = "general"
    
    for ct in ["termination", "liability", "payment", "confidentiality", "indemnification"]:
        if ct in query_lower:
            clause_type = ct
            break
    
    clause_info = analyze_clause(state["context"], clause_type)
    
    response = f"""**{clause_info.clause_type.title()} Clause Analysis**

**Summary:** {clause_info.summary}

**Key Terms:** {', '.join(clause_info.key_terms) if clause_info.key_terms else 'N/A'}

**Source:** {clause_info.page_reference}
"""
    return {"response": response}


def risk_analysis_node(state: AgentState) -> AgentState:
    """Handles risk analysis queries."""
    risk_report = assess_risks(state["context"])
    
    risk_lines = []
    for risk in risk_report.risks:
        severity_emoji = {"HIGH": "🔴", "MEDIUM": "🟡", "LOW": "🟢"}.get(risk.severity, "⚪")
        risk_lines.append(f"{severity_emoji} **{risk.risk_title}** ({risk.severity})")
        risk_lines.append(f"   {risk.description}")
        risk_lines.append(f"   💡 *{risk.recommendation}*")
        risk_lines.append("")
    
    response = f"""**Risk Assessment Report**

**Overall Risk Level:** {risk_report.overall_risk_level}

**Identified Risks:**
{chr(10).join(risk_lines)}

**Summary:** {risk_report.summary}
"""
    return {"response": response}


def summarize_node(state: AgentState) -> AgentState:
    """Handles summarization queries."""
    summary = summarize_document(state["context"])
    return {"response": f"**Executive Summary**\n\n{summary}"}


def general_qa_node(state: AgentState) -> AgentState:
    """Handles general Q&A queries."""
    prompt = f"""Based on the following document excerpts, answer the user's question.

Document Context:
{state["context"]}

Question: {state["query"]}

Provide a clear, direct answer. If the answer is not in the context, say so."""
    
    answer = invoke_llm(prompt)
    
    # Add citations
    citations_text = "\n".join(state.get("citations", []))
    response = f"{answer}\n\n**Sources:**\n{citations_text}"
    
    return {"response": response}


# === Routing Logic ===

def decide_next_node(state: AgentState) -> Literal["clause_search", "risk_analysis", "summarize", "general_qa"]:
    """Determines which specialist node to run based on the route."""
    route_map = {
        "CLAUSE_SEARCH": "clause_search",
        "RISK_ANALYSIS": "risk_analysis",
        "SUMMARIZE": "summarize",
        "GENERAL_QA": "general_qa"
    }
    return route_map.get(state["route"], "general_qa")


# === Graph Builder ===

def build_graph() -> StateGraph:
    """Constructs the LangGraph workflow."""
    graph = StateGraph(AgentState)
    
    # Add nodes
    graph.add_node("router", router_node)
    graph.add_node("retriever", retriever_node)
    graph.add_node("clause_search", clause_search_node)
    graph.add_node("risk_analysis", risk_analysis_node)
    graph.add_node("summarize", summarize_node)
    graph.add_node("general_qa", general_qa_node)
    
    # Define edges
    graph.set_entry_point("router")
    graph.add_edge("router", "retriever")
    
    # Conditional routing after retrieval
    graph.add_conditional_edges(
        "retriever",
        decide_next_node,
        {
            "clause_search": "clause_search",
            "risk_analysis": "risk_analysis",
            "summarize": "summarize",
            "general_qa": "general_qa"
        }
    )
    
    # All specialist nodes end the graph
    graph.add_edge("clause_search", END)
    graph.add_edge("risk_analysis", END)
    graph.add_edge("summarize", END)
    graph.add_edge("general_qa", END)
    
    return graph.compile()


# === Main Entry Point ===

def run_agent(query: str) -> str:
    """
    Runs the full agent pipeline for a query.
    
    Args:
        query: User's natural language question.
        
    Returns:
        The agent's response as a formatted string.
    """
    graph = build_graph()
    
    initial_state: AgentState = {
        "query": query,
        "route": "",
        "context": "",
        "response": "",
        "citations": []
    }
    
    final_state = graph.invoke(initial_state)
    
    return final_state["response"]
