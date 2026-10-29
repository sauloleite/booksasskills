---
name: fsa-ch22-analyzing-risk
description: Applies Chapter 22 of Richards and Ford's "Fundamentals of Software Architecture" (2nd ed.) on analyzing architecture risk. Covers the impact x likelihood risk matrix, risk assessments by characteristic and domain with totals, filtering and trend direction, three-phase risk storming (identification, consensus, mitigation), unknown-technology scoring, cost-versus-risk negotiation, user-story risk and mitigation patterns. Use when scoring a risk, building a risk report, facilitating or aggregating a risk-storming session, or proposing mitigations.
---

# Analyzing Architecture Risk (FSA Chapter 22)

## Purpose

This skill helps an agent turn vague worries about an architecture into quantified, prioritized, discussable risks and then into costed mitigations the business can approve. It covers operational risk (availability, elasticity, data integrity, security) and structural risk (such as coupling decay), scored with a two-axis matrix, summarized in a criteria-by-context assessment, and discovered collaboratively through risk storming. The chapter's central claim: risk scoring is subjective, so make it numeric, gather many independent views, and repeat it throughout the system's life.

## Key decision rules (apply even without opening references)

1. **Score = impact x likelihood**, each low 1, medium 2, high 3. Bands: 1 to 2 low, 3 to 4 medium, 6 to 9 high. Keep both factors, not just the product.
2. **Judge impact first, likelihood second.** Existing safeguards (clustering, failover, headroom) lower likelihood, never impact.
3. **Unknown likelihood counts as 3** until evidence says otherwise.
4. **Unknown or unproven technology scores 9 automatically.** Treat a participant not knowing a technology as a finding: swap the technology or fund training.
5. **Assess against the critical characteristics only.** Rows are the few characteristics the system must deliver; columns are domains or subdomains, not individual services (service granularity misses inter-service risk).
6. **Read row and column totals separately:** rows say which quality is most exposed, columns say which part of the system is.
7. **Filter for stakeholders:** show only high cells to them; keep the full grid for the team.
8. **Show direction** (rising, falling, steady) from fitness-function measurements, always with a legend. A snapshot is not a trend.
9. **Risk storming has three phases:** individual identification, collaborative consensus, collaborative mitigation. The individual phase must happen alone to avoid anchoring.
10. **Invite senior developers and tech leads**, not just architects. They add implementation knowledge and learn the architecture.
11. **One criterion or one context per session.** If several are mixed, label every note with its criterion and discuss each separately.
12. **In consensus, skip unanimous areas;** spend time on divergent scores, areas only one person flagged (often the most valuable), and unknown-technology flags. Either side may change its mind.
13. **Mitigation costs money, so a stakeholder with budget authority decides** whether the cost is worth the risk reduction. If the full fix is rejected, offer a cheaper partial one.
14. **Third-party risk is mitigated with evidence:** check for an SLA (usually binding) or SLO (usually not) and compare its downtime budget to business need.
15. **Repeat continuously:** after major features, at iteration ends, before demand peaks, or when trends worsen.

## Default workflow

1. Confirm the system's critical characteristics and its domain partitioning.
2. Score known concerns with the matrix (rules 1 to 4) to seed an assessment.
3. Plan a risk-storming session on one criterion; send the current diagram, scope and logistics.
4. Collect independent scores; aggregate them (script `storm`) to separate agreed, divergent, lone and unknown-tech areas.
5. Facilitate consensus on the non-agreed areas, factor by factor.
6. Propose mitigations with cost and residual risk; take them to a decision-maker; record the outcome (an ADR fits well).
7. Update the diagram and the assessment (script `assess`), add direction from fitness functions, and set the trigger for the next session.

## References

- [references/risk-matrix-and-assessment.md](references/risk-matrix-and-assessment.md): read when scoring a single risk, building or presenting a criteria-by-context assessment, filtering it for stakeholders, or adding trend direction.
- [references/risk-storming-playbook.md](references/risk-storming-playbook.md): read when planning, facilitating or reviewing a risk-storming session, resolving disagreements, negotiating mitigation cost, setting cadence, or scoring user-story risk in grooming.
- [references/mitigation-patterns-and-case-study.md](references/mitigation-patterns-and-case-study.md): read when choosing mitigations for availability, elasticity, security or third-party risk, or when you need a worked end-to-end example.
- [references/source-map.md](references/source-map.md): read to see which reference covers each chapter section.

## Scripts

- Run `python3 scripts/risk_storm.py score --impact 3 --likelihood unknown` (or `--unknown-tech`) to compute a single risk score and band.
- Run `python3 scripts/risk_storm.py storm notes.csv [--participants a,b,c] [--json]` to aggregate phase-1 notes (CSV: participant, area, criterion, impact, likelihood[, note]) into agreed, divergent, lone and unknown-tech areas, ordered for discussion; it warns when criteria are mixed.
- Run `python3 scripts/risk_storm.py assess grid.csv [--high-only] [--json]` to build the assessment table (CSV: criterion, context, score[, previous]) with row and column totals, highest-risk criterion and context, and direction markers.
- Run `python3 scripts/risk_storm.py downtime 99.95` to convert an SLA or SLO availability percentage into allowed downtime per year, month and week.
