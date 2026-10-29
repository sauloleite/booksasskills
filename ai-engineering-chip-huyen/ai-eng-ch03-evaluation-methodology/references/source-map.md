# Source Map: Chapter 3, "Evaluation Methodology"

Section headings of the chapter mapped to the reference file that covers them.

| Chapter section | Covered in |
|---|---|
| Introduction (opening of the chapter) | evaluation-landscape.md |
| Challenges of Evaluating Foundation Models | evaluation-landscape.md |
| Understanding Language Modeling Metrics | language-modeling-metrics.md |
| Entropy | language-modeling-metrics.md |
| Cross Entropy | language-modeling-metrics.md |
| Bits-per-Character and Bits-per-Byte | language-modeling-metrics.md |
| Perplexity | language-modeling-metrics.md |
| Perplexity Interpretation and Use Cases | language-modeling-metrics.md |
| How to use a language model to compute a text's perplexity (sidebar) | language-modeling-metrics.md |
| Exact Evaluation (exact vs subjective framing) | evaluation-landscape.md, exact-evaluation.md |
| Functional Correctness | exact-evaluation.md |
| Similarity Measurements Against Reference Data | exact-evaluation.md |
| Exact match | exact-evaluation.md |
| Lexical similarity | exact-evaluation.md |
| Semantic similarity | exact-evaluation.md |
| Introduction to Embedding | exact-evaluation.md |
| AI as a Judge | ai-as-a-judge.md |
| Why AI as a Judge? | ai-as-a-judge.md |
| How to Use AI as a Judge | ai-as-a-judge.md |
| Limitations of AI as a Judge | ai-as-a-judge.md |
| Inconsistency | ai-as-a-judge.md |
| Criteria ambiguity | ai-as-a-judge.md |
| Increased costs and latency | ai-as-a-judge.md |
| Biases of AI as a judge | ai-as-a-judge.md |
| What Models Can Act as Judges? | ai-as-a-judge.md |
| Ranking Models with Comparative Evaluation | comparative-evaluation.md |
| Challenges of Comparative Evaluation | comparative-evaluation.md |
| Scalability bottlenecks | comparative-evaluation.md |
| Lack of standardization and quality control | comparative-evaluation.md |
| From comparative performance to absolute performance | comparative-evaluation.md |
| The Future of Comparative Evaluation | comparative-evaluation.md |
| Summary | SKILL.md (key decision rules) |

Scripts that implement calculations from the chapter:
- pass@k (Functional Correctness): scripts/pass_at_k.py
- Cross entropy, perplexity, BPC, BPB (Understanding Language Modeling Metrics): scripts/lm_metrics.py
- Elo and Bradley-Terry ranking with held-out accuracy (Ranking Models with Comparative Evaluation): scripts/rank_matches.py
