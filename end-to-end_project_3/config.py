"""
LegalMind AI - Configuration Management
Handles environment variables, API keys, and system paths.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# === Paths ===
PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "data"
CHROMA_PERSIST_DIR = PROJECT_ROOT / ".chroma_db"

# === LLM Configuration ===
# Supports both OpenAI and Google Gemini
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini")  # "openai" or "gemini"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")

# Model selection based on provider
LLM_MODEL = os.getenv("LLM_MODEL", "gemini-1.5-flash" if LLM_PROVIDER == "gemini" else "gpt-4o-mini")

# === Embedding Configuration ===
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
EMBEDDING_DIMENSION = 384

# === Chunking Configuration ===
CHUNK_SIZE = 500  # Characters per chunk
CHUNK_OVERLAP = 50  # Overlap between chunks

# === Retrieval Configuration ===
TOP_K_RESULTS = 5  # Number of chunks to retrieve

# === Validation ===
def validate_config():
    """Validates that required API keys are present."""
    if LLM_PROVIDER == "openai" and not OPENAI_API_KEY:
        raise EnvironmentError("OPENAI_API_KEY not set. Add to .env file.")
    if LLM_PROVIDER == "gemini" and not GOOGLE_API_KEY:
        raise EnvironmentError("GOOGLE_API_KEY not set. Add to .env file.")
    return True
