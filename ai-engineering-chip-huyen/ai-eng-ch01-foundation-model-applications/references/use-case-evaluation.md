# Use-Case Evaluation: Whether, Why, and How Much Autonomy

Covers the first planning decisions: the motivation for building, buy versus build, the role AI plays in the product, the role humans keep, staged autonomy, and defensibility of standalone AI products. Use it when someone asks "should we build this?", "should we buy instead?", "how much should the AI do on its own?" or "can a big player copy us?".

## Contents
- Learn mode vs business mode
- Step 1: classify the motivation
- Step 2: buy or build
- Step 3: the role of AI in the product
- Step 4: the role of humans
- Step 5: defensibility (standalone products only)
- Decision record template
- Worked examples
- Pitfalls

## Learn mode vs business mode

For learning or fun, skip formal planning and build; building teaches best, and many AI leaders let teams experiment early to upskill. For a business bet, ask why and how first: a striking demo is cheap, a profitable product is not.

## Step 1: classify the motivation

Rank from highest to lowest stakes:

| Level | Situation | Typical sectors or signals | Implication |
|---|---|---|---|
| 1. Existential | AI-using competitors could make you obsolete | Document processing and aggregation (financial analysis, insurance, data processing); creative work (advertising, web design, imagery) | Top priority; keep core capability in-house rather than with a vendor who may compete |
| 2. Opportunity | Missing profit or productivity gains | Cheaper acquisition via better copy and visuals, retention via support and personalization, lead generation, internal comms, market and competitor research | The common case; survey buy options first |
| 3. Exploratory | Unsure where AI fits, unwilling to fall behind | Cautionary tales of firms that waited too long on a transformative shift | Fine if affordable (an R&D function at large firms); small startups usually cannot spare anyone to "look around" |

Avoid both chasing every hype wave and waiting until disruption arrives. Use industry exposure rankings to test whether a level-1 claim is credible.

## Step 2: buy or build

- Existential threat: lean toward building in-house.
- Profit or productivity: there are often vendor options that save time and money and perform better than a first in-house attempt; default to evaluating those first.
- Keep revisiting: this choice can flip as prices and capabilities change (see maintenance planning).

## Step 3: the role of AI in the product

Classify along three axes (popularized by Apple's guidance on AI in products); each sets requirements.

**Critical vs complementary.** Would the app still work without the AI? Face unlock would not (critical); an email client without autocomplete would (complementary). The more critical, the higher the accuracy and reliability bar; users forgive more when AI is not core.

**Reactive vs proactive.** A chatbot answers when asked; a traffic alert appears on its own. Reactive features usually, not always, need speed because someone is waiting. Proactive ones can be precomputed, so latency matters less, but because nobody asked for them low quality feels intrusive: set a higher quality bar.

**Dynamic vs static.** Face recognition must track a changing face (dynamic); photo object detection is likely refreshed only with app releases (static). Dynamic in foundation-model terms means per-user models continually finetuned on user data, or lighter personalization such as a memory of user preferences; it implies feedback pipelines, per-user state and privacy handling. Static means one shared model updated periodically.

Combinations: critical plus reactive carries the strictest accuracy and latency needs; complementary plus proactive relaxes latency but should stay silent unless confidence is high; complementary, reactive and static is the cheapest place to start.

## Step 4: the role of humans

Decide whether AI supports humans, decides directly, or both. For a support bot: (1) AI drafts several replies agents can use, (2) AI handles simple requests and routes complex ones to humans, (3) AI handles everything. Involving people in AI decisions is human-in-the-loop.

**Crawl-Walk-Run (Microsoft, 2023):** Crawl, human involvement mandatory; Walk, AI interacts directly with internal employees; Run, more automation, possibly direct AI contact with external users.

**Promote on evidence, per request class.** Example: if agents send AI drafts for simple requests unchanged about 95% of the time, let customers talk to the AI directly for that class. Write promotion criteria up front: verbatim acceptance rate, degree of edits otherwise, post-promotion escalation and complaint rates, and a rollback trigger.

## Step 5: defensibility (standalone products only)

Relevant when the app is sold as a product. The low barrier cuts both ways: what is easy for you is easy for rivals (hence the "thin wrapper" jibe).

**Three moats.** Technology is weak because most firms share similar models. Distribution (reaching users) usually favors incumbents. Data is the nuanced one: incumbents start with more, but a startup first to market that gathers enough usage data to keep improving can make data its moat. Even when usage data cannot train models (privacy, contracts), it reveals behavior and product gaps that steer data collection and training. When founders cite a "data flywheel", ask what concretely turns.

**Subsumption test.** Your product is a layer over a model; if the model gains the capability your layer supplies, the layer vanishes. Example: a PDF parser that exists because today's chat model handles PDFs poorly or not at scale. Ask which model weakness you compensate for and what happens when it is fixed. Mitigation: serve a segment the provider will not, such as organizations that must self-host open models.

**Feature test.** Could a platform giant replicate this with three engineers in two weeks? Not automatically fatal: several well-known companies began as a missing feature of a larger product (scheduling vs a calendar, email marketing vs a mail client, background removal vs a photo library) and grew from an overlooked niche. The question is whether you can outgrow the wedge before the incumbent notices.

## Decision record template

```
Use case:
Mode: learning | business
Motivation level: existential | opportunity | exploratory
Buy options reviewed: [list] -> decision: buy | build | hybrid, because ...
AI role: critical|complementary, reactive|proactive, dynamic|static
  -> implied bars: accuracy ..., latency ..., quality ...
Human role: drafts | route simple | full automation
  Crawl-Walk-Run stage: ...
  Promotion criteria per request class: ...
Defensibility (if selling): tech ..., data flywheel ..., distribution ...
  Subsumption risk: ...   Feature risk: ...
Revisit date:
```

## Worked examples

**Regional bank, loan-document intake.** Competitors automate document processing, so this is existential: build core extraction in-house. AI role: critical, reactive, static. Start at Crawl with every extracted field reviewed; promote per document type once reviewers accept fields unchanged at a pre-agreed high rate.

**Startup selling "chat with your spreadsheets".** Fails the feature test (a spreadsheet vendor could ship it) and carries high subsumption risk (models keep improving at tables). Options: target regulated customers who self-host open models, or specialize in a vertical whose proprietary usage data compounds.

**Proactive alerting.** A team wants AI to push unprompted "insights" to managers. Raise the quality bar: precompute, rank, and surface only items above a strict threshold, accepting fewer alerts.

## Pitfalls

- Treating a demo as proof of business value.
- Building in-house for a non-core gain when good vendors exist, or outsourcing an existential capability to a potential competitor.
- Giving proactive features the same quality bar as reactive ones.
- Jumping to full automation, or promoting the whole system at once instead of per request class.
- Claiming a data moat without a mechanism that feeds usage back into improvement.
- Building a business on a model weakness the next release removes.
