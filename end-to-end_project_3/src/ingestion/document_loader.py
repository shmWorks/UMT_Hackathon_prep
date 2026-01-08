"""
Document Loader Module
Handles loading PDF and DOCX files into raw text with metadata.
"""
from pathlib import Path
from dataclasses import dataclass


@dataclass
class DocumentPage:
    """Represents a single page/section of a document."""
    content: str
    page_number: int
    source: str  # Original filename


def load_pdf(file_path: Path) -> list[DocumentPage]:
    """
    Loads a PDF file and returns a list of DocumentPage objects.
    
    Args:
        file_path: Path to the PDF file.
        
    Returns:
        List of DocumentPage objects, one per page.
    """
    from pypdf import PdfReader
    
    reader = PdfReader(file_path)
    pages = []
    
    for i, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        if text.strip():  # Skip empty pages
            pages.append(DocumentPage(
                content=text,
                page_number=i + 1,
                source=file_path.name
            ))
    
    return pages


def load_docx(file_path: Path) -> list[DocumentPage]:
    """
    Loads a DOCX file and returns content as a single DocumentPage.
    
    DOCX files don't have native page numbers, so we treat as single document.
    """
    from docx import Document
    
    doc = Document(file_path)
    full_text = "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
    
    return [DocumentPage(
        content=full_text,
        page_number=1,
        source=file_path.name
    )]


def load_document(file_path: str | Path) -> list[DocumentPage]:
    """
    Universal document loader. Detects file type and uses appropriate loader.
    
    Args:
        file_path: Path to document (PDF or DOCX).
        
    Returns:
        List of DocumentPage objects.
        
    Raises:
        ValueError: If file type is not supported.
    """
    path = Path(file_path)
    
    if not path.exists():
        raise FileNotFoundError(f"Document not found: {path}")
    
    suffix = path.suffix.lower()
    
    if suffix == ".pdf":
        return load_pdf(path)
    elif suffix in (".docx", ".doc"):
        return load_docx(path)
    else:
        raise ValueError(f"Unsupported file type: {suffix}. Use PDF or DOCX.")
