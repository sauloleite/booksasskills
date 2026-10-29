# The AI Engineering Stack and How the Role Differs

Covers the three layers of an AI application stack, what carries over from classic ML engineering, the three big differences from ML engineering, adaptation categories, the responsibilities within model development and application development, training vocabulary, and how AI engineering converges with full-stack work. Use it to staff a team, plan a platform, explain role boundaries, or decide which layer to invest in next.

## Contents
- Cutting through the hype
- The three layers and the top-down order
- What the ecosystem data shows
- Enduring ML principles
- Three structural differences from ML engineering
- Adaptation: weights unchanged vs weights changed
- Model development responsibilities
- Training vocabulary
- Application development responsibilities
- AI engineering vs full-stack engineering
- Staffing and investment checklist
- Worked examples
- Pitfalls
- Glossary

## Cutting through the hype

New tools and models arrive daily and fuel fear of missing out. Anchor on stable building blocks instead: map each tool to a layer and responsibility below, then ask whether that responsibility is a current bottleneck.

AI engineering grew out of ML engineering, so existing ML teams often lead early work; some employers merge the titles, others separate them. Skills overlap heavily, ML engineers can broaden into AI engineering, and many AI engineers have no ML background.

## The three layers and the top-down order

| Layer | Responsibilities |
|---|---|
| Application development | Prompts and context, evaluation, interfaces (most activity, fastest change) |
| Model development | Modeling, training, finetuning, inference optimization, dataset engineering, evaluation |
| Infrastructure | Serving, data and compute management, monitoring (changes least) |

Work top-down: prove value with prompts, context and interface; descend into data and models when the product shows promise and the top layer is exhausted; invest in infrastructure as scale demands.

## What the ecosystem data shows

A March 2024 scan of about 920 AI repos with 500+ GitHub stars showed tooling jumping in 2023, led by applications and application development; infrastructure grew far less because serving, resource management and monitoring needs did not change. Implication: infra skills largely transfer; spend new learning on the top two layers.

## Enduring ML principles

Keep applying, regardless of the excitement:
- Solve a business problem; map business metrics to ML metrics and back.
- Experiment systematically. The search space changed: instead of mainly hyperparameters, you vary models, prompts, retrieval algorithms, sampling parameters and more.
- Make models faster and cheaper.
- Close the loop: collect production data and feedback to improve iteratively.

A decade of ML engineering practice therefore lowers the barrier for everyone; innovations specific to foundation models sit on top of it.

## Three structural differences from ML engineering

1. **Someone else trained the model.** Effort shifts from modeling and training to adaptation.
2. **Models are bigger.** More compute, higher latency, so more pressure on efficient training and inference optimization. Many organizations now need many more GPUs and bigger clusters, creating demand for engineers who can run large clusters. One Fortune 500 AI leader admitted his team was comfortable with ten GPUs but not a thousand.
3. **Outputs are open-ended.** That flexibility enables more tasks but makes evaluation much harder.

Net summary: less model building, more adapting and evaluating.

## Adaptation: weights unchanged vs weights changed

| | Prompt-based (prompt engineering, context) | Finetuning |
|---|---|---|
| Weights | Untouched | Updated |
| Start-up effort | Low | Higher, more complex |
| Data | Little | More |
| Benefit | Fast iteration; easy to try many models, raising the odds of finding one unexpectedly good for your task | Can significantly improve quality, latency and cost |
| Limits | May fall short on complex tasks or strict performance requirements | Needed for things prompts cannot do, such as a task absent from training |

Decision rule: start prompt-based and try several models. Move to finetuning when a measured gap remains on quality, latency or cost, or when the task is genuinely new to the model. Many successful products never needed finetuning.

## Model development responsibilities

**Modeling and training.** Architecture design, training and finetuning (TensorFlow, Transformers, PyTorch). Classic ML knowledge (algorithm families, network types, gradient descent, losses, regularization) is no longer a prerequisite for building apps, though many dispute this. It stays valuable: it widens your toolset and is key to diagnosing a misbehaving model.

**Dataset engineering.** Curating, generating and annotating data to train or adapt models.
- Classic ML outputs are mostly close-ended (spam or not); foundation model outputs are open-ended, and annotating them is far harder (judging spam is easier than writing an essay).
- Classic ML centers on tabular data and feature engineering; foundation model work is unstructured and centers on quality control (stripping sensitive and toxic content), deduplication, tokenization and context retrieval.
- Data need: training from scratch > finetuning > prompt engineering. Many argue data becomes the main differentiator as models commoditize, and even without training, a model's training data hints at its strengths and weaknesses.

**Inference optimization.** Making models faster and cheaper; more important than ever because foundation models raise both cost and latency. Sequential decoding is the core obstacle: at 10 ms per token, 100 tokens take a second, against roughly 100 ms users expect from web apps. Techniques include quantization, distillation and parallelism.

