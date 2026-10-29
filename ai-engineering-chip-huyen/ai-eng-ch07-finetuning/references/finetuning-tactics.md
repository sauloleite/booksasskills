# Finetuning Tactics: Base Model, Method, Framework, Hyperparameters

## Contents
- The three choices
- Choosing a base model and development path
- Choosing a finetuning method
- Choosing a framework or API
- Learning rate
- Batch size and gradient accumulation
- Epochs
- Prompt loss weight
- Reading loss curves
- Run hygiene and checklists
- Glossary

## The three choices

Deciding to finetune, getting data and maintaining the result are the hard parts. The run itself is comparatively mechanical once you have picked which base model, which method, and which tool to train with. Frameworks even propose sensible defaults; your job is to choose well and read the signals.

## Choosing a base model and development path

Apply normal model-selection criteria (size, license, benchmarks, cost, hosting). Then:
- **Feasibility: use the strongest model you can afford.** If it fails, weaker ones will too; if it succeeds, it is the benchmark for cheaper candidates.
- **Reuse what prompting taught you** about each model's behavior and failure modes.
- Prefer an instruct checkpoint close to the task.

Two paths, from OpenAI's finetuning guidance:

**Progression** (find the price/performance sweet spot):
1. Debug training code on the cheapest, fastest model.
2. Validate data on a mid-size model: training loss should keep dropping as data grows; if not, suspect data or pipeline.
3. Push quality with a few runs on the best model.
4. Train across sizes to map the price/performance frontier and choose.

**Distillation** (scarce labels, low serving budget):
1. Finetune the strongest affordable model on a small, high-quality set; strong bases need less data.
2. Generate a larger training set with it.
3. Train a cheaper model on that set.

## Choosing a finetuning method

- Start with an adapter method such as LoRA; try full finetuning later if needed. LoRA is cheap but usually tops out below full finetuning.
- Match data volume: full finetuning generally needs thousands of examples at minimum, often far more; with a few hundred, it may not beat LoRA.
- Count served variants: adapters let many share one base; full finetuning means a full model each.

## Choosing a framework or API

| Option | Pros | Cons | Fit |
|---|---|---|---|
| Hosted finetuning API (model, cloud or third-party provider) | Upload data, pick a base, get a model; no infra | Only supported bases; hidden knobs (rank caps, schedules) | Quick, simple projects |
| Open frameworks (LLaMA-Factory, unsloth, Hugging Face PEFT, Axolotl, LitGPT) | Many methods, esp. adapters; full control | You provision compute and debug | Customization |
| The model's own training code | Most faithful path to full finetuning | Most engineering | Full finetuning of a specific open model |

Adapter-only training fits on a mid-tier GPU for most models. Need more: choose a framework that integrates with your cloud. Multi-machine training needs DeepSpeed, PyTorch Distributed or ColossalAI. Curated lists such as Llama Police help track frameworks and model repos.

## Learning rate

The step size of each update: too small crawls, too large overshoots and may never converge.
- No universal value; search about 1e-7 to 1e-3.
- Common start: the end-of-pre-training learning rate times a constant from 0.1 to 1.
- Loss swinging widely: too high. Smooth but barely falling: too low. Push it up as long as the curve stays stable.
- Use a schedule: larger early, smaller late.
- Check the base model's and framework's documented values first.

## Batch size and gradient accumulation

Examples per weight update.
- Below about eight tends to be unstable; larger batches average more signal.
- Larger batches are faster but need more memory, so hardware sets the cap: more expensive compute buys faster finetuning.
- Memory-bound to tiny batches? Accumulate gradients over several micro-batches and update once. Effective batch = micro-batch x accumulation steps x devices.
- If cost is not the main constraint, try several sizes and keep the best-quality one.

## Epochs

One epoch is one pass over the data.
- Millions of examples: 1 to 2 epochs may do. Thousands: gains can continue for 4 to 10.
- Train and validation loss both still falling: more epochs (or data) help. Train falling, validation rising: overfitting, cut epochs.

## Prompt loss weight

Instruction examples contain a prompt and a response, and both can feed the loss. Users supply prompts at inference, so responses should dominate learning. 100% weights prompt tokens like response tokens; 0% learns only from responses; 10% is the usual default. Consider 0 when prompts are templated or noisy; a little higher when prompts contain domain text you want absorbed.

## Reading loss curves

| Observation | Likely cause | Action |
|---|---|---|
| Loss jumps around | LR too high or batch too small | Lower LR; raise effective batch |
| Smooth but barely decreasing | LR too low | Raise LR to just below instability |
| Flat as data grows (mid-size model) | Data or pipeline bug | Check formatting, labels, masking |
| Train and validation both still falling | Underfit | More epochs or data |
| Train falling, validation rising | Overfitting | Fewer epochs, more data, lower LoRA rank |
| Good loss, poor task metric | Loss misaligned with goal | Trust the evaluation pipeline |

## Run hygiene and checklists

Validate the whole pipeline, including checkpoint writes, on the cheapest model; an overnight run can be lost at the end because the checkpoint directory did not exist. Log hyperparameters, LoRA targets, rank and alpha, data version and base version per run.

**Before approving a project**
- [ ] Eval pipeline exists and was used for systematic prompt experiments.
- [ ] Remaining failures are behavioral; RAG tried for factual ones.
- [ ] Data source, size and quality plan exist.
- [ ] Someone can debug training; hosting and monitoring are owned and budgeted.
- [ ] Policy for re-evaluating when a better base model appears.

**Before launching a run**
- [ ] Memory estimate (weights, gradients, optimizer, activations) fits the hardware.
- [ ] Model loaded in its release dtype.
- [ ] Code and checkpoint paths validated on the cheapest model.
- [ ] LR, schedule, batch or accumulation, epochs, prompt loss weight chosen with a rationale.
- [ ] Train and validation loss both logged.

**Before shipping**
- [ ] Beats prompt-only and RAG baselines.
- [ ] No unacceptable regressions on other traffic; hallucination rate checked.
- [ ] The quantized serving artifact was evaluated.
- [ ] Serving mode chosen (merged LoRA or multi-adapter).

## Glossary

- **Progression / distillation path**: size sweep after cheap debugging / strong model's outputs train a cheap one.
- **Learning rate schedule**: rule for changing the learning rate during training.
- **Gradient accumulation**: summing gradients over micro-batches before one update.
- **Prompt loss weight**: share of loss from prompt tokens relative to response tokens.
