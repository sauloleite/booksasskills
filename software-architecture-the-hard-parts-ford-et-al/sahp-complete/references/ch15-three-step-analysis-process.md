# The Three-Step Process for Building Your Own Trade-Off Analysis

The book's worked analyses (saga patterns, communication styles, granularity forces) are a starting kit, not a complete catalog. Every real system adds its own entangled concerns, so the architect must extend the method: add columns for local concerns, drop ones that do not apply, and rerun it. The method has three steps.

1. **Find** which parts of the problem are entangled.
2. **Analyze** how those parts are coupled.
3. **Assess** trade-offs by asking what a change in one part does to the parts that depend on it.

## Step 1: Find entangled dimensions

Entangled (or "braided") dimensions are concerns that cannot be decided independently: choosing one constrains the others. They are specific to each architecture, but people who know the ecosystem (developers, architects, operations staff, DBAs) can surface them. Include those roles in discovery; an architect working alone will miss operational and data entanglements.

### The working definition of coupling

Use the simplest test: if X changes, could Y be forced to change? If yes, X and Y are coupled and belong in the analysis.

### Building a static coupling inventory for a service

No off-the-shelf tool can draw this for you, because every estate is different. Build it by hand or, better, emit it from the automation that already provisions environments. For each deployable unit (architecture quantum), record:

- Base image, OS and container runtime it depends on.
- Frameworks and libraries, including what arrives transitively through the dependency manager.
- Data stores and platform services it persists to or queries (relational and document databases, search indexes, cloud resources).
- Integration points it must reach just to start up (config servers, secret stores, service registries, identity providers).
- Messaging infrastructure needed to talk to other quanta (brokers, topics, queues).

Exclude services whose only link to this one is participation in a shared workflow. Those are statically independent but dynamically coupled at runtime; track them in the dynamic analysis instead.

Teams with infrastructure-as-code or generated pipelines should add a step that writes these coupling points out on every build, so the inventory never drifts from reality.

### How the authors chose their dimensions

The communication, consistency and coordination dimensions were not invented up front. They emerged from reviewing a large number of distributed systems and noticing which concerns every one of them was sensitive to. Do the same locally: look across several of your own systems or incidents and ask which concerns repeatedly forced change elsewhere. Those recurring concerns are your dimensions.

## Step 2: Analyze coupling points

1. **Enumerate combinations lightly.** List the possible combinations of the chosen dimensions (for example, sync or async times atomic or eventual times orchestrated or choreographed). Sketch each as a small topology, not a full design.
2. **Prune infeasible combinations early.** Some pairings make no practical sense; skip modeling them and note why.
3. **Pick the forces to rate.** Decide which outcome qualities need trade-off analysis. The book rated coupling level, complexity, responsiveness/availability and scale/elasticity alongside the three dimensions. Your list may add cost, security exposure, team autonomy, data residency or operability.
4. **Rate each option in isolation first.** Evaluate one candidate at a time against all forces, without peeking at the others, to avoid anchoring.
5. **Consolidate into one matrix afterwards.** Only then line the candidates up side by side.
6. **Read the matrix for correlations.** Patterns across rows are often the most useful finding.

### Correlations the book observed

- More coupling in a workflow goes with worse scalability and elasticity, consistently and strongly: more participating services means more things that must scale together.
- More coupling also goes with lower responsiveness and availability, somewhat less strictly: every extra participant is one more thing whose failure can sink the whole workflow.

Use such correlations as heuristics: if an option raises coupling, expect to pay in scale and availability unless something specific offsets it.

## Step 3: Assess trade-offs

1. Treat the matrix as a "what if" platform: change one dimension and observe what moves.
2. **Decide the most fundamental dimension first.** In the book this was synchronous versus asynchronous communication, because it opens some options and closes others. Fixing it shrinks the remaining space.
3. With that choice locked, repeat the analysis for the decisions it encourages or forces.
4. Stop iterating when the hard, entangled decisions are settled. Whatever remains is ordinary design work, not trade-off analysis.

## Iteration is the method, not a fallback

No architect gets a novel situation right on the first draft, and complex systems keep producing new nuances. Sketching sample topologies and permuting one dimension at a time gives a faster and more thorough view than reasoning ad hoc. Expect several passes.

## Worked example (invented)

A logistics firm must design a shipment-rebooking workflow touching Booking, Carrier, Billing and Notification services.

- Step 1: Ops points out that Carrier calls hit a partner API with strict rate limits; the DBA notes Billing shares a schema with Booking. Both become dimensions alongside communication, consistency and coordination.
- Step 2: Of eight communication/consistency/coordination combinations, two are dropped (atomic consistency across the partner API is impossible). The remaining six are rated in isolation on coupling, complexity, availability, scale and rate-limit safety, then consolidated. The matrix shows every synchronous variant scoring poorly on rate-limit safety.
- Step 3: The team fixes asynchronous communication first. That makes eventual consistency the natural fit, which then raises the question of who tracks rebooking state; orchestration wins because Billing needs a single place to see failures. The rest (topic names, retry intervals) is design.
