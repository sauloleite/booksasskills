# Long Context vs Retrieval, and Dynamic Knowledge Graphs

Covers the chapter's "promise and peril" discussion plus its closing guidance on choosing a memory architecture.

## Long context vs retrieval

Context ceilings of about 1M tokens (roughly 750,000 words, over 2,500 pages) make retrieval-free designs possible: load the whole policy manual or spec into the prompt and let attention find the passage. Index-free RAG pushes chunking and relevance scoring inside a long-context model instead of an external index.

What you gain: a simpler pipeline with no retrieval or ranking nodes to orchestrate.

What you pay:
- Compute, latency and cost per call grow with every token loaded, which can cancel the simplicity win.
- No guarantee the model picks out the one relevant fact from a huge context.

Current guidance from the chapter (it explicitly allows that bigger models may eventually make text and vector search obsolete):
- Hybrid is the consensus default. Combine an extended window with selective retrieval nodes.
- Prefer retrieval for fact-seeking questions and enterprise workloads, especially when freshness of the data or precise ranking matters.
- Long context alone is reasonable when the corpus is small and stable, queries are few, and latency or cost per call is not a constraint.

Decision table:

| Situation | Lean toward |
|---|---|
| Corpus fits comfortably, changes rarely, low query volume | Load into context |
| Facts change often, must be current | Retrieval (refresh the index, not the prompt) |
| Precise fact lookup, high volume, cost sensitive | Retrieval |
| Needs both broad grounding and exact facts | Long context plus targeted retrieval |
| Multi-document reasoning, entity relationships | GraphRAG (plus vector RAG) |

## Dynamic knowledge graphs

A dynamic graph is updated continuously as new information arrives, instead of in periodic rebuilds.

Benefits:
- Real-time grounding for fast-changing domains: news, social media, live monitoring.
- Learns from new data without retraining or manual refresh cycles; valuable where stale knowledge is costly (medicine, technology, finance) and decisions must be fast.
- Structured, operable representation that supports reasoning, offers more flexibility than a vector store, and captures the full context around an entity.

Risks and the matching mitigation:

| Risk | What goes wrong | Mitigation |
|---|---|---|
| Maintenance complexity | Continuous inflow injects errors and contradictions that spread through connected nodes | Automated validation on every ingest (schema checks, contradiction detection, entity resolution) |
| Resource intensity | Updating and validating at scale consumes heavy compute; scalability suffers | Distributed databases, cloud scaling, batching of low-priority updates |
| Security and privacy | User or sensitive data in a live graph complicates regulatory compliance; one lapse becomes a breach | Encryption, access control, anonymization, compliance review of every input source |
| Overreliance | Automated graph-driven decisions miss factors the graph does not model | Human oversight on consequential decisions |

Rule of thumb: go dynamic only when freshness is a hard requirement; otherwise scheduled incremental loads give most of the value with far less operational risk.

## Choosing a memory architecture (escalation ladder)

Derived from the chapter's ordering and conclusion. Move up only when the current rung demonstrably fails.

1. Rolling context window. Default; enough for many agents.
2. Add keyword search (BM25) over history or documents when old but exact details must be recalled.
3. Add semantic retrieval (vector store) when paraphrase or concept matching fails.
4. Add RAG over a curated knowledge base when domain or company facts and policies must steer answers.
5. Add semantic experience memory when users expect continuity across sessions or tasks outlive the window.
6. Add GraphRAG when questions span documents, require themes, or follow relationships.
7. Make the graph dynamic only when real-time freshness justifies the operational cost.

Orthogonal option at any rung: self-notes, for long or multi-part inputs where the agent must track state while reading.

## Worked example (invented)

An internal IT helpdesk agent.
- Week 1: rolling window only. Users complain it forgets the laptop model mentioned earlier in long chats. Pin key facts and keep the window.
- Week 3: questions quote exact error codes from old tickets. Add BM25 over the ticket archive.
- Week 5: users describe symptoms in their own words. Add embeddings and run hybrid lookup.
- Week 8: IT policies must govern answers. Add RAG over the policy set with source metadata for citations.
- Later: "which teams were affected by the VPN changes and why?" spans tickets, change logs and org data. Pilot GraphRAG on change records with an ontology of Service, Team, Change, Incident. Keep it batch-updated nightly; real-time updates are not needed.
