# Hard parts playbook and cross-chapter decisions (Software Architecture: The Hard Parts)

Whole-book synthesis: a migration playbook from monolith to distributed system, a symptom-to-fix map that crosses chapters, and a review checklist. Chapter tags such as (ch09) point to the `chNN-*` reference files in this folder.

## Contents
- Migration playbook
- Symptom-to-fix map
- Review checklist
- Book-wide pitfalls

## Migration playbook

### 1. Justify and frame (ch01, ch03, ch15)
- Tie the migration to speed to market or competitive advantage and to observed problems.
- Record the business case and accepted costs in an ADR.
- List the entangled decisions you will face and agree how trade-offs will be presented.

### 2. Understand coupling (ch02)
- Build a static coupling inventory and identify current quanta (`scripts/quantum_coupling.py`).
- Note synchronous call chains and their operational mismatches.

### 3. Assess and decompose code (ch04, ch05)
- Measure decomposability (`scripts/decomposability_metrics.py`) and pick component-based decomposition or tactical forking.
- Apply the component patterns in order, sizing with `scripts/component_sizing.py` and keeping every pattern as a CI check.
- Group components into domains with business stakeholders and extract coarse domain services first.

### 4. Decompose data (ch06)
- Decide whether to split the database, map data domains and break cross-domain links (`scripts/data_domain_check.py`).
- Migrate in stages through schemas, service restrictions and separate servers; manage connections (`scripts/connection_budget.py`).

### 5. Size services (ch07, ch08)
- Evaluate disintegrators and integrators with real measurements (`scripts/granularity_drivers.py`).
- Decide how shared code is packaged: library, service, replication or sidecar.

### 6. Assign ownership and access (ch09, ch10)
- Classify table ownership and resolve joint cases (`scripts/data_ownership.py`).
- Pick consistency patterns for distributed writes and read-access patterns for foreign data (`scripts/replicated_cache_sizing.py`).

### 7. Design workflows, transactions and contracts (ch11, ch12, ch13)
- Choose orchestration or choreography per workflow and decide where state lives.
- Choose a saga variant, prefer state management over compensation, and validate the state machine (`scripts/saga_check.py`).
- Set contract strictness per integration and remove stamp coupling (`scripts/contract_usage.py`).

### 8. Design analytics (ch14)
- Replace or complement warehouse and lake with domain-owned data products; enforce completeness (`scripts/daily_completeness_check.py`).

### 9. Keep analyzing (ch15)
- Re-run weighted trade-off analysis as context changes (`scripts/tradeoff_worksheet.py`).

## Symptom-to-fix map

| Symptom | Likely cause | First move | Then |
|---|---|---|---|
| Services must deploy together | Shared data or code, synchronous chains | Map quanta (ch02) | Split data domains, add async links (ch06, ch12) |
| Migration produced a distributed monolith | Piecemeal extraction, services too fine | Reassess decomposition approach (ch04) | Merge by integrators, go service-based (ch07, ch05) |
| One giant component dominates | Poor component sizing | Size components (ch05) | Split by subdomain, flatten namespaces (ch05) |
| Cross-service writes keep failing midway | Distributed transactions with weak error handling | Choose saga variant and state management (ch12) | Reconsider granularity or consolidate (ch07, ch09) |
| Several services write the same table | Joint ownership | Classify ownership (ch09) | Split, delegate, share domain or consolidate (ch09) |
| Reads of foreign data are slow or fragile | Synchronous inter-service calls | Evaluate read-access patterns (ch10) | Replicated cache or column replication (ch10) |
| Shared library change breaks many services | Domain code reused across boundaries | Assess volatility (ch08) | Duplicate or move to a shared service (ch08) |
| Choreographed workflow is hard to debug | Complex errors without central control | Compare on failure paths (ch11) | Introduce an orchestrator for that workflow (ch11) |
| Contract changes ripple everywhere | Overly strict or bloated contracts | Measure field usage (ch13) | Looser contracts with consumer-driven tests (ch13) |
| Analytics breaks when services change | Centralized pipelines coupled to schemas | Data products per domain (ch14) | Contract and completeness fitness functions (ch14) |

## Review checklist

- [ ] The business driver and accepted costs are recorded in an ADR.
- [ ] Quanta and coupling are mapped, including synchronous chains.
- [ ] Decomposition followed an explicit approach and patterns are guarded in CI.
- [ ] The database split follows data domains, with ownership assigned to writers.
- [ ] Service boundaries were tested against both disintegrators and integrators.
- [ ] Each cross-service read and write has a chosen pattern and consistency model.
- [ ] Each workflow has a coordination style, saga variant and error-handling approach.
- [ ] Contracts are as loose as governance allows and free of unused payload.
- [ ] Analytical data is owned by domains and validated by fitness functions.
- [ ] Trade-off analyses are revisited when context changes.

## Book-wide pitfalls

- Looking for a best practice instead of analyzing the trade-offs at hand.
- Splitting code without splitting data, or splitting data without assigning ownership.
- Going straight to fine-grained microservices.
- Keeping atomic consistency across services by default.
- Reusing domain code across services and calling it efficiency.
- Letting choreography grow until domain services carry hidden workflow logic.
- Treating analytics as an afterthought fed by fragile pipelines.
