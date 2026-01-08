"""
Text Chunking Module
Splits documents into semantically meaningful chunks for embedding.
"""
from dataclasses import dataclass
import sys
sys.path.append(str(__file__).rsplit("src", 1)[0])
from config import CHUNK_SIZE, CHUNK_OVERLAP


@dataclass
class TextChunk:
    """A chunk of text with source metadata for citations."""
    content: str
    chunk_index: int
    page_number: int
    source: str
    
    def to_metadata(self) -> dict:
        """Returns metadata dict for vector store."""
        return {
            "chunk_index": self.chunk_index,
            "page_number": self.page_number,
            "source": self.source
        }


def chunk_text(
    text: str,
    chunk_size: int = CHUNK_SIZE,
    overlap: int = CHUNK_OVERLAP
) -> list[str]:
    """
    Splits text into overlapping chunks.
    
    Uses a simple character-based approach with paragraph-aware splitting.
    Tries to break at paragraph boundaries when possible.
    
    Args:
        text: The input text to chunk.
        chunk_size: Target size of each chunk in characters.
        overlap: Number of overlapping characters between chunks.
        
    Returns:
        List of text chunks.
    """
    if len(text) <= chunk_size:
        return [text]
    
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        
        # Try to find a paragraph break near the end
        if end < len(text):
            # Look for paragraph break in last 20% of chunk
            search_start = end - int(chunk_size * 0.2)
            para_break = text.rfind("\n\n", search_start, end)
            
            if para_break != -1:
                end = para_break + 2  # Include the newlines
            else:
                # Fall back to sentence break
                sentence_break = text.rfind(". ", search_start, end)
                if sentence_break != -1:
                    end = sentence_break + 2
        
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        
        # Move start forward, accounting for overlap
        start = end - overlap if end < len(text) else len(text)
    
    return chunks


def chunk_documents(pages: list) -> list[TextChunk]:
    """
    Chunks a list of DocumentPage objects into TextChunks.
    
    Args:
        pages: List of DocumentPage objects from document_loader.
        
    Returns:
        List of TextChunk objects with full metadata.
    """
    all_chunks = []
    global_index = 0
    
    for page in pages:
        raw_chunks = chunk_text(page.content)
        
        for chunk_text_content in raw_chunks:
            all_chunks.append(TextChunk(
                content=chunk_text_content,
                chunk_index=global_index,
                page_number=page.page_number,
                source=page.source
            ))
            global_index += 1
    
    return all_chunks
