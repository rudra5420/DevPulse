Running notes on AI/ML concepts, updated as I learn. Focused on practical understanding over pure theory.

---

## 1. LLM Basics

What an LLM is: a neural network (almost always a Transformer) trained to predict the next token in a sequence, at massive scale, over massive text/code corpora.

Key building blocks:
- **Tokenization** — text is split into subword tokens (e.g. via BPE) before being fed to the model. Token count, not word count, is what matters for context limits and cost.
- **Context window** — the maximum number of tokens (input + output) the model can attend to in one pass. Bigger isn't always better; relevant info can still get lost in the middle of a long context.
- **Attention** — each token computes a weighted relevance score against every other token in the context, letting the model figure out which earlier tokens matter for predicting the next one.
- **Training stages**, roughly:
  1. Pretraining — next-token prediction over huge unlabeled corpora.
  2. Instruction tuning (SFT) — fine-tuning on (prompt, ideal response) pairs.
  3. Preference tuning (RLHF/DPO) — aligning outputs to human preference judgments.
- **Sampling parameters**:
  - `temperature` — higher = more random/creative, lower = more deterministic.
  - `top_p` (nucleus sampling) — only sample from the smallest set of tokens whose cumulative probability exceeds p.
  - `max_tokens` — caps the length of generated output.

Things that trip people up:
- LLMs don't "look things up" by default — they generate from learned patterns, which is why hallucination happens for facts that are obscure or post-training-cutoff.
- A model's knowledge cutoff is different from "now" — always worth checking if a fact could be stale.

---

## 2. Prompt Engineering

Core techniques:
- **Zero-shot** — just ask. Works well for tasks the model has clearly seen a lot of during training.
- **Few-shot** — give 2–5 examples of (input → output) before the real task. Helps lock in format and style.
- **Chain-of-thought (CoT)** — ask the model to reason step by step before giving a final answer. Improves performance on multi-step reasoning/math tasks.
- **Role/system prompting** — set persona, constraints, and tone in a system message, separate from the user's actual request.
- **Structured output prompting** — explicitly request JSON/XML and specify the schema; much more reliable than asking for a list in prose.

Practical tips:
- Be explicit about format, length, and constraints — models default to "reasonable guess" when instructions are vague.
- Put the most important instructions near the start and end of a long prompt (positional bias is real).
- Iterate like you would with code: treat a prompt as something you test and refine, not something you get right on the first try.

---

## 3. RAG (Retrieval-Augmented Generation)

Why it exists: LLMs can't know everything, and fine-tuning new facts in is slow and expensive. RAG instead retrieves relevant documents at query time and stuffs them into the prompt, so the model can answer from up-to-date, specific source material.

Typical pipeline:
1. **Chunking** — split source documents into smaller passages (by tokens, sentences, or semantic boundaries).
2. **Embedding** — convert each chunk into a vector using an embedding model.
3. **Indexing** — store vectors in a vector database for fast similarity search.
4. **Retrieval** — at query time, embed the user's question and fetch the top-k most similar chunks.
5. **Re-ranking** (optional) — use a smaller, more precise model to re-score retrieved chunks before passing the best ones to the LLM.
6. **Generation** — the LLM answers using the retrieved context plus the original question.

Common failure modes:
- Bad chunking: too large = irrelevant content dilutes the answer; too small = loses context.
- Retrieving documents that are topically similar but don't actually answer the question.
- No re-ranking step, so noisy results reach the model directly.

---

## 4. Embeddings

What they are: dense numeric vectors that represent the meaning of text (or images, audio, etc.), such that semantically similar inputs end up close together in vector space.

Similarity measures:
- **Cosine similarity** — most common; measures the angle between two vectors, ignoring magnitude.
- **Dot product / Euclidean distance** — alternatives, sometimes used depending on whether the embedding model normalizes vectors.

Common uses:
- Semantic search — find documents related in meaning, not just keyword overlap
- Clustering — group similar items without labels
- Recommendation systems
- Deduplication / near-duplicate detection
- The retrieval step in RAG

Practical note: embedding model choice matters — a model trained on general web text may underperform on code or domain-specific text (e.g. legal, medical) compared to a model fine-tuned for that domain.

---

## 5. AI Agents

Definition: an LLM wrapped in a loop that can decide actions, call tools, observe results, and decide again — rather than producing a single one-shot response.

Typical agent loop:
1. **Plan** — decide what needs to happen to answer the request.
2. **Act** — call a tool (search, code execution, an API, a database query).
3. **Observe** — read the tool's result.
4. **Repeat or finish** — loop again if more steps are needed, or return a final answer.

Memory in agents:
- **Short-term** — the current conversation/context window.
- **Long-term** — external storage (vector DB, structured DB) the agent can read/write across sessions.

Multi-agent systems: instead of one agent doing everything, split responsibilities across specialized agents (e.g. a planner, a researcher, a coder) that communicate with each other — can improve reliability on complex tasks but adds coordination overhead and cost.

Evaluation is the hard part: agents fail in ways that are hard to catch with simple accuracy metrics (wrong tool choice, infinite loops, silently wrong intermediate steps). Logging every step, not just final output, is essential for debugging.

---

## 6. Fine-Tuning

When to fine-tune vs. not:
- Prompt engineering first — cheapest, fastest to iterate.
- RAG next — if the problem is "the model doesn't know this fact/document".
- Fine-tuning last — if the problem is "the model knows the facts but doesn't behave/format/reason the way I need", and you have enough quality training examples.

Approaches:
- **Full fine-tuning** — update all model weights. Expensive, needs a lot of data and compute.
- **Parameter-efficient fine-tuning (PEFT)**:
  - **LoRA** (Low-Rank Adaptation) — freeze the base model, train small low-rank adapter matrices injected into specific layers. Much cheaper, easy to swap adapters per task.
  - **QLoRA** — LoRA combined with a quantized (lower-precision) base model, cutting memory requirements further.

Risks:
- **Catastrophic forgetting** — aggressive fine-tuning on a narrow dataset can degrade general capability.
- **Overfitting** on a small dataset — the model memorizes examples instead of generalizing.
- Data quality matters more than data quantity for instruction-style fine-tuning.

---

## 7. Vector Databases

Purpose: store embeddings and support fast approximate nearest-neighbor (ANN) search at scale — exact search over millions of high-dimensional vectors is too slow.

Common indexing approaches:
- **HNSW** (Hierarchical Navigable Small World) — graph-based index, good recall/speed tradeoff, widely used as a default.
- **IVF** (Inverted File Index) — clusters vectors, searches only the most relevant clusters; often paired with quantization for memory savings.

Examples in the ecosystem: FAISS (library, not a managed DB), Chroma (lightweight, good for prototyping), Weaviate, Milvus, Pinecone (managed/hosted).

Things to actually check before picking one:
- Does it support metadata filtering alongside vector search (e.g. "find similar docs, but only from project X")?
- How does it handle updates/deletes? Some ANN indexes are easier to rebuild than to update in place.
- Hosting cost and latency at the scale you actually need, not the scale you imagine needing.

---

_Next to explore: evaluation frameworks for RAG/agents, multimodal embeddings, structured generation/constrained decoding._
