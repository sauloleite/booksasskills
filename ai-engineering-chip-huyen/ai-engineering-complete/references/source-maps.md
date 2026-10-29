# Source maps: book sections to reference files

File names below are the chapter-prefixed names used in this folder.

## Source Map: Chapter 1 Sections to Reference Files

Chapter 1, "Introduction to Building AI Applications with Foundation Models", of Chip Huyen's "AI Engineering" (O'Reilly, 2025).

| Chapter section | Reference file |
|---|---|
| (Chapter introduction) | ch01-foundation-models-and-adaptation.md |
| The Rise of AI Engineering | ch01-foundation-models-and-adaptation.md |
| From Language Models to Large Language Models | ch01-foundation-models-and-adaptation.md |
| Language models (incl. note on tokens vs words vs characters) | ch01-foundation-models-and-adaptation.md |
| Self-supervision | ch01-foundation-models-and-adaptation.md |
| From Large Language Models to Foundation Models | ch01-foundation-models-and-adaptation.md |
| From Foundation Models to AI Engineering | ch01-foundation-models-and-adaptation.md |
| Sidebar: Why the Term "AI Engineering?" | ch01-foundation-models-and-adaptation.md |
| Foundation Model Use Cases | ch01-use-case-patterns.md |
| Coding | ch01-use-case-patterns.md |
| Image and Video Production | ch01-use-case-patterns.md |
| Writing | ch01-use-case-patterns.md |
| Education | ch01-use-case-patterns.md |
| Conversational Bots | ch01-use-case-patterns.md |
| Information Aggregation | ch01-use-case-patterns.md |
| Data Organization | ch01-use-case-patterns.md |
| Workflow Automation | ch01-use-case-patterns.md |
| Planning AI Applications | ch01-use-case-evaluation.md |
| Use Case Evaluation | ch01-use-case-evaluation.md |
| The role of AI and humans in the application | ch01-use-case-evaluation.md |
| AI product defensibility | ch01-use-case-evaluation.md |
| Setting Expectations | ch01-expectations-milestones-maintenance.md |
| Milestone Planning | ch01-expectations-milestones-maintenance.md |
| Maintenance | ch01-expectations-milestones-maintenance.md |
| The AI Engineering Stack | ch01-ai-engineering-stack.md |
| Three Layers of the AI Stack | ch01-ai-engineering-stack.md |
| AI Engineering Versus ML Engineering | ch01-ai-engineering-stack.md |
| Model development | ch01-ai-engineering-stack.md |
| Modeling and training | ch01-ai-engineering-stack.md |
| Sidebar: On the Differences Among Training, Pre-Training, Finetuning, and Post-Training | ch01-ai-engineering-stack.md |
| Dataset engineering | ch01-ai-engineering-stack.md |
| Inference optimization | ch01-ai-engineering-stack.md |
| Application development | ch01-ai-engineering-stack.md |
| Evaluation | ch01-ai-engineering-stack.md |
| Prompt engineering and context construction | ch01-ai-engineering-stack.md |
| AI interface | ch01-ai-engineering-stack.md |
| AI Engineering Versus Full-Stack Engineering | ch01-ai-engineering-stack.md |
| Summary | SKILL.md (decision rules and workflow) |

Latency and cost arithmetic from Setting Expectations and Inference optimization is also implemented in scripts/usefulness_check.py.

## Source Map: Chapter 2, "Understanding Foundation Models"

Chapter section headings mapped to the reference file that covers each.

