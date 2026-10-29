# Architecture Quantum and Static Coupling

## Contents
- Definition and the four criteria
- Criterion 1: independently deployable
- Criterion 2: high functional cohesion
- Criterion 3: high static coupling (inside the quantum)
- Criterion 4: synchronous dynamic coupling (pointer)
- The bootstrap test
- Counting quanta across topologies
- User interfaces and micro-frontends
- Quantum versus bounded context
- Building a static quantum diagram
- Checklist
- Pitfalls

## Definition and the four criteria

An architecture quantum is the unit that measures both topology and runtime behavior. A unit qualifies when it is:
1. independently deployable,
2. highly functionally cohesive,
3. highly statically coupled internally (everything it needs to run comes along), and
4. joined to other quanta through runtime calls, where synchronous calls can temporarily bind them.

The typical example is a well-formed microservice taking part in a workflow. Word usage: singular "quantum", plural "quanta" (Latin "how much"; the same pattern as datum/data). Static coupling captures how parts are wired; dynamic coupling captures how they call each other. Static coupling is about operational dependencies, dynamic coupling about communication dependencies.

## Criterion 1: independently deployable

Each quantum is a separate deployable unit. A monolith deployed as one artifact is, by definition, exactly one quantum. A microservice is a candidate quantum, subject to its coupling.

Why this boundary is worth naming:
- **Shared vocabulary.** Architects read it as a coupling scope, developers as a behavior scope, operations as a deployment scope. Everyone discusses the same box.
- **A granularity force.** Release cadence, blast radius of a deploy, and engineering practices per unit all depend on where deploy boundaries are.
- **It drags in the database.** Independent deployment must include common coupling points. A shared database that has its own release cadence breaks independent deployability for every service using it, unless schema and application deploy in lock step. Many "distributed" systems fail here.

Deployability alone is too coarse (a giant monolith passes it), so always pair it with cohesion.

## Criterion 2: high functional cohesion

Functional cohesion means related behavior and data sit close together. At the domain level it lines up with a bounded context: the behavior and data that carry out one domain workflow. Large monoliths are deployable as one unit but rarely cohesive, and cohesion tends to fall as size grows. In a microservices design each service ideally models one domain or workflow. Cohesion here is about how independent one service is from others, not about how services cooperate.

## Criterion 3: high static coupling (inside the quantum)

Everything inside a quantum is tightly wired together, and that wiring is a matter of contracts. Contracts include more than REST or SOAP payloads: method signatures, library versions and operational endpoints (hosts, URLs, queue names) all count. Static coupling resolves through these contracts and covers the OS, frameworks, transitively managed libraries, data stores, brokers, container platform and any other operational prerequisite. Use the strictest available view of each dependency when deciding whether it binds units together.

Side effect worth exploiting: static coupling defines the scope of operational characteristics. Whatever is statically fused must share scalability, elasticity, availability and security targets, because it scales and fails together.

## Criterion 4: synchronous dynamic coupling (pointer)

The last criterion concerns how quanta behave together at runtime. A synchronous call makes caller and callee share responsiveness, availability and scale for the duration of the call. Details are in the dynamic coupling reference.

## The bootstrap test

The single most useful question: "Is this element required to bring this unit up and keep it operating?" Imagine provisioning the service on an empty environment and list everything you must install or reach: language runtime, application framework, every library in the dependency manifest, container image and orchestrator, database, message broker, secrets store, configuration service, and any other service it cannot start or function without.

Rules that follow:
- A service that never touches the database still joins the database's quantum if it statically depends on a service that does.
- Any holistic coupling point that the whole architecture needs in order to work (shared database, central mediator, tightly bound UI) forms one quantum around everything attached to it.
- A unit that can run in a production-like environment and send and receive requests on its own is its own quantum, even if it cannot complete every business workflow alone.

## Counting quanta across topologies

Use these patterns as quick heuristics (described in prose; derive the count from the actual dependencies):

- **Any monolith (layered, modular, pipeline, microkernel) with one database:** one quantum. The database is the usual single coupling point in domain systems.
- **Service-based architecture:** separately deployed UI, coarse domain services, one shared relational database. Services are isolated in code but the database makes it one quantum. This hybrid is intentional when teams see little value (or too many costs) in splitting data, and it is a common first target when breaking up a monolith because schemas and integrations stay intact.
- **Mediator event-driven architecture:** one quantum, because both the shared database and the central request orchestrator are coupling points the system cannot run without.
- **Broker event-driven architecture with one shared database:** still one quantum. Removing the mediator reduces coupling but does not remove the data coupling point.
- **Broker event-driven architecture with separate data stores and no static links between service groups:** multiple quanta, one per independent group.
- **Microservices with per-service data and no shared coupling points:** potentially one quantum per service, each free to have its own characteristics (one more scalable, another more secure) and its own team pace.
- **Two otherwise separate systems integrated through a shared database:** one quantum spanning both systems.

Distributed topologies make multiple quanta possible; they never guarantee them.

## User interfaces and micro-frontends

A UI tightly bound to many back-end services is a coupling point: it usually stops working when parts of the back end are unavailable, and it makes per-service operational characteristics hard to vary, especially when it calls services synchronously. A microservices back end behind such a UI can collapse to a single quantum.

The decoupled alternative is a micro-frontend approach: each service emits its own UI fragment, the shell page only provides a canvas, and fragments communicate loosely (typically through events). Each service plus its fragment then forms its own quantum with its own characteristics.

## Quantum versus bounded context

The quantum is roughly the architectural counterpart of a bounded context. The two overlap on cohesion and independent deployment, but the quantum adds explicit static and dynamic coupling analysis. Keep the terms distinct to avoid overloading the precise DDD meaning.

## Building a static quantum diagram

Drawing how things are wired is an effective way to understand a legacy estate, predict what a change will hit, and find decoupling opportunities. It also supports defensive reliability work: before changing anything, know what must be retested and which teams could be affected.

No off-the-shelf tool fits every mix of technologies, so expect to assemble one:
- Build-time sources: container manifests, dependency files (Maven, npm, pip and similar), infrastructure-as-code, deployment descriptors.
- Runtime sources: consistent logs and tracing showing who calls whom, when and how often, aggregated into a call graph.
- Combine both into a graph: static edges define quanta; runtime edges annotated with call style show dynamic coupling.

## Checklist

- [ ] For each service, list bootstrap dependencies (runtime, libraries, data store, broker, platform, required services, UI).
- [ ] Mark every dependency shared by two or more services; decide whether it truly forces joint change or deployment.
- [ ] Check every shared database for its own deploy cadence.
- [ ] Check for a central mediator or tightly coupled UI.
- [ ] Count quanta; compare with the number the team believes it has.
- [ ] Assign operational characteristics per quantum, not per service, when services are fused.

## Pitfalls

- Counting services instead of quanta and claiming independent scaling that a shared database prevents.
- Ignoring databases and UIs because most architecture discussions leave them out.
- Treating a shared broker's presence and messages sent through it as the same kind of coupling.
- Splitting code into services while keeping a shared schema, then expecting independent release cadence.
