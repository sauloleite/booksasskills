# Trade-Off Techniques: Framing the Comparison Correctly

## Contents
- Qualitative versus quantitative analysis
- MECE lists
- The "out of context" trap
- Model relevant domain cases
- Checklist before trusting a comparison

## Qualitative versus quantitative analysis

Almost all useful architecture comparisons are qualitative: they rate how well something behaves (low, medium, high) rather than measure it in units. Two architectures always differ in enough ways that a clean numeric comparison is rarely valid.

How to make qualitative ratings trustworthy:

- Base each rating on many implementations, not one. The book's relative scalability ratings came from looking at many combinations of communication, consistency and coordination and judging scale in each.
- Inside an organization, gather representative examples from existing systems, or run small, local spikes to test a hypothesis, then rate from that evidence.
- Use relative scales (better or worse than the alternatives) rather than absolute claims.
- Treat any numbers attached to qualitative ratings (for example in a weighted worksheet) as a thinking aid, not a measurement.

Guidance for an agent: invest in qualitative reasoning. Do not wait for hard numbers that architecture rarely supplies, and do not dress up opinions as precise metrics. Where a concern can be tested objectively (latency under load, failover time), do test it; that is how analysis moves toward engineering.

## MECE lists

Before comparing anything, check that the candidates form a MECE set: Mutually Exclusive, Collectively (the book says "Combinatorially") Exhaustive. The idea is borrowed from technology strategy consulting.

- **Mutually exclusive:** candidates must be the same kind of thing with no overlapping scope. Comparing a lightweight queue with a full integration platform that bundles a queue plus routing, transformation and orchestration is invalid. Fix it by narrowing: compare only the platform's messaging capability against the queue.
- **Exhaustive:** the set must cover the decision space without obvious gaps. A shortlist of high-throughput messaging options that leaves out a log-based streaming platform is incomplete.

Why exhaustiveness matters for long-lived decisions: the tool landscape changes constantly. Before locking in something that will last years, deliberately search for capabilities that appeared recently and might change the criteria.

Practical MECE check:
1. Write one sentence describing the category being decided (for example, "durable point-to-point message transport").
2. Strike any candidate that is mostly something else, or reduce it to the slice that fits the category.
3. Ask a peer or search for "what else does this job today?" and add missing categories.
4. Confirm each criterion applies to every candidate.

## The "out of context" trap

A generic matrix can favor one option overall and still lead to the wrong choice, because the deciding factor in this specific situation is missing or underweighted. Balance the trade-offs that matter here, not every trade-off that exists. An option with many generic strengths can fail on one critical capability.

Invented example: shared library versus shared service for currency-conversion logic.

- Generic research plus a few internal experiments favor the library on most rows: lower latency, no network failure mode, simpler operations, easier local testing.
- Then the context arrives: the consuming services are written in four languages, and the conversion rules change weekly because of regulatory updates. A library would need four implementations and a coordinated redeploy of every consumer each week. The service now wins despite losing most generic rows.

Two lessons follow:

1. **The right narrow context shrinks the option space.** Once the context is pinned, most options fall away and the decision becomes simple. This is a concrete way to achieve "keep designs simple": think about fewer things by deciding in the right context.
2. **Iterate to find the context.** Sketch a few candidate solutions, then ask "what if" questions about each to observe how the dimensions push on one another; that exploration is how the real context of a decision surfaces.

## Model relevant domain cases

Generic forces (for example the granularity integrators and disintegrators) are a start. Real decisions need domain drivers added back, so options can be filtered and the important trade-offs exposed. Do this by modeling a few likely business scenarios against each option, escalating from simple to complex.

The book illustrates this with one payment service versus one service per payment type. Simple scenarios favor separate services; a scenario where one purchase is split across several payment types forces coordination, and the trade-off becomes performance and consistency versus extensibility and agility.

Invented example: one notification service versus one per channel (email, SMS, push).

| Scenario | What it reveals |
|---|---|
| Swap the SMS provider | Separate services isolate the change: better testability, deployability, smaller blast radius. Watch for duplicated templating code copied to avoid a shared dependency, which erodes the benefit. |
| Add a WhatsApp channel | Separate services make extension easy: a new service, no change to existing ones. |
| Send a critical alert with fallback (push, then SMS if unread in 5 minutes, then email) | Now channels must be coordinated. Separate services need an orchestrator, which adds latency and makes "exactly one delivery" harder to guarantee. Skipping the orchestrator does not remove the fallback logic; it just moves it somewhere else. |

Bottom line for stakeholders: is delivery guarantee and speed for multichannel alerts more important (single service), or is the ability to add and change channels independently more important (per-channel services)?

Rule worth remembering: semantic coupling (the inherent coupling in the business workflow) can never be reduced by implementation choices, only increased. If the domain requires coordinated steps, some component must own that coordination.

Escalation pattern for scenario modeling:
1. A change confined to one variant.
2. Adding a new variant.
3. A workflow that combines several variants or crosses several services.
4. A failure in the middle of that workflow.

The hard parts usually appear at steps 3 and 4.

## Checklist before trusting a comparison

- Are candidates MECE for the stated category?
- Were ratings formed from several examples or spikes, not one anecdote?
- Has the specific context (languages, change rate, regulation, team topology, load profile) been written down and applied?
- Were at least three domain scenarios modeled, including a complex multi-step one?
- Is the semantic coupling of the workflow identified, so no option claims to eliminate it?