| Chapter section | Reference file |
|---|---|
| (Chapter introduction) | SKILL.md |
| Training Data | ch02-training-data.md |
| Training Data > Multilingual Models | ch02-training-data.md |
| Training Data > Domain-Specific Models | ch02-training-data.md |
| Modeling | ch02-model-architecture-and-scale.md |
| Modeling > Model Architecture | ch02-model-architecture-and-scale.md |
| Model Architecture > Transformer architecture | ch02-model-architecture-and-scale.md |
| Model Architecture > Attention mechanism | ch02-model-architecture-and-scale.md |
| Model Architecture > Transformer block | ch02-model-architecture-and-scale.md |
| Model Architecture > Other model architectures | ch02-model-architecture-and-scale.md |
| Modeling > Model Size | ch02-model-architecture-and-scale.md |
| Model Size > Inverse Scaling (sidebar) | ch02-model-architecture-and-scale.md |
| Model Size > Scaling law: Building compute-optimal models | ch02-model-architecture-and-scale.md, scripts/scaling_calculator.py |
| Model Size > Parameter Versus Hyperparameter (sidebar) | ch02-model-architecture-and-scale.md |
| Model Size > Scaling extrapolation | ch02-model-architecture-and-scale.md |
| Model Size > Scaling bottlenecks | ch02-model-architecture-and-scale.md |
| Post-Training | ch02-post-training.md |
| Post-Training > Supervised Finetuning | ch02-post-training.md |
| Post-Training > Preference Finetuning | ch02-post-training.md |
| Preference Finetuning > Reward model | ch02-post-training.md |
| Preference Finetuning > Finetuning using the reward model | ch02-post-training.md |
| Sampling | ch02-sampling-and-test-time-compute.md |
| Sampling > Sampling Fundamentals | ch02-sampling-and-test-time-compute.md |
| Sampling > Sampling Strategies | ch02-sampling-and-test-time-compute.md, scripts/sampling_demo.py |
| Sampling Strategies > Temperature | ch02-sampling-and-test-time-compute.md |
| Sampling Strategies > Top-k | ch02-sampling-and-test-time-compute.md |
| Sampling Strategies > Top-p | ch02-sampling-and-test-time-compute.md |
| Sampling Strategies > Stopping condition | ch02-sampling-and-test-time-compute.md |
| Sampling > Test Time Compute | ch02-sampling-and-test-time-compute.md |
| Sampling > Structured Outputs | ch02-structured-outputs.md |
| Structured Outputs > Prompting | ch02-structured-outputs.md |
| Structured Outputs > Post-processing | ch02-structured-outputs.md |
| Structured Outputs > Constrained sampling | ch02-structured-outputs.md |
| Structured Outputs > Finetuning | ch02-structured-outputs.md |
| Sampling > The Probabilistic Nature of AI | ch02-inconsistency-and-hallucination.md |
| The Probabilistic Nature of AI > Inconsistency | ch02-inconsistency-and-hallucination.md |
| The Probabilistic Nature of AI > Hallucination | ch02-inconsistency-and-hallucination.md |
| Summary | SKILL.md (decision rules) |

## Source Map: Chapter 3, "Evaluation Methodology"

Section headings of the chapter mapped to the reference file that covers them.

| Chapter section | Covered in |
|---|---|
| Introduction (opening of the chapter) | ch03-evaluation-landscape.md |
| Challenges of Evaluating Foundation Models | ch03-evaluation-landscape.md |
| Understanding Language Modeling Metrics | ch03-language-modeling-metrics.md |
| Entropy | ch03-language-modeling-metrics.md |
| Cross Entropy | ch03-language-modeling-metrics.md |
| Bits-per-Character and Bits-per-Byte | ch03-language-modeling-metrics.md |
| Perplexity | ch03-language-modeling-metrics.md |
| Perplexity Interpretation and Use Cases | ch03-language-modeling-metrics.md |
| How to use a language model to compute a text's perplexity (sidebar) | ch03-language-modeling-metrics.md |
| Exact Evaluation (exact vs subjective framing) | ch03-evaluation-landscape.md, ch03-exact-evaluation.md |
| Functional Correctness | ch03-exact-evaluation.md |
| Similarity Measurements Against Reference Data | ch03-exact-evaluation.md |
| Exact match | ch03-exact-evaluation.md |
| Lexical similarity | ch03-exact-evaluation.md |
| Semantic similarity | ch03-exact-evaluation.md |
| Introduction to Embedding | ch03-exact-evaluation.md |
| AI as a Judge | ch03-ai-as-a-judge.md |
| Why AI as a Judge? | ch03-ai-as-a-judge.md |
| How to Use AI as a Judge | ch03-ai-as-a-judge.md |
| Limitations of AI as a Judge | ch03-ai-as-a-judge.md |
| Inconsistency | ch03-ai-as-a-judge.md |
| Criteria ambiguity | ch03-ai-as-a-judge.md |
| Increased costs and latency | ch03-ai-as-a-judge.md |
| Biases of AI as a judge | ch03-ai-as-a-judge.md |
| What Models Can Act as Judges? | ch03-ai-as-a-judge.md |
| Ranking Models with Comparative Evaluation | ch03-comparative-evaluation.md |
| Challenges of Comparative Evaluation | ch03-comparative-evaluation.md |
| Scalability bottlenecks | ch03-comparative-evaluation.md |
| Lack of standardization and quality control | ch03-comparative-evaluation.md |
| From comparative performance to absolute performance | ch03-comparative-evaluation.md |
| The Future of Comparative Evaluation | ch03-comparative-evaluation.md |
| Summary | SKILL.md (key decision rules) |

