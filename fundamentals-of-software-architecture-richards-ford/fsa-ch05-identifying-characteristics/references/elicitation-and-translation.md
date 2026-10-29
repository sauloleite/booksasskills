# Eliciting Characteristics and Translating Business Language

## Contents
- Three sources of characteristics
- Translating domain concerns into "-ilities"
- Composite characteristics and how to decompose them
- Explicit versus implicit characteristics
- Decoding numbers: scalability, elasticity, performance
- Integration points and the brittleness trap
- Glossary

## Three sources of characteristics

Look in three places, in this order of effort:

1. **Domain concerns** voiced by business stakeholders. This is where most characteristics originate, but they arrive in business vocabulary.
2. **Requirements artifacts** (specs, user counts, SLAs, regulatory notes). These often contain numbers that hide a characteristic.
3. **Implicit domain knowledge** the architect brings. Every system implicitly needs things like security and modularity, and some domains carry their own implicit needs. Example: anyone building software that ingests readings from clinical devices treats data integrity and message loss as non-negotiable without being told.

Agent rule: when a user gives you only a requirements list, explicitly add a pass for (3). Ask "what would a veteran of this industry assume without writing it down?"

## Translating domain concerns into "-ilities"

Stakeholders and architects talk past each other: one side says "user happiness" or "we are buying competitors", the other says "fault tolerance" or "interoperability". The architect owns the translation. Typical mappings (a starting point, not a lookup table to apply blindly):

- **Acquisitions and mergers**: the system must absorb foreign systems and data, so look at interoperability, scalability, adaptability and extensibility.
- **Speed to market**: the team must ship often and safely, so look at agility and its parts (testability, deployability).
- **User satisfaction**: very broad; it can touch performance, availability, fault tolerance, security, plus the delivery-speed group (testability, deployability, agility).
- **Competitive edge**: usually means change fast and stay up under growth, so the delivery-speed group plus scalability, availability and fault tolerance.
- **Tight time and budget**: favor simplicity and feasibility over ambitious capabilities.

After translating, force the ranking question: is speed to market worth more than scalability here, or do fault tolerance, security and performance dominate? Sometimes the answer is a combination, but the question must be asked so decisions are justifiable later.

## Composite characteristics and how to decompose them

A composite characteristic has no single objective measure; it is made of several measurable ones. Agility is the canonical case: you cannot measure it directly, but you can measure deployability, modularity and testability.

Pitfalls:
- **False equivalence**: treating a composite as identical to one business concern (for example "agility means time to market") or to one of its parts.
- **Partial focus**: optimizing only the most obvious component because it is convenient. This is like baking a cake and leaving out a core ingredient.

Decomposition procedure an agent can run:
1. Write the stakeholder statement verbatim.
2. Name the obvious characteristic it suggests.
3. Ask failure questions against it: What if it is fast but down? What if volume grows? What if it crashes midway? What if it is fast but wrong? Who must prove later that it was right?
4. Each failure question that matters becomes a component characteristic (availability, scalability, reliability, recoverability, auditability, and so on).
5. Give each component an objective definition so it can be measured and governed later.

Worked example (invented): "Payroll must reach the bank before the 18:00 transfer cutoff, every business day." A naive reading yields only performance. Running the failure questions adds availability (the batch window cannot be missed because a node is down), scalability (headcount grows after an acquisition), reliability (no mid-run crashes), recoverability (resume from the last committed employee batch instead of restarting), and auditability (regulators and employees can dispute amounts). All of these deserve equal attention with performance.

Most business goals begin life as composites. Decomposing them and attaching objective definitions is core architect work, and it feeds directly into measurement and governance (the next chapter's topic).

## Explicit versus implicit characteristics

- **Explicit**: stated in the requirements as part of the needed design, often as a number (concurrent users, response time, regions served).
- **Implicit**: never written down, yet essential. Typical members: availability (users can reach it), stability (sessions are not dropped mid-interaction), security (nobody wants insecure software), modularity.

Implicit does not mean architectural by default. Security, for instance, is always present, but it becomes an architectural characteristic only when it shapes structure and is critical to success. If payments are delegated to a third-party processor and developers follow ordinary hygiene (no plaintext card numbers, minimal retention), security is handled by good design, not by architecture.

When pruning later, explicit characteristics are the more likely candidates to cut, because implicit ones tend to underpin general success.

## Decoding numbers: scalability, elasticity, performance

Requirements rarely say "scalability"; they say "thousands of users, maybe millions one day." Decode such statements into engineering terms.

- **Scalability**: handling a growing number of concurrent users over time without serious degradation. Think of a curve that rises steadily.
- **Elasticity**: absorbing sudden bursts. Think of spikes. A seasonal hotel booking site is scalable but not especially elastic; a ticketing site at on-sale time needs heavy elasticity. Elastic systems frequently also need scalability.
- Treat them as separate characteristics: they are often lumped together but impose different constraints.
- Look for bursts the requirements never mention by asking about real-world usage patterns. Meals cluster around lunch and dinner; students procrastinate.

Worked calculation (from the chapter's registration scenario, numbers reused for illustration): 1,000 students and a 10-hour window. Even spread: 100 per hour. Realistic last-minute crush: all 1,000 in the last 10 minutes, which is 6,000 per hour equivalent, a 60x peak over the naive average. Domain knowledge, not the spec, reveals the 60x.

- **Performance**: nuanced (several kinds exist). Always define it together with scale: set a baseline with no particular load, then state the acceptable level at a given user count. Characteristics interact, so many must be defined relative to each other.

## Integration points and the brittleness trap

A requirement to call external services (maps, traffic, payments) introduces integration points, and a failing dependency can reduce the caller's reliability. The opposite error is overspecifying: if the traffic feed is down, should the whole ordering site fail, or degrade to directions without live traffic? Prefer graceful degradation and avoid designing in unnecessary fragility.

```python
def directions(order, router, traffic):
    route = router.route(order.shop, order.address)
    try:
        route = traffic.adjust(route, timeout=0.5)
    except (TimeoutError, ConnectionError):
        route.note = "live traffic unavailable"
    return route
```

## Glossary

- **Composite characteristic**: one with no direct measure, defined by measurable parts (agility).
- **Implicit characteristic**: needed but never stated; becomes architectural only if structural and critical.
- **Elasticity**: tolerance for bursts, distinct from steady growth (scalability).
- **Sacrificial architecture**: a deliberately simple design expected to be replaced, chosen when cost, time or skills are tight.
