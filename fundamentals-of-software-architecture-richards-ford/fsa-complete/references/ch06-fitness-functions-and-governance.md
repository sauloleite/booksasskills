# Governance and Architectural Fitness Functions

## Contents
- Why governance needs automation
- What a fitness function is
- Mechanism catalog
- Modularity fitness functions: cycles, main-sequence distance, layers
- Collaboration and the gaming problem
- Production fitness functions: chaos engineering and the Simian Army
- The checklist mindset
- Design playbook
- Glossary
- Self-check questions

## Why governance needs automation

Governance (the word traces to the Greek for steering) is a core architect responsibility covering any part of development the architect wants to influence, including software quality. The hard part is enforcement under schedule pressure: urgent work crowds out important-but-not-urgent concerns such as modularity. The industry's automation lineage gives a path: Extreme Programming led to continuous integration, CI led to operations automation (DevOps), and the same chain extends to automated architectural governance via fitness functions (from *Building Evolutionary Architectures*, Ford, Parsons, Kua and Sadalage).

## What a fitness function is

The term is borrowed from evolutionary computing. A genetic algorithm needs an objective function that scores how close a candidate solution is to the goal; for a traveling-salesperson search you might score route length, total cost and time away, each with its own function. An **architectural fitness function** is any mechanism that objectively assesses the integrity of one architecture characteristic or a combination of them.

Key implications:

- It is a perspective, not a framework to install. Many existing tools become fitness functions when used to guard a characteristic.
- "Any mechanism" is deliberate: verification is as varied as the characteristics.
- Each one should be objective (pass/fail or a number against a threshold), automated where possible, and traceable to a prioritized characteristic.

## Mechanism catalog

| Mechanism | Guards, for example | Runs |
|---|---|---|
| Unit-test-style architecture rules (ArchUnit for Java, NetArchTest for .NET) | layering, naming, dependency direction, test hygiene | build |
| Metrics with thresholds (JDepend, CC tools) | cycles, main-sequence distance, complexity | build |
| Monitors | latency percentiles, error rates, page weight | deploy, production |
| Chaos engineering | resilience, latency tolerance, region failure | production |

## Modularity fitness functions: cycles, main-sequence distance, layers

**Cyclic dependencies.** Components that reference each other in a loop cannot be reused or deployed alone, and spreading cycles push the system toward a Big Ball of Mud. IDE auto-import dialogs make accidental cross-component references trivially easy, and developers dismiss them by reflex. Code review catches this too late: a week of careless imports does real damage before anyone looks. Fix: a build-time test that analyzes package or module dependencies and fails when any cycle exists. The book uses JDepend; any language can do the same.

**Distance from the main sequence.** Using the abstractness (A) and instability (I = Ce / (Ca + Ce)) metrics from Chapter 3, D = |A + I - 1|. A test iterates over every package and fails when D exceeds a tolerance around the ideal of 0. The tolerance is project specific; 0.5 is a reasonable starting point. High D means the zone of pain (concrete and heavily depended upon) or the zone of uselessness (abstract and unused).

**Layer rules.** In a layered monolith the architect defines layers for reasons (see Chapter 10). Some developers do not grasp those reasons; others knowingly bypass them for a local concern such as performance, preferring to apologize later. Either way, erosion damages long-term health. A declarative rule set states which layer may be accessed by which, and the build fails on any other dependency. A rule-file example for `scripts/dependency_fitness.py`:

```ini
[layers]
api         = shop.api.*
domain      = shop.domain.*
persistence = shop.persistence.*
[allow]
api -> domain
domain -> persistence
```

An edge `shop.api.cart -> shop.persistence.cart_repo` then fails as "api -> persistence not allowed".

## Collaboration and the gaming problem

- Design fitness functions with developers, not from an ivory tower. Esoteric checks nobody understands breed resentment and workarounds. The book's guidance: developers should understand why a fitness function exists before it is imposed on them.
- Any visible metric invites gaming: people optimize the number instead of the outcome. Classic case: tests with no assertions that touch code purely to lift coverage. Counter with a governance rule that every test contains at least one assertion (expressible in ArchUnit-style tools or a custom lint), and consider mutation testing.
- Determined rule-breakers will always find a way; fitness functions mainly stop accidental lapses, which is most of the value.

## Production fitness functions: chaos engineering and the Simian Army

When Netflix moved to AWS it lost direct control of operations and created chaos engineering to find out how the system behaved when things went wrong.

| Tool | What it checks or does |
|---|---|
| Chaos Monkey | injects general failures in production to test endurance |
| Latency Monkey | injects high latency (a real AWS issue at the time) |
| Chaos Kong | simulates losing a whole Amazon datacenter, so real outages of that size are survivable |
| Conformity Monkey | enforces architect-defined rules in production, e.g. every service answers all requests without errors |
| Security Monkey | flags known security defects such as unexpected open ports and misconfiguration |
| Janitor Monkey | finds services nothing routes to anymore (left behind by evolutionary migration) and removes them to stop cloud spend |

Conformity, Security and Janitor are the clearest examples of automated governance. The broader lesson: failure is a matter of when, not if, so rehearsing it makes systems robust (see Rosenthal and Jones, *Chaos Engineering*).

## The checklist mindset

Atul Gawande's *The Checklist Manifesto* shows pilots and surgeons using checklists not from ignorance but because repetitive, detailed work lets small things slip. Fitness functions play that role: lightweight, automated reminders of principles that compete with hundreds of other priorities (developers know not to ship insecure code, yet it still happens). They embed governance into the substrate of the architecture rather than adding a heavyweight approval process.

## Design playbook

1. Start from the prioritized characteristics list; pick the few whose erosion would hurt most.
2. For each, choose the mechanism and the stage (build, deploy, production) where the check is cheapest and earliest.
3. Write the rule objectively with an explicit threshold; record the rationale next to it.
4. Review it with the developers who will live with it; adjust until they agree it guards something real.
5. Wire it into the pipeline so it fails the build or raises an alert, not a report nobody reads.
6. Allow explicit, documented exceptions instead of loosening the global rule.
7. Revisit thresholds as the system and its tools evolve; retire checks that no longer map to a priority.

## Glossary

- **Architectural fitness function**: objective, ideally automated integrity check for one or more architecture characteristics.
- **Important versus urgent**: the governance gap; fitness functions guard important concerns that daily deadlines push aside.
- **Production fitness function**: a check that runs against the live system (monitors, chaos experiments, conformity scans).
- **Gaming a metric**: satisfying the measurement without the intended quality.

## Self-check questions

- Which of our top characteristics has no automated check at all?
- Would a new cyclic dependency be caught today before merge?
- Can every developer explain why each failing fitness function exists?
- Which metric could be satisfied without delivering the quality it stands for?
