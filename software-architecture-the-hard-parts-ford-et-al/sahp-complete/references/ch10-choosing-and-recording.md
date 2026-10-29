# Choosing a Read-Access Pattern and Recording the Decision

## Contents
- Elimination rules
- Hypothesis-based trade-off session
- Worked examples (invented)
- ADR template
- What the chapter story illustrates

## Elimination rules

Work through hard constraints first; each one removes candidates.

| Constraint observed | Removes |
|---|---|
| Owner is unreliable, or per-request latency budget is tight, or reader is called very often | Inter-service communication |
| Reader must see changes immediately and consistently | Column schema replication |
| Data is large (cache over roughly 500 MB, or memory x instances unaffordable) | Replicated caching |
| Data changes very frequently | Replicated caching (and strains column replication) |
| Reader already bound to another shared schema and cannot connect to a second; or services are in unrelated business domains; or some data must be hidden from the reader | Shared data domain |
| Cloud or container network blocks peer discovery and cannot be changed | Replicated caching |
| Referential integrity, views, procedures or triggers across the two tables must be kept | Favors shared data domain |
| Reporting or aggregation over large historical sets | Favors column schema replication |

Also check whether the two services should simply be consolidated; if they belong to different domains, that is off the table.

Fallback ordering when several survive: prefer the option that keeps a single writer and a narrow contract (remote call or replicated cache) unless performance or volume forces otherwise; reach for a shared domain when consistency and integrity dominate; use column replication sparingly.

## Hypothesis-based trade-off session

1. Present all options with their trade-offs to the deciding group.
2. Apply the elimination rules and agree on the survivors.
3. The architect proposes one survivor as a hypothesis.
4. The group tries to find its negatives. Facilitators may hold back a known weakness so the team discovers it, which builds shared understanding.
5. For each negative, compare against the alternative (for example, a startup dependency on the owner is still better than a permanent runtime dependency on the owner).
6. Turn unknowns into tasks: PoC of the technique, licensing research, environment limits (zones, firewalls).
7. Get approval, then write the ADR.

## Worked examples (invented)

**A. Shipping service needs carrier names.** 300 carriers, 500 bytes each, edited monthly, owner 2 instances, shipping up to 8. Cache size 150 KB, total about 1.5 MB. Reads happen on every shipment. Decision: replicated cache. Negatives: startup dependency, product license, team inexperience. Mitigations: readiness gate, PoC.

**B. Billing needs current account balances from Ledger.** Values change constantly and must be exact. Replicated cache fails on update rate; column replication fails on consistency. Data domain blocked because Ledger is a separate regulated domain and must hide other columns. Decision: inter-service call with batching, a tight timeout and a clear contract; accept availability coupling and scale Ledger with Billing.

**C. Claims service needs policy coverage rules with foreign keys and a validation trigger.** Data is large (tens of GB) and the policy service has poor uptime. Cache fails on volume, remote calls fail on reliability, column replication fails on consistency. Decision: shared data domain for policy and claim tables. Consequences: schema changes need sign-off from both teams; add database roles limiting claims to the needed tables.

**D. Analytics service builds monthly sales reports.** Large volumes, latency tolerant on freshness, needs local joins. Decision: column schema replication fed by an event stream, with read-only enforcement and a nightly reconciliation.

## ADR template

```
Title: <Pattern> for <reader> read access to <owner data>
Context: <reader> needs <fields> owned by <owner>, read <frequency>,
  ~<rows> rows, ~<bytes> each, changes <rate>, consistency need <level>.
  Options considered: inter-service call, column replication,
  replicated cache, shared data domain.
Decision: Use <pattern>. <owner> remains sole writer.
  Rejected <x> because <constraint>; rejected <y> because <constraint>.
Consequences: <startup ordering / license cost / schema change
  coordination / staleness window / security exposure>; mitigations.
```

## What the chapter story illustrates

A ticket assignment component reads expert profiles many times per decision, after those profiles moved to a different service. Rewriting the algorithm or switching to messaging does not help, and a shared domain is ruled out, so the team weighs remote calls against a replicated cache, sizes the small static dataset across peak instances, and chooses the cache while noting the startup dependency and licensing cost.
