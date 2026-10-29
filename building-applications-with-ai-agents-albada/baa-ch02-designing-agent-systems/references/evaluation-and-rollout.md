# Iterative Design, Evaluation and Real-World Rollout

## Contents
- Iterative design
- Evaluation strategy (functional, generalization, user experience, human review, end-to-end)
- Real-world testing and phased rollout
- Launch readiness checklist

## Iterative design

Do not aim for a perfect first build. Ship a small working prototype, measure, adjust, repeat.

Why it pays:
- **Early issue detection**: design flaws and bottlenecks show up before they are baked in, avoiding costly refactors.
- **User-centric**: frequent input from users, stakeholders and developers keeps behavior matched to real needs.
- **Scalability of the program**: an MVP grows in controlled increments, each tested before broad release.

Loop:
1. **Prototype fast**: core function only; basic is fine if it delivers value.
2. **Test and collect feedback** after every iteration; let it set the next priorities.
3. **Refine and repeat** using feedback plus performance data until performance, usability and scale targets are met.

## Evaluation strategy

Build a framework that covers every capability under expected and unexpected scenarios, along accuracy, efficiency, robustness and scalability.

**Functional testing** (test each skill or module on its own):
- Correctness: outputs match intended behavior consistently.
- Boundary testing: extreme or odd inputs, very large data, unusual or ambiguous requests.
- Task-specific metrics: domain accuracy and compliance thresholds for regulated fields.

**Generalization**: test on scenarios the agent was not built or tuned for, and on adjacent tasks outside its original domain, to see whether it copes without retraining. Most important for general-purpose agents and changing environments.

**User experience** (technical success is not enough):

| Signal | How | Watch for |
|---|---|---|
| Satisfaction scores | NPS, CSAT | Trend after each release |
| Task completion rate | Share of users who finish the task with the agent | Low rates point to confusion or friction |
| Explicit feedback | Thumbs, stars, accept / reject / edit of outputs | Edits are rich supervision |
| Implicit feedback | Mine interaction logs | Misreads, delays, negative sentiment, inappropriate replies |

**Human-in-the-loop validation**: have domain experts review a sample of outputs for correctness, ethics and best practice; use their verdicts to calibrate the automated graders.

**End-to-end in realistic conditions**: evaluate the full path from data ingestion through processing and action to final output, across the real systems, data sources and platforms involved.

## Real-world testing

Controlled tests use predictable inputs; production does not. Live exposure is how you find:
- **Real complexity**: diverse users and situations nobody scripted.
- **Hidden edge cases**: a bot fine on scripted queries can fail on ambiguity and phrasing variety.
- **Behavior under load**: fluctuating traffic in support bots or recommenders.

Rollout procedure:
1. **Deploy in phases**: small, limited audience first; widen only after issues are handled.
2. **Monitor** KPIs: response time, accuracy, user satisfaction, system stability.
3. **Collect user feedback** to find gaps and usability problems.
4. **Feed insights back** into the next development iteration.

## Launch readiness checklist

- [ ] Offline eval set with positives, negatives and edge cases; tool selection, argument accuracy and task success measured.
- [ ] Domain thresholds defined and met (for regulated tasks).
- [ ] Out-of-distribution sample tested.
- [ ] Expert review on a sample; grader agreement with experts checked.
- [ ] End-to-end test across real integrations.
- [ ] Monitoring dashboards for latency, accuracy proxy, satisfaction, errors.
- [ ] Explicit feedback controls in the UI; implicit signals logged.
- [ ] Phase plan with audience size per phase and exit criteria to widen or roll back.
