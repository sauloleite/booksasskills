# Coordination Strategies: Democratic, Manager, Hierarchical, Actor-Critic, ADAS

## Contents
1. Comparison at a glance
2. Democratic coordination
3. Manager coordination
4. Hierarchical coordination
5. Choosing among the three structural strategies
6. Actor-critic loops
7. Automated Design of Agentic Systems (ADAS) and Meta Agent Search
8. Pitfalls
9. Glossary

## 1. Comparison at a glance

| Strategy | Who decides | Message paths | Main strength | Main weakness | Natural fit |
|---|---|---|---|---|---|
| Democratic | All agents, as equals, by consensus | Many-to-many | No single point of failure; adapts by pooling input; equal voice | Heavy messaging, slow decisions, complex protocol | Sensor networks, collaborative robotics, fairness-sensitive decisions |
| Manager | One (or a few) managers | Worker to manager only | Fast decisions, clear task assignment, simple paths | Manager is a failure point and a bottleneck; less local awareness | Customer support, manufacturing-style structured flows |
| Hierarchical | Several tiers: strategy above, execution below | Up and down the tree | Scales coordination; redundancy across levels | Hard to design; propagation delay; waiting for orders | Large systems like supply chain planning, military-style command |
| Actor-critic | Critic accepts or rejects actor output | Actor and critic loop | Quality boost without training | More inference cost | Fuzzy or generative tasks with a clear rubric |
| ADAS / MAS | A meta-agent that writes agents | Meta-agent, archive, evaluator | Discovers novel designs that transfer | Expensive, safety concerns | Research and offline design search |

## 2. Democratic coordination

Every agent has equal authority and the group converges on a decision by sharing information and negotiating. There is no leader.

Use when: losing any single agent must not stop the system; inputs from all participants genuinely matter; fairness among contributors is a requirement; the environment changes and pooled input helps track it.

Cost model: consensus requires many exchanges (roughly every agent hearing every other agent, for as many rounds as it takes to agree), so both message volume and decision time grow quickly with the number of agents. You also need explicit protocols for communication and conflict resolution before consensus can be reached.

Design checklist:
- Define the decision rule (majority, weighted vote, unanimity) and a round limit.
- Define what happens on deadlock (fallback agent, human, default action).
- Bound the number of voters; split large populations into smaller voting groups.

## 3. Manager coordination

