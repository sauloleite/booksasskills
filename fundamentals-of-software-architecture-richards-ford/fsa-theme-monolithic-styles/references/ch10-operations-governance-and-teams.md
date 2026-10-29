# Data, Cloud, Risks, Governance and Team Fit

## Contents
- Data topology
- Cloud deployment options
- Operational risks: fault tolerance and recovery time
- Governance with fitness functions
- Team topology fit
- Growth strain on platform teams
- Checklist

## Data topology

The default is one monolithic application over one monolithic (usually relational) database. The Persistence layer commonly carries the object-relational mapping work, translating between object graphs in the application language and set-oriented tables. Implications for the agent:
- Schema changes ripple through Persistence and often Business; treat schema as a cross-layer contract.
- Splitting the database later is a large migration, not a configuration change. If future decomposition is likely, keep data access behind Persistence so the split stays contained.

## Cloud deployment options

Because the style is a monolith cut into technical layers, cloud choices are limited to placing one or more layers with a cloud provider. The technical partitioning does make that split natural (for example, hosting Presentation in the cloud while Business and Persistence stay on-prem).

Warning to raise: nearly every workflow crosses most layers, so a layer boundary that also becomes an on-prem to cloud boundary adds latency on almost every request. Before recommending a hybrid split, count the cross-boundary calls per typical request and estimate round-trip cost. Chatty Business-to-Persistence traffic across that link is the usual failure.

## Operational risks: fault tolerance and recovery time

- Fault tolerance is poor. There is a single deployment unit and no architectural modularity, so one defect that, say, exhausts memory takes down the whole application.
- Availability suffers through mean time to recovery (MTTR). Monolith restarts are slow: the book cites roughly 2 minutes for small applications and 15 minutes or more for large ones.

When availability targets are strict, quantify: expected crashes per month multiplied by restart time gives downtime from restarts alone; compare that with the SLO budget. Mitigations within the style (more instances behind a load balancer, faster startup, health checks) help but do not create isolation between features.

## Governance with fitness functions

Governance is a strength. Structural testing tools such as ArchUnit (Java), NetArchTest and ArchUnitNET (.NET), import-linter (Python) and dependency-cruiser (JavaScript/TypeScript) were largely designed with layers in mind. The pattern:
1. Name each layer and bind it to a package or namespace pattern.
2. Declare, for each layer, which layers may access it. Closed layers translate into "only the layer directly above may call me"; open layers widen that list.
3. Run the check in CI so violations fail the build.

Original illustration (Python, framework-agnostic idea): map modules to layers, then fail on any import outside an allow-list.

```python
import ast, pathlib

LAYER_OF = {"app.web": "presentation", "app.domain": "business",
            "app.repo": "persistence"}
ALLOWED = {"presentation": {"business"},
           "business": {"persistence"},
           "persistence": set()}

def layer(module):
    return next((l for p, l in LAYER_OF.items() if module.startswith(p)), None)

def test_layer_dependencies():
    bad = []
    for f in pathlib.Path("app").rglob("*.py"):
        src = layer(".".join(f.with_suffix("").parts))
        for node in ast.walk(ast.parse(f.read_text())):
            if isinstance(node, ast.ImportFrom) and node.module:
                dst = layer(node.module)
                if src and dst and dst != src and dst not in ALLOWED[src]:
                    bad.append(f"{f}: {src} -> {dst}")
    assert not bad, "\n".join(bad)
```

The `ALLOWED` table is exactly what `scripts/layer_rules_check.py --emit-allowed` prints from an ordered list of layers with open/closed flags, so the design and the test stay in sync. Note that some tools' built-in "layers" contracts only forbid upward calls and do not forbid skipping; enforcing closed layers may need explicit forbidden rules.

## Team topology fit

The style is largely indifferent to team structure and works with all four Team Topologies types:

| Team type | Why it fits |
|---|---|
| Stream-aligned | System is usually small and self-contained; one team can own a flow end to end through every layer. |
| Enabling | Specialists can experiment inside one layer (for example, trial a new UI library in Presentation) without disturbing the others. |
| Complicated-subsystem | A layer with a narrow job is a natural attachment point; for example, an analytics team given access at Persistence to operational data, leaving stream-aligned teams' layers untouched. |
| Platform | Abundant tooling for this style (structural tests, profilers, deployment pipelines for monoliths) is easy to leverage. |

## Growth strain on platform teams

The recurring monolith problem: keep adding features and, however clean the layering and governance, the system starts hitting ceilings such as database connection limits, memory, throughput, concurrent users. Keeping it running demands ever more effort from the platform team. Track these ceilings as leading indicators that the style is being outgrown (see the style-fit reference for when to migrate).

## Checklist

- [ ] Data store and ORM boundary identified; schema treated as a contract.
- [ ] Any hybrid cloud split assessed for per-request cross-boundary latency.
- [ ] Restart time measured; downtime-from-restarts compared with availability target.
- [ ] Layer access map encoded as a CI fitness function, including open-layer exceptions.
- [ ] Team ownership mapped: who owns flows end to end, who owns specialist layers.
- [ ] Capacity ceilings (connections, memory, concurrency) monitored with thresholds.
