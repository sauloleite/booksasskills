# Agent Types and Reference Use Cases

## Contents
- Why a taxonomy matters
- Practical agent types
- Emerging modalities
- Reference use cases and what each stresses
- Using the taxonomy in a design conversation

## Why a taxonomy matters

"Agent" now covers everything from a trigger-driven automation to a planner that writes and runs code. Placing a request in a type sets expectations about autonomy, reasoning depth, integration surface and risk before any architecture discussion. The book's taxonomy (seven types, adapted from The Information) follows how products are actually deployed.

## Practical agent types

For each: what it is, what dominates the design, and a design hint.

1. **Business-task agents** (UiPath RPA, Power Automate, Zapier). Event-triggered deterministic action sequences with little contextual reasoning. Design is dominated by integration reliability. Hint: these are often workflows by the solution-tier test; do not add a model unless inputs vary.
2. **Conversational agents** (support chatbots, embedded assistants). Built around dialogue management, intent detection and turn-taking. Hint: invest in intent coverage, handoff to humans and conversation state.
3. **Research agents** (Perplexity, Elicit). Gather, synthesize and summarize from documents, knowledge bases or the web into structured output for analysts. Hint: source attribution and coverage are the quality levers.
4. **Analytics agents** (Power BI Copilot, Glean). Turn structured data into insights, dashboards and reports; let users query warehouses in natural language. Hint: correctness of generated queries and data-access permissions dominate.
5. **Developer agents** (Cursor, Windsurf, GitHub Copilot). Generate, refactor and explain code inside the IDE. Hint: tight IDE integration and test execution matter more than raw model size.
6. **Domain-specific agents** (Harvey for law, Hippocratic AI for medicine, finance agents). Pair domain knowledge with structured workflows to give expert-grade help. Hint: domain evaluation and compliance are the main costs.
7. **Browser-using agents**. Navigate sites, extract data and take actions without a person. Unlike classic RPA with prescripted clicks, they combine language understanding, visual perception and live planning to adapt as pages change. Hint: plan for page drift, authentication and action safety.

## Emerging modalities

- **Voice agents**: end-to-end speech understanding and generation for support lines, appointment booking and live order taking. Latency and turn-taking are the hard constraints.
- **Video agents**: avatar responses with synchronized lips, facial expression and gesture for sales, training, onboarding, marketing and virtual presence, producing personalized video without a studio.

Expect new types to keep appearing. The book itself centers on language-model agents working in text and code; business automation, voice and video receive lighter treatment.

## Reference use cases and what each stresses

The book's companion GitHub repository implements seven example agents with evaluation harnesses, reused across later chapters. Use them as templates when a user's problem resembles one.

| Example agent | Typical actions | What it stresses most |
|---|---|---|
| Customer support | Answer common questions, refunds, order changes, escalation | Escalation rules, 24/7 load, satisfaction vs cost |
| Financial services | Account servicing, loan processing, fraud review, portfolio rebalancing | Real-time anomaly detection, compliance, high-stakes actions |
| Healthcare intake and triage | Registration, insurance checks, symptom-based prioritization, scheduling, history, referrals | Safety of triage decisions, privacy |
| IT help desk | Access management, troubleshooting, software rollout, incident response, escalation | Permissioned system actions |
| Legal document review | Contract review, research, intake and conflict checks, discovery, compliance, damages, deadlines | Accuracy, citation, deadline tracking |
| SOC analyst | Alert investigation, threat intel, log queries, triage, host isolation, team updates | Parallel investigation, destructive-action safeguards |
| Supply chain and logistics | Inventory, shipment tracking, supplier evaluation, warehouse coordination, forecasting, disruption handling, compliance | Replanning under live data, exception volume |

(The table summarizes and classifies the examples; the "stresses" column is guidance added here, not from the book.)

Common thread: each agent mixes read actions (lookups, investigation) with write actions (refunds, isolation, scheduling) and has a defined human escalation path. Benefits claimed across them are efficiency, service quality and room for new offerings.

## Using the taxonomy in a design conversation

1. Name the type (or types) the request belongs to.
2. Check the solution tier: business-task agents frequently do not need a model; research and conversational agents may be RAG plus light actions; SOC, supply chain and support at scale usually justify a true agent.
3. Pick the nearest reference use case and borrow its action list, escalation design and evaluation approach.
4. List write actions separately and decide which require human approval.
5. Note modality (text, browser, voice, video) because it changes latency budgets and UX.

See also: solution-tier-selection.md.
