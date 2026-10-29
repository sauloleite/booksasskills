## Contents
- Why the framing matters
- Terminology map
- ML problem types and how developers meet them
- Deep learning and pretrained models
- Generative AI modalities
- LLMs and generation settings
- Where AI pays off for developers
- Limitations checklist
- Model versus product
- Decision aid: should AI do this task?
- Glossary

# AI Concepts, Capabilities and Limits

## Why the framing matters

The chapter opens with an industrial analogy: an automated loom driven by punch cards did not end weaving as a profession. It shifted weavers into designing patterns, running machines and engineering textiles, and output rose. The authors argue AI is following the same pattern for developers. The practical takeaway for an agent: when a developer is anxious or dismissive about AI, steer toward adaptation. People who combine the old craft with the new tool tend to come out ahead.

AI as a field dates to the 1950s and has gone through hype cycles and funding droughts ("AI winters"), while narrow applications (fraud detection, image recognition, search ranking) kept running quietly. Public adoption exploded after ChatGPT's release in late 2022, which reached about a million users in five days and roughly 100 million within two months. The point: the tech is not new, its accessibility is.

## Terminology map

Think of nested sets: AI is the broad umbrella (from hand-written rule engines to neural networks). Machine learning sits inside AI, deep learning inside ML, and generative AI is built largely on deep learning. LLMs are the most prominent kind of generative model.

The shared idea of modern AI: the system learns statistical patterns and outputs the most probable answer, instead of executing explicit step-by-step logic written by a programmer.

A developer does not need research-level depth. The goal is enough fluency to integrate AI features and to talk productively with data scientists and ML engineers.

## ML problem types and how developers meet them

Classic programming combines inputs with hand-written rules to get outputs. ML flips it: provide inputs together with known correct outputs, and the algorithm infers the rules. This is the right approach when humans recognize the answer easily but cannot enumerate the rules, and when the rules keep shifting (spam filters face adversaries who constantly change tactics).

| Type | Question it answers | Typical use | Key property |
|---|---|---|---|
| Classification | Which category? | spam vs not, fraud flag, moderation | labels are known in advance |
| Regression | What number? | price estimate, ETA, demand forecast | output is continuous |
| Clustering | What groups exist? | customer segments, document grouping | groups are discovered, not given |

Most developers consume ML through hosted APIs or pretrained models, not by writing algorithms. A common integration pattern is to act on a prediction only when both the label matches and the confidence clears a threshold you choose. Make that threshold a configurable, tested value, and decide explicitly what happens below it (fallback rule, human queue, or default behavior).

```python
def route_ticket(text, classifier, threshold=0.8):
    label, confidence = classifier.predict(text)
    if confidence >= threshold:
        return label
    return "needs_human_triage"   # explicit low-confidence path
```

## Deep learning and pretrained models

Deep learning uses neural networks with several stacked layers (commonly three or more counts as "deep"). Raw data enters an input layer, hidden layers progressively transform it, and an output layer emits a result. In image tasks, early layers pick up edges, middle layers shapes, later layers parts such as eyes, and the final layer the overall label. Depth is what lets these models capture nuance and context beyond shallow pattern matching.

Developers usually load a model that someone else trained on a huge dataset and call it. Engineering concerns then become versioning the model identifier, handling latency and failure, and validating outputs.

## Generative AI modalities

Traditional ML judges or sorts existing data; GenAI produces new artifacts by learning how humans compose them across large multimodal corpora. Developer-relevant modalities:

- Text and code: docs, functions, friendly error messages, synthetic test data.
- Images: icons in a house style, placeholders, marketing visuals.
- Audio: speech for accessibility, music, sound effects.
- Video: product demos, animated explainers.

Rule: validate every generated artifact. Test generated code, review generated data (synthetic test data can be unrealistic or leak patterns), and check anything user-facing for accuracy and appropriateness. Requesting structured output (a typed object or JSON schema) makes generated data easier to validate.

## LLMs and generation settings

LLMs are deep neural networks and the leading form of GenAI. Products such as ChatGPT, Claude and GitHub Copilot run on them. Their edge over keyword-era AI is handling context, meaning and implied intent across a conversation, which is why they can debug, explain and complete code.

Generation settings matter when you embed an LLM in an application:

- Temperature controls randomness. Use about 0.0 to 0.5 for code and factual output; reserve about 0.7 to 1.0 for brainstorming or creative copy, knowing hallucination risk rises.
- A max token cap bounds response length and cost.
- Keep the prompt template in code under review, like any other logic.

## Where AI pays off for developers

Ordered roughly by the return the authors expect:

1. Repetitive coding: replicating a pattern across files, keeping APIs consistent, scaffolding features. Highest ROI.
2. Automation and glue: shell scripts, file shuffling, deployment steps.
3. Code explanation: onboarding to an unfamiliar codebase (ask for high-level purpose, entry points, major dependencies) or generating a study plan for a new topic.
4. Documentation: method to project level, plus format conversion (Markdown to HTML and similar).
5. Refactoring and optimization suggestions: bottlenecks, cleaner idioms, newer language features or libraries, like a senior reviewer on demand.
6. Test generation: filling gaps in neglected suites and finding missed edge cases, matching the existing suite's style when given context.
7. Code conversion between languages or frameworks: solid for high-level languages, shakier for low-level, hardware-specific or dependency-heavy code. Always test the result thoroughly.
8. UI mockups: layouts, component structure, responsive patterns, quick prototypes to compare approaches before building.
9. Language and framework questions: a patient expert to interrogate instead of trawling docs.

## Limitations checklist

Before trusting an answer, check each:

- [ ] Freshness: does the task depend on recent releases, current docs or live data? Models stop at a training cutoff.
- [ ] Hallucination: could a confident, plausible answer be invented (nonexistent APIs, wrong flags, fake citations)? Outputs come from pattern prediction, not verified facts.
- [ ] Codebase context: does the answer respect your architecture, conventions and business rules, which the model cannot see unless given?
- [ ] Bias: could training data have baked in outdated practices, cultural assumptions, or inaccessible and exclusionary patterns?
- [ ] Business judgment: does the decision involve performance vs maintainability trade-offs, regulation, or domain knowledge? Those stay human.
- [ ] Domain coverage: is the language, framework or field niche or new? Quality drops where training data is thin.
- [ ] Privacy and security: does the prompt contain secrets, credentials, schemas, proprietary logic or personal data? Many platforms retain conversations or train on inputs.

## Model versus product

Limitations belong mostly to the underlying model. A product wrapped around it may add tools that compensate, for instance web search for current information, repository indexing for codebase context, or enterprise settings that disable training on your inputs. When assessing a limitation, ask: is this a model gap that this particular product closes, or not?

## Decision aid: should AI do this task?

- Routine, well-documented, popular stack, easy to verify: yes, with review.
- Needs current information: only via a product with retrieval or search, and verify sources.
- Needs proprietary context: only with that context supplied through approved channels.
- Primarily a business or regulatory judgment: AI may enumerate options; a human decides.
- Low-level, hardware-specific or niche: use cautiously, test heavily.
- Involves sensitive data: stop unless the tool is approved for it.

## Glossary

- AI winter: a period of collapsed funding and interest in general AI research.
- Pretrained model: a model already trained on large data that you call or load rather than train.
- Hallucination: fluent, confident output that is false.
- Temperature: sampling setting controlling output randomness.
- Modality: type of content (text, image, audio, video).
