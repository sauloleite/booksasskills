# Quality Attributes, Stakeholder Alignment and Architectural Styles

## Contents
- Vocabulary and framing
- Which attributes matter depends on the system
- Attributes in tension
- Identifying attributes from requirements text
- Ranking and feedback loop
- Getting stakeholders to value invisible attributes
- Influence through indirection
- Architectural styles and how to choose
- Pitfalls

## Vocabulary and framing

Many labels name the same thing: nonfunctional requirements, architectural characteristics, quality goals, quality-of-service goals, architecturally significant requirements, constraints, the "-ilities". Understanding which of these matter most for the system is among the architect's most important jobs.

Prefer the term **quality attributes** when talking to stakeholders. "Nonfunctional" sounds like overhead and invites business people to tune out and push for features only. "Quality" is something nearly every customer is happy to discuss. Stakeholders focus on what the system must do (and those needs must be met), but someone has to own the properties they are not thinking about.

Common attributes: maintainability, scalability, elasticity, availability, reliability, fault tolerance, performance, security, privacy, usability, deployability, compatibility, simplicity, observability, cost. Simplicity is underrated; push for it.

## Which attributes matter depends on the system

- Device driver or low-level library: performance can outrank maintainability.
- Online store: availability and scalability lead.
- Internal back-office tool: maintainability, security and cost often lead; elasticity rarely matters.

## Attributes in tension

You cannot max every dial. Some pairs move inversely: raising one lowers the other. Security versus usability is the classic case (an air-gapped machine in a locked room with no login is very secure and nearly useless). Others to watch: performance versus maintainability, elasticity versus cost and simplicity, consistency versus availability, observability versus cost.

The task is twofold: find the relevant attributes, then set them in deliberate tension with one another so the trade-offs are explicit. Expect to sell the value of the less visible ones (maintainability, simplicity, deployability).

## Identifying attributes from requirements text

Scan requirements for trigger phrases and translate them:

| Signal in the text | Likely attribute |
|--------------------|------------------|
| "thousands of concurrent users", "bursts", "on-sale moment" | scalability, elasticity |
| "must not lose", "never sell twice", "exactly once" | data integrity, consistency |
| "24x7", "global", "no downtime" | availability, fault tolerance |
| "quiet after the launch" | elasticity (scale down to near zero, cost) |
| "regulated", "personal data", "audit" | security, privacy, auditability |
| "many teams", "frequent releases" | deployability, modularity |

Also look for what is **unstated** but implied by the domain. In the chapter's concert-ticketing kata (huge bursts when sales open, concurrent buying, no seat sold twice, live view of remaining seats), the implied attributes are elasticity, resilience under burst, and strong consistency on seat allocation, plus two unstated concerns: seat holds must not let one user lock up large blocks, and bots must be filtered.

Invented example: a vaccination-appointment portal opening slots for a new age group. Signals: national launch announcement (burst, elasticity), one person per slot (integrity), citizens' health data (privacy, security), many elderly users (usability, accessibility), traffic collapse after the first days (scale down, cost). Unstated: queueing to protect the backend, fraud through scripted booking.

## Ranking and feedback loop

1. Pick the top attributes (a short list; a ranking of fifteen is no ranking).
2. Order them using any light artifact: numbered list, table, or mind map.
3. Share the ranking with interested stakeholders.
4. Incorporate their feedback and iterate until there is agreement.
5. Use the final ranking to weight style and technology comparisons, and convert the top items into fitness functions.

## Getting stakeholders to value invisible attributes

Security is an easy sell; maintainability and simplicity are not. Tactics:
- Explain benefits in the stakeholder's language and with their examples (time to ship the next feature, cost of incidents, audit findings), not in technical jargon. Customers should not have to care about purely technical choices.
- Find common ground and listen to their concerns even when they seem minor; there is usually something useful in them.
- Make sure the conversation actually happens rather than deciding by assumption.
- Identify who is truly influential; it is often not who the org chart suggests. You may not reach the decision maker directly, so work through others.
- Approach peers as equals, rely on the quality of your ideas and your reputation, and use reciprocity (help others, and they help you).

## Influence through indirection

Lesson from the chapter's anecdote about introducing Git: a head-on "replace your tool" pitch triggered hard resistance from the team owning the incumbent tool, even after the architecture group approved it. Reframed by a well-respected ally as an **addition** that solved a collaboration problem (not a replacement), the idea met little resistance, ran as a pilot, and became an enterprise standard within months.

Playbook when a proposal stalls:
- Ask who loses something if this is adopted, and reframe so they do not.
- Present the change as additive or as a pilot rather than a swap.
- Recruit a sponsor with more organizational clout to carry the idea.
- Anchor it on a problem the audience already feels.

## Architectural styles and how to choose

A style is the top-level shape of the codebase plus the way it talks to persistent storage. Choose a style only after the attributes are ranked.

| Family | Deployment | Styles named in the chapter |
|--------|------------|------------------------------|
| Monolithic | one deployable unit | big ball of mud (an anti-pattern), layered, microkernel, pipeline |
| Distributed | many deployable units | space-based, service-oriented, microservices, event-driven |

Key points:
- Monoliths get a bad reputation, but poor modularity is the real culprit, not the single deployment. A disciplined modular monolith is maintainable.
- Distributed systems without discipline and technical-debt management become very hard to evolve.
- Microservices: strong elasticity and scalability; costs include network hops (performance), higher complexity and spend, the need for monitoring and observability, and harder debugging and tracing across services.
- Rule: pick microservices when scalability and elasticity are top-ranked; if they are not, another style likely fits better. What is right for one system is wrong for another.
- For deeper style-by-style ratings, the chapter defers to Richards and Ford's Fundamentals of Software Architecture.

Agent check before recommending a distributed style: Does the ranked list actually demand independent scaling or deployment? Does the team have observability, CI/CD and on-call maturity? Would a modular monolith with clear boundaries meet the top attributes for now?

## Pitfalls
- Listing attributes without ranking or tension; if everything is "high", nothing is.
- Picking a style by fashion or resume value rather than by ranked attributes.
