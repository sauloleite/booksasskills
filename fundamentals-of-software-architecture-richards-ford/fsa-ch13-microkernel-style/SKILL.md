---
name: fsa-ch13-microkernel-style
description: Guides evaluation, design and governance of the microkernel (plug-in) architecture style: stable core vs volatile plug-ins, registries, contracts, data ownership, remote plug-ins, cloud placement, risks, fitness functions and team split. Based on Chapter 13 of Richards and Ford's "Fundamentals of Software Architecture" (2nd ed.). Use when a system needs per-client, per-jurisdiction or per-product customization, when deciding whether a plug-in design is appropriate, when designing a core/plug-in boundary, or when reviewing an existing plug-in system for drift.
---

# Microkernel (Plug-in) Architecture Style

## Purpose

Help an agent decide whether the microkernel style fits a problem, shape the core/plug-in boundary, choose how plug-ins connect and register, and govern the result so it keeps its benefits. The style is a monolith with two kinds of parts: a core system holding the minimal or happy-path processing, and independent plug-ins holding the custom, variable, high-branching logic. Its natural home is installable products and any business domain dominated by customization (per state, per country, per client, per device type).

## Key decision rules

1. **Fit test: customization is the domain.** Favor this style when the problem decomposes into a stable common process plus many variations (rules per jurisdiction, per client, per product model). The structure mirrors the domain, which is why it can be read as both technically and domain partitioned.
2. **The core must be stable.** Before committing, estimate how often the core will change. A core that keeps changing defeats the style; if you cannot find a stable core, choose another style or a "supports plug-ins" design rather than a pure microkernel.
3. **Move cyclomatic complexity out of the core.** Long if/else or switch chains keyed on device, client, region or product type are the signal to extract each branch into a plug-in and replace the chain with a registry lookup plus a generic invocation.
4. **Plug-ins talk only to the core.** Avoid plug-in-to-plug-in dependencies; they force the core to resolve transitive and version conflicts. Treat any such dependency as an exception that needs justification.
5. **The core owns the shared database.** Plug-ins receive data from the core instead of connecting to the central schema. A plug-in may own a private store (external, embedded or in-memory) that nothing else touches.
6. **Standardize contracts per plug-in domain.** One contract (behavior, input, output) per family of plug-ins. Wrap third-party plug-ins whose contracts you cannot control with an adapter so the core never carries per-plug-in special cases.
7. **Keep responsibilities on the right side of the contract.** The core moves and displays plug-in output; it should not interpret plug-in-specific details (for example, a preformatted report is opaque to the core).
8. **Default to in-process (point-to-point) plug-ins.** Compile-time plug-ins are simplest but require redeploying the whole app; runtime plug-ins (OSGi-style frameworks) allow hot add/remove at higher complexity. Choose remote plug-ins (REST or messaging) only after explicit trade-off analysis: you gain decoupling, scalability of plug-ins, async responsiveness and runtime change without frameworks, but you get a distributed system, harder on-prem installation, more cost, and request failure when a synchronous plug-in is down.
9. **Remote plug-ins do not add quanta.** Every request still passes through the monolithic core, so the system remains one architecture quantum, with the core's scalability and fault-tolerance ceiling.
10. **Do not split core and plug-ins across cloud and on-prem lightly.** Plug-in calls are frequent and data-heavy; the latency of separating them usually hurts. Prefer all-cloud, or data-only in cloud.
11. **Know the profile.** Strengths: simplicity, low cost, extensibility, isolated change, ability to trim features for speed. Weaknesses: scalability, elasticity, fault tolerance (monolithic deployment). Testability, deployability, reliability, modularity, evolvability and responsiveness are moderately good when plug-ins are truly isolated.
12. **Govern the philosophy, not just the code.** Watch core churn in version control, the rate of change of the core, contract compatibility across plug-in versions, and structural rules (no cross-plug-in imports, no plug-in access to the shared DB).

## Default workflow

1. Identify the stable common process and list the dimensions of variation (who/where/what varies). If variation is small or the "core" keeps moving, stop and reconsider the style.
2. Place the system on the microkern-ality spectrum: pure (core nearly useless alone) vs plug-in-capable (core fully useful alone). Let core volatility drive this choice.
3. Define plug-in domains, one standard contract per domain, and adapters for third-party contracts.
4. Choose plug-in packaging (namespace/package vs shared library) and binding (compile vs runtime vs remote). Record the reasoning as an ADR.
5. Design the registry: what each entry holds (name, contract, protocol/location) and whether it is an in-core map or an external discovery tool.
6. Decide data ownership: core owns the shared DB; note any plug-in-private stores.
7. Decide deployment and cloud placement; check latency of every core-plug-in hop.
8. Set governance fitness functions and the team split (core stream-aligned team; plug-ins for specialists or experiments).

## References

- [references/core-plugin-design.md](references/core-plugin-design.md): read when designing or reviewing the core, plug-in packaging, binding mode, remote plug-ins, registry, contracts or data ownership.
- [references/fit-tradeoffs-and-use-cases.md](references/fit-tradeoffs-and-use-cases.md): read when deciding whether to use the style, explaining its characteristic profile, placing a system on the microkern-ality spectrum, choosing cloud placement, or looking for analogous examples.
- [references/risks-governance-teams.md](references/risks-governance-teams.md): read when auditing an existing plug-in system, writing fitness functions, handling plug-in dependencies, or organizing teams around core and plug-ins.
- [references/source-map.md](references/source-map.md): read to find which reference covers a given chapter section.

## Scripts

None. The chapter offers no calculation that benefits from a script; governance checks are described as fitness-function ideas in the risks reference.
