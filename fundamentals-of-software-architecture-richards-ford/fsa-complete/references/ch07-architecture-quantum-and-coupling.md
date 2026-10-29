# Architecture quantum and the four kinds of coupling

## Contents
- Why scope needs its own measure
- What an architecture quantum is
- Testing a candidate quantum
- Coupling vocabulary
- Coupling tolerance and brittleness
- Worked examples
- Pitfalls
- Glossary

## Why scope needs its own measure

Code-level structural metrics (afferent/efferent coupling, cyclomatic complexity, abstractness and similar) describe the inside of a code base. They are blind to dependencies that live outside it, and those dependencies (above all the database) decide most operational characteristics. A service can be engineered for elasticity and low latency, yet if it sits on a database that cannot scale or respond at that level, the effort is wasted. The authors introduced the architecture quantum, originally while measuring structural evolvability for their evolutionary-architecture work, to capture this missing dimension: the boundary within which one set of characteristics applies.

Practical consequence for an agent: never evaluate a component's performance, scalability, elasticity or availability in isolation from the data stores and runtime dependencies it cannot function without.

## What an architecture quantum is

Informally, the smallest piece of the system that can run on its own, carrying its data and other dependencies with it. The word derives from the Latin for how much, and in everyday use suggests a small indivisible thing. Plural: quanta.

Formally, a quantum marks out the scope for a set of characteristics (especially operational ones) and has four traits:

| Trait | What it means in practice |
|---|---|
| Independently deployable | Contains every piece it needs to run, data store included |
| High functional cohesion | Serves one coherent purpose, typically one workflow or bounded context |
| Low external implementation static coupling | Its wiring to other quanta is minimal; no shared databases or shared libraries across the line |
| Communicates with other quanta | Calls across the boundary are dynamic coupling; synchronous ones can bind quanta together at runtime |

Quanta sit one abstraction level above components and frequently, but not always, line up with service boundaries. Because a quantum is independently deployable and cohesive, counting and shaping quanta is a good proxy for how modular an architecture really is.

### Consequences that follow directly
- A legacy application (or a "distributed" set of services) that relies on one shared database is a single quantum. Splitting code without splitting data does not create new scopes.
- Microservices, where each service owns its data inside its bounded context, typically yield one quantum per service, so each service can have its own characteristics.
- In a single-database monolith, functional cohesion is not a useful discriminator because the whole system is the cohesive unit. Cohesion becomes decisive in distributed styles where services are designed around single workflows.

### Bounded context in one paragraph
Domain-driven design (Evans) partitions a large domain into bounded contexts: inside, every concept is visible and consistent; outside, it is hidden. Before this idea took hold, organizations tried to reuse one enterprise-wide entity (for example a single Customer class), which produced tight coupling, heavy coordination and complexity. Bounded contexts accept duplication instead: each context models its own version of the entity and translates at integration points. The quantum's demand for cohesion and low coupling between quanta inherits directly from this philosophy.

## Testing a candidate quantum

Ask, in order:
1. If every other part of the system were down, could this part still run and serve its purpose? If not, what does it need? Those needs belong inside the boundary.
2. Does it own its data store, or does it share one? Sharing pulls the sharers into one quantum.
3. Does it share a library, component or schema with others such that a change there could break them? Same verdict.
4. Is its purpose singular (one workflow or bounded context), or is it a grab bag?
5. Which of its calls to other parts are synchronous? Those can fuse it with the callee at runtime (see the communication reference).

## Coupling vocabulary

A simple working definition: two things are coupled when a change to one can break the other.

- **Semantic coupling**: the coupling inherent in the problem itself. An order system will always relate orders, inventory, catalog, carts, customers and sales. No pattern stops a change in the domain from rippling through the system, because it is a change in requirements; architects can only adapt.
- **Implementation coupling**: the coupling created by how the team chooses to build it. One database or several? Monolith or distributed? These choices barely touch semantic coupling but dominate architectural outcomes.
- **Static coupling**: the wiring. Services that depend on the same coupling point (a shared component, a shared relational database) are in the same quantum. Static coupling defines the dependency scope.
- **Dynamic coupling**: the forces at play when running quanta talk to each other to complete workflows. Its trade-offs (sync vs async, consistency, coordination) are treated in depth in the book's chapter on event-driven communication.

## Coupling tolerance and brittleness

Tight coupling is not inherently bad. It is the right choice where cohesion is required, inside a service or a subsystem. It becomes dangerous as its reach grows. An architecture is brittle when one implementation change triggers unexpected breakage in many supposedly unrelated places. The rule to apply: the narrower the scope, the more coupling you may accept; the wider the scope, the looser it must be.

Brittleness signals to look for:
- A contract change (a renamed field, a changed type) requires coordinated releases of several teams.
- A "common" or "shared" module is imported by most services.
- Several services read and write the same tables.
- Nobody can list all consumers of an endpoint or schema.

## Worked examples

**Shared address component.** Services Billing and Delivery both import a shared AddressValidation library, versioned and deployed with each service. Result: one quantum for scoping purposes, because a breaking change in the library can break both. Options: duplicate the small logic in each context, publish it as an independently versioned contract with backward compatibility, or accept the joint quantum and give both services the same characteristics.

**Field rename.** A Profile service renames `zip` to `postalCode`, believing only the web client reads it. Four reporting jobs and a partner integration fail. The service had wide-scope tight coupling hidden behind an apparently private contract. Remedies: consumer inventory, contract versioning, tolerant readers, and treating any cross-quantum contract as published.

**Split code, one database.** A team breaks a monolith into eight services but keeps one shared schema. Scope analysis: still one quantum. Any characteristic (scalability, availability) they want to differ per service is capped by the shared database.

## Pitfalls
- Counting services instead of quanta when claiming independent scalability or deployability.
- Treating a shared database as an implementation detail rather than a scope-defining dependency.
- Hoping an architecture pattern will absorb domain change; it cannot.
- Applying loose-coupling dogma inside a service, where cohesion should win.
- Building enterprise-wide shared entity models that couple every context.

## Glossary
- **Architecture quantum**: independently deployable, functionally cohesive unit (with its data) that bounds one set of characteristics.
- **Quantum of one**: a system whose shared deployment or data makes it a single scope.
- **Brittle architecture**: one where small implementation changes cause distant, unexpected failures.
- **Static vs dynamic coupling**: build-and-deploy wiring vs runtime interaction.
