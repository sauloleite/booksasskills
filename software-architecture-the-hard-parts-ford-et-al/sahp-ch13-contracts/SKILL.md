---
name: sahp-ch13-contracts
description: Guides choosing and governing integration contracts in distributed systems: placing each contract on the strict-to-loose spectrum, versioning, consumer-driven contracts as fitness functions, stamp coupling (over-coupling, bandwidth cost, and its legitimate use for choreographed workflow state). Based on Chapter 13 of Ford, Richards, Sadalage and Dehghani's "Software Architecture: The Hard Parts". Use when designing or reviewing APIs, message schemas or event payloads between services, deciding gRPC vs REST vs JSON maps, auditing payload bloat, or carrying state through a choreographed workflow.
---

# Contracts in Distributed Architectures (SAHP Ch. 13)

## Purpose

A contract here means any format through which parts of an architecture exchange information or depend on each other: RPC signatures, REST resources, GraphQL types, message schemas, shared libraries and their transitive dependencies, caches. Contracts cut across the communication, consistency and coordination forces of every dynamic quantum, so their strictness changes both static and dynamic coupling and can make workflows sturdier or more fragile. This skill helps an agent decide how strict each contract should be, how to keep loose contracts trustworthy, and when shipping a large shared payload is a mistake versus a deliberate workflow tool.

## Key decision rules (apply even without opening references)

1. **Decide contract type before protocol.** Pick strict or loose per integration first; gRPC, REST or JSON is an implementation detail chosen afterward and checked by fitness functions.
2. **Strictness is a spectrum, not a binary.** From strictest to loosest: platform remote method calls (RMI-style), RPC frameworks such as gRPC, JSON plus JSON Schema, REST resources, GraphQL, plain name/value maps (JSON, YAML).
3. **Contracts are glue, so volatility hurts.** Something that changes often and is used by many parts multiplies ripple effects. Use strict contracts only where they pay for themselves.
4. **Strict buys:** guaranteed fidelity, build-time verification, unambiguous documentation, explicit versions. **Strict costs:** every change forces both sides to change; versioning turns into a burden without a deprecation policy and a cap on live versions.
5. **Loose buys:** maximum decoupling, free evolution of each side's internal model and tech stack. **Loose costs:** no schema safety net (typos, missing keys, wrong types), so it needs consumer-driven contract tests or equivalent fitness functions.
6. **Implementation never removes semantic coupling.** Loosening the format lets implementations evolve, but a change in meaning still needs coordination with everyone who depends on that meaning.
7. **Need-to-know contracts.** Each consumer's contract should carry only what it uses. Including fields "in case they are needed later" is an anti-pattern: unrelated provider changes break consumers that never read those fields.
8. **Make strictness match semantic coupling and change cadence.** Tight contracts suit collaborators whose data changes together; loose contracts suit slow-changing or peripheral collaborators, and consumers you cannot redeploy quickly (app-store mobile clients, partner systems).
9. **Consumer-driven contracts (CDC) resolve loose-but-governed.** Consumers pull: they write tests for exactly what they need and hand them to the provider, whose pipeline must keep them green. CDC can be stricter than schemas (value ranges, cross-field rules) but demands disciplined teams and two mechanisms instead of one.
10. **Stamp coupling (passing a big structure where each service touches a slice) is usually accidental.** It over-couples and wastes bandwidth. Bandwidth per edge = requests/s x payload size; compare the full payload to the needed fields.
11. **Stamp coupling is legitimate for choreographed workflow state.** When scale pushes you to choreography on a complex workflow, the contract can carry domain data plus workflow status, transactional state and errors. Accept the higher coupling knowingly; for atomic consistency, services must re-broadcast the contract to earlier participants to compensate.

## Default workflow

1. **Inventory edges.** List every integration point (sync calls, events, shared libraries, caches) in the workflow under review.
2. **Characterize each edge.** Semantic coupling to the partner, change cadence, deploy agility of each side, number of consumers, required fidelity (money, regulation), request rate and payload size.
3. **Place on the spectrum.** Default to loose; move toward strict only where fidelity, build-time checks or documentation needs justify the coupling. Record a versioning and deprecation policy for every strict contract.
4. **Govern loose edges.** Specify CDC tests per consumer and wire them into the provider pipeline as blocking checks.
5. **Audit payloads.** Run `scripts/contract_usage.py` to find unused fields, single-consumer fields and bandwidth waste; trim to need-to-know unless the payload is a deliberate workflow-state carrier.
6. **Decide workflow state placement.** Mediator holds state, or stamp-coupled contract carries it under choreography; state the coupling and bandwidth cost explicitly.
7. **Write an ADR per non-obvious edge** with context, decision, consequences and a revisit trigger (for example, "revisit if mobile releases become continuous").

## References

- [references/strict-vs-loose-contracts.md](references/strict-vs-loose-contracts.md): read when deciding where a contract sits on the spectrum, comparing gRPC, REST, GraphQL and name/value formats, designing a versioning policy, or assigning different strictness to edges of one workflow.
- [references/consumer-driven-contracts.md](references/consumer-driven-contracts.md): read when services own separate bounded-context models, when loose contracts need verification, or when setting up CDC tests and judging team readiness for them.
- [references/stamp-coupling.md](references/stamp-coupling.md): read when payloads are large or shared, when estimating bandwidth, when a consumer breaks on fields it ignores, or when choreographing a complex workflow that must carry its own state.
- [references/source-map.md](references/source-map.md): read to trace a chapter section to the reference that covers it.

## Scripts

- `scripts/contract_usage.py`: run to compute, from a provider field list (optionally with byte sizes) and per-consumer usage lists, the unused fields (stamp coupling), fields used by a single consumer, fields consumers expect but the provider lacks, each consumer's over-coupling ratio, and bandwidth waste at the given request rate.
  - `python3 scripts/contract_usage.py spec.json` (text report)
  - `python3 scripts/contract_usage.py spec.json --format json`
  - `python3 scripts/contract_usage.py spec.json --max-unused-ratio 0.5` (exits 1 if any consumer receives more than half unused fields; usable as a fitness function in CI)
  - `python3 scripts/contract_usage.py --help` for the input format.
