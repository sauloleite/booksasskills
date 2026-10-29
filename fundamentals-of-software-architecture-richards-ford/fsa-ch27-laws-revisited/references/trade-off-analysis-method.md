# Trade-Off Analysis Method

## Contents

1. The first law and the arbiter stance
2. The analysis procedure
3. Example A: shared library versus shared service
4. Example B: point-to-point queues versus a broadcast topic
5. Weighting and the Out of Context antipattern
6. Invented worked example with weights
7. Checklist and review questions

## 1. The first law and the arbiter stance

The first law says no architectural option is free: each one buys some qualities by spending others. The practical consequence is a job description. The architect is not the person who finds the clever answer that makes the problem vanish; heroic silver bullets are rare, and architects tend to be remembered for failures rather than successes. The real work is analyzing trade-offs well.

Two reasons to cultivate a reputation for objectivity instead of advocacy:

- **Decisions age.** Choices are made with partial knowledge under current conditions. The technology ecosystem keeps shifting, so even a sound choice tends to weaken or become wrong over time. An architect who campaigned for it loses credibility when it must be reversed. Neutral analysis lets you revise without loss of face.
- **Leaders want sober judgment.** Executives facing a critical call look for someone whose analysis they can trust, not a cheerleader. Being the reliable source of balanced comparisons makes an architect valuable.

Agent behavior: when asked "should we use X?", never open with enthusiasm for X. Open with the forces in play.

## 2. The analysis procedure

1. **Name the options.** Usually two, sometimes three. Keep them concrete.
2. **Derive contextual factors.** Pull from the organization's technology landscape, team capabilities, budget, change rate of the code involved, security posture and growth expectations. The list must be specific to this organization and this solution.
3. **Judge each factor.** For each factor, mark which option it favors (plus, minus, or neutral) and write one sentence of reasoning.
4. **Tally, then weight.** The raw count shows the shape of the forces but is not the answer (see section 5).
5. **Return to goals.** Ask which organizational objectives dominate (security, speed of change, cost, growth) and pick the option that serves them.
6. **Record it.** Capture factors, weights, the choice, and the downsides you accepted, so mitigation work is known in advance.

Use `scripts/tradeoff_matrix.py` to compute steps 3 and 4 and to flag a flip between raw and weighted results.

## 3. Example A: shared library versus shared service

The situation: several services in a distributed architecture (microservices or event-driven) need the same behavior. Either compile a common library into every service at build time, or deploy one service that others call over the network at runtime.

Factors where the **shared service** comes out ahead:

- **Multiple technology stacks.** Callers reach a service over the network, so its implementation language is irrelevant. A library must be rewritten for each stack and the copies kept consistent, which adds a lot of complexity.
- **Fast-changing code.** Once the service is redeployed, every caller gets the new behavior. A library change forces a rebuild and redeploy of every consuming service.

Factors where the **shared library** comes out ahead:

- **Versioning.** Version differences are settled at build time; each consumer pins what it needs. A service must negotiate versions at runtime, which complicates every interaction.
- **Change risk.** Compilation and tests give strong confidence that a library change works in the consumer. A service can change underneath callers with no build-time check, raising the chance of failures at call time.
- **Performance.** In-process calls beat network calls with their latency.
- **Fault tolerance.** No network hop means no network failure modes; once built and tested, the consumer is stable.
- **Scalability.** Network latency on every call limits throughput; in-process access does not.

Raw count favors the library by a wide margin. That is only the first pass; section 5 shows how weighting can reverse it.

## 4. Example B: point-to-point queues versus a broadcast topic

The situation: a trading service must tell downstream consumers (for example notification and analytics) about each trade. Point-to-point queues mean one queue per consumer, and the producer knows every recipient. A topic means one published message that any subscriber receives, and the producer neither knows nor cares who listens.

Queues, strengths:

- Each consumer can receive a message shaped for it (heterogeneous contracts).
- The producer controls exactly who receives data, which makes eavesdropping by an unexpected service harder; good when confidentiality ranks high.
- Each queue can be monitored for depth and scaled on its own.

Queues, weaknesses:

- Tight coupling: the producer knows how many consumers exist.
- The producer manages connections to several queues, and more infrastructure is needed.
- Adding a consumer (say, compliance) means changing the producer to feed a new queue, so extensibility suffers.

Topic, strengths:

- Loose coupling; the producer emits one message.
- Highly extensible: a new consumer subscribes without touching the producer or other consumers.

Topic, weaknesses:

- Every subscriber gets the same payload, inviting stamp coupling (consumers depend on a large contract while using a fraction of it).
- Every subscriber sees all fields, raising confidentiality questions.
- No per-consumer monitoring or scaling, and fewer scaling options overall.

Decision rule: confidentiality as top priority points to queues; rapid organizational growth with many new interested consumers points to a topic.

## 5. Weighting and the Out of Context antipattern

**Out of Context antipattern**: the architect correctly identifies the trade-offs but treats them as equally important, or weights them by habit instead of by the current situation.

Applied to Example A: suppose a team runs code on several platforms, does not care much about raw speed or scale, and mainly wants one clean place to manage common behavior. Then the two factors favoring the service dominate, and the service is the right choice despite losing the raw count. A side benefit: the analysis already lists the library's advantages, which become the risks the team must mitigate (runtime versioning, change risk, network faults).

Takeaways:

- Experience supplies the candidate factors; context supplies the weights.
- A generic comparison has little value; it becomes useful only when tied to a specific situation.
- Always show stakeholders both the raw and the weighted picture, and state where the weights came from.

Spotting the antipattern in a conversation: a recommendation justified by "it wins on more criteria", weights that nobody elicited from stakeholders, or the same answer reused from a different project.

## 6. Invented worked example with weights

An insurance claims platform must choose between an orchestrated workflow (a mediator coordinates claim intake, fraud check, assessment and payout) and a choreographed one (services react to each other's events).

| Factor | Weight | Orchestration | Choreography |
|---|---|---|---|
| Error handling and state visibility | 5 | + | - |
| Auditability for regulators | 5 | + | - |
| Recoverability and compensation | 4 | + | - |
| Responsiveness | 1 | - | + |
| Scalability | 1 | - | + |
| Coupling between services | 2 | - | + |
| No central bottleneck | 2 | - | + |

Raw tally: choreography wins four factors to three. Weighted (plus adds the weight, minus subtracts it): orchestration +8, choreography -8. The regulated context flips the answer. A spectrum-minded recommendation: orchestrate the core claim path, and let non-critical side effects (customer notifications, analytics feeds) be choreographed events. Record in the ADR that a change in regulatory requirements or a large jump in claim volume should trigger re-analysis.

## 7. Checklist and review questions

- Are the factors specific to this organization, or copied from a blog?
- Does every factor state which option it favors and why?
- Were weights elicited from stakeholders and written down?
- Does the weighted result differ from the raw count, and is the difference explained?
- Are the accepted downsides listed with mitigations?
- Review question: which single change in context would reverse this recommendation?
- Review question: what would a skeptic who favors the losing option say, and is it addressed?
