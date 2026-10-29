# Source maps: book sections to reference files

File names below are the chapter-prefixed names used in this folder.

## Source Map: Chapter 1 Sections to Reference Files

Chapter 1, "Introduction to Agents", of Michael Albada's "Building Applications with AI Agents" (O'Reilly, 2025).

| Chapter section | Reference file |
|---|---|
| (Chapter introduction) | ch01-solution-tier-selection.md |
| Defining AI Agents | ch01-solution-tier-selection.md |
| The Pretraining Revolution | ch01-models-and-frameworks.md |
| Types of Agents | ch01-agent-types-and-use-cases.md |
| Model Selection | ch01-models-and-frameworks.md |
| From Synchronous to Asynchronous Operations | ch01-solution-tier-selection.md |
| Practical Applications and Use Cases | ch01-agent-types-and-use-cases.md |
| Workflows and Agents | ch01-solution-tier-selection.md |
| Principles for Building Effective Agentic Systems | ch01-principles-and-organization.md |
| Organizing for Success in Building Agentic Systems | ch01-principles-and-organization.md |
| Agentic Frameworks | ch01-models-and-frameworks.md |
| LangGraph | ch01-models-and-frameworks.md |
| AutoGen | ch01-models-and-frameworks.md |
| CrewAI | ch01-models-and-frameworks.md |
| OpenAI Agents Software Development Kit (SDK) | ch01-models-and-frameworks.md |
| Conclusion | ch01-principles-and-organization.md; SKILL.md (decision rules) |

The chapter has no calculations that warrant a script.

## Source Map: Chapter 2, Designing Agent Systems

| Chapter section | Covered in |
|---|---|
| (Chapter introduction) | SKILL.md |
| Our First Agent System | ch02-scoping-the-first-agent.md |
| Core Components of Agent Systems | ch02-core-components.md |
| Model Selection | ch02-core-components.md (+ scripts/model_cost_compare.py) |
| Tools | ch02-core-components.md |
| Designing Capabilities for Specific Tasks | ch02-core-components.md |
| Tool Integration and Modularity | ch02-core-components.md |
| Memory | ch02-core-components.md |
| Short-Term Memory | ch02-core-components.md |
| Long-Term Memory | ch02-core-components.md |
| Memory Management and Retrieval | ch02-core-components.md |
| Orchestration | ch02-core-components.md |
| Design Trade-Offs | ch02-design-trade-offs.md |
| Performance: Speed/Accuracy Trade-Offs | ch02-design-trade-offs.md |
| Scalability: Engineering Scalability for Agent Systems | ch02-design-trade-offs.md |
| Reliability: Ensuring Robust and Consistent Agent Behavior | ch02-design-trade-offs.md |
| Fault tolerance | ch02-design-trade-offs.md |
| Consistency and robustness | ch02-design-trade-offs.md |
| Costs: Balancing Performance and Expense | ch02-design-trade-offs.md (+ scripts/model_cost_compare.py) |
| Development costs | ch02-design-trade-offs.md |
| Operational costs | ch02-design-trade-offs.md |
| Cost versus value | ch02-design-trade-offs.md |
| Architecture Design Patterns | ch02-architecture-patterns.md |
| Single-Agent Architectures | ch02-architecture-patterns.md |
| Multiagent Architectures: Collaboration, Parallelism, and Coordination | ch02-architecture-patterns.md |
| Best Practices | ch02-evaluation-and-rollout.md |
| Iterative Design | ch02-evaluation-and-rollout.md |
| Evaluation Strategy | ch02-evaluation-and-rollout.md |
| Real-World Testing | ch02-evaluation-and-rollout.md |
| Conclusion | SKILL.md |

## Source Map: Chapter 3 Sections to Reference Files

