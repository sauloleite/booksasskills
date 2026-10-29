# Source maps: book sections to reference files

File names below are the chapter-prefixed names used in this folder.

## Source Map: Chapter 1, What Happens When There Are No "Best Practices"?

| Chapter section | Covered in |
|---|---|
| Chapter introduction (no silver bullets, least worst) | [ch01-trade-off-mindset-and-decision-records.md](ch01-trade-off-mindset-and-decision-records.md) |
| Why "The Hard Parts"? | [ch01-trade-off-mindset-and-decision-records.md](ch01-trade-off-mindset-and-decision-records.md) |
| Giving Timeless Advice About Software Architecture | [ch01-trade-off-mindset-and-decision-records.md](ch01-trade-off-mindset-and-decision-records.md) |
| The Importance of Data in Architecture (operational vs analytical data) | [ch01-data-vocabulary-and-running-example.md](ch01-data-vocabulary-and-running-example.md) |
| Architecture Decision Records | [ch01-trade-off-mindset-and-decision-records.md](ch01-trade-off-mindset-and-decision-records.md) |
| Architecture Fitness Functions | [ch01-fitness-functions-governance.md](ch01-fitness-functions-governance.md) |
| Using Fitness Functions | [ch01-fitness-functions-governance.md](ch01-fitness-functions-governance.md) |
| The Equifax Data Breach (sidebar) | [ch01-fitness-functions-governance.md](ch01-fitness-functions-governance.md) |
| Architecture versus Design: Keeping Definitions Simple | [ch01-trade-off-mindset-and-decision-records.md](ch01-trade-off-mindset-and-decision-records.md) (why over how), [ch01-data-vocabulary-and-running-example.md](ch01-data-vocabulary-and-running-example.md) (definitions) |
| Introducing the Sysops Squad Saga | [ch01-data-vocabulary-and-running-example.md](ch01-data-vocabulary-and-running-example.md) |
| Non-Ticketing Workflow | [ch01-data-vocabulary-and-running-example.md](ch01-data-vocabulary-and-running-example.md) |
| Ticketing Workflow | [ch01-data-vocabulary-and-running-example.md](ch01-data-vocabulary-and-running-example.md) |
| A Bad Scenario | [ch01-data-vocabulary-and-running-example.md](ch01-data-vocabulary-and-running-example.md) |
| Sysops Squad Architectural Components | [ch01-data-vocabulary-and-running-example.md](ch01-data-vocabulary-and-running-example.md) |
| Sysops Squad Data Model | [ch01-data-vocabulary-and-running-example.md](ch01-data-vocabulary-and-running-example.md) |

## Source Map: Chapter 2, Discerning Coupling in Software Architecture

| Chapter section | Covered in |
|---|---|
| Part I. Pulling Things Apart (part opener: static vs dynamic coupling) | ch02-trade-off-analysis-framing.md |
| Chapter 2 opening (story setup, coupling definition, trade-off method, service size question) | ch02-trade-off-analysis-framing.md |
| Architecture (Quantum \| Quanta) | ch02-architecture-quantum-static-coupling.md |
| Independently Deployable | ch02-architecture-quantum-static-coupling.md |
| High Functional Cohesion | ch02-architecture-quantum-static-coupling.md |
| High Static Coupling | ch02-architecture-quantum-static-coupling.md |
| Sidebar: Service-Based Architecture | ch02-architecture-quantum-static-coupling.md |
| Dynamic Quantum Coupling | ch02-dynamic-coupling-dimensions.md |
| Communication | ch02-dynamic-coupling-dimensions.md |
| Consistency | ch02-dynamic-coupling-dimensions.md |
| Coordination | ch02-dynamic-coupling-dimensions.md |
| Sysops Squad Saga: Understanding Quanta | ch02-architecture-quantum-static-coupling.md (bootstrap test, quantum vs bounded context, static quantum diagram); ch02-dynamic-coupling-dimensions.md (runtime entanglement, elasticity) |

Script support: `scripts/quantum_coupling.py` implements the static quantum count, the per-call dynamic coordinates and runtime fusion by synchronous calls.

## Source Map: Chapter 15, Build Your Own Trade-Off Analysis

| Chapter section | Reference file |
|---|---|
| Chapter opening (Sysops Squad retrospective) | ch15-communicating-and-staying-objective.md |
| Introduction and the three-step process | ch15-three-step-analysis-process.md |
| Finding Entangled Dimensions | ch15-three-step-analysis-process.md |
| Coupling | ch15-three-step-analysis-process.md |
| Analyze Coupling Points | ch15-three-step-analysis-process.md |
| Assess Trade-Offs | ch15-three-step-analysis-process.md |
| Trade-Off Techniques | ch15-trade-off-techniques.md |
| Qualitative versus Quantative Analysis | ch15-trade-off-techniques.md |
| MECE Lists | ch15-trade-off-techniques.md |
| The "Out of Context" Trap | ch15-trade-off-techniques.md |
| Model Relevant Domain Cases | ch15-trade-off-techniques.md |
| Prefer Bottom Line over Overwhelming Evidence | ch15-communicating-and-staying-objective.md |
| Avoiding Snake Oil and Evangelism | ch15-communicating-and-staying-objective.md |
| Sysops Squad Saga: Epilog | ch15-communicating-and-staying-objective.md |
