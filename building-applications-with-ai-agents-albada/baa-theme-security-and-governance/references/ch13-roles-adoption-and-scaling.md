# Roles, Adoption and Scaling Collaboration

## Contents
- The four human roles, with interface needs and promotion triggers
- Case patterns for role progression
- Stakeholder alignment and adoption playbook
- Phased rollout with metric gates
- Growing from individual to enterprise agents
- Pitfalls
- Worked example

## The four human roles, with interface needs and promotion triggers

The human's job changes as the agent earns autonomy. Treat these as stages on one arc, chosen per task and per stakes, not as a fixed property of a product. For each stage: what the person does, what to build for them, and what should trigger moving on.

- **Executor.** The person launches each task and inspects every result; the agent works only under close watch. Build guided steps, instant feedback and cheap correction. Move on when measured accuracy holds above an agreed bar for a sustained period.
- **Reviewer.** The person samples outputs and deals with flagged cases, typically in high-stakes or regulated work; the agent finishes routine items alone. Build exception queues, per-item confidence, dashboards and audit views so attention lands only where needed. Move on when exception rates and reviewer overrides fall and reviewers report low friction.
- **Collaborator.** The person sets goals and priorities, co-plans, and edits in real time, stepping in for nuance, exceptions and moral judgment; the agent drafts, acts and sometimes decides. Build shared planning surfaces and in-context annotation. Move on when policy, not individual judgment, explains most interventions.
- **Governor.** The person sets policy limits, audits system behavior, owns escalation rules and watches how agents interact across teams; the agent acts freely inside those rules. Build policy configuration, escalation logs, explainability and checks against compliance frameworks and organizational values.

Decision rule: the riskier or more regulated the decision, the longer it should stay at reviewer or below, even if other tasks in the same product have moved on. Design for today's role and the one users will grow into; a reviewer UI with no path to policy configuration forces a rebuild later.

## Case patterns for role progression

- Contract extraction at a large bank (JPMorganChase COiN): junior legal staff began as executors checking every extracted clause; once accuracy passed enterprise thresholds, experienced lawyers moved to reviewing only unusual documents; senior counsel became governors who set extraction policy, audit, and decide expansion to new contract types. Lesson: promotion between roles is triggered by measured accuracy, and each role is staffed by people of matching seniority.
- Security scanning bot (GitLab): the bot ran SAST and DAST on merge requests and flagged issues for engineers (executor mode). Findings above a risk threshold went to security champions (reviewers), whose triage tuned rules and cut false positives, gradually raising autonomy. Senior security leaders audited rules and escalation logs (governors). Lesson: the three roles can run at once, and reviewer feedback is the fuel for autonomy growth.

## Stakeholder alignment and adoption playbook

Capable agents still fail when people treat them as gimmicks, quietly resist, or route around them. Plan adoption as organizational change alongside the software release.

1. Inventory stakeholders and their lens: engineers usually want efficiency, legal wants compliance, end users want ease of use. Write these down and reconcile them before design.
2. Recruit stakeholders as co-creators, not late-stage testers.
3. Agree on: the outcomes the agent should improve, the decisions it takes vs. those that stay human, and concrete descriptions of success and failure.
4. Define success beyond technical metrics: perceived usefulness, reliability, fit with existing workflows and values, and whether it adds friction or erodes trust.
5. Use disagreements (between users and builders, or between capability and expectation) as inputs to clarify priorities and adjust roles. Handled openly, friction drives iteration.
6. Sustain adoption with training, feedback channels, responsive support, onboarding material that evolves with the agent, places to raise concerns, and recognition of small wins.

Goal state: stakeholders see the agent as an extension of their own goals, not a tool imposed on them.

## Phased rollout with metric gates

ZoomInfo's GitHub Copilot rollout is the reference pattern: four phases, starting with roughly 50 engineers and only reaching the full 400+ after hitting preset gates (33% of suggestions accepted, 72% of developers satisfied), plus qualitative confirmation that suggestions really helped.

Template for any agent:
- Phase gates combine at least one usage metric (acceptance, task completion), one sentiment metric (satisfaction, trust survey), and qualitative review.
- Thresholds are set before the pilot starts.
- Each expansion step is explicit; missing a gate means iterate, not expand.

## Growing from individual to enterprise agents

| Level | Typical work | Main design concern |
|---|---|---|
| Individual | Calendar, email summaries, research help | Rich personal context, low authority and risk; learn one user's preferences |
| Team | Shared knowledge, project tracking, meeting synthesis | Shared memory boundaries, interpersonal dynamics, conflicting expectations; surface uncertainty for group decisions instead of acting unilaterally |
| Division or function | Finance, legal, customer success support | Sensitive systems and many stakeholders; RBAC distinguishing public, internal, restricted data; privileges that depend on who the agent is serving; delegation rules and logging |
| Enterprise | Cross-department workflows, cross-functional synthesis, strategic advice | Strict policies, regular audits, human sign-off for critical actions; awareness of dependencies, business rules, organizational politics |

Bank of America's Erica illustrates scaling through transparency: it shows a confidence figure to users and hands off to a live person when uncertainty crosses a set threshold, which let it grow from FAQs to billions of requests and over half of internal IT help-desk tickets.

Scaling is sociotechnical: align with culture and incentives, make review, approval and modification easy, and grow escalation paths with responsibility. Error cost rises with scope, so trust boundaries must tighten as reach widens. Each new scope is another step of progressive delegation, not a separate project.

## Pitfalls

- Shipping an agent as a pure technical upgrade with no change management.
- Building for an imagined average user.
- Measuring only speed or accuracy and missing trust erosion.
- Expanding a pilot on enthusiasm rather than pre-set gates.
- Giving a team agent the unilateral-action habits of a personal assistant.

## Worked example

A support-ticket triage agent for a 30-person team. Stage 1 (executor): agents propose labels, leads approve each one; gate is 90% label agreement for two weeks and lead satisfaction at 4 of 5 or higher. Stage 2 (reviewer): routine labels apply automatically, low-confidence ones land in an exception queue with confidence shown. Stage 3 (collaborator): agent drafts first replies that humans edit in a shared view. A support operations manager acts as governor, owning the routing policy and reviewing escalation logs monthly.
