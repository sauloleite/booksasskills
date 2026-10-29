# Component Inventory and Sizing

## Contents
- Where this fits in the pattern sequence
- Architecture stories
- What counts as a component
- The inventory record
- Why statements are the size metric
- Sizing rules and thresholds
- Reading the numbers: signals and what to do
- Resizing an oversized component
- Worked example
- Pitfalls

## Where this fits in the pattern sequence

The chapter defines six refactoring patterns applied in a fixed order to move a namespace-organized monolith toward domain services: identify and size components, gather common domain components, flatten components, determine component dependencies, create component domains, create domain services. The first pass runs them in sequence. After that, while the monolith keeps receiving features and fixes during a long migration, each pattern is reapplied individually whenever its fitness function raises an alert. Every pattern therefore has three parts: the refactoring itself, automated governance that keeps it true, and an application to a running example.

Sizing always comes first because every later pattern reasons about components: you cannot consolidate, flatten, map dependencies or group into domains until you have a trustworthy, evenly sized catalog.

## Architecture stories

Record each structural refactoring as an architecture story rather than a user story or a tech-debt ticket.

- A user story changes features. A tech-debt story is cleanup that can wait for a later iteration.
- An architecture story changes the structure of the code to serve a named business driver or architecture characteristic (scalability, agility, time to market, extensibility). It is not optional cleanup; it is part of the migration.
- Template: "As an architect, I need to <structural change> in order to support <characteristic or business driver>." Example: "As an architect, I need to split the Pricing component into rule evaluation and price publication so that new promotion types can be added without touching publication code."

Every pattern in this skill produces one or more architecture stories (split this, move that namespace, consolidate these three).

## What counts as a component

A component is the code grouped under one leaf-node namespace (or directory) that performs a specific, nameable job. A namespace that has child namespaces is a sub-domain, not a component, and should hold no code of its own (see the flattening reference). Services are assembled from components, usually several per service, so mis-sized components produce mis-sized services.

## The inventory record

Capture one row per component with these fields:

| Field | Guidance |
|---|---|
| Component name | Self-describing; a reader should infer the responsibility from the name alone. Vague names such as "Order Manager" or "Ticket Handler" hide scope; rename the component (and ideally its namespace) until the role is obvious. Use the same name in every diagram and document. |
| Namespace | Where the code physically lives. If components are directories, turn path separators into dots (`app/order/checkout` becomes `app.order.checkout`). Some languages force namespace to match directory, others do not; pick one convention and use it for every component. |
| Statements | Sum of statements across all source files in the component. Primary measure of size and a rough proxy for complexity. |
| Percent | Component statements divided by total statements in the whole codebase. The quickest way to see outliers. |
| Files | Number of source files (classes, interfaces, types). Not a size measure, but it reveals class-structure problems. |

Most static analyzers report statements per file but do not roll them up per component, so plan a small post-processing step (script or spreadsheet) to aggregate by namespace and compute percentages. The bundled `scripts/component_sizing.py` does this from a CSV.

## Why statements are the size metric

File count, class count and lines of code all depend on personal style: one developer writes ten small classes where another writes one large one, and formatting inflates or deflates line counts. A statement is one complete action in the code, typically ending with a semicolon in C-family languages (Java, C#, C, C++, Go, JavaScript) or with a newline in languages such as Python, Ruby and F#. Summing statements per component is imperfect but tracks both how much a component does and how complex it is far better than the alternatives.

## Sizing rules and thresholds

1. **Consistency matters more than absolute size.** Aim for component sizes that cluster around the mean, generally within one to two standard deviations of it.
2. **Percent of codebase should be roughly even.** No component should hold a dramatically larger share than its peers.
3. **Percent thresholds scale with component count.** With about 10 components, a single component above roughly 30 percent is an outlier; with about 50 components, roughly 10 percent is already suspicious. A reasonable starting point is two to three times the fair share (100 divided by component count), tuned to the codebase.
4. **Standard deviation uses the sample formula** (divide by N minus 1). Number of standard deviations = absolute difference from the mean divided by the standard deviation. Governance checks often alert at 3 for stability; during an active sizing pass, inspect anything beyond 2.
5. **Outliers mask each other.** One giant component inflates the standard deviation so much that nothing else looks abnormal. Fix the biggest outlier, then recompute before judging the rest. Use the percent rule alongside the z-score so a single monster is caught either way.
6. **Too small also matters.** A component that does very little is a weak service candidate and often signals fragmentation; consider merging it with the sibling it always changes with. Size distributions are skewed to the right, so small outliers rarely cross a symmetric z threshold; scan the bottom of the list manually.

## Reading the numbers: signals and what to do

| Signal | Likely meaning | Action |
|---|---|---|
| Large percent and high z-score | Component does several jobs and is probably highly coupled | Split by sub-domain (below) |
| High statement count behind a simple-sounding name | Hidden complexity in what looks single-purpose | Investigate before treating it as a cheap service |
| Very high statements per file (for example, tens of thousands of statements in two or three files) | God classes inside the component | Refactor into smaller, contextual classes; component boundary may be fine |
| Name does not explain the responsibility | Unclear ownership, likely a grab bag | Rename; if no single name fits, it is probably two components |
| New component appears or old one disappears between builds | Team changed structure without the architect knowing | Update the inventory and re-run the other patterns' checks |

Why oversized components hurt: relative to peers they tend to carry more incoming and outgoing dependencies, are harder to extract into a service, and make the whole system less modular.

## Resizing an oversized component

1. Look for sub-domains inside it, using functional decomposition (which distinct activities does it perform?) or domain-driven design (which bounded sub-contexts does it hold?).
2. Give each sub-domain its own leaf namespace beneath the original one.
3. Move code that all the new pieces depend on (utilities, shared queries, formatters, base types) into a dedicated shared leaf such as `.shared`, not into the parent namespace.
4. The original namespace now becomes a sub-domain and stops being a component.
5. Re-run the sizing analysis and confirm the distribution is even.
6. If no clear sub-domains exist, leave the component alone. A large but genuinely cohesive component is preferable to an arbitrary split.

The book's running story makes this concrete: one reporting component held about a third of all code; it turned out to contain three families of reports plus common plumbing, and was split into three report components and one shared component, after which every component landed in a narrow size band.

## Worked example

An online-retail monolith has 14 namespaces holding about 58,500 statements. Running the sizing script shows `shop.reporting` at roughly 41 percent with a z-score of about 3.4, far above everything else (mean about 4,200 statements). Two other observations: `shop.promo` packs 2,100 statements into 3 files (about 700 per file), and `shop.order` holds code while also having child namespaces.

Decisions:
- Architecture story: split reporting into `shop.reporting.sales`, `shop.reporting.inventory`, `shop.reporting.finance` and `shop.reporting.shared`.
- Developer task (not an architecture story): break the promotions god classes into smaller classes; the component boundary stays.
- `shop.order` is a flattening problem, handled by the next patterns.
- After the split, recompute: the standard deviation drops sharply and the very small `shop.notify` component (400 statements) now stands out, so evaluate it during the common-domain pass.

## Pitfalls

- Sizing by files, classes or lines, which rewards style rather than substance.
- Using a fixed percent threshold regardless of how many components exist.
- Trusting a single pass of z-scores when one huge outlier dominates.
- Splitting a large component that has no natural seams.
- Dumping shared code from a split into the parent namespace, which creates orphaned code.
- Skipping the inventory step because the code "already has packages": packages are not automatically well-sized components.
