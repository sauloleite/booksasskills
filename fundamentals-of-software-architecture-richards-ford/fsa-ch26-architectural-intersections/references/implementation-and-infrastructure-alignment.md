# Implementation and Infrastructure Alignment

## Contents
- The nine intersections at a glance
- Implementation: three things the code must honor
- Operational concerns: when good local decisions break the system
- Structural integrity: source layout must mirror logical components
- Architectural constraints: rules that make a style work
- Infrastructure: where operational characteristics are actually delivered
- Cloud-era misalignments
- Pitfalls and review questions

## The nine intersections at a glance

An architecture can be a sound match for its characteristics and still fail because something around it pulls in another direction. The chapter names nine surrounding facets that must line up with the design. Use this as an audit list when creating or validating an architecture:

| Intersection | Question to ask |
|---|---|
| Implementation | Does the code honor operational goals, the logical structure, and the stated constraints? |
| Infrastructure | Can the deployment environment actually deliver the scalability, availability, responsiveness and fault tolerance the style promises? |
| Data topologies | Do the database layout and database types fit the style and the data? |
| Engineering practices | Do build, test, release and the pipeline match what the style assumes? |
| Team topologies | Are teams partitioned the same way the architecture is? |
| Systems integration | Do the systems you call (or that call you) match your characteristics and keep your quanta intact? |
| Enterprise | Does the solution conform to company-wide standards and principles? |
| Business environment | Does the style suit where the company is heading (cost pressure, growth, volatility)? |
| Generative AI | If LLMs are part of the system, can they be swapped, guarded and evaluated? |

## Implementation: three things the code must honor

Architects often wave off concerns as "an implementation detail". The chapter argues this dismissal causes many architecture failures. The source code must stay aligned with the design on three axes:

1. **Operational concerns** (the architecture characteristics that drove the style choice).
2. **Internal structure** (the logical components and their dependencies).
3. **Constraints** (the restrictive rules the style needs in order to deliver its benefits).

## Operational concerns: when good local decisions break the system

Pattern to watch for: the architect optimizes for characteristic A, the developers solve a local problem by optimizing for characteristic B, and the two optimizations collide under real load. Neither party made a bad call; they served different goals.

Invented example in the spirit of the chapter: a ticketing platform picks microservices for elasticity during on-sale spikes. Developers find that the Seat Booking service must synchronously ask the Venue Inventory service for seat maps, which hurts latency and couples the two. They embed a replicated in-memory copy of the seat map in every Booking instance. Latency drops. During a large on-sale the orchestrator adds dozens of Booking instances; each carries the full replica, memory is exhausted across the fleet, and the system falls over at exactly the moment elasticity was meant to save it.

How to catch this early:
- Restate the top driving characteristics to the team whenever a cross-service data access pattern is designed.
- For any per-instance replicated state, estimate memory per instance multiplied by the peak instance count, and compare to node capacity.
- Ask of every performance fix: which driving characteristic does this weaken?
- Record the fix in an ADR so the trade-off is visible and reviewable.

## Structural integrity: source layout must mirror logical components

Logical components normally materialize as directories, packages or namespaces. If developers create folders and namespaces ad hoc, the code stops reflecting the logical architecture. Consequences: harder maintenance, testing and deployment, lower reliability, and poor ability to absorb new features.

Remedies:
- Communicate the component map and keep collaborating with the team; tooling alone is not enough.
- Automate structural checks in the build. Tools named in the chapter: ArchUnit (Java), ArchUnitNet and NetArchTest (.NET), PyTestArch (Python), TSArch (TypeScript/JavaScript).

A small framework-agnostic illustration of the idea (not tied to any of those tools):

```python
# Fails the build if a module imports from a namespace it is not allowed to see.
ALLOWED = {
    "app.orders":    {"app.orders", "app.shared"},
    "app.billing":   {"app.billing", "app.shared"},
    "app.shared":    {"app.shared"},
}

def violations(import_graph):
    """import_graph: dict of module -> set of imported modules."""
    bad = []
    for mod, deps in import_graph.items():
        owner = next((k for k in ALLOWED if mod.startswith(k)), None)
        for dep in deps:
            if owner and not any(dep.startswith(a) for a in ALLOWED[owner]):
                bad.append((mod, dep))
    return bad
```

## Architectural constraints: rules that make a style work

A constraint is a restrictive rule the architecture depends on (for example, only REST between services, or a mandated database type). If the code ignores it, the architecture fails, so the architect must both identify constraints and communicate them.

Worked pattern (layered style chosen for low budget, tight deadline and frequent schema churn). The style only pays off if:
- all persistence logic lives in the persistence layer, and
- presentation code never calls persistence directly; requests pass through every layer, including trivial lookups.

Typical violations: UI developers query the database for speed; backend developers merge business and data access code because it feels easier to test. The result is that a column rename ripples through every layer, changes slow down, and the very business goal that justified layering is missed.

Checklist for constraints:
- Write each constraint down with the characteristic or business goal it protects.
- Explain the "why" to every team that could break it.
- Govern each constraint with an automated structural test where possible (the same tools as above).
- Treat a constraint violation discovered in review as an architecture defect, not a style nit.

## Infrastructure: where operational characteristics are actually delivered

Key idea: a style's capacity for scale or availability is only potential. If the infrastructure does not supply it, the system will not have it. Architects and developers are frequently blamed for failures that really came from an architecture/infrastructure mismatch.

Historical arc, summarized:
- Around the mid-2000s operations was commonly outsourced under formal SLAs, and the relationship with architecture was contractual.
- Architects designed defensively, assuming operations was beyond their control, and built scale and elasticity into the architecture itself (orchestration-driven SOA with heavy tooling; space-based architecture with built-in elastic scale). These designs became very complex.
- Microservices took the opposite stance: let operations handle operational concerns, and collaborate closely. This simplified designs and helped seed DevOps.
- The Pets.com story (late 1990s pet supplies retailer) is the cautionary tale: a famous marketing mascot, an underpowered platform, a holiday rush that overwhelmed it, and collapse. The lesson is that sudden success without elastic capacity can kill a business, which is why on-demand scaling became a commodity cloud feature.

Root cause of most misalignment: weak communication between architects and the people who run infrastructure, plus architects underestimating how strongly infrastructure shapes scalability, responsiveness, fault tolerance, performance, availability and elasticity.

## Cloud-era misalignments

Even with cloud platforms, deployment choices can quietly cancel design benefits:
- Spreading services across regions or availability zones can erode or eliminate the speed and consistency gains of replicated or distributed caches.
- Packing services, containers or pods onto the same VM boosts performance but hurts scalability, fault tolerance, availability and elasticity (shared failure domain, shared resource ceiling).

Remedy: close architect/infrastructure collaboration or full DevOps practice, so everyone knows which operational characteristics are critical and why.

## Pitfalls and review questions

- Did anyone multiply per-instance memory by peak instance count?
- Is there an automated test for each structural rule and each constraint?
- Does the deployment topology (zones, regions, co-location) support or undermine each driving characteristic?
- Was infrastructure staff in the room when the style was chosen?
- When something fails in production, has the team checked for an intersection mismatch before blaming the design?