Scripts that implement calculations from the chapter:
- pass@k (Functional Correctness): scripts/pass_at_k.py
- Cross entropy, perplexity, BPC, BPB (Understanding Language Modeling Metrics): scripts/lm_metrics.py
- Elo and Bradley-Terry ranking with held-out accuracy (Ranking Models with Comparative Evaluation): scripts/rank_matches.py

## Source map: Chapter 4, "Evaluate AI Systems"

Chapter headings (in order) and the reference file that covers each.

| Chapter section | Covered in |
|---|---|
| Chapter introduction | SKILL.md |
| Evaluation Criteria | ch04-evaluation-criteria.md |
| Evaluation-driven development (sidebar) | ch04-evaluation-criteria.md |
| Domain-Specific Capability | ch04-evaluation-criteria.md |
| Generation Capability | ch04-evaluation-criteria.md |
| Factual consistency | ch04-factual-consistency-and-safety.md |
| Safety | ch04-factual-consistency-and-safety.md |
| Instruction-Following Capability | ch04-evaluation-criteria.md |
| Instruction-following criteria | ch04-evaluation-criteria.md |
| Roleplaying | ch04-evaluation-criteria.md |
| Cost and Latency | ch04-evaluation-criteria.md |
| Model Selection | ch04-model-selection-and-hosting.md |
| Model Selection Workflow | ch04-model-selection-and-hosting.md |
| Model Build Versus Buy | ch04-model-selection-and-hosting.md |
| Open source, open weight, and model licenses | ch04-model-selection-and-hosting.md |
| Open source models versus model APIs | ch04-model-selection-and-hosting.md |
| Data privacy | ch04-model-selection-and-hosting.md |
| Data lineage and copyright | ch04-model-selection-and-hosting.md |
| Performance | ch04-model-selection-and-hosting.md |
| Functionality | ch04-model-selection-and-hosting.md |
| API cost versus engineering cost | ch04-model-selection-and-hosting.md |
| Control, access, and transparency | ch04-model-selection-and-hosting.md |
| On-device deployment | ch04-model-selection-and-hosting.md |
| Navigate Public Benchmarks | ch04-public-benchmarks-and-contamination.md |
| Benchmark selection and aggregation | ch04-public-benchmarks-and-contamination.md |
| Public leaderboards | ch04-public-benchmarks-and-contamination.md |
| Custom leaderboards with public benchmarks | ch04-public-benchmarks-and-contamination.md |
| Are OpenAI's models getting worse? (sidebar) | ch04-public-benchmarks-and-contamination.md |
| Data contamination with public benchmarks | ch04-public-benchmarks-and-contamination.md |
| How data contamination happens | ch04-public-benchmarks-and-contamination.md |
| Handling data contamination | ch04-public-benchmarks-and-contamination.md; scripts/ngram_contamination.py |
| Design Your Evaluation Pipeline | ch04-evaluation-pipeline.md |
| Step 1. Evaluate All Components in a System | ch04-evaluation-pipeline.md |
| Step 2. Create an Evaluation Guideline | ch04-evaluation-pipeline.md |
| Define evaluation criteria | ch04-evaluation-pipeline.md |
| Create scoring rubrics with examples | ch04-evaluation-pipeline.md |
| Tie evaluation metrics to business metrics | ch04-evaluation-pipeline.md |
| Step 3. Define Evaluation Methods and Data | ch04-evaluation-pipeline.md |
| Select evaluation methods | ch04-evaluation-pipeline.md |
| Annotate evaluation data | ch04-evaluation-pipeline.md; scripts/eval_sample_size.py |
| Evaluate your evaluation pipeline | ch04-evaluation-pipeline.md |
| Iterate | ch04-evaluation-pipeline.md |
| Summary | SKILL.md |

