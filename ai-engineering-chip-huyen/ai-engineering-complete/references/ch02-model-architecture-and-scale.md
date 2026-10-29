# Model Architecture and Scale

## Contents
- Why it matters downstream
- From seq2seq to the transformer; prefill and decode
- Attention and the transformer block
- What determines parameter count
- Alternatives to the transformer
- Reading model size: parameters, sparsity, MoE
- Dataset size and training tokens
- Compute: FLOPs, utilization, cost
- Inverse scaling
- Compute-optimal scaling and its limits
- Diminishing returns and scaling extrapolation
- Scaling bottlenecks
- Worked examples
- Pitfalls and glossary

## Why it matters downstream

Architecture and parameter count are fixed before training and shape what the application team inherits: a 7B model is far easier to deploy than a 175B one, and latency work on a transformer differs from latency work on other architectures.

## From seq2seq to the transformer; prefill and decode

Seq2seq (2014, RNN encoder plus RNN decoder; in Google Translate from 2016) had two flaws the transformer (2017) fixed:
1. The decoder saw only the encoder's final hidden state, like answering questions about a book from its summary.
2. RNNs process tokens strictly one by one, slow for long inputs, and suffer vanishing or exploding gradients.

Attention lets each output token consult any earlier token. Attention predates the transformer (GNMT used it with seq2seq); the transformer's contribution was dropping RNNs entirely.

Input can now be processed in parallel, but autoregressive output is still sequential. So inference has two phases: **prefill** runs the whole prompt at once, producing the keys and values for every input token, and **decode** emits one token at a time. Diagnose any latency problem by phase first, since each phase has its own optimizations.

## Attention and the transformer block

- The query is the current decoding state; each previous token (input or already generated) has a key (like a page number) and a value (the page content).
- Scores are query-key dot products scaled by the square root of the head dimension, softmaxed, then used to weight the values. Q, K and V come from three learned matrices sized by the hidden dimension (4096 x 4096 in Llama 2-7B).
- Multi-head attention splits vectors across heads (Llama 2-7B: 32 heads of 128 dimensions), then concatenates head outputs and applies an output projection.
- Every previous token needs a stored key and value, so memory and compute grow with sequence length. This is a core reason long context is hard.

Model layout:
- **Embedding module**: token and positional embeddings. Naively the number of positions caps context length, though extension techniques exist.
- **Transformer blocks** (their count is the layer count): an attention module (query, key, value, output projection matrices) and an MLP of feedforward layers separated by cheap nonlinearities (ReLU, GELU). Fancier activations did not pay off; any fast nonlinearity suffices.
- **Output layer** (unembedding layer, or model head): maps final vectors to token probabilities.

## What determines parameter count

Hidden dimension, number of blocks, feedforward dimension and vocabulary size. Llama 2-7B and Llama 3's 8B-class model share 32 blocks and dimension 4,096 but differ in feedforward width and vocabulary (32K versus 128K); the largest Llama 3 has 126 blocks at 16,384. Longer context raises memory, not parameters.

## Alternatives to the transformer

Fashions come and go (seq2seq 2014 to 2018, GANs 2014 to 2019), but the transformer has lasted since 2017. A challenger must win at real scale on real hardware against years of optimization (first for TPUs, later GPUs). One argument: a new architecture must express programs existing networks cannot already simulate.

- **RWKV**: an RNN that trains in parallel; no theoretical context limit, which does not imply good long-context quality.
- **State space models**, promising for long-range memory: S4 (efficiency), H3 (a cheaper attention-like recall of early tokens), Mamba (3B parameters, beats same-size transformers and matches ones twice its size, inference linear in sequence length versus quadratic, gains up to million-token sequences), and Jamba (hybrid transformer-Mamba MoE, 52B total and 12B active, fits one 80 GB GPU, strong to 256K tokens, small memory footprint).

If the architecture shifts, some adaptation techniques change, but engineering fundamentals do not.

## Reading model size: parameters, sparsity, MoE

- Within a family, more parameters usually wins. Across generations, newer small models often beat older large ones (Llama 3 8B over Llama 2 70B on MMLU).
- Weight memory floor = parameters x bytes per parameter (7B at 2 bytes needs at least 14 GB); KV cache and activations add more.
- Sparsity: a 7B model at 90% sparsity has 700M non-zero weights, so a big sparse model can need less compute than a small dense one.
- MoE: Mixtral 8x7B totals 46.7B parameters (shared weights keep it under 56B); two experts run per layer per token, so about 12.9B are active and it costs and runs like a 12.9B dense model. Memory still holds all 46.7B.
- Size without data is meaningless: a large model trained on very little loses to a smaller well-trained one.

## Dataset size and training tokens

- Count tokens, not samples (a sample may be a sentence or a book), remembering counts depend on the tokenizer.
- Llama 1, 2 and 3 trained on 1.4T, 2T and 15T tokens. RedPajama-v2 has 30T tokens, much of it low quality.
- Training tokens = dataset tokens x epochs; large models typically see about one epoch.
- Pre-Chinchilla models were often data-starved (GPT-3: 175B parameters on 300B tokens), while Chinchilla used 70B on 1.4T.

