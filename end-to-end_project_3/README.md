# LegalMind AI

**Multi-Agent Legal Document Analyst with RAG and LangGraph Orchestration**

A hackathon-winning AI system that analyzes legal documents using specialized agents for clause extraction, risk assessment, and executive summarization.

## 🎯 What It Does

Upload a contract → Get instant analysis:
- **Clause Search**: Find specific clauses (termination, liability, payment)
- **Risk Analysis**: Identify red flags and legal risks with severity levels
- **Summarization**: Get executive summaries for non-lawyers
- **Q&A**: Ask any question about the document

## 🏗️ Architecture

```
User Query → Router Agent → [Specialist Agents] → Response
                   ↓
         LangGraph Orchestrator
                   ↓
    ┌──────────────┴──────────────┐
    │  ChromaDB + Embeddings      │
    │  (Semantic Search Layer)    │
    └─────────────────────────────┘
```

### Agent Roles
| Agent | Function |
|-------|----------|
| **Router** | Classifies query type |
| **Retriever** | Semantic search with citations |
| **Clause Analyzer** | Extracts specific clause info |
| **Risk Assessor** | Identifies legal risks |
| **Summarizer** | Plain-language summaries |

## 🚀 Quick Start

### 1. Setup
```bash
cd end-to-end_project_3
uv sync
cp .env.example .env
# Add your API key to .env
```

### 2. Ingest a Document
```bash
uv run demo.py --ingest data/sample_contract.txt
```

### 3. Query the Document
```bash
uv run demo.py --query "What are the termination conditions?"
uv run demo.py --query "Analyze risks in this contract"
uv run demo.py --query "Summarize this agreement"
```

### 4. Interactive Mode
```bash
uv run demo.py
# Then type your queries
```

## 📁 Project Structure

```
end-to-end_project_3/
├── pyproject.toml          # uv dependencies
├── config.py               # Environment configuration
├── demo.py                 # CLI entry point
├── src/
│   ├── ingestion/          # Document loading & chunking
│   ├── vectorstore/        # Embeddings & ChromaDB
│   ├── agents/             # Specialized AI agents
│   ├── orchestrator/       # LangGraph workflow
│   └── llm/                # LLM API wrapper
└── data/
    └── sample_contract.txt # Demo document
```

## 🛠️ Tech Stack

- **LangGraph**: Multi-agent orchestration
- **ChromaDB**: Vector storage with metadata
- **sentence-transformers**: Local embeddings
- **LangChain**: LLM integrations
- **Rich**: Beautiful CLI output

## 💡 Why This Wins

1. **Innovation**: Multi-agent with conditional routing, not basic RAG
2. **Technical Depth**: LangGraph state machines, structured outputs
3. **Practical Impact**: Solves real $10B legal-tech problem
4. **Demo-Ready**: 60-second demo from upload to risk report

## 📄 License

MIT License - Built for Techverse AI Hackathon 2026
