# Fitness Functions and Architecture Governance

## Contents
- The governance problem
- Why automation: lessons from XP and DevOps
- Definition and its three parts
- Atomic versus holistic scope
- Fitness function or unit test? The domain-knowledge question
- Static, dynamic and manual fitness functions
- When to run them
- Enterprise-wide governance: the pipeline "slot"
- Example fitness functions (original sketches)
- Benefits and the overuse warning
- Design checklist

## The governance problem

Once an architect has defined component relationships and structural rules, the question is how to make sure implementers follow them when the architect is not the one writing the code. Architecture governance covers any organized oversight of some aspect of software development. Manual governance (code reviews, architecture review boards) is slow and superficial: details slip through, much as they did when operations staff configured servers by hand.

## Why automation: lessons from XP and DevOps

The chapter traces a recurring pattern:
- Early software borrowed a manufacturing metaphor (Waterfall at large scale, late big-bang integration at small scale). Integration pain grew with project size.
- Extreme Programming (Kent Beck and the C3 team) showed that incremental feedback and automation drive productivity; continuous integration replaced the integration phase. Branch-heavy version control habits are a leftover of the old model.
- DevOps applied the same lesson to operations once open source was good enough and machines could be defined programmatically.

In each case technology plus insight automated a recurring task that an expensive role used to do by hand. Architecture governance is the next candidate: replace review-board policing with automated, objective checks.

## Definition and its three parts

A fitness function (from Building Evolutionary Architectures, 2017) is any mechanism that objectively assesses the integrity of one architecture characteristic or a combination of them. Each phrase matters:

- **Any mechanism.** Not a specific tool. Architecture-structure test libraries, monitors for performance or scalability, and chaos engineering for reliability and resilience all qualify.
- **Objective integrity assessment.** The characteristic needs a measurable definition. "High performance" cannot be tested; "p95 checkout latency under 300 ms at 500 concurrent users" can. Beware composite characteristics such as agility: they are not measurable directly, so decompose them into measurable contributors (deployability, testability, cycle time). If you cannot measure a characteristic, the definition is probably too vague.
- **One characteristic or a combination.** This sets the scope (next section).

## Atomic versus holistic scope

- **Atomic:** checks one characteristic in isolation. Example: no dependency cycles among components.
- **Holistic:** checks several interacting characteristics together, because improving one can harm another. Security controls often cost performance; designing for many concurrent users (scalability) can make sudden bursts (elasticity) harder. A holistic function exercises the combination to ensure the net effect stays acceptable, for example a load test run with the full security stack enabled.

Rule: when a decision deliberately trades one characteristic for another, add a holistic check covering both so the trade does not silently drift.

## Fitness function or unit test? The domain-knowledge question

Fitness functions verify architecture characteristics; unit, functional and acceptance tests verify domain behavior. To decide which you need, ask whether running the check requires any domain knowledge.
- Needs domain knowledge (validating the parts of a postal address, pricing rules): write a conventional test.
- Needs none (surviving a sudden spike in users, no forbidden layer access, no cycles): write a fitness function. An elasticity check looks identical for a game, a shop or a bank.

The line is not perfectly sharp; some checks touch both. Use the question as a sorting heuristic, not a law.

## Static, dynamic and manual fitness functions

- **Static (non-contextual):** fixed result, such as pass/fail or a numeric threshold.
- **Dynamic:** the acceptable result depends on context. Typical case: scalability, where per-user response time may degrade gently as concurrent users rise, but must not collapse. The threshold is a function of load rather than a constant. Objective does not mean static.
- **Manual:** some validations need a person, for example legal review of changes to modules handling sensitive legal data. Put them in the pipeline as manual approval stages and run them as often as practical, since an unexecuted check validates nothing.

## When to run them

Fitness functions run either on demand (uncommon) or inside continuous integration (the norm). Continuous execution is what delivers the value. Configure pipelines to trigger on any ecosystem change: application code, database schema, deployment configuration, and the fitness functions themselves.

## Enterprise-wide governance: the pipeline "slot"

