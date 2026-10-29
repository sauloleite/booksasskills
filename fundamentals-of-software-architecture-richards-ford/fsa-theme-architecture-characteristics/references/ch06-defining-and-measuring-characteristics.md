# Defining and Measuring Architecture Characteristics

## Contents
- Why characteristics resist definition
- Building a shared vocabulary
- Operational measures
- Performance has many flavors
- Process measures
- When a process concern becomes architectural
- Playbook: turning a vague "-ility" into a measurable one
- Worked example
- Pitfalls

## Why characteristics resist definition

Three recurring obstacles block objective conversations about quality attributes:

| Obstacle | Symptom in a meeting | Remedy |
|---|---|---|
| Not physical quantities | "It must be blazing fast", "we need agility" | Ask what observable number would prove it |
| Conflicting definitions | Ops, dev and business each mean something different by "performance" | Write one organization-wide definition per term |
| Composite terms | "Agility", "reliability" bundle several smaller attributes | Decompose until every leaf is measurable |

Decomposition is the lever that fixes all three at once: a composite characteristic broken into its constituent parts yields leaves that each have a concrete measure and an owner.

## Building a shared vocabulary

Agreeing on standard, concrete definitions gives the organization a ubiquitous language for architecture (the Domain-Driven Design idea applied to quality attributes). Practical form:

- A glossary entry per characteristic: name, decomposition, metric(s), measurement method, target or alarm rule, owner.
- Composite entries point to their leaves (agility: modularity, deployability, testability).
- Disagreements about a term are resolved once, in the glossary, not re-litigated per project.

## Operational measures

Runtime characteristics (performance, scalability, elasticity, availability) have obvious direct measures, but the choice of statistic changes what you see.

- **Averages hide tails.** If a rare boundary condition makes about 1% of requests ten times slower, a busy system's mean barely moves. Track maximum and high percentiles (p95, p99, p99.9) alongside the mean.
- **Prefer statistical baselines to arbitrary targets.** Mature teams record the metric over time, fit a model of expected behavior (seasonality, growth), and alert when live values leave the predicted band. An alert then means one of two useful things: the model is wrong, or the system is misbehaving. Both are worth knowing.
- **Measures evolve with the platform.** New devices and tooling create new metrics; front-end teams now budget for user-perceived timings (first contentful paint, time until the CPU goes idle) because they reveal mobile pain that server timings miss. Revisit the metric set periodically.

## Performance has many flavors

"Performance" is not one number. Distinguish at least:

- **Request/response latency** for the whole interaction (classic web view).
- **Per-part performance budgets**: specific limits for specific parts of the app, e.g. first visible render on a page. Research on user behavior shows the target is a fraction of a second, while many apps are far slower; sites competing for every user track it closely.
- **Page weight (K-weight) budgets**: a cap on the bytes of libraries and frameworks a page may ship. The rationale is physical: bandwidth is finite, especially on mobile in weak-coverage areas. Such a budget constrains design decisions (framework choice, bundling, lazy loading), not just tuning.

When someone says "performance", ask which flavor, which percentile, under which load, on which device class.

## Process measures

Some characteristics live in the development process yet still shape architecture.

- **Agility** is composite; decompose into testability and deployability (and modularity).
- **Testability**: code coverage is measurable on nearly every platform, but coverage only says which lines ran. A suite can reach 100% with weak or missing assertions and prove nothing. Pair coverage with assertion checks or mutation testing.
- **Deployability**: success rate of deployments, deployment duration, and defects or incidents caused by deployments. (These overlap with DORA-style metrics; pick the set that matches your goals.)
- Each team must pick a mix of quantitative and qualitative measures aligned to its organization's priorities; there is no universal list.

## When a process concern becomes architectural

If easy deployment and testability rank high, the architect responds structurally: stronger modularity and isolation between parts. This is a characteristic driving a structural decision. Anything in project scope can become an architecture characteristic when it meets the three criteria from Chapter 4: it is a nondomain design consideration, it influences structure, and it is critical or important to success.

## Playbook: turning a vague "-ility" into a measurable one

1. Capture the stakeholder phrase verbatim ("checkout must be fast").
2. Classify: operational, structural, or process.
3. Decompose composites until each leaf is single-purpose.
4. For each leaf choose metric, statistic (mean, max, percentile, rate), scope (endpoint, page, module) and measurement point (synthetic, real user, CI).
5. Set the success rule: a fixed budget where physics or contracts dictate it, otherwise a statistical baseline with anomaly alerts.
6. Record it in the shared glossary with an owner.
7. Decide how it will be governed: which fitness function checks it, and when (build, deploy, production).

## Worked example

Request: "The mobile app must feel fast and the team must be agile."

- Fast (operational): p95 API latency for cart endpoints under expected peak; first visible render on mid-range phones on a slow network; page weight budget of N KB of script.
- Agile (process, composite): testability = coverage plus "every test asserts" rule; deployability = deploy success rate, lead time per deploy, rollback count.
- Structural consequence: because deployability is high priority, isolate cart and catalog into separately testable and deployable modules, and add a cycle check so they stay separable.

## Pitfalls

- Setting one arbitrary number (e.g. "under 200 ms") with no statistic or scope.
- Reporting only averages for latency.
- Treating coverage percentage as proof of correctness.
- Letting each department keep its private definition of a shared term.
- Freezing the metric set while devices, tools and targets keep changing.
