# Data Curation: Formats, Behaviors, Quality and Coverage

## Contents
- Why data is the application team's lever
- Match the example shape to the training phase
- Behaviors that are hard to annotate (CoT, tool use, multi-turn)
- Curation also removes data
- The three curation criteria
- Quality: six dimensions with operational tests
- Coverage: picking the diversity axes that matter
- Data mix differs by training phase
- Choosing a mix
- Worked example: support assistant for a bank
- Glossary

## Why data is the application team's lever

Model-centric work changes architecture, scale or training method on fixed data; data-centric work holds the model fixed and improves the data (fixing labels, adding edge cases, augmenting). Benchmarks increasingly take the second form (Ng's 2021 competition, DataComp, DataPerf, dcbench). Progress usually needs both, but teams that cannot pre-train compete mainly on data. Expect dedicated data roles; at scale, compliance work alone can fill a role (GPT-3 credited two people for data work, GPT-4 about eighty).

Curation, synthesis and processing are not a linear pipeline. Plan for loops: a processing finding changes the guideline, which changes what you synthesize.

## Match the example shape to the training phase

| Phase | Unit of data | How quantity is counted |
|---|---|---|
| Self-supervised / continued pre-training | raw sequences | tokens |
| Instruction finetuning (SFT) | (instruction, response) | examples |
| Preference finetuning | (instruction, winner, loser) | examples / pairs |
| Reward model | preference triplets or ((instruction, response), score) | examples |

The principles of curation are shared across phases; what differs is the mix and the target behavior.

## Behaviors that are hard to annotate

The rule is simple: the data must show the behavior you want. Some behaviors are expensive to show.

**Chain-of-thought.** If you want step-by-step answers, the responses must contain the steps. Flan-style experiments found that adding step-by-step responses to finetuning data sharply improved CoT task performance across model sizes, in some tasks roughly doubling accuracy. Writing worked reasoning costs much more than writing a final answer, which is why CoT datasets are scarcer than plain instruction sets. Budget annotator time accordingly and check that final answers are not stripped of their reasoning during processing.

**Tool use.** Examples improve latent tool skill. Typical sourcing is domain experts (prompt = task, response = action sequence). Two traps:
1. Experts describing their own workflow skip steps (memory gaps, or steps they think are trivial). Observe them doing the work instead of interviewing them.
2. Human-efficient is not agent-efficient. A person opens a browser, types a query, clicks results one by one; an agent should call a search API once and read every result. Copying human UI habits teaches the agent slow paths. This is why simulation and synthesis are common for tool data (see the synthesis reference).

Tool data may need a multi-message format: one assistant turn can address a code interpreter and the user separately. Llama 3 used per-message source/destination headers and turn-end tokens. Fix the format before collecting.

**Single-turn vs multi-turn.** Single-turn pairs teach answering one instruction and are cheap to obtain. Multi-turn data teaches task solving: asking a clarifying question first, then absorbing a user's correction in the next step. It usually needs designed scenarios or richer interaction capture. Decide which (or both) your interface requires.

## Curation also removes data

Undesired behavior often traces back to specific training examples. Illustrative case: users complain that a chatbot, asked to fact-check a sentence, confirms it and then volunteers an unrequested rewrite. Investigation finds annotations containing unsolicited suggestions. The fix is two tickets: delete those examples, and acquire new ones showing a clean fact-check with no rewrite. Treat every complaint as a hypothesis about the data.

## The three curation criteria

Quality, coverage and quantity. A cooking analogy helps: quality is whether ingredients are fresh, coverage is whether the proportions are right, quantity is how much you have. Excess in one does not compensate for failure in another.

## Quality: six dimensions with operational tests

Evidence: Yi found about 10K careful instructions beat hundreds of thousands of noisy ones; LIMA's 1,000 curated pairs on a 65B Llama matched or beat GPT-4 in 43% of human comparisons but was less robust than production models; Llama 3 found human labels error-prone on nuanced safety policy and added AI-assisted annotation.

A practical definition: data is high quality when it helps you do the job efficiently and reliably. Broader definitions exist (IBM lists seven dimensions, Wikipedia more), but for finetuning use these six. Before collecting anything, write what each means for your task.

| Dimension | Operational test |
|---|---|
| Relevant | Would this example appear in, or teach something needed for, the target task and time period? A 19th-century legal corpus is useless for current legal QA but ideal for legal history. |
| Aligned with task requirements | Does the annotation have the properties the product needs: factual if facts matter, creative if creativity matters, concise if brevity matters, a justification if the task requires one? "Aligned" is stricter than "correct": a correct but bloated answer is a bad target for a terse product. |
| Consistent | Would two annotators produce similar labels? Do equal scores mean equal quality? Inconsistency makes the target ambiguous and learning harder. A strong guideline is the main control. |
| Correctly formatted | Does every example follow the model's expected format with no stray HTML, trailing whitespace, inconsistent newlines, casing or number formats, or mistyped columns? (A float column silently stored as integer will round values and cause baffling behavior.) |
| Sufficiently unique | Are duplicates at a level your use case tolerates? Duplicates bias the model and contaminate test sets. ("Unique" here is about repetition, though owning data no one else has is also valuable.) |
| Compliant | Does the data respect laws, regulations and internal policy, for example no PII if PII is disallowed? |

## Coverage: picking the diversity axes that matter

Training data should span the problems users bring and the ways they phrase them. Coverage is achieved through diversity, so the two words are used interchangeably.

Candidate axes:
- Task type (summarize, QA, classify, extract)
- Topic or domain
- Instruction style: long and reference-heavy vs terse; with typos vs clean
- Output format: JSON, yes/no, open-ended
- Response length, context length, number of turns
- Language, dialect, culture; programming languages used
- Human-written vs AI-generated ratio

Which axes matter is application-specific. A French-to-English translator needs no language diversity but benefits from topic, length and register diversity. A global shopping assistant needs linguistic and cultural breadth more than domain breadth. General chatbots need breadth on nearly everything; NVIDIA's Nemotron data deliberately varied task, topic and instruction (format, length, open vs closed answers).

Evidence and caveats: Llama 3 credited its gains mainly to data quality, diversity and scale, not architecture; at 2,000 examples, a set both diverse and high quality beat sets with only one property; Flan gains were large from 9 to 282 tasks and small up to 1,836; and adding heterogeneous data can hurt ("The Data Addition Dilemma"). Diversity must follow the target distribution.

## Data mix differs by training phase

Llama 3 is the reference case. Domain diversity was an axis in all three phases, but proportions changed:
- Pre-training: about half general English knowledge, a quarter math and reasoning, 17% code, 8% multilingual.
- SFT: similar shape (roughly 53% general, 21% math and reasoning, 15% code, 3% multilingual) plus about 8% exam-style data and a sliver of long-context data.
- Preference finetuning: dominated by general content (about 82%), with math, reasoning and code together near 13%.

Lessons: math and code were near half of pre-training and SFT, far above their web share, because they lift reasoning more than prose, and annealing on them late in pre-training helped benchmarks; preference data mirrors real user requests; post-training adds axes (context and response length, turns, human vs synthetic ratio).

## Choosing a mix

- Default: mirror real application usage (from logs if you have them).
- At scale: run mix experiments. Meta trained several small models per candidate mix and extrapolated to the large model, then picked the best predicted mix.
- Re-check the mix after deduplication and filtering, since cleaning removes some slices disproportionately.

## Worked example: support assistant for a bank

Goal: concise card and account answers in Portuguese and English.
- Relevance: exclude superseded fee schedules. Alignment: cite the policy clause, under 120 words. Consistency: guideline gives five borderline examples each for "resolved" vs "escalate".
- Coverage axes from logs: intent (traffic-proportional, with a 3% floor for rare fraud intents), language 70/30, a quarter of instructions with natural typos, 20% multi-turn showing clarification.
- Deliberately excluded: off-domain topics, which get a small refusal slice instead.

## Glossary

- **Data mix**: domain or task proportions in one training phase.
- **Annealing**: late training with a shrinking learning rate and a shifted, higher-quality mix.
- **Multi-message format**: chat format where one turn holds several addressed messages, with headers and end-of-turn tokens.
