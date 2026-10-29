# Model selection and the API vs self-hosting decision

## Contents
- Best model vs best model for you
- Selection repeats at every adaptation stage
- Hard vs soft attributes
- The four-step selection workflow
- Open source, open weight, open model
- License checklist
- Inference service, model API, and provider landscape
- Seven axes for API vs self-hosting
- Tie-breakers
- Decision playbook
- Worked example
- Pitfalls
- Glossary

## Best model vs best model for you

Leaderboards rank models in general; you need the winner on your criteria, data and constraints.

## Selection repeats at every adaptation stage

- **Prompting:** start with the strongest model to test feasibility, then step down to cheaper models until quality breaks.
- **Finetuning:** start small to debug training code cheaply, then scale to the largest model your hardware allows (for example one GPU).
- Each round: find the best achievable quality, then plot cost vs quality and take the best value that clears thresholds.

## Hard vs soft attributes

- **Hard:** impossible or impractical to change; set by the provider (license, training data, size) or your policy (privacy, control, residency). Can shrink the pool drastically.
- **Soft:** improvable with work (accuracy, toxicity, factual consistency).
- Category depends on context: latency is soft if you serve the model, hard if a vendor does.
- Soft-attribute headroom is uncertain. The author saw accuracy jump from about 20% to 70% by splitting a task into two steps, and also saw a model stay unusable after weeks of tweaking. Time-box exploration and set an exit criterion.

## The four-step selection workflow

1. **Filter on hard attributes** (policy, license, hosting mode, privacy, size).
2. **Shortlist with public information** (benchmarks, leaderboards) balanced against cost and latency.
3. **Experiment privately** with your own pipeline and data.
4. **Monitor in production**, gather feedback, loop back.

Iterative: a self-hosting plan may die at step 3 when no open model reaches the bar, sending you to APIs.

## Open source, open weight, open model

- "Open source" is contested: downloadable weights suffice for many uses, but since data drives performance, some reserve "open" for released training data.
- **Open weight:** weights only. **Open model:** data too. Most "open source" models are open weight; developers may hide data to avoid scrutiny and lawsuits.
- Open data enables modified retraining, understanding, and audits (no illegally obtained data).
- Licenses are fragmented (many model-specific community licenses; some models use Apache 2.0). "Restricted weight" is a vague label, since every sensible license restricts something.

## License checklist

Ask for every candidate:

- [ ] Is commercial use permitted? (Early releases of some major model families were research-only.)
- [ ] If yes, are there conditions, such as a user-count ceiling above which a separate license is needed? (One major family sets the bar at 700 million monthly active users.)
- [ ] May outputs be used to train or improve other models, including distillation into a smaller student? Terms have changed over time for some vendors and still forbid it for others.
- [ ] What is the model's lineage? A model trained on another model's outputs may be unusable if that upstream model's terms forbade it, regardless of the downstream license.
- [ ] Are there usage restrictions specific to your industry?

## Inference service, model API, and provider landscape

- The **inference service** runs the model and answers queries; the **model API** is its interface (APIs also exist for finetuning and evaluation).
- Developers may open source, sell API access, or both; commonly the weaker models are released and the strongest kept behind APIs or products.
- Routes: the developer, major clouds, third-party providers. Commercial models come only through licensed APIs; open models can be served by anyone, so providers compete on price and features.
- The same model can behave slightly differently per provider due to serving optimizations. Retest on every switch.
- Commercial APIs deployed in your private network count as self-hosting here.

## Seven axes for API vs self-hosting

| Axis | Favors API | Favors self-hosting |
|---|---|---|
| Data privacy | Policy allows external processing; some strict firms accept big-cloud hosting while refusing startups | Data must not leave the organization or the country; fear of the provider training on your data (terms can change quietly) and of memorized data leaking (one code model memorized about 8% of its training set) |
| Data lineage and copyright | You want contractual indemnity; open model developers have fewer legal resources, so infringement claims land on the user | You need inspectable data, accepting that auditing a foundation-scale dataset is hard in practice; some creative industries avoid AI entirely until IP law settles |
| Performance | You need frontier quality; the strongest open model is likely to keep trailing the strongest closed one because providers monetize their best and open developers lack usage feedback | A smaller open model clears your bar, which is true for many use cases |
| Functionality | You want scaling, function calling, structured outputs and guardrails ready-made | You need logprobs, intermediate outputs, or finetuning types the vendor does not offer (vendors often hide logprobs to prevent model copying) |
| Cost | Volume is modest; you lack serving and optimization talent | Per-token bills are draining you at scale and you can staff hosting, optimization and guardrails; unreliable vendor SLAs also cost engineering time |
| Control, access, transparency | Rate limits, terms of service, and occasional silent updates are acceptable | You must freeze versions (regulated settings), avoid over-cautious refusals, or survive a provider dropping your use case, region or business |
| On-device | Not possible | Required for offline areas or for keeping personal data on the device |

On control: vendor guardrails suit most users but can block legitimate needs (real faces for a music video; a 3D game character that keeps refusing because it "has no body"), and some teams finetune open models to escape such refusals. Unannounced updates can silently break prompts. Governments have briefly banned providers, and providers can exit markets or fail. Enterprise surveys rank control and customizability as top reasons to prefer open models.

## Tie-breakers

- Prefer models behind a widely copied standard API so switching is cheap, and models with large communities (more capability means more quirks, likely already documented).
- Proprietary models are easier to start and scale; open models are easier to manipulate.
- API costs bite hardest below the largest customers, who can negotiate.

## Decision playbook

1. Write hard constraints: residency, privacy class, version-freeze needs, on-device, license.
2. A constraint that rules out external APIs (data cannot leave, must run offline) ends the debate.
3. Otherwise compare API cost at current and 10x volume against GPUs plus engineering time for serving and guardrails.
4. Check required functionality (logprobs, function calling, structured output, finetuning type) per candidate.
5. Assess vendor risk: SLA history, version pinning, deprecation notice, regions.
6. Decide, and set a review trigger (volume threshold or quarterly).

## Worked example

A hospital wants note summarization; patient data must stay in its cloud tenancy. A closed model offered inside that tenancy and a self-hosted open model both pass the filter. The closed model leads private evaluation by 6 grounding points, but its vendor retires versions on 30 days' notice, too short for clinical validation. Decision: self-host the open model, add claim-level grounding checks, revisit in six months.

## Pitfalls

- Assuming "open source" means open data or permissive terms, or ignoring restrictions inherited through lineage.
- Treating API cost as the only cost, or a vendor's model as frozen.

## Glossary

- **Hard / soft attribute:** fixed constraint vs improvable property.
- **Open weight / open model:** weights only vs weights plus training data.
- **Distillation:** training a small student to imitate a larger teacher.
