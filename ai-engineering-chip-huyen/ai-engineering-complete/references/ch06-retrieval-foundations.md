# Retrieval Foundations: Why RAG, Retriever Types, Vector Search, Evaluation, Hybrid

## Contents
- Context construction and why RAG survives long context
- RAG architecture
- Term-based (lexical) retrieval
- Sparse vs dense: a misleading split
- Embedding-based retrieval and vector search
- ANN algorithm cheat sheet
- Term-based vs embedding-based
- Evaluating retrievers and the RAG system
- Combining retrievers: cascade and Reciprocal Rank Fusion
- Worked example: retriever for a support bot
- Glossary

## Context construction and why RAG survives long context

Instructions are common to all requests; context is per request. Missing context drives hallucination, so building it is the foundation-model counterpart of feature engineering. Per-query context also means user-specific data enters only that user's prompts.

Lineage: retrieve-then-read QA (Chen et al., 2017); the RAG name and its hallucination reduction on knowledge-intensive tasks (Lewis et al., 2020).

Why long context will not end RAG:
1. **Data outgrows windows.** Data accumulates and is rarely deleted, and apps expand to whatever limit they are given (the author's Parkinson's-Law analogy).
2. **Accepted tokens are not used tokens.** Longer prompts raise the odds of attending to the wrong span, and each token adds cost and possibly latency. Retrieval can cut tokens and improve quality together.

The author expects retrieval-like selection may eventually be built into models.

**Threshold**: Anthropic (2024) says a knowledge base under about 200k tokens (roughly 500 pages) can be placed whole in a Claude prompt. Elsewhere, measure.
- Small, stable corpus, affordable cost: prompt it.
- Large, growing, per-user corpus, or tight cost/latency: RAG.
- Small corpus but a few critical facts buried in noise: retrieval or reranking may still help, because attention over long context is uneven.

## RAG architecture

- **Retriever**: *indexing* (prepare data for fast lookup) and *querying* (fetch what is relevant). Design the index around how you will query.
- **Generator**: answers from the query plus retrieved chunks, joined into the final prompt with light post-processing.
- Lewis et al. trained both jointly; today they are usually off-the-shelf and separate, though end-to-end finetuning can help substantially (a later-stage lever).
- **Retriever quality largely determines system quality.**
- Documents range from a few tokens to millions, so chunk them. "Document" and "chunk" are interchangeable here, as are "retrieval" and "search".

Every retriever scores and ranks documents by relevance; algorithms differ in how they compute the score.

## Term-based (lexical) retrieval

Keyword match, fixed twice:
1. Too many matches to fit: favor documents where the term appears more often, **TF(t, D)**.
2. Filler vs informative terms: weight rare terms up with **IDF(t) = log(N / C(t))** (N documents, C(t) contain t). With 1,000 documents, a term found in 10 has ratio 100 before the log; one found in 900 contributes almost nothing.

Naive **TF-IDF**: score(D, Q) = sum over query terms of IDF(t) times TF(t, D).

- **Elasticsearch** (on Lucene) uses an **inverted index**: term to the documents containing it, often with per-document frequency and document count, the inputs TF-IDF needs.
- **Okapi BM25** normalizes term frequency by document length, since long documents naturally collect more hits. Variants: BM25+, BM25F. Still a formidable baseline; Perplexity's CEO noted that clearly beating it is hard.

Tokenization matters: whitespace splitting breaks multiword terms ("New York"), so promote frequent n-grams to terms. Lowercasing, punctuation removal and stop-word removal are usually automatic; NLTK, spaCy and Stanford CoreNLP offer tokenizers.

Scoring by **n-gram overlap** works only when queries and documents have similar length; long documents all contain the query's n-grams, scores cluster, and ranking loses discrimination.

## Sparse vs dense: a misleading split

Sparse vectors are mostly zeros (one-hot term vectors sized to the vocabulary); dense ones mostly nonzero (typical embeddings). **SPLADE** regularizes BERT-based embeddings to be mostly zero, so it is "sparse", yet it behaves like dense semantic retrieval. Classify by **term-based vs embedding-based** instead.

## Embedding-based retrieval and vector search

Lexical scores see form, not meaning ("python memory leaks" can surface snake articles). Semantic retrieval ranks by meaning.
- **Indexing** adds an embedding step and stores vectors in a **vector database**.
- **Querying**: embed the query with the same model used for indexing, then fetch the k nearest chunks; k depends on use case, generator and query.
- Real systems add rerankers and caches; the flow mirrors classic recommender pipelines.
- A bad embedding model sinks the retriever. Storing vectors is easy; searching them fast is the hard part.

