# AI Engineering System Design: Master Knowledge Base

**Domain:** AI Engineering, LLMs, RAG, Agents, MLOps
**Source:** AI Engineering 2025 Edition (Pachaar & Chawla)
**Context:** System Design Patterns & Implementation Details

---

## 1. Large Language Models (LLMs)

### Core Mechanics
*   **Definition:** Probabilistic models trained to predict the next token in a sequence ($P(w_t | w_{1:t-1})$).
*   **Architecture:** Transformer (Decoder-only stack).
    *   **Mechanism:** Self-Attention (process all input tokens simultaneously).
    *   **Positional Encoding:** Injects sequence order information.
*   **Scaling Laws:** Capabilities emerge from scale (Parameters + Data + Compute).

### Generation Control Parameters
Use these levers to control deterministic vs. stochastic behavior:
1.  **Temperature:** Controls randomness in Softmax.
    *   `Low (~0.1)`: Deterministic, focused (Code/Math).
    *   `High (~0.8)`: Creative, diverse (Brainstorming).
2.  **Top-k:** Samples from the top $k$ most likely tokens only.
3.  **Top-p (Nucleus):** Samples from the smallest set of tokens whose cumulative probability exceeds $p$.
4.  **Frequency Penalty:** Penalizes tokens based on how many times they have appeared so far (reduces verbatim repetition).
5.  **Presence Penalty:** Penalizes tokens if they have appeared at all (encourages new topics).
6.  **Min-p:** Dynamic threshold; ignores tokens with probability $< p \times P(top\_token)$.

### Decoding Strategies
| Strategy | Description | Best Use Case |
| :--- | :--- | :--- |
| **Greedy** | Always picks highest probability token. | Deterministic tasks. |
| **Multinomial** | Samples based on probability distribution. | Creative writing. |
| **Beam Search** | Maintains $k$ best sequences; maximizes global probability. | Translation/Summarization. |
| **Contrastive** | Penalizes repetition based on similarity to context. | Long-form generation. |

---

## 2. Prompt Engineering

### Reasoning Patterns
*   **Chain of Thought (CoT):** Forces intermediate reasoning steps before the answer.
    *   *Prompt:* "Think step by step."
*   **Self-Consistency:** Generates multiple reasoning paths, then takes a majority vote.
*   **Tree of Thoughts (ToT):** Explores branching reasoning paths; evaluates states to backtrack or proceed.
*   **Verbalized Sampling:** Ask LLM to generate diverse possibilities explicitly to avoid mode collapse (Typicality Bias).

### Structured Output (JSON)
*   **Mechanism:** Constrains output to valid JSON schema.
*   **Benefit:** Deterministic parsing for downstream APIs.
*   **Implementation:** Use Markdown or specific system prompts defining schemas.

### Context Engineering (CE)
*   **Definition:** The architecture of information flow into the context window.
*   **The 6 CE Layers:**
    1.  **Instructions:** Persona, Goals.
    2.  **Examples:** Few-shot inputs.
    3.  **Knowledge:** Domain data/RAG.
    4.  **Memory:** Short-term (session) vs. Long-term (user facts).
    5.  **Tools:** Available function definitions.
    6.  **Guardrails:** Safety/Compliance boundaries.

---

## 3. Fine-Tuning

### Strategy Decision Matrix
*   **Use Prompt Engineering:** If you need to change behavior slightly/temporarily.
*   **Use RAG:** If you need new knowledge (facts not in training data).
*   **Use Fine-Tuning:** If you need to change the **form/structure** or specialized **style** of output.
*   **Use SFT (Supervised Fine-Tuning):** If you have a large labeled dataset.
*   **Use RFT (Reinforcement Fine-Tuning):** If you have verifiable rewards (math/code) or need reasoning (GRPO).

### Parameter Efficient Fine-Tuning (PEFT)
#### LoRA (Low-Rank Adaptation)
*   **Concept:** Freezes pre-trained weights ($W$). Injects trainable rank decomposition matrices ($A$ and $B$).
*   **Equation:** $W_{new} = W + \Delta W = W + \alpha (A \times B)$
    *   $A \in \mathbb{R}^{d \times r}, B \in \mathbb{R}^{r \times k}$ where $r \ll d$.
