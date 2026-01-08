"""
ChromaDB Vector Store Module
Handles storage and retrieval of document embeddings with metadata filtering.
"""
from pathlib import Path
from dataclasses import dataclass
import sys
sys.path.append(str(__file__).rsplit("src", 1)[0])
from config import CHROMA_PERSIST_DIR, TOP_K_RESULTS


@dataclass
class RetrievalResult:
    """A single retrieval result with content and metadata."""
    content: str
    score: float  # Lower is better (distance)
    page_number: int
    source: str
    chunk_index: int
    
    def to_citation(self) -> str:
        """Formats as a readable citation."""
        return f"[{self.source}, Page {self.page_number}]"


class ChromaStore:
    """
    Wrapper around ChromaDB for document storage and retrieval.
    
    Provides a clean interface for:
    - Adding documents with embeddings and metadata
    - Semantic search with optional metadata filtering
    - Persistent storage across sessions
    """
    
    def __init__(self, collection_name: str = "legal_documents"):
        import chromadb
        from chromadb.config import Settings
        
        # Ensure persist directory exists
        Path(CHROMA_PERSIST_DIR).mkdir(parents=True, exist_ok=True)
        
        self.client = chromadb.PersistentClient(
            path=str(CHROMA_PERSIST_DIR),
            settings=Settings(anonymized_telemetry=False)
        )
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}  # Use cosine similarity
        )
    
    def add_documents(
        self,
        chunks: list,  # List of TextChunk objects
        embeddings: list[list[float]]
    ) -> None:
        """
        Adds document chunks to the vector store.
        
        Args:
            chunks: List of TextChunk objects with content and metadata.
            embeddings: Corresponding embeddings for each chunk.
        """
        ids = [f"chunk_{c.chunk_index}" for c in chunks]
        documents = [c.content for c in chunks]
        metadatas = [c.to_metadata() for c in chunks]
        
        self.collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas
        )
    
    def query(
        self,
        query_embedding: list[float],
        k: int = TOP_K_RESULTS,
        where: dict | None = None
    ) -> list[RetrievalResult]:
        """
        Retrieves the most relevant chunks for a query.
        
        Args:
            query_embedding: The embedding vector of the query.
            k: Number of results to return.
            where: Optional metadata filter (e.g., {"source": "contract.pdf"}).
            
        Returns:
            List of RetrievalResult objects sorted by relevance.
        """
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=k,
            where=where,
            include=["documents", "metadatas", "distances"]
        )
        
        retrieval_results = []
        
        # Unpack results (ChromaDB returns nested lists)
        if results["documents"] and results["documents"][0]:
            for i, doc in enumerate(results["documents"][0]):
                metadata = results["metadatas"][0][i]
                distance = results["distances"][0][i]
                
                retrieval_results.append(RetrievalResult(
                    content=doc,
                    score=distance,
                    page_number=metadata.get("page_number", 0),
                    source=metadata.get("source", "unknown"),
                    chunk_index=metadata.get("chunk_index", 0)
                ))
        
        return retrieval_results
    
    def count(self) -> int:
        """Returns the number of documents in the collection."""
        return self.collection.count()
    
    def clear(self) -> None:
        """Clears all documents from the collection."""
        # Delete and recreate collection
        self.client.delete_collection(self.collection.name)
        self.collection = self.client.get_or_create_collection(
            name="legal_documents",
            metadata={"hnsw:space": "cosine"}
        )