## Source Map: Chapter 5, "Prompt Engineering"

Chapter section headings mapped to the reference file that covers each.

| Chapter section | Covered in |
|---|---|
| Chapter introduction | ch05-prompt-anatomy-and-context.md |
| Introduction to Prompting | ch05-prompt-anatomy-and-context.md |
| In-Context Learning: Zero-Shot and Few-Shot | ch05-prompt-anatomy-and-context.md |
| Sidebar: Terminology Ambiguity: Prompt Versus Context | ch05-prompt-anatomy-and-context.md |
| System Prompt and User Prompt | ch05-prompt-anatomy-and-context.md |
| Context Length and Context Efficiency | ch05-prompt-anatomy-and-context.md |
| Prompt Engineering Best Practices | ch05-writing-effective-prompts.md |
| Write Clear and Explicit Instructions | ch05-writing-effective-prompts.md |
| Explain, without ambiguity, what you want the model to do | ch05-writing-effective-prompts.md |
| Ask the model to adopt a persona | ch05-writing-effective-prompts.md |
| Provide examples | ch05-writing-effective-prompts.md |
| Specify the output format | ch05-writing-effective-prompts.md |
| Provide Sufficient Context | ch05-writing-effective-prompts.md |
| Sidebar: How to Restrict a Model's Knowledge to Only Its Context | ch05-writing-effective-prompts.md |
| Break Complex Tasks into Simpler Subtasks | ch05-writing-effective-prompts.md |
| Give the Model Time to Think | ch05-writing-effective-prompts.md |
| Iterate on Your Prompts | ch05-writing-effective-prompts.md |
| Evaluate Prompt Engineering Tools | ch05-prompt-tooling-and-versioning.md |
| Organize and Version Prompts | ch05-prompt-tooling-and-versioning.md (scripts/prompt_catalog_lint.py) |
| Defensive Prompt Engineering | ch05-prompt-attacks.md |
| Proprietary Prompts and Reverse Prompt Engineering | ch05-prompt-attacks.md |
| Jailbreaking and Prompt Injection | ch05-prompt-attacks.md |
| Direct manual prompt hacking | ch05-prompt-attacks.md |
| Automated attacks | ch05-prompt-attacks.md |
| Indirect prompt injection | ch05-prompt-attacks.md |
| Information Extraction | ch05-prompt-attacks.md |
| Defenses Against Prompt Attacks | ch05-prompt-defenses.md (scripts/safety_metrics.py) |
| Model-level defense | ch05-prompt-defenses.md |
| Prompt-level defense | ch05-prompt-defenses.md |
| System-level defense | ch05-prompt-defenses.md |
| Summary | SKILL.md (decision rules) |

## Source Map: Chapter 6 "RAG and Agents" to reference files

Chapter section headings (in book order) and the reference file that covers each.

