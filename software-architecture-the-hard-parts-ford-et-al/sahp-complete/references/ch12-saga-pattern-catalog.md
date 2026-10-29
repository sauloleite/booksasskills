## Contents

- The three forces and the eight combinations
- How to read a pattern (the qualitative lenses)
- Epic Saga (sao)
- Phone Tag Saga (sac)
- Fairy Tale Saga (seo)
- Time Travel Saga (sec)
- Fantasy Fiction Saga (aao)
- Horror Story (aac)
- Parallel Saga (aeo)
- Anthology Saga (aec)
- Selection playbook
- Common mistakes when picking a saga
- Glossary

# Saga Pattern Catalog

## The three forces and the eight combinations

A saga in this book is any workflow that spans several services, each with its own data, and that must leave the system in a sensible state. The concept is older than microservices: it was proposed in a 1987 ACM paper as a way to keep database lock scopes small, and Chris Richardson later popularized the microservices form (local transactions chained by events, with compensating updates on failure). The chapter widens that single form into a design space defined by three binary forces:

| Force | Values | Code letter |
|---|---|---|
| Communication | synchronous / asynchronous | s / a |
| Consistency | atomic / eventual | a / e |
| Coordination | orchestrated / choreographed | o / c |

Every saga sits at one of the eight corners of this cube. The book gives each corner a story-genre nickname and a three-letter code in the order communication, consistency, coordination, so "aeo" always means asynchronous, eventual, orchestrated. Prefer the code when talking to people who have not read the book; the nickname is only a handle.

A monolith would sit at the origin of this space (no distribution at all). The Epic Saga is the distributed corner closest to that monolithic behavior, and the Anthology Saga is its exact opposite.

Key mental model: the three forces are entangled. Changing one changes how the other two behave, so never evaluate a single force in isolation. Atomic consistency is the most coupling-intensive force by a wide margin; synchronous calls and a central orchestrator add coupling too, but much less.

## How to read a pattern

For each pattern, weigh four qualitative lenses:

- **Coupling**: how tightly participants are bound together in time, state and workflow knowledge.
- **Complexity**: design, debugging and operational effort, especially for error paths.
- **Responsiveness and availability**: how quickly the caller gets an answer and whether one unavailable participant breaks the whole workflow.
- **Scale and elasticity**: whether participants can grow independently without a choke point.

The chapter illustrates each pattern with "isomorphic" diagrams: deliberately generic service boxes that show only the interaction shape that makes a pattern different. Use the same trick when explaining a design: strip out domain names and show only who calls whom, synchronously or not, and where the undo logic lives.

## Epic Saga (sao): synchronous, atomic, orchestrated

**Shape.** An orchestrator calls each participant in turn and expects all of them to succeed or all to be undone. If a late call fails, the orchestrator sends compensating requests to every participant that already committed.

**Why teams pick it.** It mirrors monolithic transactions, has a familiar name ("orchestrated saga"), gives a single obvious workflow owner, and stakeholders often insist that all state must change together.

**Strengths.** Clear ownership; synchronous calls remove race conditions and deadlocks during the forward path, which keeps design complexity manageable.

**Weaknesses.** It is the most tightly coupled of the eight. The orchestrator must wait on every participant, so it becomes a timing bottleneck that hurts responsiveness, throughput and elasticity. Any unavailable participant or unrecoverable error fails the whole request. Compensating updates bring their own failure modes (see the compensation reference).

**Warning.** A named pattern only proves the problem is common, not that it is cleanly solvable. Moving local ACID semantics into a distributed system is not an incremental step, and the difficulty grows with the semantic complexity of the workflow. Use the Epic Saga only when atomicity is a genuine business requirement, and try hard to shrink its scope first.

## Phone Tag Saga (sac): synchronous, atomic, choreographed

**Shape.** No orchestrator. The first service called acts as a front controller: it does its work, then synchronously calls the next participant, and so on down the chain. On failure, each service must carry logic to send compensations back up the chain.

**Strengths.** No coupling singularity. On the happy path, the last service can answer, so there are fewer wait points and somewhat better throughput than the Epic Saga. Synchronous hand-offs guarantee each step finishes before the next starts, so no race conditions.

**Weaknesses.** Atomicity still needs coordination, so workflow knowledge, error handling and routing leak into domain services. Complexity rises roughly in step with workflow complexity, and for rich workflows the front controller ends up as complicated as a mediator. Error paths are slow because unwinding happens service to service. Scale improves only a little, since two of three forces remain tight.

