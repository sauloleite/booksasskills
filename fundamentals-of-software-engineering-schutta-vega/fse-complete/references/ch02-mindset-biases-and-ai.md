# Mindset, Biases, AI, and Deliberate Practice

## Contents
- Why reading comes first
- Brownfield reality and the "legacy" label
- The four problems hidden in every change
- Dating the code and patch-on-patch decay
- Cognitive biases that distort judgment
- Using AI to read code
- Patience and incremental understanding
- Practice plan
- Further reading
- Glossary

## Why reading comes first

Most courses teach writing code first, the way no one would learn a human language: speaking before ever listening or reading. In practice, an engineer reads far more code than they produce, and chat-driven or agentic generation makes this ratio even more lopsided because generated code still has to be understood, reviewed, and maintained. An agent coaching a developer should treat code reading as a core, trainable skill, not a chore to minimize.

## Brownfield reality and the "legacy" label

- Greenfield work (empty repository, no prior constraints) is rare in a career. Brownfield work inside a long-lived codebase is the norm.
- "Legacy" is used loosely: code from yesterday, code with too few (or too many) tests, or simply code the speaker did not write. It usually carries contempt.
- Reframe: a system that has delivered value long enough to keep receiving funding is a business success. Calling it "existing" or "heritage" code keeps the conversation about improvement instead of blame.
- Agent behavior: when a user vents about an old codebase, acknowledge the difficulty, then steer toward what the code is achieving and what it would take to make the next change safe.

## The four problems hidden in every change

When asked to change existing code, separate these explicitly:

| # | Problem | Diagnostic question | Typical move |
|---|---------|--------------------|--------------|
| 1 | Business problem | Do we understand what the domain actually requires? | Talk to product owners, read stories and ADRs, write the requirement as a test. |
| 2 | Predecessor's perspective | Why did the author solve it this way (style, pattern, library)? | Learn the unfamiliar paradigm or library before judging; many valid solutions exist. |
| 3 | Abstraction fit | Is the model too generic, missing domain nuance, merging two concepts, or forcing a pet pattern? | Plan a larger refactoring, ideally behind tests. |
| 4 | Accumulated layers | Which parts reflect practices that are now considered anti-patterns? | Read each layer in its historical context; modernize incrementally. |

The second problem is often the hardest: reconstructing another person's reasoning. A predecessor might favor a functional style, a design pattern, or a library the reader has never used. Disagreeing with the choice does not make it wrong.

## Dating the code and patch-on-patch decay

- Like an archaeologist reading strata, estimate a file's age from what it uses and what it lacks: framework idioms, configuration style, language features. Mature frameworks often support several ways of doing the same thing across versions, so the "correct" way shifts over time.
- Expect fixes stacked on fixes. Causes include partial understanding of the problem, unawareness of a newer language feature, deadline pressure, and, increasingly, large volumes of AI-generated code nobody fully reviewed. A single method can absorb an afternoon of analysis.
- Practical consequence: estimate brownfield tasks with time for archaeology, not just for typing.

## Cognitive biases that distort judgment

Reading your own old code and wincing is healthy: it means you have grown since you wrote it. Beyond that, three biases skew how developers judge code and tools:

- **IKEA effect.** People overvalue what they built themselves. A Harvard Business School working paper by Norton, Mochon, and Ariely found participants willing to pay substantially more (63% in one study) for items they assembled. In software it shows up as "my approach is the right one."
- **Mere-exposure effect.** Familiarity breeds preference. Developers often treat the first language they learned as the baseline of all programming and resist ideas that are new to them but old in the field (for example, someone objecting to lambdas being added to Java, unaware they predate the language and were part of its original plans).
- **Blub paradox** (Paul Graham, "Beating the Averages"). Languages sit on a power continuum. Looking down, a programmer sees languages missing features they rely on and calls them inferior. Looking up, they see unfamiliar features and cannot imagine needing them. Their own language feels "just right."

Agent checklist when a design debate stalls:
1. Is anyone defending code mainly because they wrote it?
2. Is the objection to a technique really unfamiliarity?
3. Is a tool being dismissed because its benefits are invisible from within the current language or stack?
4. Apply the same three questions to your own recommendation.

## Using AI to read code

- Tooling has steadily made writing code easier, while applications have grown proportionally larger and more complex. Predictions that developers will be replaced (COBOL, 4GLs, drag-and-drop builders, now LLMs) have repeatedly failed to reduce demand for engineering.
- Appropriate use: ask an assistant to summarize what a snippet does, explain an unfamiliar idiom, or suggest where to look next.
- Limits: the model does not know why a class exists in this business, cannot see relationships across many repositories and libraries, and may hallucinate. Plausible explanations must still be checked against tests, a debugger, documentation, and teammates.
- Roles: the human remains in command and sets context; the AI accelerates once the human understands the system well enough to direct and check it.
- Policy: before pasting proprietary code (pricing logic, credentials, customer data) into an external model, confirm what the organization allows and whether the provider retains or trains on inputs.

Agent behavior: when the agent itself explains code, label which claims are verified (read in code, seen in a test, observed at runtime) and which are inferred, and suggest a quick verification for each inference.

## Patience and incremental understanding

Large systems exceed what any one person can hold in their head, and that is not the target. Understanding grows each time the developer repeats the orientation loop on a new area. Encourage self-compassion: everyone finds a new codebase intimidating at first, and speed improves with repetition. Close every engagement by leaving the code a little clearer for the next reader, who may well be the same developer months later.

## Practice plan

An agent can propose a concrete regimen:

1. **Weekly reading block.** Reserve about two hours to read part of a framework the developer uses daily (or wants to use). Pick one feature and trace it with the techniques from the other references.
2. **Discovery list.** If unsure where to start, browse popular or trending open source repositories and choose one with good tests and docs.
3. **Spaced revisit.** After roughly two months, explore another module of the same project or a different project, then compare: what felt faster, which techniques paid off.
4. **Contribute.** Pick an issue tagged for newcomers in an open source project, or ask maintainers for a starter task. Making a small change end to end trains the full brownfield skill, not just reading.
5. **Reflect.** Keep a short log: what slowed you down (domain, style, abstraction, history) and which tool resolved it.

## Further reading

Titles the chapter recommends:
- Jack W. Reeves, "Code as Design: Three Essays"
- Trisha Gee, "Reading Code Is Harder Than Writing It"
- Patricia Aas, "Reading Other People's Code"
- Alex Coleman, "How to Quickly and Effectively Read Other People's Code"
- Sunny Beatteay's article on reading code without losing your sanity

## Glossary

- **Brownfield:** work within an existing system and its constraints.
- **Heritage code:** a respectful synonym for long-lived production code.
- **Carbon dating code:** estimating age from the technologies and idioms present.
- **Power continuum:** Graham's ordering of languages by expressive power, the basis of the Blub paradox.