| Chapter section | Covered in |
|---|---|
| Chapter introduction (instructions vs context) | ch06-retrieval-foundations.md |
| RAG | ch06-retrieval-foundations.md |
| RAG Architecture | ch06-retrieval-foundations.md |
| Retrieval Algorithms | ch06-retrieval-foundations.md |
| Sidebar: Sparse Versus Dense Retrieval | ch06-retrieval-foundations.md |
| Term-based retrieval | ch06-retrieval-foundations.md |
| Embedding-based retrieval | ch06-retrieval-foundations.md |
| Comparing retrieval algorithms | ch06-retrieval-foundations.md |
| Combining retrieval algorithms | ch06-retrieval-foundations.md |
| Retrieval Optimization | ch06-retrieval-optimization-and-multimodal.md |
| Chunking strategy | ch06-retrieval-optimization-and-multimodal.md |
| Reranking | ch06-retrieval-optimization-and-multimodal.md |
| Query rewriting | ch06-retrieval-optimization-and-multimodal.md |
| Contextual retrieval | ch06-retrieval-optimization-and-multimodal.md |
| Sidebar: Evaluating Retrieval Solutions | ch06-retrieval-optimization-and-multimodal.md |
| RAG Beyond Texts | ch06-retrieval-optimization-and-multimodal.md |
| Multimodal RAG | ch06-retrieval-optimization-and-multimodal.md |
| RAG with tabular data | ch06-retrieval-optimization-and-multimodal.md |
| Agents | ch06-agents-tools-and-planning.md |
| Agent Overview | ch06-agents-tools-and-planning.md |
| Tools | ch06-agents-tools-and-planning.md |
| Knowledge augmentation | ch06-agents-tools-and-planning.md |
| Capability extension | ch06-agents-tools-and-planning.md |
| Write actions | ch06-agents-tools-and-planning.md |
| Planning | ch06-agents-tools-and-planning.md |
| Planning overview | ch06-agents-tools-and-planning.md |
| Foundation models as planners | ch06-agents-tools-and-planning.md |
| Sidebar: Foundation Model (FM) Versus Reinforcement Learning (RL) Planners | ch06-agents-tools-and-planning.md |
| Plan generation | ch06-agents-tools-and-planning.md |
| Function calling | ch06-agents-tools-and-planning.md |
| Planning granularity | ch06-agents-tools-and-planning.md |
| Complex plans | ch06-agents-tools-and-planning.md |
| Reflection and error correction | ch06-agents-tools-and-planning.md |
| Tool selection | ch06-agents-tools-and-planning.md |
| Agent Failure Modes and Evaluation | ch06-agent-evaluation.md |
| Planning failures | ch06-agent-evaluation.md |
| Tool failures | ch06-agent-evaluation.md |
| Efficiency | ch06-agent-evaluation.md |
| Memory | ch06-memory.md |
| Summary | SKILL.md (decision rules) |

## Source Map: Chapter 7, "Finetuning"

Chapter section headings mapped to the reference file that covers each.

| Chapter section | Covered in |
|---|---|
| Chapter introduction | ch07-deciding-to-finetune.md |
| Finetuning Overview | ch07-deciding-to-finetune.md |
| When to Finetune | ch07-deciding-to-finetune.md |
| Reasons to Finetune | ch07-deciding-to-finetune.md |
| Reasons Not to Finetune | ch07-deciding-to-finetune.md |
| Finetuning Domain-Specific Tasks (sidebar) | ch07-deciding-to-finetune.md |
| Finetuning and RAG | ch07-deciding-to-finetune.md |
| Memory Bottlenecks | ch07-memory-and-precision.md |
| Key Takeaways for Understanding Memory Bottlenecks (sidebar) | ch07-memory-and-precision.md |
| Backpropagation and Trainable Parameters | ch07-memory-and-precision.md |
| Memory Math | ch07-memory-and-precision.md |
| Memory needed for inference | ch07-memory-and-precision.md |
| Memory needed for training | ch07-memory-and-precision.md |
| Numerical Representations | ch07-memory-and-precision.md |
| Quantization | ch07-memory-and-precision.md |
| Quantization Versus Reduced Precision (sidebar) | ch07-memory-and-precision.md |
| Inference quantization | ch07-memory-and-precision.md |
| Training quantization | ch07-memory-and-precision.md |
| Finetuning Techniques | ch07-peft-and-lora.md, ch07-model-merging.md |
| Parameter-Efficient Finetuning | ch07-peft-and-lora.md |
| PEFT techniques | ch07-peft-and-lora.md |
| LoRA | ch07-peft-and-lora.md |
| Why does LoRA work? | ch07-peft-and-lora.md |
| LoRA configurations | ch07-peft-and-lora.md |
| Serving LoRA adapters | ch07-peft-and-lora.md |
| Quantized LoRA | ch07-peft-and-lora.md |
| Model Merging and Multi-Task Finetuning | ch07-model-merging.md |
| Summing | ch07-model-merging.md |
| Linear combination | ch07-model-merging.md |
| Spherical linear interpolation (SLERP) | ch07-model-merging.md |
| Pruning redundant task-specific parameters | ch07-model-merging.md |
| Layer stacking | ch07-model-merging.md |
| Concatenation | ch07-model-merging.md |
| Finetuning Tactics | ch07-finetuning-tactics.md |
| Finetuning frameworks and base models | ch07-finetuning-tactics.md |
| Base models | ch07-finetuning-tactics.md |
| Finetuning methods | ch07-finetuning-tactics.md (also ch07-peft-and-lora.md, method selection table) |
| Finetuning frameworks | ch07-finetuning-tactics.md |
| Finetuning hyperparameters | ch07-finetuning-tactics.md |
| Learning rate | ch07-finetuning-tactics.md |
| Batch size | ch07-finetuning-tactics.md |
| Number of epochs | ch07-finetuning-tactics.md |
| Prompt loss weight | ch07-finetuning-tactics.md |
| Summary | SKILL.md (decision rules) |

