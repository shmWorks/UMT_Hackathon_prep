"""
LegalMind AI - Demo Script
Interactive CLI for analyzing legal documents.

Usage:
    uv run demo.py --doc data/sample_contract.pdf --query "What are the termination conditions?"
    uv run demo.py --ingest data/sample_contract.pdf  # Just ingest, no query
"""
import argparse
import sys
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from config import validate_config
from src.ingestion import load_document, chunk_documents
from src.vectorstore import embed_texts, ChromaStore
from src.orchestrator import run_agent


console = Console()


def ingest_document(doc_path: str) -> int:
    """Ingests a document into the vector store."""
    console.print(f"\n📄 Loading document: [cyan]{doc_path}[/cyan]")
    
    # Load and chunk
    pages = load_document(doc_path)
    console.print(f"   Found {len(pages)} pages")
    
    chunks = chunk_documents(pages)
    console.print(f"   Created {len(chunks)} chunks")
    
    # Embed
    with Progress() as progress:
        task = progress.add_task("Generating embeddings...", total=1)
        texts = [c.content for c in chunks]
        embeddings = embed_texts(texts)
        progress.update(task, completed=1)
    
    # Store
    store = ChromaStore()
    store.add_documents(chunks, embeddings)
    console.print(f"   ✅ Stored in vector database ({store.count()} total chunks)")
    
    return len(chunks)


def query_document(query: str) -> None:
    """Runs a query against the ingested documents."""
    console.print(f"\n🔍 Query: [yellow]{query}[/yellow]\n")
    
    with Progress() as progress:
        task = progress.add_task("Analyzing...", total=1)
        response = run_agent(query)
        progress.update(task, completed=1)
    
    console.print(Panel(response, title="LegalMind AI Response", border_style="green"))


def main():
    parser = argparse.ArgumentParser(description="LegalMind AI - Legal Document Analyst")
    parser.add_argument("--doc", type=str, help="Path to document (PDF/DOCX)")
    parser.add_argument("--ingest", type=str, help="Ingest document without querying")
    parser.add_argument("--query", "-q", type=str, help="Query to ask about the document")
    parser.add_argument("--clear", action="store_true", help="Clear the vector database")
    
    args = parser.parse_args()
    
    console.print(Panel.fit(
        "[bold blue]LegalMind AI[/bold blue]\n[dim]Multi-Agent Legal Document Analyst[/dim]",
        border_style="blue"
    ))
    
    # Validate config
    try:
        validate_config()
    except EnvironmentError as e:
        console.print(f"[red]Configuration Error:[/red] {e}")
        console.print("Copy .env.example to .env and add your API keys.")
        return
    
    # Handle --clear
    if args.clear:
        store = ChromaStore()
        store.clear()
        console.print("🗑️  Vector database cleared.")
        return
    
    # Handle --ingest (ingest only)
    if args.ingest:
        ingest_document(args.ingest)
        return
    
    # Handle --doc + --query
    if args.doc:
        ingest_document(args.doc)
    
    if args.query:
        query_document(args.query)
    elif not args.doc and not args.ingest:
        # Interactive mode
        console.print("\n[dim]Enter queries (Ctrl+C to exit):[/dim]")
        while True:
            try:
                query = console.input("[bold]> [/bold]")
                if query.strip():
                    query_document(query)
            except KeyboardInterrupt:
                console.print("\n[dim]Goodbye![/dim]")
                break


if __name__ == "__main__":
    main()
