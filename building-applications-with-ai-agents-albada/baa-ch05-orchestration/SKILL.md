---
name: baa-ch05-orchestration
description: Guidance for orchestrating AI agents, based on Chapter 5 of Michael Albada's "Building Applications with AI Agents". Covers agent archetypes (reflex, ReAct, planner-executor, query decomposition, reflection, deep research), standard/semantic/hierarchical tool selection, tool parametrization and execution, tool topologies (single, parallel, chain, graph) and context engineering. Use when choosing an agent type, picking tools from a large catalog, designing a chain or LangGraph-style graph, assembling per-step context, or evaluating planning approaches.
---

# Orchestration (Albada, Ch. 5)

Orchestration is the control logic that turns a user request into a sequence of model calls, tool calls and data lookups. This skill helps an agent recommend the right agent archetype, the right way to pick tools, the right execution topology and the right context for each step, always biased toward the simplest design that meets the latency and accuracy target. Apply the rules below directly; open a reference only when you need the detailed playbook.

## Core decision rules

1. **Latency and accuracy trade off against each other.** Pin down the budget for both before choosing any pattern.
2. **Count the actions.** The typical number of tool calls per task predicts how much planning machinery you need: one call means no planner; a handful of dependent calls means a chain; branching plus merging means a graph.
3. **Measure plan volatility.** If later steps depend heavily on earlier results, prefer a pattern that revises the plan incrementally (ReAct, reflection, replanning planner-executor) over a fixed up-front plan.
4. **Pick the simplest archetype that works.** Reflex for fixed triggers; ReAct for exploratory work; planner-executor when the decomposition is predictable and you want cheap executors; query decomposition for multi-fact grounded answers; reflection for high-stakes, irreversible actions; deep research only when depth beats speed and cost.
5. **Tool selection by catalog size.** Small, distinct toolset: hand all tools to the model (standard). Medium to large: embed tool descriptions and retrieve top-k before the model chooses (semantic; the author's default for most cases). Very large or many near-duplicate tools: route to a described group first, then to a tool (hierarchical), accepting extra sequential calls and maintenance.
6. **Descriptions are the main accuracy lever.** Specific verb-object names, a one-line purpose that says what is unique, an example call with inputs and outputs, explicit types and ranges. Re-test after every catalog change; overlapping descriptions are the leading cause of misselection.
7. **Validate arguments before execution.** Run a cheap type and range parser on model-filled parameters and send failures back to the model for correction. Inject time, locale or user location when tools need them.
8. **Tune timeouts and retries per use case**, separately for local and remote tools.
9. **Parallel fan-out needs a ceiling.** Retrieve up to N candidate tools (for example 5), let the model prune to the needed subset, run them independently, then synthesize once.
10. **Cap chain length.** Errors compound with every link.
11. **Graphs only when you must branch and later consolidate.** Cap depth and branching factor, unit-test every router, and verify there are no cycles, unreachable nodes, dead ends or conflicting state merges.
12. **Context is assembled fresh at every step.** Include only relevant retrieved material, structure it predictably, summarize long history, and fit the token budget. Good context lets a modest model perform well; bad context sinks a strong one.
13. **Choose by experiment.** Build a representative test set and compare candidate planning approaches on it before committing.

## Default workflow

1. Write down the latency budget, accuracy bar, typical action count and how often plans must change mid-task.
2. Choose the archetype (rule 4) and the topology (rules 2, 9 to 11). Sketch nodes and edges on paper if anything branches.
3. Choose the tool-selection strategy from catalog size and overlap (rule 5); rewrite tool descriptions (rule 6).
4. Define per-step context: role instructions, current input, retrieved snippets, workflow state, prior tool results, summaries.
5. Add argument validation, timeouts, retries, chain or graph caps.
6. Build a labeled case set; measure tool-selection precision/recall and end-to-end success; validate graph structure; iterate.
7. Add complexity only when measurements show the simpler design falls short.

## References

- [references/agent-archetypes.md](references/agent-archetypes.md): read when choosing between reflex, ReAct, planner-executor, query-decomposition, reflection and deep research agents, or explaining their trade-offs.
- [references/tool-selection-and-execution.md](references/tool-selection-and-execution.md): read when designing how an agent picks tools from a catalog, writing tool descriptions, or handling parametrization, validation, timeouts and retries.
- [references/tool-topologies.md](references/tool-topologies.md): read when deciding between single-call, parallel, chain and graph execution, or designing and testing a branching graph.
- [references/context-engineering-and-planning-choice.md](references/context-engineering-and-planning-choice.md): read when assembling per-step context windows or running the final checklist for choosing and evaluating a planning approach.
- [references/source-map.md](references/source-map.md): read to see which reference covers each chapter section.

## Scripts

- Run `python3 scripts/tool_selection_eval.py cases.jsonl` to compute exact-match accuracy, micro precision/recall/F1, candidate recall (for retrieve-then-choose pipelines), mean latency and the most frequent wrong picks per strategy, from a JSONL file of labeled tool-selection cases. Use it to compare standard vs semantic vs hierarchical selection, or to spot colliding tool descriptions. `--json` prints machine-readable output.
- Run `python3 scripts/topology_check.py graph.json --max-depth 5 --max-branching 3` to validate an orchestration graph: unreachable nodes, nodes that cannot reach the terminal, cycles, max branching factor, longest path and path count, with non-zero exit on violations. Use it before implementing or after editing a LangGraph-style flow.

Both scripts print full input format details with `--help`.