**When it fits.** Rare combination (choreography usually travels with asynchrony). Choose it for simple workflows with few error paths, ideally where participants are idempotent and can retry, and where you want more parallel capacity than an orchestrator allows. Workflow state can ride inside the messages (stamp coupling) at the cost of larger payloads.

## Fairy Tale Saga (seo): synchronous, eventual, orchestrated

**Shape.** An orchestrator handles requests, responses and errors, but each participant owns its own local transaction. The orchestrator may still trigger corrective calls, just not inside a global transaction.

**Strengths.** Combines the two easiest choices (synchronous calls, a mediator) with the loosest consistency requirement. Dropping holistic transactions removes the hardest coordination problem, especially for errors. If a participant is briefly down, the change can be held and applied later. The orchestrator keeps less time-critical transaction state, which makes it easier to load-balance. Participants can scale more independently.

**Weaknesses.** Coupling stays fairly high (synchronous plus orchestrated). Responsiveness is better than atomic variants but not as good as asynchronous ones.

**When it fits.** A common, well-balanced default for microservices whenever the business can accept eventual consistency.

## Time Travel Saga (sec): synchronous, eventual, choreographed

**Shape.** Each service receives a request, does its part in its own transaction, and passes the request onward. This is a natural fit for Chain of Responsibility or Pipes and Filters: one-way sequences of steps. The name reflects that consistency arrives gradually over time.

**Strengths.** No global transaction and no mediator, so coupling is moderate and scale is very good. Excellent for fire-and-forget, high-throughput work such as bulk ingestion or batch transaction feeds. Synchronous calls remain easy to reason about and debug.

**Weaknesses.** Every service must hold most of the workflow state and handle its own error recovery. Error recovery over synchronous calls adds overhead and slows responses. Data synchronization needs deliberate extra effort.

**When it fits.** Simple, linear workflows. Treat it as an on-ramp: if it scales well enough, stop here; if not, add asynchrony and move to the Anthology Saga.

## Fantasy Fiction Saga (aao): asynchronous, atomic, orchestrated

**Shape.** Like the Epic Saga, but the orchestrator talks to participants asynchronously.

**Why it appears.** Someone tries to speed up an Epic Saga by making calls parallel while keeping atomicity.

**Weaknesses.** Asynchrony multiplies coordination state. While workflow A is pending, workflow B starts; then workflow C needs the unresolved outcome of A. The orchestrator must track every pending transaction and their interdependencies, and must cope with ordering loss, deadlocks and race conditions. Coupling remains very high, design and operational complexity rise, responsiveness suffers (badly when a participant is down), and high scale is practically unattainable while transactions span services.

**Recommendation.** Usually the wrong answer. If the goal is performance, relax consistency instead: the Parallel Saga keeps the orchestrator and asynchrony but drops the global transaction.

## Horror Story (aac): asynchronous, atomic, choreographed

**Shape.** No mediator, asynchronous messages, and yet a demand for all-or-nothing outcomes.

**Why it is the worst.** It pairs the strictest consistency demand with the two loosest coordination styles. Each service must remember undo data for many in-flight transactions that may arrive out of order and must negotiate with peers during failures. Picture transaction A failing while B is half done: services must reverse A's effects in reverse order without disturbing B.

**Nuance.** Its raw coupling is not the highest (the Epic Saga holds that title) because it removes the mediator and synchronous waits. Scale is better than mediator-based atomic sagas. But its complexity is the worst of all eight, and the inter-service chatter needed to coordinate keeps responsiveness low.

**How teams fall into it.** Start with an Epic Saga, notice it is slow, then add asynchrony and choreography because each one "improves performance" in isolation. The lesson: these forces are entangled, so a local optimization on one axis can wreck another.

**Recommendation.** Replace with the Anthology Saga (drop holistic atomicity).

## Parallel Saga (aeo): asynchronous, eventual, orchestrated

**Shape.** An orchestrator coordinates requests and responses asynchronously; each participant owns its transaction. Shared data may need synchronization, either in the background or driven by the orchestrator. On error, the orchestrator sends asynchronous corrective messages (retries, data resynchronization, other remediation).

**Strengths.** Relaxes the two forces that slow the Epic Saga most (atomicity and synchronous waiting) while keeping a mediator, so complex workflows and error handling stay tractable. Coupling and complexity are low; responsiveness and scale are high. Because transactions are scoped to each service, the architecture can scale per domain: a public-facing service can be highly elastic while a back-office service stays small and locked down.

