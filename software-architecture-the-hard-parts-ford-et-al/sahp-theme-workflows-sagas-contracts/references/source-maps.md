# Source maps: book sections to reference files

File names below are the chapter-prefixed names used in this folder.

## Source Map: Chapter 11, Managing Distributed Workflows

| Chapter section | Covered in |
|---|---|
| Chapter introduction (coordination as a dynamic coupling dimension; orchestration vs choreography topology) | ch11-orchestration-vs-choreography.md, SKILL.md |
| Orchestration Communication Style | ch11-orchestration-vs-choreography.md |
| Choreography Communication Style | ch11-orchestration-vs-choreography.md, ch11-semantic-vs-implementation-coupling.md |
| (Semantic coupling and technical vs domain partitioning, within Choreography) | ch11-semantic-vs-implementation-coupling.md |
| Workflow State Management | ch11-choreography-workflow-state.md |
| Trade-Offs Between Orchestration and Choreography | ch11-orchestration-vs-choreography.md |
| State Owner and Coupling | ch11-orchestration-vs-choreography.md, ch11-choreography-workflow-state.md |
| Sysops Squad Saga: Managing Workflows (scenario-driven comparison and ADR) | ch11-orchestration-vs-choreography.md (Scenario-driven comparison and ADR) |

## Source Map: Chapter 12, Transactional Sagas

| Chapter section | Reference file |
|---|---|
| Chapter opening (saga origins, Sysops Squad framing) | ch12-saga-pattern-catalog.md |
| Transactional Saga Patterns | ch12-saga-pattern-catalog.md |
| Epic Saga(sao) | ch12-saga-pattern-catalog.md; ch12-compensation-vs-state-management.md |
| Phone Tag Saga(sac) Pattern | ch12-saga-pattern-catalog.md |
| Fairy Tale Saga(seo) Pattern | ch12-saga-pattern-catalog.md |
| Time Travel Saga(sec) Pattern | ch12-saga-pattern-catalog.md |
| Fantasy Fiction Saga(aao) Pattern | ch12-saga-pattern-catalog.md |
| Horror Story(aac) Pattern | ch12-saga-pattern-catalog.md |
| Parallel Saga(aeo) Pattern | ch12-saga-pattern-catalog.md |
| Anthology Saga(aec) Pattern | ch12-saga-pattern-catalog.md |
| State Management and Eventual Consistency | ch12-compensation-vs-state-management.md |
| Saga State Machines | ch12-saga-state-machines-and-tooling.md |
| Techniques For Managing Sagas | ch12-saga-state-machines-and-tooling.md |
| What Next? | ch12-saga-pattern-catalog.md (selection playbook) |
| Sysops Squad Saga: Atomic Transactions and Compensating Updates | ch12-compensation-vs-state-management.md |

Story note: the chapter's narrative shows a team discovering that a ticket-completion workflow designed as an atomic, orchestrated saga leaks side effects, can fail during compensation, and blocks the field expert on a survey step; it ends by steering toward state-managed eventual consistency. The references use invented examples instead.

## Source Map: Chapter 13 "Contracts"

| Chapter section | Covered in |
|---|---|
| Chapter introduction (contracts as a cross-cutting force; broad definition) | ch13-strict-vs-loose-contracts.md (Broad definition of a contract) |
| Strict versus Loose Contracts | ch13-strict-vs-loose-contracts.md (The strictness spectrum; Need-to-know contracts and GraphQL/REST) |
| Trade-offs Between Strict versus Loose Contracts | ch13-strict-vs-loose-contracts.md (Choosing strictness per edge) |
| Strict Contracts | ch13-strict-vs-loose-contracts.md (What strict contracts give and cost; Versioning policy checklist) |
| Loose Contracts | ch13-strict-vs-loose-contracts.md (What loose contracts give and cost) |
| Contracts in microservices | ch13-consumer-driven-contracts.md (The three decisions) |
| Coupling Levels | ch13-consumer-driven-contracts.md (Coupling levels for shared domain data) |
| Consumer-driven Contracts | ch13-consumer-driven-contracts.md (Push versus pull; Strengths and weaknesses; Readiness checklist) |
| Stamp Coupling | ch13-stamp-coupling.md (What stamp coupling is; Industry documents) |
| Over-coupling via Stamp Coupling | ch13-stamp-coupling.md (Accidental stamp coupling) |
| Bandwidth | ch13-stamp-coupling.md (Bandwidth: the cost model); scripts/contract_usage.py |
| Stamp Coupling for Workflow Management | ch13-stamp-coupling.md (Stamp coupling for workflow management; Strengths and weaknesses) |
| Sysops Squad Saga: Managing Ticketing Contracts | ch13-strict-vs-loose-contracts.md (Worked example: one workflow, mixed strictness). The story shows strictness chosen per collaborator in one workflow, with a loose contract for an app-store mobile client. |
