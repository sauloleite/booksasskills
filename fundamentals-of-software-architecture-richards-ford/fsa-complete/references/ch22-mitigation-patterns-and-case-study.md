# Mitigation Patterns and Case Study

## Contents
- The chapter's case in brief
- Session 1: availability
- Session 2: elasticity
- Session 3: security
- Lessons from the case
- Mitigation pattern catalog
- SLA and SLO quick facts
- Invented practice example

## The chapter's case in brief

A telephone and web health-advice service: nurses answer calls and guide patients with help from a third-party diagnostics engine (capacity around 500 requests per second); patients can also use a self-service website that hits the same engine. Scale: a few hundred concurrent nurses, potentially hundreds of thousands of concurrent self-service users, large surges during outbreaks and flu season. Medical records come from an external exchange and, for regulatory (HIPAA) reasons, only nurses may see them. Calls are routed by nurse skills (language, specialty).

The initial design: three web UIs (self-service, nurse, admin), call-intake and skill-based routing services, one shared database, and one API gateway doing security checks in front of case management, nurse profiles, the records-exchange adapter, and the diagnostics-engine adapter. Mostly REST internally. Critical characteristics: availability, elasticity, security. The architect considered it ready, then ran three single-criterion risk-storming sessions anyway.

## Session 1: availability

Findings:
- Shared database: impact 3, likelihood 2, score 6. If it fails, nurses could keep notes on paper, but call routing stops.
- Diagnostics engine: impact 3, likelihood unknown so rated 3, score 9.
- Records adapter: score 2, because records are not needed to reach a diagnosis.
- Everything else: no risk, since services run as multiple instances and the gateway is clustered.

Mitigations:
- Split the one database by availability need: a clustered store for nurse profiles (needed for routing) and a single-instance store for case notes. Side benefit: case notes are now isolated, which helps security.
- For the third-party systems, which the team cannot change, look up their published SLAs or SLOs. Both had SLAs (four nines for diagnostics, three nines for records), which was enough evidence to drop those risks. The SLA figures were then written onto the architecture diagram.

## Session 2: elasticity

Self-service traffic, not nurses, drives load on the diagnostics engine, and outbreaks multiply it. Everyone rated the engine adapter 9: a fixed 500 requests per second ceiling behind synchronous REST cannot absorb that surge.

Mitigations were layered, each closing a gap the previous left:
1. Asynchronous messaging between the gateway and the engine adapter, giving a backpressure point. Gap: callers still wait and time out.
2. Two channels instead of one (the Ambulance pattern), so nurse requests take priority over self-service. Gap: wait times still long.
3. A dedicated outbreak cache service answering the common outbreak-related question flows, so most surge requests never reach the engine, freeing its capacity for other symptoms.

Without the session, the bottleneck would likely have surfaced only during the first heavy flu season.

## Session 3: security

The architect believed gateway authentication and authorization made records access safe and rated it 2. Every other participant rated the shared gateway 6 (impact 3 if admin staff or the public reach records, likelihood 2 because all user types share one entry point despite per-call checks). They persuaded the facilitator. Mitigation: one gateway per user type (nurse, admin, self-service), so non-nurse traffic has no network path to the records adapter at all.

## Lessons from the case

- A design that passed many reviews still changed substantially in three areas.
- Single-criterion sessions surface different risks from the same diagram.
- The facilitator can be the one who is wrong; consensus must be genuine.
- Mitigation is often iterative: each fix exposes a residual risk.
- Structural isolation (separate stores, separate gateways) can beat stronger checks inside a shared component.
- External dependencies are mitigated with evidence (contracts, published objectives) rather than redesign.

## Mitigation pattern catalog

| Risk shape | Mitigation | Watch for |
|---|---|---|
| Shared store, mixed availability needs | Split by domain or by availability requirement; cluster only the critical part | Cross-store consistency |
| Expensive full redundancy rejected | Partial split or domain-based partitioning | Residual risk must be explicitly accepted |
| Fixed-capacity downstream, synchronous calls | Queue for backpressure | Latency and timeouts remain |
| Mixed-priority traffic to a scarce resource | Separate channels per priority (Ambulance pattern) | Starvation of low-priority traffic |
| Surge of repetitive requests | Cache or precompute the hot subset in front of the bottleneck | Cache staleness, invalidation |
| Multiple user classes, one entry point | Separate gateways or entry points per class | More infrastructure to operate |
| Third-party dependency | Find SLA (contractual) or SLO (non-binding) and compare to need; add fallback if insufficient | An SLO is a promise, not a guarantee |
| Unknown technology | Replace with a known one, or train/spike before relying on it | Schedule cost of learning |

## SLA and SLO quick facts

- SLA: usually legally binding contract. SLO: usually a target without legal force.
- Downtime per year: 99.9% is about 8.77 hours; 99.99% about 52.6 minutes; 99.999% about 5.26 minutes.
- Compare the allowed downtime against the business consequence; if the dependency's budget exceeds what the business tolerates, the risk stands. `scripts/risk_storm.py downtime <pct>` does the conversion.

## Invented practice example

A ticketing platform expecting a major concert on-sale runs an elasticity session. Notes: seat-inventory service 9 (two people), 6 (one); payment provider: one person scores 9 because they do not know the new provider's API; queue-based waiting room: all score 2.

- Waiting room: agreed, skip.
- Seat inventory: discuss; the 6 assumed autoscaling, the 9s point out the single write-primary database. Consensus 9.
- Payment provider: automatic 9 as unknown technology. Options: spike integration this sprint, or keep the previous provider for this event.
- Mitigation proposals: partition seat inventory by venue section (cost estimate attached), priority channel for checkout over browsing, cache static event pages. The product owner approves partitioning and caching, defers the provider switch. Updated diagram and assessment are published, and a follow-up session is scheduled for after the event.
