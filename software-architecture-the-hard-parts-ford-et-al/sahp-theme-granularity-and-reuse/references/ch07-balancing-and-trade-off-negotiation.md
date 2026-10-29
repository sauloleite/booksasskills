# Balancing Drivers and Negotiating Granularity Trade-offs

## Contents
- Why balance, not rules
- Mapping drivers to business value
- Writing trade-off statements
- Facilitating the decision
- Design versus architecture: mitigating without splitting
- Recording the decision
- Worked example A: claims intake and adjudication
- Worked example B: merchant onboarding
- Worked example C: shipping carriers
- Lessons from the chapter's two case studies
- Glossary

## Why balance, not rules

No single driver decides granularity. A split is justified when the disintegrators that apply outweigh the integrators that apply, and "outweigh" is a business judgment, not a technical one. The architect's job is to find every relevant driver on both sides, measure what can be measured, and then frame the conflict so a product owner or sponsor can choose. Seat-of-the-pants debates ("it is a separate thing, so it should be a separate service") are what this approach replaces.

## Mapping drivers to business value

Translate each technical driver into the outcome a sponsor understands:

Disintegrators (what splitting buys):
- Scope and function: services with one clear, tightly cohesive purpose.
- Code volatility: agility, because each change has a smaller test surface and lower release risk.
- Scalability: lower run cost and quicker response under load.
- Fault tolerance: more uptime for the functions that remain healthy.
- Security: tighter control over who can invoke sensitive operations.
- Extensibility: agility in adding new variants, hence faster time to market.

Integrators (what keeping together buys):
- Database transactions: atomic, consistent data.
- Workflow: resilience, latency and reliability of end-to-end requests.
- Shared code: simpler maintenance and synchronized change.
- Data relationships: correct data without chatty cross-service lookups.

## Writing trade-off statements

Pair one active disintegrator with one active integrator and phrase the conflict as a question about business priority. Template:

> "Splitting X gives us [disintegrator benefit, in business terms], but costs us [integrator benefit lost]. Given our goals, which matters more right now: [benefit A] or [benefit B]?"

Guidelines:
- One conflict per statement. If three drivers compete, write several statements.
- Use business vocabulary (time to market, customer wait time, audit exposure, cloud bill), not technical vocabulary (ACID, MTTS, LCOM).
- Include frequency or magnitude where you have it ("the export code changes weekly"; "most checkouts use two payment methods").
- Ask, do not advocate. The sponsor's answer is the tiebreaker, and different sponsors will legitimately answer differently.
- Record "for now" decisions as such; granularity is revisited when the measured drivers change.

## Facilitating the decision

- Bring the people who own each competing concern (for instance the product owner for consistency, a security lead for access control).
- Facilitate rather than control: state the trade-off neutrally, let each side voice its non-negotiables, then look for options that satisfy them.
- Frame disagreements between engineers in the same way. Two developers arguing "one function" versus "two functions" can usually agree on a factual statement (for example, "these are distinct activities but cannot complete without each other"), and the trade-off question follows from that shared fact.
- The goal is the most appropriate answer for this context, not a winner.

## Design versus architecture: mitigating without splitting

Several disintegrator benefits can be partially obtained inside one deployment unit:

- **Change isolation:** separate the volatile logic into its own clearly bounded component (namespace, module or package) inside the consolidated service. It does not reduce deployment scope, but it reduces cognitive and code-level coupling and keeps a future extraction cheap.
- **Access control:** enforce authorization for sensitive operations with security libraries applied at both the API gateway and inside the service mesh (a two-layer check), plus tokenization and encryption of the sensitive fields. This is a design-level control instead of an architecture-level boundary.

Use these mitigations when an integrator wins but the losing disintegrator still matters. Document what remains unmitigated (for example, the combined service still scales and deploys as one unit).

Short illustration of internal component boundaries in one service (Python-flavored, invented):

```python
# claims_service/
#   intake/        stable: form validation, document capture
#   adjudication/  volatile: rules engine, changed often
#   shared/        domain types used by both

from claims_service.intake import accept_claim
from claims_service.adjudication import decide

def submit(claim):
    accepted = accept_claim(claim)        # local call, no network hop
    return decide(accepted)               # same transaction scope
```

