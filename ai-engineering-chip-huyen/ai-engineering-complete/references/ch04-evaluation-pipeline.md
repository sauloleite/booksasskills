# Designing an evaluation pipeline for an AI application

## Contents
- Scope
- Step 1: evaluate every component
- Step 2: write the evaluation guideline
- Step 3: choose methods and data
- Evaluate the evaluation pipeline
- Iterate without losing comparability
- Pipeline design checklist
- Worked example
- Pitfalls
- Glossary

## Scope

Aimed at open-ended tasks; close-ended pipelines are a simpler version. Success depends on telling good outcomes from bad ones. No single method or number captures a high-dimensional system; combining methods offsets their weaknesses.

## Step 1: evaluate every component

- Evaluate at three levels: **per intermediate output** (each component), **per turn**, and **per task**.
- **Components independently.** In "scan an invoice to text, then extract the due date", a wrong date could come from either stage. Score stage one by similarity to ground-truth text, stage two by accuracy given correct text.
- **Turn vs task.** A turn may contain several internal steps. Turn-level grades each response; task-level asks whether the user's goal was met and in how many turns (two versus twenty is a different product).
- Task level matters more to users, but boundaries blur: a new chat message may continue a task or start another. Fix boundary rules before labeling.
- Task-level pattern: two model instances play a yes/no guessing game (one hides a concept, the other must find it), scored on success and number of questions. Reuse it: simulate a user with a goal, measure success and turns.

## Step 2: write the evaluation guideline

The most important step: vague guidelines yield misleading scores, and you cannot catch bad responses you never described.

### Define scope, including what the system must not do

List in-scope behaviour and out-of-scope inputs (a product support bot asked about an election), plus how to detect and answer the latter.

### Define criteria

- Defining "good" is usually harder than judging an output; large deployers call it their first obstacle.
- Correct can still be bad: a bare "you do not qualify" from a job-fit tool is accurate but useless; a good answer explains the gap and how to close it.
- Teams settle on two or three criteria (a survey found about 2.3 per application). Support-bot trio: relevance, consistency with context, safety.
- Find criteria empirically: run real queries, generate several responses each, label good or bad, write down why. The reasons become criteria.

### Scoring rubrics with examples

- Pick a scale per criterion: binary, three-way (contradiction -1, neutral 0, entailment 1), 1 to 5, or 0 to 1, depending on data and the decisions it drives.
- For each scale point, describe what qualifies and give an example with the reason.
- Validate with people; if they struggle or disagree, rewrite until unambiguous. Expect several rounds.
- The rubric later doubles as the annotation guide for finetuning data.

### Tie evaluation metrics to business metrics

- Know the business target first: stickiness (daily, weekly, monthly actives), engagement (conversations per user, session length), or efficiency (share of tickets automated).
- Map metric levels to impact, for example: grounding 85% auto-resolves 20% of tickets, 93% about 45%, 99% about 80%. A score can suit low-risk intents (product tips) yet fail high-risk ones (billing). The mapping tells you what an extra point is worth.
- Set a **usefulness threshold**: below it the product is not worth running even for easy requests.
- Ethics warning: chasing stickiness and engagement can push toward addictive features or extreme content.

## Step 3: choose methods and data

### Select methods per criterion

- Match method to criterion: small toxicity classifier for safety, semantic similarity for answer-to-question relevance, AI judge for consistency with the full context. Clear rubrics make scorers and judges work.
- **Mix cheap and expensive on one criterion:** a noisy cheap scorer on all traffic plus a strong judge on about 1%.
- **Use logprobs when available.** Even probabilities across three classes (each near a third) signal low confidence; one class near 95% signals high confidence. Logprobs also yield perplexity for fluency and consistency.
- **Automatic first, humans always.** Many teams treat expert review of a daily sample as the guiding metric, catching drift and odd usage (one large company reviews up to 500 conversations a day).
- **Plan for production:** references are usually missing but users are present. Decide which feedback to collect and how it relates to automatic metrics.

### Annotate evaluation data

- Label data for every component and criterion, at turn and task level.
- Prefer production data and natural labels (suggestion accepted, ticket reopened); otherwise humans or AI label against the rubric. Curated eval data can later seed synthetic training data.

### Slice the data

Slicing means scoring subsets separately. Uses:

