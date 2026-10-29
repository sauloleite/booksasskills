# Deployment Readiness, Quality Gates and Rollout

Production readiness is a holistic judgment, not a green test run: can the system do its job safely, consistently and efficiently with real users?

## Step 1: write deployment criteria before you need them

Typical criteria:
- Quantitative thresholds on the relevant eval sets (per hero scenario, not only overall).
- Stability under stress and edge cases.
- All core workflows passing end-to-end integration tests.
- Latency and uptime targets met.
- No open critical or high-severity bugs.
- A structured checklist confirming that tools, planning, memory, learning and integrations were each tested and reviewed.

Example threshold set for a support agent (the 95% tool-recall figure is the chapter's illustration; the others are invented to show the shape):

| Gate | Threshold |
|---|---|
| Tool recall on refund and cancellation slices | at least 0.95 |
| Regression on any multiturn slice (for example address changes) | none allowed |
| Forbidden tool calls (refund on non-qualifying order) | zero |
| p95 latency | under the current human-handled baseline |
| Critical or high-severity bugs | zero open |

## Step 2: enforce with gates

A gate blocks promotion until its requirement is met. Kinds:
- **Automated**: fail the pipeline if any regression appears on the latest eval suite, or a threshold is missed.
- **Manual**: explicit sign-off by technical and product leads after a pilot or beta.
- **Escalation**: when automated results are ambiguous (a small drop inside noise, a judge disagreement), route to a human instead of auto-passing or auto-failing.

Practical rules for regression gates:
- Compare per slice against the last released baseline, not only the global mean.
- Decide the allowed drop in advance; with small slices use a confidence interval rather than a raw difference, because a few cases swing the rate a lot.
- Store each release's summary so the baseline is reproducible.

## Step 3: roll out, watch, be ready to roll back

- Release to a pilot group first and monitor for real-world variation that offline sets missed.
- Monitor for regressions after launch with the same metrics used offline, so numbers are comparable.
- Keep rollback fast and rehearsed; the confidence to ship quickly comes from strong offline evaluation plus a cheap way back.
- Feed every production incident back into the eval set as a new case, closing the loop.

## Closing principles from the chapter

- Clear objectives and well-chosen metrics are the base; error analysis turns failures into targeted fixes.
- Evaluate in tiers: components, then integrated system, then real users.
- Refine metrics and eval sets iteratively as user needs change.
- Gates and readiness checks build a culture of accountability: only systems that meet the bar reach users.

## Pre-release checklist

- [ ] Criteria written, versioned and agreed by engineering and product.
- [ ] Full component and end-to-end suites green; no slice regressed beyond the agreed margin.
- [ ] Forbidden-action and safety (leakage, policy) tests at zero violations.
- [ ] Latency, cost and uptime within targets under load tests.
- [ ] Pilot completed and signed off; ambiguous results reviewed by a human.
- [ ] Rollback path tested; post-launch dashboards mirror offline metrics.
