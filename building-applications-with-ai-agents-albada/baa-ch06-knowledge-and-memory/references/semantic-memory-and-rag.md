# Semantic Memory, RAG, Experience Memory and Self-Notes

## Contents
- Semantic search in one paragraph
- Building a semantic store
- RAG: indexing and runtime
- Semantic experience memory
- Note-taking (self-notes)
- Pitfalls and checklist

## Semantic search in one paragraph

Semantic memory is long-term storage of general knowledge and past experience, recalled by meaning rather than wording. Retrieval compares embeddings, so a query can hit a passage that shares no keywords with it. Embedding quality has risen from word-level models (Word2Vec, GloVe) through BERT to large-model encoders trained on far more varied text. The practical consequence: semantic retrieval covers the paraphrase and concept gaps that BM25 leaves, which is exactly the failure that should push you here.

## Building a semantic store

1. Choose an encoder and embed every unit you want recallable (knowledge chunks or past interactions).
2. Store vectors in a store built for high-dimensional similarity search. Named options in the chapter: FAISS, Annoy (approximate nearest neighbors), and lightweight libraries such as `vectordb`.
3. Chunk before embedding. A sliding window with overlap is the default the chapter demonstrates (its example uses a window size of 128 with an overlap of 16) so a fact split across a boundary still lands intact in one chunk.
4. Attach metadata to every chunk: at minimum source title and URL, so answers can cite and so results can be filtered.
5. At query time embed the query with the same encoder, run similarity search, take the top N.

Decision notes:
- Approximate search (Annoy, FAISS indexes) trades a little recall for big speed gains at scale; exact search is fine for small stores.
- Re-embed everything when you change encoder; vectors from different models are not comparable.

## RAG: indexing and runtime

Offline indexing: documents, split into chunks, encoded, written to the vector index. The rationale for chunking: the generator, like a person, needs the relevant passage, not the whole manual.

Online runtime:
1. A controller receives the user question.
2. It queries the knowledge store for the most relevant chunks.
3. It combines retrieved context with the question.
4. The generator writes the answer, blending retrieved facts with what it already knows.

Where RAG pays off most: domain-specific or company-specific content, especially policies and rules that must steer outputs and that the base model has never seen.

Separate the two phases when debugging: a wrong answer with the right chunks retrieved is a generation or prompt problem; a wrong answer with the wrong chunks is a chunking, embedding or query problem.

## Semantic experience memory

A knowledge-base RAG still leaves two gaps: each session starts blank, and long tasks lose early context as the window rolls. Semantic experience memory closes both by indexing the agent's own past interactions.

Per turn:
1. Embed the new user input.
2. Search the store of previous interactions (all sessions for this user or task) with that embedding.
3. Reserve a fixed slice of the context window for the best matches.
4. Fill the remainder with the system message, the latest input, and the most recent turns.
5. After responding, write the new exchange back to the store.

Assembly sketch:

```python
def assemble(system, user_msg, recent, store, embed, count, limit, mem_share=0.25):
    mem_budget = int(limit * mem_share)
    hits, used = [], 0
    for h in store.search(embed(user_msg), k=20):   # best first
        if used + count(h) > mem_budget:
            break
        hits.append(h); used += count(h)
    rest = limit - used - count(system) - count(user_msg)
    window = keep_newest(recent, rest, count)        # FIFO over recent turns
    return [system, *hits, *window, user_msg]
```

The 25% share is an illustrative starting point, not a figure from the chapter; tune it per workload with `scripts/context_budget.py`. The payoff is behavior that adapts to the specific user and accumulated experience rather than only to general knowledge.

## Note-taking (self-notes)

Based on the Self-Notes paper by Lanchantin and colleagues (arXiv, 2023). Three inference styles:

| Style | Order of generation |
|---|---|
| Vanilla | context + question, then answer |
| Chain of thought | context + question, reasoning, then answer |
| Self-notes | notes written against pieces of the context (before seeing the question), a note on the question, then answer |

The model is asked to annotate, summarize or elaborate on the input without trying to answer yet, like margin notes, and those notes are interleaved with the original context. The paper reports gains on several reasoning and evaluation tasks. Use it when the input is long or multi-part and the agent must track intermediate state; the notes become a compact working memory you can also persist.

Prompt shape (original illustration):

```
Read each section below. After each, write NOTE: one or two lines on the
facts or state changes it introduces. Do not answer anything yet.
[sections]
Now write NOTE: what the question needs. Then give the final answer.
```

## Pitfalls and checklist

- Semantic search added where exact identifiers dominate; keep BM25 for those (often run both).
- Chunks without metadata, so answers cannot be cited or filtered.
- No overlap between chunks, splitting facts across boundaries.
- Experience memory with no reserved budget, so recalled items crowd out the latest turns, or vice versa.
- Experience memory that never writes back, so it never learns.
- Mixing embeddings from two encoders in one index.