- Detect bias against minority user groups.
- Debug: a weak subset may share a length, topic or format.
- Find improvements: if long inputs fail, try other processing or a long-context model.
- Avoid Simpson's paradox, where one system wins in every subgroup yet loses in aggregate because the subgroups are mixed in different proportions. Invented illustration from logged traffic where routing sent different mixes to each system:

| System | Short queries | Long queries | Overall |
|---|---|---|---|
| A | 90/100 = 90% | 120/200 = 60% | 210/300 = 70% |
| B | 170/200 = 85% | 50/100 = 50% | 220/300 = 73% |

A wins both slices but loses overall because it received more of the hard long queries. Always compare per slice and on matched mixes.

Recommended evaluation sets:

- A production-distribution set for the headline number.
- Slices by tier (paid vs free), channel (mobile vs web), usage, topic.
- Known-hard set; user-error set (typos, malformed input, if common in production); out-of-scope set.

Rule: anything you care about deserves its own test set.

### How much data

- Big enough to be reliable, cheap enough to rerun.
- **Bootstrap check:** resample N items with replacement from your N, score, repeat many times. Wide swings (say 70% vs 90%) mean the set is too small.
- **Comparing two systems:** significance tests need the score distribution, which you rarely know. A rough industry rule for 95% confidence: a 30-point gap needs about 10 examples, 10 points about 100, 3 points about 1,000, 1 point about 10,000. Each threefold shrink in the gap costs roughly tenfold more data, because the square root of 10 is about 3.
- **Reference sizes:** in a popular open harness the median benchmark has 1,000 examples and the mean is about 2,159. Organizers of one research prize called 300 the bare minimum and preferred 1,000 or more, especially for synthetic data.

## Evaluate the evaluation pipeline

Reliability matters most for subjective methods such as AI judges. Ask:

1. **Right signal?** Do better responses score higher, and do metric gains move business outcomes?
2. **Reliable?** Same data, same result twice? Low variance across eval sets? Fix configurations; judge temperature 0.
3. **Correlated?** Drop one of two perfectly correlated metrics. Uncorrelated metrics signal a real insight or a broken metric; find out which.
4. **Overhead?** Measure added latency and cost. Skipping evaluation to save latency is a gamble.

## Iterate without losing comparability

- Criteria, rubrics and examples will change with needs and user behaviour, but constant churn makes results incomparable. Change deliberately, in versions.
- Log every variable that can move a score: eval data version, rubric version, judge model, judge prompt, sampling settings.

## Pipeline design checklist

- [ ] Metrics for components, turns and tasks
- [ ] Guideline covers out-of-scope handling; criteria have scales and anchored examples validated by others
- [ ] Business mapping and usefulness threshold recorded
- [ ] Method per criterion, cheap/expensive mix, production feedback and daily human review planned
- [ ] Production-like, slice, hard, user-error and out-of-scope sets; bootstrap stable
- [ ] Judge temperature 0, repeat runs agree, metric correlations and eval overhead reviewed
- [ ] All evaluation variables versioned and logged

## Worked example

An internal HR policy assistant.

- Components: retriever scored on whether the right policy section is retrieved; generator on grounding given correct sections; end to end by an AI judge.
- Guideline: answers HR policy; declines legal advice and questions about specific colleagues, redirecting to HR staff.
- Criteria: relevance (binary), grounding (three-way), tone (1 to 5). Two colleagues labeled 50 items; tone disagreements forced clearer examples for scores 2 and 4.
- Business mapping: grounding above 95% allows answers without HR review; below 80% the tool is not worth running.
- Methods: NLI grounding on all answers, judge on 3%, HR reviews 30 conversations daily.
- Data: 600 production questions plus slices by office, typo, confusing-policy and out-of-scope sets. A new prompt scored 4 points higher; a paired bootstrap on the 600 put the interval above zero.
- Logged: dataset v3, rubric v2, judge model, prompt hash, temperature 0.

## Pitfalls

- Scoring only end-to-end output, or only turns and never task completion.
- Criteria without examples, or rubrics never tested on people.
- Declaring a winner from a small set without a bootstrap or size check.

## Glossary

- **Natural label:** outcome signal produced by real usage.
- **Usefulness threshold:** minimum score at which the application is worth running.
- **Simpson's paradox:** subgroup winners reversing in aggregate due to mix differences.
