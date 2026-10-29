# Style Fit: Strengths, Weaknesses, When to Use and When Not

## Contents
- Qualitative characteristics profile
- The size-decay dynamic
- When to choose it
- How to build it so you can leave it later
- When to avoid it
- Layering outside application design
- Worked examples
- Review questions

## Qualitative characteristics profile

Describe the style this way (own summary; no scores):

Strong
- Cost and simplicity. A monolith with familiar layers is cheap to build and maintain and easy to understand. These strengths shrink as the codebase grows.

Middling
- Responsiveness. Careful design, caching and multithreading can make it fast, but it lacks built-in parallelism, and closed layers plus sinkhole requests add overhead.
- Testability. Weak overall, though mocking or stubbing a component or an entire layer softens the pain.

Weak
- Deployability. Every change ships the whole unit. A tiny edit drags along whatever else changed in config, database scripts or code, and is usually batched with many other changes, so releases are risky, rare and ceremonious.
- Testability (the release side). Few developers run a full regression suite for a three-line change, assuming such a suite even exists.
- Elasticity and scalability. One deployment unit, no architectural modularity, and an architecture quantum of exactly one (single UI, single database, shared backend). Scaling individual functions inside a monolith needs intricate techniques such as internal messaging and multithreading that this style does not support well, so there is a hard ceiling.
- Fault tolerance and availability (see the operations reference).
- Agility and evolvability, because domains cut across every layer.

## The size-decay dynamic

The engineering characteristics (maintainability, testability, deployability, agility) start out acceptable and erode as the codebase grows. The cost and simplicity advantages fade too. When advising, always ask how big the system is now and how big it is expected to become; the same style can be the right answer at 20k lines and the wrong one at 2M.

## When to choose it

Recommend layering when one or more hold:
- The application or website is small and simple.
- Budget and schedule are very tight.
- Feasibility is the dominant characteristic: the question is whether the scope can ship at all with the people and time available (for example, an investor-funded startup racing to a first release, accepting that parts will be rewritten).
- The architecture is still uncertain and development must start anyway; layering is a low-commitment starting point.
- The team's familiarity matters more than advanced characteristics.

## How to build it so you can leave it later

If layering is chosen as a starting point, protect future migration:
- Keep code reuse low; shared utility webs become coupling that blocks extraction.
- Keep inheritance hierarchies shallow; deep trees bind modules together.
- Within each layer, group code by domain (for example, `business/orders`, `business/billing`) so domain seams exist when you later move toward a modular monolith or services.
- Keep layer access rules enforced from day one so dependencies stay predictable.

## When to avoid it

Steer away when:
- The system is, or will become, large; maintainability, agility, testability and deployability degrade with growth, and more modular styles serve better.
- Independent scaling, elasticity or high fault tolerance are top-ranked characteristics.
- Frequent, low-risk, independent deployments are required.
- The organization wants domain-aligned ownership and DDD bounded contexts.
- Profiling shows most requests are pass-through sinkholes.

## Layering outside application design

The same separation-of-concerns reasoning appears in:
- Operating systems: hardware, kernel (hardware abstraction, memory, scheduling), system call interface, user-space applications.
- Networking: the OSI reference model and the TCP/IP stack, with layers from physical transmission through data link (framing, error detection), network (routing, IP), transport (reliable delivery, TCP) up to application protocols such as HTTP, SMTP and FTP.

Use these as explanatory analogies: each layer serves the one above and depends only on the one below, which is the closed-layer idea in practice. Any system that prizes separation of concerns, maintainability and independent work per layer can benefit.

## Worked examples

1. Two founders, three contractors, a demo in ten weeks. Recommend layered: feasibility dominates. Record in the ADR that scalability is deliberately deferred, and add the migration-friendly practices above.
2. A ticketing platform expecting flash-sale spikes of 50x. Advise against layered: elasticity and per-function scaling are primary, and the single quantum cannot meet them.
3. A 12-year-old layered insurance system with 40 developers, monthly releases, 20-minute restarts. Diagnose size decay: deployability and MTTR are the pain. Suggest measuring sinkhole share and restart downtime, then planning extraction along domain seams.

## Review questions (own)

- Which layers on the main request path are closed, and is the reason for each open layer written down?
- What share of request types are pass-through, and is it trending up?
- How long does a restart take, and how does that compare with the availability budget?
- Which top-three characteristics drove the choice, and do any of them clash with a single-quantum monolith?
- If the system doubled in size, which characteristic would fail first?
