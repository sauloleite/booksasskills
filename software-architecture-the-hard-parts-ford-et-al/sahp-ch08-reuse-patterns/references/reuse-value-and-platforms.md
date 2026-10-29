# When reuse adds value, platforms, and choosing a technique

## Contents
- Reuse is not automatically good
- The central entity anti-pattern
- Abstraction versus rate of change
- Reuse via platforms
- Choosing among the four techniques
- Worked example

## Reuse is not automatically good

Organizations often treat reuse as a goal in itself. Skipping the trade-off analysis can cause serious structural damage, and many of the costs only become visible later. Orchestration-driven service-oriented architecture in the early 2000s made maximal reuse a primary objective and taught the industry this lesson the hard way.

## The central entity anti-pattern

Picture a bank whose retail lending, cards, wealth management and fraud divisions each care about different facets of a customer. The reuse-maximizing reflex is to merge them into one enterprise Customer service. Two failures follow:

1. **Complexity.** The single entity must satisfy every division's scenarios, so it becomes too heavy and convoluted for simple uses.
2. **Brittleness.** Every domain depends on one place. When the service changes to serve one division, the change can ripple into all others, demanding cross-domain coordination and testing.

Prefer letting each domain own the customer facets it needs and integrate through contracts.

## Abstraction versus rate of change

Reuse has two aspects:
- **Abstraction** is how candidates are *found*: noticing commonality.
- **Rate of change** decides whether reuse actually *pays*.

Things everyone reuses successfully (operating systems, open source frameworks and libraries) share a slow, well understood change rate and release cadence. Coupling to them is cheap. Internally built domain capabilities and fast-moving technical frameworks are the opposite and make poor coupling targets. In short: abstraction suggests reuse; slow change makes it work.

**Applying it.** For each reuse candidate, measure change frequency from version control (commits or releases per quarter on that code), not from memory. Low frequency plus broad demand favors sharing; high frequency favors either a service (if sharing is still required) or no sharing at all.

## Reuse via platforms

"Platform" is used so loosely it risks semantic diffusion, but the shared core idea is that platforms are now the main unit of reuse: each distinct domain capability is exposed through a well-defined API that hides its implementation. The reasoning is again rate of change. A loosely coupled API lets the implementation change rapidly behind a stable contract. This does not protect against changes in the *meaning* of the data exchanged between domains, but careful encapsulation and contract design limit breaking change and brittleness in integration. (The book treats contract design in its chapter on contracts.)

## Choosing among the four techniques

Qualitative summary in this skill's own framing:

| Question | Replication | Shared library | Shared service | Sidecar / mesh |
|---|---|---|---|---|
| Kind of code | Tiny, static, one-off | General shared logic | General shared logic, consumed by composition | Operational plumbing only |
| Change rate it tolerates | Essentially none | Low to moderate | High | Moderate, centrally managed |
| Platform mix | Any | Single platform preferred | Polyglot friendly | Needs one sidecar per platform |
| Where change risk lands | Every copy must be fixed by hand | Build time, contained by versions | Runtime, all callers at once | Central team, verified by fitness functions |
| Runtime cost to callers | None | None | Latency, scaling and availability coupling | Sidecar overhead on every service |

**Decision sequence.**
1. Operational and needed broadly? Sidecar.
2. Domain logic that changes fast? Reconsider sharing; if still shared, a service with a carefully designed contract.
3. Callers on several languages? Service.
4. Same language, low to moderate change? Library, fine-grained and versioned.
5. Trivial and frozen? Replicate.

## Worked example (invented)

A retailer's architects audit shared assets after a decomposition:
- Currency formatting, unchanged for two years, all services on .NET: library (`formatting`), keep three versions.
- Promotion eligibility rules, changing weekly, called from .NET checkout and a Python recommendation engine: shared service, gRPC for checkout, redundant instances, contract tests for both callers.
- Distributed tracing and token validation: sidecar owned by platform team.
- `[BoundedContext("Orders")]` attribute: copied into each repo.
- Proposed enterprise `Customer` service for all divisions: rejected; each domain keeps its own customer view, synchronized via published events and contracts.
