# Enterprise Operator and Knowing Your Audience

## Enterprise operator: the corporate telephone game

In the children's game where a phrase is whispered around a circle, the final version rarely matches the first. Organizations do the same thing: someone misspeaks, a listener hears what they expected, a person unfamiliar with a term substitutes a familiar one. No amount of personal communication skill prevents it entirely; the goal is to be ready.

Typical symptoms, especially around enterprise standards:
- "Someone in security said we are noncompliant."
- "I heard library X is now mandatory."
- A team suddenly resisting a guideline for reasons nobody can source.

Response playbook:
1. Recognize the pattern. Expect noise and frayed tempers; stay calm.
2. Locate the break. Trace the message back hop by hop to find who received a partial or misinterpreted version. The break point tells you where to focus the fix.
3. Map the people. Identify everyone involved, especially stakeholders you did not know about, and contact them directly to reconcile.
4. Retrospect. Ask what you could have done to prevent the distortion (clearer written standard, glossary, FAQ, direct briefing of business partners).

Throughout, ask for and bring evidence: does the cited standard exist, and does it actually apply to this application?

### Worked example (invented)

An architecture group publishes guidance favoring stateless services with a separate client-side UI layer. Weeks later, a product team's lead is furious, convinced they must rewrite everything onto a specific vendor framework. Rather than defend the guidance, you ask them to walk through their current architecture and discover they already meet most of it. Tracing back, a business stakeholder heard a talk mentioning one category of library, mistook it for an unrelated product with a similar acronym, and warned the team. Clearing up that single misunderstanding turns a hostile session into a cooperative one. Lessons: listen before presenting again, inspect the actual system, and find the hop where the meaning changed.

## Know your audience

Engineers spend most of their time with other technical roles (developers, architects, testers, product managers). Seniority brings more time with less technical stakeholders, so translating from engineering vocabulary into business language becomes a core skill that needs practice.

Rules:
- Jargon impresses no one outside the team. Many people know a common framework name only as an ordinary word.
- Learn from sales engineers and vendors who are good at speaking to executives: they connect technical capability to the customer's business problem.
- Decision makers fund outcomes, not novelty. Replace "it is a cool new technology" with what it changes: faster delivery, lower cost, fewer incidents, less risk.
- Tone matters. Dismissive or sarcastic responses to management ("go read the docs") stall careers compared with a collaborative approach.
- Understand the domain and your business partner's top concerns. You cannot articulate value without knowing what the business values.

### Translation drill

| Engineer framing | Business framing |
|---|---|
| Migrate to a managed message broker | Remove a class of overnight outages and the on-call cost attached to them |
| Add contract tests between services | Ship changes to partner integrations without breaking customers |
| Refactor the billing module | Cut the time to launch new pricing plans from weeks to days |

Use the drill before any update to non-technical stakeholders: state the outcome first, the technical change second, and the evidence third.

## Pitfalls

- Treating a rumored standard as fact without asking for its source.
- Re-presenting the same deck to an angry room instead of first understanding their architecture and concern.
- Assuming the loudest person in the room originated the misunderstanding.
- Leading with technology names when addressing executives.

See also: influence-and-stakeholders.md for framing arguments around a decision maker's priorities.
