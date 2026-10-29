# Communicating Capabilities, Confidence, and Asking for Input

## Contents
- Making capabilities discoverable
- Avoiding option overload
- Per-modality patterns
- Communicating confidence and uncertainty
- Asking for guidance and clarification
- Worked example
- Pitfalls

## Making capabilities discoverable

Backend design decides what an agent can do; UX decides whether anyone finds out. Traditional apps expose actions through menus and buttons; text and voice agents have no visible affordances, so users guess. Close that gap with explicit patterns:

| Pattern | What it is | Best where |
|---|---|---|
| Suggested action chips | Buttons near the input showing common or context-relevant actions ("Summarize thread", "Check order status") | Chat UIs |
| Onboarding walkthrough | First-run tour of core functions | Any new user |
| Capability cards / sidebar menu | Structured list grouped by function (retrieve, analyze, summarize, automate) | GUI agents |
| Type-ahead intent suggestions | As the user types a verb, propose concrete completions mapping to supported tools | Text input bridging free language and tool calls |
| Conversational self-introduction | Opening line naming specific things the agent does | Open text or voice |
| Redirect on unsupported request | Say what cannot be done, then offer the nearest supported alternative or a human | All |

Redirect template: "I can't [requested action], but I can [closest supported action] or [hand off to someone who can]." Never return a bare refusal.

## Avoiding option overload

- Progressive disclosure: show core capabilities first; reveal advanced ones as the user gains fluency.
- Contextual ranking: surface the actions most likely given current input, history, and workflow stage.
- Visual grouping and hierarchy inside menus and chips.

## Per-modality patterns
- Text chat: quick-reply buttons, sample prompts.
- GUI dashboards: capability menus and tooltips that do not crowd the main view.
- Voice: list only a few top options per turn (two or three) to avoid overloading working memory.
- Generative UI: render available next actions as interactive components alongside the answer.

Outcome to aim for: users understand scope and limits, so they engage productively, trust outputs, and integrate the agent into routine work.

## Communicating confidence and uncertainty

Agent outputs are probabilistic, so confidence varies per answer. Three channels for expressing it:
- Explicit verbal statements of certainty (a percentage or plain-language level).
- Visual signals: icons, color coding, confidence meters.
- Behavioral shifts: offer options or suggestions instead of a firm recommendation when confidence is low; ask before acting.

Calibration rules:
- Never sound sure when uncertainty is high; confident wrong answers destroy trust fastest.
- Do not over-hedge low-stakes answers; constant caveats make the agent seem unreliable.
- Scale disclosure with stakes: in high-stakes domains (medical, legal, financial, irreversible actions) transparency about uncertainty is mandatory; in casual settings it can be lighter.

Stakes-by-confidence playbook:

| | High confidence | Low confidence |
|---|---|---|
| Low stakes | Answer directly | Answer with a light caveat or alternatives |
| High stakes | Answer, show basis/sources, confirm before acting | Do not act; explain uncertainty, ask, or escalate |

## Asking for guidance and clarification

No agent resolves every vague or conflicting request. Asking turns a likely error into collaboration.

Rules for good clarifying questions:
1. Ask when ambiguity would change the outcome materially; otherwise use a sensible default and state it.
2. Make the question focused and specific to the missing slots (trip type, dates), not generic ("Can you clarify?").
3. Reuse what the user already said; never re-ask answered parts.
4. Give a brief reason ("to book the right fare I need...") so the question feels purposeful.
5. Avoid interrogation: ask the most outcome-critical ambiguity first, sequence the rest, and bundle at most a couple of closely related slots per turn.
6. Vary phrasing; avoid robotic repetition.

Small helper for ordering questions (illustrative):

```python
def next_questions(missing, impact, already_known, max_per_turn=2):
    # missing: slot names; impact: slot -> outcome impact score
    open_slots = [s for s in missing if s not in already_known]
    ranked = sorted(open_slots, key=lambda s: impact.get(s, 0), reverse=True)
    return ranked[:max_per_turn]
```

## Worked example (invented)

User: "Send the contract to the client." Agent detects two candidate contracts and an unknown recipient address. Highest impact is which contract (wrong document is costly), so it asks: "To make sure the right file goes out: the Q3 renewal or the new services agreement? I'll use the client contact on file, jane@acme.example, unless you prefer another." It cites what it already knows, asks one decision, and states a default for the lower-impact slot. Since sending externally is high stakes, it shows a preview and waits for confirmation.

## Pitfalls
- A blank chat box with no hints.
- Showing every capability at once.
- Bare rejections of out-of-scope requests.
- Uniform confidence tone regardless of actual certainty.
- Five clarifying questions in one turn, or asking things already answered.