The chapter uses the 2017 Equifax breach as a cautionary case: a patched Apache Struts vulnerability (CVE-2017-5638) remained in many older systems for months because finding affected projects relied on manual scans that missed some of them.

The proposed alternative: every project has a deployment pipeline, and the security team owns a slot in each pipeline where it can inject its own fitness functions. Normally these perform routine hygiene (for example, no plaintext secrets in data stores). When a zero-day appears, the team adds one check everywhere that fails any build using the vulnerable library version and alerts security. Uniform pipelines turn an enterprise-wide hunt into a single automated rollout.

Agent guidance: when advising on platform or pipeline standards, recommend a shared, centrally managed governance stage that every team's pipeline includes, so cross-cutting checks can be deployed to all projects at once.

## Example fitness functions (original sketches)

Structural, atomic: fail the build if internal Python packages import each other in a cycle.

```python
# test_no_cycles.py: reads an edge list "pkg_a -> pkg_b" produced by your import scanner
import collections

def find_cycle(edges):
    graph = collections.defaultdict(list)
    for a, b in edges:
        graph[a].append(b)
    state = {}
    def visit(node, path):
        state[node] = "open"
        for nxt in graph[node]:
            if state.get(nxt) == "open":
                return path + [node, nxt]
            if nxt not in state and (found := visit(nxt, path + [node])):
                return found
        state[node] = "done"
    for n in list(graph):
        if n not in state and (c := visit(n, [])):
            return c

def test_no_component_cycles():
    edges = [tuple(l.split(" -> ")) for l in open("deps.txt").read().splitlines()]
    assert find_cycle(edges) is None
```

Structural, macro level: declare which layers may call which, and fail on any other edge.

```python
ALLOWED = {"api": {"service"}, "service": {"persistence"}, "persistence": set()}

def layer_violations(edges, layer_of):
    return [(a, b) for a, b in edges
            if layer_of(a) != layer_of(b)
            and layer_of(b) not in ALLOWED[layer_of(a)]]
```

Dynamic, holistic: acceptable latency scales with load.

```python
def latency_budget_ms(concurrent_users):
    return 200 + 0.05 * concurrent_users   # gentle slope, no cliff

def test_latency_under_load(results):        # results: [(users, p95_ms), ...]
    assert all(p95 <= latency_budget_ms(u) for u, p95 in results)
```

Off-the-shelf equivalents exist for structural checks: ArchUnit (JVM), NetArchTest (.NET), dependency analyzers such as JDepend, and code-quality platforms such as SonarQube that ship many common checks ready to use.

Why cycles and layer bypasses matter: IDEs offer to auto-import a missing reference, developers accept reflexively, and components become mutually dependent. Then no component can be reused alone and the codebase slides toward a Big Ball of Mud. Layer rules erode the same way when developers skip a layer for a local reason such as performance. Code review catches this too late; a week of unchecked imports already does damage. Continuous checks catch it on the commit that introduces it.

## Benefits and the overuse warning

Benefits:
- An executable specification of the architecture that anyone can verify by running the build.
- Architects get to write code again and must stay close to how the system evolves.
- They guard what is important but not urgent. Projects under deadline pressure defer quality fixes with "we will fix it later", and later rarely arrives; this is a classic source of technical debt.
- They act like the professional checklists described in The Checklist Manifesto: experts skip steps not from ignorance but because repetition breeds blind spots. Fitness functions are a checklist that cannot be skipped, whether by accident or under schedule pressure.

Warning: do not build an elaborate, interlocking web of checks from an ivory tower. Overly complex governance frustrates teams and gets resented or gamed. Keep the set small and focused on principles that matter.

## Design checklist

For each proposed fitness function, confirm:
1. Which characteristic(s) does it protect, and is the definition measurable?
2. Atomic or holistic? If the decision trades characteristics, is there a holistic check?
3. Does it need domain knowledge? If yes, it is a regular test instead.
4. Static, dynamic (context-dependent threshold) or manual?
5. Where does it run (CI, deploy stage, production monitor) and what triggers it?
6. Who owns it, and how are justified exceptions recorded (link to the ADR)?
7. Is it worth its maintenance cost, or is it ivory-tower overhead?
