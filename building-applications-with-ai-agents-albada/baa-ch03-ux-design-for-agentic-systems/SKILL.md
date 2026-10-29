---
name: baa-ch03-ux-design-for-agentic-systems
description: UX design guidance for AI agents: choosing and combining modalities (text, GUI, generative UI, voice, video), autonomy sliders, sync vs async flows, proactive notifications, context and personalization, capability discovery, confidence signaling, clarifying questions, graceful failure and trust. Based on Chapter 3 of Michael Albada's "Building Applications with AI Agents". Use when designing or reviewing an agent's user-facing interaction, picking a modality, setting human-approval levels, writing error or clarification flows, or diagnosing low adoption or trust.
---

# UX Design for Agentic Systems (Albada, Ch. 3)

Purpose: help an engineer shape how users experience an agent, so its capabilities are discoverable, its autonomy matches user trust, its context persists, and its failures and uncertainty strengthen rather than erode trust. Apply the rules below directly; open a reference when you need the detailed checklist, playbook, or worked example for that area.

## Key decision rules

Modality
- Choose modality from the user's situation: hands busy or accessibility need, voice; dense, comparable or auditable content, text or GUI; multistep workflows, status and approvals, GUI; emotional presence or demonstration, video (test uncanny valley, bandwidth, privacy first).
- Voice runs about 150 to 180 wpm versus 250 to 300 wpm reading and 500+ skimming: keep spoken output to short summaries and route detail to a screen or message.
- Voice agents must support barge-in: stop speaking the instant the user talks, discard the unspoken remainder, merge the correction.
- Text agents lack affordances: always announce concrete capabilities and redirect unsupported requests to the nearest supported option.
- Generative UI needs layout constraints and prioritization or it overwhelms.
- Multimodal journeys need one shared state behind all channels and per-channel rendering (brief spoken, fuller written, structured visual).

Autonomy and timing
- Offer an autonomy slider (Manual / Assist / Auto), visible, named in plain words, switchable instantly, with consistent behavior per level.
- Assist means draft and wait for approval; Auto still reports status and allows intervention.
- Explain the risk of each level; require explicit confirmation before full autonomy on critical tasks.
- Suggest (never force) a higher level after a track record; the book's example is about 10 successful manual uses before offering Assist.
- Classify every experience as synchronous or asynchronous up front; long-running work goes async with start, ETA, progress and completion notices, never a spinner.
- Sync: low latency, brief replies, activity indicators, clarify instead of guessing.
- Proactive messages must pass relevance, urgency-versus-current-focus, and channel-fit checks; users control frequency, channels and thresholds.

Context and personalization
- Default to hybrid context: short-term on the client for speed, durable state on the server for continuity.
- Bind state to account (logged in) or session token (anonymous); at scale persist state in a DB or distributed cache, not process memory.
- Validate stored state, define session boundaries, and ask when context is missing.
- Personalize via preference retention, behavioral adaptation and proactive help, always disclosed and resettable. Retain only what is useful and privacy-safe.

Communication, failure, trust
- Make capabilities discoverable (chips, onboarding, capability cards, type-ahead suggestions) with progressive disclosure and contextual ranking; voice lists only a few options.
- Calibrate confidence to stakes: no confident tone under high uncertainty, no heavy hedging on trivial answers; in high-stakes contexts disclose uncertainty and confirm before acting.
- Clarifying questions: specific, reuse known facts, explain why, most critical ambiguity first, few per turn.
- Fail gracefully: acknowledge, explain plainly, preserve progress, offer next steps (retry, switch modality, escalate to a human), apologize, log for a learning loop.
- Trust rests on transparency (scope, rationale, enough reasoning without overload) and predictability (consistent answers; signal unavoidable variation; surface dependency outages). Never overpromise.

## Default workflow

1. Map users, environments and tasks; pick primary and secondary modalities with the selection matrix.
2. Classify each flow as sync or async; define notifications and proactive-outreach rules.
3. Define autonomy levels per task type, approval points, and escalation criteria.
4. Design context: identity scope, storage placement, session boundaries, personalization controls.
5. Design discovery: greeting, chips, capability menu, out-of-scope redirects.
6. Design uncertainty and clarification behavior by stakes.
7. Write the failure ladder and message templates; add failure logging.
8. Review against the five-pattern gate: capabilities communicated, modalities matched, context retained responsibly, errors handled, trust built.

## References

- [references/interaction-modalities.md](references/interaction-modalities.md): read when choosing or combining text, GUI, generative UI, voice or video, or when building a voice agent with interruptions.
- [references/autonomy-and-engagement-timing.md](references/autonomy-and-engagement-timing.md): read when setting human-approval levels, deciding sync vs async, or designing notifications and proactive behavior.
- [references/context-and-personalization.md](references/context-and-personalization.md): read when deciding where context lives, handling state for anonymous or logged-in users at scale, or adding personalization.
- [references/capabilities-uncertainty-clarification.md](references/capabilities-uncertainty-clarification.md): read when users do not know what the agent can do, when expressing confidence, or when writing clarifying-question logic.
- [references/graceful-failure-and-trust.md](references/graceful-failure-and-trust.md): read when designing error handling, fallbacks and escalation, or reviewing an agent for trust, predictability and reliability.
- [references/source-map.md](references/source-map.md): read to locate which reference covers a given chapter section.

## Scripts

None. The chapter offers design principles rather than calculations, so no script is included.
