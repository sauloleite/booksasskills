# Reuse Before Writing, and Using Quality Metrics Well

Covers: deciding whether new code is needed at all, judging "good" code, introducing analyzers to a legacy project, and using metrics without being misled by them.

## Contents
- The build-or-reuse ladder
- Challenging inherited practice
- Judging good code: smells plus tools
- Retrofitting analyzers onto an existing codebase
- Metrics as nudges (the observation effect)
- Metric pitfalls and how to contextualize
- Fast feedback in the editor
- Worked example
- Checklist

## The build-or-reuse ladder

Writing code is the most expensive way to solve a problem, because every line becomes something the team carries. Before writing, climb this ladder from cheapest to most costly and stop at the first rung that answers the need (adapt the rungs to your stack):

1. Does the current codebase already do this somewhere? Search before you type.
2. Does the language or its standard library cover it? Languages gain features every release; a few minutes of searching release notes can save hours.
3. Does the application framework already in use solve it (for a Spring shop, a Spring Boot starter; for a Python service, the web framework's built-ins)?
4. Do the general-purpose utility libraries the team already depends on solve it (Guava or Apache Commons in the JVM world; equivalents elsewhere)?
5. Is there any other library already on the dependency list that does it?
6. Is there a reputable open source library that does it?
7. Only after "no" on every rung: write it yourself, test-first or test-alongside.

Guardrails on rungs 4 to 6:
- Reuse is not a blank check to pile on dependencies. Inspect what the library drags in transitively, its maintenance health and its license.
- Follow the organization's approval process for third-party code.
- Prefer a dependency already present over a new one that overlaps it.

Agent behavior: when asked to implement a utility (date parsing, retries, string padding, CSV handling, HTTP clients), first report which rung could satisfy it and only generate custom code if none can, saying why.

## Challenging inherited practice

Practices age. Something that was sound a decade ago can be an anti-pattern now, and copying a pattern from the codebase, a blog post or an AI assistant without knowing why it exists is how stale habits spread. Keep asking "why is it done this way?" and periodically scan for new language and framework capabilities. Treat AI-generated code with the same skepticism: accept it only once you understand it.

## Judging good code: smells plus tools

"Good" is partly subjective, and experience builds an instinct for code smells. A smell is a prompt to look, not proof of a defect: a long method might genuinely have no simpler form. Combine instinct with objective signals:

- Cyclomatic complexity counts independent paths through code; higher counts point to code that is harder to test and a candidate for refactoring.
- Static analyzers (PMD, SonarQube, JSHint and peers) catch classes of bugs and bad practice automatically.
- Codebase-insight tools (SonarQube, CodeScene) show hotspots and trends across the whole system.

If the organization already has one of these, use it; if not, champion adopting one.

## Retrofitting analyzers onto an existing codebase

On a greenfield project, enable analysis from day one so code starts clean and stays clean, provided the team actually fixes what is flagged. On a project that is months or years old, never switch on every rule at once:
- Some rules conflict, so satisfying one breaks another.
- A flood of hundreds or thousands of warnings demoralizes people, hides newly introduced warnings in the noise, and makes cleanup effort invisible on the trend chart.

Instead, use a ratchet:
1. Agree as a team on a small set of rules everyone accepts (expect debate).
2. Enable only those; the warning count should be small enough to clear.
3. Fix them together until clean.
4. Enable a couple more rules and repeat.

After a few months the rule set is rich and the code is cleaner, and nobody had to stare at an unwinnable backlog.

## Metrics as nudges (the observation effect)

People change behavior when they know something is being watched (the Hawthorne effect). Use this deliberately: if you want more test coverage, make the coverage number highly visible, talk about it in standups and retros, praise every increase, and have teammates explain how they tested a tricky area. The author's story: a project with tests mostly disabled and coverage in single digits climbed to roughly 70% over several months just from publishing and celebrating the number. Visibility plus recognition is cheap and works.

## Metric pitfalls and how to contextualize

- Never follow a metric mechanically. Some complexity is essential, and forcing a rule of thumb can make code worse.
- Some metrics are actively harmful, such as judging engineers by lines added, removed or changed.
- Interpret every number in context. High coupling to a class usually suggests refactoring, but if that class is a facade deliberately hiding a subsystem, the coupling is the point.
- Measurable does not mean meaningful. Tie each metric to a project goal.
- Watch direction more than absolute value: is it improving or getting worse?
- Prefer short time horizons and be ready to change which metrics you track.

## Fast feedback in the editor

A pipeline gate is not the only option. IDEs and plug-ins report quality issues while you type, which is a much shorter feedback loop than a broken build. Ask whether the team shares a standard configuration and use it.

## Worked example

A team inherits a 300k-line service with no linter. Someone enables the full rule pack and gets 11,000 warnings; the team ignores the report within a week. Better path: the team votes on six rules (unused imports, empty catch blocks, missing braces on conditionals, and three others), gets 240 warnings, clears them in two sprints with a visible burn-down, then adds four more. Six months later the build fails on any new violation of 40 agreed rules.

## Checklist
- Did I check the codebase, language, framework, existing libraries and open source before writing?
- Did I vet any new dependency's transitive footprint and policy compliance?
- Can I explain why the pattern I am copying exists?
- Is each metric linked to a goal, read as a trend, and interpreted in context?
- When adding an analyzer to old code, did we start with a small agreed rule set?
