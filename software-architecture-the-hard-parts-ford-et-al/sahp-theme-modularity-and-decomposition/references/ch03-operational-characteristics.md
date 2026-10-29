# Operational Characteristics: Scalability, Elasticity, Fault Tolerance

These complete the competitive-advantage side of the driver chain. They are the drivers that most clearly require separate deployment units rather than a modular monolith.

## Contents
- Scalability vs. elasticity
- Granularity vs. modularity, and mean time to startup
- How architecture styles compare (qualitative)
- Fault tolerance and the synchronous-dependency caveat
- Decision rules and pitfalls

## Scalability vs. elasticity

- **Scalability**: staying responsive while user load grows gradually, typically over months as the business grows.
- **Elasticity**: staying responsive through sudden, large, erratic bursts of load, measured in seconds or minutes.

Both are about responsiveness as concurrent requests rise, but they are solved differently. Invented example: a university course-registration system idles at a few dozen users most of the term, then jumps to thousands within a minute when enrollment opens. Steady growth in student numbers is a scalability concern; the enrollment-minute burst is an elasticity concern. Handling the burst needs both enough peak capacity and the ability to bring new instances online almost instantly.

## Granularity vs. modularity, and MTTS

- **Elasticity depends mostly on granularity**, meaning the size of each deployment unit. Small units start fast.
- **Scalability depends mostly on modularity**, meaning that the application is split into separate deployment units at all, so each part can scale on its own.

The key metric for elasticity is **mean time to startup (MTTS)**. Architecture sets the baseline (small, fine-grained services); design then tunes it (lightweight runtimes and platforms, lean startup paths). A coarse unit cannot be made elastic by tuning alone.

## How architecture styles compare (qualitative)

- **Layered monolith**: everything scales together (application-level scaling) and startup is slow. Scaling is costly, especially on pay-per-use cloud infrastructure, because idle features are replicated alongside the hot one.
- **Service-based (coarse domain services)**: scaling improves because each domain scales separately, but elasticity improves less, since a whole domain in one unit still starts too slowly to absorb an instant spike (domain-level scaling, middling MTTS).
- **Microservices (fine-grained, single-purpose)**: both scalability and elasticity are at their best (function-level scaling, fast MTTS).

The detailed ratings for these styles come from the authors' earlier book (Fundamentals of Software Architecture); use the qualitative ordering above, not numbers.

**Communication caveat.** As with testability and deployability, the more services must call each other to finish one business transaction, the worse scalability and elasticity get. When high scale or elasticity is a goal, keep synchronous inter-service calls to a minimum.

## Fault tolerance

**Definition used here.** The ability of some parts of the system to stay responsive and available while other parts fail. Invented example: in a food-delivery app, if the loyalty-points module runs out of memory, customers should still browse menus and place orders, simply without earning points for a while.

**Monoliths.** All monoliths have weak fault tolerance. Running several load-balanced copies helps a little but is expensive and ineffective against bugs: a defect that crashes one copy is present in every copy and can take them all down.

**Modularity.** Separate deployment units confine a catastrophic failure to the unit where it happens, giving domain-level or function-level fault tolerance.

**The caveat that decides it.** If other services call the failing service synchronously and wait for it, the failure spreads and fault tolerance is lost. Asynchronous communication between services is therefore essential for keeping fault isolation in a distributed system.

Agent checks:
- For each critical user journey, trace the synchronous call chain. Any non-critical service on that chain (surveys, analytics, recommendations, notifications) is a fault-tolerance leak; move it behind a queue or event, or make the call optional with a fallback.
- Identify which area actually causes outages (from incident data) before deciding what to isolate first.
- `scripts/modularity_impact.py` reports, per unit, which other units fail with it when only synchronous edges propagate failure.

## Decision rules

1. Name the load pattern first: gradual growth (scalability) or bursts (elasticity). They lead to different granularity choices.
2. For bursts, demand small units with fast startup; coarse domain services will not absorb spikes.
3. For gradual growth with uneven load across domains, coarse domain services may be enough, and they cost less than fine-grained ones.
4. Separate competing workloads (for example, operational reporting against a transactional store) into their own units and data, or splitting the code will not relieve the contention.
5. Isolate failure-prone, non-core functions from core user flows and connect them asynchronously.
6. Re-check every benefit against the communication graph; heavy synchronous chatter cancels scalability, elasticity and fault tolerance together.

## Pitfalls

- Treating extra monolith instances as fault tolerance.
- Chasing elasticity with coarse services and runtime tuning alone.
- Splitting services while keeping a synchronous call from every core flow to every helper service.
- Claiming scalability gains while all units still hit one shared, overloaded database.
