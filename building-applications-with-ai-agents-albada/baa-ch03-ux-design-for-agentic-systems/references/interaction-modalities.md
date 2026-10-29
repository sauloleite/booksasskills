# Interaction Modalities: Choosing and Combining Text, GUI, Voice, Video

## Contents
- Selection matrix
- Text interfaces
- Graphical interfaces and generative UI
- Speech and voice interfaces
- Video interfaces
- Combining modalities
- Pitfalls
- Glossary

## Selection matrix

Pick the modality from the user's situation, not from what is newest. Rough maturity ordering in production today: text (ubiquitous) > GUI (widespread) > voice (mainstream only for simple assistants) > video (rare, experimental).

| Modality | Pick it when | Main weakness to design around |
|---|---|---|
| Text (chat, CLI, messaging) | Precision matters, the exchange may be async, a searchable/auditable record is valuable | Poor discoverability: no visible affordances |
| GUI / dashboard / IDE | Multistep workflows, status at a glance, data to compare, approvals | Limited screen space, responsiveness, cross-device layout |
| Generative UI | Open-ended questions whose answers benefit from structure (cards, tables, forms) | Generated layouts can be incoherent or overloaded |
| Voice | Hands are busy (driving, cooking, machinery), accessibility, short action-oriented tasks | Slow for dense content; latency; interruptions |
| Video / avatar | Demonstration, emotional expression, immersive tutoring or telehealth | Bandwidth/compute cost, uncanny valley, privacy |

Quick decision questions:
1. Are the user's hands or eyes occupied? If yes, voice first.
2. Must the user compare, skim, or review dense output? If yes, text or GUI; never voice alone.
3. Does the task span several steps with intermediate state or approvals? If yes, GUI.
4. Is an auditable record needed (claims, support, compliance)? If yes, text record even if another modality fronts it.
5. Is emotional presence the core value (tutoring, coaching)? Consider video, but prototype for uncanny-valley risk first.

## Text interfaces

Strengths: familiar, cheap to deploy, works synchronously and asynchronously (the user can come back later without losing the thread), and leaves a traceable transcript that helps accountability and debugging. AI-augmented terminals (Warp, Claude Code, Gemini CLI) show text getting more powerful: users state intent in plain language and the agent produces, runs and debugs commands, lowering the barrier for novices without slowing experts.

Core problem: discoverability. Users cannot see what the agent supports, so they guess, underuse it, or hit opaque refusals (example: asking a support bot to change an order field it cannot touch).

Design checklist for text agents:
- Announce capabilities: in the greeting, in occasional reminders, and as in-flow suggestions. A greeting should name two to four concrete things the agent can do, not just ask an open question.
- Keep replies short and plain; no jargon walls.
- Carry context across turns so users never restate earlier instructions.
- On failure, give a clear message plus a fallback (alternative suggestion or human escalation).
- Manage turn-taking: decide when to ask a follow-up versus when to stop and wait.
- Invest in intent recognition; phrasing will be unpredictable.
- Calibrate length: too terse reads as cryptic, too long overwhelms.
- Convey tone (empathy, urgency) deliberately through wording, since there is no voice or face.

Good fits: FAQ-style support, CLI productivity tools, knowledge retrieval over documents or databases, chat over Slack/Teams/WhatsApp, text-heavy work such as claims processing or research.

## Graphical interfaces and generative UI

Strengths: visual information is processed faster than prose, so dashboards, progress bars, color coding and alert icons lower cognitive load and show system state at a glance. Node-based workflow builders (n8n, LangSmith, Arize, AutoGen visualizers) make agent flows (tool calls, branches, outputs) inspectable without reading code. AI IDEs (Cursor, Windsurf, Cline, Copilot) embed an assistant panel next to the editor.

Generative UI: the agent emits interface elements on demand (knowledge cards, tables, reference lists, forms, config files) instead of filling a fixed layout. It pairs natural-language flexibility with graphical discoverability and extends GUIs from predefined workflows to open-ended tasks. Guard it with layout constraints, component libraries, and prioritization rules so generated screens stay coherent and uncluttered.

Classic GUI challenges still apply:
- Screen space: rank information so critical items are not buried.
- Responsiveness: stream updates and animate state transitions smoothly, especially when the agent works asynchronously.
- Device adaptation: the same state must render sensibly on desktop, tablet and phone.
- Automation versus control: let the agent propose and the user dispose. Example: a scheduling agent shows three slot buttons; one click confirms.

