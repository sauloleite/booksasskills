# Architecture Versus Design: Classifying a Decision

## Core idea

Architecture concerns the structure and shape of a system; design concerns how it looks and behaves at a finer grain. A house analogy works well: number of floors, roof shape and floor plan are structure; wall colors, flooring and light fixtures are finish. Choosing a distributed style such as microservices sets structure. Choosing the visual layout of a screen is design.

Most real decisions are not that clean. Splitting one service into several, or picking a UI framework, sits somewhere in the middle. Treat the boundary as a continuum and locate each decision on it. The position tells you two things: who should own the decision (architect, tech lead, or individual developer) and how much analysis and recording it deserves.

## The three lenses

### 1. Strategic or tactical

Strategic decisions are long-lived and entangled with other decisions. Tactical ones are short-lived and usually stand alone. Probe with three questions:

| Probe | Leans design (tactical) | Leans architecture (strategic) |
|---|---|---|
| Planning time | Minutes | Weeks |
| People involved | You alone or with one peer | Many meetings, many stakeholder groups |
| Expected lifespan | Likely to be revisited soon | Expected to hold for years |

The probes are subjective; use them to build a rough picture, not a score to defend.

### 2. Level of effort

Martin Fowler's essay "Who Needs an Architect?" defines architecture as the parts of a system that resist change. Apply that literally: estimate the cost to build the thing and, more importantly, the cost to undo it later. Migrating from a layered monolith to microservices is enormous effort, so it is architectural. Moving fields around on a form is cheap, so it is design.

### 3. Significance of trade-offs

Every decision has trade-offs, including small ones. What changes is their weight.

- Heavy: adopting microservices buys scalability, elasticity, agility and fault tolerance, but costs complexity, money, data consistency and performance (because services must call each other). That magnitude marks it as architecture.
- Light: splitting a large class improves readability and maintainability at the cost of a few more files to manage. Minor, so it is design.

## Quick classification procedure

1. State the decision in one sentence.
2. Answer the three strategic probes.
3. Estimate cost to build and cost to reverse (low, medium, high).
4. List the top two gains and top two losses; judge whether any loss is systemic (affects cost, consistency, security, operability across the system).
5. If two or more lenses point to architecture, treat it as architectural: involve the architect, consult stakeholders, and record the decision with its rationale.
6. If all three point to design, let the implementing team decide and move on.
7. If mixed, assign shared ownership: architect sets constraints, team chooses within them.

## Worked examples (invented)

- **Adopt event streaming as the integration backbone for five teams.** Months of planning, many stakeholders, multi-year horizon, costly to reverse, systemic trade-offs (operational overhead, eventual consistency). Firmly architecture.
- **Replace a date-formatting library in one service.** Hours of thought, one developer, easy to swap again, trade-offs local. Design.
- **Split the billing service into invoicing and payments.** Moderate planning, a few teams affected, effort to change is real (data ownership, contracts), trade-offs include extra network calls and distributed transactions. Middle of the spectrum leaning architecture; the architect should at least set the boundary and data rules.
- **Choose a front-end framework for a new product.** Long-lived, affects hiring and every screen, expensive to swap later, but trade-offs are mostly contained to the UI tier. Middle of the spectrum; treat as a joint architect and lead-developer decision.

## Pitfalls

- Calling everything "architecture" so the architect becomes a gate for trivial choices.
- Calling a hard-to-reverse choice "just design" because it looks small today.
- Judging only by build effort and ignoring reversal effort.
- Classifying without listing trade-offs, which hides how heavy the decision really is.
