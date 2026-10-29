---
name: sahp-ch14-analytical-data
description: Guidance for serving analytical data (BI, ML training) from distributed architectures: why centralized Data Warehouse and Data Lake designs fail with domain-partitioned services, the four Data Mesh principles, data product quantum (DPQ) types, cooperative-quantum coupling rules, and completeness fitness functions. Based on Chapter 14 of Ford, Richards, Sadalage and Dehghani's "Software Architecture: The Hard Parts". Use when designing analytics for microservices, choosing warehouse vs lake vs mesh, designing a DPQ or its contracts, or reviewing analytical pipelines for brittleness, PII or staleness.
---

# Managing Analytical Data (SAHP Chapter 14)

Once operational data is split per service, reporting and ML still need it stitched back together. This skill helps an agent pick an analytical data approach, reason about the trade-offs of the two centralized patterns (warehouse, lake), and design Data Mesh data product quanta (DPQs) whose coupling to the operational services stays safe. The chapter's core move is applying the same domain-over-technical partitioning argument used for services to analytical data.

## Key decision rules

1. **Treat operational and analytical data as different problems.** Analytical work needs history, aggregation and different shapes; forcing it onto transactional stores or keeping one schema for both is the root mistake.
2. **Centralized patterns are technically partitioned.** Warehouse and lake both split the system into ingest, transform, load and serve stages and strip domain context from the data. In a domain-partitioned architecture this re-creates the semantic coupling you just removed.
3. **Warehouse (transform, then load) failure modes:** brittle integration (every domain schema change ripples into import logic), domain knowledge split between operational teams and analysts, a separate costly ecosystem, sync bottlenecks that leak load back into operational systems, contract brittleness inside transformation pipelines, and frequent failure to deliver value matching its cost. Its real strengths are consolidation and isolating heavy analytical compute.
4. **Lake (load raw, transform on demand) failure modes:** relationships between data sets get lost, so consumers struggle to discover and join correctly; combinable PII leaks; it is still technically partitioned; pipelines still break or go stale; quality and integrity work is pushed downstream. Its strengths are less up-front work, raw data that suits ML, and a better fit for distributed systems than the warehouse.
5. **Prefer Data Mesh for microservices-style systems** with contained transactions and well-isolated services. Apply all four principles together: domain ownership, data as a product, self-serve platform, computational federated governance.
6. **Each analytics-contributing domain owns a DPQ** next to its service. Pick the type deliberately: source-aligned (serves one service's analytical view), aggregate (combines several DPQs, sync or async), fit-for-purpose (built for one consumer need such as an ML model or BI report).
7. **A DPQ is a cooperative quantum:** operationally independent of its service, tightly contract-coupled to that service, loosely contract-coupled to the analytics consumers.
8. **Static coupling:** the DPQ and its transport are part of the quantum's static coupling (analytics is a required feature), but its contract with the data plane must be independent of the service's internal implementation, like a sidecar.
9. **Dynamic coupling: never transactional.** Service-to-DPQ propagation must be asynchronous and eventually consistent (the book points to its Parallel Saga and Anthology Saga styles). A requirement to keep operational and analytical data synchronously in lockstep defeats the pattern; push back or redesign.
10. **Governance lives in the sidecar.** Federated owners write policies (access, privacy, quality, interoperability) as code; the platform embeds and executes them in every DPQ at read or write time and upgrades them uniformly.
11. **Mesh costs:** contract coordination with every DPQ, and mandatory eventual consistency. If analytical and operational data must always agree, mesh becomes hard.
12. **Protect trend data with explicit completeness contracts.** For time-series consumers, a missing period is safer than a partial one: require all-or-nothing delivery per period, mark incomplete periods as exempt, and back it with fitness functions (arrival-gap checks, consumer-driven contract tests).

## Default workflow

1. Classify the analytical needs: report/BI, ad hoc exploration, ML training, near-real-time dashboards. Note freshness and consistency requirements.
2. Check the operational architecture: domain partitioned with isolated services favors mesh; a monolith with one shared database may still justify a warehouse.
3. If any need demands synchronous agreement between operational and analytical data, flag it as a design conflict before proposing mesh.
4. For each contributing domain, define a source-aligned DPQ: owner, published data sets, cadence, quality guarantees, PII handling, and its contract.
5. Add aggregate or fit-for-purpose DPQs for cross-domain products; prefer async inputs and loose contracts.
6. Specify governance policies as code and what the platform provides (discovery, creation, lineage, monitoring).
7. Write an ADR per significant choice plus fitness functions (completeness, contract tests, async-only propagation).

## References

- [references/centralized-analytics-patterns.md](references/centralized-analytics-patterns.md): read when evaluating or migrating away from a data warehouse or data lake, explaining star schemas, or diagnosing brittleness, PII and staleness in existing pipelines.
- [references/data-mesh-and-dpq-design.md](references/data-mesh-and-dpq-design.md): read when designing a Data Mesh, choosing DPQ types, setting coupling and communication rules, defining governance, or deciding whether mesh fits.
- [references/dpq-worked-example-and-fitness-functions.md](references/dpq-worked-example-and-fitness-functions.md): read when building an aggregate or ML-oriented DPQ, writing its ADR, or defining completeness and contract fitness functions.
- [references/source-map.md](references/source-map.md): read to see which file covers each chapter section.

## Scripts

- Run `python3 scripts/daily_completeness_check.py timestamps.txt --max-gap-seconds 60` to compute, per day, the largest gap between message arrivals, mark days with a gap above the threshold as EXEMPT (and days with no data as EMPTY), and report the exempt ratio. Add `--check-day-edges` for round-the-clock feeds to also count midnight-to-first and last-to-midnight gaps, and `--start/--end` to detect wholly missing days. Add `--max-exempt-ratio 0.1` to exit non-zero when too many days are exempt (usable as a CI or scheduled fitness function). Input is one ISO 8601 timestamp per line; `--help` lists all options.
