# Experimentation: Staging, Shadow Deployments, A/B Tests and Bayesian Bandits

## Contents
- Why experiment and the rollout ladder
- Choosing a technique
- Shadow deployments
- A/B testing
- Bayesian Bandits
- Worked example: three reasoning chains
- Pitfalls

## Why experiment and the rollout ladder

Experimentation sits between insight and deployment. In interconnected agent systems a prompt tweak, tool parameter change or orchestration edit can have distant and surprising effects, so no change should jump from idea to production. Move it through progressively more realistic environments:

1. **Staging / release candidate (RC):** isolated production-like setup; catches obvious breakage without touching users.
2. **Shadow:** new version receives real inputs, outputs are only logged.
3. **Live comparison:** A/B test or bandit on a share of traffic.
4. **Progressive release:** canary (small traffic slice first), rolling update (instance by instance), or blue/green (two identical environments, flip traffic after validation, flip back to roll back).

Besides catching side effects early, this ladder produces direct comparisons between configurations so decisions are based on data.

## Choosing a technique

| Situation | Technique |
|---|---|
| High-risk change (planning workflow, external integration, major prompt rewrite), want real inputs, no user exposure | Shadow |
| Measurable user-facing effect (satisfaction, engagement, completion) that shadows cannot observe | A/B test |
| Several variants, want to limit traffic spent on losers, environment shifts over time | Bayesian Bandit |
| Ultra-high-risk action | Any of the above plus explicit approval gates; experiments alone are not enough |
| Final promotion of a validated version | Canary or blue/green |

## Shadow deployments

The candidate runs in parallel with production on the same inputs. Users only ever see production output; candidate output is logged for analysis. Think of it as a dress rehearsal behind the curtain while the real show continues.

Benefits:
- Realistic validation: exposure to the full spread of real behavior, which test suites miss.
- Safe exploration: bold or architectural changes cannot hurt users.
- Edge-case discovery: malformed inputs, ambiguous instructions and integration quirks surface before launch.
- Pairs naturally with blue/green for zero-downtime promotion and with canaries for gradual live exposure.

How to run one well:
- Instrument both versions identically. Compare traces, accuracy, latency and outputs case by case.
- Triage every discrepancy: is it an improvement or a bug? Do not count disagreement as failure by default.
- Make side-effecting tools in the shadow path no-ops or sandboxed (no emails sent, no hosts isolated, no payments).

Limitation: agents that need human interaction mid-flow (approvals, clarifying questions) cannot ask real users from the shadow path. Options: replay historical human responses, simulate them synthetically, or move interactive flows to staging or A/B tests.

Original sketch of a shadow router:

```python
async def handle(request):
    prod = await prod_agent.run(request)
    asyncio.create_task(run_shadow(request, prod))  # off the user's path
    return prod                                     # users only see production

async def run_shadow(request, prod):
    try:
        shadow = await asyncio.wait_for(
            shadow_agent.run(request, tools=sandboxed_tools), SHADOW_TIMEOUT)
        log_pair(request.id, prod, shadow)          # diffed offline, never shown
    except Exception as exc:
        log_shadow_error(request.id, exc)
```

## A/B testing

Live traffic is split between control A and treatment B (typically 50/50, randomly assigned). Users interact with one variant, and outcomes are compared on metrics such as task success, hallucination rate or satisfaction. Best for measurable changes whose effect depends on real user reactions, such as prompt variants in a chat assistant.

Strengths: results reflect real users and input variety, so they show whether a fix generalizes; direct head-to-head answer under real conditions; with correct design, differences are statistically meaningful rather than noise or sampling bias.

Rules:
1. Pick clear metrics tied to the change's objective before starting (plus guardrail metrics that must not regress).
2. Size the test for significance up front to limit false positives and negatives. Use `scripts/ab_test_analyzer.py samplesize`.
3. Prevent cross-contamination: a user must not hop between variants within a session.
4. Watch short-term and long-term effects; quick wins can hide later damage.
5. Read results qualitatively too. A lower completion rate in B might mean users are engaging more deeply, not failing.

Stateful agents (persistent memory, chat history) complicate A/B tests because reassignment across sessions produces inconsistent experiences. Mitigations:
- Sticky assignment: hash the user ID so the same user always lands in the same arm.
- Session-level randomization when cross-session state is weak.
- Separate state per arm: version or duplicate memory stores so variants do not read each other's state.

```python
def arm_for(user_id: str, experiment: str, split=0.5) -> str:
    h = int(hashlib.sha256(f"{experiment}:{user_id}".encode()).hexdigest(), 16)
    return "B" if (h % 10_000) / 10_000 < split else "A"
```

Experimentation platforms (LaunchDarkly, Optimizely, or an in-house dashboard) handle allocation, metric collection and analysis; the team's job is interpretation and action.

## Bayesian Bandits

Adaptive experimentation: instead of a fixed split, shift traffic toward variants that are winning while still sampling the others. Each variant is an arm of a multi-armed slot machine with unknown payout. Rewards (resolved tasks, lower latency, higher ratings) update a posterior belief per arm via Bayes' rule; allocation follows those beliefs (for example Thompson sampling). This balances exploration (trying alternatives) with exploitation (using the best known).

Advantages:
- Responsiveness: allocations update in near real time, lowering the cost of keeping users on weak variants.
- Efficiency: once a leader emerges, most users are served by it instead of by losing variants.
- Scalability: can search many parameters far faster than a sequence of fixed experiments.

Especially valuable in multiagent setups where each interaction is expensive or where emergent behavior only shows under load. Research such as Knowledge-Aware Bayesian Bandits (KABB) applies the idea to choosing subsets of expert agents per task using semantic knowledge.

Requirements:
- **Metric mastery:** reward must be the true goal (task success, satisfaction). A proxy reward gets optimized at the expense of the real objective.
- **Thoughtful initialization:** neutral priors (for example Beta(1,1)) and regularization so early noise does not lock in a variant.
- **Vigilant oversight:** watch for self-reinforcing feedback loops and for a bandit that chases brief spikes while long-run goals suffer. Keep a minimum exploration share so arms can recover if user behavior shifts.

Use `scripts/bandit_allocator.py` to compute posterior means, P(best) and next-round traffic shares.

Bandits vs A/B: choose A/B when you need a clean, defensible effect estimate for a decision or audit; choose a bandit when the goal is to maximize reward during the experiment and the environment changes.

## Worked example: three reasoning chains

A support triage swarm tests three reasoning chains for ambiguous tickets. After the first 1,200 tickets (400 each): chain A resolved 120, chain B 150, chain C 118. With Beta(1,1) priors, B's posterior mean is about 0.376 versus about 0.30 for the others, and P(B best) is about 0.98. With a 5% exploration floor, the next round sends about 88% of tickets to B and about 6% to each of the others. Before promotion: check guardrails (escalation rate, latency), check that the reward was not gamed (for example by closing tickets prematurely), then roll out B by canary.

## Pitfalls

- Shadow outputs never actually reviewed; the run gives false comfort.
- Shadow path calling real side-effecting tools.
- Stopping an A/B test the first day p dips under 0.05 (peeking inflates false positives); fix sample size in advance.
- Users flipping between arms because assignment is per request.
- Bandit reward = clicks or short replies, which the system learns to farm.
- Promoting a winner without a rollback path (blue/green or canary).
