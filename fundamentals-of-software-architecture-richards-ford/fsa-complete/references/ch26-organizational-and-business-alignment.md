# Organizational and Business Alignment

## Contents
- Engineering practices
- Fitness functions as the alignment check
- Team topologies
- Systems integration
- Enterprise standards
- Business environment and domain-to-architecture isomorphism
- Unknown unknowns and evolutionary design
- Residuality theory
- Glossary

## Engineering practices

Separate two things that are often conflated:
- **Process**: how people are organized and coordinated (team formation, meetings, workflow). Waterfall, Scrum, Lean, Crystal.
- **Engineering practices**: process-independent techniques and tools for building and shipping software. XP practices, continuous integration, continuous delivery, TDD.

Software engineering covers both. Engineering practices matter to the architect because software is far less predictable than physical engineering; estimation (time, people, money) is the weak spot, partly because classic estimation assumes away the exploratory nature of building software.

Guidance:
- Process is mostly orthogonal to architecture, but iterative processes suit it better. A modern distributed style run under a heavy up-front Waterfall plan creates constant friction.
- Agile processes are especially valuable when migrating from one style to another: short feedback loops make incremental techniques like the Strangler Fig approach and feature toggles practical.
- The architect, often also the technical lead, should choose engineering practices that fit the style. Microservices presumes automated provisioning, automated testing and automated deployment. A team with manual operations and thin test coverage attempting microservices is likely to fail.
- Just as domains favor certain styles, so do engineering cultures. Assess the team's practices before recommending a style.

## Fitness functions as the alignment check

Evolutionary architecture (Ford's Building Evolutionary Architectures) uses fitness functions to protect characteristics as the system changes. A fitness function is any objective check of a characteristic: metrics, unit tests, monitors, chaos experiments.

Use them to detect practice misalignment. Example: the business wants fast time to market, which maps to agility, a composite of maintainability, testability and deployability. Microservices and service-based architecture both support agility in principle, but only if practices deliver it. Track fitness functions such as:
- lead time from commit to production,
- deployment frequency and failed deployment rate,
- automated test coverage of changed code and test suite duration,
- coupling or complexity metrics per component.

If they trend the wrong way, realign either the practices to the architecture or the architecture to the practices.

## Team topologies

Teams, like architectures, are partitioned either by domain or by technical function.
- **Domain-partitioned teams** are cross-functional and own a business area end to end, from UI to data. They fit domain-partitioned styles (microservices, service-based, modular monolith).
- **Technically partitioned teams** own one technical layer or function: UI, backend, shared services, database. They fit the layered style. A different technical split, business-logic teams plus data-synchronization teams, fits space-based architecture.

Mismatch symptom: even small features need coordination across several teams and drag on. If you see that, compare the team cut with the architecture cut before blaming the design or the people.

## Systems integration

Few systems stand alone. When your system calls another, check:
- Is the other system available when you need it?
- Does it scale and respond at the level your system requires?
- Which protocol and which contract type (strict or loose) will you use?
- Are the two systems' characteristics compatible?
- Does the integration preserve each system's architectural quantum, or does synchronous coupling merge them into one quantum with the weakest characteristics of both?

Neglecting this produces static and dynamic coupling that blocks scalability, responsiveness and agility. Mitigations include asynchronous messaging, caching of the callee's data, timeouts and circuit breakers, and contracts that tolerate change.

## Enterprise standards

The enterprise means all systems and products in the company or division. Enterprises impose standards on security, platforms, technologies, documentation and diagramming regardless of system type. Find them early and conform. The authors' experience: a solution that ignores enterprise standards tends to be labeled a one-off and discarded, no matter how well it works technically. If a standard genuinely blocks a driving characteristic, raise it through governance with an ADR rather than silently deviating.

## Business environment and domain-to-architecture isomorphism

Business conditions shape architecture and keep changing. Assess the company's position:
- Under heavy cost cutting: avoid expensive-to-build-and-run styles such as microservices and space-based.
- Expanding aggressively through mergers and acquisitions: avoid monoliths that cannot evolve or absorb new systems.
- Pivoting every few months in a volatile market: favor evolvability and adaptability.
- Stable and mature: simpler, cheaper styles may be the right fit.

The chapter calls the match between business situation and architecture shape domain-to-architecture isomorphism.

## Unknown unknowns and evolutionary design

Systems usually begin with known unknowns (things the team knows it must learn). The real danger is unknown unknowns: surprises nobody anticipated. Big Design Up Front cannot plan for them, so every architecture ends up iterating anyway; Mark Richards' point is that Agile simply starts iterating earlier.

Responses:
- Evolutionary architecture with fitness functions.
- Iterative architecture work rather than a frozen up-front design.
- Prioritize change-friendly characteristics: portability, scalability, evolvability, adaptability.

## Residuality theory

Barry O'Reilly's residuality theory (book: Residues, 2024) treats business changes as stressors and each architectural response as a residue. As residues accumulate, the architecture begins to cope with changes nobody predicted, approaching a critical state in complexity-theory terms. The authors present it as promising and under observation, not settled practice. Practical use: list plausible stressors (new regulation, a key vendor failing, a merger, demand doubling), sketch how the architecture would change for each, and look for design changes that address many stressors at once.

## Glossary

- **Intersection**: a facet of the technical or business environment that must align with the architecture for it to succeed.
- **Domain-to-architecture isomorphism**: the fit between the business's situation and direction and the architecture's shape.
- **Stressor / residue**: a business change, and the architectural adaptation that survives it (residuality theory).
- **Architectural quantum**: an independently deployable unit with high functional cohesion and its own set of characteristics.
