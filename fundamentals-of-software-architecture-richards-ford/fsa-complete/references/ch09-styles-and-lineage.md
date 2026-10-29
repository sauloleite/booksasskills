# Styles, Patterns, and Where They Came From

Covers: styles versus patterns, how styles emerge, the fundamental patterns (Big Ball of Mud, unitary, client/server variants, three-tier), and the long-term-implications lesson.

## Style versus pattern

A **style** is a named bundle of structural defaults. Saying "event-driven" or "layered" implicitly asserts a position on five dimensions:

| Dimension | Question to answer |
|---|---|
| Component topology | How are components and their dependencies arranged (by technical layer or by domain)? |
| Physical architecture | One deployable unit or many networked ones? |
| Deployment | How coarse are deployable pieces, and how often do they ship? |
| Communication | In-process calls, or remote protocols (REST, RPC, messaging)? |
| Data topology | One shared database, or data split along service lines? |

A **pattern** is a reusable solution to a problem in a context. Patterns are narrower and can appear inside many different styles (for example, a layered arrangement inside one domain component of a modular monolith).

Practical rules for an agent:

- When a user names a style, expand it into the five dimensions and confirm each. Many disagreements are really about one dimension (usually data topology) hiding behind a shared label.
- A style also carries implied characteristics, good and bad. Naming it is a shortcut for those trade-offs, so state the downsides along with the upsides.
- Do not treat a style name as a literal instruction. "Microservices" is a label coined in contrast to large, heavily orchestrated services; it does not tell teams to minimize service size.

## How styles emerge

No standards body invents styles. The cycle is: the ecosystem gains a new capability, someone combines it with existing techniques to solve a stubborn problem, others copy the result, and once it is common enough it gets a name. Microservices is the canonical case: mature DevOps automation, dependable open source operating systems, and domain-driven design together made a new decomposition practical.

Implication: when evaluating a new or trendy style, ask which ecosystem capability made it viable and whether your organization actually has that capability. Adopting the name without the enabling capability (for instance, microservices without automated provisioning and deployment) imports the costs without the benefits.

## Big Ball of Mud

The name (from Foote and Yoder's 1997 PLoP paper) describes a system with no discernible structure: everything reaches everything, data is effectively global or duplicated, and the original design, if there was one, has eroded.

Recognize it by:

- Event handlers or controllers that talk straight to the database with no intermediate structure (a common starting point for small scripts and apps that later grow).
- A dependency graph where nearly every class connects to many others, so the blast radius of any edit is unknowable.
- Engineering time dominated by chasing regressions caused by side effects rather than building features.
- Pain in deployment, testing, scaling, and performance that grows with system size.

Why it happens: rarely intentional; nearly always a governance gap around code quality and structure while a team optimizes for speed over years.

Agent guidance:

- Treat it as the default failure mode of any system without structural governance, not as a rare accident.
- Recommend automated structural checks (dependency rules, cycle detection, coupling metrics) early, while they are cheap.
- When asked to rescue such a system, first make coupling visible (dependency visualization), then carve boundaries incrementally; avoid a big-bang rewrite plan as the first proposal.

## Unitary architecture

The earliest arrangement: software and hardware as one entity, later separating as needs grew (mainframes splitting data off into its own system; single PCs giving way to networked client/server). Today unitary systems survive mostly in embedded and tightly constrained environments. Most systems accumulate features until separation of concerns becomes necessary to preserve operational characteristics such as performance and scale.

## Client/server (two-tier) variants

The basic move: separate frontend from backend. Three historical flavors, each a reaction to the platform's capabilities:

1. **Desktop plus database server.** Rich desktop UI holds presentation logic; heavy data work runs on a separate, more powerful database server reachable over standard network protocols.
2. **Browser plus web server.** Thinner client, wider reach (inside and outside the firewall). Even with a separate database server, practitioners often still call it two-tier because the web and database servers sit together in the data center while the UI lives in the browser.
3. **Single-page JavaScript app.** Effectively the rich-desktop model reborn inside the browser, made possible by faster JavaScript engines.

Takeaway: layering between parts of a system is permanent; where the lines fall shifts with platform capability.

## Three-tier

Popular in the late 1990s alongside Java and .NET application servers: a database tier, an application tier on an application server, and a generated-HTML (later JavaScript) frontend. Distribution relied on protocols such as CORBA and DCOM. The plumbing those tools provided now lives in commodity infrastructure (message queues) or in named styles (event-driven architecture), so architects rarely deal with it directly.

## Lesson: decisions outlive the style that motivated them

Java's designers assumed three-tier would last, so they built object serialization into the core language. The style faded; serialization stayed, and every new language feature must still accommodate it for compatibility.

Rules to apply:

- Be wary of baking the currently fashionable style into foundations that are expensive to change (languages, platform contracts, shared schemas, wire formats).
- Prefer simple designs explicitly as a hedge against an unpredictable future; simplicity keeps options open.
- In an ADR, record which assumptions about the future a decision depends on, so a later reader can tell when they no longer hold.

## Review questions (original)

1. For the system under discussion, what is its position on each of the five style dimensions?
2. Which ecosystem capability does the proposed style depend on, and does the organization have it today?
3. What structural checks would detect drift toward a Big Ball of Mud before it becomes expensive?
4. Which current decisions would be painful to unwind if today's dominant style falls out of favor?
