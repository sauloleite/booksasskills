## Contents
- Will AI take my job? The argument
- Vibe coding: definition and limits
- Stakes-based rigor rubric
- How AI-assisted code works in serious organizations
- Why review matters more now
- Review checklist for AI-generated code
- The creator-and-curator mindset
- Force multiplier: the time flip
- Reframing productivity
- Practice plan
- Further reading

# Reviewing AI Code and the Career Shift

## Will AI take my job? The argument

Use this reasoning when a developer is worried:

1. Engineering is mostly not typing. Developers read far more code than they write, and comprehension is needed whether a human or a model wrote it.
2. The job includes turning vague, incomplete requirements into working systems, making context-dependent trade-offs (performance vs maintainability), mentoring, navigating organizational politics, and explaining technical matters to nontechnical people.
3. Models lack the company's business model, the users' real needs, and the room: they cannot notice in a meeting that product's requirements contradict what sales promised, or that an executive's "small ask" implies a redesign. These human parts are the core of the work, not exceptions.
4. History: assembly to high-level languages, plain editors to IDEs, manual releases to CI/CD. Each was predicted to shrink demand; demand kept growing.
5. Conclusion: some roles will be reshaped and some jobs may go, but wholesale replacement is not near. The real risk is being the developer who refuses the tool. A widely repeated saying, often attributed to Jeff Atwood, puts it as developers using AI displacing those who do not.

What stays valuable is not reciting a loop or a sorting algorithm on demand but knowing when each applies, why, and how it fits the larger system. Soft skills (collaboration, empathy, mentoring) become more of a differentiator as code generation gets cheap.

## Vibe coding: definition and limits

Term coined by Andrej Karpathy in February 2025, half joking, describing building whole applications by prompting agentic tools and accepting what comes out, with little reading of the code. The authors stress the term was meant to poke fun at a risky practice, not recommend it.

The upside is real: non-programmers (a restaurant owner wanting an ordering page, a teacher making a quiz, an artist building a portfolio) can now prototype ideas without hiring developers or spending years learning.

The limit: it suits disposable weekend projects. The operative word is disposable.

## Stakes-based rigor rubric

| Stakes | Example (invented) | Acceptable approach |
|---|---|---|
| Throwaway, only you affected | a script to rename your holiday photos | prompt-driven generation, light checking |
| Personal tool with mild consequences | a hobby budget tracker | generate, read the core logic, a few tests |
| Shared internal tool | team on-call rota bot | normal PR review, tests, owner named |
| Customer-facing or regulated | billing, payroll across tax jurisdictions, medical scheduling | full engineering process: specs, review, test suite, staged rollout, audit trail |

Ask: if this has a bug, who is harmed and how badly? A mis-tagged coffee expense is trivial; employees paid wrongly or taxes misfiled means legal exposure.

## How AI-assisted code works in serious organizations

Headlines that a quarter of a big company's code is AI-written do not describe casual prompting. The realistic flow, as demonstrated publicly by large vendors such as Microsoft:

1. A human writes a detailed issue stating the problem.
2. A coding agent reads the issue, makes the changes and opens a pull request.
3. One or more humans review and decide whether to merge.

AI does routine implementation; humans keep quality assurance and the decision. The difference from weekend hacking is process: code review, test frameworks, deployment pipelines, QA. Those gates apply to AI code exactly as to human code, and they matter more now, not less.

## Why review matters more now

- Faster generation does not shrink timelines proportionally, and it carries hidden costs.
- Generated code can hide subtle bugs, security holes and poor architectural fits, just like human code.
- Neal Ford has warned of a coming flood of low-quality code from teams adopting AI output without real review.
- Choose where you find problems: during review, or during an on-call page on a weekend.
- As author, own the code: before opening a PR, walk through it until you can justify every line. As reviewer, give the same attention to detail regardless of who or what authored it.

## Review checklist for AI-generated code

Run this as if a junior colleague had submitted the change:

- [ ] Can the author explain each line and why it exists?
- [ ] Does it solve the stated problem, including edge cases (null, empty, huge, concurrent)?
- [ ] Are there invented APIs, wrong library versions or deprecated calls?
- [ ] Security: input validation, injection, authz checks, secrets, unsafe defaults, dependency choices.
- [ ] Architecture: does it follow the project's layering, patterns and naming, or introduce a parallel style?
- [ ] Tests: present, meaningful (not just restating the implementation), covering failure paths.
- [ ] Bias and inclusivity: assumptions about names, locales, genders, abilities; accessibility of UI output.
- [ ] Converted code: semantics preserved (integer division, null handling, encoding, error model), and idiomatic in the target language.
- [ ] Performance and failure behavior under realistic load.
- [ ] Is the change scoped, or did the tool touch unrelated files?

## The creator-and-curator mindset

Avoid the prompt-and-pray habit. Be both producer and curator of code: use AI deliberately while holding standards high. Skills to build:

- Writing prompts that yield better code.
- Reading and understanding generated code quickly.
- Spotting defects in both human and AI code.
- Detecting bias and exclusionary assumptions.
- Communicating clearly in reviews.

The obligation to ship reliable, maintainable software does not change with the tool.

## Force multiplier: the time flip

A force multiplier amplifies existing skill but cannot create it. An expert photographer with a phone usually beats a novice with an expensive camera, because composition, light and exposure knowledge live in the person. Likewise AI does not turn someone into an engineer; knowledge and problem-solving do.

The authors' illustrative split: traditionally about 70% of time goes to boilerplate, syntax debugging and repetitive patterns, leaving 30% for creative problem-solving and everything else. AI can invert that, so roughly 70% goes to requirements analysis, architecture and hard business problems. The intended result is not necessarily more output but better-considered releases with fewer bugs and missed edge cases. Treat the percentages as a framing, not a measurement.

Applying the flip, using building an API as the example: with a house template and good prompts, the scaffolding (models, validation, handlers, persistence) takes minutes. Reinvest the time in questions such as:

- Is the API intuitive for its consumers?
- How will it behave at high throughput?
- Are we using the platform's concurrency features well?
- Does it scale and degrade gracefully under load?

Working correctly comes first; these questions are where engineering time should then go.

## Reframing productivity

Lines of code is a poor measure of value; nobody is impressed by a line count on a resume. Express accomplishments as impact, for example a measurable cloud cost reduction from an architecture change, or latency or incident reductions. When coaching a developer who fears writing less code, redirect them to outcomes. The shift from writing to problem-solving raises the role rather than shrinking it.

## Practice plan

Exercises an agent can propose, adapted from the chapter's intent:

1. Pick a method you know well, ask an assistant to explain it, propose improvements and list tests, then compare against your own reading. Note where it was wrong.
2. Write three carefully structured prompts for debugging, review and documentation, using context, environment, role, format and decomposition.
3. Start a prompt library of 5 to 10 reusable prompts.
4. Use one assistant for a week on a side project and log where it helped and where it failed.
5. Have AI write a small class, then review it rigorously as if from a junior; record findings.
6. Convert a small program between two languages with AI and verify correctness and idiom by hand.
7. Draft your AI usage rules: when you will use it, what gets extra scrutiny, how sensitive data is handled.

## Further reading

Titles the chapter points to, among others: Chip Huyen, AI Engineering; Addy Osmani, Beyond Vibe Coding; Berryman and Ziegler, Prompt Engineering for LLMs; Fred Brooks, "No Silver Bullet"; Ethan Mollick, Co-Intelligence; Russell and Norvig, Artificial Intelligence: A Modern Approach; Simon Willison's blog.
