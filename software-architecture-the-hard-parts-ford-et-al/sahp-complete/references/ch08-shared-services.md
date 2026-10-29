# Shared services

## Contents
- What it is and the composition constraint
- Change risk and versioning
- Performance
- Scalability
- Fault tolerance
- Strengths, weaknesses and fit
- Worked example: shared data access, library or service?
- Review questions

## What it is

Common functionality is deployed as its own service and called at runtime by the services that need it. It was the usual answer to shared behavior in earlier distributed styles. Updating the shared logic means redeploying one service; consumers are not rebuilt.

**Composition, not inheritance.** A remote service can only be used by calling it. If the shared code is meant to be extended (base classes, template methods, overridable hooks), it cannot become a shared service without redesign. Check this before proposing the technique; whether the code is consumed by composition or inheritance is an architectural constraint here, not merely a style choice.

## Change risk and versioning

The advantage and the danger come from the same property. A change to, say, a tax calculation service is live for every caller the moment it is deployed, with no consumer retesting. But that also means a faulty or incompatible change can break every caller at once, at runtime, in production. A library change, by contrast, only reaches a service when that service is rebuilt and tested against it.

**Versioning options and their problems.**
- *Version in the endpoint path* (for example `/v2/tax`, `/v3/tax`): each consumer, or its configuration, must be updated to target the right version.
- *Deciding when a change deserves a new version is subjective.* Does a reworded error message count? A new rule? Teams will disagree.
- *Multiple protocols.* If the service is reached via REST, a message queue, and gRPC, versions must be coordinated across all channels, which is much harder than path versioning alone.

Net: runtime change carries more risk than compile-time change, and versioning reduces but does not remove it while costing more effort than library versioning.

## Performance

Each use of shared functionality becomes a network hop, plus security overhead if the endpoint is authenticated. A library call has neither. Mitigations:
- gRPC to reduce per-call network overhead.
- Asynchronous request/reply over messaging: send the request to a request queue, keep working, and pick up the answer later from a reply queue, matched by a correlation ID.

## Scalability

The shared service must absorb the combined load of all callers. When callers scale out, the shared service must scale with them, and several callers peaking concurrently compounds the problem. Libraries scale automatically with their host service.

## Fault tolerance

If the shared service is down, every service that depends on it for that function stops working for that function. Multiple instances help, but the dependency remains a trade-off to state explicitly. Libraries avoid this entirely because the code runs in process.

## Strengths, weaknesses and fit

Strengths: handles volatile shared logic well; one implementation regardless of caller language; bounded context preserved because no code is shared statically.

Weaknesses: versioning is awkward; latency is added; availability and throughput are coupled to the shared service; every change is a runtime change with system-wide blast radius.

Fit: highly polyglot estates and shared functionality that changes frequently. Even then, watch for runtime side effects on callers.

## Worked example (invented)

**Situation.** An insurer splits claims handling into Claim Intake (customer-facing, high traffic), Claim Triage and Claim Settlement. All three run the same database queries and updates against shared claim tables. One proposal wraps that logic in a Claim Data service; another packages it as a library each service links.

**Method.** Treat it as a hypothesis ("a shared data service is the better option") and test it against the actual services, rather than debating preferences.

| Consideration | Shared data service | Shared library |
|---|---|---|
| Latency | Every query becomes a remote call; hurts the customer-facing intake service most | In-process |
| Availability | Data service outage stops all three services | No new runtime dependency |
| Scaling | Must scale the data service whenever intake scales | Scales with each service |
| Change risk | Runtime change; to be safe, all three services must be regression tested on every data service release | Versioned; services adopt changes deliberately |
| Abstraction | Callers know nothing about the database | Callers include the data access code |
| Connection pooling | Centralized, but still needs several instances for intake load | Each service manages its own pool |
| Deploying data logic changes | Only the data service redeploys | Consuming services retest and redeploy |

**Evidence step.** Look at the version history of the shared data access classes. If changes are rare, the main argument for a service (easy rollout of frequent changes) disappears.

**Outcome in this case.** Low change rate, a latency-sensitive customer-facing caller, and few services mean the library wins. Record the decision in an ADR, including the consequences: data logic changes require retesting and redeploying the claim services, and each service owns its connection pool.

The chapter's own story reaches the same verdict for a ticketing domain split into three services; its point is that "the backend is not latency sensitive" collapses as soon as one caller is customer-facing, and that perceived volatility must be checked against repository history.

## Review questions

- Is the shared code consumed by composition? If it relies on inheritance, a service is not an option.
- How often has it actually changed over the past year?
- Which callers are latency-sensitive or customer-facing?
- What happens to each caller when the shared service is unavailable?
- How will the shared service scale relative to its busiest callers?
- Which protocols reach it, and how will versions be expressed on each?
- Who regression tests the callers when the shared service changes?
