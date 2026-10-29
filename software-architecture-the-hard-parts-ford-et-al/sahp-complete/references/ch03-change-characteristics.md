# Change Characteristics: Maintainability, Testability, Deployability

These three together make up architectural agility (and therefore speed-to-market). All three improve with modularity, and all three degrade again when the resulting pieces talk to each other too much.

## Contents
- Maintainability: definition, the maintainability-level metric, component metrics, change scope
- Testability: ease plus completeness, and the communication trap
- Deployability: ease, frequency, risk, and lockstep deployment
- Checklist and pitfalls

## Maintainability

**Definition used here.** How easily features can be added, changed or removed, plus how easily internal upkeep can be applied (patches, framework and third-party upgrades). It is a composite and hard to measure directly.

**Maintainability level (ML).** Alexander von Zitzewitz proposed an objective metric. Its initial form is:

```
ML = 100 * (1/k) * sum over components i of (1 - c_i / k)
```

k is the number of logical components; c_i is the coupling level of component i, emphasizing incoming coupling (how many others depend on it). The result runs from 0 to 100 percent. Reading: the more components lean on each component, the lower the score. The full published metric is more elaborate (it also condenses dependency cycles), so use the simple form to compare designs or track a trend, not as an absolute grade. `scripts/modularity_impact.py` computes it from an edge list.

**Practical component metrics** (when the formula is overkill):

- Coupling: how much and in what ways components know about each other.
- Cohesion: how strongly a component's operations relate to one another.
- Cyclomatic complexity: nesting and indirection inside a component.
- Size: total statements in a component (a size outlier often hides several components).
- Technical vs. domain partitioning: whether components follow layers (UI, logic, persistence) or business areas.

A **component** in this sense is a building block that performs a business or infrastructure function, usually visible as a package, namespace or directory grouping (for example a `billing.invoice.reminders` namespace).

**Change scope ladder.** Ask at which level a typical requirement lands:

| Style | Typical change scope | Coordination |
|---|---|---|
| Layered monolith (technical partitioning) | Application level: every layer | Often UI, backend and database specialists |
| Service-based (coarse domain services) | Domain level: one domain service | One team, one deployment unit |
| Microservices (fine-grained) | Function level: one small service | Smallest blast radius |

Invented example: adding a "pause subscription" option in a layered monolith needs a screen change, new business rules and contract changes in the service layer, and a new column in the schema, each owned by a different team. In a domain-partitioned design the same change stays within the subscriptions unit. Low maintainability in large monoliths usually comes from three things together: technical layering that smears each domain across the stack, tight component coupling, and weak domain cohesion.

## Testability

**Definition used here.** Both the ease of testing (mostly automated) and the completeness of testing. Measuring only one of the two is the classic mistake; a team with many unit tests can still have neither if a large share are disabled, stale, or missing on critical workflows.

**Why monoliths score low.** Full regression of one huge deployment unit is hard to achieve, and even when it exists, a tiny change triggers thousands of tests. Developers then chase failures unrelated to their change, which slows every change.

**What modularity buys.** Smaller deployment units shrink the test scope per change, allow targeted suites, and make suites easier to maintain, which improves both ease and completeness.

**The communication trap.** If service A is independent, a change to A needs only A's tests. Once B and C call A (or A calls them in a business flow), a change to A drags B and C into the test scope, and ease and completeness both fall. Modularity with chatty services can recreate the monolith's testing problem in a distributed form.

Agent checks:
- For a proposed service, list who calls it. Every consumer joins its change test scope.
- Prefer contracts and consumer-driven contract tests over end-to-end suites spanning many services.

## Deployability

**Definition used here.** Three factors, all required for agility: ease of deployment, deployment frequency, and deployment risk.

- Long release intervals (two weeks or more) bundle many changes, which raises risk and delays fixes that are already done.
- Frequency still has to match what users can absorb; faster is not always better for the customer.

**Why monoliths score low.** Heavy ceremony (code freezes, rehearsal deployments), fear that an unrelated area breaks, and release cycles of weeks or months. Separately deployed units carry less ceremony and risk and can ship more often.

**The lockstep warning.** As services get smaller and must cooperate to finish a business transaction, deployment risk rises again: changing one service means worrying about breaking others. If a set of services has to be deployed together, in a fixed order, the split has failed and merging them back is the honest option (Matt Stine's advice, paraphrased). This end state is the distributed big ball of mud: all the costs of distribution with almost none of the benefits.

Agent checks:
- Can each unit be released alone, with no coordinated release train? If not, find the coupling (shared schema, synchronous chains, breaking contracts, dependency cycles).
- Cycles between services are the clearest lockstep signal; `scripts/modularity_impact.py` reports them.
- Separate the pipeline problem from the architecture problem: the pipeline may also need work, but if one change requires redeploying the whole system, the structure is part of the cause.

## Checklist and pitfalls

- Measure before and after: ML or coupling counts, test suite duration and disabled-test share, release cadence and rollback rate.
- Do not stop at "smaller is better"; check each new boundary for how many consumers it creates.
- Do not count high unit test volume as testability without checking completeness.
- Do not accept a design whose deployment plan has an ordering list of services.
