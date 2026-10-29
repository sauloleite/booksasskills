# Component Testing: Tools, Planning, Memory, Learning

## Contents
- Tools
- Planning
- Memory
- Learning
- Component test checklist

Unit-level tests isolate each building block so a failing end-to-end run can be traced to a cause. Each component has its own risk profile.

## Tools

Tools are where the agent touches the world, so they deserve the most exhaustive enumeration of cases.

- **Cover more than the happy path**: rare, adversarial and malformed inputs expose hidden assumptions. A lookup tool should be exercised with different data formats, slow or flaky networks, and both clean and deliberately corrupted sources.
- **Assert more than output correctness**: also latency, resource use, and error handling. The tool should degrade gracefully under load or upstream failure (clear error object, no hang, no partial write).
- **Determinism**: same input, same output, unless randomness is a designed feature; then test statistical properties (distribution, bounds) over many calls.
- **External dependencies**: replace APIs and databases with mocks or simulators so rare but catastrophic conditions (timeouts, 500s, schema drift, duplicate records) are reproducible on demand.
- **Regression rule**: any change to a tool reruns that tool's full suite.

## Planning

The planner converts a goal into a sequence of actions, often adaptively: branching, conditionals, early stopping. Validation answers one question: does the agent know what to do?

Procedure:
1. Build canonical workflows: common intents paired with known-good outcomes (starting environment, conversation so far, expected tool calls and expected user-facing message).
2. Execute the full agent and pull every tool invocation with its arguments from the trace.
3. Compare with ground truth and compute:
   - **Tool recall**: expected calls that were made / expected calls. Low recall means an essential action was skipped.
   - **Tool precision**: necessary calls / all calls made. Low precision means the planner misread the goal or intent and did extra things.
   - **Parameter accuracy**: expected calls matched with exactly the right arguments / expected calls. Low values indicate weak contextual grounding: wrong item, wrong amount, acting on an order that does not qualify.
4. Add edge cases: only one item in a multi-item order is defective; the user is vague or contradicts an earlier turn; a required field is missing; a tool fails mid-plan. The planner must navigate ambiguity and recover.
5. Test consistency: identical deterministic inputs give identical plans; for stochastic planners, repeated runs stay within an acceptable set of plans. Probe sensitivity with tiny input perturbations.
6. Keep growing the planning corpus from single-step flows to multiturn, interdependent actions; it becomes the backbone of integration testing.

Implementation choice: count tools as a multiset rather than a set so duplicate calls (calling a lookup twice, issuing two refunds) are penalized. A set-based count hides double refunds, which is exactly the costly mistake.

Short illustration (original):

```python
from collections import Counter

def plan_scores(expected, actual):
    e = Counter(c["tool"] for c in expected)
    a = Counter(c["tool"] for c in actual)
    hit = sum((e & a).values())
    recall = hit / sum(e.values()) if e else 1.0
    precision = hit / sum(a.values()) if a else float(not e)
    pool = list(actual)
    exact = 0
    for c in expected:
        if c in pool:           # same tool and same params
            pool.remove(c)
            exact += 1
    params = exact / len(expected) if expected else 1.0
    return recall, precision, params
```

## Memory

Memory testing is more than store-then-fetch; integrity, relevance and efficiency all degrade as the store grows.

- **Correctness**: written items come back exactly, immediately and after time has passed or other operations intervened. Include capacity limits, odd data types, rapid read/write bursts, and malformed, duplicate or ambiguous entries.
- **Retrieval accuracy@k**: for a set of queries with known relevant items, the share of queries where at least one relevant item appears in the top k. Report several k values.
- **Relevance and freshness**: a query for current preferences must not return superseded ones (a leak or indexing bug). Lookalike but irrelevant items must not win on surface similarity alone; include near-miss distractors in the test set.
- **Efficiency**: benchmark latency and resource use as the store grows; look for cliffs where retrieval time jumps. For vector or semantic memory, include easy and hard retrievals to catch embedding or index errors.
- **Resilience**: simulate store unavailability, corrupted records and schema or version migrations. Acceptable outcomes are graceful recovery or a controlled, low-impact failure.

## Learning

For components that update from data, feedback or reward, the risk is that they overfit, regress, or forget what they already did well.

- **Learning loop works**: parameters, caches or rules actually change in response to labels, feedback or reward.
- **Supervised**: on a canonical dataset, reach the expected accuracy and generalize to validation data.
- **Reinforcement**: reward maximization produces better behavior over time; plateaus are detected and handled (early stopping, adjusted exploration).
- **Generalization**: test on holdout, synthetic and adversarial out-of-distribution cases built to break memorized answers.
- **Adaptability**: simulate distribution shift (new input types, new tool failure modes, a changed reward landscape) and confirm no catastrophic forgetting or collapse. Keep a frozen "previously mastered" suite and rerun it after every update.
- **Mixed paradigms**: when supervised, unsupervised and RL pieces coexist, test their interactions explicitly.

## Component test checklist

- [ ] Every tool has happy, rare, malformed and adversarial cases, plus latency and error-path assertions.
- [ ] External dependencies are mocked with failure injection.
- [ ] Planner scored with tool recall, tool precision and parameter accuracy on a growing scenario corpus.
- [ ] Planner consistency checked with repeated runs and small perturbations.
- [ ] Memory: accuracy@k, stale-data and distractor tests, load benchmark, outage and migration tests.
- [ ] Learning: improvement, generalization, shift and forgetting tests.
- [ ] Any change to a component reruns its whole suite.