*   **Advantages:** drastically reduced VRAM usage; modular adapters.

#### Variants
*   **QLoRA:** LoRA + 4-bit Quantization of base model.
*   **DoRA:** Decomposes weights into Magnitude and Direction for better stability.
*   **LoRA-FA:** Freezes matrix A, trains only B.

### DeepSeek GRPO (Group Relative Policy Optimization)
*   **Use Case:** Reasoning models (like R1).
*   **Method:** Removes the "Critic" model requirement in PPO. Uses group scores to normalize rewards.
*   **Workflow:** Generate $N$ outputs $\rightarrow$ Score verification $\rightarrow$ Update policy based on group relative advantage.

---

## 4. RAG (Retrieval Augmented Generation)

### Core Workflow
1.  **Chunking:** Splitting text (Fixed-size, Semantic, or Recursive).
2.  **Embedding:** Vectorizing chunks (Bi-encoders).
3.  **Indexing:** Storing in Vector DB (Milvus, Pinecone).
4.  **Retrieval:** ANN search (Cosine Similarity).
5.  **Generation:** Injecting context into prompt.

### Advanced RAG Architectures
1.  **HyDE (Hypothetical Document Embeddings):** LLM generates a fake answer $\rightarrow$ Embed fake answer $\rightarrow$ Retrieve real docs similar to fake answer. *Solves query-document semantic mismatch.*
2.  **GraphRAG:** Uses Knowledge Graphs to capture entity relationships.
3.  **Agentic RAG:** Agent plans retrieval steps (e.g., Rewrites query $\rightarrow$ Selects Source $\rightarrow$ Validates Context).
4.  **Corrective RAG (CRAG):** Evaluates retrieved documents; if low confidence, falls back to web search.
5.  **CAG (Cache-Augmented Generation):** Pre-loads "cold" (static) context into KV-Cache; retrieves only "hot" (dynamic) data.

---

## 5. AI Agents

### Definition
**Agent = LLM (Brain) + Memory + Planning + Tools**

### Design Patterns
1.  **ReAct (Reason + Act):** Loop of `Thought -> Action -> Observation -> Thought`.
2.  **Reflection:** Agent critiques its own output before finalizing.
3.  **Tool Use:** Dynamic selection of APIs.
4.  **Planning:** Breaking complex goals into sequential sub-tasks.
5.  **Multi-Agent Orchestration:**
    *   *Router:* Directs task to specialized agent.
    *   *Hierarchical:* Boss agent delegates to worker agents.
    *   *Sequential:* Assembly line processing.

### Protocols
*   **MCP (Model Context Protocol):** Standardized interface connecting AI models to data/tools.
    *   *Primitives:* Tools (Exec), Resources (Read), Prompts (Templates).
    *   *Benefit:* $M$ Apps $\times$ $N$ Tools becomes $M+N$ integrations.
*   **A2A (Agent-to-Agent):** Protocol for agents to discover and collaborate without sharing internal state.
*   **AG-UI:** Protocol for streaming agent state/actions to frontend UIs.

---

## 6. Optimization

### Techniques
1.  **Quantization:** Reducing precision (FP32 $\rightarrow$ INT8/INT4). Trade-off: Memory vs. Precision.
2.  **Pruning:** Removing redundant weights/neurons.
3.  **Distillation:** Training a small "Student" to mimic a large "Teacher" (Soft labels or Hard labels).

### Inference Optimization (vLLM)
*   **Continuous Batching:** dynamic batching that doesn't wait for all sequences to finish.
*   **PagedAttention:** Stores KV-Cache in non-contiguous memory blocks (like OS virtual memory) to eliminate fragmentation.
*   **KV Caching:** Caching Attention Key/Value vectors to avoid re-computation in autoregressive steps.
*   **Prefix Caching:** Sharing KV cache for common system prompts across requests.

---

## 7. Observability & Evaluation

