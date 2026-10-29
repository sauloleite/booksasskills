## Contents
- The pair programmer stance
- Category 1: standalone chatbots
- Category 2: inline IDE assistants
- Category 3: agentic IDE environments
- Worked example: agent adding a component
- Tool selection matrix
- Personal and team AI usage guidelines
- Pitfalls

# AI Coding Assistants and Usage Policy

## The pair programmer stance

Treat AI as a tireless colleague who is always available and never impatient with basic questions. The authors deliberately describe tools by category because specific products churn quickly while the categories stay stable. When advising, name the category first and mention products only as current examples.

Overriding principle: the developer flies the plane. AI amplifies thinking; it does not replace it. Responsibility for understanding, architecture and quality never moves to the tool.

## Category 1: standalone chatbots

Conversational assistants used outside the editor (current examples: ChatGPT, Gemini, Claude). Role: an on-demand mentor.

Best for:
- Grasping concepts and learning a new technology.
- Untangling difficult bugs through back-and-forth.
- Architecture and design discussions.
- Code generation where you want the reasoning explained too.

Practices:
- State the goal, not just the symptom.
- Paste the relevant code, error and versions.
- Tell it who you are (experience level) and what role to play.
- Ask for the explanation as well as the fix, so you learn.

A one-line question with no data types, language version or ordering is a weak prompt. A strong one names the element type, the sort key, the direction and the language version.

## Category 2: inline IDE assistants

Plug-ins or built-in features that complete code as you type (current examples: GitHub Copilot, JetBrains AI Assistant, Amazon CodeWhisperer, now folded into Amazon Q Developer).

Use for:
- Boilerplate such as accessors and constructors.
- Well-known patterns (builder, singleton and similar).
- Unit tests derived from existing code.
- Comments and doc blocks.
- Fast API and syntax hints.

Working rules:
- Read each suggestion before pressing accept.
- Treat completions as a starting point.
- Watch which local patterns the tool picks up; it will replicate bad ones too.
- Never let a completion silently change an architectural decision.
- Begin with trivial repetitive work, then move to more complex patterns as confidence grows.

Comprehension gate: for every accepted suggestion, the developer should be able to explain it in review. If not, research until they can. Accepting without understanding trades short-term speed for long-term skill loss.

## Category 3: agentic IDE environments

The newest category (examples at time of writing: Cursor, Junie, Cline). These tools act rather than suggest: they read the wider codebase, plan, and edit many files.

Good fits:
- Refactors spanning many files.
- Features that require coordinated edits in several layers.
- Migrations and modernization.
- Any task where broad project context matters.

Setup checklist before launching an agentic task:
- [ ] Specific functional requirements written down.
- [ ] Nonfunctional requirements stated: style guide, security standards, test strategy.
- [ ] Task sliced into pieces small enough to review in one sitting.
- [ ] Clean working tree on a branch so every AI change is tracked and revertible.
- [ ] Plan to read every diff before committing.

## Worked example: agent adding a component

Scenario (invented): an e-commerce admin app has four existing report modules (sales, refunds, inventory, traffic). You ask an agent for a new "abandoned carts" report.

What a well-behaved agent does, and what you should verify at each phase:

1. Analyze. It inspects the existing reports: the shared base type, the common lifecycle methods, how data is fetched through a service layer, naming and styling conventions. Verify: did it actually read the siblings, or invent a structure?
2. Plan. It states intentions: new report extending the base type, a new data service matching the existing service shape, same caching and refresh policy, registration in the report index. Verify: does the plan match your architecture? Correct it now; correcting a plan is cheaper than correcting code.
3. Implement. Only then does it write the report, the service, the registry entry and matching styles. Verify: tests, conventions, security (query safety, authorization on the new endpoint), and that no unrelated files changed.

The value of agentic tools is consistency with existing project patterns, not raw code volume. If an agent skips analysis and planning, ask it to stop and produce the plan first.

## Tool selection matrix

| Situation | Tool category | Why |
|---|---|---|
| "Why does this concurrency bug happen?" | Chatbot | needs dialogue and explanation |
| Writing accessors, mappers, doc comments | Inline | fast, local, low risk |
| Tests for a single existing class | Inline or chatbot | local context is enough |
| Rename a concept across 40 files | Agentic | needs whole-repo context |
| Upgrade framework major version | Agentic, in slices | multi-file, pattern-driven |
| Choosing between two architectures | Chatbot for options, human decides | trade-offs need business context |
| Learning a new language | Chatbot | ask for a study plan and explanations |

Rule of thumb: the wider the context a task needs and the more files it touches, the more you move from inline to agentic; the more understanding or judgment it needs, the more you move toward conversational use with a human decision.

## Personal and team AI usage guidelines

The chapter's practice section asks developers to write down their own rules. A useful template to fill in:

1. Where I use AI freely: boilerplate, scripts, doc drafts, test scaffolding, learning.
2. Where I use AI with extra scrutiny: security code (auth, crypto, input validation), money or tax calculations, concurrency, data migrations, code conversions, performance-critical paths, accessibility-sensitive UI.
3. Where I do not use AI, or only with approved tools: anything containing secrets, credentials, customer or personal data, proprietary algorithms, or code under restrictive licenses or contracts.
4. Data handling: which tools are company-approved, whether inputs are retained or used for training, how to redact before pasting.
5. Review rule: AI-assisted changes go through the same PR review, tests and CI as any change; the author can explain every line.
6. Traceability: AI work happens on branches with normal commits so it is auditable and revertible.

## Pitfalls

- Accept-and-move-on with inline completions.
- Handing an agent a vague, large task and committing the result wholesale.
- Letting the tool's habits drift the codebase away from agreed architecture.
- Pasting secrets or customer data into an unapproved chatbot.
- Choosing a tool by brand hype rather than by task shape.
