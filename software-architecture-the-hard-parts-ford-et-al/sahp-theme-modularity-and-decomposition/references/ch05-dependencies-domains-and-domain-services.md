# Component Dependencies, Component Domains and Domain Services

## Contents
- Determine Component Dependencies
  - The three migration questions
  - What counts as a dependency
  - Coupling measures
  - Reading the dependency picture: golf ball, basketball, airliner
  - Filtering noise and reducing coupling before extraction
- Create Component Domains
  - Namespace as domain map
  - Procedure
  - Validation with the business
- Create Domain Services
  - Target: service-based architecture
  - Sequencing rules
  - What changes during extraction
- Worked example
- Pitfalls

## Determine Component Dependencies

### The three migration questions

Stakeholders want three answers before funding a migration:
1. Can this monolith be broken apart at all?
2. Roughly how big is the effort?
3. Will it be a refactoring (moving existing code into separately deployed units) or a rewrite?

Component dependency analysis answers all three quickly and at the coarse grain executives want. In the authors' experience, coupling between components ranks among the most decisive factors in whether a migration succeeds, and that teams who start carving out microservices without first visualizing the monolith's structure routinely struggle.

### What counts as a dependency

Only dependencies **between** components count. A dependency exists when a class in one component namespace calls or references a class in another. How tangled the classes are inside a single component is irrelevant here.

Direction matters. If `app.invoice.Generator` calls `app.mail.Sender`, Invoice has an outgoing (efferent) dependency on Mail, and Mail has an incoming (afferent) dependency from Invoice.

### Coupling measures

- **CA (afferent):** number of other components that depend on this one.
- **CE (efferent):** number of other components this one depends on.
- **CT (total):** CA plus CE.

Analyze both directions. High CA marks a component many others need (shared or core); high CE marks a component that will make many remote calls once distributed.

### Reading the dependency picture: golf ball, basketball, airliner

Generate a component-level dependency diagram (IDE plug-ins and static analysis tools do this; boxes are components, lines are coupling points) and use the book's coarse size vocabulary when reporting:

- **Golf ball.** Components barely touch each other. The breakup is clearly viable, the work is modest, and existing code can mostly be relocated into services rather than rewritten.
- **Basketball.** Some regions form dense knots while others are loosely connected; this is what most real business systems look like. Viability is uncertain, the effort is substantially larger, and expect to rewrite parts of the knotted regions while moving the rest.
- **Airliner.** Coupling is pervasive with no recognizable modules. Breaking it apart is not realistic; a distributed version would amount to rebuilding the application from scratch, so advise against the migration as framed.

Even within the airliner category, size varies (a regional jet versus a wide-body), so add a qualifier when reporting. Treat the diagram as radar: it shows where high coupling is concentrated and previews the service dependency graph you will inherit if you distribute the system as-is. Uneven pictures also guide sequencing: extract the sparse regions first.

### Filtering noise and reducing coupling before extraction

- **Filter shared library components.** Components that hold interfaces, entities and helpers used through compile-time references (the `.sharedcode` leaves) will become libraries, not services. Hide them from the diagram to see the coupling between the components that will actually become services. A picture that looks alarming with them can look modest without them.
- **Expect shared business components to have the highest CA.** A consolidated notification or audit component will be referenced widely; that is by design, not a defect.
- **Split to reduce coupling.** High CA does not mean every dependent needs everything. Example: a Pricing component has CA of 18, but 12 dependents only call its tax lookup. Splitting it into Tax Lookup (CA 12) and Pricing Rules (CA 6) leaves most of the logic with far fewer dependents and makes the small, widely used piece easier to treat as a library or stable service.
- **Restrict forbidden paths.** Once you know which components must never depend on each other, encode each rule as its own automated check (see the fitness-functions reference).

## Create Component Domains

Services and components have a one-to-many relationship: a service normally contains several components. This pattern groups related components into domains so that coarse-grained domain services can be cut along those groupings.

### Namespace as domain map

