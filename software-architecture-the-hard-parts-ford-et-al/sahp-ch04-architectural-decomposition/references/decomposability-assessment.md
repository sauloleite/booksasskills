## Contents
- Purpose of the assessment
- The Big Ball of Mud question
- Raw coupling: afferent and efferent
- Derived metrics: abstractness and instability
- Distance from the main sequence and the two zones
- Reading the results: decision guide
- Worked example
- Pitfalls
- Glossary

# Is the codebase decomposable?

## Purpose of the assessment

Before choosing any technique for splitting a monolith, establish whether the code has enough internal structure to be worth restructuring at all. Architecture is, at heart, about internal structure; a system that has none gives decomposition patterns nothing to grip. The assessment is the first node of the decision tree: decomposable or not, and if so, structured or chaotic.

No single number settles this. Metrics describe macro characteristics of the code, and a human architect makes the call after looking at them alongside the source itself.

## The Big Ball of Mud question

The Big Ball of Mud anti-pattern (named by Brian Foote, 1999) describes code with no discernible modularity: for example, UI event handlers that issue SQL directly, business rules smeared across screens, and no namespaces that mean anything. Such systems usually arrive there through lack of governance over time, not through a single bad decision.

Frame the question as salvageability: is this codebase a candidate for decomposition patterns, or would another approach (tactical forking, or a rewrite) be a better use of effort?

## Raw coupling: afferent and efferent

Defined by Yourdon and Constantine (Structured Design, 1979):

- Afferent coupling (Ca): number of incoming dependencies on an artifact (who uses me).
- Efferent coupling (Ce): number of outgoing dependencies from an artifact (whom I use).

Why these two alone matter during a split: monoliths encourage reuse of core concepts (an `Address`, `Money`, or `AuditLog` class). That reuse was healthy in a single deployable but becomes a cross-service dependency once the system is distributed. A high-Ca artifact is a shared asset whose ownership must be decided before services are carved out (duplicate it, move it into a shared library, or make it a service). Count those first.

Most platforms have tooling that emits a dependency matrix per package or component (JDepend for Java, NDepend for .NET, and dependency-graph tools for other ecosystems). Use them rather than hand-counting.

## Derived metrics: abstractness and instability

Robert Martin introduced two ratios (late 1990s, originally for C++, applicable to any OO language) that capture the balance of a component.

Abstractness (A): proportion of abstract artifacts (interfaces, abstract classes) relative to implementation artifacts. In Martin's common form, A = Na / (Na + Nc), bounded between 0 and 1. The chapter phrases it as the ratio of abstract to concrete counts; for components with mostly concrete code the two readings are close. Low A means implementation without abstraction; a 10,000 line program in one entry function scores near zero and is hard to comprehend.

Instability (I): I = Ce / (Ce + Ca). It expresses how exposed a component is to change forced on it by the things it depends on.

- I near 1: depends on many, depended on by few. Breaks easily when neighbours change.
- I near 0: depended on by many, depends on little. This is either stable (if mostly abstract) or rigid (if mostly concrete and therefore hard to change without breaking its many clients).

Quick check of the arithmetic: a component with Ca = 2 and Ce = 0 has I = 0; with Ca = 2 and Ce = 3 it has I = 3/5 = 0.6.

Trade-off to keep in mind: pushing every component toward high stability (self-contained, nothing outgoing) tends to produce duplication, because reuse requires outgoing dependencies. Stability is bought with reduced reuse.

Interpret A and I together, never in isolation; a low I is good or bad depending on A.

## Distance from the main sequence and the two zones

The main sequence is the idealized line A + I = 1 on a plot with I on one axis and A on the other. Normalized distance:

D = |A + I - 1|, ranging from 0 (on the line) to 1 (farthest corner).

- Near the line: healthy balance between abstraction and dependency direction.
- Zone of pain (low A, low I, near the origin): concrete code that many others depend on. Brittle, expensive to change, painful to move.
- Zone of uselessness (high A, high I): abstractions nobody depends on. Indirection with little payoff; hard to use.

D is one of the few holistic structural measures available, which is why it is useful for unfamiliar codebases, migration planning and technical-debt assessments.

## Reading the results: decision guide

Analogy from construction: relocating a building with a cracked foundation is risky, and shoring the foundation up first makes the move easier. Likewise, improving internal structure makes a later split cheaper.

| Observation | Interpretation | Next step |
|---|---|---|
| Most components close to the main sequence, a few outliers | Structure is salvageable | Proceed to choose an approach (component-based decomposition is likely available) |
| Clusters of components in the zone of pain, especially high-Ca shared ones | Rigid shared core | Plan ownership of shared code; refactor or isolate before extraction |
| Many components in either zone, few near the line | Repairing structure may cost more than it returns | Do not invest in shoring it up; consider tactical forking or replacement |
| Few identifiable components at all (one giant namespace) | Metrics have little to measure | Treat as unstructured; tactical forking is the likely fit |

Thresholds are judgment calls. The chapter gives no numeric cut-off; treat D around 0.5 or more as a red flag worth inspecting, and look at the distribution rather than a single average.

## Worked example

An insurance claims monolith has nine packages. Tooling reports:

- `claims.intake`: A = 0.2, Ca = 1, Ce = 4, so I = 0.8, D = 0.0. Healthy.
- `common.party` (customer and address types): A = 0.0, Ca = 7, Ce = 0, so I = 0, D = 1.0. Deep in the zone of pain and used by almost everything.
- `rules.spi`: A = 0.9, Ca = 0, Ce = 2, so I = 1.0, D = 0.9. Zone of uselessness: an abstraction layer nobody implements against any more.
- The other six sit within D of 0.3.

Conclusion: the codebase is decomposable. Before forming services, decide how `common.party` will be shared (it will otherwise couple every future service), and delete or fold `rules.spi`. Then move to component-based decomposition because component boundaries clearly exist.

The bundled script `scripts/decomposability_metrics.py` computes Ca, Ce, A, I, D, zone labels and the most-shared components from simple CSV input.

## Pitfalls

- Trusting one aggregate number. Averages hide a rigid shared core; inspect the worst components and the highest-Ca ones.
- Reading low instability as automatically good. Without abstractness it means rigidity.
- Ignoring shared utility classes because they are small. Their Ca, not their size, determines how much they will entangle services.
- Running metrics on a codebase where namespaces do not reflect real components. The numbers will look tidy while the coupling lives inside a few giant packages.
- Spending months polishing a structure that is mostly in the two zones. If the code is beyond repair, choose an approach that does not depend on its structure.

## Glossary

- Main sequence: the line A + I = 1 representing balanced components.
- Rigid component: low instability and low abstractness; many dependents, all concrete.
- Salvageable codebase: one whose existing structure is good enough to apply decomposition patterns to.
