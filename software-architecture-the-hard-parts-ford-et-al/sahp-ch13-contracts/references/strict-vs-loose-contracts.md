# Strict versus Loose Contracts

## Contents
- Broad definition of a contract
- The strictness spectrum
- What strict contracts give and cost
- What loose contracts give and cost
- Need-to-know contracts and GraphQL/REST
- Choosing strictness per edge (checklist)
- Worked example: one workflow, mixed strictness
- Versioning policy checklist
- Pitfalls
- Glossary

## Broad definition of a contract

Treat as a contract anything one part of a system relies on to get information or behavior from another: remote APIs, event and message schemas, shared libraries and their transitive dependencies, internal and external integration points, and caches that several parts read. Contract strictness is a cross-cutting force: it does not sit on the communication, consistency or coordination axis but influences all three, and it affects static coupling (what must be deployed together) and dynamic coupling (what must agree at runtime).

Order of decisions: first choose the contract type (how tight), then let teams pick the protocol, and verify the outcome with fitness functions. "Use gRPC everywhere because it is fast" is an implementation choice masquerading as an architecture decision.

## The strictness spectrum

From strict to loose, with what makes each one strict or loose:

| Format | Why it sits there |
|---|---|
| Platform remote method call (Java RMI and similar) | Mirrors a local call exactly: name, parameter order, types, everything |
| RPC frameworks (gRPC, XML-RPC, SOAP) | Generated stubs and typed messages; gRPC defaults to strict |
| JSON with JSON Schema | Loose syntax with an optional overlay of types, required keys and constraints |
| REST resources | Consumers bind to resources, not procedures; additive changes rarely break readers |
| GraphQL | Each consumer declares the fields it wants from an aggregated read model |
| Name/value maps (plain JSON, YAML) | Raw facts only, no type or presence guarantees |

Strict formats tend to imitate method-call semantics, which is why developers find them comfortable. That comfort hides brittleness: the integration inherits the fragility of a shared signature.

## What strict contracts give and cost

Strengths:
- **Fidelity is guaranteed.** Schema validation enforces names, types and governed metadata; some domains (payments, regulated reporting) want change to be forced to coordinate.
- **Build-time checking.** Schema tooling and code generation catch mismatches before deployment, giving integration points something like type checking.
- **Self-documenting.** Typed parameters leave nothing to interpretation.
- **Explicit versions.** Versioning lets a provider serve several consumer generations and evolve its domain gradually.

Weaknesses:
- **Lockstep change.** When the shared contract changes, both sides must change, which is tight coupling by definition.
- **Versioning cuts both ways.** The same versions that enable precision become an integration burden when nobody retires old ones or too many are kept alive.

## What loose contracts give and cost

Strengths:
- **Least coupling.** Each side keeps its own model and stack; name/value pairs are readable by every mainstream platform, making them the common language of integration.
- **Easy evolution.** With little or no schema, implementation details move freely.

Weaknesses:
- **No built-in contract management.** Misspelled keys, absent pairs and wrong value types surface only at runtime.
- **Governance must be added.** Teams need fitness functions, typically consumer-driven contract tests, to prove each loose contract still carries what consumers need. See also consumer-driven-contracts.md.

Remember the limit: loosening the format reduces implementation coupling only. If the meaning of a field changes (for example, "amount" switches from gross to net), every consumer that depends on that meaning still has to be coordinated.

## Need-to-know contracts and GraphQL/REST

REST models resources rather than procedures, so adding new attributes to a resource does not break consumers that read older ones. Invented example: a `Vehicle` resource used by a dealership app to list colors keeps working when a team later adds battery telemetry.

GraphQL is commonly used as a read-only aggregation layer so that a consumer does not have to orchestrate calls to many services. Its real value for contracts is per-consumer shape: a recommendations service can ask a `Customer` type only for `displayName`, while a billing service asks for addresses and tax IDs. Same concept, two different minimal contracts.

The anti-pattern: binding a consumer to a provider's full structure on the theory that it may need the rest someday. The consumer then breaks, and teams must coordinate, whenever an attribute it never reads changes. Size each contract to what the consumer actually uses today; this keeps the necessary semantic coupling while dropping needless fragility.

## Choosing strictness per edge (checklist)

Lean strict when:
- The two sides are semantically entangled and their data changes together (adding a new item type means the partner must also understand it).
- Correctness errors are expensive or regulated, and build-time detection matters.
- There are few consumers and the provider can coordinate releases with them.

Lean loose when:
- The partner is peripheral or its data changes slowly (notifications, surveys, analytics feeds).
- Either side cannot redeploy quickly: app-store mobile clients, partner integrations, embedded devices. A loose contract plus a deliberate extension slot (for example a generic `attributes` map) lets you add data without a client release.
- Many consumers with different needs share one provider.
- Teams want independent technology choices.

Whenever loose: budget extra validation logic on both ends and add CDC tests.

## Worked example: one workflow, mixed strictness

An insurance claims orchestrator talks to five collaborators:
- **Claim Intake and Claim Adjudication:** strict (typed schema, versioned). A new claim category must be understood by adjudication immediately, so the data is coupled anyway; strictness makes the coupling visible and checked at build time.
- **Payment service:** strict, because payout amounts and currency codes demand fidelity and audit.
- **Customer notification and satisfaction survey:** loose name/value messages; their data rarely changes and they gain nothing from brittle coupling.
- **Field adjuster mobile app:** semantically it deserves the same strictness as adjudication, but releases pass through public app stores with unpredictable review delays. Choose a loose contract with an extension map, put validation in both orchestrator and app, and record a revisit trigger if the app moves to over-the-air updates.

The lesson: strictness is decided per edge from semantic coupling, change rate and deploy agility, not once for the whole system.

## Versioning policy checklist (for every strict contract)

- Maximum number of concurrently supported versions (two is a common ceiling).
- Deprecation notice period and how consumers are told.
- Telemetry that shows which consumers still call each version.
- Additive-only rule for minor versions; breaking changes require a new major version.
- An owner who retires old versions on schedule.

## Pitfalls

- Choosing strict contracts because they feel like local method calls.
- Defaulting to one protocol for all edges and calling it architecture.
- Loose contracts without any verification, discovered broken in production.
- Unbounded version proliferation.
- Over-specified "future-proof" contracts.

## Glossary

- **Contract fidelity:** confidence that the data sent matches what the receiver expects in names, types and presence.
- **Semantic coupling:** dependency on shared meaning; it can be moved but not eliminated by implementation choices.
- **Extension mechanism:** a sanctioned place in a contract for temporary, unversioned additions.
