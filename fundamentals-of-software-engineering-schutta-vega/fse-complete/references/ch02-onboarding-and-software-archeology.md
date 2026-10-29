# Onboarding and Software Archeology

## Contents
- Orientation order
- Lightweight documentation while learning
- Pitfall: trusting a metric over the practice
- Software archeology: structure survey
- Tracing from a landmark
- Worked example (invented)
- Verify what names and exceptions claim
- Tool-assisted analysis
- Version-control history
- Generated diagrams
- Checklist

## Orientation order

Gather the cheapest, highest-context information first:

1. **People.** Ask teammates for a project overview; a decent onboarding should include one. Ask who owns which area.
2. **Written overviews.** README, wiki, project website. Read them, but assume parts may be outdated and verify claims against the code.
3. **Architecture decision records (ADRs).** They preserve the reasons behind choices, which are exactly what gets lost during incident firefighting. Reasons are rarely recoverable from code alone.
4. **Coding standards.** Knowing the team's conventions lets you recognize intended patterns quickly and spot deviations.
5. **Only then the editor and debugger.** A short session with docs routinely beats a long session stepping through code.

## Lightweight documentation while learning

- Stale docs: correct them as you discover the truth. Missing docs: write them as a by-product of learning. This reinforces your own understanding and treats future teammates the way you wish you had been treated.
- Keep it low ceremony. Aim to answer four questions:
  - What does the service do?
  - How does it work (main flow, key components)?
  - What does it depend on (services, data stores, queues, third parties)?
  - How do you build and run it locally?
- To keep documentation from drifting, push behavior descriptions into tests written in a behavior-driven style (given/when/then naming and structure). Those tests run in CI, so they fail when they stop being true.

## Pitfall: trusting a metric over the practice

Coverage measures which lines executed during tests, not whether behavior was checked. A team can report very high coverage and still ship regressions every release if the tests execute code without asserting anything.

Agent heuristics:
- When a user cites coverage, sample several test files and look for real assertions on outputs or interactions.
- Watch for tests that only call methods, assert trivially true conditions, or swallow exceptions.
- Generalize: any metric can be gamed or satisfied ceremonially. Ask what the practice is for, check whether that purpose is being met, and be willing to change approach.

## Software archeology: structure survey

With context gathered, open the code and survey before diving:

- **Organization.** How is code grouped: by feature, by technical layer, by module? Does the language enforce packaging, or is it convention?
- **Topology.** One deployable monolith, or a distributed system of many services? Where are the boundaries?
- **Domain vocabulary.** Which business concepts appear as types, modules, tables? Do the names match what stakeholders say?
- **Tests.** What behaviors do they describe? (See the IDE and tests reference for how to read them.)
- **Intent check.** After this pass, can you state the purpose of a given class in one sentence? If not, keep digging.

## Tracing from a landmark

1. **Work backward from callers.** Use "find callers" to climb from an unclear class up toward its entry point, often an HTTP handler, message consumer, or scheduled job. Callers reveal purpose.
2. **Run the application.** See what it actually does from a user's perspective.
3. **Pick a landmark.** A visible UI element, a request parameter, a log message, an error string, or a known side effect such as a database update. Search for it and connect it to code.
4. **Use the backlog.** A single bug or feature gives a narrow path to follow instead of the whole system.
5. **Confirm with the debugger.** Set a breakpoint where you think execution goes, trigger the action, and inspect state. Did you land where expected? A surprising path is valuable information.
6. **Iterate.** If the guess was wrong, return to step 3 with a different landmark or search term. Each loop refines your mental model of the running system.

Not every project names files helpfully; lean on full-text and symbol search when names do not guide you.

## Worked example (invented)

A developer must fix "exported invoices show the wrong currency."
- Landmark: the "Export CSV" button label in the UI. A text search finds the template, which posts to `/invoices/export`.
- Search for the route string; among several hits, the controller handler is the likely entry point.
- Find callees: the handler calls `InvoiceExporter.write`, which calls `MoneyFormatter.format`.
- Breakpoint in `format`, trigger the export: the locale argument is `null`, so a default applies. The bug is upstream, where the exporter forgets to pass the customer's locale.
- Before fixing, read the formatter's tests to learn the intended default and add a test for the export path.

## Verify what names and exceptions claim

- Names decay. A function called `validateOrder` may also persist, notify, or no longer validate anything. Read the body and its tests before relying on a name.
- Do not shortcut confirmation. Skipping verification tends to create rework later; slowing down now usually speeds up the whole task.
- Exceptions can encode wrong assumptions about what can fail. Handlers that catch the most general exception type are convenient for the author but blur which failures are possible and how each is handled. Flag them, and identify the specific failures they hide.

## Tool-assisted analysis

Modern IDEs and plug-ins can display package or module dependency graphs, revealing coupling and how pieces fit together. Use them early instead of inferring structure manually.

## Version-control history

- Browse file history and commit messages for the area you are learning. Messages often explain intent that code omits.
- Start with hotspots: files changed most often recently. A typical approach counts filenames in `git log` output over the past year.

```sh
# Top 10 most frequently changed Python files in the last year
git log --since="1 year ago" --name-only --pretty=format: -- '*.py' \
  | grep -v '^$' | sort | uniq -c | sort -rn | head -10
```

- Use blame (CLI or IDE annotations) to see who changed lines last and who changes a file most. Those people are your best first contacts.
- Ask questions early; history tells you whom to ask.

## Generated diagrams

Hand-drawn architecture models drift from reality. Diagrams generated from source stay truthful:
- Many IDEs generate class or UML diagrams with a shortcut.
- Tools such as Umbrello, Doxygen, or Structurizr can render structure from code or from a model kept next to it.
- Consider a pipeline step that regenerates diagrams on each commit so they never go stale.

## Checklist

- [ ] Talked to a teammate; know the owners
- [ ] Read README, ADRs, coding standards; noted stale parts
- [ ] Surveyed layout, topology, domain vocabulary
- [ ] Sampled tests for real assertions (not just coverage)
- [ ] Traced at least one landmark with a breakpoint
- [ ] Identified hotspots and their recent authors
- [ ] Verified suspicious names and catch-all handlers
- [ ] Updated or created the four-question docs
