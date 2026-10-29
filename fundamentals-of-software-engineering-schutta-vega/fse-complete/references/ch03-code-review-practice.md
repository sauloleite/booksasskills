# Code Review Practice: Focus, Format, Tone and Trust

Covers: what reviews are for, where to spend review effort, checkbox and rubber-stamp reviews, pull request dynamics, giving and receiving criticism, and building team trust around reviews.

## Contents
- Purpose and forms
- Where to spend attention
- Anti-patterns
- Giving feedback humanely
- Escalation and private conversations
- Building trust and shared learning
- Comment rewrites (examples)
- Reviewer checklist

## Purpose and forms

A review can be anything from a quick "does this method look right?" to a long multi-person walk-through, and pair programming is continuous review. Whatever the format, the goals are learning, sharing experience, spreading knowledge, collective code ownership and team trust. Better code is the output; the reviewer's ego is not.

## Where to spend attention

Think of review concerns as a pyramid (the Code Review Pyramid): the cheap, mechanical layer is formatting and style, and it should be fully automated with formatters and linters. Human time belongs on what tools cannot judge:
- Do identifiers say plainly what they mean?
- Could someone new to this area follow it?
- Is logic duplicated?
- Are logging, tracing and metrics adequate for running it in production?
- Do new interfaces match conventions used elsewhere in the system?
- Did the author use an error-prone form?
- Is the domain model right?
- Is this the right abstraction, or the wrong one?

Agent behavior: when reviewing, do not lead with style nits a formatter would fix. Order findings by the list above, model and abstraction issues first if present.

## Anti-patterns

- Checkbox review: mandatory pre-merge review degenerates into a colleague ticking approve without reading. Well-intended policy, no value. Countermeasure: small batches, which make real review fast enough that people actually do it.
- Rubber-stamp ("looks fine to me") approvals on pull requests: occasionally acceptable for trivial changes, otherwise just another checkbox.
- PRs as a battleground: nitpicking, turf fights, or reopening decisions already settled.
- Showing off: dropping obscure trivia to display expertise instead of improving the code.
- Text-only harshness: written comments lack tone and body language, so neutral remarks can land as cutting. Junior developers in particular may come to dread PRs.

## Giving feedback humanely

People invest themselves in their work, so criticism stings. Rules:
- No snark, no sarcasm.
- Review the code, not the coder; keep it impersonal.
- Never use a review to embarrass someone for missing a new language feature or a simpler approach. Everyone has gaps.
- Be humble; ask questions rather than issuing verdicts.
- Mention what is good, not only what is wrong; balanced feedback is easier to absorb.
- Share personal experience ("on a previous project this pattern caused X"); stories lower resistance more than rules do.
- Avoid sweeping pronouncements. Before declaring something will not work, check for constraints or background you might not know.
- Treat it as the Golden Rule in practice; senior engineers should model the tone they want.

## Escalation and private conversations

If something worries you, talk to the author one-on-one. Group settings make people defensive, and ambushing someone in front of the team helps no one. A quiet conversation usually resolves more, faster.

## Building trust and shared learning

- Encourage questions and constructive feedback in both directions.
- Flag confusing idioms and deprecated approaches as shared learning, not as failures.
- Run a recurring "bug of the week" or a short slot (say, in the Friday standup) where people describe an interesting defect and how they fixed it. Knowledge you assume is common often is not.
- Be kind, do what is right, do what works.
- Inspect the review process itself regularly, Agile or not, and change what is not working.

## Comment rewrites (examples)

| Instead of | Try |
|---|---|
| "Obviously this should be a stream." | "Would a stream pipeline read more clearly here? Happy to pair on it." |
| "This will never scale." | "What load do we expect? At 10x I think this query becomes a full scan; is there a constraint I'm missing?" |
| "Wrong." | "I expected X here because of Y. Can you walk me through the choice?" |
| (approve with no comments on a 900-line PR) | "This is too big for me to review well. Could we split it by concern?" |

## Reviewer checklist
- Formatting and style left to automation?
- Names, readability, duplication checked?
- Observability (logs, traces, metrics) present?
- Interfaces consistent; no error-prone forms?
- Model and abstraction sound?
- Tone: questions not verdicts, positives noted, nothing personal?
- Anything sensitive moved to a private conversation?
- Batch small enough for a real review?
