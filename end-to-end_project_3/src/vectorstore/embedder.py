"""
Embedding Module
Generates vector embeddings for text using sentence-transformers.
"""
from typing import Sequence
import sys
sys.path.append(str(__file__).rsplit("src", 1)[0])
from config import EMBEDDING_MODEL


# Lazy-loaded model to avoid loading on import
_model = None


def get_embedding_model():
    """Lazily loads the embedding model on first use."""
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        _model = SentenceTransformer(EMBEDDING_MODEL)
    return _model


def embed_texts(texts: Sequence[str]) -> list[list[float]]:
    """
    Generates embeddings for a list of texts.
    
    Args:
        texts: List of text strings to embed.
        
    Returns:
        List of embedding vectors (each is a list of floats).
    """
    model = get_embedding_model()
    embeddings = model.encode(texts, convert_to_numpy=True)
    return embeddings.tolist()


def embed_single(text: str) -> list[float]:
    """
    Generates embedding for a single text.
    
    Args:
        text: Text string to embed.
        
    Returns:
        Embedding vector as list of floats.
    """
    return embed_texts([text])[0]
