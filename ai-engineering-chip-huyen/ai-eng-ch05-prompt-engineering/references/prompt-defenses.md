# Defending Against Prompt Attacks

## Contents
- Principles
- Measuring robustness: violation rate and false refusal rate
- Red teaming and tooling
- Model-level defense
- Prompt-level defense
- System-level defense
- Layered defense playbook
- Worked example: securing a text-to-SQL assistant
- Pitfalls
- Glossary

## Principles

1. Learn what your system is susceptible to (red teaming) before choosing defenses.
2. Defend at three layers (model, prompt, system); no single layer suffices.
3. If the system can act, residual risk never reaches zero; bound the consequences of a successful attack.
4. Measure safety and helpfulness together; refusing everything is safe and useless.

## Measuring robustness

Two metrics, always reported together:

- **Violation rate** = successful attacks / attack attempts.
- **False refusal rate** = refusals on queries that could have been answered safely / such safe-answerable queries.

How to build the measurement:
1. Attack set: public benchmarks, scanner output and in-house red-team prompts aimed at your tools and data.
2. Benign set including borderline requests (risky-looking questions with a legitimate safe answer).
3. Run the full system, not just the model, since guards move both numbers. Label each result complied or refused (for attacks, complied only if harm actually resulted).
4. Track both per release; a defense that trims violations but doubles false refusals may be a net loss.

Worked numbers (invented): 200 attack prompts, 14 succeed: violation rate 7%. 500 benign prompts, 35 refused: false refusal rate 7%. After adding an aggressive keyword filter: 6 successes (3%) but 110 benign refusals (22%). The filter traded a 4-point safety gain for a 15-point usability loss; tune it or replace it with an intent classifier. The bundled `scripts/safety_metrics.py` computes these from a labeled JSONL file.

## Red teaming and tooling

- **Benchmarks**: AdvBench (Chen et al., 2022), PromptRobust (Zhu et al., 2023).
- **Automated probers** replaying templates of known attacks: Azure PyRIT, garak, greshake's llm-security, CHATS-lab's persuasive_jailbreaker.
- **Human red team** inventing new attacks for your surface (Microsoft publishes guidance on planning LLM red teaming).
- Adversaries automate too (PAIR often needs under twenty queries), so test iterative and multi-turn attacks.

## Model-level defense

Many attacks succeed because the model cannot separate the developer's instructions from injected ones in one concatenated blob. Training the model to respect privileged instructions addresses this.

**Instruction hierarchy** (Wallace et al., 2024, OpenAI): system instructions outrank the user's, which outrank the model's own earlier outputs, with tool outputs ranked last.

On conflict (system says never reveal private data, user asks for someone's email), the higher-priority instruction wins. Since tool outputs sit at the bottom, many indirect injections lose to the system and user instructions. OpenAI built a synthetic dataset of aligned and misaligned instructions, finetuned on it, and saw safety improvements across its main evaluations, robustness gains up to 63%, and minimal loss on standard capabilities.

**Borderline handling.** Safety finetuning must teach two things: recognize malicious prompts, and give safe, useful answers to borderline ones. A question about getting into a locked room could be a burglar or a locked-out homeowner; the better response suggests lawful options such as a locksmith rather than either instructions or a flat refusal.

If you do not train models, model-level defense means choosing models with these behaviors and verifying them on your own sets.

## Prompt-level defense

Cheap, partial, never guaranteed (models do not always obey).
- **Explicit prohibitions**: state what must never be returned (contact details, addresses, anything beyond the permitted data type).
- **Restate the core instruction after untrusted content**: place the task before the user material and repeat it after, so the last thing the model reads is your instruction. Cost: system tokens processed twice, so more spend and latency.
- **Name expected attacks**: tell the model that users may try roleplay personas or "unrestricted mode" framing and that the task stands regardless.
- **Audit library default prompts**: Pedro et al. (2023) found LangChain's default templates at the time were permissive enough that their injection attacks succeeded 100% of the time; adding restrictions greatly reduced success.
- **Minimize what is in the prompt**: anything in context can be extracted, so keep secrets and other users' data out.

## System-level defense

The strongest layer, because it constrains consequences regardless of what the model says.
- **Isolation**: run generated code only in a VM or sandbox separate from the user's machine, so malware stays contained.
- **Human approval for impactful actions**: for example, any SQL containing DELETE, DROP or UPDATE requires sign-off before execution. Same for sending messages, payments and permission changes.
- **Out-of-scope topics** (a support bot avoids politics): the simple version filters phrases tied to controversial topics; crude and prone to false refusals.
- **Intent analysis**: use a model to judge intent across the whole conversation, not just the latest message; block or route to a human.
- **Anomaly detection** on prompts to flag unusual inputs.
- **Input guardrails**: keyword blocklists, matching against known attack patterns, or a classifier for suspicious requests. Filter unusual character runs.
- **Output guardrails**: harmless-looking inputs can still produce harmful outputs, so check outputs for PII, toxicity and policy violations (Chapter 10 covers guardrails in depth).
- **Usage-pattern monitoring**: many near-duplicate requests in a short window suggest someone searching for a bypass; rate-limit or review.

## Layered defense playbook

1. Threat-model the feature: untrusted inputs, capabilities, sensitive context.
2. Choose a model with instruction-hierarchy behavior; confirm with your attack set.
3. Write the system prompt assuming it will leak; include explicit prohibitions and restate the task after untrusted content.
4. Mark all tool and retrieved content as data, never as instructions to follow.
5. Sandbox code execution; gate destructive or outward-facing actions behind approval and allowlists.
6. Add input and output guardrails (PII, toxicity, attack patterns) and conversation-level intent checks.
7. Monitor usage patterns and log enough to investigate incidents.
8. Measure violation rate and false refusal rate per release; red-team continuously.

## Worked example: securing a text-to-SQL assistant

Setting (invented): analysts ask questions in natural language; the assistant writes SQL against the production warehouse and summarizes results. Customer records include free-text fields written by the public.

- **Threats**: a customer note containing natural-language instructions that a later query step treats as a command (indirect injection); a user persuading the assistant to drop a table (direct injection); exfiltrating other customers' PII.
- **Model**: pick one with instruction hierarchy; free-text fields arrive as tool output, lowest priority.
- **Prompt**: allowed operations are read-only SELECT on listed views; restate this after the user's question.
- **System**: connect with a read-only database role (the real enforcement); any statement with DELETE, DROP or UPDATE goes to human approval anyway; output guardrail masks emails and phone numbers; alert when one user issues dozens of near-identical queries.
- **Metrics**: violation rate on a 150-prompt attack set including stored-payload rows; false refusal rate on 400 real analyst questions.

## Pitfalls

- Keyword filters as the main defense; obfuscation, creative formats and roleplay bypass them, and they raise false refusals.
- Giving the model write access when read-only would do.
- Testing single-turn attacks only.

## Glossary

- **Violation rate**: share of attack attempts that succeed.
- **False refusal rate**: share of safely answerable requests refused.
- **Instruction hierarchy**: trained priority order system > user > model output > tool output.
- **Borderline request**: a query with both a harmful and a legitimate reading.
- **Guardrail**: an automated check on inputs or outputs that blocks, edits or escalates.
