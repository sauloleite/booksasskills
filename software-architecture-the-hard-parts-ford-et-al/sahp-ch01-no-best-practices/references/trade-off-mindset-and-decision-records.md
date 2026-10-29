# Trade-off Mindset and Decision Records

## Contents
- Why there is no "best practice" for hard architecture problems
- The least-worst principle in practice
- The two meanings of "hard"
- Reading an architecture style through its historical constraints
- Why over how: staying on the architecture side
- Architecture Decision Records (ADRs)
- Worked example: a least-worst decision recorded as an ADR
- Pitfalls

## Why there is no "best practice" for hard architecture problems

Developers can usually search their way out of a problem: someone has configured the same tool, hit the same error, and written it up. Architects rarely get that luxury. An architecture question fuses technology with the specific business, organization, politics, legacy and timing of one company, so the exact combination is almost never documented anywhere. Often it is new not just locally but globally.

Consequences for an agent assisting an architect:
- Do not answer an architecture question by retrieving "the best practice" and asserting it. Generic patterns are inputs to the analysis, never the answer.
- Treat each consequential decision as a novel case. Ask for the forces specific to this organization before recommending.
- Remember Brooks's "No Silver Bullet" argument (1986): no single technique delivers an order-of-magnitude gain on its own. Claims that a style or tool removes the trade-offs are a red flag.

The architect's real job is to identify, objectively, what is gained and lost on each side of a decision that matters, and then choose the option whose overall balance best serves the project.

## The least-worst principle in practice

"Best" implies every competing force was maximized at once, which is impossible when forces conflict (for example, consistency versus availability, or independence versus shared data). The book's tongue-in-cheek reframing: seek the least-worst mix of compromises rather than a perfect design. The winning design usually lets no single characteristic shine on its own; it wins because the overall balance supports project success.

How to operationalize it:
1. List the options actually on the table (at least two; "do nothing" is often a valid third).
2. Name the characteristics that matter for this decision, and which ones the business ranks highest.
3. For each option, state qualitatively what it improves and what it damages. Write both sides; an option with no listed downside has not been analyzed.
4. Eliminate options that fail a hard constraint (regulation, budget, a must-have characteristic).
5. Among the survivors, pick the one whose weaknesses fall on the characteristics the business cares least about.
6. Record the choice and the rejected alternatives (see ADRs below), including what you knowingly gave up.

Language to prefer in recommendations: "the least-worst option here is X because its weaknesses (A, B) hit lower-priority concerns, while Y would compromise C, which the business ranked first." Avoid "X is the best practice."

## The two meanings of "hard"

1. **Difficult.** Problems that nobody has solved in this exact form, with long-lived technical consequences layered on top of interpersonal and political dynamics.
2. **Solid, foundational.** By analogy with hardware versus software, the hard parts change least and everything else rests on them. Architecture is the structural layer; design is the part that is cheaper to change. A popular informal definition says architecture is whatever is expensive to change later.

Practical test for whether a question deserves full trade-off treatment: if reversing the decision in a year would require rewriting deployment units, migrating data, or renegotiating contracts between teams, it is architecture and deserves explicit analysis and an ADR. If it can be refactored inside one team's codebase in days, treat it as design.

## Reading an architecture style through its historical constraints

The software ecosystem keeps replacing itself piece by piece, and each new capability unlocks others nobody predicted. So never judge a style by fashion; judge it by the constraints that made it dominant, and check whether those constraints still hold.

Illustration from the chapter (summarized): orchestration-driven service-oriented architecture dominated large enterprises when mergers created integration pain and open source was politically unacceptable, so reuse of shared, centralized resources looked economical. Later, Linux made the operating system free to license, and infrastructure-as-code tools (Puppet, Chef) made environments free to operate because teams could provision them from the build. That operational shift, more than licensing, enabled microservices, containers and orchestrators such as Kubernetes.

Agent checklist when evaluating a legacy or proposed style:
- Which constraints (cost of environments, licensing, org structure, integration needs, team skills) made this style rational?
- Which of those constraints have since changed in this organization?
- If constraints changed, the style may now carry costs that once paid for themselves (for example, heavy sharing and central coordination).
- If constraints have not changed, the "outdated" style may still be the least-worst choice here.

Because tools churn, the durable skill is the reasoning method, not the tool list. Use current technologies as context for examples, but base recommendations on trade-off reasoning that would survive a change of stack.

## Why over how: staying on the architecture side

The authors deliberately stay on the architecture end of the architecture/design spectrum, for three reasons that also apply to an agent:
- An architect must grasp the governing principles before choosing an implementation. Example: synchronous versus asynchronous communication has trade-offs that exist regardless of which broker or protocol is used.
- There are countless implementations of any concept; reasoning at the concept level keeps advice reusable.
- Covering every implementation variant is unbounded.

This echoes the "second law" from the authors' earlier book: why is more important than how. When answering, explain why one option's trade-offs fit better before discussing how to build it. If the user asks only "how", briefly surface the "why" assumptions you are relying on.

## Architecture Decision Records (ADRs)

ADRs, popularized by Michael Nygard and listed as "adopt" on the ThoughtWorks Technology Radar, are short documents (typically one or two pages) that each capture one architecture decision. Format is flexible: plain text, Markdown, AsciiDoc or a wiki template.

The lightweight structure the book uses throughout (all records assumed approved):
- **Title**: a brief noun phrase naming the decision.
- **Context**: one or two sentences on the problem, plus the alternatives that were considered.
- **Decision**: the choice made and a thorough justification.
- **Consequences**: what follows once the decision is applied, including the trade-offs weighed.

Guidance for an agent drafting ADRs:
- Keep the context short; the justification belongs in Decision.
- Always list rejected alternatives in Context. A record without alternatives cannot show a trade-off analysis happened.
- Consequences must include negatives. The least-worst framing means something was sacrificed; say what.
- One decision per record. Split compound decisions.
- Documenting a decision is not the same as enforcing it. Pair each structural ADR with at least one fitness function where the decision is checkable (see the fitness functions reference).

## Worked example: a least-worst decision recorded as an ADR

Invented scenario: a clinic-scheduling platform must decide whether the Appointment service calls the Billing service synchronously or publishes an event.

```markdown
# ADR: Asynchronous hand-off from Appointment to Billing

## Context
Booking must stay available when Billing is slow or down. Options:
(1) synchronous REST call, (2) publish an "appointment booked" event.

## Decision
Publish an event. Booking availability is the top-ranked characteristic;
billing can lag by minutes without business harm.

## Consequences
+ Booking no longer fails when Billing fails.
- Billing is eventually consistent; reports may briefly disagree.
- Need retry, dead-letter handling and a reconciliation job.
Fitness function: build fails if Appointment imports a Billing client.
```

Note how the record names the sacrificed characteristic (immediate consistency) and links the decision to an automated check.

## Pitfalls

- Presenting a pattern as universally correct, ignoring the organization's context.
- Comparing options only on their strengths.
- Using fashion ("everyone does microservices now") instead of constraints as the argument.
- Diving into implementation detail before the why is agreed.
- Writing ADRs after the fact with no alternatives, which turns them into announcements rather than records of analysis.
