---
name: sahp-theme-granularity-and-reuse
description: Theme skill on sizing services and sharing code from "Software Architecture: The Hard Parts" (Ford, Richards, Sadalage, Dehghani) (chapters 7 and 8). Use when deciding whether to split or merge services using disintegrators and integrators, measuring service size, checking data dependencies between candidate services, or choosing how to share code across services (replication, shared libraries, shared services, sidecars and service mesh, platforms).
---

# Granularity and reuse (Software Architecture: The Hard Parts, ch. 7 and 8)

Most distributed-system pain comes from services that are the wrong size and from code shared in the wrong way.

## Cross-chapter rules

1. **Balance both forces.** Disintegrators (scope and cohesion, volatility, scalability, fault tolerance, security, extensibility) push toward splitting; integrators (transactions, workflow, shared domain code, data relationships) push toward merging. Evaluate both (`scripts/granularity_drivers.py`).
2. **Measure before arguing.** Use change frequency, load skew, incidents and data sensitivity, not only a sense of responsibility.
3. **Check what remains after a split.** If a leftover service can only be named "other", the cut is wrong.
4. **Watch synchronous coupling.** It erases fault tolerance gains and adds latency per hop; mostly cross-service requests suggest merging.
5. **Two-way data dependencies mean one service.**
6. **Settle granularity as a business trade-off,** stated in business terms and recorded in an ADR.
7. **Choose a reuse technique by context.** Shared libraries for stable code on one platform, shared services for frequently changing or multi-language logic, replication only for tiny frozen code, sidecars and a mesh for operational concerns. Version libraries deliberately and never depend on "latest".
8. **Reuse slow-changing code; prefer duplication for fast-changing domain code,** and favor platforms with stable APIs over central entity services.

## Default workflow

1. Gather measurements and run the disintegrator and integrator analysis (ch07).
2. Map data dependencies of the proposed split (ch07).
3. Decide how shared code will be packaged and owned (ch08).

<!-- BEGIN GENERATED: run tools/build_bundles.py to refresh -->

## References by chapter

Each link is one level deep; read only the files whose description matches the task.

### CH07: Service Granularity

- [ch07-balancing-and-trade-off-negotiation.md](references/ch07-balancing-and-trade-off-negotiation.md): read when drivers conflict and you must frame trade-off statements, facilitate a stakeholder decision, mitigate through design, or write the ADR; includes worked examples and case-study lessons.
- [ch07-granularity-integrators.md](references/ch07-granularity-integrators.md): read when checking whether to keep or merge services: transactions, workflow (request-mix rule, latency math), shared domain code, and table-ownership analysis.
- [ch07-sizing-metrics-and-disintegrators.md](references/ch07-sizing-metrics-and-disintegrators.md): read when measuring service size or judging any reason to split, including the leftover-cohesion naming test and extensibility caution.

### CH08: Reuse Patterns

- [ch08-replication-and-shared-libraries.md](references/ch08-replication-and-shared-libraries.md): read when considering copying code into services, sizing or splitting shared libraries, or designing versioning, release communication and deprecation policies.
- [ch08-reuse-value-and-platforms.md](references/ch08-reuse-value-and-platforms.md): read when someone argues for reuse as a goal, proposes a central entity service, asks how to compare all four techniques side by side, or wants the platform approach.
- [ch08-shared-services.md](references/ch08-shared-services.md): read when a shared service is proposed (including a shared data access service), to assess change risk, versioning, latency, scaling and availability, and for a worked library-versus-service analysis.
- [ch08-sidecars-and-orthogonal-reuse.md](references/ch08-sidecars-and-orthogonal-reuse.md): read when standardizing cross-cutting operational behavior, deciding what belongs in a sidecar, choosing sidecar ownership, or explaining duplicate-versus-couple and orthogonal coupling.

Merged section maps: [source-maps.md](references/source-maps.md).

## Scripts

Python 3 standard library only; run any script with `--help` for its arguments.

| Script | Purpose |
|---|---|
| `scripts/granularity_drivers.py` (ch07) | Granularity driver worksheet for service split/merge decisions. |

<!-- END GENERATED -->
