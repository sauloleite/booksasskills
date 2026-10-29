# Framing Trade-off Analysis Through Coupling

## Contents
- Why distributed decisions got harder
- The working definition of coupling
- The three-step untangling method
- Coupling as a dose, not a sin
- The canonical hard question: service size and communication
- Static versus dynamic coupling in one page
- Worked example: untangling a "just add a saga" proposal
- Pitfalls
- Glossary

## Why distributed decisions got harder

Distributed systems built with queues and events are decades old, so the mechanisms are not what changed. What changed is the bounded-context philosophy behind microservices. Earlier event-driven designs typically had every handler write to one shared relational database, and that database quietly took care of integrity and transactions. Once each service owns its data inside its own boundary, transactionality stops being a database feature and becomes an architecture decision. Every data split now creates a coordination, consistency and communication question that someone must answer explicitly.

Consequences for an agent:
- Treat any proposal that moves data into service boundaries as also proposing new transactional and workflow problems. Name them.
- Do not offer generic "best practices" for granularity or communication. The chapter's stance is that no universal answer exists for real, complex systems; the goal is the least bad set of trade-offs for this case.
- Established methods such as ATAM exist, but they are not tuned to the everyday problems architects face in distributed systems. Prefer the coupling-centered method below for those problems.

## The working definition of coupling

Use the simplest, change-based definition: two parts are coupled when changing one may force a change in the other. This definition is deliberately operational. It lets you ask about any pair of things (service and database, service and UI, two services in a workflow, a service and its broker) the same question: if I change X, what else might have to change, be redeployed, or be retested?

## The three-step untangling method

Complex architecture problems are multi-dimensional: several forces interact and depend on each other, like strands in a braid. You cannot weigh them until you separate them. Apply these steps in order:

1. **Find the entangled parts.** List every element involved in the decision: services, data stores, brokers, UIs, orchestrators, libraries, platform pieces, and the workflows that cross them.
2. **Analyze how they are coupled.** For each pair, decide whether the coupling is static (needed to bootstrap and run) or dynamic (arises only during a runtime call), and for dynamic coupling characterize communication, consistency and coordination.
3. **Assess the trade-offs by the impact of change.** For each candidate design, trace what a change to each part would ripple into, and what operational characteristics (scale, elasticity, performance, availability) become shared or independent.

Only after step 2 can you list which forces actually trade against each other; skipping it produces apples-to-oranges arguments (for example, comparing a service bus product with a streaming platform as if they solved the same problem).

## Coupling as a dose, not a sin

The chapter opens with the toxicology idea that the amount, not the substance, determines harm. Apply it literally: a system with zero coupling does nothing useful, because nothing can talk to anything. Advice that only says "decouple" gives no guidance on how much or where. Driving services very fine-grained to maximize decoupling simply relocates the pain into orchestration, transactions and asynchrony. The architect's job is choosing where coupling buys something (atomicity, simplicity, responsiveness) and where it costs too much (shared release cadence, shared scaling limits, cascading failures).

## The canonical hard question: service size and communication

The book uses one question as its running problem: how big should a microservice be, and how should services talk? Both extremes fail:
- Too small: transactions span services, workflows need heavy orchestration, consistency becomes hard.
- Too large: scaling, deployment and distribution suffer because unrelated concerns share one unit.

Do not answer this question directly. Decompose it into static coupling (what each unit needs to run), dynamic coupling (how units interact in workflows), and the impact-of-change analysis above. Later chapters supply the integrator and disintegrator forces for granularity, data ownership patterns and saga patterns; this chapter supplies the vocabulary.

## Static versus dynamic coupling in one page

| Aspect | Static coupling | Dynamic coupling |
|---|---|---|
| Question it answers | What must exist for this unit to start and operate? | What happens when units interact during a workflow? |
| Typical elements | OS, runtime, frameworks, transitive libraries, data store, broker presence, orchestration platform, UI it is bound to | Call style (sync/async), transactional strictness, orchestration vs choreography |
| How to measure | Mostly at build time: manifests, dependency files, deployment descriptors | Continuously at runtime: monitoring, tracing, call logs |
| What it scopes | Quantum boundaries and therefore the scope of operational characteristics | Temporary entanglement of quanta during calls |

Note the subtle point about brokers: the broker existing is static coupling (the service cannot run without it); a service sending a message through it to another service is dynamic coupling.

## Worked example: untangling a "just add a saga" proposal

Scenario (invented): a team wants to split an Invoicing module into Invoice, Tax and Payment services and "wire them with a saga" so each service can be tiny.

1. Entangled parts: three services, the current shared billing schema, an API gateway, a web checkout UI, the payment provider, the posting workflow.
2. Coupling analysis: if all three keep the shared schema, they are still one quantum statically, so the split buys code separation but not independent deployment or scaling. If the schema is split, the posting workflow needs either an atomic cross-service transaction or eventual consistency, plus a choice of orchestrator or choreography, and a sync or async call style per step.
3. Impact of change: an atomic, synchronous, orchestrated flow keeps the business rule "invoice exists only if tax was computed" simple but ties the three services' availability and latency together. An asynchronous, eventual, choreographed flow lets each scale alone but needs compensation logic and tolerance for temporarily inconsistent views.
Recommendation pattern: present both options with what each buys and costs; do not declare the saga a default.

## Pitfalls

- Treating "loosely coupled" as an end in itself rather than a dose to tune.
- Comparing tools before separating the forces they address.
- Measuring dynamic coupling with build-time analysis only; runtime coupling needs continuous monitoring.
- Assuming that more services automatically means more independence (a shared database or UI can collapse them back to one quantum).

## Glossary

- **Coupling (change-based):** a change in one part may require a change in another.
- **Static coupling:** operational and build dependencies a unit needs to run.
- **Dynamic coupling:** runtime interaction between quanta during workflows.
- **Least worst:** the set of trade-offs that best fits the specific context, accepting that every option has costs.
