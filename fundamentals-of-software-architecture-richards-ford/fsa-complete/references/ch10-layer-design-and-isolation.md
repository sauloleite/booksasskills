# Layer Design, Open/Closed Layers and the Sinkhole Check

## Contents
- Logical topology: what the layers are
- Physical topology: three deployment variants
- Separation of concerns and technical partitioning
- Closed vs open layers and layers of isolation
- Adding a layer to enforce a restriction
- Documenting the access map
- Architecture Sinkhole antipattern and the 80/20 check
- Pitfalls
- Worked example
- Glossary

## Logical topology: what the layers are

A layered system arranges components into horizontal bands, each with one technical job. The book places no hard limit on how many bands there must be, but the usual default is four, top to bottom:

1. Presentation (UI, browser or client communication)
2. Business (rules, calculations, aggregation for a request)
3. Persistence (mapping between objects and stored data, query execution)
4. Database (the actual store or filesystem)

Common variations to recognize in a client's design:
- Business and Persistence merged, typically when SQL lives directly inside business components.
- Three layers for small apps; five or more for large, complex business systems (extra bands such as Rules or Services).

Each layer is an abstraction over one slice of the work a request needs. The Presentation layer formats and shows customer data without knowing where it came from; the Business layer computes on data it obtains from Persistence without caring how it will be rendered.

## Physical topology: three deployment variants

Logical layering says nothing on its own about how many deployables exist. Map the client's system to one of these:

| Variant | Deployables | Typical fit |
|---|---|---|
| A | Presentation + Business + Persistence in one unit; database external | Classic monolithic web app |
| B | Presentation alone; Business + Persistence together; database external | Separate UI tier (SPA, thick client) talking to a backend |
| C | All four layers, database included, in one unit | Mobile apps or small tools with an embedded or in-memory DB; many on-prem shrink-wrapped products |

Variant choice affects network hops and where the cloud can help (see the operations reference), but not the architecture quantum: the system still deploys and fails as one quantum.

## Separation of concerns and technical partitioning

Strength: people can specialize. UI developers stay in Presentation, data engineers in Persistence, and each component's scope is narrow. Role and responsibility models are easy to define.

Cost: the whole system responds slowly to change. Layering is technically partitioned (by role such as presentation or persistence), not domain partitioned (by business area such as customer or order). So one domain concept is smeared across every layer. A change to "customer" touches the customer screens, customer rules, customer services and customer tables. Consequence the agent should state plainly: domain-driven design and bounded contexts sit awkwardly in this style; if the client is committed to DDD, lean toward a domain-partitioned style.

## Closed vs open layers and layers of isolation

- Closed layer: a request travelling downward must pass through it; callers above may not skip it.
- Open layer: callers above may bypass it and go to the next layer down.

Skipping layers looks attractive for simple reads (the historical Fast-Lane Reader idea of letting the UI query the database directly). The decision hinges on layers of isolation: a change inside one layer should not ripple into others as long as the contracts between layers hold, and each layer knows little about the internals of the others.

Rule: every layer on the main request path must be closed if you want isolation. If Presentation reaches Persistence directly, a Persistence change now breaks both Business and Presentation, and the codebase drifts toward tight, brittle coupling that is costly to change.

Payoff of isolation: a whole layer can be swapped (for example, moving to a new UI framework entirely within Presentation) without disturbing the rest, provided contracts are well defined. The Business Delegate pattern helps here: an adapter on the presentation side that hides how business services are located and invoked, so the UI depends on the delegate, not on business internals.

## Adding a layer to enforce a restriction

Scenario: the Business layer holds shared utilities (date and string helpers, auditing, logging). You decide the UI must not use them. As long as they live inside Business, Presentation can legally reach them, so the rule depends on discipline and is hard to govern.

Fix: move the shared objects into a new Services layer below Business. Because Business is closed, Presentation can no longer reach Services. Mark Services open, otherwise Business would be forced to route every persistence call through Services. With Services open, Business may use it or skip straight to Persistence.

General technique: when an access rule is hard to enforce, change the structure so the rule falls out of the open/closed topology, then choose the new layer's openness so it does not force needless pass-throughs.

## Documenting the access map

Open/closed status is a design decision that must be written down and communicated, including the reason for each open layer. When teams do not know which layers may be skipped, the system ends up tightly coupled, brittle, hard to test, hard to maintain and hard to deploy. Record it in an ADR and enforce it with a fitness function (see the operations and governance reference).

## Architecture Sinkhole antipattern and the 80/20 check

A sinkhole request flows down and back up the stack with no layer adding value: no aggregation, calculation, rule or transformation, just handoffs to a plain query. Each hop still instantiates objects and does work, wasting memory and CPU.

Some sinkholes are unavoidable in any layered system. Measure the share of request types that behave this way:

- Around 20% or less: acceptable, normal for the style.
- Around 80% or more: strong signal that layering is the wrong style for this problem.
- In between: judgment call; look at whether the pass-through share is growing and whether the expensive paths are the sinkholes.

Remedies, in order of preference:
1. If the share is high, reconsider the style rather than patching.
2. Selectively open specific layers for the pass-through paths, documenting each.
3. Open all layers. This removes the waste but surrenders isolation, so change becomes harder to manage.

`scripts/layer_rules_check.py` computes the share and applies these bands.

## Pitfalls

- Treating "we just started coding" as a design. Unplanned systems tend to become layered by default (the Architecture by Implication and Accidental Architecture antipatterns). Make the choice explicit.
- Opening a layer for convenience in one feature, undocumented, then discovering many components now depend on it.
- Adding layers without deciding their openness, which either creates new sinkholes or silently breaks isolation.
- Assuming logical layers imply separate deployables (or vice versa).

## Worked example

An internal HR portal has Presentation, Business, Rules, Persistence and Database layers, all closed. Profiling 60 request types finds 41 that only fetch and display records. 41/60 is about 68%, well above the comfortable 20% band and approaching 80%. Options to present: (a) open Rules and Business for read-only lookups, recorded in an ADR and encoded in the dependency rules; (b) if most features are plain CRUD, question whether elaborate layering is worth it at all and simplify to three layers. Note that option (a) trades some isolation for performance and less boilerplate.

## Glossary

- Layers of isolation: property where changes stay inside one layer while inter-layer contracts are stable.
- Business Delegate: presentation-side adapter that hides business-service lookup and invocation.
- Fast-Lane Reader: older term for letting a top layer read data directly, bypassing middle layers.
- Architecture Sinkhole: request that passes through layers with no processing.