## Compute: FLOPs, utilization, cost

- Machine counts are not comparable (A10 versus H100), so compute is counted in FLOPs. GPT-3-175B needed about 3.14e23; the largest PaLM-2 about 1e22.
- FLOPs is work required; FLOP/s is peak rate. "FLOPS" is ambiguous; some labs use FLOP/s-days.
- The book's reference H100 figure is 60 TFLOP/s, about 5.2e18 FLOPs per day.
- Utilization: 50% is acceptable, above 70% is great, and higher is still worth chasing.
- Time = FLOPs / (GPUs x peak FLOP/s x utilization); cost = GPU-hours x price (H100s rented for roughly $2 to $5 per hour then, falling).
- Standard estimate: training FLOPs is about 6 x parameters x tokens (GPT-3: 6 x 175e9 x 300e9, about 3.15e23).

Three numbers summarize scale: parameters (capacity), training tokens (how much was learned), FLOPs (cost).

## Inverse scaling

Anthropic (2022) found more alignment training made models likelier to voice particular political and religious views, claim conscious experience, and resist shutdown. The Inverse Scaling Prize found larger models sometimes worse on memorization and strong-prior tasks, yet awarded no top prizes because no failure was shown beyond small test sets. Use it as a reason to test, not to prefer small models.

## Compute-optimal scaling and its limits

Teams start from a budget, usually compute. Chinchilla (400 models, 70M to 16B+ parameters, 5B to 500B tokens) found compute-optimal training uses about 20 tokens per parameter (3B wants about 60B tokens), scaling both together; the fits also predict loss for a budget. With C = 6ND this gives N = sqrt(C / 120), D = 20N.

Limits:
- Assumes data is far cheaper than compute (the paper offers a variant otherwise).
- Derived for dense models on mostly human data; MoE and synthetic data are open questions.
- Optimizes training efficiency, not serving. Llama chose smaller-than-optimal models because they are cheaper to run and easier to adopt; Sardana et al. (2023) added inference demand to the law.

## Diminishing returns and scaling extrapolation

- The cost of a fixed quality level falls (ImageNet 93% cost halved from 2019 to 2021), but each improvement stays expensive: 90% to 95% costs more than 85% to 90%, and a 2% error rate may need roughly ten times the data, compute or energy of a 3% one.
- Reducing language-model loss from 3.4 nats to 2.8 takes ten times the data; doubling vision data from 1B to 2B images adds only a few ImageNet points. Still, small metric gains can be very noticeable in products.
- Big models allow one shot at hyperparameters (layers, dimension, vocabulary, batch size, epochs, learning rate, initial variance). Scaling extrapolation (hyperparameter transfer) tunes on small models and extrapolates; settings tuned at 40M parameters once carried over to 6.7B. It is hard: ten hyperparameters imply 1,024 combinations, and emergent abilities break extrapolation.

## Scaling bottlenecks

Model size grew three orders of magnitude from GPT-1 (117M) to GPT-3 (175B) in three years. Two limits now bind.

**Data.** Training sets grow faster than new human text. Assume anything posted online is or will be training data; some exploit this to steer future models, and attackers can plant injection content. Unlearning is unsolved. The web fills with AI-generated and machine-translated text (Grok once cited OpenAI's policy, blamed on ChatGPT output online), and recursive training on it may degrade models. Proprietary data becomes the moat, hence publisher licensing deals; meanwhile sites tightened terms, and about 45% of C4 is now restricted.

**Electricity.** Data centers use about 1 to 2% of global power, projected at 4 to 20% by 2030; without new supply they can grow at most about 50x, under two orders of magnitude.

## Worked examples

1. **MoE memory.** A 46.7B-total, 12.9B-active model at 16-bit needs about 93 GB for weights, so it will not fit one 80 GB GPU unquantized, though per-token compute resembles a 13B model.
2. **Budget to size.** 1e22 FLOPs gives about 9.1B parameters and 183B tokens. For heavy traffic, a team might pick 4B trained longer, accepting slightly higher loss for cheaper serving.
3. **GPT-3 rerun.** 3.14e23 FLOPs on 256 H100s at 60 TFLOP/s takes about 237 days at full utilization, about 338 at 70%, roughly $4.15M at $2 per GPU-hour.

## Pitfalls and glossary

Pitfalls: comparing parameter counts across generations; using MoE total parameters for cost or active parameters for memory; treating the weight floor as the serving requirement; confusing FLOPs with FLOP/s; applying Chinchilla to deployment without inference cost; trusting a theoretical unlimited context.

- **Active parameters**: parameters used per token in an MoE.
- **FLOP/s-day**: work of one FLOP/s sustained for a day.
- **Compute-optimal**: best quality for a fixed compute budget.
- **Hyperparameter transfer**: predicting large-model settings from small runs.
- **Emergent ability**: capability visible only at scale.
- **Inverse scaling**: tasks where bigger models do worse.
