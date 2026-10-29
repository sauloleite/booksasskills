# Retrieval Optimization and RAG Beyond Text

## Contents
- Chunking strategy
- Reranking
- Query rewriting
- Contextual retrieval (chunk enrichment)
- Checklist: evaluating a retrieval product
- Multimodal RAG
- RAG over tables (text-to-SQL)
- Pitfalls
- Worked example: tuning a contract-search assistant
- Glossary

Four levers raise the odds that relevant documents come back: chunking, reranking, query rewriting, contextual retrieval. Chunking is the most consequential indexing decision.

## Chunking strategy

Options, from simplest to most tailored:
- **Fixed-length units**: characters (for example 2,048), words (for example 512), a fixed number of sentences, or one paragraph per chunk.
- **Recursive splitting**: try the largest natural unit first (section), fall back to paragraph, then sentence, until each piece fits the maximum size. This lowers the odds of cutting related text apart.
- **Format-aware splitting**: code splitters per programming language; one chunk per question-answer pair (some teams find Q&A-shaped data retrieves best); language-specific rules (Chinese differs from English).
- **Token-based chunks** using the generator's tokenizer. Convenient downstream, but switching to a model with another tokenizer forces a full reindex.

**Overlap.** Without overlap, a boundary can sever a statement so that neither half carries its meaning (think "the patient is not" / "allergic to penicillin"). A small overlap guarantees each boundary region appears whole in at least one chunk. Scale cited: about 20 characters of overlap for 2,048-character chunks.

**Hard limits.** Chunk size must stay below the generator's context length and, for semantic retrieval, below the embedding model's input limit.

**Size trade-offs.**

| Effect | Smaller chunks | Larger chunks |
|---|---|---|
| Variety of sources in one prompt | Higher: halve size, fit twice as many | Lower |
| Risk of stranding information | Higher: a topic named only early in a document leaves later chunks unretrievable for that topic | Lower |
| Compute and storage | Halving size doubles chunks, embeddings and search space, slowing queries | Lower |

There is no universally correct size or overlap. Treat both as hyperparameters and tune them against retrieval and end-to-end metrics.

## Reranking

Purpose: refine the retriever's initial order, mainly so you can cut the candidate list down to fit the context window or to save input tokens.

Variants:
- **Precision cascade**: cheap retriever for recall, expensive scorer for ordering (see the hybrid section of retrieval foundations).
- **Recency weighting**: boost newer items when freshness matters, such as news aggregation, assistants over a mailbox, or market analysis.

How context reranking differs from search-engine ranking: in web search, position 1 vs position 5 is decisive. For a model's context, *inclusion* matters most. Order still has some effect, since models tend to process material at the start and end of the context better than the middle, so place the strongest evidence at the edges. But an included document in the middle still helps far more than an excluded one.

## Query rewriting

Also known as query reformulation, normalization or (sometimes) expansion. In multi-turn chat, follow-ups like "and the Berlin office?" are meaningless to a retriever on their own. Rewrite each user turn into a self-contained query using the conversation, for example "What is the parental leave policy for the Berlin office?".

- Classic search engines do this with heuristics; AI apps can ask a model to restate the latest user turn as what the user actually means, given the history.
- **Identity and knowledge resolution** make it harder. "What did her manager approve?" first requires looking up who her manager is.
- **Fail safely.** If the needed fact is unavailable, the rewriter should report the query as unresolvable rather than invent an entity, because a fabricated name poisons retrieval and the answer.
- Rewriting is not RAG-specific; it helps any search interface.

## Contextual retrieval (chunk enrichment)

Goal: make each chunk easier to find by attaching context before indexing.

Techniques:
- **Metadata**: tags, keywords; for products, descriptions and reviews; for images and video, titles and captions.
- **Extracted entities and identifiers**: store literal strings such as error codes in metadata so they stay searchable by keyword even after the body is embedded. This patches the main weakness of semantic search.
- **Answerable questions**: attach the questions a chunk answers. A "change billing address" article could carry "update my card address", "wrong address on invoice", "moved house, where do I change it".
- **Parent-document context**: chunks cut from a long document may not say what they are about. Add the document title and summary, or, following Anthropic's contextual retrieval approach, have a model write a short situating note (typically 50 to 100 tokens) explaining how the chunk fits in the whole document, prepend it, and index the combined text. (Do not reuse Anthropic's prompt verbatim; write your own instruction asking for a brief, retrieval-oriented situating note and nothing else.)

## Checklist: evaluating a retrieval product

- Retrieval mechanisms supported; is hybrid search available?
- For vector databases: which embedding models and ANN algorithms?
- Scalability in both storage volume and query traffic; does it fit your traffic shape (bursty vs steady)?
- Time to index your corpus; bulk add and delete limits.
- Query latency for each retrieval mode.
- Managed pricing basis: stored documents or vectors, or query volume?
- Enterprise features (outside the core list but often decisive): access control, compliance, separation of data plane and control plane.

## Multimodal RAG

With a multimodal generator, retrieved context can include images, video or audio, not just text. Example: "what does the logo on the original 1977 cartridge look like" is answered better with the image retrieved.

Two retrieval routes:
1. **Metadata route**: match the query against titles, tags or captions; return the item whose metadata scores relevant. Cheap, but limited by metadata quality.
2. **Content route**: use a joint text-image embedding model such as CLIP. Embed every text and image into one vector store; embed the query; return the nearest items regardless of modality.

Any modality can be substituted for images in this pattern, given an embedding model that spans it.

## RAG over tables (text-to-SQL)

Many questions need structured data ("how many returns did store 14 process last quarter?"). The workflow differs from document RAG:
1. **Text-to-SQL**: from the question plus table schemas, produce SQL. This is semantic parsing.
2. **Execute** the SQL.
3. **Generate** the answer from the result and the original question.

Design points:
- If the schema catalog is too large for the context, add a step that predicts which tables are relevant and include only those schemas.
- The same generator can write the SQL, or a specialized text-to-SQL model can.
- The system needs both SQL generation and SQL execution capabilities, which makes this a small agent; treat the executor as a tool with read vs write permissions (see agent design).

## Pitfalls
- Chunks over the embedder's limit (silently truncated); no boundary overlap.
- Tokenizer-based chunks without planning for reindexing on model swap.
- Retrieving with the raw follow-up turn; rewriters that invent entities.
- Embeddings alone for codes and SKUs without metadata enrichment.
- Polishing in-context order when the real win is getting the right document included.

## Worked example: tuning a contract-search assistant

Invented: clause questions over 8,000 contracts; recall 0.62 on 200 labeled queries.
1. Misses sit late in contracts whose parties are named only on page 1: prepend title, parties and a 60-token situating note to each chunk.
2. Misses straddling boundaries: split recursively by clause then paragraph, with modest overlap.
3. Follow-ups fail ("and for the Lisbon lease?"): add a history-aware rewriter that returns UNRESOLVABLE when ambiguous.
4. Top-20 overflows context: rerank to top-6, strongest evidence first and last.
5. Change one thing at a time; re-measure precision, recall, MRR and answer accuracy.

## Glossary
- **Contextual retrieval**: augmenting chunks before indexing with metadata, questions, or model-written situating text. **Text-to-SQL**: semantic parsing of a question into an executable query.
