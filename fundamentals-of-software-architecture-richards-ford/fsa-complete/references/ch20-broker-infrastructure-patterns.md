# Infrastructure Patterns: Single Broker vs Domain Broker

## Contents
- Why infrastructure is a coupling concern
- Topic ownership in event choreography
- Single-Broker pattern
- Domain-Broker pattern
- Decision guide
- Worked example
- Pitfalls

## Why infrastructure is a coupling concern

Architects track coupling between components, data, and APIs, and the same lens applies to shared infrastructure. Patterns exist wherever teams repeatedly solved a problem in context, and infrastructure patterns frequently intersect with the wider engineering ecosystem (deployment, operations, team structure). The book names this pattern both "Broker-Domain" and "Domain-Broker"; they are the same thing.

## Topic ownership in event choreography

In an event-driven workflow (the chapter uses order placement), processors subscribe to events published by others, and brokers deliver them. The default convention is that the producer owns the topic or queue: consumers such as a payment processor must know the producer's channel address in order to subscribe. Consequence: the broker hosting that channel is part of the producing service's infrastructure footprint, and every subscriber depends on it.

## Single-Broker pattern

All services in the workflow (or the whole system) use one broker.

Strengths
- Centralized discovery: every processor knows where to find every channel.
- Least infrastructure to provision and run.
- One place for logging, monitoring and governance of messaging.

Weaknesses
- Fault tolerance: if the broker fails, the whole workflow halts, which undercuts a key motive for going distributed.
- Throughput: all traffic shares one broker, which can saturate as volume grows.

## Domain-Broker pattern

Infrastructure is partitioned at the same granularity as the domains: each cluster of related services shares its own broker, mirroring the system's domain partitioning.

Strengths
- Better isolation: a broker failure or overload stays inside one domain.
- Aligns infrastructure with domain boundaries, which also aligns with team ownership.
- Improves scalability, elasticity and other operational characteristics.
- Discovery remains reasonable within a domain.

Weaknesses
- Cross-domain discovery of topics and queues becomes harder.
- More brokers cost more money.
- More moving parts to patch, monitor and secure.

Neither option is a best practice; the choice balances ease of discovery against domain isolation.

## Decision guide

| Signal | Leans toward |
|---|---|
| Small system, few domains, modest message volume | Single broker |
| Strong need for central messaging governance with a small ops team | Single broker |
| Workflow outage on broker failure is unacceptable | Domain brokers |
| Message volume growing toward broker limits, or bursty domains | Domain brokers |
| Teams aligned to domains and owning their infrastructure | Domain brokers |
| Tight infrastructure budget | Single broker |

Mitigations that soften each side:
- Single broker: cluster it for high availability and capacity, but note that this reduces rather than removes shared fate (a misconfiguration or upgrade still hits everyone).
- Domain brokers: publish a channel catalog (registry of topics, owners and schemas), standardize broker configuration as code, and route cross-domain events through clearly owned bridge topics.

Questions to ask before deciding:
1. Which domains must keep running if another domain's messaging fails?
2. What is the projected peak message rate per domain over the next 18 months?
3. Who will operate each broker, and do they have the skills and budget?
4. How will a consumer in domain A discover and get access to a topic owned by domain B?

## Worked example

A retailer has order, inventory, payment and shipping services on one broker. A Black Friday surge in inventory events saturates it, delaying payment confirmations.

Option analysis: scaling the shared broker treats throughput but keeps shared fate. Domain brokers (Order plus Payment in a "checkout" broker, Inventory alone, Shipping alone) isolate the inventory burst, at the cost of three brokers to operate and a catalog for cross-domain topics like "order placed". Recommendation: domain brokers for checkout and inventory, since those have the divergent load profiles; keep shipping on the checkout broker until its volume justifies a split. Record that discovery is now catalog-dependent and assign an owner for the catalog.

## Pitfalls

- Choosing a single broker for convenience and only discovering the shared-fate risk during an outage.
- Splitting brokers along technical lines (by message type) instead of domain lines, which gains cost without the isolation benefit.
- Creating domain brokers with no discovery mechanism, so teams hard-code addresses and recreate coupling.
- Ignoring that producer-owned topics make consumers depend on the producer's infrastructure availability.
