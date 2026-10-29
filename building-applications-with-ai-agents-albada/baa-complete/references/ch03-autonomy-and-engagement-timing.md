# Autonomy Levels, Sync vs Async, and Proactive Engagement

## Contents
- The autonomy slider
- Five design principles for the slider
- Synchronous vs asynchronous: choosing
- Synchronous design checklist
- Asynchronous design checklist
- Proactive vs intrusive behavior
- Worked example
- Pitfalls

## The autonomy slider

Idea (credited to Andrej Karpathy): let users dial how much the agent does on its own, from none to full delegation, and move that dial at any time. Three canonical settings:

| Level | Agent behavior | Human role |
|---|---|---|
| Manual | No AI action; at most passive tooling (editor linting) or backend analytics | Does the work |
| Ask / Assist | Drafts suggestions, replies, refactors, policy references | Reviews, edits, approves each one |
| Agent / Auto | Executes routine actions without per-item approval; escalates hard or sensitive cases | Is notified; can intervene |

Two domain illustrations: in a coding tool, Auto might apply standard refactors, fix lint errors, and scaffold boilerplate per project conventions; in customer support, Auto might resolve password resets, order tracking and FAQs while routing complex or sensitive tickets to people. All three levels can coexist in one product, chosen per query type, customer profile, or organizational trust.

Why it matters: preferences change with trust, familiarity, stakes and workload. A fixed autonomy level makes the agent either underpowered (too much manual work) or overbearing (acting without consent in sensitive areas). The slider is a trust mechanism, not just a setting; it signals respect for user expertise.

Diagnostic question for any design review: how easily can a user move between manual, assisted and autonomous modes right now?

## Five design principles for the slider

1. Make the levels visible and named in plain words (Manual / Assist / Auto), each with a one-line explanation of what changes.
2. Make switching instant (a toggle or slider, not a settings page), so users can move up or down as confidence and workload change.
3. Define each level's behavior precisely and keep it consistent. Assist means draft then wait for approval. Auto still emits status updates and offers a way to stop or undo.
4. Explain the trade-off of each level (speed gained versus risk accepted). For critical tasks, require an explicit confirmation before full autonomy is enabled.
5. Adapt over time: suggest moving up as the user and agent build a track record. The book's example threshold: after about 10 successful manual uses, offer Assist. Generalize to a success count or acceptance rate per task type, and never auto-escalate silently.

Implementation sketch for principle 5 (illustrative):

```python
def suggest_level(stats, current, critical):
    # stats: dict with 'successes' and 'acceptance_rate' for this task type
    if current == "manual" and stats["successes"] >= 10:
        return "assist"   # offer, do not switch
    if current == "assist" and stats["acceptance_rate"] >= 0.95 and not critical:
        return "auto"     # offer with risk explanation
    return None
```

The thresholds beyond the first are assumptions to tune, not book numbers. Critical task types never get an automatic Auto suggestion without explicit confirmation.

## Synchronous vs asynchronous: choosing

- Synchronous: real-time exchange (chat, voice call, live collaboration, live dashboard). Use when the user needs instant feedback or is making a decision now.
- Asynchronous: agent and user work independently and communicate intermittently (notifications, email-like threads, reports delivered on completion). Use for long-running, background, or attention-optional work.

Rule: decide explicitly, per experience, which bucket it belongs in. The failure mode of leaving it implicit is a user staring at a spinner for a task that should have been fire-and-notify. If a request will likely exceed what a person will wait for interactively, switch it to async and say so.

## Synchronous design checklist
- Low latency and no re-asking for facts already given.
- Short, clear replies; long explanations break the rhythm.
- Turn-taking logic: when to answer, when to wait, when to escalate.
- Activity cues (typing indicator, spinner, streamed partial output) so silence is never ambiguous.
- Recover from misunderstandings in-line; when unsure, ask a clarifying question or redirect instead of guessing.

## Asynchronous design checklist
- Status transparency: what the agent is doing, which stage it is in, when the next update arrives.
- Lifecycle notifications: started (with ETA), meaningful progress, finished (with a short actionable summary), failed (with next step).
- Well-structured deliverables: summary first, detail after.
- Context persistence across long gaps; returning users should not re-explain (memory mechanics are covered in the book's memory chapter).
- Expectation management: timelines, progress indicators, follow-ups; uncertainty about progress is what frustrates.

## Proactive vs intrusive behavior

Proactivity helps when it surfaces urgent issues, useful optimizations, or timely reminders. Badly timed or irrelevant outreach disrupts work and can drive users away entirely.

Decision rule for any proactive message, check all four:
1. Relevance: does it solve a problem or deliver an insight the user would want? If it is noise, drop it.
2. Urgency versus current focus: is the user in something high-stakes (presenting, in a meeting)? If so, defer unless truly urgent.
3. Channel fit: interruptive channels (popups, calls) for urgent items; passive channels (email, digest, inbox) for completions and FYIs.
4. User control: does the user own frequency, channels, and escalation thresholds? Expose those settings.

The underlying skill is empathy for the user's workflow and mental state, not technical capability.

## Worked example (invented)

An expense-audit agent processes a quarter of receipts (about 40 minutes). Design: async. On submit it replies "Started; about 40 minutes; I'll message you in Teams when done." Midway it finds a duplicate charge above the user's alert threshold while the calendar shows the user presenting; it queues the alert and delivers it right after the meeting ends. On completion it sends a three-line summary plus a link to a dashboard where each flagged item has Approve / Dismiss buttons (Assist level). After the user has accepted the agent's flags across many runs, the agent offers to auto-dismiss low-value duplicates (Auto, for that sub-task only).

## Pitfalls
- One global autonomy level for all tasks and users.
- Auto mode that runs silently with no status or interrupt control.
- Escalating autonomy without asking.
- Synchronous UX for minutes-long jobs.
- Notifications without relevance filtering or user-controlled thresholds.
