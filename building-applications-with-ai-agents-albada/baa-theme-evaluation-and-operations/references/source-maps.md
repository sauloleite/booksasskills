# Source maps: book sections to reference files

File names below are the chapter-prefixed names used in this folder.

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
