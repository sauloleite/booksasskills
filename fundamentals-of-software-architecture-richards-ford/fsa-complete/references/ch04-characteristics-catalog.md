# Characteristics Catalog and Shared Vocabulary

## Contents
- How to use this catalog
- Operational characteristics
- Structural characteristics
- Cloud characteristics
- Cross-cutting characteristics
- Ambiguous and overlapping terms
- ISO-style families and the functional suitability exception
- Building an organizational glossary

## How to use this catalog

Characteristics range from code-level concerns (modularity) to sophisticated runtime concerns (scalability, elasticity). No authoritative universal list exists, every organization reads the terms differently, and new ones keep appearing as the ecosystem evolves. Use the categories below as a blind-spot checklist, not as a menu to adopt wholesale. For each entry, the "probe" is a question an agent can put to stakeholders.

## Operational characteristics

Runtime capabilities; they overlap heavily with operations and DevOps and are the most likely to need structural support.

- **Availability**: share of time the system must be usable; for round-the-clock service, fast recovery mechanisms. Probe: what does an hour of downtime cost, and when?
- **Continuity**: disaster recovery capability. Probe: what happens if a whole site or region is lost?
- **Performance**: responsiveness and throughput, assessed through stress tests, peak analysis, usage frequency of functions, and response times. Probe: which operations are latency-sensitive, and at what percentile?
- **Recoverability**: how fast the system must return after a disaster, including backups and spare hardware. Probe: target recovery time and acceptable data loss?
- **Reliability / safety**: whether failure endangers lives or causes major financial loss; usually a spectrum, not a yes/no. Probe: what is the worst credible consequence of a failure?
- **Robustness**: graceful handling of errors and edge conditions at runtime, such as losing power or connectivity. Probe: which external dependencies can disappear mid-operation?
- **Scalability**: keeping performance as users or requests grow. Probe: expected growth curve and peak multiplier?

## Structural characteristics

Internal code quality the architect owns fully or jointly: modularity, readability, controlled coupling, and similar.

- **Configurability**: end users adjusting behavior through interfaces.
- **Extensibility**: adding functionality without disruptive rework.
- **Installability**: ease of installing on every required platform.
- **Leverageability / reuse**: sharing common components across products.
- **Localization**: multilingual support in data entry and query screens.
- **Maintainability**: ease of changing and enhancing the system.
- **Portability**: running on more than one platform (for example, different database engines).
- **Upgradeability**: speed and ease of moving servers and clients to new versions.

## Cloud characteristics

Added because most systems now touch cloud services in some way. These describe what the provider offers and what the design can rely on.

- **On-demand scalability**: provider grows resources as demand rises.
- **On-demand elasticity**: provider absorbs sudden spikes; close cousin of scalability, focused on bursts.
- **Zone-based availability**: spreading resources across compute zones for resilience.
- **Region-based privacy and security**: legal capacity to keep data in specific countries; many jurisdictions restrict where citizens' data may live.

Agent guidance: when a style is under consideration, ask how it uses these provider capabilities (the book adds a cloud section to each style chapter).

## Cross-cutting characteristics

Concerns that resist neat categories but still constrain design.

- **Accessibility**: usable by everyone, including people with color blindness, hearing loss, or other disabilities.
- **Archivability**: rules for archiving or deleting data after a set period.
- **Authentication**: confirming identity.
- **Authorization**: limiting what each user may reach, at granularities from subsystem down to field.
- **Legal**: regulatory constraints (GDPR, Sarbanes-Oxley, rules on building or deploying the application, rights the company must reserve).
- **Privacy**: concealing transactions even from insiders such as DBAs and network architects.
- **Security**: encryption in storage and between internal systems, remote access authentication, and related controls.
- **Supportability**: needed level of technical support, logging, and debugging facilities.
- **Usability / achievability**: how much training users need to reach their goals.

## Ambiguous and overlapping terms

Any list is incomplete, and projects legitimately invent characteristics for unique needs. Many terms are vague or have no objective definition. Watch for:

- **Interoperability vs. compatibility**: sometimes interchangeable, but interoperability stresses easy integration with other systems (implying published, documented APIs), while compatibility stresses conformance to industry and domain standards.
- **Learnability**: either how quickly people learn the software, or how well the system learns its environment to configure or optimize itself with machine learning. Always clarify which.
- **Availability vs. reliability**: related but distinct. IP is a useful illustration: it is available, yet packets can arrive out of order or be lost, so receivers must request retransmission; it is not reliable on its own.

## ISO-style families and the functional suitability exception

The ISO quality model groups capabilities into families with subcharacteristics. It overlaps the categories above and is also incomplete. In summary form:

- **Performance efficiency**: time behavior, resource utilization, capacity relative to resources consumed.
- **Compatibility**: coexistence in a shared environment, and interoperability (exchanging and using information).
- **Usability**: recognizing fitness for one's needs, learnability, protection from user mistakes, accessibility.
- **Reliability**: maturity under normal load, availability, fault tolerance, recoverability of data and state.
- **Security**: confidentiality, integrity, nonrepudiation, accountability (tracing user actions), authenticity.
- **Maintainability**: modularity, reusability, analyzability (ease of obtaining metrics), modifiability without regressions, testability.
- **Portability**: adaptability to new environments, installability and uninstallability, replaceability.
- **Functional suitability**: completeness, correctness, appropriateness of functions.

The authors exclude functional suitability: it expresses the reason the software exists (domain motivation), not an architecture characteristic. This reflects an evolving view of how characteristics relate to the domain. Agent guidance: when a stakeholder lists "correctness" or "feature completeness" as a quality goal, route it to domain requirements and testing, not to the characteristics list.

## Building an organizational glossary

Because there is no standard nomenclature (even "software architecture" itself lacks one), teams use opaque terms or the same word for different meanings. Follow the domain-driven design advice: establish a ubiquitous language.

Glossary entry template:

```
term: availability
definition: fraction of a calendar month the public API answers health checks
measure: synthetic probe every 60 s from two regions
target_examples: 99.9% for checkout, 99% for reporting
not_to_confuse_with: reliability (correctness of delivered results)
owner: platform architecture
```

Rules: one meaning per term; include a measurable definition; note look-alike terms; revisit when new characteristics emerge.
