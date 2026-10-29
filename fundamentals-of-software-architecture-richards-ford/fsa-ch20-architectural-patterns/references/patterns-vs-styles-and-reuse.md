# Patterns vs Styles, and Reuse of Operational Concerns

## Contents
- Vocabulary: style, pattern, solution, "best practice"
- Problem: domain coupling vs operational coupling
- Orthogonal coupling
- Hexagonal (Ports and Adapters): what it gets right and wrong
- Sidecar and Service Mesh
- Decision checklist
- Worked example
- Pitfalls
- Review questions

## Vocabulary: style, pattern, solution, "best practice"

| Term | What it is | How to use it |
|---|---|---|
| Architecture style | A named overall topology, told apart by its physical shape, deployment model, communication approach and data layout | Choose once per system (or per subsystem) |
| Architecture pattern | A reusable answer to a recurring problem, valid only within a context (the idea descends from the Gang of Four tradition) | Apply within or across styles; many patterns can coexist in one style |
| Solution / implementation | A concrete tool, framework or library that embodies one or more patterns, sometimes faithfully, sometimes mixed with other patterns | Pick after the pattern is settled |
| "Best practice" | A label implying you must always apply a practice whenever a situation appears | Treat as a warning sign: it suppresses trade-off thinking |

Agent rules:
- When a user names a product ("let's use Istio", "let's use Kafka"), back up and ask which pattern it is meant to deliver. Then check whether that pattern fits, and only then whether the product is a good carrier for it.
- When a user calls something a best practice, reframe it as a pattern with a context, and list the situations where it would be the wrong call.
- Patterns often already exist in a design without being named. Naming them makes their known trade-offs visible.

## Problem: domain coupling vs operational coupling

Distributed architectures, microservices in particular, aim for strong decoupling. The chapter cites the common slogan that duplicating something beats coupling to it.

Domain side (favor duplication):
- When two services exchange the same business concept (say, a customer profile) but bounded contexts must keep internals private, each service keeps its own internal model and they exchange loosely structured data (for example JSON key/value payloads).
- Benefit: each service can change its representation or even its technology stack without breaking the contract.
- Cost accepted: duplicated code, synchronization effort, gradual semantic divergence. These are judged less harmful than coupling.

Operational side (favor consistency):
- Every service needs the same plumbing: monitoring, logging, authentication and authorization, circuit breakers.
- If each team implements these on its own, you lose (a) any reliable way for operations to verify that every service actually complies, and (b) any practical way to roll out an organization-wide upgrade of the chosen tool.
- So here, high coupling to a shared, consistent capability is desirable.

The architectural problem: keep domain logic decoupled while making operational capabilities uniform and centrally upgradable. The pattern answering it is "separate operational concerns from domain concerns". Hexagonal and Service Mesh are two ways to implement that pattern.

## Orthogonal coupling

Two parts of a system are orthogonally coupled when they serve independent purposes yet must meet to form a working whole. Monitoring and a checkout workflow are the canonical pair: neither depends on the other's logic, but a production service needs both.

Why it matters:
- The system's primary hierarchy (for microservices, domain partitioning) cannot accommodate a concern that cuts across every domain.
- An orthogonal reuse pattern provides a separate, consistent layer for that concern, threaded through the architecture without disturbing the domain hierarchy.
- The design goal is to find the meeting points between the two concerns that create the least entanglement.

Other examples to recognize: tenant isolation, audit trails, rate limiting, encryption at rest and in transit, feature-flag evaluation.

## Hexagonal (Ports and Adapters): what it gets right and wrong

Shape: domain logic sits in the core; ports and adapters connect it to everything outside (UI, other systems, persistence). Alistair Cockburn named it; the "hexagon" has no meaning in the number of sides, and "Ports and Adapters" is the more descriptive name.

What it gets right: a clean boundary between core business behavior and external technical concerns.

Where it misleads in microservices: it treats the database as just another pluggable adapter, reflecting an older belief that persistence is separate machinery. Domain-Driven Design (Eric Evans) corrected this: the schema encodes business rules and has to evolve with them, wherever it physically lives. A microservice owns its data as part of its bounded context, so isolating data behind an adapter as if it were interchangeable conflicts with that principle.

Agent rules:
- If someone says "hexagonal", ask whether they mean the general idea (domain vs operational separation) or the literal structure (data as an outside adapter). The first is acceptable shorthand; the second needs pushback in a microservices context.
- For modern distributed systems, recommend Sidecar plus Service Mesh as the implementation of the separation pattern. Hexagonal remains a reasonable general-purpose structure inside a single deployable.

## Sidecar and Service Mesh

- Sidecar: a co-deployed companion process that carries operational capabilities (telemetry, security, resilience) alongside each domain service, so the service code stays focused on the domain.
- Service Mesh: the connected fabric of all sidecars, which gives a uniform control point for operational policy across services.
- Together they are an orthogonal reuse pattern: they solve one specific kind of coupling, not coupling in general.

Qualitative trade-offs:

Strengths
- A uniform, isolated way to attach cross-cutting capabilities.
- Coordinated infrastructure changes (one upgrade path for the whole estate).
- Flexible ownership: a central platform team, the individual service teams, or a mix.

Weaknesses
- You need a sidecar implementation for each platform or runtime you support.
- The sidecar tends to accrete features until it becomes heavy and complex.
- When several teams own pieces of it independently, their versions diverge.

Mitigations to propose: limit the platforms supported; set a scope charter for what belongs in the sidecar; assign a single owner for the sidecar's core with an explicit extension mechanism; automate compliance checks (for example, a deployment gate that rejects services without the current sidecar version).

## Decision checklist

1. Is the concern domain behavior or operational plumbing? Domain: decouple and allow duplication. Operational: standardize.
2. Does the concern cut across the primary partitioning? If yes, treat it as orthogonal and look for a cross-cutting layer.
3. Is the system a single deployable or distributed? Single deployable: a Ports and Adapters structure in code is adequate. Distributed: prefer Sidecar plus Service Mesh.
4. How many runtimes are in play? Each one multiplies sidecar work.
5. Who owns the sidecar, and how will drift be detected?
6. How will an organization-wide upgrade of the operational tool be executed and verified?

## Worked example

A fintech runs 40 services in three languages. Each team bolted on its own logging agent and auth middleware; an audit asks for proof that every service enforces token validation, and nobody can produce it quickly.

Analysis: authentication and logging are orthogonal to the lending, payments and onboarding domains. Pattern: separate operational from domain concerns. Implementation candidates: shared libraries per language (still per-team integration, three codebases, drift likely) vs sidecar plus mesh (one policy point, but three runtimes to validate and a sidecar that may grow). Recommendation: mesh for authN/authZ and telemetry, platform team owns the sidecar, deployment gate rejects services lacking it, domain models stay duplicated per service. Revisit if the language count grows or the sidecar's resource overhead becomes material.

## Pitfalls

- Choosing a mesh product before agreeing on the separation pattern it should deliver.
- Extending "duplication over coupling" to operational concerns, which recreates the chaos the pattern avoids.
- Literal Hexagonal in microservices: hiding the database behind a generic adapter as if schemas were domain-neutral.
- Letting the sidecar absorb business rules; it should carry only operational capabilities.

## Review questions

- Which concerns in your system are orthogonal to the domain partitioning, and how is each reused today?
- If the monitoring vendor changed tomorrow, how many teams would need to ship code?
- When a colleague says "hexagonal", which of the two meanings do they intend?