Calculations from Memory Math and LoRA configurations are implemented in `scripts/finetune_memory.py` and `scripts/lora_params.py`.

## Source Map: Chapter 8 "Dataset Engineering"

Chapter headings mapped to the reference file that covers each.

| Chapter section | Covered in |
|---|---|
| Chapter 8 introduction | ch08-curation-quality-and-coverage.md |
| A Data-Centric View of AI (sidebar) | ch08-curation-quality-and-coverage.md |
| Data Curation | ch08-curation-quality-and-coverage.md |
| Data Quality | ch08-curation-quality-and-coverage.md |
| Data Coverage | ch08-curation-quality-and-coverage.md |
| Data Quantity | ch08-quantity-acquisition-and-annotation.md |
| Data Acquisition and Annotation | ch08-quantity-acquisition-and-annotation.md |
| Resources for Publicly Available Datasets (sidebar) | ch08-quantity-acquisition-and-annotation.md |
| Data Augmentation and Synthesis | ch08-data-synthesis-techniques.md |
| Why Data Synthesis | ch08-data-synthesis-techniques.md |
| Traditional Data Synthesis Techniques | ch08-data-synthesis-techniques.md |
| Rule-based data synthesis | ch08-data-synthesis-techniques.md |
| Simulation | ch08-data-synthesis-techniques.md |
| AI-Powered Data Synthesis | ch08-data-synthesis-techniques.md |
| Instruction data synthesis | ch08-data-synthesis-techniques.md |
| Data verification | ch08-verification-limits-and-distillation.md |
| Limitations to AI-generated data | ch08-verification-limits-and-distillation.md |
| Quality control | ch08-verification-limits-and-distillation.md |
| Superficial imitation | ch08-verification-limits-and-distillation.md |
| Potential model collapse | ch08-verification-limits-and-distillation.md |
| Obscure data lineage | ch08-verification-limits-and-distillation.md |
| Model Distillation | ch08-verification-limits-and-distillation.md |
| Data Processing (efficiency tips) | ch08-data-processing.md |
| Inspect Data | ch08-data-processing.md |
| Deduplicate Data | ch08-data-processing.md |
| Clean and Filter Data | ch08-data-processing.md |
| Format Data | ch08-data-processing.md |
| Summary | SKILL.md (key decision rules) |

## Source Map: Chapter 9, "Inference Optimization"

Chapter section headings mapped to the reference file that covers each.

