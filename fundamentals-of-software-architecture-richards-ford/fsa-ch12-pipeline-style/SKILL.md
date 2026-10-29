---
name: fsa-ch12-pipeline-style
description: Guidance for evaluating, designing and governing the pipeline (pipes and filters) architecture style, based on Chapter 12 of Richards and Ford's "Fundamentals of Software Architecture" (2nd ed.). Covers filter roles (producer, transformer, tester, consumer), pipe contracts, data and cloud topologies, risks, tag-based governance, team fit and trade-offs. Use when a user designs ETL, EDI, telemetry or step-by-step workflows, asks whether pipes and filters fits, reviews an overloaded or bidirectional pipeline, or weighs monolithic versus distributed filters.
---

# Pipeline (Pipes and Filters) Architecture Style

## Purpose

Help an agent decide whether a pipeline is the right style, shape it correctly (single-purpose filters joined by one-way pipes), anticipate its known failure modes, and govern it so it does not decay into an unstructured monolith. The style is usually a single deployment unit that is technically partitioned by filter type, so its architectural quantum is normally one. Its strengths are low cost, simplicity and modularity; its weaknesses are the usual monolithic ones (scalability, elasticity, fault tolerance, slow recovery).

## Key decision rules (apply without opening references)

1. **Fit test.** Choose a pipeline when processing is a sequence of distinct, ordered, deterministic, one-way steps. Complexity of the overall system does not disqualify it; the shape of the flow does.
2. **Budget and deadline.** Favor it under tight time or money constraints; its simplicity is the selling point.
3. **Reject or redesign** when the flow needs back-and-forth between steps. A need for a reply from a downstream filter means either the style is wrong or filter boundaries are drawn badly.
4. **Nondeterministic flows** (routing that depends on many runtime events) can technically be forced into a pipeline with lots of tester filters. Do not. Recommend event-driven architecture instead; the tester sprawl harms maintainability, testability, deployability and therefore reliability.
5. **Four filter roles only.** Producer (source, outbound only), transformer (map-like: enrich, convert, compute), tester (filter or route on criteria; may stop the flow), consumer (sink: persist or display). Every filter has exactly one role and one task; composite work becomes several filters in sequence.
6. **Filters are components**, even if one class. Treat a filter as an architectural building block, not a function call.
7. **Pipes are one-way and usually point-to-point.** Keep payloads small for performance. Each pipe carries a contract; changing it needs strict governance and tests on every receiving filter.
8. **Sync or async is independent of deployment.** Monoliths get asynchrony from threads or embedded messaging; distributed filters use REST, messaging or streaming.
9. **Data topology is free.** Anything from one shared database to one database per filter is legitimate.
10. **Monolith first.** Most pipelines are small enough for one deployment unit. Go distributed with asynchronous pipes only when scalability, elasticity or fault tolerance are driving characteristics, and state the price: more cost, less simplicity. This is the classic trade-off, not a free upgrade.
11. **Plan failure before structure.** Enumerate fatal error conditions and how the pipeline exits and recovers before committing to the design.
12. **Govern roles, not just runtime.** Operational fitness functions are use-case specific; structural governance relies on filter roles. Automated checks of role correctness are hard, so mark each filter entry point with metadata (annotation, attribute, decorator) declaring its type.
13. **Team fit is broad.** The style works with stream-aligned, enabling, complicated-subsystem and platform teams.

## Default workflow

1. **Qualify the flow.** Confirm steps are ordered, deterministic and one-way. If not, apply rules 3 and 4 and stop.
2. **Identify driving characteristics.** If scalability, elasticity or fault tolerance dominate, plan a distributed, asynchronous variant and document the cost and simplicity loss; otherwise default to a monolith.
3. **Decompose into filters.** Name each step, assign exactly one role, split any filter that needs two roles.
4. **Define pipes and contracts.** Direction, sync/async, transport, payload schema, owner, versioning approach.
5. **Choose data topology** per filter (shared, separate raw store, separate config store, separate results store).
6. **Design error handling.** List fatal conditions, exit points, recovery or replay strategy.
7. **Set governance.** Entry-point and role tags, contract tests, review checklist against overloading and back-channels.
8. **Map teams.** Pick the topology interactions that suit ownership (whole-flow ownership, experimental filters, specialist filters, shared tooling).
9. **Record the decision** with the trade-offs accepted and the conditions that would trigger moving to another style.

## References

- [references/topology-filters-and-pipes.md](references/topology-filters-and-pipes.md): read when designing or reviewing the structure: filter roles in depth, compositional reuse, pipe rules, data topologies, monolithic versus distributed and cloud deployment options (step-function workflows, serverless, containers).
- [references/risks-governance-and-teams.md](references/risks-governance-and-teams.md): read when assessing risks (overloaded filters, bidirectional pipes, error handling, contract drift), setting up role-tagging governance, or mapping team topologies onto a pipeline.
- [references/fit-tradeoffs-and-examples.md](references/fit-tradeoffs-and-examples.md): read when deciding whether to use the style, explaining its qualitative strengths and weaknesses, comparing it to alternatives, or needing worked examples (telemetry routing, ETL, EDI, integration frameworks) and review questions.
- [references/source-map.md](references/source-map.md): read to check which reference covers a given chapter section.

## Scripts

None. The chapter offers no calculation or structural metric that would justify one.
