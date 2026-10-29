# Ranking Models with Comparative Evaluation

## Contents
- Pointwise vs comparative
- How a comparative evaluation runs
- When preference is the wrong question
- Win rates and rating algorithms
- What makes a ranking correct
- Challenge 1: scalability
- Challenge 2: standardization and quality control
- Challenge 3: from relative to absolute performance
- Why comparative evaluation still matters
- Playbook: an internal comparative leaderboard
- Worked example: is a 55% win rate worth double the cost?
- Glossary

## Pointwise vs comparative

Often you want a choice, not a score. Two routes to a ranking:
- **Pointwise**: score each model independently, then sort. Hard part: designing benchmarks and metrics; sorting is trivial.
- **Comparative**: show several models' outputs for the same input, ask which is better, compute a ranking from outcomes. Both collecting signals and computing the ranking are hard.

For subjective quality, picking the better of two is usually easier than assigning absolute scores (which of two jingles is catchier vs rating each out of 10). Anthropic first used it to rank language models in 2021; LMSYS Chatbot Arena runs on it; providers also collect side-by-side choices in production, where outputs may come from different models or one model with different sampling settings.

Not the same as A/B testing: there each user sees one variant; here the evaluator sees several at once.

## How a comparative evaluation runs

1. Two or more candidates answer each request; public arenas hide identities until after the vote.
2. A human or AI evaluator picks a winner. Allow ties so equally good or bad pairs are not decided at random.
3. Each comparison is a match: (model A, model B, outcome).
4. A rating algorithm turns match history into scores and a ranking.

## When preference is the wrong question

- **Factual questions** need correctness grading. Letting users vote between "yes" and "no" on a health-risk question yields wrong signals that, used in training, push toward misaligned behavior.
- **Users who lack the expertise** cannot pick the right one of two math answers they asked for precisely because they could not compute it, and being asked is frustrating.
- **Where it works**: assistant-style use, where AI speeds up tasks users know how to do and can verify.

Design rule: classify each request type as preference-appropriate or correctness-appropriate before adding side-by-side voting.

## Win rates and rating algorithms

- **Win rate of A over B**: share of A-vs-B matches A won (state how ties count).
- Two models: rank by win rate. Many models: pairwise rates are sparse and can conflict, so you need a strength model.
- Algorithms from sports and games: **Elo** (online updates per match), **Bradley-Terry** (fits a strength per model with P(A beats B) = s_A / (s_A + s_B), from all matches at once), **TrueSkill** (Bayesian, tracks uncertainty, supports multi-player matches).
- Chatbot Arena moved from Elo to Bradley-Terry because Elo results shifted with the order of votes and prompts. It kept labeling ratings "Elo" for a while by rescaling Bradley-Terry strengths (times 400, plus 1,000, then shifted so a reference model sits at 800). Arena numbers are a display scale, not raw Elo.

Practical choice: Bradley-Terry for batches (order-invariant); Elo with a modest K for streaming updates, refit with Bradley-Terry periodically; TrueSkill when you need explicit uncertainty or team matches. Run `scripts/rank_matches.py` to fit Elo and Bradley-Terry and compare held-out accuracy.

## What makes a ranking correct

A ranking is correct if every higher-ranked model beats every lower-ranked one more than half the time. There is no ground-truth ranking, so treat ranking as prediction: fit on past matches, test on held-out future ones, and prefer the algorithm that predicts better. Analyses of Chatbot Arena suggest good predictive quality for pairs with many matches and weak quality for thinly sampled pairs.

## Challenge 1: scalability

- Pairs grow quadratically, n(n-1)/2. For scale: 57 models with 244,000 comparisons averaged only about 153 per pair across 1,596 pairs, thin for the range of tasks involved.
- **Transitivity** lets algorithms infer A > C from A > B and B > C. It may not hold: human preferences need not be transitive, and different pairs are judged by different people on different prompts. Several analyses name this a core limitation of Elo-style model evaluation.
- **New models** must play incumbents and can reshuffle the existing ranking; pointwise evaluation tests only the newcomer.
- **Private models** cannot easily enter public arenas; build your own pipeline or pay for a private evaluation.
- **Mitigation: smarter matchmaking.** Stop pairing models whose order is settled; sample matches that most reduce ranking uncertainty (close ratings, few matches).

