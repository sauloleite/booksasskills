# Usability Qualities and How to Prioritize Them

## Framing

- The interface is what users experience as "the product". UX defines the goals; UI is the concrete realization that has to serve them.
- Usability reduces to one test: how easily can the people this product is actually for get their work done with it?
- Usability tends to be the first casualty of schedule pressure, and engineers often assume it belongs to designers or specialists. Treat that as a myth: an engineer with basic principles can avoid most damage.
- Bolting usability, accessibility or translation onto a mature product is far more expensive than designing for them up front. The authors recount a retrofit where a screen-reader walkthrough revealed unlabeled fields and almost no keyboard path; it took a large effort to reach "mostly usable".

## The seven quality components (audit questions)

| Component | Ask |
|---|---|
| Learnability | How long until a newcomer is productive? Does it serve novices and experts? Can scaffolding be switched on and off as users grow? Is contextual help easy to reach? |
| Efficiency | How many clicks, screens or keystrokes does a routine task cost? |
| Memorability | After weeks away, can a user resume without relearning? |
| Discoverability | Can users find what the product can do, especially the core functions? |
| Error handling | Does it prevent mistakes (hints, validation, masks, cues), tolerate omissions, and protect data when something fails? |
| User satisfaction | Do users leave content or resentful? |
| Accessibility | Does it work with assistive technology and for different abilities? |

## Prioritization: context decides

Do not try to max out all seven. Start from how, how often, and by whom the product is used.

Decision rules:

1. Heavy daily use or inherently complex tools (CAD, trading desks, call-center consoles): weight efficiency, memorability and satisfaction. Users get training or learn by repetition, so some less discoverable power features are acceptable.
2. Casual, optional, consumer products with many alternatives: weight learnability and discoverability. Users will not invest time; if it is not intuitive they leave.
3. Rarely used tools (annual filings, occasional admin tasks): learnability and discoverability are vital; memorability matters little because users effectively start fresh each time. Accept a slightly slower flow if it makes the path obvious.
4. Throughput-measured work (tasks per hour): efficiency has direct business value. Small per-task savings multiply across many repetitions and many users.
5. Deliberately hard experiences (puzzle games): low discoverability can be the point. Context is the guide, not a universal rule.
6. Training never excuses a poor interface; training budgets are cut as readily as usability work.

### Worked example: the multiplier

A claims-processing screen is used by 300 agents, each handling 80 claims a day. Removing two clicks saves about 3 seconds per claim:

- 3 s x 80 x 300 = 72,000 s, or 20 hours of staff time every working day.
- Over about 230 working days that is roughly 4,600 hours a year.

Use this arithmetic when arguing for efficiency work on internal tools.

### Interplay of qualities

- Discoverability feeds memorability: an obvious path is also easier to recall later. When unsure, choose the more obvious design.
- Frequent use makes almost anything memorable, which is why daily tools can afford a few hard-to-learn interactions.
- Efficiency features (keyboard shortcuts) help experts but are hard to remember; pair them with discoverability aids (see the discoverability reference).

## Pitfalls

- "Our users have no choice" (internal or mandated software). A captive audience still pays the cost in time, errors and morale, and secondary users (customers waiting on the operator) feel it too.
- Assuming competition is the only reason to care about satisfaction. In open markets users simply migrate to the easier product.
- Measuring usability only by appearance. Polish without ease of use fails the test above.
