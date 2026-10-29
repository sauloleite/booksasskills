# Trade-Offs and the Least-Worst Architecture

## Contents
- Why a system can support only a few characteristics
- The coupled-controls mental model
- The least-worst stance
- Iteration as risk reduction
- Pruning playbook
- Worked example
- Review questions

## Why a system can support only a few characteristics

Four forces cap how many characteristics a design can honor:

1. **Cost.** Each one consumes architect design time, developer effort to build and maintain, and often dedicated structure.
2. **Synergy.** Characteristics interact with each other and with the domain design; every element affects the rest. Example: tightening security adds encryption, indirection to hide secrets, and other work that slows the system.
3. **Ambiguity.** Without standard definitions, teams cannot even agree on what they are optimizing. The industry will never freeze a list, but each organization can maintain its own objectively defined vocabulary.
4. **Expanding scope.** Both the number of characteristics and the number of categories keep growing. Operations was once a black box outside architecture; with microservices and similar styles, architects and operations now work closely, and architecture increasingly entangles with other parts of the organization.

Consequence: maximizing every characteristic is almost never possible. Decisions reduce to trade-offs among competing concerns.

## The coupled-controls mental model

The book compares this to a pilot learning to fly a helicopter: hands and feet each work a control, and moving any one shifts the others. Selecting characteristics is the same balancing act. When proposing to raise one characteristic, the agent should state which others it pushes down and by roughly how much.

Common tension pairs to check (illustrative, not exhaustive):

| Raising | Often pressures |
|---|---|
| Security | Performance, usability |
| Scalability / elasticity | Simplicity, cost, data consistency |
| Configurability / extensibility | Performance, testability |
| Availability | Cost, consistency |
| Portability | Use of platform-specific optimizations |

## The least-worst stance

Do not search for the best architecture; search for the one whose unavoidable weaknesses are most tolerable for this business. Implications:

- Every option has flaws; compare options by the harm of their weaknesses, not by the length of their strength list.
- Over-ambition fails: a design that tries to satisfy every characteristic for every business problem turns generic and unwieldy, and such architectures rarely succeed.
- Make the sacrifices explicit so stakeholders accept them knowingly.

## Iteration as risk reduction

Design the architecture to be as changeable as practical. The cheaper it is to change, the less the team must agonize over getting each characteristic exactly right at the start. Agile's core lesson, the value of iteration, applies at the architecture level too. Prefer decisions that can be revisited, and flag the ones that cannot.

## Pruning playbook

1. List all candidates (explicit and implicit) after the qualification test.
2. For each, write the concrete failure that would occur without it. Remove any with no credible failure.
3. Merge synonyms and split ambiguous terms using the team glossary.
4. Map tensions among the survivors (use the table above as a prompt).
5. Pick the few most critical, typically a handful. Treat the rest as design standards or nice-to-haves.
6. For each kept characteristic, note what it costs (effort, structure, other characteristics).
7. Record which decisions are hard to reverse; invest extra analysis there and keep the rest flexible.

## Worked example

A regional clinic network wants an appointment platform. Stakeholders list 14 qualities. After qualification:

- Kept: availability (patients book at all hours), privacy and legal (health data residency), security (structural: isolated patient-record service), scalability (moderate, seasonal flu peaks).
- Downgraded to standards: maintainability, accessibility (handled by UI guidelines and testing), supportability (logging conventions).
- Dropped: portability across databases (no business driver), configurability by end users (no request).
- Tension accepted: the isolated, encrypted records service adds latency to booking confirmation; stakeholders agree a slightly slower confirmation is preferable to weaker privacy. This is the least-worst choice.
- Changeability: records service sits behind a stable interface so the scaling approach can change later without touching the booking flow.

## Review questions

1. Which kept characteristic would you drop first if the budget halved, and what risk does that create?
2. For each kept characteristic, can you name the structure it requires? If not, why is it architectural?
3. Which two kept characteristics conflict most, and how was the conflict resolved?
4. Which decisions are hardest to reverse, and did they receive proportionally more analysis?
5. Does every term in the list have one agreed, measurable definition?