| Chapter section | Covered in |
|---|---|
| Chapter introduction (modality overview, context over time, capability communication, trust) | ch03-interaction-modalities.md (selection matrix), ch03-context-and-personalization.md (context spectrum) |
| Interaction Modalities | ch03-interaction-modalities.md |
| Text-Based | ch03-interaction-modalities.md |
| Graphical Interfaces | ch03-interaction-modalities.md |
| Speech and Voice Interfaces | ch03-interaction-modalities.md |
| Video-Based Interfaces | ch03-interaction-modalities.md |
| Combining Modalities for Seamless Experiences | ch03-interaction-modalities.md |
| The Autonomy Slider | ch03-autonomy-and-engagement-timing.md |
| Synchronous Versus Asynchronous Agent Experiences | ch03-autonomy-and-engagement-timing.md |
| Design Principles for Synchronous Experiences | ch03-autonomy-and-engagement-timing.md |
| Design Principles for Asynchronous Experiences | ch03-autonomy-and-engagement-timing.md |
| Finding the Balance Between Proactive and Intrusive Agent Behavior | ch03-autonomy-and-engagement-timing.md |
| Context Retention and Continuity | ch03-context-and-personalization.md |
| Maintaining State Across Interactions | ch03-context-and-personalization.md |
| Personalization and Adaptability | ch03-context-and-personalization.md |
| Communicating Agent Capabilities | ch03-capabilities-uncertainty-clarification.md |
| Communicating Confidence and Uncertainty | ch03-capabilities-uncertainty-clarification.md |
| Asking for Guidance and Input from Users | ch03-capabilities-uncertainty-clarification.md |
| Failing Gracefully | ch03-graceful-failure-and-trust.md |
| Trust in Interaction Design | ch03-graceful-failure-and-trust.md |
| Conclusion | ch03-graceful-failure-and-trust.md (pattern summary) |

## Source map: Chapter 4, Tool Use

| Chapter section | Covered in |
|---|---|
| Chapter introduction (what a tool is, why tools matter) | SKILL.md (purpose), ch04-tool-types-and-selection.md |
| LangChain Fundamentals | ch04-tool-definition-and-invocation.md (basic invocation loop) |
| Local Tools (metadata guidance; scalability, duplication, maintenance; calculator example) | ch04-tool-types-and-selection.md, ch04-tool-definition-and-invocation.md (metadata) |
| API-Based Tools (Wikipedia and stock price examples; design guidance) | ch04-tool-types-and-selection.md |
| Plug-In Tools (platform comparison, open source ecosystem, applications, future) | ch04-tool-types-and-selection.md |
| Model Context Protocol | ch04-mcp-integration.md |
| Stateful Tools | ch04-stateful-tool-safety.md |
| Automated Tool Development | ch04-automated-tool-development.md |
| Foundation Models as Tool Makers | ch04-automated-tool-development.md |
| Real-Time Code Generation | ch04-automated-tool-development.md |
| Tool Use Configuration (tool-choice modes; validate, retry, fall back, log) | ch04-tool-definition-and-invocation.md |
| Conclusion | SKILL.md (key decision rules), ch04-automated-tool-development.md (imitation and reinforcement learning mention) |

## Source map: Chapter 5, Orchestration

| Chapter section | Covered in |
|---|---|
| Introduction (orchestration overview) | SKILL.md |
| Agent Types | ch05-agent-archetypes.md |
| Reflex Agents | ch05-agent-archetypes.md |
| ReAct Agents | ch05-agent-archetypes.md |
| Planner-Executor Agents | ch05-agent-archetypes.md |
| Query-Decomposition Agents | ch05-agent-archetypes.md |
| Reflection Agents | ch05-agent-archetypes.md |
| Deep Research Agents | ch05-agent-archetypes.md |
| Tool Selection | ch05-tool-selection-and-execution.md |
| Standard Tool Selection | ch05-tool-selection-and-execution.md |
| Semantic Tool Selection | ch05-tool-selection-and-execution.md |
| Hierarchical Tool Selection | ch05-tool-selection-and-execution.md |
| Tool Execution | ch05-tool-selection-and-execution.md |
| Tool Topologies | ch05-tool-topologies.md |
| Single Tool Execution | ch05-tool-topologies.md |
| Parallel Tool Execution | ch05-tool-topologies.md |
| Chains | ch05-tool-topologies.md |
| Graphs | ch05-tool-topologies.md |
| Context Engineering | ch05-context-engineering-and-planning-choice.md |
| Conclusion | ch05-context-engineering-and-planning-choice.md |

## Source Map: Chapter 6, Knowledge and Memory