One or more designated managers decide, assign tasks and resolve disputes; subordinates talk mainly to their manager. A supervisor that routes each request to one specialist (as in the chapter's multiagent example) is the simplest instance.

Advantages: no lengthy negotiation; explicit assignment prevents duplicate work and conflicts; communication paths collapse from many-to-many to hub-and-spoke.

Risks and mitigations:
- Single point of failure, including compromise of the manager: keep a hot standby or a deterministic fallback router; treat the manager's prompt as a high-value attack surface.
- Bottleneck as volume grows: cap reports per manager, cache routing for repeated intents, or move to hierarchical.
- Weaker adaptability because the manager may lack real-time detail from each worker's environment: let workers return structured status, and allow workers to push back ("not my domain") so the manager can reroute.

## 4. Hierarchical coordination

Agents sit in multiple tiers. Upper tiers make strategic choices and direct the tier below; lower tiers keep some autonomy for tactical execution. It mixes centralized and decentralized control.

Advantages: coordination load is spread over several managers, so the system can handle more agents than a flat manager; tasks can be picked up at different levels, which adds redundancy and fault tolerance; authority lines are clear.

Costs: each level must be designed so handoffs between layers are clean; information must travel through several levels, which slows response to urgent change; lower tiers may idle waiting for instructions.

Design checklist:
- Keep depth minimal; each extra level adds at least one sequential hop.
- Give lower tiers explicit autonomy limits (what they may decide without asking).
- Provide an urgent path that skips levels for time-critical events.

## 5. Choosing among the three structural strategies

1. Few agents, clear task types, latency matters: manager.
2. Many agents or several distinct domains each with sub-specialties: hierarchical (a manager of managers).
3. No agent may be a failure point, fairness or pooled judgment is the goal, and slower decisions are acceptable: democratic.
4. Very many simple agents with local rules and no need for precise control: swarm (see the agent-count reference).

Then layer actor-critic on any node whose output quality is the problem, independent of the structural choice.

## 6. Actor-critic loops

An actor proposes candidates (answers, plans, actions); a critic acts as a quality gate against a rubric and either accepts or sends feedback for another attempt. It spends extra inference at test time to buy reliability; no training is involved.

Use it when all three hold:
- a clear rubric or checklist exists (correctness, completeness, tone, feasibility, cost, risk);
- extra generations are affordable relative to the quality gain;
- the task is fuzzy or generative, so a filtered or reranked set beats a single shot.

The core heuristic: actor-critic pays off when judging an output is easier than producing it. Given its low implementation cost, try it whenever a quality lift is worth the compute.

Design checklist:
- Make the critic output structured (scores per criterion, selected candidate, concrete feedback).
- Feed the critic's feedback to the next actor attempt, not just "try again".
- Set an acceptance threshold and a hard cap on iterations; on exhaustion return the best candidate with a flag or escalate.
- Consider a different model or prompt for the critic to reduce shared blind spots.
- Track acceptance rate per iteration; if most runs hit the cap, the rubric or actor prompt is wrong.

```python
def actor_critic(task, actor, critic, threshold=0.8, max_rounds=4):
    best, feedback = None, ""
    for round_no in range(1, max_rounds + 1):
        candidates = actor(task, feedback)            # list of proposals
        verdict = critic(task, candidates)            # {"score", "pick", "feedback"}
        if best is None or verdict["score"] > best["score"]:
            best = verdict
        if verdict["score"] >= threshold:
            return {"result": verdict["pick"], "rounds": round_no, "accepted": True}
        feedback = verdict["feedback"]
    return {"result": best["pick"], "rounds": max_rounds, "accepted": False}
```

Use `scripts/topology_overhead.py actor-critic` to estimate expected rounds, calls and success probability for a given per-round acceptance rate.

## 7. Automated Design of Agentic Systems (ADAS) and Meta Agent Search

Idea (Hu, Lu and Clune, 2024; ICLR 2025): instead of hand-building agents, let a meta-agent generate, evaluate and refine agent designs, following the broader machine learning trend where learned solutions replace hand-designed ones. Foundation models serve as general-purpose modules; the meta-agent can invent new prompts, control flows and tool-use patterns.

Three components frame any ADAS setup:
- **Search space**: which agent architectures can be expressed. Defining agents as code in a Turing-complete language makes the space effectively unbounded.
- **Search algorithm**: how the space is explored.
- **Evaluation function**: how a candidate is scored (performance, robustness, efficiency).

Meta Agent Search (MAS) loop, per generation:
1. Condition the meta-agent on the archive of previously discovered agents.
2. Have it write a high-level design description, then implement it as code exposing a single forward function.
3. Run two self-reflection passes, one for novelty and one for correctness.
4. Evaluate on validation data; on runtime errors allow up to five debug-and-retry passes.
5. Store the agent in the archive with its fitness (accuracy or F1, summarized with a bootstrap confidence interval).
6. Repeat, typically for about 25 to 30 generations, balancing exploration of new designs with exploitation of strong ones.

Implementation shape: a base wrapper that queries the model for structured JSON (role and temperature tunable), a search loop over generations, and a task abstraction that knows how to load data, format inputs and parse predictions (for example letter-to-index exact match for multiple choice, exact grid match for ARC puzzles). Evaluation runs candidate code over the dataset in parallel.

Reported results: on ARC, discovered agents beat hand-designed baselines such as Chain-of-Thought, Self-Refine and LLM-Debate. On DROP, F1 of 79.4 plus or minus 0.8 (13.6 above a role-assignment baseline); MGSM 53.4% (14.4 points above LLM-Debate); MMLU 69.6% (2 points above OPRO); GPQA 34.6% (1.7 points above OPRO). Designs transferred across domains (ARC agents applied to MMLU) and across models (GPT-3.5 to GPT-4), suggesting they capture general structure rather than overfitting one task.

Practical guidance for engineers:
- Treat ADAS as an offline design-search tool, not a runtime component.
- Start the archive with your current hand-built agents so search begins from known baselines.
- Executing model-written code is dangerous: run candidates in an isolated sandbox with no credentials, network limits and time and memory caps.
- Hold out a test split the search never sees; report fitness with confidence intervals, since small validation sets make lucky designs look good.
- Review discovered agents before deployment: automated design raises safety, reliability and alignment questions, so constrain what the meta-agent may generate (allowed tools, side effects) to keep behavior predictable.

## 8. Pitfalls

- Choosing democratic coordination for a latency-sensitive product.
- A single manager with dozens of direct reports and no fallback.
- Deep hierarchies where an urgent event must climb three levels before anyone acts.
- Actor-critic loops with no iteration cap or with a critic that shares the actor's prompt and blind spots.
- Trusting ADAS validation scores without a held-out test set or sandboxing.

## 9. Glossary

- **Test-time compute**: spending more inference at run time (sampling, critiquing, retrying) to improve output quality.
- **Archive**: the growing store of discovered agent designs and their fitness, used to condition the next generation.
- **Forward function**: the single entry point that defines a generated agent's behavior in MAS.
- **Fitness**: the evaluation score of a candidate agent design.
