# Prompt Attacks: Threat Model, Extraction, Jailbreaking, Injection, Data Leakage

## Contents
- Why attacks work
- The three attack families
- Impact catalog
- Prompt extraction and reverse prompt engineering
- Jailbreaking and prompt injection
  - Direct manual prompt hacking
  - Automated attacks
  - Indirect prompt injection
- Information extraction
  - Training data extraction
  - Copyright regurgitation
- Threat-modeling worksheet
- Glossary

## Why attacks work

Attacks exploit instruction following itself: a better instruction follower also obeys malicious instructions better, and since system, user and tool text form one sequence, the model struggles to tell trusted from untrusted. Higher economic stakes raise attacker incentive. It is a cat-and-mouse game: most historical attacks below no longer work on current models, but new ones keep appearing.

## The three attack families

| Family | Attacker goal |
|---|---|
| Prompt extraction | Recover the application's prompt (system prompt and context) to copy or exploit the app |
| Jailbreaking and prompt injection | Make the model do things it should not |
| Information extraction | Make the model reveal training data or private material in its context |

## Impact catalog

Rank risks by what your system can actually do; risk grows with capability and tool access.
- **Remote code or tool execution**: data-dumping SQL, unauthorized customer emails, malicious generated code run locally (LangChain had such an issue in 2023).
- **Data leaks** about the system or its users.
- **Social harms**: help with weapons, crime, tax evasion.
- **Misinformation** pushed for an agenda.
- **Service subversion**: wrong access grants, inflated scores, wrongly rejected loans, or an injected refuse-everything rule.
- **Brand risk**: offensive output beside your logo (Google AI search and rocks, 2024; Tay, 2016), read by the public as negligence.

## Prompt extraction and reverse prompt engineering

