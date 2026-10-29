# Agile and Evolutionary Architecture, Fitness Functions

## Contents
- Architecture inside Agile teams
- Designing for change
- Hypothesis-driven development
- Titles versus responsibilities
- Why architectures decay
- Fitness functions: definition and uses
- Writing fitness functions
- Lifecycle of fitness functions
- Pitfalls

## Architecture inside Agile teams

Teams that claim to be "too Agile for architects" still make architectural decisions; someone is always making them, and whether they were good becomes visible a year or two later. Architecture and agility coexist, with two adjustments:
- Many architectural activities span more than one iteration (vendor procurement, legal review, platform setup). Plan them as tracks that run alongside sprints instead of forcing them into one.
- Stop trying to foresee every future requirement. Assume change will come and design so it is cheap.

## Designing for change

Evolutionary architecture (from Ford, Parsons, Kua and Sadalage) means supporting guided, incremental change along several dimensions (business, technical, data, operational). The emphasis is on **incremental**. Agile is a set of nested feedback loops: short iterations and frequent demos of working software let stakeholders react early instead of discovering after months that the target was missed. Architectural decisions should ride the same loops.

## Hypothesis-driven development

Settle architectural debates with data, not with whoever argues loudest. Frame each change as a testable bet:

- We believe **[change]**
- will lead to **[outcome]**
- and we will consider it successful when **[metric moves past threshold]**.

Invented examples:
- We believe moving PDF generation to a background queue will cut checkout latency; success is p95 checkout under 800 ms for a week of normal traffic.
- We believe consolidating three reporting services into one module will speed feature delivery; success is median lead time for reporting changes falling from 9 days to under 4 within two months.

Rules: pick the metric and threshold before building, measure a baseline, run the smallest experiment possible, and revert or adjust when the threshold is not met.

## Titles versus responsibilities

The architect title varies wildly: some companies reserve it for people reporting to an architecture VP, some have no such title. Regardless, senior developers routinely make decisions in the architect's territory, and busy architects delegate tasks to developers. For an aspiring architect, accept those delegated tasks; they are the apprenticeship.

## Why architectures decay

Organizations invest heavily in choosing an architecture and little in keeping it. Like entropy in a closed system, structure degrades unless someone counteracts it. From the first commit the system drifts; new joiners lack the context of why key choices were made; eventually customers notice slowness or outages. The chapter's anecdote: a legacy application whose slowdown had crept in over roughly three years, making the root cause very hard to find. A regularly run performance check would have caught it early, likely before users did.

## Fitness functions: definition and uses

The term comes from evolutionary computing, where each mutated candidate is scored for how well it meets the objective. In architecture, a fitness function is any check that measures how closely the system still meets a chosen architectural characteristic, flagging when it drifts out of bounds.

Think of them as:
- tests that ensure refactorings and new features do not violate the architecture;
- an executable to-do list that architects hand to developers;
- lightweight, low-ceremony governance (no review board needed to catch a broken rule).

Typical targets (thresholds are per-system choices):
- average or p95 service response time under a budget (for example 100 ms);
- cyclomatic complexity per function at or below a limit (for example 5);
- response time staying reasonable as users and request rates grow (load test curve);
- dependency rules (the domain layer never imports the web layer; no module reads another module's tables);
- availability and error-rate budgets; container image size; startup time; licence or vulnerability policies.

## Writing fitness functions

Start from the ranked quality attributes: each top attribute should have at least one check. Prefer automated checks in the CI/CD pipeline; keep a small, explicit set of manual checks where automation is impractical (for example a quarterly security review), with an owner and a date.

Example: a dependency-direction rule as an ordinary test (Python, stdlib only).

```python
import ast, pathlib

FORBIDDEN = {"app.domain": ("app.web", "app.infra")}  # layer -> must not import

def imports_of(path):
    tree = ast.parse(path.read_text())
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            yield node.module
        elif isinstance(node, ast.Import):
            yield from (a.name for a in node.names)

def test_domain_layer_stays_pure():
    for layer, banned in FORBIDDEN.items():
        root = pathlib.Path(*layer.split("."))
        for f in root.rglob("*.py"):
            bad = [m for m in imports_of(f) if m.startswith(banned)]
            assert not bad, f"{f} imports {bad}"
```

Example: a latency budget check run against a staging deploy.

```python
import statistics, time

def p95(samples):
    return statistics.quantiles(samples, n=20)[18]

def test_quote_endpoint_latency(client):  # client: test fixture
    samples = []
    for _ in range(200):
        t0 = time.perf_counter()
        client.get("/quote?sku=123")
        samples.append((time.perf_counter() - t0) * 1000)
    assert p95(samples) < 150, f"p95={p95(samples):.0f} ms"
```

Link each fitness function to the ADR it enforces (the ADR's Governance section names it), and vice versa in a code comment.

## Lifecycle of fitness functions

- Identify the first set early in the project, right after ranking attributes.
- Expect them to change as the system and priorities change.
- Review them on a schedule: drop the irrelevant ones, tighten or relax thresholds, and replace manual checks with automated ones as better techniques appear.

## Pitfalls
- Choosing an architecture and never verifying it afterward.
- Thresholds with no rationale; record why 150 ms and not 500 ms.
- Flaky performance checks that teams learn to ignore; run them in a stable environment and compare against a trend, not a single run.
- Fitness functions that nobody owns once the original architect moves on.