| Responsibility | Classic ML | Foundation models |
|---|---|---|
| Modeling and training | ML knowledge required | Nice to have (disputed) |
| Dataset engineering | Feature engineering, tabular | Quality control, dedup, tokenization, retrieval |
| Inference optimization | Important | Even more important |

## Training vocabulary

- Training always changes weights, but quantization changes weights without being training.
- **Pre-training:** from random initialization, usually text completion. By far the costliest phase (up to about 98% of compute and data for InstructGPT); slow, and one mistake can waste large sums. Few can do it, and they are in very high demand.
- **Finetuning:** continuing from trained weights; far fewer resources than pre-training.
- **Post-training:** conceptually the same as finetuning. By convention model developers post-train (for example for instruction following before release) and application developers finetune. Pre- and post-training form a spectrum with similar tooling.
- **Misuse to correct:** putting documents in the context and calling it "training" or "finetuning" is prompt engineering, with entirely different cost, data and portability implications.

## Application development responsibilities

When many teams share the same models, differentiation moves from model quality to application development, which has three responsibilities.

**Evaluation.** Reduces risk and finds opportunities at every step: model selection, progress tracking, deployment readiness, production issue detection. Harder for foundation models because:
- Open-ended outputs: fraud detection has a ground truth; a chatbot has too many valid answers for an exhaustive reference list.
- Many adaptation techniques: a system weak under one can be strong under another.
- Case to cite: a late-2023 launch claimed a new model beat GPT-4 on MMLU using a 32-sample chain-of-thought setup against the rival's 5-shot; under identical 5-shot prompting the rival won, and the new model's own score moved over 6 points from prompting alone. Rule: compare only under identical prompting and sampling setups, and report the setup with the score.

**Prompt engineering and context construction.** Eliciting behavior from inputs alone, including supplying the context and tools a task needs, and for long, complex tasks a memory management system to track history.

**AI interface.** Previously AI lived inside the products of organizations that could build models (fraud detection in payment apps, recommendations in media apps). Now anyone can ship AI standalone or embedded in others' products. Options: standalone web, desktop or mobile apps (Streamlit, Gradio, Plotly Dash for quick builds); browser extensions; bots inside Slack, Discord, WeChat or WhatsApp; plug-ins through host product APIs (IDEs, commerce platforms, office suites), which agents can also use to act; voice; AR and VR. Chat dominates and makes feedback easy to give in natural language but hard to extract, so design feedback capture deliberately.

| Responsibility | Classic ML | Foundation models |
|---|---|---|
| AI interface | Secondary | Central |
| Prompt engineering | Did not exist | Central |
| Evaluation | Important | Even more critical |

## AI engineering vs full-stack engineering

- The interface emphasis pulls AI engineering toward full-stack work; tooling now courts front-end developers with JavaScript support (LangChain.js, Transformers.js, OpenAI's Node library, Vercel's AI SDK) alongside Python.
- More AI engineers come from web backgrounds; their edge is turning ideas into demos fast, gathering feedback and iterating.
- Workflow inversion: classic ML went data, then model, then product. AI engineering can start with the product and fund data and model work only after users validate it.
- AI engineers are usually deeply involved in product decisions, unlike many classic ML teams. One practitioner's summary: software engineering with models added to the stack.

## Staffing and investment checklist

- [ ] Application layer owners: evaluation, prompts and context, interface, feedback capture; evaluation infrastructure before the first model comparison.
- [ ] Model layer only once prompting plateaus: finetuning, dataset engineering, inference optimization.
- [ ] Infrastructure reused where possible; GPU and cluster skills match planned scale.
- [ ] At least one person with ML fundamentals for debugging.
- [ ] AI engineers sit in product discussions.

## Worked examples

**Platform team planning.** Reuse serving, monitoring and compute management. Invest in prompt and dataset versioning, an evaluation harness for open-ended outputs, retrieval services, and a model gateway allowing swaps; add inference optimization once volume justifies it.

**Model comparison request.** A manager sends two vendor benchmark tables. Check whether prompting setups match (shots, chain-of-thought, sampling); if not, rerun both on your own task under one setup before deciding.

## Pitfalls

- Starting at the bottom of the stack before validating the product.
- Comparing benchmark numbers from different prompting setups, or assuming ground truth exists for open-ended tasks.
- Treating ML knowledge as useless because it is not required.
- Underestimating the jump from a handful of GPUs to a large cluster.
- Under-investing in interfaces and feedback capture.

## Glossary

- **Context construction:** assembling the information, tools and memory the model needs in its input.
- **Quantization:** lowering weight precision; changes weights without training.
- **CoT@k:** chain-of-thought prompting with k samples; scores under different k are not comparable.
- **TTFT / TPOT:** time to first token / time per output token.
