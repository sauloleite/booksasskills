# Problem-First Engineering

## Contents
- Strategic laziness defined
- Brute force as a draft, not a destination
- Reuse before you build
- Resist the rush to a solution
- The cost curve of defects and shifting left
- Problems of misconception
- Getting to the real need: Five Whys and solution-shaped requests
- Biased requirement sources
- Pragmatism versus overengineering
- Pre-coding checklist
- Glossary

## Strategic laziness defined

The "lazy programmer" stance is about efficiency, not avoidance of work. Newer engineers often start typing immediately; a deliberately lazy engineer spends a moment on the problem domain first because thinking up front is the cheapest way to finish sooner with a better result. The motto the chapter borrows from horse training boils down to: invest time early so the whole job takes less.

Agent behavior: when a user says "just write it", still spend one short message confirming the goal and checking for an existing solution, unless the task is trivial.

## Brute force as a draft, not a destination

Starting with the obvious approach is fine; stopping there is not. Engineers consider best, average and worst case behavior (big O is the shorthand for comparing how algorithms scale) and choose accordingly. Classic illustration: bubble sort works but is rarely the right sort.

Invented example, duplicate detection:

```python
# Draft: compares every pair, O(n^2) time
def has_duplicate_naive(items):
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            if items[i] == items[j]:
                return True
    return False

# Iteration: single pass with a set, O(n) time, O(n) extra memory
def has_duplicate(items):
    seen = set()
    for item in items:
        if item in seen:
            return True
        seen.add(item)
    return False
```

Decision note: the second version trades memory for time. For ten items either is fine; for ten million, the first one is a production incident. Ask what input sizes are realistic before optimizing further.

## Reuse before you build

Assume someone has solved the problem already. Search the language's standard library, mature third-party packages, the organization's internal code, and managed services.

- Budget: around ten minutes of searching can save days of building; a few hours of comparing alternatives can save weeks.
- Trigger: if it feels like there ought to be a simpler way, there usually is.
- Homegrown utilities in old codebases often predate a language or library feature that now does the same job better. Check before adopting (or extending) an in-house helper with a sprawling signature.
- Seniority is no guarantee that someone knows the built-in exists; a newcomer's search can beat a room of veterans.

Invented example: a team maintains a 300-line date parsing module full of special cases. A quick look at the standard library reveals ISO 8601 parsing and timezone handling built in. Replacing the module removes a recurring source of bugs.

See also the chapter's pointer to a later section on not reinventing the wheel.

## Resist the rush to a solution

Before coding, find the root cause. This is hard in practice: calendars full of meetings, chat interruptions, frequent status updates to several stakeholders, a growing backlog and fresh bug reports all push toward the fastest patch. Protect some uninterrupted thinking time anyway.

Quick fix versus root-cause fix:

| Choose a stopgap only if | Prefer the root-cause fix when |
|---|---|
| Users are actively harmed right now and a safe mitigation exists | The issue will recur or spread |
| A follow-up ticket for the real fix is created and owned | The patch would add special cases others must understand |
| The patch is easy to remove later | Data integrity or security is involved |

Warning: stopgaps frequently generate new problems of their own.

## The cost curve of defects and shifting left

Cheapest to most expensive place to deal with a defect:

1. **Design**: the bug is never written.
2. **Development**: caught while the code is fresh (one motivation behind test-driven development).
3. **Testing / QA**: the code is still recent in the team's memory, test datastores can be reset easily, and no customer is waiting, so pressure is lower.
4. **Production**: customers are affected, money may be lost, data may be corrupted and hard to reconcile, and the fix may span many routines plus coordination with other teams.

"Shifting left" means moving every valuable activity earlier on the timeline, not only testing:

| Activity | Shift-left form | Benefit |
|---|---|---|
| Code review | Pair programming | Review happens live instead of days or weeks later |
| Testing | Continuous, during development | Problems found close to when they were introduced |
| Integration | CI, merging small changes often | Fewer painful merge conflicts |
| Release | Continuous delivery | Environment differences surface before customers see them |
| Security | Built into every stage | Lower odds of a catastrophic vulnerability |

## Problems of misconception

Many serious failures come from not understanding what you are building before building it. These cannot be caught by tests or a type system; they are differences in understanding, so only shared understanding fixes them.

- Look for near-synonyms that the business distinguishes. Invented example: in an insurance system, "policyholder" and "insured" may sound identical, yet only one may be allowed to change the beneficiary.
- Remedy: keep a project glossary. The authors rate it among the highest-value artifacts a project can have; create one if none exists.
- Questions to settle first: What problem does the application solve? What are its context and constraints? Which related problems sit next to it?

## Getting to the real need: Five Whys and solution-shaped requests

Customers often arrive with a specific solution rather than a problem. A seasoned engineer asks what need lies behind it, because what is requested and what solves the business problem frequently differ. Customers may not see alternatives because they are anchored on current practice.

**Five Whys** (from the Toyota Production System): ask why, then ask why about the answer, roughly five times, to dig from symptom to root cause. Five is a guideline; stop when you reach something actionable.

Invented software example:
- Problem: the nightly invoice job failed again.
- Why? It ran out of memory.
- Why? It loads every open invoice into memory at once.
- Why? The loader was written when there were a few hundred invoices.
- Why was that never revisited? No one monitors job memory or input volume.
- Why? Batch jobs were left out of the observability rollout.
- Actions: stream invoices in pages, and add the batch jobs to monitoring so growth is visible.

Invented solution-shaped request: "Email me this report every night." Probing reveals the manager only wants to know when a metric crosses a threshold. An alert serves that better than a nightly email nobody reads.

Agent behavior: when a request names an implementation, reply with one or two clarifying "what will you do with it?" questions before building, unless the user has already explained the need.

## Biased requirement sources

The main requirements source is often an expert user of the system being replaced. Their knowledge is valuable but shaped by what they already have; they may not know why a feature exists and may assume the current approach is the only one. Unchecked, the result is the old system re-implemented in new technology (the authors joke that this is why so many systems drift back to email and spreadsheets).

Countermeasures:
- Ask what outcome each legacy feature serves.
- Talk to more than one user role.
- Separate "must keep" behavior from "how it happens to work today".

## Pragmatism versus overengineering

Tension to manage: experienced engineers fear painting themselves into a corner, so they imagine every future need; but speculative code is either thrown away or, worse, kept around unused.

Rules:
- Keep the actual problem in view; there are many valid solutions.
- Choose the right tool for this problem, not the favorite one.
- Be realistic, not optimistic. Scalability matters, but very few systems will carry a large share of global traffic.
- Remember that predicting future requirements is unreliable; prefer designs that are easy to change over ones that anticipate everything.

## Pre-coding checklist

- [ ] I can state the problem and the user need in one or two sentences.
- [ ] I asked why until I reached a root cause or real goal.
- [ ] Ambiguous domain terms are defined (glossary entry if needed).
- [ ] I spent a timeboxed search on existing solutions.
- [ ] I sketched the domain and at least two options.
- [ ] I know the realistic input sizes and load, and the complexity of my approach.
- [ ] I talked through the plan with an experienced colleague if the change is risky.
- [ ] Tests or checks will catch regressions before production.

## Glossary

- **Brute force**: the most direct approach, usually exhaustive; acceptable as a first draft.
- **Big O**: notation for how running time or memory grows with input size.
- **Shift left**: moving quality, review, integration and security activities earlier.
- **Problem of misconception**: a defect caused by misunderstanding the domain, invisible to tests.
- **Five Whys**: iterative questioning to reach a root cause.
- **Stopgap**: a temporary fix that treats a symptom.