| Chapter section | Reference file |
|---|---|
| Chapter introduction (knowledge vs memory, LangGraph framing) | ch06-context-and-keyword-memory.md |
| Foundational Approaches to Memory | ch06-context-and-keyword-memory.md |
| Managing Context Windows | ch06-context-and-keyword-memory.md (budgeting also in scripts/context_budget.py) |
| Traditional Full-Text Search | ch06-context-and-keyword-memory.md |
| Semantic Memory and Vector Stores | ch06-semantic-memory-and-rag.md |
| Introduction to Semantic Search | ch06-semantic-memory-and-rag.md |
| Implementing Semantic Memory with Vector Stores | ch06-semantic-memory-and-rag.md |
| Retrieval-Augmented Generation | ch06-semantic-memory-and-rag.md |
| Semantic Experience Memory | ch06-semantic-memory-and-rag.md |
| GraphRAG | ch06-graphrag-and-knowledge-graphs.md |
| Using Knowledge Graphs | ch06-graphrag-and-knowledge-graphs.md |
| Building Knowledge Graphs | ch06-graphrag-and-knowledge-graphs.md |
| Promise and Peril of Dynamic Knowledge Graphs | ch06-long-context-and-dynamic-graphs.md |
| Note-Taking | ch06-semantic-memory-and-rag.md |
| Conclusion | ch06-long-context-and-dynamic-graphs.md (escalation ladder) |

## Source Map: Chapter 7, Learning in Agentic Systems

| Chapter section | Covered in |
|---|---|
| Chapter introduction (nonparametric vs parametric learning) | ch07-nonparametric-learning.md (Framing); ch07-fine-tuning-decisions.md (Parametric learning in one paragraph) |
| Nonparametric Learning | ch07-nonparametric-learning.md |
| Nonparametric Exemplar Learning | ch07-nonparametric-learning.md (Exemplar learning) |
| Reflexion | ch07-nonparametric-learning.md (Reflexion) |
| Experiential Learning | ch07-nonparametric-learning.md (Experiential learning) |
| Parametric Learning: Fine-Tuning | ch07-fine-tuning-decisions.md |
| Fine-Tuning Large Foundation Models | ch07-fine-tuning-decisions.md (Go / no-go checklist; Method menu; Costs and payoffs) |
| The Promise of Small Models | ch07-fine-tuning-decisions.md (The case for small models; Picking a model size) |
| Supervised Fine-Tuning | ch07-sft-dpo-rlvr-playbook.md (SFT for function calling) |
| Direct Preference Optimization | ch07-sft-dpo-rlvr-playbook.md (DPO for output quality) |
| Reinforcement Learning with Verifiable Rewards | ch07-sft-dpo-rlvr-playbook.md (RLVR for any measurable reward) |
| Conclusion | ch07-sft-dpo-rlvr-playbook.md (Combining nonparametric and parametric learning) |

## Source Map: Chapter 8 headings to reference files

| Chapter section | Covered in |
|---|---|
| (Chapter introduction) | ch08-agent-count-and-decomposition.md (sections 1, 4) |
| How Many Agents Do I Need? | ch08-agent-count-and-decomposition.md (sections 1 to 3) |
| Single-Agent Scenarios | ch08-agent-count-and-decomposition.md (sections 1 to 3) |
| Multiagent Scenarios | ch08-agent-count-and-decomposition.md (sections 4 to 6) |
| Swarms | ch08-agent-count-and-decomposition.md (section 7) |
| Principles for Adding Agents | ch08-agent-count-and-decomposition.md (section 8) |
| Multiagent Coordination | ch08-coordination-strategies.md (section 1) |
| Democratic Coordination | ch08-coordination-strategies.md (section 2) |
| Manager Coordination | ch08-coordination-strategies.md (section 3) |
| Hierarchical Coordination | ch08-coordination-strategies.md (section 4) |
| Actor-Critic Approaches | ch08-coordination-strategies.md (section 6); scripts/topology_overhead.py actor-critic |
| Automated Design of Agent Systems | ch08-coordination-strategies.md (section 7) |
| Communication Techniques | ch08-communication-infrastructure.md (section 1) |
| Local Versus Distributed Communication | ch08-communication-infrastructure.md (section 2) |
| Agent-to-Agent Protocol | ch08-communication-infrastructure.md (section 3) |
| Message Brokers and Event Buses | ch08-communication-infrastructure.md (section 4) |
| Actor Frameworks: Ray, Orleans, and Akka | ch08-communication-infrastructure.md (section 5) |
| Orchestration and Workflow Engines | ch08-communication-infrastructure.md (section 6) |
| Managing State and Persistence | ch08-state-and-persistence.md |
| Conclusion | ch08-communication-infrastructure.md (section 7); ch08-coordination-strategies.md (section 5) |

## Source Map: Chapter 9, Validation and Measurement

