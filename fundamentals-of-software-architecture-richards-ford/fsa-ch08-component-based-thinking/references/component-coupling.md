# Component Coupling and the Law of Demeter

## Contents
- What counts as coupling
- Static coupling: afferent and efferent
- Temporal coupling
- Law of Demeter (Principle of Least Knowledge)
- Worked example: knowledge redistribution
- Reading coupling numbers
- Pitfalls
- Review questions

## What counts as coupling

Two components are coupled if they communicate, **or** if changing one may force a change in the other. The second clause matters: components can be coupled without any direct call between them. More coupling makes the system harder to maintain and test, so track it deliberately.

Benefits of loose coupling: easier maintenance and testing, lower deployment risk, and higher overall reliability because a change touches fewer components and creates fewer chances for error.

## Static coupling: afferent and efferent

In this chapter, static coupling refers to components that call each other synchronously. Measure two directions:

| Term | Also called | Meaning | Count |
|---|---|---|---|
| Afferent coupling, **Ca** | incoming, fan-in | How many other components depend on this one | Number of distinct incoming dependencies |
| Efferent coupling, **Ce** | outgoing, fan-out | How many other components this one depends on | Number of distinct outgoing dependencies |

Example: if Checkout and Returns both call Customer Messaging, then Customer Messaging has Ca = 2. If Checkout calls Fulfillment only, Checkout has Ce = 1.

Interpretation for an agent:
- High Ca: many dependents. Changes are risky and should be backward compatible; this component deserves stability, strong tests, and careful contracts. Typical for shared services such as notification.
- High Ce: depends on many others. It breaks when any of them changes and often signals a component that "knows too much" (see Law of Demeter below).
- Count distinct components, not calls. Ignore dependencies inside one component.

The bundled script `scripts/component_coupling.py` computes Ca and Ce from a dependency list (component level, or class files mapped to their leaf directory).

## Temporal coupling

Temporal coupling is a non-static dependency based on timing or on a shared transaction (single unit of work). Example: shipping logic may only run after order placement logic has run, so they are temporally coupled even if neither imports the other.

Why it is dangerous: current tooling largely cannot detect it. It is usually discovered from design documents or, worse, from failures in production.

Agent practice:
- Ask explicitly: "Which operations must happen before or after this, or inside the same transaction?"
- Write those ordering and transactional constraints down (design notes, ADRs, sequence diagrams) because static analysis will not reveal them.
- Treat a temporal dependency like a real coupling edge when judging change impact.

## Law of Demeter (Principle of Least Knowledge)

Idea: a component or service should know as little as possible about other components or services. Named after the harvest goddess who supplied grain without knowing what anyone did with it.

The crucial insight: coupling comes from **knowledge**, not only from responsibility. A component that merely tells others what to do still couples itself to them because it knows those things must happen.

How to apply:
1. For a highly coupled component, list every downstream thing it "knows must happen".
2. For each item, ask: is this knowledge intrinsic to my job, or a consequence of some other component's job?
3. Keep edges that are intrinsic. If inserting a go-between would leave the component's outgoing count unchanged, the edge stays as is.
4. Move consequential knowledge to the component whose state triggers it.

Important caveat: applying the law **does not necessarily lower total coupling in the system**. It usually moves coupling to another component. Use it to put knowledge where it naturally belongs and to protect components that change often, not as a way to make coupling disappear.

## Worked example: knowledge redistribution

Before (invented library system): `Loan Checkout` records a loan and then, itself, (a) tells `Copy Availability` to mark the copy as out, (b) if no copies remain, tells `Hold Queue` to promote the next reservation, (c) if no copies remain, tells `Acquisitions` to flag the title for purchase, and (d) tells `Patron Messaging` to send a receipt.

Loan Checkout Ce = 4. It knows the rules about stock running out, which are not about checkout.

Analysis:
- (a) is intrinsic: checkout must update availability. Putting something between them would not reduce Checkout's outgoing count, so keep it.
- (b) and (c) are consequences of availability reaching zero. Move that knowledge into `Copy Availability`.
- (d) is intrinsic to the checkout experience (receipt). Keep.

After: Loan Checkout Ce = 2 (Copy Availability, Patron Messaging). Copy Availability Ce rises from 0 to 2 (Hold Queue, Acquisitions). Total edges are unchanged at 4, but each component now holds only knowledge it owns.

## Reading coupling numbers

There are no universal thresholds in the chapter. Use relative judgment:
- Compare components with one another; outliers deserve a look.
- A high-Ce component whose outgoing edges are "if X then also do Y" rules is a Demeter candidate.
- A high-Ca component should be stable and well-tested rather than split by reflex.
- Re-measure after each restructuring pass; Demeter refactors should show Ce moving, not vanishing.

## Pitfalls

- Counting only direct calls and missing change-impact or temporal coupling.
- Claiming a refactor "reduced coupling" when it only moved it.
- Adding intermediary components that do not change the caller's outgoing count.
- Relying on dependency tools to find ordering or transactional dependencies.

## Review questions

1. Why can two components with no calls between them still be coupled?
2. What evidence would you gather to discover temporal coupling in a legacy system?
3. After a Demeter refactor, total edge count is unchanged. Was the change worthwhile? On what grounds?