### Evaluation (Offline)
*   **Metrics:** Not just accuracy. Correctness, Faithfulness, Relevance.
*   **LLM-as-a-Judge:** Using a strong model (GPT-4) to score outputs of a weaker model.
*   **G-Eval:** Framework for creating custom evaluation metrics using Chain-of-Thought prompting.
*   **Red Teaming:** Adversarial testing for bias, toxicity, and jailbreaks (e.g., DeepTeam).

### Observability (Online)
*   **Tracing:** monitoring individual steps in a chain (Retriever latency, LLM token usage, Tool outputs).
*   **Tools:** Opik, LangSmith.

---

## 8. Implementation Snippets (Python/Unsloth/vLLM)

### LoRA Config (Unsloth)
```python
from unsloth import FastLanguageModel
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = "unsloth/Qwen2.5-7B-Instruct",
    max_seq_length = 2048,
    load_in_4bit = True,
)
model = FastLanguageModel.get_peft_model(
    model,
    r = 16, # Rank
    target_modules = ["q_proj", "k_proj", "v_proj", "o_proj"],
    lora_alpha = 16,
    lora_dropout = 0,
    use_gradient_checkpointing = "unsloth",
)
```

### ReAct Loop Logic (Simplified)
```python
def react_loop(query, tools):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": query}]
    while True:
        response = llm.chat(messages)
        if "Action:" in response:
            tool_name, args = parse_action(response)
            result = tools[tool_name](args)
            messages.append({"role": "user", "content": f"Observation: {result}"})
        elif "Answer:" in response:
            return response
```

### MCP Server (mcp-use)
```typescript
import { createMCPServer } from "mcp-use/server";

// Define a tool
server.tool({
    name: "get_weather",
    inputs: { location: { type: "string" } },
    cb: async ({ location }) => {
        return { temperature: 72, condition: "Sunny" };
    }
});
```

Here is the continuation and completion of the **AI Engineering System Design** knowledge base, specifically targeting the requested technologies (Models, Vector DBs, Frameworks) based strictly on the provided source material constraints and implementation examples.

***

## 9. Model Landscape & Specific Capabilities

### Proprietary Models (The "Brains")
*   **GPT-4o (OpenAI):**
    *   **Role in Material:** Used as the baseline "strong model" for **LLM-as-a-Judge** and **G-Eval** metrics.
    *   **Integration:** Standard for testing agent flows via the OpenAI API client.
    *   **Specific Capability:** Apps SDK support for rendering interactive UI widgets (via MCP).
*   **Claude 3.5 Sonnet / Opus (Anthropic):**
    *   **Role in Material:** The reference model for **MCP (Model Context Protocol)** and **Context Engineering**.
    *   **Specific Capability:**
        *   **Claude Skills:** A 3-layer context management system (Main Context $\rightarrow$ Skill Metadata $\rightarrow$ Active Skill) to handle reusable workflows without context overflow.
        *   **Desktop App:** Acts as a primary **MCP Host** client.
*   **Gemini 1.5/2.5 Pro (Google):**
    *   **Role:** Mentioned in the context of **Verbalized Sampling**.
    *   **Performance:** Larger models like Gemini benefit more from diversity prompting strategies (1.6x-2.1x gains) compared to smaller models.

### Open-Weights Models (The "Workhorses")
*   **DeepSeek (R1 & V3):**
    *   **Specialty:** Reasoning-heavy tasks.
    *   **Training:** The primary subject of **Distillation** (Teacher model) and **GRPO** (Reasoning fine-tuning).
*   **Llama 3 / 3.1 (Meta):**
    *   **Role:** The standard for **Local Deployment** and **Fine-tuning**.
    *   **Implementation:** Used in `Unsloth` examples for GRPO and `vLLM` for serving.
*   **Qwen 2.5:**
    *   **Role:** Used as the base model for reasoning fine-tuning demonstrations.

---

## 10. Vector Databases & Retrieval Infrastructure

*Source material emphasizes specific implementation stacks over general market lists.*

### Core Function
**Vector DBs** act as the **Long-Term Memory** for RAG and Agents. They store embeddings (numerical representations of text) to enable semantic similarity search.

