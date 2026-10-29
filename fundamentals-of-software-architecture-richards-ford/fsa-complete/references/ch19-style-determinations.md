# Making the Style Determinations

## Contents
- Domain/architecture isomorphism
- Fit and misfit heuristics
- Determination 1: monolith or distributed
- Determination 2: where data lives
- Determination 3: synchronous or asynchronous
- Outputs of the process
- Pitfalls
- Self-check questions

## Domain/architecture isomorphism

"Isomorphism" here means the generic shape of an architecture: how its parts depend on each other across the topology, ignoring specific technologies. The term comes from Greek roots for "equal" and "form"; mathematically it is a mapping that keeps elements and their relationships intact.

Using it in practice:
- Sketch each candidate style as an abstract shape. A layered monolith reads as horizontal technical slices; a modular monolith reads as vertical domain slices; a distributed style reads as separate deployable nodes linked by network calls.
- Sketch the problem's shape too: Is it a stable core plus many variations? Many independent parallel tasks? A long chain where each step depends on earlier ones? Several areas with very different load profiles?
- Prefer the style whose shape mirrors the problem's shape. A mismatch means fighting the architecture forever.

## Fit and misfit heuristics

| Problem shape | Good structural match | Poor match |
|---|---|---|
| Stable core with many customer- or region-specific variations | Microkernel (variations as plug-ins) | Styles with no natural extension point, unless customization is designed into the domain |
| Huge numbers of independent, discrete computations (e.g. genomic analysis jobs) | Space-based (many parallel processing units) | Single-process monolith |
| Very high concurrent user load | Distributed, independently scalable parts | Large, tightly coupled monolith |
| Heavy semantic coupling (e.g. a multi-page insurance application where each page depends on prior answers) | Deliberately coarse-grained style such as service-based | Fine-grained, highly decoupled microservices |
| Parts with sharply different operational needs | Microservices (separates by characteristics) | Pure event-driven split by orchestration vs choreography only |

Note that event-driven architectures tend to be partitioned by communication pattern (orchestrated vs choreographed) rather than by characteristic, so when the main driver is variance in characteristics across parts, microservices usually maps better.

## Determination 1: monolith or distributed

Ask: can one set of architecture characteristics serve the whole system?
- Yes: a monolith is likely suitable, though other factors (team scale, deployment independence) may still push toward distribution.
- No, different parts need different characteristics: favor a distributed style.
- Tool: architecture quantum analysis. Each quantum is an independently deployable unit with its own characteristics; more than one quantum means distribution.
- Smaller budgets and simpler applications reward the simplicity of a monolith.

## Determination 2: where data lives

- Monolith: usually one relational database, occasionally a few. Consider grouping tables to match domain components so a future split is cheap.
- Distributed: choose which services persist data and which are pass-through (a conduit service may need no storage at all). Then trace how data moves between services to compose each workflow.
- Design structure (what owns what) and behavior (how workflows flow) together, and iterate; the first combination is rarely the best.

## Determination 3: synchronous or asynchronous

Decide only after data placement is settled.

Default to synchronous. It is simpler to design, implement and debug. Its cost is weaker scalability, reliability and related characteristics, because callers depend on callees being available and fast.

Move a link to asynchronous only with a stated reason, for example:
- Producer and consumer have very different throughput, so a queue must absorb bursts.
- Many requests can arrive at once (e.g. many events closing together) and a slow downstream would cause timeouts.
- A downstream dependency is critical but fragile, and buffering adds reliability.
- Performance or scale targets cannot be met with blocking calls.

Budget for the async costs: data consistency across services, deadlocks, race conditions, harder debugging and tracing.

A compact rule an agent can encode for each connection:

```python
def choose_link(rate_mismatch: bool, burst_risk: bool,
                fragile_downstream: bool, needs_extreme_scale: bool) -> str:
    """Return 'async' only when a concrete reason exists; else 'sync'."""
    reasons = [name for name, flag in [
        ("throughput mismatch", rate_mismatch),
        ("burst / timeout risk", burst_risk),
        ("fragile downstream", fragile_downstream),
        ("extreme scale/perf", needs_extreme_scale)] if flag]
    return "async: " + ", ".join(reasons) if reasons else "sync (default)"
```

## Outputs of the process

A finished style selection should deliver:
1. **Topology**: the chosen style plus any hybrid elements (for instance a microkernel core with BFF adapters, or microservices that use queues on selected links).
2. **ADRs** for the decisions that took the most effort or are most contestable.
3. **Fitness functions** that protect key structural principles (e.g. "every domain component consults the customization component") and operational characteristics (latency, throughput, availability).

## Pitfalls

- Choosing by domain label ("it's e-commerce, so microservices") instead of by characteristics.
- Choosing by trend without checking whether the trend's original pain applies.
- Selecting microservices without mature engineering practice.
- Making everything async "for scale" and inheriting consistency and debugging pain everywhere.
- Fragmenting a semantically coupled workflow into many tiny services.
- Abandoning a well-fitting style because of one weakness that targeted design could mitigate.
- Presenting the result as the correct answer rather than the least-bad trade-off under stated assumptions.

## Self-check questions

1. Which characteristics, if any, differ between parts of this system, and how many quanta does that imply?
2. What is the problem's shape, and which candidate style shares it?
3. Which services must own data, and which only relay it?
4. For every async link, what specific reason justifies it?
5. Which weakness of the chosen style matters most here, and how is the design compensating?
6. Which ADRs and fitness functions accompany the topology?