| Chapter section | Covered in |
|---|---|
| (Chapter introduction) | [ch09-metrics-and-evaluation-sets.md](ch09-metrics-and-evaluation-sets.md) |
| Measuring Agentic Systems | [ch09-metrics-and-evaluation-sets.md](ch09-metrics-and-evaluation-sets.md) |
| Measurement Is the Keystone | [ch09-metrics-and-evaluation-sets.md](ch09-metrics-and-evaluation-sets.md) |
| Integrating Evaluation into the Development Lifecycle | [ch09-metrics-and-evaluation-sets.md](ch09-metrics-and-evaluation-sets.md) |
| Creating and Scaling Evaluation Sets | [ch09-metrics-and-evaluation-sets.md](ch09-metrics-and-evaluation-sets.md) |
| Component Evaluation | [ch09-component-testing.md](ch09-component-testing.md) |
| Evaluating Tools | [ch09-component-testing.md](ch09-component-testing.md) |
| Evaluating Planning | [ch09-component-testing.md](ch09-component-testing.md) |
| Evaluating Memory | [ch09-component-testing.md](ch09-component-testing.md) |
| Evaluating Learning | [ch09-component-testing.md](ch09-component-testing.md) |
| Holistic Evaluation | [ch09-system-level-evaluation.md](ch09-system-level-evaluation.md) |
| Performance in End-to-End Scenarios | [ch09-system-level-evaluation.md](ch09-system-level-evaluation.md) |
| Consistency | [ch09-system-level-evaluation.md](ch09-system-level-evaluation.md) |
| Coherence | [ch09-system-level-evaluation.md](ch09-system-level-evaluation.md) |
| Hallucination | [ch09-system-level-evaluation.md](ch09-system-level-evaluation.md) |
| Handling Unexpected Inputs | [ch09-system-level-evaluation.md](ch09-system-level-evaluation.md) |
| Preparing for Deployment | [ch09-deployment-readiness.md](ch09-deployment-readiness.md) |
| Conclusion | [ch09-deployment-readiness.md](ch09-deployment-readiness.md) |

The planning, end-to-end and deployment metrics are computable with [../scripts/agent_eval_report.py](../scripts/agent_eval_report.py).

## Source Map: Chapter 10, Monitoring in Production

| Chapter section | Covered in |
|---|---|
| Chapter introduction (open source reference stack) | ch10-stack-instrumentation-and-alerting.md |
| Monitoring Is How You Learn | ch10-failure-triage-and-metrics.md |
| (failure vs. expected variation decision tree) | ch10-failure-triage-and-metrics.md |
| (metric taxonomy, Table 10-1) | ch10-failure-triage-and-metrics.md |
| (privacy, RBAC, PII scrubbing) | ch10-failure-triage-and-metrics.md |
| Monitoring Stacks | ch10-stack-instrumentation-and-alerting.md |
| Grafana with OpenTelemetry, Loki, and Tempo | ch10-stack-instrumentation-and-alerting.md |
| ELK Stack (Elasticsearch, Logstash/Fluentd, Kibana) | ch10-stack-instrumentation-and-alerting.md |
| Arize Phoenix | ch10-stack-instrumentation-and-alerting.md |
| SigNoz | ch10-stack-instrumentation-and-alerting.md |
| Langfuse | ch10-stack-instrumentation-and-alerting.md |
| Choosing the Right Stack | ch10-stack-instrumentation-and-alerting.md |
| OTel Instrumentation | ch10-stack-instrumentation-and-alerting.md |
| Visualization and Alerting | ch10-stack-instrumentation-and-alerting.md |
| Monitoring Patterns | ch10-release-patterns-and-feedback.md |
| Shadow Mode | ch10-release-patterns-and-feedback.md |
| Canary Deployments | ch10-release-patterns-and-feedback.md |
| Regression Trace Collection | ch10-release-patterns-and-feedback.md |
| Self-Healing Agents | ch10-release-patterns-and-feedback.md |
| User Feedback as an Observability Signal | ch10-release-patterns-and-feedback.md |
| Distribution Shifts | ch10-drift-detection.md |
| Metric Ownership and Cross-Functional Governance | ch10-metric-ownership-governance.md |
| Conclusion | SKILL.md (purpose and key decision rules) |

## Source Map: Chapter 11, Improvement Loops

Chapter section headings mapped to the reference file that covers each.