### Implementation Stack (From Source)
1.  **Milvus (Self-Hosted):**
    *   **Usage:** The chosen Vector DB for the **Context Engineering Workflow** example.
    *   **Function:** Stores RAG-ready chunks + Metadata.
    *   **Integration:** Accessed via `pymilvus` client.
2.  **Tensorlake:**
    *   **Usage:** **Ingestion Layer**. Converts complex documents (PDFs) into RAG-ready markdown chunks before embedding.
    *   **Benefit:** Handles parsing logic so the Vector DB receives clean data.
3.  **Concept - The "Memory" Stack:**
    *   While specific DBs like **Pinecone**, **Chroma**, or **FAISS** are standard industry alternatives, the source material focuses on **Zep** for the *Memory Layer* (Temporal Knowledge Graphs) distinct from the Vector DB used for document retrieval.

---

## 11. Orchestration Frameworks & Libraries

### Orchestration (Building the Graph)
1.  **CrewAI:**
    *   **Status:** The primary framework used for **Multi-Agent Systems** in the source.
    *   **Key Primitives:** `Agent`, `Task`, `Crew`, `Process`.
    *   **Design Pattern:** Heavily relies on **ReAct** logic and **Role-Playing**.
    *   **Integration:** Native support for MCP tools.
2.  **LangGraph:**
    *   **Status:** Mentioned as a robust backend for building stateful agent workflows.
    *   **Challenge:** Implementing custom WebSocket logic and UI adapters can be messy.
    *   **Solution:** Can emit **AG-UI** events to standardize frontend communication.
3.  **Mastra:**
    *   **Status:** Listed as a TypeScript-first agent development toolkit compatible with AG-UI.

### Training & Fine-Tuning Libraries
1.  **Unsloth:**
    *   **Purpose:** Efficient Fine-tuning (SFT, GRPO).
    *   **Optimization:** Makes LoRA/QLoRA training up to 2x faster with 70% less memory.
    *   **Key Function:** `FastLanguageModel.from_pretrained()`.
2.  **HuggingFace TRL (Transformer Reinforcement Learning):**
    *   **Purpose:** Provides the trainer loop (`GRPOTrainer`) for Reinforcement Fine-Tuning.
    *   **Integration:** Works in tandem with Unsloth for the model backend.

---

## 12. Deployment & Developer Experience (DX)

### Github Copilot / Cursor (AI IDEs)
*   **Context:** The source material frames these not just as tools to *use*, but as architectures to *emulate* or *integrate with*.
*   **Cursor as MCP Host:** The source explicitly mentions Cursor (an AI-enhanced IDE) as a "Host" in the MCP architecture. This means Cursor can connect to your local MCP servers to gain access to your custom tools and data.
*   **CopilotKit:**
    *   **Role:** The "Stripe for AI integration".
    *   **Function:** Provides the **AG-UI (Agent-User Interaction Protocol)**.
    *   **Goal:** To build "Copilot-like" experiences (streaming text, tool visualization, state syncing) inside your own applications without rebuilding the infrastructure from scratch.

### Serving Engines
*   **vLLM:**
    *   **Role:** High-performance inference engine.
    *   **Key Tech:** **PagedAttention** (non-contiguous memory management) and **Continuous Batching**.
    *   **API:** OpenAI-compatible server (`python -m vllm.entrypoints.api_server`).
*   **LitServe:**
    *   **Role:** Flexible serving layer built on PyTorch Lightning.
    *   **Use Case:** When you need custom pre-processing, post-processing, or complex routing logic wrapping the model.

---

## 13. Summary of Protocols (The "Glue")

To build the systems described in the source, you must understand the three critical protocols:

| Protocol | Scope | Purpose | Source Equivalent |
| :--- | :--- | :--- | :--- |
| **MCP** | Agent $\leftrightarrow$ Tool | Standardizes how AI connects to data/tools. | *USB-C for AI* |
| **A2A** | Agent $\leftrightarrow$ Agent | Standardizes how agents collaborate/delegate. | *Manager-Worker Comms* |
| **AG-UI** | Agent $\leftrightarrow$ User | Standardizes streaming, state-sync, and UI rendering. | *Frontend/Backend API* |
