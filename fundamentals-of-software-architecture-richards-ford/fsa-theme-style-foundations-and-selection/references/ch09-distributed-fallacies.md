# Monolithic Versus Distributed, and the Fallacies of Distributed Computing

## Contents
- The primary classification
- How to use the fallacies
- The original eight (Deutsch and colleagues, Sun, 1994)
- The authors' three additions
- Pre-distribution checklist
- Invented worked example

## The primary classification

- **Monolithic**: all code ships as one deployment unit. Book's examples: layered, pipeline, microkernel.
- **Distributed**: multiple deployment units talking over remote protocols. Book's examples: service-based, event-driven, space-based, service-oriented, microservices.

No taxonomy is perfect, but this split is useful because every distributed style shares a family of problems monoliths simply do not have. Distributed styles can deliver far better performance at scale, scalability, and availability; they pay for it with the fallacies below. Treat the fallacies as a mandatory cost line in any monolith-versus-distributed trade-off analysis.

## How to use the fallacies

Each fallacy is a false assumption. For every one, the agent should (a) name the assumption the design is silently making, (b) ask for the measurement or owner that would disprove it, and (c) name the mitigation and its cost. The more remote calls a design depends on, the larger every fallacy's impact becomes.

## The original eight

### 1. The network is reliable
A healthy service can still be unreachable, or a request can be sent and its reply lost. Mitigations: timeouts on every remote call, circuit breakers, retries only for idempotent operations, and designs that tolerate partial failure. Fine-grained styles with many hops are the most exposed.

### 2. Latency is zero
In-process calls cost nanoseconds to microseconds; remote calls cost milliseconds. Before endorsing any distributed style, especially fine-grained ones, obtain the production round-trip latency: average **and** the 95th to 99th percentile. The tail usually decides whether the design is feasible. Chained calls add up (ten sequential hops at 100 ms each add a full second). Network administrators can usually supply the numbers.

### 3. Bandwidth is infinite
Inside a monolith a request consumes almost no network bandwidth; once split into services, interservice traffic can be large, and saturation feeds back into latency and reliability.
**Stamp coupling** is the main culprit: a consumer receives a whole large structure but uses a sliver of it. Remedies:
- dedicated private endpoints shaped for a consumer
- field selection in the contract
- GraphQL or similar consumer-shaped queries
- value-driven contracts verified with consumer-driven contract tests
- internal messaging endpoints for interservice data
The principle behind all of them: send only what the caller needs.

### 4. The network is secure
Firewalls and VPNs breed complacency. Every endpoint of every deployment unit, including internal service-to-service ones, needs protection against unknown or malicious requests. Distribution multiplies the attack surface, and authenticating every hop adds latency, one reason synchronous fine-grained styles tend to be slower.

### 5. The topology never changes
Routers, switches, firewalls, and appliances change constantly. A "minor" overnight network upgrade can invalidate latency assumptions and trip timeouts and circuit breakers with no application deploy at all. Mitigation: standing communication with operations and network teams about planned changes, plus alerting on latency drift, not just errors.

### 6. There is only one administrator
Large organizations have many network administrators. Knowing whom to ask about latency or topology changes is itself coordination work that a single deployment unit never needed. Map the owners before going distributed.

### 7. Transport cost is zero
Not latency: actual money. Distribution typically needs more hardware, servers, gateways, firewalls, subnets, and proxies than the monolith did. Assume the needed infrastructure is not already there. Before committing, analyze existing servers and network for capacity, bandwidth, latency, and security zones.

### 8. The network is homogeneous
Real networks mix hardware vendors. Standards help, but not every load and combination has been tested, so packets occasionally vanish. This loops back to reliability, latency, and bandwidth: the fallacies compound each other.

## The authors' three additions

### 9. Versioning is easy
Versioning contracts is a sound way to evolve services, but it opens decisions to settle up front:
- Version per service or for the whole system?
- How far does versioning propagate, and which parts of the architecture must understand it?
- How many concurrent versions will be supported? (Unplanned answers drift into supporting dozens.)
- Is deprecation coordinated system-wide or decided service by service?
Agent rule: when a design says "we'll just version the API", require answers to all four in the ADR.

### 10. Compensating updates always work
A compensating update is an orchestrator-issued reversal that restores prior state when a multi-service update partially fails. Designers routinely assume the reversal succeeds. It may not. Any transactional workflow across services must specify both the normal compensation path and the recovery path when the update and its compensation (or parts of each) fail: retries with idempotency, a durable record of pending compensations, alerting, and a manual repair procedure.

```python
# Illustrative orchestration skeleton: compensation can itself fail.
def place_order(order, steps, pending_store, alert):
    done = []
    for step in steps:
        try:
            step.apply(order)
            done.append(step)
        except Exception as err:
            for prior in reversed(done):
                try:
                    prior.compensate(order)
                except Exception as comp_err:
                    pending_store.save(order.id, prior.name, repr(comp_err))
                    alert(f"compensation failed for {order.id}: {prior.name}")
            raise err
```

### 11. Observability is optional
In a monolith, logging is helpful; in a distributed system, comprehensive monitoring and interaction logs are essential, because remote calls fail in many ways that cannot be debugged otherwise. Treat observability as a required architecture characteristic for every distributed style: correlation IDs across hops, per-call latency and error metrics, and traces.

## Pre-distribution checklist

Answer each before recommending a distributed style:

- [ ] Production round-trip latency known: average, p95, p99 (fallacy 2).
- [ ] Longest synchronous call chain per key workflow, and its latency budget (2).
- [ ] Timeout, retry, and circuit-breaker policy defined (1).
- [ ] Largest interservice payloads versus fields actually used; request rates (3).
- [ ] Endpoint-level authentication and authorization for internal calls (4).
- [ ] Channel with network and ops teams for topology changes; latency drift alerts (5, 6).
- [ ] Infrastructure cost estimate: gateways, proxies, subnets, extra servers (7).
- [ ] Vendor and network heterogeneity known risks (8).
- [ ] Contract versioning policy covering scope, reach, count, deprecation (9).
- [ ] Failure path for failed compensations (10).
- [ ] Tracing, correlation IDs, and centralized logs from day one (11).

Use `scripts/call_chain_budget.py` to turn the latency, availability, and payload items into numbers.

## Invented worked example

A team proposes splitting a checkout flow into six services called in sequence. Measured: 40 ms average, 250 ms p95 per hop, 99.9 percent availability per service. Checkout must finish in under 800 ms.

- Average chain: 6 x 40 = 240 ms, inside budget.
- If every hop hit its p95 simultaneously: 1,500 ms, nearly double the budget. More realistically, about 26 percent of checkouts (1 - 0.95^6) hit at least one tail-latency hop.
- Availability of the chain: 0.999^6, about 99.4 percent, versus 99.9 percent for one deployment.
- Recommendation: collapse the synchronous chain (merge services or make non-critical steps asynchronous) before accepting the design, and record the measured numbers in the ADR.