Use namespace hierarchy to express ownership: `app.<domain>.<subdomain>.<component>`. In `app.customer.billing.invoice.InvoiceRun`, `customer` is the domain, `billing` a sub-domain, `invoice` the component, and `InvoiceRun` a class. Many legacy monoliths predate domain-driven design, so their namespaces are organized by technical layer or by history and must be refactored before domains are visible in the code.

### Procedure

1. Start from the flattened, consolidated component list.
2. With business stakeholders, name a small set of domains (typically a handful, plus one shared domain for cross-cutting business components such as login or notification).
3. Assign every component to exactly one domain. Draw the grouping; check that no component is left over and that components inside each domain are cohesive.
4. For each component whose namespace does not begin with its domain node, write an architecture story to move it (for example, `app.refund` becomes `app.customer.refund`). One story per domain, or one story covering several small domains, keeps the work reviewable.
5. Remove unnecessary nesting while renaming: if a sub-domain would hold only one component, rename so the component sits directly under the domain.
6. Lock the domain list with an automated check so teams cannot create new top-level domains silently.

### Validation with the business

Grouping is a joint exercise with the product owner or business sponsor. If components refuse to fit any domain, or a domain looks incoherent, that is a signal to go back to the business, not to force the fit. The book recommends treating service-based architecture as the first stop on the way to finer-grained architectures, and component domains are exactly the units that become its services.

## Create Domain Services

### Target: service-based architecture

A domain service is a coarse-grained, separately deployed unit containing all components of one domain. The basic topology: a user interface calling several domain services remotely, all still sharing the monolithic database. Variants (split user interfaces, split databases, an API gateway) can come later; start with the basic shape.

Why stop here first: running coarse services teaches the team which domains genuinely need to be broken into microservices and which can stay as they are. Teams that start fine-grained must immediately absorb everything microservices demand (splitting data, distributed workflows and transactions, heavy operational automation, containers) even when the business never needed that granularity.

### Sequencing rules

1. **Do not extract any domain until all domains have been identified and their namespaces refactored.** If a component is reassigned to a domain after that domain's service already exists, the service must be reopened and changed. Finishing the logical grouping first minimizes rework.
2. Extract one domain at a time into its own project or repository, deploy it, and point the user interface at it.
3. Keep each domain service internally aligned: every component in it should share the domain's namespace prefix, so the service does not decay into a small, unstructured monolith and remains splittable later.
4. After all domains are services, move on to data decomposition and service granularity analysis (later chapters) where the business case warrants it.

### What changes during extraction

- Code for the domain moves into a new workspace with its own build and deployment.
- The user interface switches from in-process calls to remote calls for that domain.
- Cross-domain calls that used to be method calls become network calls; the dependency analysis tells you how many to expect.
- The database stays shared at this stage, so data ownership questions are deferred, not solved.

## Worked example

A clinic-management monolith has 22 flattened components. The dependency diagram looks dense, but after hiding three `.sharedcode` leaves only two clusters remain tight: appointment scheduling with resource booking, and claims with payments. Verdict for the sponsor: feasible, basketball-sized, mostly refactoring with some rewrite in the two clusters.

Domains agreed with the operations lead: Patient, Scheduling, Billing, Clinical, and Shared (login, notification). Eight components need namespace moves; one, "Insurance Eligibility", fits nowhere cleanly, so the team returns to the business, which places it in Billing. Only after all moves are merged does extraction start, beginning with Clinical (fewest incoming dependencies), then Patient, then the rest. Each new service gets a check that all its classes live under its own domain prefix.

## Pitfalls

- Counting class-level coupling instead of component-level coupling.
- Looking only at incoming or only at outgoing coupling.
- Judging feasibility with shared library components still cluttering the picture.
- Starting a migration with no dependency picture at all.
- Grouping components into domains without business stakeholders.
- Extracting the first domain service before every component has a domain.
- Jumping straight to fine-grained microservices and inheriting all their operational and data burdens prematurely.
