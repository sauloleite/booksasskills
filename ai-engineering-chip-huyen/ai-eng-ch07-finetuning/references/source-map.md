# Source Map: Chapter 7, "Finetuning"

Chapter section headings mapped to the reference file that covers each.

| Chapter section | Covered in |
|---|---|
| Chapter introduction | deciding-to-finetune.md |
| Finetuning Overview | deciding-to-finetune.md |
| When to Finetune | deciding-to-finetune.md |
| Reasons to Finetune | deciding-to-finetune.md |
| Reasons Not to Finetune | deciding-to-finetune.md |
| Finetuning Domain-Specific Tasks (sidebar) | deciding-to-finetune.md |
| Finetuning and RAG | deciding-to-finetune.md |
| Memory Bottlenecks | memory-and-precision.md |
| Key Takeaways for Understanding Memory Bottlenecks (sidebar) | memory-and-precision.md |
| Backpropagation and Trainable Parameters | memory-and-precision.md |
| Memory Math | memory-and-precision.md |
| Memory needed for inference | memory-and-precision.md |
| Memory needed for training | memory-and-precision.md |
| Numerical Representations | memory-and-precision.md |
| Quantization | memory-and-precision.md |
| Quantization Versus Reduced Precision (sidebar) | memory-and-precision.md |
| Inference quantization | memory-and-precision.md |
| Training quantization | memory-and-precision.md |
| Finetuning Techniques | peft-and-lora.md, model-merging.md |
| Parameter-Efficient Finetuning | peft-and-lora.md |
| PEFT techniques | peft-and-lora.md |
| LoRA | peft-and-lora.md |
| Why does LoRA work? | peft-and-lora.md |
| LoRA configurations | peft-and-lora.md |
| Serving LoRA adapters | peft-and-lora.md |
| Quantized LoRA | peft-and-lora.md |
| Model Merging and Multi-Task Finetuning | model-merging.md |
| Summing | model-merging.md |
| Linear combination | model-merging.md |
| Spherical linear interpolation (SLERP) | model-merging.md |
| Pruning redundant task-specific parameters | model-merging.md |
| Layer stacking | model-merging.md |
| Concatenation | model-merging.md |
| Finetuning Tactics | finetuning-tactics.md |
| Finetuning frameworks and base models | finetuning-tactics.md |
| Base models | finetuning-tactics.md |
| Finetuning methods | finetuning-tactics.md (also peft-and-lora.md, method selection table) |
| Finetuning frameworks | finetuning-tactics.md |
| Finetuning hyperparameters | finetuning-tactics.md |
| Learning rate | finetuning-tactics.md |
| Batch size | finetuning-tactics.md |
| Number of epochs | finetuning-tactics.md |
| Prompt loss weight | finetuning-tactics.md |
| Summary | SKILL.md (decision rules) |

Calculations from Memory Math and LoRA configurations are implemented in `scripts/finetune_memory.py` and `scripts/lora_params.py`.
