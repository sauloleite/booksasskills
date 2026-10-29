# Semantic vs Implementation Coupling

## Definitions

- **Semantic coupling**: the coupling that the problem domain itself imposes on a workflow. If the business process says a request must be validated, matched to a qualified person, checked against schedules and locations, then dispatched, those dependencies exist no matter how the software is built.
- **Implementation coupling**: how the architect chooses to realize that workflow: components, layers, services, links, messages.

## Core rule

Implementation can never lower semantic coupling; it can only match it or add to it. The architect's goal is to keep implementation complexity as close as possible to the domain's inherent complexity. This does not forbid challenging the business: requirements that are impractical or nearly impossible to implement should be pushed back on, since some domain rules create disproportionately hard architecture problems.

## Partitioning as the classic illustration

- Technical partitioning (layers such as presentation, business rules, persistence) splits a single domain concept, say "renew subscription", across every layer. The concept is spread thin over the codebase, so changing or following the workflow means touching each layer.
- Domain partitioning (for example a modular monolith or services organized by domain) places "renew subscription" in one component with its own data. The implementation mirrors the workflow, so its complexity is about the same as the domain's.
- When technical layers are imposed, the team pays twice: the semantic complexity of the workflow plus the structural complexity added by the layering.

This echoes a central insight of Domain-Driven Design: domain workflows come first, and architecture should align with them.

## When extra implementation complexity is justified

Added structure is acceptable when a concrete benefit outweighs it. Historically, layered systems were often chosen to consolidate shared technical concerns such as database connection pooling for cost savings; in many cases that cost argument legitimately beat the complexity it introduced. Make such trade-offs explicit and documented rather than accidental.

## Link to coordination choice

- More workflow steps mean more potential error and optional paths, so coordination needs grow with semantic coupling.
- Because the orchestrator's value rises with semantic complexity, a highly complex domain workflow implemented in choreography usually ends up scattering that complexity across services (implementation coupling exceeding the semantic floor).
- Conversely, adding an orchestrator to a trivial, high-volume flow imposes structure the domain does not require.

## Checklist for a design review

1. Write the domain workflow in business terms first, independent of any architecture.
2. Map each workflow step to the component that implements it. Does one step span many components or layers? That is added implementation coupling.
3. For each extra component or layer on the path, name the benefit it buys (cost, reuse, scale, security). No named benefit means it is a candidate for removal.
4. Count error and alternate paths in the domain workflow; use that count to inform the orchestration vs choreography decision.
5. Flag any domain requirement whose implementation cost seems out of proportion and raise it with stakeholders.

## Worked example (invented)

A clinic scheduling workflow: patient requests appointment, system finds a practitioner with the right specialty, checks room and equipment availability, books, and sends reminders. In a layered design, "find practitioner" logic lives partly in controllers, partly in a business service, partly in stored procedures; a change to specialty matching touches three layers and two teams. Reorganized by domain into Matching, Resources, Booking and Reminders components, the same change touches only Matching. The semantic coupling (matching depends on specialties, booking depends on resources) is unchanged; only the avoidable implementation coupling was removed. With six or more failure branches (no specialist, room conflict, equipment out of service, patient cancels, practitioner sick, reminder bounces), an orchestrator for the booking flow is the natural next decision.