An architecture fitness check (for example, an import-linter rule) can keep `intake` from importing `adjudication` internals, preserving a clean seam for later extraction.

## Recording the decision

Write an architecture decision record for each granularity decision. Useful content:
- Context: the functions involved and the options considered (single, fully split, partial split).
- Decision with the drivers that won and the evidence behind them (change rates, throughput numbers, request mix, transactional requirement).
- Consequences: the drivers that lost and what they cost (larger test scope, shared scaling, weaker isolation) plus any design-level mitigation adopted.
- Revisit trigger: the measurement that would reopen the question.

## Worked example A: claims intake and adjudication

Drivers found:
- Volatility: adjudication rules change roughly three times a month; intake changes quarterly.
- Workflow: every accepted claim is adjudicated immediately and synchronously; a rejection by adjudication sends the claim back to intake for more documents. Nearly all requests cross both functions.
- Throughput: identical, since every intake request produces one adjudication.
- Fault tolerance: no gain, because neither can complete a claim without the other.

Trade-off statement: "Separating adjudication lets us release rule changes with less testing, but every claim would need two services and a back-and-forth on rejection. Which matters more: faster rule releases, or faster and simpler claim processing with fewer failure modes?"

Likely outcome: one service with separate internal components for intake, adjudication and shared types. Consequence: rule changes still retest and redeploy intake.

## Worked example B: merchant onboarding

Drivers found:
- Security: bank account and tax identifiers are regulated; only a small finance team should reach those operations.
- Transactions: the business insists that a merchant can never exist without verified banking details.

Options: one service; separate Profile and Banking services; or a single service with gateway plus mesh authorization and field-level encryption.

Trade-off statement: "Separate services give us stronger access control to banking data, but we lose the guarantee that a merchant is created with its banking details or not at all. Which do we prioritize: access isolation, or all-or-nothing onboarding?"

If the sponsor picks atomicity and the security lead accepts layered authorization, consolidate and record the security mitigation as a consequence. If the security lead rejects it, split and plan for compensating actions on failed onboarding.

## Worked example C: shipping carriers

Drivers found:
- Extensibility: four carriers today; the business has signed letters of intent with three more this year (a confirmed pattern, not speculation).
- Workflow: about one order in five ships in multiple parcels across carriers; label generation happens asynchronously after checkout, so no customer waits on it.

Analysis: the confirmed growth pattern supports splitting per carrier. The workflow share is small and non-interactive, so the integrator is weak. Split.

Contrast: if the request mix were reversed and labels had to be returned synchronously during checkout, responsiveness could outweigh extensibility, especially with only one or two new carriers expected.

## Lessons from the chapter's two case studies

The chapter closes with two stories from its running fictional company. In the first, a team debates splitting a frequently changing expert-assignment algorithm from the routing step that delivers work to the expert. Because the two steps are synchronously bound (routing failure loops back to assignment), share the same load, and give no fault-tolerance benefit apart, the team keeps one service and isolates the algorithm in its own internal component, accepting larger test scope. In the second, customer registration spans profile, payment card, credential and product data; the business demands all-or-nothing registration, so the team keeps one service and handles access risk with layered security libraries, accepting shared scaling and deployment.

Takeaways:
- Volatility alone loses to tight synchronous coupling.
- A firm atomicity requirement can beat a security disintegrator when security can be addressed through design.
- Always state the losing side's cost in the decision record.

## Glossary

- **Granularity disintegrator:** an evidence-based reason to split a service.
- **Granularity integrator:** an evidence-based reason to keep or merge services.
- **Volatility-based decomposition:** splitting along areas of differing change frequency.
- **Atomic request:** a request fully served by one service.
- **Workflow request:** a request that needs more than one service to complete.
- **MTTS (mean time to start):** how fast a new instance becomes ready; larger units start slower, hurting elasticity.
- **Leftover cohesion:** whether the functions remaining after a split still form a nameable, purposeful service.
- **Trade-off statement:** a business-language question pairing what a split gains with what it costs.
