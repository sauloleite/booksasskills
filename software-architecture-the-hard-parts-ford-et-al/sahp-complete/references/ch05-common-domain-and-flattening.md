# Gathering Common Domain Logic and Flattening Components

## Contents
- Part A: Gather Common Domain Components
  - Domain versus infrastructure sharing
  - How to find duplicated domain logic
  - Consolidation decision checklist
  - Shared service or shared library
- Part B: Flatten Components
  - Vocabulary
  - Two directions of flattening
  - Choosing the direction
  - Shared code inside a sub-domain
  - Shared-code metrics as a feasibility gauge
- Worked example
- Pitfalls

## Part A: Gather Common Domain Components

Goal: find business logic that is repeated across components and pull it into one component, so the eventual distributed system does not end up with several near-identical services.

### Domain versus infrastructure sharing

- **Shared domain logic** belongs to business processing and is needed by only some workflows: customer notification, auditing user actions, data validation, formatting business documents.
- **Shared infrastructure logic** is operational and needed by virtually every workflow: logging, metrics, security, configuration.

This pattern targets only the first kind. Infrastructure concerns are handled by other means (platform libraries, sidecars, service templates) and should not be merged into a business component.

Duplicated domain logic usually differs only in small details per caller (a different message template, an extra field written). Those differences are almost always cheap to parameterize inside one shared component.

### How to find duplicated domain logic

Mostly manual judgment, assisted by a few cheap signals:

1. **A class used from many components.** If, say, a `MailGatewayClient` is referenced by classes in five different namespaces, notification behavior is probably scattered across the code.
2. **A shared base class or interface hierarchy** extended in several components often indicates the same domain concept implemented several times.
3. **Repeated leaf names.** Namespaces such as `app.order.audit`, `app.payment.audit`, `app.returns.audit` all suggest one concern implemented three times. Each writes who did what to an audit store; the context differs, the outcome does not. Consolidate into `app.shared.audit`.
4. **Same-named source files** appearing in more than one component.

Expect false positives. Generic leaf names (`.validate`, `.calculate`, `.util`) repeat without implying duplicate domain logic; keep an exclusion list so the same non-issue is not reported again.

### Consolidation decision checklist

Before merging, check coupling, not just duplication:

1. List each candidate component and its afferent coupling (CA: how many other components depend on it) with the names of those dependents.
2. Predict the CA of the merged component (usually the union of the dependents).
3. Compare totals. If the merged component's CA roughly equals the sum of the parts, consolidation does not increase coupling to that concern; it just makes it visible in one place. That is acceptable.
4. If merging pulls in many new dependents (for example, because the merged component now also offers unrelated features), you are creating a hotspot that many components will depend on. Reconsider or merge more narrowly.
5. Confirm the code really is similar (not just the name).
6. Write an architecture story, move the code into one namespace, delete the old ones, and update the inventory.

The running story illustrates this: three customer-notification components with two, two and one dependents were merged; the merged component had five dependents, identical to the combined total, so the merge was approved.

### Shared service or shared library

Not every consolidated domain component becomes a service. The common code may instead ship as a library bound at compile time. That choice involves its own trade-offs (versioning, change propagation, runtime coupling, fault tolerance) and is analyzed separately in the book's chapter on reuse patterns; at this stage the goal is only to collect the logic in one place.

## Part B: Flatten Components

Goal: ensure code lives only in leaf-node namespaces so every source file belongs to exactly one identifiable component, and no component is stacked on top of another.

### Vocabulary

- **Component:** classes grouped in a leaf-node namespace that perform one specific function.
- **Root namespace (sub-domain):** any namespace that another namespace extends. Once `app.billing.invoices` exists, `app.billing` is a root namespace, not a component.
- **Orphaned classes:** source files sitting directly in a root namespace. They belong to no component.
- **Hills:** components built upon components (code at several levels of the same branch). Drawing namespaces from the bottom up makes these hills visible.

Why it matters: with code in both `app.survey` and `app.survey.templates`, nobody can say whether templates are part of the survey service or a separate one. Defining components strictly as leaves removes that ambiguity.

### Two directions of flattening

1. **Collapse down (merge):** move the child namespace's code into the parent and delete the child. The parent becomes the leaf and therefore a component. Use when the child was split off for no strong reason.
2. **Build up (split):** move the parent's orphaned code into new leaf namespaces created by functional decomposition or domain analysis (for example, `app.survey.create` and `app.survey.process`). The parent becomes a clean sub-domain. Use when the parent mixes several responsibilities or the existing children deserve to stay separate.

Either way, the invariant is the same: after flattening, no non-leaf namespace contains source files.

### Choosing the direction

Favor **keeping children separate and splitting the parent** when:
- the child functionality is complex or changes often (separating it isolates churn and future deployment);
- the parent's orphaned code naturally divides into distinct activities (create, complete, cancel);
- the combined component would become an oversized outlier.

Favor **collapsing into the parent** when:
- the functionality is small, stable and rarely changes;
- the original author cannot give a reason for the separate namespace;
- the merged size still sits comfortably in the normal range.

Talk to the developers who own the code; the history behind a namespace often settles the question quickly.

### Shared code inside a sub-domain

Root namespaces often hold interfaces, abstract classes and helpers used by the child components. These are still orphaned. Move them into a dedicated leaf, for example `app.survey.sharedcode`.

Pick one distinctive leaf name for shared code across the whole company (something like `.sharedcode` or `.commoncode` that no business namespace already uses). A unique marker makes shared code machine-countable.

### Shared-code metrics as a feasibility gauge

Two numbers fall out of consistent naming:

- **Shared-code share:** statements in all shared leaves divided by total statements. A high share (the book cites 45 percent as an example of trouble) predicts a distributed system tangled in shared-library dependencies that will be painful to maintain. Treat this as a red flag for the whole migration, not just a cleanup item.
- **Shared-component count:** each shared leaf is likely to become one shared library (JAR, DLL, package) or one shared service, so the count estimates how many such artifacts the target architecture will carry.

## Worked example

A logistics monolith has these namespaces:

- `fleet.vehicle` (60 files) plus `fleet.vehicle.maintenance` (12 files) and `fleet.vehicle.telemetry` (30 files)
- `fleet.route` (8 files) plus `fleet.route.optimizer` (5 files)

Analysis: telemetry changes weekly and is complex; maintenance is stable. The 60 orphaned files in `fleet.vehicle` cover registration, assignment to drivers and common entity classes. Decision: build up. Create `fleet.vehicle.registration`, `fleet.vehicle.assignment` and `fleet.vehicle.sharedcode`, keep the two existing children. For routing, the optimizer was separated "to keep it tidy", is small and rarely touched; collapse it into `fleet.route`, which becomes a single component. Then add `fleet.vehicle.sharedcode` to the shared-code tally and verify that the total shared share stays modest.

The book's story runs the same decision twice with opposite outcomes: the ticket area was raised into a sub-domain (assignment logic was complex and volatile, and the root code split into maintenance, completion and shared), while the survey area was collapsed into one component (stable, simple, and the template sub-namespace had no real justification).

## Pitfalls

- Merging infrastructure concerns (logging, security) into a business "common" component.
- Consolidating on name similarity alone without comparing the code.
- Skipping the before-and-after afferent coupling comparison.
- Treating shared code in a root namespace as acceptable because it is "shared".
- Using different shared-leaf names per team, which makes the shared-code share impossible to measure.
- Flattening in whichever direction is quickest instead of following complexity and change frequency.
