# Agents: Definition, Tools, Planning, Function Calling, Reflection, Tool Selection

## Contents
- What an agent is
- Why agents demand stronger models
- Tool categories and their risks
- Planning: task, plan, search
- Decouple plan, validate, execute
- Intent classification and human involvement
- Can foundation models plan? (and FM vs RL planners)
- Plan generation and how to improve it
- Function calling mechanics
- Planning granularity and plan language
- Control flows
- Reflection and error correction (ReAct, Reflexion)
- Tool selection and tool evolution
- Worked example: an expense-report agent
- Glossary

## What an agent is

(The author flags this framework as provisional; agents are a young field.) Following Russell and Norvig, an agent perceives an environment and acts on it. Two things define it: its **environment** and its **action set**.
- The use case fixes the environment: a game, the web, a kitchen, roads, a terminal with a file system (SWE-agent, built on GPT-4, can navigate a repo, search, view and edit files).
- Tools extend the action set. ChatGPT is an agent (search, code execution, image generation); a RAG system is an agent whose tools are retrievers and SQL executors.
- **Mutual constraint**: the environment limits sensible actions (only legal chess moves); the tool inventory limits reachable environments (a swim-only robot stays in water).
- The model is the brain: it reads the task and feedback, sequences actions, and judges completion. Traces alternate reasoning and tool calls, notice data gaps, fetch more, then answer and declare done.

## Why agents demand stronger models

1. **Compounding errors**: success is roughly per-step accuracy to the power of the step count. At 95% per step: about 60% over 10 steps, about 0.6% over 100. Use `scripts/agent_compound_success.py` for other values.
2. **Higher stakes**: tools make each mistake more consequential.

Long runs cost time and API money; the payoff is human time saved through autonomy. Given an environment, success rests on the **tool inventory** and the **planner's strength**.

## Tool categories and their risks

Tools serve perception (**read-only actions**) or change (**write actions**).

**1. Knowledge augmentation.** Text and image retrievers, SQL executors, people search, inventory APIs, Slack retrieval, email readers: they inject private organizational knowledge. **Web access** (browsers, search, news, GitHub, social APIs) prevents staleness after the training cutoff (weather, prices, events, flight status) but exposes the agent to junk and hostile content: choose internet APIs deliberately.

**2. Capability extension.** Cheaper than training the weakness away: calculators (models are poor at large-number arithmetic), calendars, time zone and unit converters, translators for weak languages. **Code interpreters** make the agent a coder, analyst or experiment runner, but invite code injection, so sandbox and secure them. **Modality bridges**: a text-only model can call an image generator (ChatGPT uses DALL-E), render charts through code, compile LaTeX, render HTML; on the input side, captioning, transcription and OCR. Evidence: Chameleon (GPT-4 plus 13 tools such as knowledge retrieval, image captioner, text detector, Bing search) beat GPT-4 alone, adding 11.37% over the best published few-shot result on ScienceQA and 17% accuracy on TabMWP.

**3. Write actions.** One API often both reads and writes (SQL select vs drop; email read vs reply; bank balance vs transfer). They allow whole workflows (outreach from research to follow-up) to be automated. Risk: treat an unreliable model like an intern barred from the production database and from moving money. Trust needs capability plus protection against manipulation, and harm can be non-physical (market manipulation, IP theft, privacy breaches, misinformation). The author favors earning trust through safeguards over banning action.

## Planning: task, plan, search

- **Task = goal + constraints.** Invented example: a three-day offsite for 25 people in Lisbon under EUR 15,000.
- A **plan** is the step roadmap; good planning understands the task, weighs alternatives, and picks the best.
- **Valid plans differ in efficiency.** Invented example: "suppliers that are ISO-certified and located in Vietnam". If 40,000 are certified and 300 are in Vietnam, filter by country first. Pick the order that shrinks the intermediate set fastest.

## Decouple plan, validate, execute

Planning and executing in one prompt is risky: a long, aimless plan can run for hours and burn API spend unnoticed. Instead:
1. **Generate** a plan for the whole task or just the next subtask.
2. **Validate** before running: heuristics (reject unknown tools, reject plans over a step cap) and/or an AI judge asked whether the plan is sound and how to improve it.
3. Regenerate if invalid; otherwise **execute**, using function calls for tools.
4. **Evaluate outcomes** and loop.

Generator, validator and executor can each be seen as agents, so this is a multi-agent system (most real agentic workflows are). To cut latency, generate several plans in parallel and let the evaluator pick one, at extra cost.

## Intent classification and human involvement

- An **intent classifier** (prompt or trained model) steers tool choice: billing needs a payments lookup, how-to needs documentation retrieval. Include an **out-of-scope** class so impossible requests are declined instead of planned.
- **Humans can join any stage**: provide a high-level plan for the agent to expand, approve plans, or execute risky steps (database updates, merging code). This requires an explicit **automation level per action**.

Process: plan generation (task decomposition), reflection on the plan, execution, reflection on outcomes (done? errors? replan). Reflection is not required to run but strongly lifts success. Asking to reason step by step is decomposition; asking to verify an answer is reflection.

## Can foundation models plan? (and FM vs RL planners)

- Skeptics: LeCun says autoregressive LLMs cannot plan; Kambhampati says their plans look plausible but break at execution. The author calls the evidence mostly anecdotal; whether the limit is fundamental is open.
- **Planning is search**: explore paths, predict each one's reward, pick the best, or conclude none exists. Backtracking is possible in practice: the model can revise a failed path or restart.
- **Outcome prediction is the missing piece**: choosing an action needs the resulting state (prune the step off the cliff), which bare chain-of-thought does not model. Hao et al. (2023) argue an LLM's world knowledge lets it predict outcomes and plan coherently.
- A weak planner can still sit inside a system that adds search and state tracking.
- **FM vs RL planners**: both agent types are defined by environment and actions. RL planners are trained by RL, which is expensive; FM planners are the model itself, improved by prompting or finetuning, usually cheaper. FM agents can still use RL; the author expects convergence.

