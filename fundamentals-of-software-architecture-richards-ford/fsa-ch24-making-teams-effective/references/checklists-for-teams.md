# Checklists for Development Teams

## Contents
- Why checklists
- What belongs in a checklist (and what does not)
- Getting checklists used (Hawthorne effect)
- Developer code-completion checklist
- Unit and functional testing checklist
- Software-release checklist
- Maintenance rules

## Why checklists

Aviation and surgery rely on checklists because skipping one routine step can be catastrophic. Atul Gawande's *The Checklist Manifesto* documents surgical checklists cutting hospital infection rates to near zero while hospitals without them saw rates climb. Software rarely carries life-or-death stakes, so not everything needs a checklist, but the authors are convinced well-chosen checklists noticeably improve team effectiveness. The skill is choosing where to apply them.

## What belongs in a checklist (and what does not)

Good candidates:
- Tasks with no fixed order and no dependencies between items.
- Processes where people regularly skip steps or make mistakes.

Poor candidates:
- Procedures with ordered, dependent steps (step 4 cannot happen until step 3 is done). Write those as a procedure or runbook, not a checklist. Example: requesting a new database table, waiting for approval, then verifying the table exists is a sequence, not a checklist.
- Simple, familiar processes the team performs often and reliably.

Design rules:
- **Avoid checklist sprawl.** Once architects see checklists work, they tend to make everything one. Diminishing returns set in: the more checklists exist, the less any of them is used.
- **Keep each one as short as possible** while still complete. Long checklists get ignored.
- **Automate whatever can be automated, then delete it from the list.** This improves signal to noise.
- **Include the obvious.** Obvious items are exactly the ones people skip when rushed.

## Getting checklists used (Hawthorne effect)

The hardest part is real usage; under time pressure people tick every box without doing the work.

Escalating tactics:
1. Explain why checklists matter; consider having the team read Gawande's book.
2. Make sure everyone understands the reason for each item.
3. Build the checklist together with the team so they own its contents.
4. If that is not enough, use the Hawthorne effect: people change behavior when they believe they are observed. Announce that completed checklists will be verified. In practice occasional spot checks suffice; the perception of monitoring is what changes behavior.

## Developer code-completion checklist

Use when a developer declares code "done"; it effectively becomes the team's definition of done.

Include:
- Coding and formatting standards that automated tools do not enforce.
- Commonly forgotten items, such as swallowed (silently caught) exceptions.
- Standards specific to this project.
- Special team instructions or procedures.

Then audit every item for automation potential: linters, static analysis rules, code-crawling scripts, or custom plugins for the code validator. Some project rules (for example, "every public API class carries our routing annotation") may be hard to check; others (for example, "only methods in the service layer may call the audit writer") are easy to verify with a simple structural scan. Move the automatable ones out.

Invented sample:
```
[ ] IDE cleanup and formatting run
[ ] No empty catch blocks or swallowed exceptions
[ ] New endpoints registered with the gateway config
[ ] Feature flag added for user-visible change
[ ] Log statements contain correlation id
[ ] README or ADR updated if behavior changed
```

## Unit and functional testing checklist

Often the most valuable and usually the longest checklist, because it spans every kind of test. It captures unusual and edge cases developers tend to forget. Aim: when a developer finishes it, the code is essentially ready for production.

Typical items:
- Special characters in text and numeric inputs.
- Minimum and maximum boundary values.
- Unusual and extreme cases.
- Missing or empty fields.

Growth rule: every time QA finds a defect tied to a specific kind of test case, add that case to the checklist. Removal rule: when an item is covered by automated tests, delete it.

Benefits: gives developers a starting point when unsure what or how much to test, and where testing and development are separate teams it narrows the gap, freeing testers to concentrate on business scenarios the checklist does not reach.

## Software-release checklist

Release is among the most error-prone moments in the lifecycle, which makes it a strong candidate. It reduces failed builds and deployments.

Typical items:
- Configuration changes on servers or in external configuration services.
- Newly added third-party libraries or binaries.
- Database changes and their migration scripts.

This is the most volatile checklist. After every failed or troubled build or deployment, the architect does a root-cause analysis and adds an item so the next release verifies it.

## Maintenance rules

| Checklist | Grows when | Shrinks when |
|---|---|---|
| Code completion | A recurring review finding appears | A rule becomes a lint or static check |
| Testing | QA finds a defect class | The case is covered by automated tests |
| Release | A build or deployment fails | A pipeline step verifies the item |

Agent use: when asked to draft a checklist, first classify the process (ordered vs unordered, error-prone vs routine), then propose a short list, then mark each item "automate" or "keep manual".
