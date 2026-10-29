# Source Map: Chapter 12, Transactional Sagas

| Chapter section | Reference file |
|---|---|
| Chapter opening (saga origins, Sysops Squad framing) | saga-pattern-catalog.md |
| Transactional Saga Patterns | saga-pattern-catalog.md |
| Epic Saga(sao) | saga-pattern-catalog.md; compensation-vs-state-management.md |
| Phone Tag Saga(sac) Pattern | saga-pattern-catalog.md |
| Fairy Tale Saga(seo) Pattern | saga-pattern-catalog.md |
| Time Travel Saga(sec) Pattern | saga-pattern-catalog.md |
| Fantasy Fiction Saga(aao) Pattern | saga-pattern-catalog.md |
| Horror Story(aac) Pattern | saga-pattern-catalog.md |
| Parallel Saga(aeo) Pattern | saga-pattern-catalog.md |
| Anthology Saga(aec) Pattern | saga-pattern-catalog.md |
| State Management and Eventual Consistency | compensation-vs-state-management.md |
| Saga State Machines | saga-state-machines-and-tooling.md |
| Techniques For Managing Sagas | saga-state-machines-and-tooling.md |
| What Next? | saga-pattern-catalog.md (selection playbook) |
| Sysops Squad Saga: Atomic Transactions and Compensating Updates | compensation-vs-state-management.md |

Story note: the chapter's narrative shows a team discovering that a ticket-completion workflow designed as an atomic, orchestrated saga leaks side effects, can fail during compensation, and blocks the field expert on a survey step; it ends by steering toward state-managed eventual consistency. The references use invented examples instead.
