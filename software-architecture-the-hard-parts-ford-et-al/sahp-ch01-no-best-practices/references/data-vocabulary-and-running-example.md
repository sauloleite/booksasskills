# Data as an Architectural Concern, Shared Vocabulary, and the Running Example

## Contents
- Why data makes modern distributed architecture hard
- Operational versus analytical data
- Working vocabulary (deliberately simple definitions)
- The running example: a ticketing monolith in trouble
- How to use these ideas when assessing a real system

## Why data makes modern distributed architecture hard

Data typically outlives the systems and architectures built around it, so it deserves careful design. Businesses now use data in nearly every function (serving and retaining customers, acquiring new ones, improving products, forecasting), which means software architecture ultimately exists to make the right data available and usable across the enterprise. Tim Berners-Lee's observation that data lasts longer than systems is the chapter's epigraph for this point.

The authors' diagnosis of why microservices decisions feel harder than earlier distributed systems: in the early days, services were distributed but data mostly still lived in one relational database, so transactions stayed simple. Microservices, following the Domain-Driven Design idea of a bounded context to limit implementation coupling, push each service toward owning its own data. Data, and transactionality with it, therefore became an architecture concern. Many of the hard parts come from tension between data concerns and architecture concerns.

Implications for an agent:
- When a team proposes splitting a monolith, ask early where each piece of data will live, who owns it, and which workflows currently rely on a single ACID transaction across that data.
- Expect friction between instincts that favor a single, tightly integrated schema and the goal of independent services. Neither side is simply wrong; the conflict must be analyzed as a trade-off.
- Business data must survive the breakup and keep producing value; plan the migration with the database team, not around it.

## Operational versus analytical data

| Aspect | Operational (OLTP) | Analytical |
|---|---|---|
| Purpose | Runs the business day to day (sales, transactions, inventory) | Predictions, trends, business intelligence for strategy |
| Typical operations | Insert, update, delete | Read-heavy, aggregations, snapshots |
| Shape | Usually relational, transactional | Often non-relational (graphs, alternative snapshot formats), not transactional |
| Outage impact | Organization stops functioning quickly | Strategic decisions slow down; daily operations continue |

Use this split whenever a design mixes the two. A common smell is reporting queries and views coupled directly to the operational schema, which blocks splitting the operational data by service. Classify each consumer as operational or analytical before deciding where its data comes from.

## Working vocabulary (deliberately simple definitions)

The book keeps definitions minimal so the discussion stays at the architecture level. Use these meanings consistently when helping a user, and restate them if the user's team uses the words differently.

- **Service:** a cohesive set of functionality deployed as its own independently running executable. The concepts apply to distributed architectures broadly, microservices in particular. Later chapters tie services to the architecture quantum, which adds static and dynamic coupling.
- **Coupling:** two artifacts are coupled when changing one may force a change in the other for things to keep working. Note this is a change-propagation definition, not a call-graph one.
- **Component:** a building block performing a business or infrastructure function, usually expressed as a package, namespace or directory grouping of source files (for example, an "invoice history" component living under a matching namespace).
- **Synchronous communication:** the caller blocks until it gets a response.
- **Asynchronous communication:** the caller proceeds without waiting; optionally the receiver signals completion later on a separate channel.
- **Orchestrated coordination:** the workflow includes a service whose main job is to coordinate it.
- **Choreographed coordination:** no coordinator; participating services share responsibility for driving the workflow.
- **Atomicity:** a workflow is atomic when all its parts are consistent at every moment. The alternative is a spectrum of eventual consistency (covered in the book's later chapters on distributed data and transactions).
- **Contract:** any interface where two pieces of software meet: function or method calls, remote integration calls, dependencies and so on.
- **Saga:** the book plays on the everyday meaning (a long heroic tale) and the architectural one (a pattern for transactional behavior across distributed services, covered in later chapters).

These terms give three independent dimensions that later chapters combine: communication (sync/async), coordination (orchestrated/choreographed) and consistency (atomic/eventual). When analyzing a workflow, label it on each dimension explicitly rather than assuming one implies another.

## The running example: a ticketing monolith in trouble

The book threads a fictional story through every chapter, set at a large electronics retailer whose field technicians fix customers' devices under purchased support plans. Chapter 1 sets the starting point: a long-lived ticketing monolith that is failing the business. Do not reuse the story's characters or dialogue; the useful content is the problem shape, summarized here in brief.

Problem shape:
- **Users and workflows:** administrators (staff, expert skills, billing, reference data), customers (registration, plans, tickets, surveys), field experts (receive tickets on a mobile app, consult and update a knowledge base) and managers (operational and analytical reports). A ticket flows from creation, to automatic expert matching on skills, location and availability, to mobile dispatch and customer notification, to completion, knowledge-base update and a follow-up survey. Non-ticket workflows cover expert maintenance, customer registration, monthly automatic billing and reporting.
- **Symptoms:** lost tickets, wrong experts dispatched, the system unavailable for ticket entry, slow and risky changes that break unrelated features, and frequent freezes or crashes taking everything down for minutes to hours. The business line itself is at risk.
- **Structure:** roughly eighteen components grouped around login and users, billing (payment and history), customer (profile and notification), expert profile, knowledge base (maintenance and search), reporting, tickets (core, assignment, routing, notification), support contracts, and surveys (core, notification, templates).
- **Data:** one shared schema in third normal form covering customers, users and profiles, contracts, billing and payments, knowledge-base articles with tags and keywords, tickets and their history, and survey structures and responses. Few stored procedures or triggers, but many views, mostly feeding reporting.

Why this shape matters: it combines every pressure the book addresses. Reliability and deployability failures argue for splitting; a single shared schema with reporting views means data decomposition is the real constraint; ticket workflows need coordination decisions; billing needs consistency decisions; reporting mixes operational and analytical needs.

## How to use these ideas when assessing a real system

Invented example: a regional logistics company runs a dispatch monolith with one schema; drivers report lost jobs and every release breaks invoicing.

1. Separate symptoms by characteristic: lost jobs (reliability, data integrity), release breakage (deployability, testability, coupling), outages (availability, fault tolerance).
2. Inventory components by namespace and their tables. Mark which components share tables and which views feed reports.
3. Classify data consumers as operational or analytical; flag analytical views reading operational tables.
4. Identify workflows that span many components (dispatch to invoice) and note where they currently rely on one database transaction.
5. Only then discuss decomposition options, each with trade-offs, recorded as ADRs and protected by fitness functions.
