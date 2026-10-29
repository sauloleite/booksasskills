# Legacy Code, Fresh Eyes and the Golden Rule of Code

## Contents
- Living in existing code
- The newcomer advantage
- How to question an established practice
- Worked example: independent work hiding in a sequential job
- The Golden Rule applied to software
- Readability practices
- Pitfalls

## Living in existing code

Most engineering time goes into code someone else wrote, often long ago, carrying decisions nobody remembers. Practical stance for an agent coaching someone in a new codebase:

- Normalize partial understanding. A safe change needs understanding of the area being touched, its callers and its tests, not the whole system.
- Ramp up by following one real request or job end to end, then widen.
- Before changing odd code, ask why it is that way; but be prepared for teammates to be guessing too.
- Treat even brand-new code as future legacy; it will accumulate debt within months.

## The newcomer advantage

People new to a codebase, team or industry lack years of context, but they also lack attachment to past decisions that no longer make sense. That outsider view can surface inefficiencies, overturn stale assumptions and suggest new approaches. Newcomers can also restore energy to a tired project.

Coaching point: tell a new team member their questions are an asset, and encourage them to keep a running list of things that look strange during the first weeks, before familiarity makes those things invisible.

## How to question an established practice

Habit is a weak reason for a design. Something done the same way for years may have started as an accident or as the fastest option at the time, so a better approach often exists.

Protocol:
1. Notice something that looks odd, redundant or out of place.
2. Ask a teammate to explain it, privately or in a low-stakes setting.
3. Frame the question as wanting to learn ("What constraint led to this?"), never as exposing past or present colleagues.
4. Accept that some unusual choices have solid reasons; record those reasons in a comment or doc so the next person does not need to ask.
5. If the reason has expired, propose a change and a cleanup task, and tell other developers to stop copying the pattern.

Most engineers respond well when the motive is curiosity rather than blame.

Invented example: every API handler in a service sleeps for half a second before retrying a downstream call. Asking why reveals it compensated for a rate limit on a vendor API that was replaced two years ago. New handlers kept copying the delay. Outcome: remove the sleep, add a note to the team's coding conventions, and file a ticket to clean up the remaining handlers.

## Worked example: independent work hiding in a sequential job

Pattern from the chapter, retold with invented details: a nightly reconciliation job processed accounts one at a time. It was fine when the company was small, but as accounts grew, the run spilled past its window into business hours.

Key question a fresh pair of eyes asks: does processing item A depend on item B?

If the answer is no (apart from a final roll-up), restructure:
- A pool of workers pulls the next item from a queue.
- Each worker processes its item and emits a result.
- A final step aggregates results.

```python
from concurrent.futures import ThreadPoolExecutor

def reconcile(account):        # independent per item
    ...
    return result

def run_nightly(accounts, aggregate, workers=16):
    with ThreadPoolExecutor(max_workers=workers) as pool:
        results = list(pool.map(reconcile, accounts))
    return aggregate(results)   # only the roll-up is sequential
```

Lesson: the insight required no special expertise, only the willingness to question why the job was sequential. Check for shared state, ordering requirements and downstream rate limits before parallelizing.

## The Golden Rule applied to software

Treat future maintainers the way you would want to be treated, remembering that the future maintainer may well be you, puzzling over code you no longer recognize as your own.

Core claim: code instructs a machine, but its more important role is communicating with other developers. So write for readers and optimize for people rather than the compiler. The exception is narrow, specialized work (for example tight inner loops or hardware-constrained code) where performance genuinely dominates; such cases are usually obvious.

What following the rule looks like:
- Clean, readable code with intention-revealing names.
- Documentation kept current so nobody wastes hours on an outdated procedure.
- Diagrams that clarify rather than confuse.
- Time made for answering questions and helping colleagues.

Payoff: engineers who make everyone around them more effective become the people others want on their teams.

## Readability practices

Invented before and after:

```python
# Before: correct, but the reader must reverse-engineer intent
def chk(u, d):
    return (d - u.c).days > 90 and not u.f

# After: the same logic, stated for the next reader
INACTIVITY_LIMIT_DAYS = 90

def is_dormant(user, today):
    days_since_login = (today - user.last_login).days
    return days_since_login > INACTIVITY_LIMIT_DAYS and not user.is_frozen
```

Review checklist for an agent reviewing or generating code:
- [ ] Could a new teammate explain what this does without running it?
- [ ] Are magic numbers named?
- [ ] Is the non-obvious "why" recorded near the code?
- [ ] Did the change leave docs or diagrams stale?
- [ ] Is cleverness justified by a measured need?

## Pitfalls

- Copying an existing pattern without knowing its reason (that is how obsolete workarounds spread).
- Asking "why" in a way that sounds like an accusation.
- Assuming seniors know every library feature; they often do not.
- Refusing to touch code until it is fully understood; this stalls delivery.
- Writing for the compiler in ordinary business code.
