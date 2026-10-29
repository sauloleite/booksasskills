# Risks, Governance and Team Topology

## Contents
- Common risks
- Style-specific governance
- Fitness function sketches
- Team alignment
- Team Topologies fit
- Pitfall summary

## Common risks

**Chatty domain services.** Calls between domain services are normal in microservices but should be rare here. Ideally domains couple only through the shared database. Heavy inter-service traffic signals one of two things: the domain boundaries are wrong, or this is the wrong style for the problem. Diagnose which before patching with more calls.

**Too many services.** Treat roughly 12 as a practical ceiling. Past it, testing, deployment, monitoring, database connection usage and schema change coordination all get harder. If the domain analysis yields 20 services, either merge related ones or reconsider whether a finer-grained style is the real need.

## Style-specific governance

Apply the general structural and operational checks (cyclomatic complexity, scalability, responsiveness and so on), plus two checks specific to this style:

1. **Change locality.** A typical change should land in one domain service. Track how often commits, tickets or releases span several services. A rising rate means boundaries are poorly drawn or the style no longer fits.
2. **Inter-service communication volume.** Where calls between services can be observed, measure them. Some legitimate cases exist (an order domain asking a notification domain to email status updates), but most cross-domain coordination should happen in the UI or API gateway, not service to service.

## Fitness function sketches

Invented examples an agent can adapt:

```python
# Change-locality check over recent merged changes
def change_locality(changes, max_ratio=0.15):
    """changes: list of sets of service names touched per change."""
    multi = sum(1 for svcs in changes if len(svcs) > 1)
    ratio = multi / max(1, len(changes))
    return ratio <= max_ratio, ratio

# Inter-service call budget from tracing data
def call_budget(edges, allowed):
    """edges: {(caller, callee): calls_per_day}; allowed: set of pairs."""
    return [e for e in edges if e not in allowed]  # unexpected couplings
```

Thresholds such as 15% are team choices, not book numbers. Pick a baseline from history and alert on drift.

Other cheap checks:

- Count deployable domain services; fail the build or raise a review above the agreed ceiling (default about 12).
- Verify each service imports only the entity libraries for partitions it owns or reads.
- Verify the common entity library can only be changed by its designated owners.

## Team alignment

The style is domain partitioned, so it pairs well with cross-functional teams organized by domain. A domain request can be built entirely inside one service by one team without stepping on others.

Teams split by technical layer (UI team, backend team, DBA team) fit poorly. Every domain feature then needs several teams to coordinate, which most organizations find hard to sustain. If the organization is layer-aligned and will not change, weigh that cost explicitly.

## Team Topologies fit

| Team type | Fit | Guidance |
|---|---|---|
| Stream-aligned | Good when streams follow domain boundaries | If a value stream cuts across several services, re-examine service boundaries and granularity; realign them to the stream or pick another style. |
| Enabling | Weaker than in finer-grained styles | Coarse services give specialists fewer seams. Raise internal modularity by defining clear components inside each service so experts can propose changes and experiment at component level. |
| Complicated-subsystem | Good | Domain and subdomain modularity lets these teams own a difficult area in isolation. |
| Platform | Good | Modularity makes shared tooling, services and APIs easy to adopt across domain services. |

## Pitfall summary

- Growing service count beyond the ceiling while keeping one shared database.
- Splitting databases in a way that forces services to call each other for data.
- One entity library shared by everyone.
- Orchestrating across domains via service-to-service calls instead of UI or gateway.
- Assigning domain features to layer-based teams.
- Treating coarse services as untouchable: frequently changing slices should be considered for extraction.
