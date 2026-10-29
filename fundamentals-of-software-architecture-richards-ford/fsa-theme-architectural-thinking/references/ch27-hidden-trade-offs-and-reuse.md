# Hidden Trade-Offs, Reuse, and Repeated Analysis

This file covers the two corollaries of the first law: (1) an apparent free win means the trade-off is still undiscovered, and (2) trade-off analysis is never finished once and for all.

## Corollary 1: there is always a missing trade-off

When a choice seems to have only upside, assume the analysis is incomplete and keep searching. Useful probes:

- What does this cost later (change, migration, operations), not just now?
- Who else becomes coupled to this choice, and what happens to them when it changes?
- Which architecture characteristic gets worse (security, scalability, evolvability, testability, deployability)?
- What does it constrain in the future (choice of language, team boundaries, release cadence)?
- Was it ever a widely praised practice that later caused pain elsewhere?

## Worked case: code reuse

Reuse looks purely beneficial: less code to write, less duplication. Its effectiveness actually depends on two conditions, and teams usually check only the first.

1. **Abstraction.** The code can be cleanly generalized and called from multiple places.
2. **Low volatility.** The code rarely changes.

Why volatility matters: when shared code changes, every consumer must coordinate around the change. Even a non-breaking change obliges each consumer to verify nothing broke. If shared code churns, that coordination cost multiplies across the system, and teams spend their time chasing breakages through the architecture.

Historical lesson: orchestration-driven service-oriented architecture made maximal reuse a founding goal. Teams in those systems found that each change could trigger unpredictable side effects far away, so progress felt like wading through mud.

Resulting guidance:

| Reuse target | Volatility | Recommendation |
|---|---|---|
| Technical plumbing (frameworks, logging, security libraries, platforms) | Low | Good candidate; share it |
| Domain concepts and business rules | High | Poor candidate; duplicate or keep local |

The domain is usually the fastest-changing part of an application, because it is the reason the software exists. This is also the logic behind bounded contexts in domain-driven design: one context never reuses another's implementation details.

Agent heuristics:

- Before recommending a shared module, ask for its change history (commits per month, number of consumers). High churn plus many consumers is a red flag.
- Prefer sharing stable technical capabilities; for domain logic, prefer duplication with clear ownership, or expose it through a well-defined interface owned by one context.
- When reuse is already in place and painful, look for the volatile part and pull it back into the owning context.

## The reuse versus decoupling impossibility

Organizations often ask for a highly decoupled distributed architecture (for agility and independent deployment) and, at the same time, extensive cross-team reuse so nobody rewrites anything. These goals conflict at the root: reuse is achieved by coupling consumers to a shared artifact. More reuse means more coupling, which erodes the independence that motivated the distributed style.

How to respond:

- State the conflict explicitly and ask which goal ranks higher.
- If decoupling ranks higher: limit reuse to stable plumbing; accept some domain duplication.
- If reuse ranks higher: accept coordinated releases and consider a less distributed style.
- Place the answer on a spectrum (for example, a small set of versioned platform libraries, nothing domain-specific), not as all or nothing.

## Corollary 2: analysis must be repeated

It is tempting to analyze once and issue a permanent rule ("all workflows use choreography"). Two problems prevent that:

- Decisions depend on many variables: how complex the problem is, how skilled and how organized the teams are, money, deadlines, and much more. Small differences among them can push the result either way.
- Assumptions that held for one application may not hold for the next, so blanket rules are risky.

The real job is ongoing analysis, not perfect permanent decisions. The authors frame this, half jokingly, as job security for architects.

Agent behavior:

- When a user cites an organizational standard ("we always do X"), check whether the conditions that justified X still hold for the current case.
- When proposing a standard, attach its assumptions and the conditions that would invalidate it.
- In ADRs, record re-analysis triggers (volume thresholds, team changes, new compliance rules).

## Pitfalls

- Declaring a pattern "best practice" without naming what it costs.
- Sharing domain models across services to save effort.
- Promising stakeholders both maximum decoupling and maximum reuse.
- Copying a previous project's decision because the situation looks similar.