## Challenge 2: standardization and quality control

Crowdsourced arenas capture diverse real preferences and are relatively hard to game, but:
- **No standard of "better"**: volunteers rarely fact-check, so confident wrong answers can win.
- **Wild preferences may not fit your product**: some voters punish refusals your product would want (declining an offensive joke); some vote maliciously for toxic output; gaming attempts grow with popularity.
- **Ungrounded prompts**: voters type whatever comes to mind, rarely use advanced prompting, and are outside their work context. In one public release of tens of thousands of arena prompts, about 0.5% were bare greetings (more with variants), and one sibling-counting riddle appeared dozens of times. Easy prompts do not discriminate and pollute rankings.
- **No support for your context construction**: without your retrieved documents or tools, the ranking says little about a model inside your RAG system; generating from good context differs from finding it.

| Quality approach | Benefit | Cost |
|---|---|---|
| Fixed prompt set | Standardized | Loses real-use diversity |
| Free prompts, then keep only hard ones via a classifier (LMSYS) | Diversity plus discrimination | Depends on the filter |
| Trained evaluators with realistic prompts (Scale's private leaderboard) | Reliable | Expensive, far fewer comparisons |
| In-product comparisons (two code completions in the editor) | Real workflows and context | Users may lack expertise or click without reading; noisy, though a minority of careful voters can still separate models |
| AI evaluators | Scalable, more reliable than random crowds | Inherit judge biases |

## Challenge 3: from relative to absolute performance

Products need good enough, not necessarily best. "B beats A" fits B good and A bad, both bad, or both good; other evaluation decides which. Suppose A resolves 70% of support tickets and B wins 51% of matches: how many more tickets B resolves is unknown, and practitioners report that a one-point win-rate change can mean a large gain in one application and almost none in another. If B costs twice as much, the comparison cannot justify switching.

Rule: before switching, measure both on an absolute task metric on your data and price the difference.

## Why comparative evaluation still matters

- **Beyond-human outputs**: raters who cannot score an answer absolutely can often still tell which of two is better (the Llama 2 report found this for writing beyond the best annotators). It may become the only workable human signal.
- **Targets the real objective**, human preference, and eases the race to build new benchmarks.
- **Does not saturate** while stronger models keep arriving.
- **Hard to game**: no reference answers to train on, which is why public comparative leaderboards earn more trust than most.
- **Complements** benchmarks offline and A/B tests online.

## Playbook: an internal comparative leaderboard

1. Build prompts from real traffic, stratified by use case; drop trivial and duplicate prompts; include your real context construction.
2. Route correctness-type prompts to exact checks instead of votes.
3. Use domain experts on a calibration subset and a validated AI judge (with order swapping) for scale.
4. Randomize position, hide identities, allow ties.
5. Warm up round-robin, then switch to uncertainty-driven matchmaking.
6. Fit Bradley-Terry; hold out about 20% of matches to check predictive accuracy; report per-pair match counts.
7. For the top contenders, measure absolute task metrics and cost per request before deciding.

## Worked example: is a 55% win rate worth double the cost?

Invented numbers. Current model resolves 72% of tickets at $0.010 each; a candidate wins 55% of comparisons at $0.020. On 1,000 historical tickets the candidate resolves 75%. Each unresolved ticket costs $4 of human time. Per 1,000 tickets: current $10 + 280 x $4 = $1,130; candidate $20 + 250 x $4 = $1,020, so switch. Had the candidate resolved only 72.2%, it would save $8 in human time against $10 of extra model cost. The win rate alone could not tell these cases apart.

## Glossary

- **Match**: one comparison between candidates with a recorded outcome.
- **Transitivity**: A beats B and B beats C implies A beats C; assumed by rating algorithms, not guaranteed.
- **Matchmaking**: the policy choosing which pair to compare next.
- **Display scale**: a cosmetic rescaling of ratings (for example Elo-like numbers from Bradley-Terry fits).