**Weaknesses.** The mediator carries more error-resolution burden without a global transaction to lean on. Asynchrony brings timing problems: race conditions, deadlocks, queue reliability.

**When it fits.** Complex workflows that also need high scale. Often the best replacement for an Epic or Fantasy Fiction design.

## Anthology Saga (aec): asynchronous, eventual, choreographed

**Shape.** Services exchange messages through queues with no orchestrator; each keeps its own transactional integrity and must know enough about the workflow to handle errors.

**Strengths.** The loosest coupling of all eight, no choke points, the highest potential throughput, scale and elasticity, and high responsiveness (no transactional or synchronous speed governors).

**Weaknesses.** Services become more complex; resolving data consistency errors is hard without a mediator. Coordination becomes prohibitive for complex or critical workflows. Stamp coupling can carry workflow state in messages, as with the Phone Tag Saga.

**When it fits.** Simple, mostly linear, very high-throughput flows with rare or easy errors. Pipes and Filters is the textbook match.

## Selection playbook

Ask these questions in order:

1. **Is atomic consistency truly required by the business, or merely familiar?** Challenge it. Ask what actually goes wrong if one step lands seconds or minutes later. Much of the real world runs without two-phase commit (Gregor Hohpe's "Starbucks does not use two-phase commit" essay makes this point). If eventual consistency is acceptable, you are choosing among Fairy Tale, Time Travel, Parallel and Anthology.
2. **How complex is the workflow, and how frequent are its error paths?** The usefulness of a mediator rises with workflow complexity. Complex or critical workflows: orchestrate (Fairy Tale or Parallel). Simple, linear, rarely failing workflows: choreography is viable (Time Travel or Anthology).
3. **How much scale and responsiveness do you need?** If synchronous calls meet the target, stay synchronous (easier to build and debug). Add asynchrony only when needed, accepting race conditions, ordering and queue reliability work.
4. **If atomicity is non-negotiable:** prefer the Epic Saga with the smallest possible scope; consider Phone Tag only for simple chains. Avoid Fantasy Fiction and Horror Story; their extra asynchrony or choreography buys little and costs a lot.
5. **Record the choice** with the trade-off accepted on each axis, and revisit it when workflow complexity or load changes.

Quick heuristics:

- Need atomic plus complex workflow: Epic Saga, shrunk as far as possible.
- Need eventual plus complex workflow plus moderate load: Fairy Tale.
- Need eventual plus complex workflow plus high load: Parallel.
- Need eventual plus simple linear flow: Time Travel first, Anthology when load demands it.

### Worked example (invented)

A travel platform books a flight, a hotel and a car for one trip. The product owner first asks for "all or nothing", which yields an Epic Saga: the booking orchestrator holds the traveler on a spinner while three partner APIs respond, and any partner outage cancels the trip. Probing reveals that what customers actually need is a guaranteed flight, with hotel and car confirmed within an hour or offered alternatives. The architect switches to a Parallel Saga: the orchestrator confirms the flight, fires hotel and car requests asynchronously, tracks saga state (FLIGHT_CONFIRMED, HOTEL_PENDING, CAR_FAILED, and so on), retries partner failures and escalates to an agent after a deadline. Responsiveness improves sharply and partner outages no longer cancel trips; the cost is a period where the itinerary is incomplete and a heavier orchestrator.

## Common mistakes when picking a saga

- Defaulting to the Epic Saga because it feels like the monolith.
- Trying to buy speed for an atomic saga with asynchrony (creates Fantasy Fiction) or with asynchrony plus choreography (creates the Horror Story).
- Choosing choreography for a workflow with many branches and error paths; the "simple" services quietly become mediators.
- Assuming a pattern name implies a clean, solved implementation.
- Treating the eight corners as good versus bad; all have legitimate uses, but each has a distinct trade-off profile.

## Glossary

- **Isomorphic diagram**: a generic interaction sketch that shows only the communication shape distinguishing one pattern from another.
- **Front controller**: in a choreographed atomic saga, the first service called, which ends up coordinating the chain.
- **Coupling singularity**: a single component (usually the orchestrator) that every workflow instance depends on.
- **Stamp coupling for workflow**: carrying workflow state inside the messages so choreographed services know where they are in the flow.
- **Holistic transaction**: one transaction boundary spanning all participants, as opposed to each service committing locally.
