# Risk Storming Playbook

## Contents
- Purpose and participants
- Scoping the session
- Phase 1: Identification (individual)
- Phase 2: Consensus (collaborative)
- Phase 3: Mitigation (collaborative, with business)
- Cadence
- Beyond architecture: user-story risk
- Facilitator checklist
- Pitfalls

## Purpose and participants

Risk storming is a team exercise for finding and scoring architecture risk. One architect cannot do it alone: a solo reviewer misses things, and almost nobody holds detailed knowledge of every part of a system.

Invite:
- Several architects.
- **Senior developers and tech leads (strongly recommended).** They bring the implementation view, and taking part teaches them the architecture.
- For phase 3, **business stakeholders who can approve spending**.

The architect running it is the **facilitator**. The facilitator owns the diagram (comprehensive or contextual, kept current) and distributes it to everyone before and during the session.

## Scoping the session

Analyze one dimension per session: either one criterion across the system ("where are our elasticity risks?") or one context across criteria ("what is risky in onboarding?"). A single dimension keeps attention focused and avoids confusion over what a note actually means.

If staffing or schedule forces several criteria into one session, participants write the criterion beside the number on each note, and the group discusses each criterion separately even when the notes sit on the same box. Example: three people all mark a shared cache as 6, but one means availability and two mean latency. These are two distinct risks, not agreement.

## Phase 1: Identification (individual)

Goal: an unbiased, independent view from every participant.

1. The facilitator sends an invitation containing: the architecture diagram (or a link to it), the criterion or context under analysis, the date, time and place (physical or virtual) of the collaborative session, and any logistics.
2. Each participant, working alone, applies the risk matrix (impact first, then likelihood) to areas of the diagram.
3. Each risk is written as its score on a note colored by band: green for 1 to 2, yellow for 3 to 4, red for 6 to 9.

Working alone matters: it prevents a vocal participant from anchoring others or steering attention away from areas they personally overlook.

## Phase 2: Consensus (collaborative)

Setup: a large printed diagram on a wall, or a shared screen or virtual whiteboard. On arrival, participants place their notes on the relevant components. Then classify each annotated area:

| Situation | Action |
|---|---|
| Everyone placed the same score | Accept it; no discussion needed |
| Scores differ | Ask the outliers (high and low) for their reasoning; usually the disagreement sits in one factor, so argue impact and likelihood separately |
| Only one person flagged it | Highest-value case: hear them out; they may hold experience nobody else has (for instance, having seen that product fail under comparable load) |
| A participant does not know the technology | Score it 9 automatically; record it as a knowledge gap |

Key behaviors:
- Either side may move. A lone high score can be talked down with evidence (redundancy exists), or it can convince the room that everyone else missed something. Both outcomes are why this phase exists.
- An unknown-technology flag is information, not ignorance to be dismissed. It tells the architect the team cannot yet operate or debug that piece; responses are substituting a familiar technology or funding training.
- The phase ends when all notes are consolidated into one agreed score per area.

## Phase 3: Mitigation (collaborative, with business)

Goal: reduce or remove the agreed risks. Expect to change parts of the architecture that previously looked finished. Responses range from a full redesign to targeted refactoring (for example inserting a queue to absorb a throughput bottleneck).

Mitigation almost always costs money or time, so:
1. Propose options with cost and the residual risk each leaves.
2. Bring them to stakeholders who have authority to weigh cost against risk.
3. If the first option is rejected as too expensive, offer a cheaper partial mitigation rather than dropping the matter.

Invented example: the team scores a single shared reporting database as 4 for availability. Option A, a multi-region cluster, costs about $80k a year. The product owner declines. The architect offers option B: split off the operational tables needed for order capture into their own database (about $20k), leaving reports on the old one. Order capture risk drops; reporting risk remains and is accepted. The negotiation, and its record, is a core output of risk storming.

Combined with assessments, risk storming gives you a way to find risk, track it, improve the design, and structure negotiations with the business on a shared, quantified footing.

## Cadence

Risk storming is continuous, not a one-off gate. Frequency depends on how often things change, on ongoing architecture refactoring, and on how incrementally the architecture is being built. Typical triggers:
- After a major feature lands.
- At the end of each iteration, on selected dimensions.
- Before a known demand event (seasonal peak, launch).
- When fitness-function trends show a criterion rising.

## Beyond architecture: user-story risk

The same matrix works during story grooming. For each story:
- Impact: how bad is it if the story is not finished this iteration?
- Likelihood: how probable is it that it will not be finished?

Track high-scoring stories closely, prioritize them early, and sum story risk to gauge the risk of the iteration as a whole.

## Facilitator checklist

- [ ] Critical characteristics known; one criterion or context chosen.
- [ ] Current diagram sent with the invitation and logistics.
- [ ] Developers and tech leads invited, not only architects.
- [ ] Individual scoring done before the meeting, independently.
- [ ] Agreed areas skipped; divergent, lone and unknown-tech areas discussed.
- [ ] Unknown technologies scored 9 and logged as gaps.
- [ ] Mitigations costed; a decision-maker present or scheduled.
- [ ] Revised diagram and assessment published; next session trigger set.

## Pitfalls

- Group scoring from the start (anchoring, groupthink).
- Discussing areas everyone already agreed on.
- Dismissing the lone voice or the "what is this?" question.
- Mixing criteria on one note without labels.
- Agreeing mitigations without anyone who can approve their cost.
- Treating one session as permanent clearance.
