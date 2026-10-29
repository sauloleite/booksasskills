---
name: sahp-ch08-reuse-patterns
description: Guidance for sharing code and functionality across distributed services, based on Chapter 8 of Ford, Richards, Sadalage and Dehghani's "Software Architecture: The Hard Parts". Covers code replication, shared libraries (granularity, versioning, deprecation), shared services (runtime change risk, latency, scaling, availability), sidecars and service mesh for operational coupling, and when reuse adds value (abstraction versus rate of change, platforms). Use when deciding where common code should live, splitting a shared library, choosing library versus service, or reviewing a sidecar or reuse proposal.
---

# SAHP Ch. 8: Reuse Patterns

This skill helps an agent decide how common behavior (validators, formatters, data access logic, security, logging, monitoring) should be shared once a system has been split into separately deployed services. The chapter rejects both "share nothing" dogma and reuse-as-virtue. It offers four mechanisms (replicate, shared library, shared service, sidecar in a service mesh), each with a distinct risk profile, and one test for whether reuse pays off at all: the thing found through abstraction must also change slowly. The agent's job is to match each piece of shared code to the mechanism whose trade-offs fit its volatility, its consumers' platforms and the operational needs of the callers.

## Key decision rules

**Choosing the mechanism**
1. Ask first whether the code should be shared at all. Reuse candidates come from abstraction, but only a slow, predictable rate of change makes reuse valuable. Fast-moving internal domain code is a poor coupling target.
2. Replicate (copy into each repo) only small, static, almost certainly bug-free code such as marker annotations or attributes, or a utility class each service will trim and evolve for its own context during a migration. Explore the other options first.
3. Default to a shared library in a homogeneous (single language or platform) environment where shared code changes at a low to moderate rate. Binding at build time leaves latency, scalability and availability untouched and lets versioning contain change risk.
4. Prefer a shared service when consumers are polyglot or the shared logic changes often. Accept that every change becomes a runtime change and that callers inherit latency, scaling coupling and an availability dependency.
5. Use a sidecar plus service mesh for operational (plumbing) concerns that must be uniform across services: monitoring, logging, service discovery, authentication, authorization, circuit breaking.
6. Never put shared domain classes (Customer, Address) in a sidecar by default. That is domain coupling and needs explicit trade-off analysis and contracts.
7. Add a utility to the sidecar only when a broad share of teams needs it. A practical cut-off: if fewer than about half the services use it, keep it as a library and revisit later, because every service pays the size overhead.
8. Shared code in a separate service must be consumable through composition (calls), not inheritance.

**Shared library hygiene**
9. Favor several small, function-oriented libraries over one catch-all library. You trade dependency management pain for better change control, smaller test scope and fewer forced upgrades. Isolate static functionality (formatters, security) into its own library.
10. Always version shared libraries, so one consumer can take a change without forcing the rest to retest and redeploy.
11. Treat versioning as hard, not simple. Plan how version changes are announced (what changed, which services and teams are affected) and how old versions are retired.
12. Set deprecation windows per library according to its change rate (keep few versions of slow libraries, many versions of fast ones). A single global window is easier to govern but causes churn on volatile libraries.
13. Expect serious defects or breaking changes to override any deprecation policy and force near-simultaneous upgrades. That is another argument for fine-grained libraries.
14. Pin explicit versions; do not depend on a floating "latest" version, which bites during hotfixes.

**Shared service hygiene**
15. Versioning a shared service via endpoint versions is subjective (what counts as a new version?), forces callers to repoint, and gets harder when the service is reached by several protocols (REST, messaging, gRPC).
16. Mitigate latency with gRPC or asynchronous request/reply messaging correlated by ID; mitigate availability with multiple instances; plan the shared service's scaling against all its callers' peaks.

**Organizational reuse**
17. Do not consolidate every division's view of a core entity into one central service. It becomes too complex for simple uses and a brittle ripple point for every change.
18. Prefer platforms: domain capabilities behind well-designed, loosely coupled APIs that let the implementation change quickly while the contract stays stable.

## Default workflow

1. Inventory the shared code and classify each piece: operational versus domain, static versus volatile (check repository history, not opinions), consumer count, consumer platforms, and whether callers are latency-sensitive or customer-facing.
2. Apply the reuse test (rule 1). If the code is domain-specific and volatile, consider letting each service own its own representation and integrate via contracts.
3. Pick the mechanism with rules 2 to 8.
4. For libraries, set granularity, versioning, communication and deprecation policy. For services, set versioning approach, protocol, scaling and redundancy. For sidecars, set ownership and fitness functions that confirm every service carries it.
5. Frame the choice as a hypothesis, list benefits and costs for each option against the actual callers, and record the decision and its consequences in an ADR.

## References

- [references/replication-and-shared-libraries.md](references/replication-and-shared-libraries.md): read when considering copying code into services, sizing or splitting shared libraries, or designing versioning, release communication and deprecation policies.
- [references/shared-services.md](references/shared-services.md): read when a shared service is proposed (including a shared data access service), to assess change risk, versioning, latency, scaling and availability, and for a worked library-versus-service analysis.
- [references/sidecars-and-orthogonal-reuse.md](references/sidecars-and-orthogonal-reuse.md): read when standardizing cross-cutting operational behavior, deciding what belongs in a sidecar, choosing sidecar ownership, or explaining duplicate-versus-couple and orthogonal coupling.
- [references/reuse-value-and-platforms.md](references/reuse-value-and-platforms.md): read when someone argues for reuse as a goal, proposes a central entity service, asks how to compare all four techniques side by side, or wants the platform approach.
- [references/source-map.md](references/source-map.md): read to see which reference covers each chapter section.

## Scripts

None. The chapter's guidance is qualitative; the only numeric rule of thumb (roughly half the teams before something joins the sidecar) needs no tooling.
