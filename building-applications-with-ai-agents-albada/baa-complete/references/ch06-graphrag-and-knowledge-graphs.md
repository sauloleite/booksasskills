# GraphRAG and Knowledge Graphs

## Contents
- When baseline RAG breaks
- GraphRAG components
- Tooling ladder: prototype to production
- Building a knowledge graph (8 steps)
- Loading a graph safely (Cypher practice)
- Querying: multihop and neighborhood expansion
- Pitfalls

## When baseline RAG breaks

Chunk-embed-retrieve handles direct fact lookup well. Switch to, or add, GraphRAG when you observe one of these:

1. Connecting the dots: the answer is spread across several documents and no single chunk holds it.
2. Global or thematic questions: "what are the main themes across this corpus?" needs aggregation, not a nearest chunk.
3. Data that is large, messy, or narrative rather than a set of discrete facts.

Probe question to test a baseline: ask for everything a specific person or entity has done. If no chunk summarizes them, vector RAG returns fragments; a graph of that entity and its relations answers it.

Cost reality: GraphRAG is more expensive and more complex to build and run, and in practice it frequently gives better results once vector retrieval has hit its ceiling. Adopt it on evidence of that ceiling, not by default.

## GraphRAG components

- Knowledge graph: entities as nodes, relations as edges, both explicit. Graph databases handle multi-hop queries efficiently.
- Retrieval system: pulls the subgraph or node cluster most relevant to the query instead of text snippets.
- Generator: turns the retrieved structure into a grounded, coherent answer.

## Tooling ladder: prototype to production

| Stage | Option | Notes |
|---|---|---|
| Fastest trial | Microsoft `graphrag` package (CLI: `init`, `index`, `query`) | No Python needed. `--method global` for corpus-wide themes, `--method local` for questions about a specific entity |
| Learn the internals | `nano-graphrag`, small community example repos | Whole pipeline in a few hundred lines |
| Code-level control | `neo4j-graphrag` Python package | Configure connection, embedder, retriever |
| Production | Neo4j Enterprise or AuraDB | Clustering, fault tolerance, ACID, multi-region; native storage with index-free adjacency keeps traversal cost roughly flat as the graph grows |

Other graph stores named for population: OrientDB, Amazon Neptune. Note the chapter is openly enthusiastic about Neo4j; evaluate alternatives on your own cloud, scale and licensing constraints.

Global vs local query choice: route "summarize / themes / overall" questions to global search and "who is / what did X / how is X related to Y" questions to local search.

## Building a knowledge graph (8 steps)

1. Collect data: databases, documents, sites, user content. Favor diverse, high-quality sources; for an enterprise agent, start with the core policy and reference documents meant to shape its behavior.
2. Preprocess: remove irrelevant and duplicate material, fix errors, standardize formats. Noise here becomes wrong entities later.
3. Extract entities: people, places, organizations, concepts, typically via NER models or a foundation model.
4. Extract relations: predicates linking entities become edges. Hardest on unstructured text, though foundation models keep getting better at it.
5. Design the ontology: the schema of entity types and allowed relation types. It is the backbone that keeps the graph queryable.
6. Populate: create nodes and edges in the graph store following the ontology.
7. Integrate and validate: link to other systems, run entity resolution to merge duplicates, verify the graph reflects the domain (user testing and automated checks).
8. Maintain: add and revise data, extend the ontology as new entity or relation types appear; automate where possible.

Ordering note: steps 3 to 5 iterate in practice. Draft an ontology early to constrain extraction, then refine it from what extraction finds.

Extraction format: semantic triples (subject, predicate, object) following the RDF data model, for example (Marie Curie, won, Nobel Prize in Physics). Foundation models extract triples well enough to build graphs at scale; still validate a sample by hand before trusting bulk output.

## Loading a graph safely (Cypher practice)

- Make loads idempotent: use `MERGE` (match or create) rather than blind `CREATE` so reruns and incremental batches do not duplicate entities.
- Stage scripts: create or merge nodes, then match them, then create relationships. Easier to debug and extend.
- Support incremental loading so new documents update the graph without rebuilding it.
- Scale reads and writes with the database's clustering, caching and query planner.

Original example in a different domain:

```cypher
MERGE (s:Service {name: 'checkout'})
MERGE (d:Service {name: 'payments'})
MERGE (t:Team {name: 'Commerce'})
WITH s, d, t
MERGE (s)-[:CALLS]->(d)
MERGE (t)-[:OWNS]->(s);

// Which teams are affected if 'payments' fails? (up to 3 hops upstream)
MATCH (t:Team)-[:OWNS]->(:Service)-[:CALLS*1..3]->(:Service {name:'payments'})
RETURN DISTINCT t.name;
```

## Querying: multihop and neighborhood expansion

Graphs express what flat tables and vector stores cannot: paths. Useful patterns for an agent's retrieval node:

- Path between two concepts (`shortestPath`) to explain how they relate.
- Typed lookups (all models built with a given tool).
- Neighborhood expansion: locate a seed node by search, then pull everything within k hops as context.
- Controller loop: the agent traverses at runtime, gathering several degrees of separation before generating.

Bound hop depth and result size; unbounded variable-length patterns explode on dense graphs and flood the context window.

## Pitfalls

- Expecting prototype-quality extraction to survive production: prototyping a graph is easy, hardening it is a major project.
- Skipping entity resolution, so one real entity becomes several nodes and multihop answers fragment.
- No ontology, so relation labels proliferate and queries become unwritable.
- Using `CREATE` in rerunnable loaders.
- Treating GraphRAG as a replacement for vector RAG; many systems keep both and route by question type.