| Chapter section | Reference file |
|---|---|
| Chapter introduction (model, hardware and service levels) | ch09-bottlenecks-and-hardware.md |
| Understanding Inference Optimization | ch09-bottlenecks-and-hardware.md |
| Inference Overview | ch09-bottlenecks-and-hardware.md |
| Computational bottlenecks | ch09-bottlenecks-and-hardware.md |
| Terminology Ambiguity: Memory-Bound Versus Bandwidth-Bound (sidebar) | ch09-bottlenecks-and-hardware.md |
| Online and batch inference APIs | ch09-service-level-optimization.md |
| Inference Performance Metrics | ch09-metrics-and-measurement.md |
| Latency, TTFT, and TPOT | ch09-metrics-and-measurement.md |
| Throughput and goodput | ch09-metrics-and-measurement.md |
| Utilization, MFU, and MBU | ch09-metrics-and-measurement.md |
| AI Accelerators | ch09-bottlenecks-and-hardware.md |
| What's an accelerator? | ch09-bottlenecks-and-hardware.md |
| Computational capabilities | ch09-bottlenecks-and-hardware.md |
| Memory size and bandwidth | ch09-bottlenecks-and-hardware.md |
| Power consumption | ch09-bottlenecks-and-hardware.md |
| Selecting Accelerators (sidebar) | ch09-bottlenecks-and-hardware.md |
| Inference Optimization | ch09-model-compression-and-decoding.md (intro, quality drift) |
| Model Optimization | ch09-model-compression-and-decoding.md |
| Model compression | ch09-model-compression-and-decoding.md |
| Overcoming the autoregressive decoding bottleneck | ch09-model-compression-and-decoding.md |
| Speculative decoding | ch09-model-compression-and-decoding.md |
| Inference with reference | ch09-model-compression-and-decoding.md |
| Parallel decoding | ch09-model-compression-and-decoding.md |
| Attention mechanism optimization | ch09-attention-kv-cache-and-kernels.md |
| Calculating the KV Cache Size (sidebar) | ch09-attention-kv-cache-and-kernels.md |
| Redesigning the attention mechanism | ch09-attention-kv-cache-and-kernels.md |
| Optimizing the KV cache size | ch09-attention-kv-cache-and-kernels.md |
| Writing kernels for attention computation | ch09-attention-kv-cache-and-kernels.md |
| Kernels and compilers | ch09-attention-kv-cache-and-kernels.md |
| Inference Optimization Case Study from PyTorch (sidebar) | ch09-attention-kv-cache-and-kernels.md |
| Inference Service Optimization | ch09-service-level-optimization.md |
| Batching | ch09-service-level-optimization.md |
| Decoupling prefill and decode | ch09-service-level-optimization.md |
| Prompt caching | ch09-service-level-optimization.md |
| Parallelism | ch09-service-level-optimization.md |
| Summary | ch09-service-level-optimization.md (choosing techniques by workload); SKILL.md decision rules |

## Source Map: Chapter 10 Headings to Reference Files

| Chapter section | Covered in |
|---|---|
| Chapter introduction | SKILL.md (purpose) |
| AI Engineering Architecture (overview, simplest architecture, build order) | ch10-context-and-guardrails.md |
| Step 1. Enhance Context | ch10-context-and-guardrails.md |
| Step 2. Put in Guardrails | ch10-context-and-guardrails.md |
| Input guardrails | ch10-context-and-guardrails.md |
| Output guardrails | ch10-context-and-guardrails.md |
| Guardrail implementation | ch10-context-and-guardrails.md |
| Step 3. Add Model Router and Gateway | ch10-routing-gateway-and-caching.md |
| Router | ch10-routing-gateway-and-caching.md |
| Gateway | ch10-routing-gateway-and-caching.md |
| Step 4. Reduce Latency with Caches | ch10-routing-gateway-and-caching.md |
| Exact caching | ch10-routing-gateway-and-caching.md |
| Semantic caching | ch10-routing-gateway-and-caching.md |
| Step 5. Add Agent Patterns | ch10-agents-and-orchestration.md |
| Monitoring and Observability | ch10-observability.md |
| Monitoring versus observability | ch10-observability.md |
| Metrics | ch10-observability.md |
| Logs and traces | ch10-observability.md |
| Drift detection | ch10-observability.md |
| AI Pipeline Orchestration | ch10-agents-and-orchestration.md |
| User Feedback | ch10-conversational-feedback-signals.md |
| Extracting Conversational Feedback | ch10-conversational-feedback-signals.md |
| Natural language feedback (early termination, error correction, complaints, sentiment) | ch10-conversational-feedback-signals.md |
| Other conversational feedback (regeneration, conversation organization, conversation length, dialogue diversity) | ch10-conversational-feedback-signals.md |
| Feedback Design | ch10-feedback-design-and-limitations.md |
| When to collect feedback | ch10-feedback-design-and-limitations.md |
| How to collect feedback | ch10-feedback-design-and-limitations.md |
| Feedback Limitations | ch10-feedback-design-and-limitations.md |
| Biases | ch10-feedback-design-and-limitations.md |
| Degenerate feedback loop | ch10-feedback-design-and-limitations.md |
| Summary (modularity, system thinking, engineers owning feedback) | ch10-agents-and-orchestration.md, ch10-feedback-design-and-limitations.md |
