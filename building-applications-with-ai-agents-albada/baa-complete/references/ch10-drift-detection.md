# Detecting and Responding to Distribution Shift

## Contents
- What shifts and how it shows up
- Choosing a statistic
- Thresholds cheat sheet
- Formulas and implementation notes
- Operational indicators
- Response playbook
- Pitfalls

## What shifts and how it shows up

The agent's environment changes over time: user vocabulary, new product terms, altered API responses, a silently updated foundation model. Shifts rarely throw errors. They show up as lower success, misaligned answers and more fallbacks. Monitoring is the first line of defense; dashboards of success rate, tool failures, token trends and hallucination frequency give the early hint, and statistical tests confirm it.

## Choosing a statistic

| Data shape | Statistic | Example inputs |
|---|---|---|
| Continuous numeric, unknown distribution | Two-sample Kolmogorov-Smirnov (KS) | Query length, latency, token counts |
| Probability or frequency vectors | Kullback-Leibler (KL) divergence | Token or word frequencies, topic mixes |
| Categories or binned numerics | Population Stability Index (PSI) | Tool or intent mix (refund, cancel, modify) |
| Semantic content | Mean cosine similarity of embeddings to baseline | Query embeddings |

## Thresholds cheat sheet

Chapter defaults; recalibrate per system.
- **KS**: statistic above 0.1, ideally together with p below 0.05.
- **KL**: above 0.5 suggests concept change. (The triage tree uses under 0.2 as the band of normal variation.)
- **PSI**: under 0.1 stable; 0.1 to 0.25 minor drift, monitor; above 0.25 major drift, intervene.
- **Embeddings**: mean similarity to baseline under 0.8 triggers review. Tools such as Evidently AI can automate this and feed Grafana alerts.

## Formulas and implementation notes

- **KS** = maximum vertical gap between the two empirical CDFs; nonparametric, no normality assumption. With tiny samples the statistic jumps in coarse steps (with n=4 per side the smallest nonzero value is 0.25), so a 0.1 cutoff alone fires on noise. Require a p-value and a minimum sample size.
- **KL(P||Q)** = sum of P(i) * ln(P(i)/Q(i)), with P the historical baseline and Q current. Asymmetric: KL(P||Q) differs from KL(Q||P); pick a direction and keep it. Add a small epsilon before normalizing to avoid log of zero.
- **PSI** = sum over buckets of (actual% - expected%) * ln(actual% / expected%), expected = baseline, actual = current. Symmetric in effect, always non-negative. Zero buckets need an epsilon floor; use the same bucket edges for both periods (deciles of the baseline are common for continuous data).

Compact original implementation:

```python
import math
def _norm(xs, eps=1e-6):
    xs = [max(x, 0) + eps for x in xs]
    s = sum(xs)
    return [x / s for x in xs]

def psi(baseline_counts, current_counts):
    e, a = _norm(baseline_counts), _norm(current_counts)
    return sum((ai - ei) * math.log(ai / ei) for ai, ei in zip(a, e))

def kl(baseline_counts, current_counts):
    p, q = _norm(baseline_counts), _norm(current_counts)
    return sum(pi * math.log(pi / qi) for pi, qi in zip(p, q))
```

Run `scripts/drift_check.py` for a tested CLI version that also computes KS.

## Operational indicators

Business-level symptoms that warrant a drift investigation:
- Accuracy falls more than 5 to 10% within a rolling 24 hours.
- Abandonment rises above 15%.
- Retries appear in more than 20% of sessions.

## Response playbook

1. Confirm with the matching statistic and check whether the change persists.
2. Export degraded traces for analysis to separate transient from systemic causes.
3. **Transient**: retune thresholds, fix parsing logic.
4. **Persistent**: adapt to the new API, rework workflows, retrain or fine-tune. Rule of thumb: prioritize retraining when PSI stays above 0.25 for 48 hours.
5. Validate the fix with an A/B test before declaring victory.

## Pitfalls

- Treating drift as an incident only when errors appear; most drift is silent.
- Comparing windows of very different size or seasonality (weekday versus weekend).
- Recomputing bucket edges on the current window, which hides the shift.
- Forgetting that a provider-side model update is also a distribution shift: pin and log model versions in spans.