Best fits: task dashboards, AI analytics, e-commerce recommendations with filters and previews, and hybrid flows where the agent works in the background and surfaces options for confirmation.

Forward-looking recommendation: developer tools already have excellent agentic GUIs; the open opportunity is designing equivalent decision-centric interfaces for lawyers, accountants, insurers, product managers and other knowledge workers, rather than bolting chat onto documents and spreadsheets.

## Speech and voice interfaces

Strengths: hands-free use and accessibility for users with visual or motor impairments.

What changed: latency used to make voice feel robotic (transcribe, interpret, respond in series). Low-latency recognition and realtime speech models now allow natural turn-taking, and voice agents can call tools to fetch context, update records, book appointments or place orders.

Caveat: fully multiturn, context-aware, action-taking voice agents are still uncommon in enterprises; treat voice as frontier work and budget for iteration.

Throughput numbers that drive design:
- Speaking: about 150 to 180 words per minute.
- Reading: about 250 to 300 wpm; skimming: above 500 wpm.
- Implication: voice is roughly half the speed of reading and far slower than skimming. Keep spoken output to short summaries and send detail to a screen or message.

Interruption handling (barge-in) is a first-class requirement: users correct themselves mid-sentence ("for 7pm, no, make it 8"). The agent must stop speaking immediately when the user starts, discard the unspoken remainder, merge the correction, and continue without forcing a restart.

Minimal barge-in pattern (framework-agnostic sketch):

```python
async def relay_events(model_stream, speaker, model):
    current_reply = None
    async for event in model_stream:
        if event.kind == "audio_chunk":
            current_reply = event.reply_id
            await speaker.play(event.audio)
        elif event.kind == "user_speech_started" and current_reply:
            await speaker.flush()              # stop local playback now
            await model.cancel(current_reply)  # drop unspoken remainder
            current_reply = None               # next user turn wins
```

Architecture notes: stream audio both ways over a persistent socket; use server-side voice activity detection for turn boundaries; keep sample formats consistent end to end; truncate the assistant item on user speech.

Best fits: short hands-free tasks, quick lookups, action commands; clinical note dictation; replacing rigid IVR trees in call centers; field and industrial workers logging observations or controlling equipment. Poor fits: dense information, side-by-side comparison, complex decisions.

## Video interfaces

Forms: talking avatars simulating face-to-face conversation, and agents inside video tools (Zoom, Teams, virtual events), with AR overlays emerging.

Strength: combines facial expression, gesture, speech, captions and animation, which adds emotional nuance (an avatar visibly reassuring an upset customer).

Risks to test before committing:
- Compute and bandwidth: lag and pixelation destroy the experience.
- Uncanny valley: slightly-off lip sync or expressions create discomfort, not rapport.
- Privacy: users are warier of sharing camera feeds with AI.

Likely domains: telehealth, education and tutoring, remote collaboration, entertainment, service avatars.

## Combining modalities

Users think in goals, not channels. The strongest experiences let a task move across modalities while keeping state.

Worked example (invented): a field sales rep dictates "prep me for the Acme visit" while driving; the agent answers with a 20-second spoken brief, then pushes a text summary to the phone; at the desk the rep opens a dashboard with pipeline charts and the same open action items, already marked with what was discussed in the car.

Requirements:
- One shared task state and preference store behind every channel, keyed to the user, not to the channel session.
- Per-modality rendering: concise when spoken, fuller when written, structured when visual.
- Explicit handoff cues ("I've sent the full report to your inbox").

Product warning: new modalities and generative UI are not goals in themselves. Start from a deep understanding of users and their situation; use technology to amplify them unobtrusively.

## Pitfalls
- Choosing voice for content users need to skim or compare.
- A chat box with no capability hints (discoverability failure).
- Generative UI with no layout constraints, producing cluttered screens.
- Losing task state when the user switches device or channel.
- Shipping a video avatar without uncanny-valley and bandwidth testing.

## Glossary
- Affordance: a visible cue that signals what action is possible.
- Discoverability: how easily users can find out what the system can do.
- Generative UI: interface components created at runtime by the model for the current request.
- Barge-in: the user speaking over the agent; the agent should yield.
- Uncanny valley: discomfort caused by near-but-imperfect human likeness.