| Chapter section | Reference file |
|---|---|
| Chapter introduction (RL analogy, three pillars, organizational alignment, overview table) | ch11-feedback-pipelines-and-diagnosis.md (The improvement loop as a whole); ch11-continuous-learning.md (Choosing the mechanism) |
| Feedback Pipelines | ch11-feedback-pipelines-and-diagnosis.md |
| Feedback Pipelines: DSPy, Trace, APO and the running SOC agent example | ch11-feedback-pipelines-and-diagnosis.md (Optimizer frameworks) |
| Automated Issue Detection and Root Cause Analysis | ch11-feedback-pipelines-and-diagnosis.md |
| Human-in-the-Loop Review | ch11-feedback-pipelines-and-diagnosis.md; scripts/escalation_tuner.py |
| Prompt and Tool Refinement | ch11-refinement-and-prioritization.md |
| Prompt refinement | ch11-refinement-and-prioritization.md |
| Tool Refinement | ch11-refinement-and-prioritization.md |
| Aggregating and Prioritizing Improvements | ch11-refinement-and-prioritization.md |
| Experimentation | ch11-experimentation-and-rollouts.md |
| Shadow Deployments | ch11-experimentation-and-rollouts.md |
| A/B Testing | ch11-experimentation-and-rollouts.md; scripts/ab_test_analyzer.py |
| Bayesian Bandits | ch11-experimentation-and-rollouts.md; scripts/bandit_allocator.py |
| Continuous Learning | ch11-continuous-learning.md |
| In-Context Learning | ch11-continuous-learning.md |
| Offline Retraining | ch11-continuous-learning.md |
| Conclusion | ch11-continuous-learning.md (Integrating the whole cycle) |

## Source Map: Chapter 12, Protecting Agentic Systems

| Chapter section | Covered in |
|---|---|
| Chapter introduction (incidents and statistics) | ch12-agent-risks-and-threat-vectors.md |
| The Unique Risks of Agentic Systems | ch12-agent-risks-and-threat-vectors.md |
| (HITL vulnerabilities and red team training tools, Table 12-1) | ch12-agent-risks-and-threat-vectors.md |
| Emerging Threat Vectors (Table 12-2) | ch12-agent-risks-and-threat-vectors.md |
| Securing Foundation Models (model selection) | ch12-model-selection-defenses-red-teaming.md |
| Defensive Techniques (incl. PINT and BIPIA benchmarks) | ch12-model-selection-defenses-red-teaming.md |
| Red Teaming (lifecycle, Figure 12-1, DeepTeam, Garak, PyRIT) | ch12-model-selection-defenses-red-teaming.md |
| Threat Modeling with MAESTRO (Figure 12-2, Table 12-3) | ch12-maestro-threat-modeling.md |
| Protecting Data in Agentic Systems | ch12-data-protection.md |
| Data Privacy and Encryption | ch12-data-protection.md |
| Data Provenance and Integrity | ch12-data-protection.md |
| Handling Sensitive Data | ch12-data-protection.md |
| Securing Agents | ch12-agent-safeguards-and-resilience.md |
| Safeguards | ch12-agent-safeguards-and-resilience.md; scripts/audit_tool_manifest.py |
| Protections from External Threats (Figure 12-3, DMZ) | ch12-agent-safeguards-and-resilience.md |
| Protections from Internal Failures (KPIs, chaos engineering) | ch12-agent-safeguards-and-resilience.md; scripts/check_agent_kpis.py |
| Conclusion | SKILL.md (decision rules and workflow) |

## Source Map: Chapter 13 Headings to Reference Files

| Chapter section | Covered in |
|---|---|
| Chapter introduction (calibrating autonomy, progressive delegation) | SKILL.md; ch13-trust-accountability-and-escalation.md |
| Roles and Autonomy | ch13-roles-adoption-and-scaling.md |
| The Changing Role of Humans in Agent Systems | ch13-roles-adoption-and-scaling.md |
| Aligning Stakeholders and Driving Adoption | ch13-roles-adoption-and-scaling.md |
| Scaling Collaboration | ch13-roles-adoption-and-scaling.md |
| Agent Scope and Organizational Roles | ch13-scope-access-and-memory.md |
| Shared Memory and Context Boundaries | ch13-scope-access-and-memory.md |
| Trust, Governance, and Compliance | ch13-trust-accountability-and-escalation.md |
| The Lifecycle of Trust | ch13-trust-accountability-and-escalation.md |
| Accountability Frameworks | ch13-trust-accountability-and-escalation.md |
| Escalation Design and Oversight | ch13-trust-accountability-and-escalation.md |
| Privacy and Regulatory Compliance | ch13-compliance-and-next-steps.md |
| Conclusion: The Future of Human-Agent Teams | ch13-compliance-and-next-steps.md |
