## Contents

1. Why production differs (two failure sources)
2. Diagnosing "works on my machine"
3. Closing the gap
4. Performance as a habit
5. Error handling tactics
6. Logging discipline
7. Worked example
8. Pitfalls

# Production gap, performance and error handling

## 1. Why production differs

Code that passed every test and every sign-off can still fall over on launch day. The chapter traces this to two sources that no test suite fully removes:

- **Real users.** Developers overestimate how well they know their audience. Real people type odd values into forms, arrive in large concurrent bursts, use every mix of OS, browser, security setting and network quality, and invent workflows nobody designed for. Version skew between environments adds behavior that was never present during testing.
- **Environment mismatch.** The software is the same, the surroundings are not.

Treat real usage as the final test stage and limit its blast radius: expose changes to a slice of users first (canary), compare variants (A/B), and keep enough observability (logs, metrics, distributed traces) to see what happened.

## 2. Diagnosing "works on my machine"

Closing a ticket as "cannot reproduce" fixes nothing for the user. Walk this checklist instead; each line is a dimension the chapter names as differing between a laptop and production.

| Dimension | Question to ask | Typical surprise |
|---|---|---|
| Platform and resources | Same OS, memory limits, CPU? | macOS laptop vs memory-capped Linux container |
| Data store | Same vendor and major version? | MySQL locally, PostgreSQL in production |
| Dependencies | Same library and runtime versions? | Transitive upgrade only in one environment |
| Configuration | Which endpoints, log levels, credentials, sandbox vs live providers? | Test payment API locally, real one in prod |
| Concurrency and load | How many simultaneous requests? | Cart works for one clicker, collapses under a sales spike; memory jumps from about a third to nearly full |
| Data diversity and volume | Clean handmade rows or years of messy legacy records? | Validation rejects legacy formats; queries fine on hundreds of rows crawl on millions |
| External dependencies | What if the payment, email or identity provider is slow, rate limited or down? | One partner outage takes the whole flow down |
| Security controls | Firewalls, mandatory TLS, CORS? | Plain HTTP call or cross-origin request blocked only in prod |

## 3. Closing the gap

Four levers, usually combined:

1. **Containers** so the runtime image is identical from laptop to production.
2. **Observability** (logs, metrics, tracing) so production behavior is visible before users complain.
3. **Environment parity**: a staging environment that mirrors production closely enough to expose environment-specific faults.
4. **CI/CD** so every change is exercised regularly under production-like conditions.

Also test with realistic, varied, high-volume datasets, not only a few tidy fixtures.

## 4. Performance as a habit

The chapter frames performance as a mindset adopted before coding and revisited throughout, and its goal is user experience rather than raw speed. Adopt the techniques incrementally; none is mandatory on day one.

Backend levers:

- **Asynchronous work** for tasks that need not block the caller. Use deliberately: it adds ordering, error-propagation and debugging complexity.
- **Fewer network round trips.** Each call costs time and resources; batch many small requests into one.
- **Caching** for data that is read often and changes rarely (in memory or a fast store). Reduces database load and latency; weigh staleness and invalidation.
- **Query hygiene**: efficient queries, correct indexes, and no N+1 patterns (one query per item in a loop).

Frontend delivery levers:

- **Minification** strips whitespace, newlines and comments without changing behavior.
- **Bundling** merges many files into one or two; tools such as Webpack or Vite also do **tree shaking** (dropping unused code).
- **Lazy loading** defers images, code chunks and components until needed, cutting initial load.
- **CDNs** serve static assets from locations near the user and complement minification and bundling.

Decision rule: pick the lever that matches the measured bottleneck (round trips, database, payload size, first paint) rather than applying all of them.

## 5. Error handling tactics

Planning heuristic from the chapter: the happy path may be roughly a fifth of the code, while edge cases and failures can consume around four fifths of the effort. Engineers are distinguished by how they handle the unhappy paths.

Four tactics:

- **Graceful degradation**: when a feature fails, serve a reduced version (for example last known data marked as possibly stale) instead of an error page.
- **Human-friendly messages**: users get plain language and a next step; internals such as connection errors stay hidden.
- **Log the technical detail**: error codes and stack traces go to logs for engineers, not to the screen.
- **Fallbacks**: have a second option for critical dependencies, such as a backup payment processor that takes over automatically.

Practice habit: before coding a feature, list what could break and implement handling for the three most likely failures.

## 6. Logging discipline

Too little logging leaves you blind; too much buries the signal. Use severity levels consistently (names vary by language; Java-style levels shown):

| Level | Use for |
|---|---|
| ERROR | Serious problems needing prompt action |
| WARN | Situations that may become harmful |
| INFO | Normal business events |
| DEBUG | Detailed diagnostics, usually off in production |

The chapter's environment example runs development at INFO and production at ERROR; treat verbosity as configuration, not code.

Never log: secrets (passwords, API keys, tokens), PII, whole objects or full response bodies (log the identifying fields that explain the failure), or the same event repeated at several layers.

Operational rules learned from incidents (also used for monitoring):

1. Decide in advance what you will need when something breaks, and log that.
2. Every entry carries a timestamp and a user or request identifier.
3. Errors are logged at ERROR, never hidden inside INFO.
4. No private data in logs.
5. Rotate and delete old logs before they fill storage.
6. Do log security-relevant actions (logins, permission changes), minus sensitive values.

A short sketch of the pattern (fallback plus split user and engineer messages):

```python
def get_forecast(city, client, cache, log):
    try:
        data = client.fetch(city)
        cache.put(city, data)
        return {"data": data, "stale": False}
    except TimeoutError as exc:
        log.error("forecast_fetch_failed city=%s err=%s", city, exc)
        cached = cache.get(city)
        if cached is not None:
            return {"data": cached, "stale": True}
        return {"error": "Forecast is unavailable right now. Please retry shortly."}
```

## 7. Worked example

A checkout service passes QA but times out in production at peak. Diagnosis by checklist: concurrency (hundreds of sessions), data volume (order history query lacks an index and issues one query per line item), external dependency (tax service latency). Fix order: add the index and collapse the N+1 into one query, batch tax lookups, cache static tax tables, add a timeout with a fallback that queues orders for later tax calculation, and log a single ERROR per failed order with request ID.

## 8. Pitfalls

- Treating "unable to reproduce" as resolution.
- Testing only with a handful of clean records.
- Reaching for async everywhere and inheriting race conditions.
- Showing stack traces or database errors to end users.
- Logging the full request body "just in case", which leaks PII and floods storage.
- Assuming that silence means health; users often quit rather than report.
