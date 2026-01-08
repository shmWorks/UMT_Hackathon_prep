# 🧠 PROJECT: **LegalMind AI**

### *Multi-Agent Legal Document Analyst with RAG & LangGraph*

---

## 1. Project Overview — Problem, Solution, Value

### 🔴 The Real Problem (High-Impact, Underserved)

**Target Users**
* Law firms & paralegals
* Startup founders reviewing investor contracts
* HR teams reviewing employment agreements
* Compliance officers
* Small businesses without legal budgets

**Problem**
Legal professionals spend 60-80% of their time reading contracts to find:
* Termination conditions
* Liability caps
* Auto-renewal traps
* Hidden risks

Existing solutions:
* Ctrl+F keyword search (misses context)
* Expensive lawyers ($300-600/hour)
* Generic ChatGPT (hallucinates, no citations)

**Gap**
No system today:
* Understands *document structure* (clauses, sections, exhibits)
* Routes queries to *specialized analyzers*
* Provides *citations* back to exact page numbers
* Identifies *risks* proactively (not just answers questions)

---

### 🟢 The Solution: LegalMind AI

**LegalMind AI** is an **agentic, multi-agent legal intelligence system** that:

✔ Ingests contracts (PDF, DOCX, TXT)
✔ Chunks intelligently (paragraph-aware, with overlap)
✔ Uses **Vector DB + RAG** for grounded answers with citations
✔ Routes queries through a **Router Agent** to specialists:
  * Clause Analyzer
  * Risk Assessor
  * Summarizer
  * General Q&A
✔ Uses **LangGraph** for conditional workflow orchestration
✔ Produces **citation-backed, structured outputs**

---

### 💰 Commercial Value

**Monetization paths**
* B2B SaaS for startups ($50-200/month)
* Legal-tech API for contract management platforms
* Enterprise deployments (banks, HR departments)
* Audit trail / compliance documentation tool

This is **not a demo chatbot** — it's a *product skeleton*.

---

## 2. System Architecture (High-Level & Low-Level)

---

### 🧠 High-Level Architecture

```
User Query
   ↓
Router Agent (Classifies: Clause? Risk? Summary? QA?)
   ↓
Retriever Agent (Semantic Search in ChromaDB)
   ↓
┌──────────────┬───────────────┬──────────────┬──────────────┐
│ Clause       │ Risk          │ Summarizer   │ General      │
│ Analyzer     │ Assessor      │ Agent        │ QA Agent     │
└──────────────┴───────────────┴──────────────┴──────────────┘
            ↓
   Grounded Response + Citations
```

---

### 🔬 Low-Level Data Flow (End-to-End)

```
1. Document Ingestion (src/ingestion/)
   - PDF/DOCX loaded via pypdf/python-docx
   - Smart chunking: 500 chars, 50 overlap, paragraph-aware
   - Each chunk tagged: {source, page_number, chunk_index}

2. Embedding Pipeline (src/vectorstore/)
   - sentence-transformers/all-MiniLM-L6-v2 (local, free)
   - 384-dimensional vectors
   - Stored in ChromaDB with cosine similarity

3. User Query (demo.py)
   - Query text entered via CLI
   
4. Router Agent (src/agents/router.py)
   - LLM classifies into: CLAUSE_SEARCH, RISK_ANALYSIS, SUMMARIZE, GENERAL_QA
   
5. Retriever Agent (src/agents/retriever.py)
   - Embeds query
   - Top-5 semantic search from ChromaDB
   - Returns chunks with citations
   
6. Specialist Agent (src/agents/clause_analyzer.py, risk_assessor.py, summarizer.py)
   - Receives context + query
   - Produces structured output (Pydantic models)
   
7. Response (src/orchestrator/graph.py)
   - LangGraph compiles final state
   - Returns formatted Markdown response
```

---

## 3. Core Technical Components & Justifications

---

### 📦 Vector Database — **ChromaDB**

**Why ChromaDB?**
* Lightweight, runs locally (hackathon-friendly)
* Persistent storage (survives restarts)
* Metadata filtering (filter by source, page)
* Cosine similarity built-in

**Stored Data Structure**
```json
{
  "id": "chunk_42",
  "document": "...This Agreement shall terminate upon...",
  "metadata": {
    "source": "sample_contract.txt",
    "page_number": 3,
    "chunk_index": 42
  },
  "embedding": [0.023, -0.156, ...]
}
```

---

### 📚 RAG Pipeline (Production-Grade)

**Key Features**
| Feature | Implementation |
|---------|---------------|
| Smart Chunking | Paragraph-aware splits, 50-char overlap |
| Metadata Tracking | Source file, page number attached |
| Citation Injection | `[sample_contract.txt, Page 3]` in response |
| Confidence via Distance | Lower distance = more relevant |

This avoids **hallucination** — every claim is traceable.

