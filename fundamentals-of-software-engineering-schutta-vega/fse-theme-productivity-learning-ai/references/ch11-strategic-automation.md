# Strategic Automation

Covers: Strategic Automation (including the time-sink warning).

## The principle

Developers spend their days writing software for others; they should also write small programs for themselves. A short helper script (dozens of lines, not hundreds) can return hours. Side benefit: personal tooling is a low-stakes place to practice a new language, regex, or technique.

## The "zero, one, n" heuristic

Borrowed from computer science folklore: things happen zero times, once, or an unbounded number of times. Practical reading: a task done a second time is likely to recur indefinitely, so repetition is the signal to consider automating.

## The counterweight: automation can be a time sink

The chapter immediately qualifies the heuristic:
- Building the automation can take longer than doing the task by hand.
- Genuine one-offs should not be automated.
- Prefer to wait until the task has been done a few times by hand (which also clarifies what exactly to automate).
- Even then, timebox the effort and apply judgment.

## Decision procedure

1. Has this been done manually more than once, and will it recur? If no, do it by hand.
2. Estimate: manual minutes per run, runs per month, expected remaining lifetime of the task.
3. Estimate build time plus ongoing maintenance.
4. If cumulative time saved over the horizon clearly exceeds build plus maintenance, automate; otherwise keep doing it manually, or write a checklist instead.
5. Set a timebox equal to (or below) the break-even build time. Stop when it expires and reassess.
6. Non-time benefits can justify automation even near break-even: fewer errors, consistency, handing the task to teammates, learning value. State them explicitly instead of letting them inflate the estimate silently.

The bundled script `scripts/automation_payback.py` performs steps 2 to 5.

## AI-written helpers

The cost of writing helper scripts has dropped because an AI assistant can draft them. Requirement that does not change: read and test generated code before trusting it, especially anything that deletes, moves or pushes.

## Evolving automations

Once a small script works, consider extending it to cover a larger chunk of the workflow, and share it with the team so the payback multiplies across people.

## Worked example (invented)

A developer spends 6 minutes each morning pulling three repos, starting containers and seeding a local database, about 20 workdays per month. Over 12 months that is 6 x 20 x 12 = 1,440 minutes (24 hours). A script would take an estimated 3 hours to write and 15 minutes per month to maintain (3 hours per year), and still needs 30 seconds per run. Remaining manual time: 0.5 x 240 = 120 minutes (2 hours). Net saving: 24 - 2 - 3 - 3 = 16 hours. Monthly net saving is 120 - 10 - 15 = 95 minutes, so the 180-minute build pays back in about 1.9 months. Verdict: automate, with a timebox of about 3 hours for the first version. Contrast: a one-time data migration taking 40 minutes by hand that would need 3 hours to script is better done manually unless correctness risk justifies the script.

## Pitfalls

- Automating something done once.
- Polishing a personal script well past its payback.
- Ignoring maintenance (APIs change, paths move).
- Running AI-generated scripts unread.
- Keeping useful automations private when teammates face the same toil.
