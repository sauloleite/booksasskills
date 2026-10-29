# Building an Aggregate DPQ: Worked Example and Fitness Functions

## Contents
- What the chapter's story illustrates
- Worked example: a demand forecasting DPQ
- Completeness contract: all or nothing per period
- Fitness functions
- ADR template for a DPQ decision
- Design checklist

## What the chapter's story illustrates

The chapter's closing story shows a team that already attaches a DPQ to every new service, with an aggregate DPQ for its ticket domain, using those existing products to feed a new ML-driven aggregate product. It also shows the platform and governance pieces in operation, and ends with a rule that a trend-oriented consumer should receive whole days of data or nothing, enforced by fitness functions.

## Worked example: a demand forecasting DPQ

Invented scenario: a home appliance repair network wants weekly forecasts of technician demand by region and skill.

Existing source-aligned and aggregate DPQs:
- **Work Orders DPQ** (aggregate across intake and dispatch services): history of opened and closed jobs with region, appliance type, duration.
- **Technician Roster DPQ** (source-aligned to the HR profile service): daily snapshot of technician skills, certifications, home region.
- **Customer Feedback DPQ** (source-aligned to the feedback service): event log of ratings and comments, with PII stripped by policy.

New product:
- **Technician Demand DPQ** (fit-for-purpose, ML oriented), owned by the planning domain. It subscribes asynchronously to the three inputs, trains a forecasting model, and publishes a daily "staffing recommendations" data set.

Steps an agent should walk through:
1. Confirm each input DPQ already exposes the needed output port; if not, the owning domain team adds it (not the planning team).
2. Choose async subscription for all inputs; the model only refreshes daily, so synchronous queries add load without benefit.
3. Define consumer-side contracts loosely: depend on the minimal fields needed (region, skill, timestamps, counts), tolerate extra fields, and version explicitly.
4. Declare governance: feedback text is excluded, technician identifiers are pseudonymized by the sidecar before data leaves the roster product.
5. Define the completeness rule and fitness functions (below).
6. Register the product with the platform so others can discover it and see its lineage.

## Completeness contract: all or nothing per period

Trend and forecasting consumers are distorted more by partial data than by missing data. A day with half its events looks like a demand drop and corrupts the trend; an empty day can simply be excluded.

Rule: each source must deliver a complete snapshot for a period or deliver nothing for it; incomplete periods are flagged as exempt and excluded from training and trend analysis.

Consequence to record: if too many periods become exempt (for example, due to source outages), forecast accuracy degrades. Track the exempt ratio and alert when it crosses an agreed limit.

Keep the contracts between feeds and the aggregate loosely coupled so this rule does not make the pipeline brittle.

## Fitness functions

1. **Arrival-gap completeness check.** Inspect timestamps of incoming messages. Choose a gap threshold from the feed's normal volume (for a busy feed, a gap above about one minute is suspicious). Any gap above the threshold marks the period as exempt. Run continuously or at period close. The bundled script `scripts/daily_completeness_check.py` implements this check over a list of timestamps.
2. **Consumer-driven contract test.** The aggregate DPQ publishes its expectations of each source DPQ (fields, types, semantics); each source runs those tests in its own build so internal evolution in the source domain cannot silently break the consumer.
3. **Async-only propagation check.** Verify that no operational service calls its DPQ synchronously on the request path, for example by inspecting dependency declarations or tracing data.
4. **Exempt-ratio threshold.** Fail or alert if exempt periods over a rolling window exceed the tolerance agreed in the ADR.

Minimal sketch of a consumer-driven contract assertion:

```python
REQUIRED = {"job_id": str, "region": str, "skill": str,
            "opened_at": str, "closed_at": (str, type(None))}

def check_contract(sample_records):
    for rec in sample_records:
        for field, typ in REQUIRED.items():
            assert field in rec, f"missing {field}"
            assert isinstance(rec[field], typ), f"bad type for {field}"
    # Extra fields are allowed: loose coupling on purpose.
```

## ADR template for a DPQ decision

- **Title:** short imperative statement of the decision.
- **Context:** consumer need, input DPQs, freshness and consistency needs, sensitivity of data.
- **Decision:** DPQ type, owner, input mode (async or sync), contract style, completeness rule.
- **Consequences:** costs (contract coordination, eventual consistency), risks (exempt periods, stale inputs), what would trigger revisiting.
- **Fitness functions:** each with what it measures, threshold, and where it runs.

## Design checklist

- Owner is the domain team closest to the data, not a central team.
- Type chosen deliberately: source-aligned, aggregate, or fit-for-purpose.
- Published contract independent of the service's internal schema.
- All service-to-DPQ propagation async and eventually consistent; no shared transaction.
- Governance policies (access, PII, quality) enforced by the platform sidecar.
- Discoverable via the platform, with lineage recorded.
- Completeness and freshness expectations explicit, with fitness functions.
- Consumer-driven contract tests in place for every input.
