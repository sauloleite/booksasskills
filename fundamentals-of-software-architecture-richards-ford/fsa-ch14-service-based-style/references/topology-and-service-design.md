# Topology and Domain Service Design

## Contents
- Baseline topology
- Inside a domain service
- Granularity trade-off: transactions vs. change scope
- User interface variants
- Adding an API layer
- Cloud deployment
- Glossary

## Baseline topology

The default shape has three macro-layers, each deployed on its own:

1. One user interface (UI) deployment.
2. A handful of remote, coarse-grained **domain services**, each owning a whole domain or subdomain (for example order fulfillment, shipping, assessment).
3. Optionally, one shared relational database.

Every part of that baseline can be split further (several UIs, several databases), which is why the style is called flexible. Treat the baseline as a starting point, not a rule.

Deployment facts an agent should state when proposing the style:

- Domain services deploy like a normal monolithic application. Containers are allowed but not required.
- Default is one running instance per service. Add instances only for throughput or failover, and then put a load balancer between UI and service.
- Access protocol is usually REST. Messaging, RPC, SOAP or a gateway are also valid.
- The UI typically locates services itself through an embedded service locator; the same locator logic can instead live in a gateway or proxy.
- A single shared database lets services keep using SQL joins across tables. Connection exhaustion is rarely a concern because there are few services. The hard part is schema change (see data-topologies.md).

**Size limit:** with one shared database, keep the service count low. The authors recommend at most about 12 domain services; beyond that, change control, scaling and fault isolation degrade.

## Inside a domain service

Because each service is large, it needs internal structure. Two common designs:

| Design | Internal structure | When it fits |
|---|---|---|
| Layered | API facade, then business layer, then persistence layer | Simple domains, teams used to layered apps |
| Subdomain-partitioned | Components per subdomain, like a small modular monolith | Rich domains where you want finer modularity inside the service |

Whatever the internal design, every service exposes an **API access facade**. The facade receives one business request from the UI and orchestrates all internal steps with in-process calls.

Worked illustration (invented): a `ClaimsService` receives "submit claim". Its facade validates the policy, records the claim, reserves a payout, and schedules an adjuster, all as class-level calls inside one deployment. In a microservices design the same request would fan out into remote calls to several single-purpose services. That shift from internal class orchestration to external service orchestration is the key structural difference between the two styles.

```python
# Facade orchestrates in-process, inside one ACID transaction
class ClaimsFacade:
    def submit(self, req):
        with self.db.transaction():          # commit or roll back as a unit
            policy = self.policies.validate(req.policy_id)
            claim = self.claims.record(policy, req)
            self.payouts.reserve(claim)      # raises -> whole unit rolls back
            self.scheduler.assign_adjuster(claim)
        return claim.id
```

## Granularity trade-off: transactions vs. change scope

Coarse services buy data integrity and pay for it in change scope.

**What you gain (ACID inside a service):** if a step fails (say the payment card is expired during checkout), the service simply rolls back everything it wrote in that request and reports the failure. No partial state escapes.

**What fine-grained services pay instead:** with separate order and payment services, the order row is already committed before the remote payment call fails. The data is now inconsistent and needs a compensating update to undo the order. Such systems rely on BASE semantics (basic availability, soft state, eventual consistency).

**What you lose (change scope):** a change to one function in a large service means retesting and redeploying the entire service, including unrelated functionality living in it. More code shipped per deployment means more chance of breaking something unrelated. A single-responsibility microservice confines both the test effort and the blast radius.

Decision rule: when a domain needs strong transactional consistency across several steps and changes at a moderate pace, coarse is the better bet. When one slice of a domain changes very often or has a very different scaling profile, that slice is a candidate to carve out.

## User interface variants

Three points on a spectrum:

1. **Single UI** for all services (baseline).
2. **Domain-grouped UIs**, one per user group or area (for example a public customer app, an internal warehouse app, a support console).
3. **One UI per domain service.**

Moving down the list improves scalability, fault isolation and agility at the UI tier, and lets you keep internal screens off the public network. It also raises the number of deployables to manage.

## Adding an API layer

Insert a reverse proxy or API gateway between UIs and services when one or more of these holds:

- Domain functionality must be exposed to external systems.
- Cross-cutting concerns (metrics, security, auditing, service discovery) should be consolidated in one place rather than repeated in every service.
- Some services run multiple instances and need load balancing.

The gateway is also the right place for any cross-domain orchestration, keeping services independent of each other.

## Cloud deployment

The style is distributed, so it runs naturally in the cloud. Because services are broad in scope, package them as containers rather than serverless functions. They can consume managed storage, database and messaging services like any other workload.

## Glossary

- **Domain service:** a separately deployed, coarse-grained service scoped to one domain or subdomain.
- **API access facade:** the entry point of a domain service that takes a UI request and orchestrates the internal work.
- **Compensating update:** an extra write that reverses an earlier committed write when a later step in a distributed workflow fails.
- **Service locator:** logic that resolves which service endpoint to call; embedded in the UI or in a gateway.
