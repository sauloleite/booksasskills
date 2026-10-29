## Contents

- Selection criteria
- Database families: fit, signals, examples
- Worked selection examples
- Persistence abstraction levels
- Connection pooling
- Transactions and boundaries
- Practice drills

# Database Selection and Persistence

## Selection criteria

Choose from requirements, not from trends, conference talks or what the last team used. Score the workload on:

1. **Relationship complexity:** how many entities, how tightly linked?
2. **Read/write mix:** read-dominated, write-dominated, balanced?
3. **Query shape:** lookups by key, ad hoc filters, joins, aggregations, traversals, similarity?
4. **Growth:** expected data volume and traffic over the next year or two.
5. **Consistency needs:** what does a stale or contradictory read cost the business?

The choice is reversible. Many products start on one simple store and move when the need is proven; outgrowing a database because you have millions of users is a success problem. Pick for today's requirements, keep the design reasonably flexible, and move on.

## Database families

| Family | Pick it when | Avoid or reconsider when | Examples |
|---|---|---|---|
| Relational | Clear entity relationships; joins and complex queries; transactions and integrity are critical; structure is fairly stable | Records vary wildly in shape, or the schema churns weekly | PostgreSQL, MySQL, Oracle, SQL Server |
| Document | Record shape varies; requirements change often; need horizontal scale; CMS and catalogs | Many cross-document relationships and multi-entity transactions | MongoDB, Couchbase, Firestore |
| Key-value | Access is almost always by key; extreme speed matters more than query power; caches, sessions, preferences | You need filtering or reporting across values | Redis, DynamoDB, Riak |
| Graph | Data is densely connected; relationships matter as much as entities; multi-hop traversals and pathfinding; social graphs, recommendations, knowledge graphs | Mostly tabular data with shallow links | Neo4j, JanusGraph, Amazon Neptune |
| Vector | You need "find things like this" over embeddings: semantic search, recommendations, RAG context retrieval, similar image/video lookup, anomaly detection, near-duplicate detection | You need exact matches or relational integrity | Pinecone, Weaviate, Chroma, Qdrant |

Notes per family:

- **Relational** rests on relational algebra and ACID:
  - *Atomicity*: a transaction applies completely or not at all; failure rolls everything back.
  - *Consistency*: every committed transaction leaves constraints and relationships valid.
  - *Isolation*: concurrent transactions behave as if run alone, preventing dirty reads and lost updates.
  - *Durability*: committed changes survive crashes and power loss.
- **Document** stores embed related data (an article with its author snapshot, tags and comments) in one JSON-like record, trading join flexibility for read locality and schema freedom.
- **Key-value** is the simplest NoSQL model. Use key prefixes as namespaces (`session:<id>`, `prefs:<user>`) and set expirations for ephemeral data such as sessions.
- **Graph** makes edges first-class. Queries follow connections instead of computing joins over foreign keys, which surfaces patterns that are painful to find in tables.
- **Vector** stores hold embeddings: arrays with hundreds to thousands of dimensions where semantic closeness becomes geometric closeness. The core operation is nearest-neighbor similarity search, not equality matching.

One-line summary: relational for structure and consistency, document for evolving shapes, key-value for speed on simple access, graph for relationships, vector for AI similarity.

## Worked selection examples

- **Personal blog:** users author posts; posts carry tags and comments. Well-defined entities and relationships point to relational.
- **Custom merchandise catalog:** a mug, a hoodie and a poster share few attributes, and new product types appear monthly. Variable, changing attributes point to document.
- **Login sessions for a web app:** fetch by session ID, auto-expire after inactivity. Key-value with TTL.
- **"People you may know":** friends-of-friends traversal. Graph.
- **Support-ticket assistant that retrieves similar past tickets for an LLM:** vector store, usually alongside a relational store holding the ticket records themselves.

Polyglot persistence is normal: a single product can combine several of these.

## Persistence abstraction levels

Pick the abstraction level by application complexity, team expertise and timeline. Team skills are a legitimate deciding factor: a group fluent in SQL and new to ORMs may be faster and safer without adopting one.

| Level | What you write | Gains | Costs |
|---|---|---|---|
| Direct access | Raw SQL or the store's native query language | Full control, predictable performance | Needs deep database knowledge; manual mapping; boilerplate |
| Repository pattern | A domain-named interface (`find_active_users`) that hides queries | Separates business logic from data access; easy to fake in unit tests; data code lives in one place | Another layer to maintain |
| ORM (Hibernate/JPA, Entity Framework, etc.) | Annotated or configured entity classes; a simplified query language | Little hand-written SQL or mapping; fast start | Hidden queries, harder debugging, N+1 traps, performance surprises |

A good repository:

1. Owns every query and database call for its aggregate.
2. Shields callers from schema details and vendor specifics.
3. Exposes intention-revealing method names.
4. Translates driver exceptions into one domain-level error type.
5. Opens and releases connections deterministically (context managers, try-with-resources, `using`).

```python
class UserRepository:
    def __init__(self, pool):
        self._pool = pool

    def find_active_users(self, limit=100):
        sql = ("SELECT id, handle, email_address FROM accounts "
               "WHERE status = %s ORDER BY joined_at DESC LIMIT %s")
        try:
            with self._pool.connection() as conn, conn.cursor() as cur:
                cur.execute(sql, ("active", limit))
                return [User(*row) for row in cur.fetchall()]
        except DatabaseError as exc:
            raise RepositoryError("active user lookup failed") from exc
```

Warning: more abstraction is not automatically better. ORMs get you started quickly but obscure what hits the database. Evaluate per use case; a common pragmatic answer is ORM for routine CRUD plus hand-written SQL on hot paths.

## Connection pooling

Opening a connection per operation is a beginner pattern that does not survive production. A pool keeps a set of open connections in memory and lends them out, removing the setup cost per request.

- Configure at least the JDBC/DSN URL, credentials (from a secret store, never hard-coded) and a maximum pool size.
- Frameworks such as Spring Boot wire a pool (HikariCP) automatically; know that it exists and how to read its metrics.
- Pool sizing signals are covered in the query performance reference (pending, active, idle counts).

## Transactions and boundaries

A transaction groups several operations into one all-or-nothing unit. The canonical example is a transfer: the debit and the credit must both land or neither does.

Key point: the database enforces ACID for a transaction, but **the application decides where a transaction starts and ends**. Grouping related writes into the same scope is the developer's job.

```python
def transfer(pool, src, dst, amount):
    with pool.connection() as conn:
        try:
            conn.autocommit = False
            conn.execute("UPDATE accounts SET balance = balance - %s WHERE id = %s",
                         (amount, src))
            conn.execute("UPDATE accounts SET balance = balance + %s WHERE id = %s",
                         (amount, dst))
            conn.commit()
        except Exception:
            conn.rollback()
            raise
```

Checklist for boundaries:

- Every multi-step write that must be consistent is in one transaction.
- Keep transactions short; long ones hold locks and pool connections.
- No network calls to other services inside a database transaction.
- Use exact decimal types for money.

## Practice drills

- Take an open-source blog engine or small e-commerce app, diagram its entities and relationships, and judge whether its database family fits its query patterns.
- Implement the same "active users" lookup three ways (raw SQL, repository, ORM), then compare the SQL each one actually sends.
