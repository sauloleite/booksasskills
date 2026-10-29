---
name: ai-eng-ch01-foundation-model-applications
description: Scoping and planning guidance for products built on foundation models, based on Chapter 1 of Chip Huyen's "AI Engineering". Covers why and whether to build, buy vs build, AI and human roles, staged autonomy, defensibility, success metrics and usefulness thresholds, last-mile milestones, maintenance risk, use-case patterns, and the AI engineering stack vs ML engineering. Use when someone asks if an idea is a good LLM use case, needs success criteria or a delivery plan, worries about moats, or confuses training, finetuning and prompting.
---

# AI Engineering Ch. 1: Planning Applications on Foundation Models

This skill helps an agent advise at the very start of an AI project: deciding whether an application deserves to exist, how much the AI should do, how success will be measured, how long the hard part will take, what will break as the field moves, and which layer of the stack to work on first. It distills the opening chapter of Chip Huyen's "AI Engineering" into rules and checklists. The chapter is a map; deeper material (evaluation, prompting, RAG, finetuning, inference) belongs to later chapters.

## Key decision rules

Apply these even without opening a reference.

**Whether to build**
1. Learning project: just build. Business project: plan first, because demos are cheap and profitable products are not.
2. Rank the motivation: existential threat > profit or productivity opportunity > exploration. Existential threat means highest priority and in-house capability; opportunity means survey vendors before building; exploration only if affordable (usually not for small startups).
3. Risk-averse organizations should start internal-facing and close-ended (classification, extraction) before external or open-ended work.
4. A task is a strong candidate if AI can cut its completion time by at least half. Writing, summarization, extraction, coding documentation and creative variation are proven; highly complex coding shows little gain.

**AI and human roles**
5. Critical AI (product fails without it) needs far higher accuracy than complementary AI.
6. Proactive features need a higher quality bar than reactive ones (unrequested junk feels intrusive) but tolerate more latency (they can be precomputed).
7. Dynamic (per-user, continually updated) features require personalization and feedback infrastructure; static ones update with a shared model.
8. Raise autonomy in stages (Crawl: human mandatory; Walk: AI talks to internal staff; Run: AI talks to external users). Promote a request class only on evidence, such as agents sending AI drafts unchanged around 95% of the time.

**Defensibility (if selling the app)**
9. Technology rarely differentiates and distribution favors incumbents; data from early usage is the realistic moat for newcomers.
10. Fail the subsumption test (value exists only because today's model is weak at X) or the feature test (a big platform could clone it in weeks) and you need a niche the giants ignore, such as self-hosted open models.

**Expectations and milestones**
11. Lead with business metrics (automation share, throughput, response time, labor saved), always paired with satisfaction as a guardrail.
12. Set a usefulness threshold across quality, latency (TTFT, TPOT, total), cost per request, and fairness or interpretability. Judge latency against the current process, not an ideal.
13. Measure off-the-shelf models first; plan the gap from that baseline; abandon or rescope if reaching the threshold costs more than it returns.
14. Budget the last mile: one reported case reached 80% in a month and needed four more months to pass 95%. Never extrapolate demo velocity.

**Maintenance**
15. Re-run cost-benefit reviews periodically; today's cheapest option (for example self-hosting) can flip when API prices halve.
16. Keep models swappable, but expect to re-tune prompts and data per model; versioning plus an evaluation suite make swaps safe.
17. Track regulatory, compute-supply and IP risk; IP uncertainty can be fatal for IP-heavy businesses.

**Stack and adaptation**
18. Work top-down: application layer (prompts, context, evaluation, interface) first, then model layer (finetuning, data, inference optimization), then infrastructure as scale demands. Build the product first; invest in data and models once it shows promise.
19. Start prompt-based across several models; finetune when a measured quality, latency or cost gap remains, or the task is new to the model. Data needed: prompting < finetuning < pre-training.
20. Putting documents in the context is prompt engineering, not training or finetuning. Post-training is done by model developers; finetuning by application developers.
21. Compare models only under identical prompting setups; a prompting change alone moved one model more than 6 MMLU points.
22. Autoregressive decoding is sequential: 10 ms per token is about 1 s per 100 tokens, so plan streaming or precomputation where web-speed latency is expected.

## Default workflow

1. Clarify mode (learning or business) and the motivation level.
2. Check buy options; decide buy, build or hybrid.
3. Classify the AI role (critical/complementary, reactive/proactive, dynamic/static) and choose the starting autonomy stage with written promotion criteria.
4. If selling: run the subsumption and feature tests and name the data flywheel.
5. Write business metrics, guardrails and usefulness thresholds; run `scripts/usefulness_check.py` to sanity-check latency and cost.
6. Evaluate off-the-shelf models, record the baseline gap, and make a go or no-go call.
7. Plan milestones as metric thresholds with an explicit last-mile buffer.
8. Set up versioning, an evaluation suite and a periodic review cadence; log regulatory and IP risks.
9. Staff the application layer first; descend the stack only when the top layer is exhausted.

## References

- [references/use-case-evaluation.md](references/use-case-evaluation.md): read when deciding whether to build, buy vs build, the AI's and humans' roles, Crawl-Walk-Run promotion criteria, or defensibility. Includes a decision record template.
- [references/expectations-milestones-maintenance.md](references/expectations-milestones-maintenance.md): read when writing success metrics, usefulness thresholds, a milestone plan, last-mile estimates, or a maintenance and risk register.
- [references/use-case-patterns.md](references/use-case-patterns.md): read when brainstorming or ranking ideas, applying the exposure lens, or needing evidence for a category (coding, image and video, writing, education, bots, aggregation, data organization, workflow automation).
- [references/ai-engineering-stack.md](references/ai-engineering-stack.md): read when staffing a team, planning a platform, choosing prompting vs finetuning, explaining AI vs ML vs full-stack engineering, interface options, or why evaluation is harder.
- [references/foundation-models-and-adaptation.md](references/foundation-models-and-adaptation.md): read when explaining tokens, masked vs autoregressive models, self-supervision, model size and data, foundation and multimodal models, the three adaptation levers, or why AI engineering grew so fast.
- [references/source-map.md](references/source-map.md): read to find which reference covers a given chapter section.

## Scripts

Run `python3 scripts/usefulness_check.py` to compute estimated total latency (TTFT + TPOT x remaining output tokens) and cost per request, and to report PASS/FAIL against latency, TTFT, cost and current-process baseline targets. Exit code 1 means a target failed.

```
python3 scripts/usefulness_check.py --output-words 120 --input-tokens 1500 \
  --ttft-ms 800 --tpot-ms 40 --price-in 3 --price-out 15 \
  --max-ttft-ms 1500 --max-latency-s 8 --max-cost 0.01 \
  --baseline-s 3600 --requests-per-day 20000
```

Use `--output-tokens` instead of `--output-words` when the token count is known; `--words-per-token` (default 0.75) adjusts the conversion for other tokenizers or languages. Run with `--help` for all flags.