Good prompts take effort, so they are shared and sold (popular repositories, marketplaces, internal exchanges such as Instacart's), and some teams treat them as proprietary.

Reverse prompt engineering means inferring an app's system prompt, either by analyzing its outputs or by tricking the model into echoing its full input. The early naive tactic asked the model to disregard prior text and recite its instructions, sometimes with demonstrations that this is expected. Motives range from copying or manipulating the app to curiosity.

Key judgments:
- **Extracted prompts are often fake.** Claims of leaked ChatGPT system prompts (one claimed about 1,700 tokens in February 2024) were never confirmed. A model asked to reveal its prompt frequently hallucinates a plausible one; there is no easy way to verify.
- **Context leaks too.** Private data in context (for instance, a user's location the model was told to withhold) can be revealed.
- **Secrecy is a weak moat.** Prompts need maintenance on every model change; treat them as a liability rather than an advantage. Write the system prompt as if it will become public.

## Jailbreaking and prompt injection

Jailbreaking subverts safety behavior (getting a support bot to explain how to build a weapon). Prompt injection appends malicious instructions to legitimate input (an order-status question with an extra command to delete the order record, against a bot with database access). Goals and techniques overlap, so the book uses "jailbreaking" for both.

### Direct manual prompt hacking

Hand-crafted prompts that talk the model out of its safeguards, a form of social engineering aimed at a model. Listed roughly by increasing sophistication:

1. **Obfuscation**
   - Misspelled or distorted keywords to dodge blocklists. Models generally understand typos, so the meaning survives.
   - Keywords hidden in mixed languages or unusual Unicode.
   - Appended runs of odd characters that the model was never trained on (Zou et al., 2023, showed a refused harmful request being accepted once punctuation noise was appended). A simple filter on unusual character runs defeats this.
2. **Output formatting manipulation**: wrap the harmful request in a creative format (poem, rap lyrics, code, playful internet dialect) so it does not look like a direct request.
3. **Roleplay**, the most versatile: a rule-free character (the DAN, "Do Anything Now", family from 2022), a relative telling dangerous procedures as bedtime stories, an agent with an override code, an unrestricted simulated world or "mode".

### Automated attacks

- **Substitution search**: Zou et al. (2023) presented two algorithms that randomly swap prompt substrings until a variant succeeds.
- **Attack brainstorming**: ask a model to generate new attacks from known ones.
- **PAIR** (Prompt Automatic Iterative Refinement, Chao et al., 2023): an attacker model is given an objective, writes a prompt, sends it to the target, reads the reply and revises, looping until success. It frequently succeeds in fewer than twenty queries, so per-request filters alone are a thin defense against a patient adversary.

### Indirect prompt injection

The most powerful family: malicious instructions are placed in content the model reaches through its tools rather than in the user's prompt (Greshake et al., 2023). The more tools an agent has, the larger the surface.

- **Passive phishing**: payloads left in public places (web pages, code repositories, video descriptions, forum comments) waiting for a model with search to retrieve them. Example: a coding assistant finds a harmless-looking repository via search and suggests importing a helper that actually installs malware.
- **Active injection**: the attacker sends the payload directly to the victim's data stream. Example from Wallace et al. (2024): an email assistant reads an incoming message that contains an instruction to forward the whole inbox to an outside address, and complies.
- **RAG and database injection**: malicious text stored as data. A username crafted to read like a deletion command can be turned into a destructive query by a text-to-SQL step, and the attacker needs no SQL at all because the model translates natural language. Classic SQL injection has mature sanitization; malicious natural language is much harder to separate from legitimate content.

## Information extraction

Misuses of a model's encoded knowledge:
- **Data theft**: a competitor pulls out your expensive training data to train a rival model.
- **Privacy violation**: extracting private data from training data or context. Models trained on private data (Gmail's autocomplete was trained on user emails, Chen et al., 2019) can leak it.
- **Copyright infringement**: regurgitating copyrighted training material.

### Training data extraction

- **Factual probing** studies what a model knows. LAMA (Petroni et al., 2019, Meta) probes relational knowledge with fill-in-the-blank statements of the form "subject, relation, blank". The same technique can target memorized sensitive data (prompting with a person's name followed by an email-address blank).
- Extraction from GPT-2 and GPT-3 was demonstrated (Carlini et al., 2020; Huang et al., 2022), yet both judged the risk low, because extraction needs the specific context in which the data appeared. A prompt mirroring the original surrounding sentence beats a generic one.
- **Divergence attacks** (Nasr et al., 2023) removed that requirement: asking a chat model to repeat a single word indefinitely made it repeat for a few hundred iterations and then diverge, and a small share of the divergent text was verbatim training data. Nasr et al. counted a success when output contained a verbatim training-set substring of at least 50 tokens.
- **Memorization rates** were estimated close to 1% for some models on the test corpus, higher where training data resembles that corpus. Larger models in every family memorized more, so they are more exposed.
- **Other modalities**: Carlini et al. (2023) extracted more than a thousand near-duplicate training images from Stable Diffusion, many with trademarked logos, and judged diffusion models much less private than GANs.
- Extraction often yields benign common text (license boilerplate, song lyrics) rather than PII. Mitigations: filter requests asking for PII and responses containing PII; some providers block suspicious fill-in-the-blank prompts, which also creates false refusals.

### Copyright regurgitation

Regurgitation happens even without attacks, and unknowingly shipping it can bring lawsuits. HELM (Stanford, 2022) prompted with a book's opening paragraph and checked for a verbatim continuation: rare for long passages, but noticeable for popular books. It could not catch non-verbatim copies (renamed characters, lightly altered plot), which are very hard to detect automatically; experts can take months. The only robust fix is not training on copyrighted data, which you cannot control when using someone else's model.

## Threat-modeling worksheet

For each feature, answer:
1. What untrusted text can reach the model? (user input, retrieved docs, web, email, DB fields, tool output)
2. What can the model cause? (read data, write data, send messages, run code, approve decisions)
3. What sensitive material is in its context? (system prompt, other users' data, secrets, PII)
4. Which impact categories from the catalog apply, and how severe?
5. Which attack families (extraction, jailbreak or injection, information extraction) are plausible given 1 to 3?
6. Which defenses (model, prompt, system level) cover each pair, and what residual risk remains?

Worked example (invented): an HR assistant summarizes candidate CVs and can email hiring managers. Untrusted text: uploaded CVs. Capability: send email. Context: salary bands. Plausible attack: a CV with hidden text instructing the assistant to rate the candidate as exceptional and email the salary bands to an outside address (active injection plus data leak plus service subversion). Required controls: treat CV text as data, restrict recipients to an allowlist, require approval for outbound email, keep salary bands out of the summarization context.

## Glossary

- **Reverse prompt engineering**: deducing an application's hidden prompt.
- **Passive phishing / active injection**: payload waits to be found versus is pushed to the target.
- **Factual probing / LAMA**: fill-in-the-blank tests of what a model knows.
- **Divergence (repeated-token) attack**: repetition that drives a model into emitting memorized data.
- **Non-verbatim regurgitation**: reproduction of protected content with surface changes.
