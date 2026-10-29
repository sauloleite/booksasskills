# Risk Matrix and Risk Assessments

## Contents
- Why quantify risk
- The two-axis risk matrix
- Scoring procedure and rules
- Building a risk assessment
- Reading totals and choosing priorities
- Filtering for an audience
- Adding direction (trend)
- Pitfalls
- Review questions

## Why quantify risk

Architecture risk comes in two flavors: operational (availability, scalability, data integrity and similar runtime concerns) and structural (for example, static coupling between logical components that slowly decays the design). Left as opinion, "this part is risky" turns into an argument between architects who weigh the same thing differently. A simple numeric scheme does not remove judgment, but it forces each person to separate two questions and makes disagreements visible and discussable.

## The two-axis risk matrix

Rate each concern on two axes, each with three levels:

| Level | Value |
|---|---|
| Low | 1 |
| Medium | 2 |
| High | 3 |

Risk = impact x likelihood. The only possible products are 1, 2, 3, 4, 6 and 9 (5, 7 and 8 cannot occur).

Bands:
- 1 to 2: low (conventionally green)
- 3 to 4: medium (yellow)
- 6 to 9: high (red)

Accessibility note: pair each color with a pattern, shade or the number itself so the chart still works in grayscale and for color-blind readers.

## Scoring procedure and rules

1. **Impact first.** Ask what happens to the business and users if this concern materializes, ignoring how probable it is. Fixing impact first keeps the likelihood debate from bleeding into the severity judgment.
2. **Likelihood second.** Now consider existing safeguards: clustering, redundancy, proven operating history, load headroom.
3. **Unsure of likelihood? Rate it high (3)** until evidence lowers it. Uncertainty is itself a risk.
4. **Unknown or unproven technology gets 9 outright.** If a participant does not know the technology, or it has no track record in your context, the matrix cannot be applied meaningfully, so the area is treated as maximum risk until training, a spike, or a substitution changes that.
5. Record the two factors, not just the product, so later discussions can target the factor in dispute.

Example (invented): a payment-token vault is central to checkout, so impact is high (3). It runs as an active/passive pair with automated failover that has been exercised in production, so likelihood is low (1). Risk = 3, medium. The same vault without tested failover would be likelihood 2, risk 6, high.

## Building a risk assessment

A risk assessment is a summary report of overall architecture risk laid out as a grid:

- **Rows: criteria.** Use the system's most critical architecture characteristics (the handful identified during characteristic analysis). Spending effort scoring, say, performance when the system lives or dies on elasticity and data integrity wastes the exercise. Identifying characteristics is therefore the prerequisite to risk analysis.
- **Columns: context.** Prefer domains or subdomains (for example registration, checkout, fulfillment, shipping). Service-level columns are usually too fine: they hide risk that lives in communication and coordination between services.
- **Cells:** the 1 to 9 score for that criterion within that context.
- **Totals:** sum each row and each column.

## Reading totals and choosing priorities

The grid answers two different prioritization questions:
- **Row totals** rank criteria: which quality is most at risk across the whole system.
- **Column totals** rank contexts: which part of the system carries the most combined risk.

A criterion can be the worst overall while a specific context is the worst for a different reason, so read both before deciding where extra effort goes. Use individual high cells for concrete action items and totals for portfolio-level focus.

## Filtering for an audience

The full grid is right for the working team but noisy for stakeholders. For a briefing, blank out the low and medium cells and show only the high ones. Raising the signal-to-noise ratio makes the message (here is where we are exposed) land faster and keeps the meeting from drifting into green cells. Keep the full version available as backup.

## Adding direction (trend)

A single grid is a snapshot; it cannot say whether things are improving. Add a third dimension, direction, per cell:

- An upward-pointing marker: risk rising (score heading higher).
- A downward-pointing marker: risk falling.
- A neutral marker (circle): no change.

Always include a legend, because direction symbols are easy to misread. Direction should come from continuous, objective measurements, which means fitness functions (automated checks on characteristics such as error rates, latency percentiles, coupling metrics or failed integrity checks) feeding the assessment over time, not from someone's memory of last quarter. A cluster of rising markers on one criterion across several contexts usually points to a shared cause (for example a common database).

## Pitfalls

- Scoring every characteristic instead of the critical few.
- Scoring at service granularity and missing inter-service risk.
- Reporting only the product, losing which factor drives the score.
- Showing the full grid to executives and burying the signal.
- Presenting a snapshot as if it were a trend.
- Guessing likelihood low when evidence is missing.

## Review questions

1. Why can a risk score of 5 never appear?
2. A component has catastrophic impact but nobody knows how often it fails. What score do you start with, and what evidence would lower it?
3. When would you choose subdomains rather than services as assessment columns?
4. What data source should drive the direction markers?