**Exact k-NN** (score all vectors, e.g. cosine, sort, take top k) is precise but heavy; use only for small collections. Large collections use **ANN** libraries such as FAISS, ScaNN, Annoy, Hnswlib. Most teams buy rather than build, so learn the algorithms to evaluate products. Vectors are organized into buckets, trees or graphs, and may be quantized or sparsified for cheaper comparisons.

## ANN algorithm cheat sheet

| Algorithm | Mechanism | Notes |
|---|---|---|
| LSH | Hash nearby vectors into shared buckets; works beyond vectors | Cheap, small index; slower, less accurate queries. In FAISS, Annoy |
| HNSW | Layered proximity graph walked coarse to fine | Fast, accurate queries; heavy build time and memory. In FAISS, Milvus |
| Product quantization | Split vectors into subvectors, compare compact codes | Big speed and memory savings; near-universal support |
| IVF | k-means clusters; search clusters nearest the query | Aim for about 100 to 10,000 vectors per cluster; IVF + PQ is FAISS's backbone |
| Annoy | Forest of random-split binary trees | From Spotify |
| Others | SPTAG, FLANN | |

**Index vs query trade-off**: richer indexes (HNSW) give accurate, fast queries but cost build time and memory; light ones (LSH) the opposite. Frequent rebuilds make build time decisive. **ANN-Benchmarks** compares on recall, queries per second, build time and index size; shortlist on the same four. Any store that holds and searches vectors is a vector database, and mainstream databases are adding the feature.

## Term-based vs embedding-based

| Dimension | Term-based | Embedding-based |
|---|---|---|
| Speed (index and query) | Much faster | Embedding plus ANN search add latency |
| Out-of-the-box quality | Strong, few knobs | Depends on embedder |
| Headroom | Limited | Can surpass lexical via finetuning embedder, retriever, or jointly with generator |
| Query style | Hurt by term ambiguity | Handles natural, paraphrased queries |
| Exact identifiers | Good | Can blur codes like `EADDRNOTAVAIL (99)` and product names |
| Cost | Much cheaper | Embedding, storage, search can be costly |

Latency: generation, especially long output, usually dominates, so retrieval latency may be minor, but still measure its UX effect. Cost: changing data forces re-embedding (imagine 100 million documents a day), and vector DB spend can reach one fifth to one half of model API spend.

## Evaluating retrievers and the RAG system

- **Context precision** (also context relevance): fraction of retrieved documents that are relevant.
- **Context recall**: fraction of relevant documents that were retrieved.

Build test queries and a document pool, label each pair relevant or not (humans or AI judge), compute both. Recall requires labeling every stored document per query, so some production frameworks report only precision, which an AI judge can compute on retrieved items alone.

When order matters, add **NDCG, MAP, MRR** (see `scripts/retrieval_metrics.py`). For semantic retrieval, evaluate embeddings intrinsically (similar items closer) and on tasks via **MTEB**. **BEIR** spans 14 retrieval benchmarks.

Evaluate three things: retrieval quality, final outputs (a retriever is good only if answers are good), and embeddings when applicable.

## Combining retrievers: cascade and Reciprocal Rank Fusion

Lexical plus semantic is **hybrid search**, the usual production choice.

**Cascade**: cheap, coarse retrieval (BM25) gathers candidates; a precise, costlier step (exact k-NN on candidates, or a cross-encoder) reranks. Example: for "which rep closed the most deals with Northwind", keyword-filter on "Northwind", then vector-search the remaining intent within that subset.

**Ensemble**: run retrievers in parallel and merge rankings with **RRF** (Cormack et al., 2009):

score(D) = sum over lists i of 1 / (k + r_i(D))

r_i(D) is D's rank in list i; k (typically 60) prevents division by zero and damps low ranks. With k = 0, ranks 1 and 2 earn 1 and 0.5, so a document first in one list and second in another totals 1.5. With k = 60 the same document scores 1/61 + 1/62, about 0.0325. Absent documents contribute nothing for that list. RRF ignores raw score scales, so heterogeneous retrievers merge cleanly. Use `scripts/rrf_fuse.py`.

## Worked example: retriever for a support bot

Invented: 40k help articles, queries full of SKUs and firmware error strings, weekly updates, 2 s budget with generation at 1.2 s. Far above 200k tokens, so RAG. Identifiers make BM25 mandatory (and the baseline). Paraphrased symptom queries justify embeddings; weekly re-embedding of 40k chunks is affordable. Fuse with RRF (k = 60), rerank the top 30 with a cross-encoder, keep 5. Track precision online with an AI judge and recall offline on a labeled subset; keep the hybrid only if it beats BM25 by enough to pay for itself.

## Glossary
- **Hybrid search**: lexical plus semantic retrieval. **RRF**: rank-based fusion independent of score scales. **IVF**: cluster-then-search ANN index.