---

### 🤝 Multi-Agent System (5 Specialized Agents)

| Agent | Role | Tool Access |
|-------|------|-------------|
| **Router** | Classify query intent | LLM only |
| **Retriever** | Semantic search | ChromaDB |
| **Clause Analyzer** | Extract specific clauses | LLM + Context |
| **Risk Assessor** | Identify legal red flags | LLM + Context |
| **Summarizer** | Plain-language summaries | LLM + Context |

Each agent:
* Has a **specialized prompt**
* Returns **structured output** (Pydantic)
* Is called **conditionally** by LangGraph

---

### 🔗 LangGraph State Machine

**Why LangGraph (not just chains)?**
* Conditional routing based on `state["route"]`
* State persists across all nodes
* Easy to extend with loops or human-in-the-loop

**The Graph**
```python
graph.set_entry_point("router")
graph.add_edge("router", "retriever")
graph.add_conditional_edges(
    "retriever",
    decide_next_node,  # Returns "clause_search", "risk_analysis", etc.
    {
        "clause_search": "clause_search",
        "risk_analysis": "risk_analysis",
        "summarize": "summarize",
        "general_qa": "general_qa"
    }
)
# All specialist nodes → END
```

Judges love **LangGraph** because it shows *system thinking*, not just prompting.

---

## 4. Production-Quality Code Walkthrough

Below is a guided tour of the key files.

---

### `config.py` — Environment Management

```python
# Supports both OpenAI and Gemini
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini")  

# Model selection
LLM_MODEL = os.getenv("LLM_MODEL", "gemini-1.5-flash")

# Embedding (local, free)
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Chunking strategy
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
```

**Why this matters:** Swap `gemini` → `openai` with one env var change.

---

### `src/ingestion/chunker.py` — Smart Chunking

```python
def chunk_text(text: str, chunk_size=500, overlap=50) -> list[str]:
    """
    Splits text into overlapping chunks.
    Tries to break at paragraph boundaries when possible.
    """
    # Look for \n\n near chunk end
    para_break = text.rfind("\n\n", search_start, end)
    if para_break != -1:
        end = para_break + 2
```

**Why this matters:** Breaking mid-sentence loses context. This preserves meaning.

---

### `src/vectorstore/chroma_store.py` — Vector Operations

```python
class ChromaStore:
    def query(self, query_embedding, k=5, where=None):
        """
        Retrieves top-k chunks with optional metadata filtering.
        
        Args:
            where: {"source": "contract.pdf"} to filter
        """
        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=k,
            where=where
        )
```

**Why this matters:** Metadata filtering lets you scope queries to specific documents.

---

### `src/agents/router.py` — Query Classification

```python
ROUTER_PROMPT = """Classify the query into ONE of:
- CLAUSE_SEARCH: Looking for specific clauses
- RISK_ANALYSIS: Wants legal risks
- SUMMARIZE: Wants a summary
- GENERAL_QA: General question

Respond with ONLY the category name."""

def route_query(query: str) -> str:
    response = invoke_llm(ROUTER_PROMPT.format(query=query))
    # Robust parsing handles LLM variations
    for route in valid_routes:
        if route in response.upper():
            return route
    return "GENERAL_QA"  # Safe fallback
```

**Why this matters:** Deterministic routing ensures the right specialist handles each query.

---

### `src/agents/risk_assessor.py` — Structured Risk Output

```python
class RiskItem(BaseModel):
    risk_title: str
    severity: str  # HIGH, MEDIUM, LOW
    description: str
    recommendation: str

def assess_risks(context: str) -> RiskReport:
    """Returns structured risk report with severity levels."""
```

**Why Pydantic?**
* Validates LLM output structure
* Easy to serialize to JSON/API
* Type hints for IDE autocomplete

---

### `src/orchestrator/graph.py` — LangGraph Workflow

```python
from langgraph.graph import StateGraph, END

class AgentState(TypedDict):
    query: str
    route: str
    context: str
    response: str
    citations: list[str]

def build_graph():
    graph = StateGraph(AgentState)
    
    # Add nodes
    graph.add_node("router", router_node)
    graph.add_node("retriever", retriever_node)
    graph.add_node("clause_search", clause_search_node)
    # ... other specialist nodes
    
    # Conditional routing
    graph.add_conditional_edges(
        "retriever",
        decide_next_node,
        {"clause_search": "clause_search", ...}
    )
    
    return graph.compile()
```

**The Key Insight:** State flows through nodes. Each node reads and updates state.

---

## 5. How To Run (Quick Start)

