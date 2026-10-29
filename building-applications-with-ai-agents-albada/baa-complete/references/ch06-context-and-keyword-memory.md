# Context Windows and Keyword Memory

The cheapest memory tiers. The chapter's position: these two are enough for a large share of agents, so prove they fall short before building anything heavier.

## Knowledge vs memory (framing)

| | Knowledge | Memory |
|---|---|---|
| What it holds | Verifiable facts from outside the model: specs, policies, catalogs, logs | The agent's own trail: past user turns, tool results, state changes |
| Typical mechanism | RAG over a document corpus | Conversation history, experience store, checkpoints |
| Problem it solves | Model weights lack domain or fresh facts | Continuity across turns and sessions |

Both feed context engineering (Chapter 5). Memory is the store; context engineering is the selection and assembly step that decides what from the store enters a given call. Design them separately: a good store with a bad selector still produces bad prompts.

## Memory as graph nodes (LangGraph framing)

The chapter builds on a graph-of-nodes orchestrator where state is one typed object passed through the run. Practices worth carrying to any framework:

- Make each memory operation (trim window, extract keywords, semantic lookup, write back) its own node so it can be unit-tested and swapped.
- Use edges to fix ordering: read memory before the model call, write memory after it. Ordering bugs show up as the agent answering with stale context.
- Persist state through checkpointing keyed by a session or thread id. A graph that is invoked twice without a persisted thread forgets everything between calls (the classic "what's my name?" failure).
- Cycles and conditional edges let retries and memory-refresh loops live in the graph instead of ad hoc code.

## Managing the context window

Vocabulary: the context window is what one call actually receives; context length is the model's ceiling for it. Treat the window as working memory for that single request.

Conversions for quick budgeting: 1 token is about 0.75 English words or about 4 characters, so 1,000 tokens is about 750 words. Model ceilings have climbed from roughly 4K and 8K tokens to hundreds of thousands and, for some models, about 1M input tokens. Always check the current limit of the exact model and endpoint; published numbers go stale quickly.

Budget rule: give the model everything the task needs and nothing more. When the candidate material exceeds the window, allocation becomes an explicit design decision, not an accident of truncation.

### Rolling (FIFO) window

Pass the whole conversation each turn; when it overflows, drop the oldest material first.

- Pros: trivial to build, no extra infrastructure, fine for short or casual sessions.
- Core weakness: eviction ignores importance. A constraint stated in turn 2 disappears once enough later text accumulates.
- Eviction accelerates with long prompts, pasted documents, and wordy model replies. Cap reply verbosity if history matters.
- Long prompts also suffer from the model overlooking content. Mark the most relevant material clearly and put it near the end of the prompt, close to the question.

Minimal trimming sketch (always keep the system message, keep newest turns that fit):

```python
def trim_fifo(system, turns, limit, count):
    """turns: oldest->newest list of strings; count: token estimator."""
    budget = limit - count(system)
    kept = []
    for turn in reversed(turns):          # walk newest first
        cost = count(turn)
        if cost > budget:
            break                         # everything older is evicted
        kept.append(turn)
        budget -= cost
    return [system] + list(reversed(kept))
```

Use `scripts/context_budget.py` to see how many recent turns survive a given budget.

## Keyword memory with full-text search

Mature, fast, and precise. Index past messages or documents, then inject only top hits instead of the whole history.

Mechanics to get right:

1. Inverted index: each normalized term points to the chunks containing it (its postings list), so lookup cost does not scale with scanning history.
2. Analysis pipeline: tokenize, lowercase, stem, drop stop words. Run the identical pipeline on queries; a mismatch (stemming at index time only, say) silently kills recall.
3. Ranking with BM25, which combines term frequency, inverse document frequency (rare terms count more), and length normalization (very long or very short chunks are penalized).
4. Take the top K, shorten or summarize them if needed, then inject. K is a budget knob, not a quality guarantee.
5. Prototype in memory; in production keep the index in a database or search engine.

When it wins: exact identifiers, names, error codes, product terms, quotes the user is likely to repeat verbatim.

When it fails: paraphrase, synonyms, and theme-level questions where the stored text never used the query's words. That gap is the trigger to add semantic memory (see semantic-memory-and-rag.md).

## Pitfalls

- Assuming a larger window removes the need to choose what goes in. Cost, latency, and missed details still scale with size.
- Letting FIFO evict the task goal or user constraints; pin them outside the rolling region.
- Different text normalization at index and query time in BM25.
- Injecting full BM25 hits verbatim and blowing the budget; truncate first.
