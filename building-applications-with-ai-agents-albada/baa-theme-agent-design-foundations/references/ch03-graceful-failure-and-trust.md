# Failing Gracefully and Building Trust

## Contents
- Graceful failure playbook
- Fallback ladder
- Failure message anatomy
- Trust: transparency and predictability
- Reliability checklist
- Chapter-wide pattern summary
- Worked example
- Pitfalls

## Graceful failure playbook

Failures are certain (missing data, ambiguous input, tool limits, edge cases). The handling of failure shapes trust as much as success does. Every failure response should:
1. Acknowledge the problem honestly; never fabricate an answer to avoid admitting a gap.
2. Explain briefly in user terms (not stack traces).
3. Offer concrete next steps: retry, rephrase, alternative resource, troubleshooting steps, or human escalation.
4. Preserve progress in multistep tasks so the user resumes rather than restarts.
5. Use considerate, apologetic wording; avoid cold or technical error text.
6. Log the failure for later analysis.

Learning loop: record failure points, cluster recurring ones, feed them into prompts, tools, routing or UX fixes, and track whether the rate drops. Agents that iterate on their failure patterns become steadily more resilient.

## Fallback ladder

Prepare predefined fallbacks for predictable failure points; escalate one step at a time:
1. Clarify: ask a targeted question.
2. Rephrase prompt to the user: suggest wording or examples.
3. Switch modality: if speech recognition fails repeatedly, offer typing or a text link.
4. Degrade scope: deliver the part that works, flag what is missing.
5. Escalate: hand to a human with full context attached so the user does not repeat themselves.

## Failure message anatomy

[apology/acknowledgment] + [plain reason] + [what is saved] + [options]

Example (invented): "Sorry, I couldn't reach the shipping system just now. Your return request is saved. I can retry in a minute, email you once it goes through, or connect you to support."

## Trust: transparency and predictability

Trust accumulates slowly and collapses quickly (the book frames it as "gained in drops and lost in buckets"). Two levers:

Transparency
- State capabilities and constraints so users never wonder whether a task is in scope.
- Explain decisions at the right moments: how a recommendation was reached, why a request was declined, how an ambiguous instruction was interpreted. Explanations also teach users to give better instructions.
- Do not dump the full reasoning trace. Give enough insight for confidence, via status messages, visual cues, and one-line rationales; keep detail available on demand.

Predictability
- Consistent behavior across similar situations; users should be able to anticipate responses from experience.
- Inconsistency damages trust even when each answer is defensible (cautious in one case, brashly confident in a near-identical one).

## Reliability checklist

- [ ] Same question under same conditions yields the same answer (pin temperature/seed/prompt versions where feasible; cache deterministic lookups).
- [ ] Where variation is unavoidable, the agent signals that the answer is uncertain or context-dependent.
- [ ] Defined, consistent behavior for edge cases (incomplete data, conflicting instructions, ambiguity): clarify, neutral fallback, or escalate, chosen by rule rather than by chance.
- [ ] Resilience: recover from errors, keep state through interruptions, isolate failures so they do not cascade.
- [ ] Dependency outages are surfaced: if an external API is down, tell the user, explain, and propose a next step; never fail silently or return misleading output.
- [ ] Promises match delivery: only claim capabilities that work every time. Overpromising then underdelivering hurts trust more than stating limits up front.

## Chapter-wide pattern summary

Use as a final design-review gate:
- Capabilities communicated (onboarding, suggestions, buttons).
- Modalities matched to task and context.
- Context retained without bloat or privacy violations.
- Errors handled with clear, polite fallbacks.
- Trust built through openness about limits, confidence and reasoning.

Closing stance: core product principles outlast modality trends. Re-evaluate interaction paradigms regularly as capabilities shift, but anchor on clarity, adaptability, transparency and trust.

## Worked example (invented)

A travel agent bot calls a fare API that times out during step 3 of 5. Bad: it says "Error 504" and clears the form. Good: "Sorry, the airline's pricing service isn't responding. Your passenger details and dates are saved. Want me to retry, check another carrier, or have an agent finish this by email?" The failure is logged with step, dependency and latency; weekly review shows this API times out at peak hours, so the team adds a cached-fare preview and an async completion path.

## Pitfalls
- Hallucinating an answer instead of admitting failure.
- Restarting multistep flows after an error.
- Technical or blaming error copy.
- Silent dependency failures.
- Marketing capabilities that work only sometimes.
- Exposing raw chain-of-thought as "transparency".
