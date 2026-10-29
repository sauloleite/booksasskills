# Source maps: book sections to reference files

File names below are the chapter-prefixed names used in this folder.

## Source Map: Chapter 7, Service Granularity

| Chapter section | Covered in |
|---|---|
| Opening story (team debates how small services should be) | ch07-balancing-and-trade-off-negotiation.md (Why balance, not rules) |
| Modularity versus granularity; size metrics | ch07-sizing-metrics-and-disintegrators.md |
| Granularity Disintegrators | ch07-sizing-metrics-and-disintegrators.md |
| Service Scope and Function | ch07-sizing-metrics-and-disintegrators.md |
| Code Volatility | ch07-sizing-metrics-and-disintegrators.md |
| Scalability and Throughput | ch07-sizing-metrics-and-disintegrators.md |
| Fault Tolerance | ch07-sizing-metrics-and-disintegrators.md (plus leftover-cohesion and naming test) |
| Security | ch07-sizing-metrics-and-disintegrators.md |
| Extensibility | ch07-sizing-metrics-and-disintegrators.md |
| Granularity Integrators | ch07-granularity-integrators.md |
| Database Transactions | ch07-granularity-integrators.md |
| Workflow and Choreography | ch07-granularity-integrators.md |
| Shared Code | ch07-granularity-integrators.md |
| Data Relationships | ch07-granularity-integrators.md; scripts/granularity_drivers.py datamap |
| Finding The Right Balance | ch07-balancing-and-trade-off-negotiation.md; scripts/granularity_drivers.py assess |
| Sysops Squad Saga: Ticket Assignment Granularity | ch07-balancing-and-trade-off-negotiation.md (Lessons from the case studies, Worked example A) |
| Sysops Squad Saga: Customer Registration Granularity | ch07-balancing-and-trade-off-negotiation.md (Lessons from the case studies; Design versus architecture; Worked example B) |

## Source map: Chapter 8, Reuse Patterns

| Chapter section | Covered in |
|---|---|
| Part II introduction (Putting Things Back Together) | SKILL.md (purpose) |
| Chapter opening story (single versus multiple shared libraries, library versus service) | ch08-replication-and-shared-libraries.md, ch08-shared-services.md |
| Chapter introduction (reuse in distributed systems, share nothing, WET versus DRY) | ch08-replication-and-shared-libraries.md (Context) |
| Code Replication | ch08-replication-and-shared-libraries.md |
| Code Replication: When To Use | ch08-replication-and-shared-libraries.md |
| Shared Library | ch08-replication-and-shared-libraries.md |
| Dependency Management and Change Control | ch08-replication-and-shared-libraries.md |
| Versioning Strategies | ch08-replication-and-shared-libraries.md |
| Shared Library: When To Use | ch08-replication-and-shared-libraries.md |
| Shared Service | ch08-shared-services.md |
| Change Risk | ch08-shared-services.md |
| Performance | ch08-shared-services.md |
| Scalability | ch08-shared-services.md |
| Fault Tolerance | ch08-shared-services.md |
| Shared Service: When To Use | ch08-shared-services.md |
| Sidecars and Service Mesh | ch08-sidecars-and-orthogonal-reuse.md |
| Sidebar: Orthogonal Coupling | ch08-sidecars-and-orthogonal-reuse.md |
| Sidecars and Service Mesh: When To Use | ch08-sidecars-and-orthogonal-reuse.md |
| Sysops Squad Saga: Common Infrastructure Logic | ch08-sidecars-and-orthogonal-reuse.md (what belongs in the sidecar, ownership) |
| Code Reuse: When Does It Add Value? | ch08-reuse-value-and-platforms.md |
| Sidebar: Reuse | ch08-reuse-value-and-platforms.md (abstraction versus rate of change) |
| Reuse via Platforms | ch08-reuse-value-and-platforms.md |
| Sysops Squad Saga: Shared Domain Functionality | ch08-shared-services.md (worked example) |

The four techniques are compared side by side in ch08-reuse-value-and-platforms.md. No scripts: the chapter has no calculations.