```bash
# 1. Install dependencies
cd end-to-end_project_3
uv sync

# 2. Configure API key
cp .env.example .env
# Edit .env: GOOGLE_API_KEY=your-key-here

# 3. Ingest a document
uv run demo.py --ingest data/sample_contract.txt

# 4. Query it
uv run demo.py --query "What are the termination conditions?"
uv run demo.py --query "Analyze risks in this contract"
uv run demo.py --query "Summarize this agreement"

# 5. Interactive mode
uv run demo.py
> What is the liability cap?
> Are there any auto-renewal clauses?
```

---

## 6. Performance, Scalability, Cost

### ⚡ Performance
* Local embeddings (no API call for embedding)
* ChromaDB on disk (instant startup)
* Lazy model loading (only loads when first query)

### 📈 Scalability
* Swap ChromaDB → Pinecone for cloud scale
* Each agent is stateless → horizontal scaling
* API-ready architecture (wrap `run_agent()` in FastAPI)

### 💸 Cost Control
* Gemini Flash = $0.075/1M input tokens (very cheap)
* Local embeddings = $0
* Retrieval-first = only relevant context sent to LLM

---

## 7. Hackathon Pitch (2-Minute Judge Version)

> "Every startup founder signs contracts they don't fully understand. Miss one auto-renewal clause, and you're locked in for a year.
>
> **LegalMind AI** is not ChatGPT with documents. It's a **multi-agent system** that:
> 1. **Routes** your question to a specialist agent
> 2. **Retrieves** relevant clauses with citations
> 3. **Analyzes** for risks and red flags
> 4. **Summarizes** in plain English
>
> Upload a contract. Ask 'What can hurt me?' Get a risk matrix in 60 seconds.
>
> Built with LangGraph, ChromaDB, and Gemini. Production-ready. No hallucinations. Every answer cites the source."

---

## 🏆 Why This Wins (Explicitly)

| Criterion | Why It Scores High |
|-----------|-------------------|
| **Innovation (15%)** | Multi-agent routing, specialized analyzers |
| **Technical Execution (30%)** | LangGraph state machine, Pydantic outputs, local embeddings |
| **Feasibility (15%)** | Works offline, uses free/cheap APIs |
| **Real-world Impact (15%)** | $10B legal-tech market, real pain point |
| **Presentation (25%)** | Clear demo: upload → query → cited answer |

---

## 8. Hackathon Survival Tips

1. **Hours 0-2:** Get sample contract ingested into ChromaDB. Verify retrieval works.
2. **Hours 2-6:** Build Router → Retriever → One Specialist path. Test end-to-end.
3. **Hours 6-12:** Add remaining specialists (Risk, Summary, etc).
4. **Hours 12-16:** Polish output formatting, add citations.
5. **Hours 16-18:** Create demo script, practice the pitch.

**The Demo Moment:**
* Ask "What risks should I be aware of?"
* Watch it return a structured risk matrix with severity levels
* Point at the citations: "Every risk is traceable to the source. No hallucination."

---

## 9. Key Learnings for Your Hackathon

### Pattern 1: State-Driven Architecture
```python
# Instead of passing arguments everywhere:
response = analyze(query, context, config, ...)

# Use a state dict:
state = {"query": q, "context": c, "response": ""}
state = node_1(state)
state = node_2(state)
```

### Pattern 2: Graceful LLM Parsing
```python
# LLMs aren't perfect. Handle variations:
for route in valid_routes:
    if route in response.upper():
        return route
return "FALLBACK"  # Always have a default
```

### Pattern 3: Metadata is Power
```python
# Don't just store text. Store WHERE it came from:
{"content": "...", "page": 3, "source": "contract.pdf"}
# Now you can cite sources and filter by document
```

### Pattern 4: Structured Outputs Beat Free Text
```python
# Instead of: "There are some risks..."
# Return:
class RiskItem(BaseModel):
    risk_title: str
    severity: Literal["HIGH", "MEDIUM", "LOW"]
    recommendation: str
```

---

## 10. File Map (Your Learning Path)

| Order | File | What You Learn |
|-------|------|----------------|
| 1 | `config.py` | Environment management, provider switching |
| 2 | `src/ingestion/document_loader.py` | PDF/DOCX loading patterns |
| 3 | `src/ingestion/chunker.py` | Smart text splitting with overlap |
| 4 | `src/vectorstore/embedder.py` | Lazy model loading, batch embedding |
| 5 | `src/vectorstore/chroma_store.py` | ChromaDB CRUD operations |
| 6 | `src/agents/router.py` | LLM-based classification |
| 7 | `src/agents/retriever.py` | Vector search + citation formatting |
| 8 | `src/agents/clause_analyzer.py` | Structured extraction with Pydantic |
| 9 | `src/agents/risk_assessor.py` | Complex structured output parsing |
| 10 | `src/orchestrator/graph.py` | LangGraph state machine |
| 11 | `demo.py` | CLI patterns with Rich |

**Study this order. Each file builds on the previous.**

---

🚀 **You now have a complete, production-grade reference architecture. Adapt it for your hackathon problem.**