## Plan generation and how to improve it

- Simplest planner: a prompt listing allowed actions, requiring plans to use only them, with a few task-to-plan examples. A function-name list with arguments filled later is one of many plan formats.
- Useful helper action: build the next model query from the task history plus the latest tool output; append each output to history.
- **Arguments often depend on earlier outputs** (a date lookup fixes the date range for a sales query).
- **Underspecified requests force guesses** ("average price of our top sellers": how many, what period?). Guesses can be wrong; ask or state assumptions.
- Both actions and arguments can be hallucinated.

Improvements, cheapest first: (1) better system prompt with more examples; (2) clearer tool and parameter descriptions; (3) simpler tools, splitting complex functions; (4) a stronger model; (5) finetuning for plan generation.

## Function calling mechanics

1. **Declare a tool inventory**: entry point (function name), parameters, documentation of behavior and parameters.
2. **Restrict per query** which tools are allowed; many APIs add a mode: `required` (call at least one), `none` (call none), `auto` (model decides).
3. The model returns tool calls (name plus JSON arguments); your code executes them and returns results.

Some APIs guarantee valid function names; none guarantee correct argument values. Have the system report every parameter value it uses and inspect them.

## Planning granularity and plan language

- Detailed plans are hard to generate but easy to execute; coarse plans the reverse. **Hierarchical planning** resolves this: high-level stages first, then the same or another planner details each stage.
- **Exact function names are brittle**: a rename breaks prompts and examples, a planner finetuned on the old inventory must be retrained, and reuse across products with different APIs suffers.
- **Natural-language plans** survive API changes and match the model's training distribution, reducing hallucination. They need a **translator** to executable calls; translating is much easier than planning, so a weaker model can do it (Chameleon calls it a program generator).

## Control flows

| Flow | Meaning | Invented example |
|---|---|---|
| Sequential | B depends on A | Generate SQL, then run it |
| Parallel | A and B at once | Check stock at five warehouses simultaneously |
| If statement | B or C based on prior output | Auto-renew clause found: draft cancellation; else file it |
| For loop | Repeat until a condition holds | Retry a flaky API until success or a limit |

The model, not exact code, decides the conditions, so non-sequential plans are harder to generate and translate. When evaluating a framework, check which flows it supports; parallelism sharply cuts perceived latency.

## Reflection and error correction (ReAct, Reflexion)

Reflection is not needed to operate but is needed to succeed. Insert it after the request (feasible?), after planning (sensible?), after each step (on track?), and at the end (truly done?). Reflection finds problems; error correction fixes them.

Implementations:
- Self-critique in the same agent, a separate **scorer** model that outputs a number per outcome, or a second agent reviewing every step or every few (akin to RL actor-critic).
- **ReAct** (Yao et al., 2022): interleave reasoning (planning plus reflection) and actions in a thought, action, observation loop until a finish action; prompted with examples; shown on HotpotQA multi-hop QA.
- **Reflexion** (Shinn et al., 2023): an *evaluator* scores the outcome, a *self-reflection* module explains the failure, and the actor proposes a new trajectory (their term for plan). Invented example: tests reveal a date parser fails on leap days; reflection names the cause; the retry handles February 29.

Trade-off: reflection is easier to build than good planning and pays off surprisingly well, but its token-heavy thoughts and observations, plus the many in-prompt examples, raise cost and latency and eat context.

## Tool selection and tool evolution

The right tools depend on environment, task and model. Literature ranges from 5 tools (Toolformer, finetuned GPT-J) through 13 (Chameleon) to 1,645 APIs (Gorilla). More tools mean more capability, harder use, and longer tool descriptions that may not fit in context.

Experiment-driven selection:
1. Compare performance across alternative tool sets.
2. **Ablate**: drop a tool; if performance holds, leave it out.
3. Find tools the agent keeps misusing; if prompting and finetuning cannot fix it, replace the tool.
4. Plot the **distribution of tool calls** to spot heavy and idle tools.

Chameleon showed tool needs vary by task (ScienceQA used knowledge retrieval far more than TabMWP) and by model (GPT-4 ranged wider and favored retrieval; ChatGPT favored captioning). For frameworks, check supported planners, tool families (AutoGPT: social media APIs; Composio: enterprise APIs) and ease of adding tools.

**Tool evolution**: *tool transition* statistics (after X, how likely is Y) reveal pairs worth merging into one composite tool, which an agent could do itself. Voyager's *skill manager* saves agent-written programs that proved useful into a skill library for later retrieval and reuse.

## Worked example: an expense-report agent

Invented: file monthly expenses within policy by the 5th. Tools: receipt OCR (capability), policy retriever and card-transaction lookup (read), create-draft (write, automatic), submit (write, human approval). An intent classifier separates filing, rejection questions and out-of-scope. Plans are natural language, translated by a small model; the validator rejects unknown tools and plans over 15 steps. OCR runs in parallel; a conditional branch flags over-limit receipts for a manager. Final reflection confirms every card transaction is matched before completion is accepted, and all calls are logged for audit.

## Glossary
- **Translator / program generator**: maps natural-language plan steps to executable calls. **Trajectory**: Reflexion's word for a plan attempt. **Tool transition**: likelihood of calling Y right after X. **Skill library**: validated agent-written programs kept for reuse.
