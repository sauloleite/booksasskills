# Fit, Trade-offs and Use Cases

## Contents
- When the style fits
- The microkern-ality spectrum
- Characteristic profile (qualitative)
- Partitioning and quanta
- Cloud placement options
- Use cases and analogies
- Worked fit assessment

## When the style fits

Strong signals:
- The product is shipped as a single installable unit, often run on the customer's premises.
- The business has one standard process with many local or client-specific variations (insurance rules per state, shipping rules per country, tax forms per regulation, assessment rules per device model).
- Users or customers expect to extend or customize features (issue trackers, IDEs, CI servers, browsers).
- Rule sets change often while the overall workflow changes rarely.

Weak or negative signals:
- High or bursty load requiring independent scaling or elasticity of the main flow.
- Strict fault-tolerance needs where one failing component must not affect others.
- No identifiable stable center; most change requests touch the shared workflow.
- Variations need to call each other heavily.

## The microkern-ality spectrum

Supporting plug-ins does not make a system a microkernel; every microkernel, however, supports plug-ins. Position on the spectrum depends on how much a core does on its own:
- **Pure end**: the core is almost useless alone (an IDE editor shell, a linter whose core only parses code into a syntax tree for rule plug-ins).
- **Plug-in-capable end**: the core is a complete product, and plug-ins are optional extras (a web browser).

Decision aid: the more volatile you judge the core functionality to be, the less you should aim for a pure microkernel. A pure design assumes a core that almost never changes.

## Characteristic profile (qualitative)

Shared with the layered style:
- Main strengths are simplicity and low overall cost.
- Main weaknesses are scalability, elasticity and fault tolerance, all caused by monolithic deployment.
- Always a single architecture quantum.

Where it is better than layered:
- **Testability, deployability, reliability**: moderately good, because changes are confined to isolated plug-ins, which shrinks test scope and deployment risk (most so with runtime plug-ins).
- **Modularity and evolvability**: moderately good; features are added, swapped or removed as self-contained plug-ins, so teams react to change quickly (a new regulatory form becomes a new plug-in; an obsolete one is unplugged).
- **Responsiveness**: moderately good, because these applications tend to stay small, suffer less from pass-through layers (the sinkhole antipattern), and can be trimmed by unplugging unused features (an application server runs faster with clustering, caching and messaging removed).

## Partitioning and quanta

This is the one style the authors treat as able to be both technically and domain partitioned. Most implementations are technically partitioned (core vs plug-ins), but when plug-ins line up one-to-one with domain variations (location, client, product), the architecture becomes isomorphic to the domain and behaves as domain partitioned. Use this argument when justifying the style for customization-heavy domains.

Quantum count stays at one regardless of remote plug-ins, because the core is in every request path.

## Cloud placement options

Monoliths offer coarse cloud choices:
1. Whole application in the cloud (VMs, managed platforms or containers).
2. Data in the cloud, application on-premises.
3. Core on-premises, plug-ins in the cloud.

Option 3 looks modular but is usually a latency trap: key workflows run through plug-ins, calls are frequent, and payloads are large, so each core-plug-in hop over a WAN adds noticeable overhead. Estimate calls per request times added round-trip before accepting it.

## Use cases and analogies

- Developer and release tooling: IDEs, static-analysis tools, issue trackers, CI servers.
- Browsers: viewers and extensions add capabilities to a working core.
- Tax preparation: the summary return is the core driver; each supporting form and worksheet is a plug-in, so legal changes land in one plug-in.
- Insurance claims: the standard filing and processing flow is the core; each jurisdiction's rules live in its own plug-in, written as code or delegating to a dedicated rules-engine instance. This avoids one giant shared rules engine degrading into a Big Ball of Mud where every rule change needs a large team to verify nothing broke. Jurisdictions can be added or removed independently.

General lesson: customization is everywhere in software, and this structure maps directly onto it, so expect to recognize it in many systems.

## Worked fit assessment (invented)

Scenario: a lending platform must compute affordability rules for 12 countries; rules change quarterly per country, the application workflow (intake, scoring, decision, notification) changes about once a year, load is steady, and the product is deployed in each client bank's own data center.

- Stable common process: yes (workflow). Variation dimension: country. Fit signal strong.
- Deployment: on-prem, single unit favored; keep plug-ins in-process. Runtime binding is worth it only if banks need hot updates of rules without downtime.
- Spectrum: core is useful alone (workflow), so a plug-in-capable design, not pure.
- Weak spots: elasticity irrelevant (steady load); fault tolerance acceptable for batch scoring.
- Decision: microkernel with `app.plugin.affordability.<country>` packages, standard contract (applicant data in, decision and explanation out), core-owned database, per-country rule tables owned by each plug-in. Record in an ADR with the rejected remote-plug-in option and why (on-prem install burden).
