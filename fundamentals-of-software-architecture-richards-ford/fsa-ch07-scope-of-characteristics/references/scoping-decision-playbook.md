# Scoping decision playbook: from characteristics to style, boundaries, data and communication

## Contents
- The scoping decision sequence
- Step details and criteria
- Worked kata: Going Green (analysis in our own words)
- Second worked example (invented)
- Scoping in the cloud
- Pitfalls
- Review questions

## The scoping decision sequence

The chapter frames style selection as a short decision tree driven by characteristic scope. In prose:

1. **How many characteristic sets?** Can the system succeed with one set, or does it need several groups that differ?
2. **One set: monolith.** Pick a monolithic architecture. Persistence is a single monolithic database developed and deployed in lockstep with the application. Then choose among monolithic styles. Done.
3. **Several sets: distributed.** Determine quantum boundaries (granularity).
4. **Choose persistence** for the distributed system: one shared database (common in event-driven systems) or data partitioned along service granularity (microservices).
5. **Choose communication** between quanta: synchronous or asynchronous.
6. **Loop back**: synchronous communication can alter the quantum boundaries drawn from static coupling in step 3; the two kinds of coupling interact, so re-check.

## Step details and criteria

**Step 1, counting sets.** Do the characteristic analysis per capability area, not for the system as a whole. Signals that you need more than one set:
- Some areas face the public with spiky load while others are internal and steady.
- Some areas are governed by audit, security or integrity rules that slow change, while others must change weekly.
- Characteristics pull against each other (fast deployability vs heavy auditability; extreme scalability in the UI vs modest scale in back-office).
If one set clearly covers everything without painful compromises, stop and go monolithic; it removes most downstream decisions.

**Step 3, quantum boundaries.** Let each cluster of agreeing characteristics suggest a quantum. This is a starting point for granularity, not the final answer (the book revisits granularity drivers in its microservices chapter). Validate each quantum with the tests in the coupling reference.

**Step 4, persistence.** A shared database keeps data consistency simple but makes its sharers one static quantum; per-quantum databases enable distinct characteristics but bring distributed data concerns. Choose consciously: if you share, accept that the sharers' operational characteristics converge on the database's.

**Step 5, communication.** Default to async across quanta with mismatched operational profiles; keep sync where an immediate answer is essential and both ends can be given compatible targets.

## Worked kata: Going Green (analysis in our own words)

Scenario: a company buys used electronics (phones and similar) from the public through both street kiosks and a website running the same system. A customer enters model and condition, receives a bid, and if accepted either drops the device in a kiosk or ships it in a mailer box. The company inspects the device, pays the customer, then decides whether to resell or recycle it, and runs reporting and analytics.

Characteristic analysis reveals three clusters:

| Area | Characteristics it needs | Why |
|---|---|---|
| Public-facing (kiosk, web, bidding) | Scalability, availability, agility | Unpredictable public demand; must be up when customers are |
| Back office (payments, accounting, reporting) | Security, data integrity, auditability | Money and records |
| Device assessment | Maintainability, deployability, testability (together: agility) | New device models appear constantly; the faster assessment rules ship, the sooner high-value newer devices can be bought and resold |

The assessment cluster is the instructive one: it is driven by the business model, not by a technical concern. Profit depends on reselling the most valuable devices, and those are the newest, so speed of change is a revenue lever.

Could one architecture satisfy all eight characteristics at once? Possibly, but with great difficulty: several conflict (rapid deployment fights strict auditability; UI-grade scalability is wasted on the back office). The better move is to use the three clusters as three quanta, each with its own characteristic set, and treat that as the first approximation of service granularity.

## Second worked example (invented)

A clinic network wants online appointment booking, clinical records, and a nightly claims export to insurers.
- Booking: public, peaky on Monday mornings: scalability, availability, responsiveness.
- Clinical records: regulated: security, integrity, auditability, privacy.
- Claims export: batch: reliability, recoverability; scalability irrelevant.

Three sets, so distributed. Tentative quanta: Booking, Records, Claims. Persistence: Records must own its store (regulatory isolation); Booking keeps its own slot store; Claims reads a replicated extract. Communication: Booking confirms appointments without a sync call to Records (publishes an event that Records consumes), so a Records maintenance window never blocks booking. Re-check: no sync edge links mismatched profiles, so three quanta stand.

Counter-case: a small practice with one clinic, low traffic and one admin team. A single characteristic set (security, integrity, modest availability) covers everything; a modular monolith on one database is the right answer.

## Scoping in the cloud

Cloud platforms package many operational characteristics, so the scope analysis must include the platform. Two deployment models need different questions:

**Cloud as a container host.** The cloud acts as a remote operations center running orchestrated containers. Evaluate the characteristics of the containers themselves and the constraints imposed by the orchestrator (for example Kubernetes: scheduling, scaling policies, resource limits, networking, upgrade behavior).

**Cloud services as building blocks.** The application is assembled from provider primitives (triggered functions, managed databases, queues, storage). Here the quantum's characteristics largely come from what each service advertises, so check documented limits and SLAs and whether the provider actually meets them; design around quotas, cold starts, throttling and regional availability.

Perspective: features that are now configuration switches, such as elasticity, were once hard engineering problems on physical hardware. Those are easier today, but new trade-offs replace them: dependence on provider availability, a broader security surface, and limits you do not control. Specifics change; the job of analyzing trade-offs does not.

## Pitfalls
- Running one characteristic analysis for the whole system and averaging the result.
- Going distributed when one characteristic set would suffice.
- Splitting into services but sharing one database, then expecting per-service characteristics.
- Fixing quantum boundaries before deciding communication, and never revisiting them.
- Assuming a managed cloud service's characteristics without checking its limits.

## Review questions (our own)
1. For each proposed service, which characteristics apply only to it, and which are shared?
2. Which data stores or libraries are shared, and which quanta do they merge?
3. Which synchronous edges cross between quanta with different scalability or availability targets?
4. What would make a single characteristic set sufficient, and is that true here?
5. Which characteristics are delegated to a cloud provider, and how are they verified?
