---
name: sahp-ch12-transactional-sagas
description: Guides the choice and implementation of distributed transactional sagas using the eight combinations of communication (sync/async), consistency (atomic/eventual) and coordination (orchestrated/choreographed), compensating updates versus state management, saga state machines and saga tagging. Based on Chapter 12 of Ford, Richards, Sadalage and Dehghani's "Software Architecture: The Hard Parts". Use when designing a multi-service workflow, picking a saga pattern, replacing a slow atomic saga, handling failed steps, or auditing which services join which saga.
---

# SAHP Chapter 12: Transactional Sagas

## Purpose

This skill helps an agent design and critique workflows that write data across several services. It treats a saga not as one pattern but as a point in a space of three entangled forces (communication, consistency, coordination), giving eight variants with very different coupling, complexity, responsiveness and scale profiles. It also covers how to handle failure (undo with compensating updates or repair forward with a state machine) and how to keep track of every saga a system contains. Apply it whenever a request involves "all of these must succeed together" across service boundaries.

## Key decision rules (apply without opening references)

1. **Name the saga by its three forces.** Code letters in order communication, consistency, coordination: sao Epic, sac Phone Tag, seo Fairy Tale, sec Time Travel, aao Fantasy Fiction, aac Horror Story, aeo Parallel, aec Anthology. Always state the triple, not just the nickname.
2. **Atomicity is the costliest force.** Challenge every "must be atomic" requirement; ask what actually breaks if a step completes later. Dropping to eventual consistency usually yields the biggest gain in scale, responsiveness and simplicity.
3. **Do not default to the Epic Saga (sao)** just because it resembles the monolith. It is the most tightly coupled option; its orchestrator becomes a timing bottleneck and any unavailable participant fails the request. A pattern having a name does not mean the problem is cleanly solvable.
4. **Never speed up an atomic saga by adding asynchrony.** That produces Fantasy Fiction (aao); adding choreography too produces the Horror Story (aac), the most complex corner. Relax consistency instead: go to Parallel (aeo) or Anthology (aec).
5. **Mediator value grows with workflow complexity.** Complex or error-prone workflows: orchestrate. Choreography fits simple, mostly linear flows; otherwise domain services quietly absorb mediator logic.
6. **Balanced defaults.** Fairy Tale (seo) when eventual consistency is acceptable and load is moderate; Parallel (aeo) for complex workflows needing high scale; Time Travel (sec) as an on-ramp to Anthology (aec) for high-throughput pipelines with rare errors.
7. **Phone Tag (sac)** only for short atomic chains with few error paths, idempotent participants and retries.
8. **Compensating updates are fragile.** No isolation (others act on interim data), irreversible downstream side effects, compensation that can itself fail, slow error responses, a lock-or-not dilemma, and users coupled to steps they do not own. Plan for each explicitly or avoid compensation.
9. **Prefer state management for non-critical steps.** Move the saga to an explicit error state, answer the user, retry in the background, escalate to a human if retries fail. Accept a bounded window where data is out of sync.
10. **Always know the state of every distributed transaction**, whichever error technique is used. Model sagas as finite state machines with one entry, named terminal states, explicit wait and error states, and a transition table.
11. **Sagas are built, not bought.** Keep one central list of sagas in code and tag each service entry point with the sagas it joins; use a code-walk tool for test scoping and impact analysis.
12. **No universal answer.** Pick per workflow and record the trade-off accepted on each axis.

## Default workflow

1. Write the workflow as numbered steps; mark which ones the initiating user must wait for.
2. Establish the real consistency need per step (atomic vs. eventual) with the business.
3. Judge workflow complexity and error frequency; decide orchestration vs. choreography.
4. Decide sync vs. async from responsiveness and scale targets; stay sync if it is enough.
5. Map the triple to a pattern; if it is aao or aac, redesign.
6. Choose the error technique per step: compensation (only if truly atomic and side-effect-free) or state-managed repair.
7. Draw the saga state machine and transition table; run `scripts/saga_check.py` on the definition.
8. Register the saga in the central saga list and tag participating services.
9. Document the decision with qualitative trade-offs; revisit as load or workflow complexity changes.

## References

- [references/saga-pattern-catalog.md](references/saga-pattern-catalog.md): read when choosing or critiquing a saga pattern, explaining one of the eight variants, or redesigning a slow or fragile atomic workflow.
- [references/compensation-vs-state-management.md](references/compensation-vs-state-management.md): read when deciding how a saga handles a failed step, diagnosing compensation problems (side effects, failed undo, isolation), or converting an atomic saga to eventual consistency.
- [references/saga-state-machines-and-tooling.md](references/saga-state-machines-and-tooling.md): read when modeling a saga as a state machine, writing its transition table, or setting up saga annotations and an inventory tool.
- [references/source-map.md](references/source-map.md): read to see which reference covers each chapter section.

## Scripts

- `scripts/saga_check.py` (Python 3 stdlib). Run `python3 scripts/saga_check.py saga.json` to identify the pattern code from the declared forces, list steps lacking compensation and explain the implication under the declared consistency model, flag side effects, non-idempotent compensations, user coupling and risky force combinations, and check an optional state machine for unreachable, dead-end or non-terminating states. Add `--json` for machine output and `--strict` to exit 1 when step or state findings exist. Input schema is in the script docstring; `--help` lists options.
