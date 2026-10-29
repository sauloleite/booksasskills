# Structure, Communication and Data in a Modular Monolith

## Contents
- Shape of the style (domain partitioning in one deployable)
- Glossary
- Choosing the structural option: single code base vs separate module artifacts
- Inter-module communication: direct calls vs a mediator
- Data topology options
- Cloud fit
- Pitfalls

## Shape of the style

A modular monolith ships as exactly one deployable (one WAR/EAR, one .NET assembly, one container image, one wheel). What makes it "modular" is that the code inside is partitioned by business domain, not by technical layer.

The quickest litmus test is the namespace or top-level folder. Look at the segment right after the application root:

| Partitioning | Example path | Segment after root means |
|---|---|---|
| Technical (layered) | `app.web.billing.invoice` | a layer (web, service, persistence) |
| Domain (modular monolith) | `app.billing.invoice` | a business area |
| Domain, then technical inside | `app.billing.invoice.api`, `app.billing.invoice.store` | domain first; layers only as a sub-split |

Rule: the domain always comes first. A module may be split by technical concern underneath when its internals are complex enough, but never the other way around.

A module is one domain or subdomain, built from one or more components (component = a cohesive namespace/folder of source files). Most modules hold several components.

## Glossary
- **Module**: the unit of decomposition in this style; maps to a domain or subdomain and is visible as a top-level namespace, package or directory.
- **Monolithic structure**: every module lives in one repository, separated only by folders/namespaces.
- **Modular structure**: each module is built as its own binary artifact (JAR, DLL, package) and the artifacts are assembled into the single deployable at deploy time.
- **Big Ball of Mud / unstructured monolith**: the end state when boundaries erode; code is so entangled it cannot be pulled apart.
- **DLL Hell / JAR Hell**: version and compile-time dependency tangles among many separately built artifacts.
- **Architectural quantum**: independently deployable unit with its own functional cohesion; for this style it is normally 1.

## Choosing the structural option

| Factor | Favors single code base (monolithic structure) | Favors separate module artifacts (modular structure) |
|---|---|---|
| Module independence | Modules call each other frequently | Modules are mostly self-sufficient |
| System size/complexity | Small to medium | Large, with modules needing distinct expertise or business knowledge |
| Team setup | One team, or teams comfortable sharing a repo | Several teams wanting their own repos and release rhythm per module |
| Operational simplicity | Highest: one place to build, test, deploy | Extra build/versioning work per artifact |
| Boundary protection | Weak by default; needs strict automated governance | Strong by default; compile-time dependencies make crossing deliberate |
| Governance tooling | Easy: one scan over one tree covers everything | Harder: each module repo needs its own checks |

Decision procedure:
1. Map expected call paths between modules. If most business workflows chain through several modules, pick the single code base; separate artifacts will only add shared-interface artifacts and version pain.
2. If modules are largely independent and owned by different teams (or need specialist knowledge), pick separate artifacts for cleaner separation of concerns and less temptation to over-share code.
3. If you pick the single code base, budget for governance from day one (see the governance reference). The convenience of reaching into any class is exactly what erodes it.

## Inter-module communication

Default stance: every cross-module call is a cost. Accept it only when a workflow genuinely spans domains (for example, placing an order must reserve stock and take payment).

### Option A: direct (peer-to-peer) calls
One module instantiates or obtains a class from another module and invokes it.
- Single code base: trivially easy, which is the danger. Nothing stops a developer from reaching into any internal class, so the boundary silently dissolves.
- Separate artifacts: the caller cannot compile without the callee's types, forcing a compile-time dependency. Teams typically extract a shared interface artifact so each module compiles on its own. Too many of these links produce DLL/JAR Hell.
- Use when: few, stable, well-understood interactions.

### Option B: mediator (orchestrator)
A dedicated mediator component receives a request and drives the needed modules in sequence. Modules no longer know about each other.
- Coupling does not vanish; it is concentrated. Every module now depends on, or is driven by, the mediator.
- Only the mediator needs access to other modules' APIs; individual modules stay ignorant of their peers.
- Use when: multi-step workflows touch three or more modules, or peer-to-peer links are multiplying.

Illustrative mediator (original, language-neutral Python):

```python
class CheckoutMediator:
    def __init__(self, orders, stock, payments):
        self.orders, self.stock, self.payments = orders, stock, payments

    def checkout(self, cart):
        order_id = self.orders.create(cart)
        self.stock.reserve(order_id, cart.items)
        self.payments.charge(order_id, cart.total)
        self.orders.mark_paid(order_id)
        return order_id
```

The `orders`, `stock` and `payments` objects expose small public facades; none of them imports another.

### Choosing between them
- Count the distinct module pairs that would talk directly. If the number keeps rising, introduce a mediator.
- If one module would be called by most others, check whether it is really shared infrastructure (a platform concern) rather than a domain.
- If many workflows still need heavy cross-module chatter even with a mediator, the domain boundaries are probably wrong; redraw them before adding more plumbing.

## Data topology options

| Option | When it fits | Trade-off |
|---|---|---|
| One shared database | Default for a single deployable; modules that need each other's data | Fewer cross-module calls because data is directly reachable, but schema coupling grows silently |
| Database (or schema) per module | Modules are independent and own clearly contextual data | Stronger isolation and an easier future split, but cross-module data needs go through calls |

Practical middle ground: one physical database with a schema or table prefix per module, plus a rule (enforced by review or tooling) that a module reads and writes only its own tables.

## Cloud fit
- The single deployable cannot scale or provision pieces on demand, so it gains little from elastic cloud infrastructure.
- Small systems can still run happily in the cloud and use managed services (object storage, managed databases, messaging).
- If the main reason for going to the cloud is elastic, per-function scaling, this style is the wrong fit.

## Pitfalls
- Organizing the root by layer and calling it "modular" because it has many packages.
- Shared "common" or "utils" modules that grow until every module depends on them.
- Reaching into another module's internal classes instead of a published facade.
- Splitting into separate artifacts while modules are still chatty, then drowning in shared-interface artifacts.
- Treating a mediator as a fix for bad domain boundaries.
