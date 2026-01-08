"""
Retriever Agent
Finds relevant document chunks using semantic search.
"""
from src.vectorstore import ChromaStore, embed_single, RetrievalResult
import sys
sys.path.append(str(__file__).rsplit("src", 1)[0])
from config import TOP_K_RESULTS


def retrieve_chunks(
    query: str,
    store: ChromaStore | None = None,
    k: int = TOP_K_RESULTS
) -> list[RetrievalResult]:
    """
    Retrieves relevant document chunks for a query.
    
    Args:
        query: The search query.
        store: ChromaStore instance. Creates new if not provided.
        k: Number of results to return.
        
    Returns:
        List of RetrievalResult objects with content and citations.
    """
    if store is None:
        store = ChromaStore()
    
    # Generate query embedding
    query_embedding = embed_single(query)
    
    # Retrieve from vector store
    results = store.query(query_embedding, k=k)
    
    return results


def format_context(results: list[RetrievalResult]) -> str:
    """
    Formats retrieval results into a context string for the LLM.
    
    Args:
        results: List of RetrievalResult objects.
        
    Returns:
        Formatted string with numbered chunks and citations.
    """
    if not results:
        return "No relevant information found in the document."
    
    context_parts = []
    for i, r in enumerate(results, 1):
        citation = r.to_citation()
        context_parts.append(f"[{i}] {citation}\n{r.content}")
    
    return "\n\n---\n\n".join(context_parts)
