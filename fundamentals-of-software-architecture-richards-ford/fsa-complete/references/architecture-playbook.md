# Architecture playbook and cross-chapter decisions (Fundamentals of Software Architecture)

Whole-book synthesis: an end-to-end architecture workflow, a symptom-to-fix map that crosses chapters, and a review checklist. Chapter tags such as (ch07) point to the `chNN-*` reference files in this folder.

## Contents
- End-to-end workflow
- Symptom-to-fix map
- Architecture review checklist
- Book-wide pitfalls

## End-to-end workflow

### 1. Understand the problem and context (ch01, ch02, ch05)
- Clarify business drivers and translate them into candidate characteristics; dig out implicit ones from the domain.
- Separate architectural decisions from design decisions by reversibility and scope.
- Note constraints: budget, time, team skills, enterprise standards, existing data.

### 2. Define and prioritize characteristics (ch04, ch05, ch06)
- Filter candidates with the three-part test; decompose composites into measurable parts.
- Reduce to a short driving list and a top three chosen with stakeholders.
- Write an objective measure for each, with percentiles or budgets where relevant.

### 3. Identify logical components (ch08, ch03)
- Seed components from actors and actions or from workflows; assign stories; test each responsibility statement for cohesion.
- Let differing characteristics split components; measure coupling (`scripts/component_coupling.py`) and modularity (`scripts/modularity_metrics.py`).

### 4. Scope characteristics and find quanta (ch07)
- Group components whose characteristics match; map shared data stores and synchronous calls (`scripts/quantum_finder.py`).
- One set of characteristics points to a monolith; several sets point to a distributed style.

### 5. Choose the style and patterns (ch09, ch19, ch20, ch10 to ch18)
- Check the cost of distribution (`scripts/call_chain_budget.py`) and choose technical or domain partitioning.
- Shortlist styles whose strengths match the driving characteristics and whose shape matches the problem.
- Decide data placement and communication per boundary, defaulting to synchronous.
- Add patterns (sidecar and mesh, orchestration or choreography, CQRS, broker topology) with explicit trade-offs.

### 6. Record and govern (ch21, ch06)
- Write ADRs for the significant decisions and route them for approval (`scripts/adr_check.py`).
- Encode structure and characteristics as fitness functions: cycles and layers (`scripts/dependency_fitness.py`, `scripts/layer_rules_check.py`), module boundaries (`scripts/check_module_boundaries.py`), complexity (`scripts/complexity_gate.py`), service coupling (`scripts/coupling_audit.py`).

### 7. Assess risk (ch22)
- Score characteristics by domain area, risk storm with the team (`scripts/risk_storm.py`), and agree mitigations with budget holders.

### 8. Communicate and lead (ch23, ch24, ch25)
- Draw layered, consistent diagrams for each audience.
- Set your involvement level (`scripts/involvement_score.py`), negotiate with evidence (`scripts/availability_budget.py`), and keep teams in the loop.

### 9. Align and evolve (ch26, ch27)
- Check implementation, infrastructure, data, practices, team topology, integration, standards, business context and AI use against the architecture.
- Revisit trade-offs as context changes (`scripts/tradeoff_matrix.py`); analysis is never finished.

## Symptom-to-fix map

| Symptom | Likely cause | First move | Then |
|---|---|---|---|
| Every change touches many layers or teams | Technical partitioning against domain-shaped change | Reassess top-level partitioning (ch09) | Modular monolith or service-based (ch11, ch14) |
| Most requests just pass through layers | Architecture sinkhole | Measure pass-through share (ch10) | Open layers deliberately or change style (ch10, ch19) |
| Services must deploy together | Shared database or synchronous chains fuse quanta | Find quanta (ch07) | Split data, add asynchronous links (ch18, ch15) |
| Microservices slow and chatty | Granularity too fine | Coupling audit (ch18) | Merge services by transaction and chattiness (ch18) |
| Distributed transactions everywhere | Wrong boundaries or style | Regroup services (ch18) | Consider service-based (ch14) |
| Event flows hard to follow or loop | Unbounded choreography | Lint the event model (ch15) | Mediator for complex workflows (ch15, ch20) |
| Shared code changes break many services | Domain reuse creating coupling | Duplicate domain code, reuse plumbing (ch27, ch20) | Sidecars for operational concerns (ch18, ch20) |
| Characteristics argued but never met | Vague definitions, no governance | Measurable definitions (ch06) | Fitness functions in CI (ch06) |
| Same decision debated repeatedly | Missing rationale | ADR with justification (ch21) | Single system of record (ch21) |
| Stakeholders demand extreme targets | Untranslated expectations | Convert to concrete downtime and cost (ch25) | Scope the demand to where it matters (ch25) |
| Design ignored in implementation | Weak collaboration or governance | Right-size involvement and constraints (ch24) | Align intersections and automate checks (ch26) |

## Architecture review checklist

- [ ] Driving characteristics are few, measurable and agreed, with a top three.
- [ ] Logical components have clear responsibilities and measured coupling.
- [ ] Quanta are identified and justify the monolith versus distributed choice.
- [ ] The style's strengths match the drivers and its known weaknesses have mitigations.
- [ ] Data placement and synchronous versus asynchronous choices are explicit per boundary.
- [ ] Significant decisions have ADRs with business and technical justification.
- [ ] Fitness functions guard structure and the top characteristics.
- [ ] A current risk assessment exists with agreed mitigations.
- [ ] Diagrams show topology consistently and include keys.
- [ ] Team structure, infrastructure, data and practices align with the architecture.

## Book-wide pitfalls

- Treating a pattern or style as a universal best practice instead of a context-specific trade-off.
- Choosing a style by fashion before analyzing characteristics and quanta.
- Specifying too many characteristics, or none measurably.
- Splitting services too finely and rebuilding a distributed monolith.
- Reusing domain logic across boundaries and calling it efficiency.
- Leaving decisions undocumented or buried in email.
- Dictating to teams instead of collaborating, or disappearing entirely.
