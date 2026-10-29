---
name: fse-theme-productivity-learning-ai
description: Theme skill on how engineers work faster, keep learning and use AI well, from Schutta and Vega's "Fundamentals of Software Engineering" (chapters 11, 12 and 15). Use when improving a development environment or command-line and keyboard fluency, deciding whether to automate a task, building learning habits and spaced review, evaluating or introducing new technology, choosing AI coding tools, writing prompts for code, reviewing AI-generated code, or setting personal AI usage rules.
---

# Productivity, learning and AI-assisted engineering (Fundamentals of Software Engineering, ch. 11, 12, 15)

Tools, learning and AI are multipliers: each amplifies skill that already exists. The theme is about investing in them deliberately rather than chasing them.

## Cross-chapter rules

1. **Own your toolkit.** Learn the IDE, version control and command line thoroughly, one feature at a time; customize, but timebox it.
2. **Automate what repeats.** Wait until a task has recurred a few times, timebox the build, and check payback with `scripts/automation_payback.py`; read and test any AI-written script.
3. **Learning needs spacing and depth choices.** Cramming fades; review at growing intervals (`scripts/spaced_review_schedule.py`), choose how deep to go per topic, and match guidance to skill level.
4. **Protect a learning cadence.** Small regular blocks, learning in public, an external notes system, and shared learning with the team.
5. **Be a critical consumer of technology.** Avoid resume-driven choices, keep a personal radar, recognize old ideas in new names, and introduce tools to a team in stages (briefing, workshop on real constraints, low-risk trial).
6. **You own all code you ship,** whoever or whatever generated it. Treat AI output as a first draft that passes the same tests and review.
7. **Pick the AI tool by task shape.** Chat for learning and design discussion, inline assistants for boilerplate and tests, agentic tools for multi-file work with a plan first.
8. **Prompt with context.** Role, environment, examples, constraints, output format and edge cases; iterate and keep prompts that work. Never paste secrets or proprietary data into unapproved tools.
9. **Review matters more now.** Scale rigor to the cost of a bug; vibe coding only for throwaway work.
10. **Pace yourself.** Steady, sustainable progress beats bursts.

## Default workflow

1. Remove friction in the environment and automate proven repeats (ch11).
2. Plan learning: depth per topic, cadence, review schedule, radar (ch12).
3. Adopt AI tools with a written personal policy, strong prompts and full review (ch15).

<!-- BEGIN GENERATED: run tools/build_bundles.py to refresh -->

## References by chapter

Each link is one level deep; read only the files whose description matches the task.

### CH11: Powering Up Your Productivity

- [ch11-command-line-and-keyboard.md](references/ch11-command-line-and-keyboard.md): read when teaching shell composition, aliases, history and fuzzy finding, alternative shells, touch typing, shortcut layers, Emacs/vi bindings, clipboard managers or text expanders.
- [ch11-environment-and-ergonomics.md](references/ch11-environment-and-ergonomics.md): read when tuning an IDE, OS or physical workspace, choosing fonts/themes/keyboards, handling Git safety basics, or warning about customization time sinks.
- [ch11-learning-habits-and-knowledge.md](references/ch11-learning-habits-and-knowledge.md): read when building learning cadence, team knowledge sharing, keeping up with language releases, setting up personal knowledge management, or planning practice exercises and further reading.
- [ch11-strategic-automation.md](references/ch11-strategic-automation.md): read when deciding whether and how far to automate a task, including the decision procedure, worked example and pitfalls.

### CH12: Learning to Learn

- [ch12-evaluating-new-technology.md](references/ch12-evaluating-new-technology.md): read when someone feels FOMO, wants to adopt a hyped tool, or needs a method to judge staying power (resume-driven development, pendulum patterns, radars, network sharding).
- [ch12-how-learning-works.md](references/ch12-how-learning-works.md): read when explaining why cramming fails, designing retention (stories, spacing), helping someone who is stuck, or tailoring guidance to Shu Ha Ri or Dreyfus stage.
- [ch12-introducing-technology-to-teams.md](references/ch12-introducing-technology-to-teams.md): read when spreading knowledge or proposing a technology inside an organization: book clubs, hack days, showcases, talks, internal conferences, architectural briefings, workshops, legacy constraints, trial projects.
- [ch12-learning-habit-and-cadence.md](references/ch12-learning-habit-and-cadence.md): read when building a personal learning plan: depth levels, weekly/monthly/yearly cadence, calendar blocks, learning out loud, AI-assisted study, avoiding burnout, practice projects.

### CH15: The AI-Powered Software Engineer

- [ch15-ai-coding-assistants-and-usage-policy.md](references/ch15-ai-coding-assistants-and-usage-policy.md): read when choosing between chatbot, inline and agentic tools, setting up an agentic task, or writing personal or team AI usage guidelines.
- [ch15-ai-concepts-capabilities-limits.md](references/ch15-ai-concepts-capabilities-limits.md): read when explaining AI, ML, deep learning, GenAI or LLM concepts, picking a temperature, or deciding whether a task suits AI given its strengths and its known limitations.
- [ch15-prompt-engineering-playbook.md](references/ch15-prompt-engineering-playbook.md): read when writing, critiquing or rewriting a prompt, or choosing zero/one/few-shot, delimited structure or task decomposition.
- [ch15-reviewing-ai-code-and-career-shift.md](references/ch15-reviewing-ai-code-and-career-shift.md): read when reviewing AI-generated code, judging whether vibe coding is acceptable, addressing job-loss worries, reframing productivity, or planning practice exercises.

Merged section maps: [source-maps.md](references/source-maps.md).

## Scripts

Python 3 standard library only; run any script with `--help` for its arguments.

| Script | Purpose |
|---|---|
| `scripts/automation_payback.py` (ch11) | Automation payback calculator (Strategic Automation, FSE Chapter 11). |
| `scripts/spaced_review_schedule.py` (ch12) | Spaced-repetition review scheduler for things you are learning. |

<!-- END GENERATED -->
