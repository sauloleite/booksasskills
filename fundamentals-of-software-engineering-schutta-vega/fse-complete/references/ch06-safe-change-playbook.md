# Safe Change Playbook: Refactoring, Scout Rule, Small Reversible Changes, Version Control

## Contents
- Stance
- Refactoring on top of existing tests
- Characterization tests before refactoring
- The scout rule and when to defer cleanup
- Small, reversible changes and change management
- Splitting large requests
- Version control habits on existing code
- Pull requests and reviews
- Pitfalls

## Stance

An existing system carries years of iterations, fixes and features you do not yet understand. Pace yourself and move methodically. "Move fast and break things" does not apply here. At the same time, do not be timid: with tests, the scout rule and small reversible steps, you can make a real mark.

## Refactoring on top of existing tests

- Have a plan and limit scope; do not refactor everything you notice.
- If a solid test suite exists, it is your safety net. Loop: one small structural change, run the relevant tests, repeat.
- Do not edit tests during a pure refactor. A refactor preserves behavior; if a test must change, you are changing behavior, which is a separate step.

## Characterization tests before refactoring

When the area you will touch lacks coverage, add tests first (often called test-driven refactoring):
1. Write tests that pin down what the code does today.
2. Confirm they pass against the current implementation.
3. Refactor.
4. Confirm they still pass.

Hard rule: the first tests on legacy code record current behavior, even behavior you believe is a bug. Fix bugs and pursue better designs only after the safety net exists, in a separate change.

Original sketch (Python, pinning a shipping-fee rule as it behaves today):
```python
def test_shipping_fee_current_behavior():
    # Observed today: orders at exactly 50.00 still pay the fee.
    # Possibly a bug, but we pin it first and fix it in a later change.
    assert shipping_fee(order_total=49.99) == 5.00
    assert shipping_fee(order_total=50.00) == 5.00
    assert shipping_fee(order_total=50.01) == 0.00
```

## The scout rule and when to defer cleanup

Scout rule: every time you touch a file, leave it a bit cleaner than you found it. Typical small improvements:
- add missing documentation
- rename unclear variables or methods
- split an overly long or complex method
- delete dead code
- fix minor bugs you stumble on (as separate, visible commits)

Balance it against the task. In a big codebase you can polish forever and never ship the fix you were assigned.

Decision rule:

| Refactor now when... | Defer when... |
|---|---|
| The code is hard to understand | It works and rarely changes |
| You are adding a feature in this area | A tight deadline is in force |
| You are fixing a bug here | Breakage risk outweighs the gain |
| It causes performance problems | It would sprawl far beyond the current task |
| Many developers change this area often | Test coverage is too thin to make it safe |

Git history quantifies two of these rows: commit frequency ("rarely changes" vs "changes often") and number of distinct authors. Run the bundled `git_hotspots.py` to get them.

## Small, reversible changes and change management

Prefer many small, easily undone modifications over one sweeping change, even when product owners push for big-bang impact. This takes ongoing practice.

A change management strategy is the team's structured way of proposing, reviewing, implementing and tracking changes. Tuned for small reversible work, it emphasizes safety and visibility:
- **Visible:** document each change briefly: what motivated it and how it was done.
- **Verified:** automated tests, code review and static analysis confirm it works.
- **Reversible:** assume something will go wrong (Murphy's law) and know how to revert; small changes make reverts cheap.
- **Monitored:** watch production for side effects; good observability pays off here.

Benefits of small, testable increments: smaller blast radius per change, sharper tests, reviews people can actually do well, and faster troubleshooting.

## Splitting large requests

If a request is too big, push back and split it into smaller deliverables. Several small successes beat one large change that ships bugs.

Pattern for an overgrown method (for example, one that validates, totals, discounts, ships, taxes, charges, updates stock and notifies): extract one responsibility at a time, add tests for the extracted piece, verify, commit, then move to the next. Never rewrite the whole method in one go.

## Version control habits on existing code

Situations where you may need to establish or repair practices:
- Legacy repos: everything committed to main, no branching model, vague messages, huge unmerged changes, generated files or vendored dependencies tracked.
- Personal or tiny projects: skipping version control on the grounds that you work alone builds debt and hurts later onboarding.
- Open source: follow the upstream's conventions and keep your fork in good shape.
- Consulting or contract work: you may be the one introducing discipline.

Commits should narrate how the code evolved:
- **Atomic:** one logical change per commit, independently reviewable and revertible.
- **Explained:** state what changed and why. Contrast:
  - weak: `fix tax`
  - strong: `Round VAT per line item instead of per invoice` plus a body explaining the customer-visible discrepancy it fixes.
- **Frequent:** small commits make it easy to locate when a regression appeared (and enable bisecting).

Branching principles:
- Isolate work on feature branches so main stays stable.
- Keep branches short-lived; merge in days, not weeks, because divergence makes integration painful.
- Rebase onto the latest main before merging when appropriate, but remember rebasing rewrites history; be careful on shared branches.

## Pull requests and reviews

- One concern per PR. A PR touching around a thousand lines across twenty files is effectively unreviewable.
- In the description, state the problem, how the change solves it, and links to related issues or requirements.
- Reviews improve the solution; they are not judgments of the author. Stay open and iterate.

## Pitfalls

- Mixing refactoring, behavior changes and bug fixes in one commit or PR.
- "Fixing" suspected bugs while writing the first characterization tests.
- Scout-rule cleanup that balloons until the assigned task is forgotten.
- Large refactors in areas without tests.
- Long-lived branches and force-pushed rebases on branches others use.
- No rollback plan, or no monitoring after release.
