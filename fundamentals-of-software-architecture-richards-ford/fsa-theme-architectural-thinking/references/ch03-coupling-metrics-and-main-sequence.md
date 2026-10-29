# Coupling metrics and the main sequence

## Contents
- Afferent and efferent coupling
- Abstractness
- Instability
- Distance from the main sequence and the two zones
- Interpreting results (playbook)
- Limits of code metrics
- Worked example

## Afferent and efferent coupling

Coupling is more tractable than cohesion because calls form a graph that can be counted. The terms come from Yourdon and Constantine's structured design work (1979).

- **Afferent coupling (Ca):** incoming dependencies. How many other artifacts depend on this one.
- **Efferent coupling (Ce):** outgoing dependencies. How many other artifacts this one depends on.
- Mnemonic: a comes before e as "arriving" comes before "exiting"; e for exit means outgoing. The names favored mathematical symmetry over clarity, so spell out "incoming/outgoing" when talking to non-specialists.
- Static analysis tools exist for virtually every platform; count at the level you care about (class, package, component).

Structured design predates OO and lists further coupling types that modern languages have made obsolete; connascence is the more refined vocabulary that replaced them.

## Abstractness

Robert C. Martin's derived metrics build on raw coupling.

A = abstract types / (abstract types + concrete types)

- Abstract types: interfaces, abstract classes, protocols, traits.
- A near 0: all implementation, no seams (the extreme is a whole program in one giant function).
- A near 1: mostly abstractions, hard to follow how anything is wired (deep stacks of factories, proxies and abstract bases with vague names).
- Neither extreme is a goal by itself; it matters only relative to how much the module is depended on.

## Instability

I = Ce / (Ce + Ca)

- I near 1: depends on many things, few depend on it. It breaks easily when its dependencies change, but changing it hurts no one.
- I near 0: many dependents, few dependencies. It is hard to change safely because changes ripple outward.
- "Instability" means susceptibility to breakage from outgoing coupling, not code quality. A class that delegates to many others is fragile when any callee changes.

## Distance from the main sequence and the two zones

D = |A + I - 1|, both inputs in [0, 1], so D is in [0, 1].

- The main sequence is the line A + I = 1. Components on or near it balance abstraction against dependency direction: stable things are abstract, volatile things are concrete.
- D is one of the few holistic structural metrics available to architects.
- **Zone of pain** (low A, low I, bottom left): concrete code that lots of others depend on. Rigid, brittle, painful to change. Typical: a shared "common" library of concrete classes, a database schema module, a core domain class used everywhere.
- **Zone of uselessness** (high A, high I, top right): abstractions that nothing uses. Speculative interfaces, frameworks within the app, dead extension points.
- Exceptions are normal: stable concrete code that never changes (string utilities from the platform, a frozen value type) can live in the pain zone harmlessly. Pain only hurts when the code must change.

## Interpreting results (playbook)

1. Compute A, I, D per component (run the bundled script or a platform tool).
2. Sort by D. Inspect the top outliers, not every component.
3. For pain-zone components, ask: does this change often? If yes, introduce abstractions that dependents use (interfaces, ports) or reduce dependents by splitting. If no, accept it and document why.
4. For uselessness-zone components, ask: is any of this abstraction used? Remove or inline unused interfaces; fold thin abstract layers into their single implementation.
5. Check direction: dependencies should point toward stable, abstract components. A stable component depending on a volatile one is a red flag regardless of D.
6. Baseline and trend. Turn the metric into a fitness function that fails the build when a component crosses an agreed D threshold or when D worsens release over release.

Use these metrics for: getting familiar with a code base, preparing a migration (which parts are entangled), and assessing technical debt.

## Limits of code metrics

- Software metrics are blunt compared to other engineering disciplines; all of them need interpretation.
- Cyclomatic complexity cannot distinguish essential complexity (the problem is hard) from accidental complexity (the code is worse than necessary). The same caution applies to D and LCOM.
- Still worth it: establish baselines for critical metrics so deviations stand out, and automate them as governance checks.
- Metrics depend on correct inputs. Counting generated code, test code or vendored libraries skews A and I; define scope before measuring.
- Edge cases: a component with no couplings has undefined I; a component with no types has undefined A. Report them separately rather than forcing a number.

## Worked example (invented)

| Component | Ca | Ce | Abstract | Concrete |
|---|---|---|---|---|
| shared.common | 14 | 1 | 0 | 22 |
| payments.ports | 9 | 1 | 8 | 2 |
| reporting.ui | 0 | 8 | 0 | 15 |
| plugins.api | 0 | 1 | 9 | 1 |

- shared.common: A = 0, I = 1/15 = 0.07, D = 0.93. Pain zone. It changes monthly, so extract interfaces for the three most used services and split date and money helpers into their own components.
- payments.ports: A = 0.8, I = 0.1, D = 0.1. Close to the line: stable and abstract, as intended.
- reporting.ui: A = 0, I = 1, D = 0. Volatile and concrete, which is fine for a leaf.
- plugins.api: A = 0.9, I = 1, D = 0.9. Uselessness zone: nobody implements the plugin interfaces. Delete or defer until a real plugin exists.
