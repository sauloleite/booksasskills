# Feedback Design and Feedback Limitations

## Contents
- Principles
- When to collect: four moments
- The positive-feedback debate
- How to collect: workflow integration
- Context, consent, transparency
- UI clarity
- Private versus public signals
- Feedback biases
- Degenerate loops and sycophancy
- Pre-training checklist
- Ownership and glossary

## Principles

Offer feedback options across the user journey, especially for reporting errors. Collection must be non-intrusive, easy to ignore, and free of extra work, and users should have a reason to give good feedback.

## When to collect: four moments

**Onboarding.** Calibration: a face unlock scan, reading a phrase for wake-word recognition, a placement quiz in a language app. Mandatory only if the product cannot work without it; otherwise optional, since it adds friction. If skipped, start neutral and calibrate from usage.

**When something goes wrong.** Hallucination, a wrongly blocked request, a compromising image, slowness. Offer downvote, regenerate, switch model, and accept plain remarks (too generic, shorter please).
- Let users still finish the task: if an item is miscategorized, let them fix the category. Collaboration with the AI comes first, and a human second; support bots commonly offer a human agent when chats drag on or users seem upset.
- Region-level editing is a strong pattern: in image inpainting the user selects the bad region and describes the fix, getting a better result while you get precise feedback. The same idea would help elsewhere (fixing one mispronounced word in generated speech).

**When the model has low confidence.** Ask the user to resolve it. Unsure between a short overview and a detailed summary: show both, if the extra generation does not hurt latency; the choice is preference data. Unsure whether two photos show the same person: ask.
- Full side-by-side responses demand reading effort and invite careless votes. Some products show only the openings and treat the expand click as the vote. Practitioners disagree on which is more reliable: full text informs the choice, but once both are read there is little incentive to click.

**When something good happens.** Thumbs up, favorite, share; see the debate below.

## The positive-feedback debate

Against: some design guidelines, including Apple's human interface guidelines, discourage requesting praise; good results should be the default, and asking implies they are exceptions. Happy users just keep using the product.

For: teams report that positive feedback shows which features users love, letting them focus on a few high-impact features.

Resolution: allow it but limit prompts, for example to about 1% of a large user base at a time. Smaller slices annoy fewer users but carry more bias, so keep the absolute sample large.

## How to collect: workflow integration

Make the user's natural next action the signal.

| Pattern | Signal |
|---|---|
| Image generator shows four candidates; user upscales one, varies one, or regenerates | Upscale: strongest positive. Variation: weaker positive. Regenerate: none good enough, or just exploring |
| Code assistant shows a grey inline suggestion; Tab accepts, typing on ignores | Accept vs ignore per suggestion |
| Email client drafts a reply | Sent, edited, or discarded |

Integrated products see downstream outcomes. Standalone chat assistants cannot tell whether a drafted email was ever sent, so they must lean on in-conversation signals.

## Context, consent, transparency

- Bare thumbs suffice for satisfaction analytics; diagnosis needs context, roughly the previous 5 to 10 turns.
- That context may include PII, so capturing it can need explicit consent: terms of service covering analytics and improvement, or a **data donation** checkbox at feedback time.
- Explain the use (personalization, aggregate statistics, model training); clear explanations raise feedback volume and quality.
- Promise privacy (no training use, data stays on device) only when it is true.

## UI clarity

- Never ask users to choose between answers they cannot evaluate, and never ask for a preference where there is an objectively correct answer (a statistics result). Provide an "I don't know" or skip option.
- Add icons and tooltips where they aid understanding.
- Test scale direction: one event-feedback form placed its angry emoji in the five-star position, so delighted attendees submitted one-star ratings next to glowing comments.

## Private versus public signals

Visibility shapes behavior and data quality.
- **Private** signals are more candid and plentiful because users feel less judged; after a large social network made likes private in 2024, its owner claimed a notable rise in likes.
- **Public** signals support discoverability and explainability: users find what connections liked, and like-based recommendations make sense. Hiding them can make recommendations confusing.
- Some products start public (an image generator's early upscale and variation choices were visible to all). Decide deliberately.

## Feedback biases

| Bias | Effect | Mitigation |
|---|---|---|
| Leniency | Ratings inflated to be nice or to dodge a follow-up "what went wrong?" | Never demand extra work after a low rating; inspect the distribution; use descriptive options instead of bare numbers to destigmatize low scores |
| Randomness | Unmotivated users click arbitrarily (long side-by-sides, which image to vary) | Shorter comparisons, previews, attention checks, filtering |
| Position | First option clicked more regardless of merit | Randomize order, or model success rate conditioned on position |
| Length | Longer answer preferred even when less accurate, since length is easier to spot than errors | Length-controlled comparisons; audit winners for accuracy |
| Recency | Last-seen option favored | Randomize and balance presentation |

Leniency case: a ride-hailing platform reported a 4.8 average driver rating in 2015, with drivers under about 4.6 at risk of removal, so four stars effectively meant trouble. It still served the goal of separating good from bad drivers. Ask whether a bias defeats your specific goal, not just whether it exists. Inspect each app's feedback for its own biases before deciding on it.

## Degenerate loops and sycophancy

- **Exposure censoring**: you get feedback only on what you showed; unshown options never accumulate evidence.
- **Degenerate feedback loop**: predictions shape the feedback that trains the next model, amplifying initial bias. A recommender ranks video A slightly above B; A gets more clicks because of its rank; the next model ranks A higher; B vanishes. The literature calls this exposure bias, popularity bias, or filter bubbles.
- **Product drift**: a few early users reward a niche taste, the system produces more of it, which attracts more such users, and the product and user base reshape around it. The same mechanism can amplify racism, sexism, or explicit content.
- **Sycophancy**: optimizing for user approval teaches models to tell users what they want to hear over what is accurate or useful (Stray, 2023); Sharma et al. (2023) found human-feedback-trained models tend to echo the user's stated views.

Mitigations: reserve exploration traffic that surfaces non-top options; log display position and selection probability for debiasing; keep objective quality metrics beside approval and block updates that raise approval while cutting accuracy; run sycophancy probes (user asserts a falsehood) before and after training; monitor content and population concentration.

## Pre-training checklist

- [ ] Purpose defined (evaluation, development, personalization)
- [ ] Consent covers the captured context
- [ ] Leniency, position, and length bias measured
- [ ] Random clicks and abstentions filtered
- [ ] Exposure handled (exploration or propensity weighting)
- [ ] Accuracy and sycophancy checked on a held-out set
- [ ] Concentration monitored after release

## Ownership and glossary

Feedback design used to be seen as product work and was often neglected by engineers. Since feedback now feeds model improvement, AI engineers should help design it to get usable data, part of AI engineering's shift toward product as the data flywheel and user experience become the competitive edge.

- **Data donation flow**: opt-in sharing of recent interactions with feedback.
- **Degenerate feedback loop**: self-reinforcing bias from training on feedback the model's own outputs shaped.
- **Sycophancy**: feedback-trained models agreeing with users over being accurate.
