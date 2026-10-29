## Contents

- Cloud and serverless
- Common risks
- Governance of coupling
- Team topology alignment
- Strengths and weaknesses
- Fit assessment and worked example
- Further reading

# Risks, Governance, Teams and Fit

## Cloud and serverless

- Runs on premises (Kubernetes, Cloud Foundry) but suits cloud especially well, which is why it is often called cloud-native: on-demand VMs, containers and databases plus managed cloud services align with per-service deployment.
- The authors classify serverless (AWS Lambda, Google Cloud Functions, Azure Functions) as a deployment model of microservices, not a separate style. A function is a single-purpose, separately deployed unit, which matches the definition of a microservice.
- Containers are an equally valid deployment; most cloud vendors offer managed Kubernetes. Choose per service based on load profile and operational preferences, not on style.

## Common risks

| Risk | Symptom | Remedy |
|---|---|---|
| Grains of Sand (services too small; named by Mark Richards in 2016) | Many tiny services, each useless alone | Consolidate around behavior; "micro" refers to scope of responsibility, not size |
| Excess interservice communication | Long call chains, high dynamic coupling, workflow spread across choreography or step functions | Usually a granularity problem: merge into coarser services |
| Over-sharing data | Many services on one schema; slow, risky migrations | Know when sharing is necessary; otherwise consolidate the services |
| Code and functionality reuse via custom libraries | JAR/DLL shared across contexts; a change breaks unrelated services | Duplicate domain code; push operational code into sidecars; version anything that must remain shared, knowing it still adds complexity |

Over-sharing data threatens exactly what the style is best at: change control, scalability, fault tolerance and agility. Service granularity is covered in depth in chapter 7 of "Software Architecture: The Hard Parts".

## Governance of coupling

Governance in this style mostly means preventing structural decay, and most rules target the risks above.

**Static coupling** (shared custom or third-party libraries, and contracts between services):

- Contracts matter most: async messaging removes runtime dependency but the message contract still binds both sides statically.
- Tools: software bill of materials, deployment scripts, dependency managers to count shared artifacts.
- No fixed threshold is given; aim to minimize.

**Dynamic coupling** (runtime calls) is harder to measure and needs consistent instrumentation:

- *Log-based:* each service logs every outgoing call with target, protocol and similar metadata; fitness functions analyze the logs. Consistency is the hard part; one option is a small shared logging library that every service binds to at build time (an accepted, operational form of reuse).
- *Registry-based:* when the first instance of a service starts, it registers its outgoing call dependencies (for example as JSON) in a configuration server such as Apache ZooKeeper. Querying the registry yields a full interservice call map to govern communication volume.

Example fitness functions an agent can propose:

- Fail the build if a service declares a dependency on another team's domain library.
- Alert when any service's outgoing call count exceeds an agreed limit, or when a mutual call pair or cycle appears.
- Fail when more than six services are registered against one schema.

The bundled `scripts/coupling_audit.py` implements these checks over a JSON call map.

## Team topology alignment

The style is domain partitioned, so it works best with cross-functional, domain-aligned teams that can deliver a feature inside one service without stepping on others. Technically partitioned teams (UI, backend, database) need heavy cross-team coordination for every domain change and struggle with it.

| Team type | How it fits |
|---|---|
| Stream-aligned | Works well when each stream maps to a domain. If streams cut across many contexts, either realign service boundaries and granularity to the streams or reconsider the style |
| Enabling | Effective providing shared services for specialized or cross-cutting needs without blocking stream teams; can help platform teams build sidecars |
| Complicated-subsystem | Can own a hard subdomain inside its own services, isolated from others |
| Platform | Builds and maintains common tools, APIs, sidecars and the mesh, relieving stream teams of operational plumbing |

## Strengths and weaknesses

Described qualitatively (no score matrix):

- **Very strong:** deployability and testability (the style depends on DevOps automation), fault tolerance (independent single-purpose services fail alone), scalability, elasticity (automation plus operational integration), evolvability (small, highly decoupled deployment units support fast incremental change).
- **Weak:** performance. Many network hops, per-endpoint security checks, and data latency from multiple database calls per request. Mitigations: smart caching and replication to cut calls, and a preference for choreography to avoid bottlenecks.
- **Structure:** firmly domain partitioned; it has the most distinct architecture quanta of any modern style, serving almost as the textbook case of the quantum concept.
- **Cost and simplicity:** expect high operational cost and complexity from the decoupling; architects should understand the rules well before deliberately bending them.

## Fit assessment and worked example

Good candidates have high functional and data modularity.

Patient monitoring (book's scenario, summarized): each vital sign (heart rate, blood pressure, oxygen, and so on) is an independent service with its own readings and history; a shared alerting service notifies staff on anomalies; each service asynchronously pushes readings to a bedside display service. Occasional cross-signal needs (heart rate analysis consulting sleep data) are exceptions, not the norm. Payoffs: one crashed signal service leaves others running; changes to one signal need only that signal's tests; adding a new signal touches nothing else.

Invented contrast for practice: a general-ledger posting engine where every posting must atomically update journal, balances and audit trail. Low data modularity and pervasive transactions make it a poor fit; a coarser style (service-based or modular monolith) is safer.

Fit questions:

- Can most features be delivered by changing one service?
- Do most requests stay inside one context, or need several?
- Are cross-service transactions rare?
- Is latency budget generous enough for multiple network hops?
- Are teams (or can they become) domain aligned, with platform support for sidecars and mesh?
- Is deployment and testing automation mature?

## Further reading

Newman, "Building Microservices" (2nd ed.); Mezzalira, "Building Micro-Frontends" (2nd ed.); Richards, "Microservices vs. Service-Oriented Architecture" and "Microservices AntiPatterns and Pitfalls".
