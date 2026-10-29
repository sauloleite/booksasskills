---
name: fse-ch11-powering-up-productivity
description: Guidance for raising a developer's day-to-day productivity: owning and customizing the IDE, OS and physical setup, command-line and keyboard fluency, timeboxed strategic automation with a payback check, steady habit building, learning from teammates, and personal knowledge management. Based on Chapter 11 of Schutta and Vega's "Fundamentals of Software Engineering". Use when a developer asks how to work faster, set up or tune their environment, learn shortcuts or the shell, decide whether to script a repetitive task, or organize notes and ongoing learning.
---

# Powering Up Productivity (FSE Chapter 11)

Purpose: help a developer stop being a passive tool user and become someone who owns, tunes and keeps improving their toolkit. The aim is staying in flow (deep, uninterrupted concentration) by removing friction: unfamiliar commands, mouse trips, repetitive toil and lost knowledge. The chapter's emphasis is on being productive rather than merely busy, and on small, sustained gains rather than heroic overhauls.

## Key decision rules

Apply these even without opening the references.

1. Own the toolkit. Employers may pay for licenses, but the engineer is responsible for tool fluency. Know daily-use features cold; look up the rest.
2. Learn the editor and source control on purpose. One new IDE feature per week (use tip-of-the-day style aids). Understand what history-rewriting Git commands do to shared branches before running them; a careless force push to main can destroy weeks of team work.
3. Customize, but timebox it. Defaults rarely fit; trial fonts, themes, OS settings and utilities for a day or two each. Stop when tinkering displaces real work.
4. Stay pairable. Do not customize so far that nobody else can work at your machine; teams may agree on a shared tooling baseline.
5. Fix the physical setup early. Neutral posture (chair, monitor height), sit/stand alternation, eye breaks and screen-aware eyewear, and a better keyboard before strain injuries appear. Ask the employer or ergonomics team to pay or assess.
6. Become fluent at the CLI. Compose small tools with pipes, learn a bit of regex, read `man` pages, try modern replacements (bat, diff-so-fancy, fx, eza).
7. Alias wisely. Only frequent or long commands, and keep knowing the full command for machines without your config.
8. Exploit shell history: Ctrl-R, larger history, ignore rules, a fuzzy finder.
9. Keyboard first. Touch typing is expected; learn editor, OS and Emacs-style text navigation shortcuts. Learn enough vi to survive on a bare server. Avoid editor-war arguments.
10. Use clipboard history and text expanders, but keep secrets out of clipboard history.
11. Automate what repeats ("zero, one, n": a second occurrence predicts many more). Counterweight: skip true one-offs, wait until a task has been done by hand a few times, timebox the build, and check payback. AI may draft the helper script, but it must be read and tested.
12. Improve continuously and slowly: one new shortcut, command or tool feature per week beats a cram session.
13. Learn socially. Ask about unfamiliar tools you see; show faster ways and have the person repeat them a few times; teach while pairing; run lunch-and-learns; still attend sessions on tools you know.
14. Track language evolution: read release notes, try new features, teach them (see one, do one, teach one).
15. Keep an external brain. Write down every fix and new command; any system works if it is searchable enough, portable to mobile, and actually used. Simple beats elaborate.

## Default workflow

When a developer asks for productivity help:
1. Diagnose friction: what do they repeat, what makes them reach for the mouse, what do they keep re-searching, what hurts physically?
2. Pick at most two or three changes for this week (one shortcut, one CLI habit, one setup fix). Avoid overload.
3. For repetitive tasks, run the payback script before writing automation; set a timebox from its output.
4. Make them record each new item in their notes system; if they have none, propose the simplest viable one.
5. Suggest a weekly 15-minute review slot and a way to share discoveries with the team.
6. Flag risks: over-customization that blocks pairing, unreadable aliases, secrets in clipboard history, unreviewed AI-generated scripts, risky Git commands.

## References

- [references/environment-and-ergonomics.md](references/environment-and-ergonomics.md): read when tuning an IDE, OS or physical workspace, choosing fonts/themes/keyboards, handling Git safety basics, or warning about customization time sinks.
- [references/command-line-and-keyboard.md](references/command-line-and-keyboard.md): read when teaching shell composition, aliases, history and fuzzy finding, alternative shells, touch typing, shortcut layers, Emacs/vi bindings, clipboard managers or text expanders.
- [references/strategic-automation.md](references/strategic-automation.md): read when deciding whether and how far to automate a task, including the decision procedure, worked example and pitfalls.
- [references/learning-habits-and-knowledge.md](references/learning-habits-and-knowledge.md): read when building learning cadence, team knowledge sharing, keeping up with language releases, setting up personal knowledge management, or planning practice exercises and further reading.
- [references/source-map.md](references/source-map.md): read to find which file covers a given chapter section.

## Scripts

- `scripts/automation_payback.py`: Run it to compute whether automating a recurring task pays back over a horizon, the break-even month, the maximum build time worth spending (use it as the timebox), and a verdict (AUTOMATE, WAIT, MARGINAL, MANUAL).

```sh
python3 scripts/automation_payback.py --manual-min 6 --runs-per-month 20 --months 12 \
  --build-hours 3 --maint-min 15 --residual-min 0.5 --times-done 5
python3 scripts/automation_payback.py --help   # all options; add --json for machine output
```
