# How Learning Works: Memory, Insight and Skill Stages

Covers the chapter opening, the shiny-new-thing sidebar, "Cramming Doesn't Work" and "Skills Acquisition".

## Contents
- Why learning is part of the job
- Encoding versus cramming
- Forgetting and spaced repetition
- Getting unstuck: focused and diffuse modes
- Skill-stage models (Shu Ha Ri, Imitate/Assimilate/Innovate, Dreyfus)
- Learning a framework: the typical arc
- Agent playbook and pitfalls
- Glossary

## Why learning is part of the job

Writing code is only part of what an engineer is paid for; the larger part is thinking, and thinking runs on knowledge that has to be refreshed as the field turns over. The authors rank the ability to absorb something new quickly, and then apply it to a real problem, as arguably the single most important trait of a successful engineer. A useful loop: watch someone do it, do it yourself, then teach it.

**The shiny-new-thing paradox.** Engineers gravitate to novelty, and launch-time buzz creates a feeling of falling behind. Yet early versions are usually rough; the moment the excitement fades is often the moment the technology becomes worth adopting. Another wave will always arrive soon, so missing the first one is cheap.

## Encoding versus cramming

Cramming can carry you through an exam but rarely leaves anything behind. For knowledge to persist it has to be encoded: elaborated, tied to meaning, and placed in a context. Narrative is the oldest encoding tool. "Be careful with forced recursive deletes" is easy to forget; a colleague's account of erasing their own laptop while debugging a cleanup script is not.

Agent implications:
- When teaching a concept, attach a concrete incident, a consequence, or a "why it exists" story, not just a rule.
- Ask the learner to connect the new idea to something they already know (an analogy to a tool they use daily).
- Prefer a small real task that uses the concept over a summary of it.

## Forgetting and spaced repetition

Forgetting is a feature: the brain discards what it judges unused. Some memories persist for decades while others vanish within minutes, and the rate differs by person and by fact, but decay follows a predictable shape. Hermann Ebbinghaus (1880s) showed that much of newly learned material is lost within the first half hour, and that repeated exposure flattens the curve. Spaced repetition exploits this: review just before the material would be lost, then lengthen the gap each time.

Tools range from paper flash cards to apps that schedule prompts and add gamification (a common route to learning human languages). The skill's script `scripts/spaced_review_schedule.py` generates expanding review dates.

Practical rules:
- Turn each key concept into a question you must answer from memory (active recall), not a passage to reread.
- First review within a day, then stretch: a few days, a week, two weeks, a month, two months.
- If recall fails, restart that item's schedule from a short gap.
- Mix spacing with application: answering a card is good, using the idea in code is better.

## Getting unstuck: focused and diffuse modes

The chapter uses the L-mode / R-mode framing (popularized by Andy Hunt's "Pragmatic Thinking and Learning"):
- **L-mode**: verbal, analytical, linear, deliberate. It is what you use while staring at a stack trace.
- **R-mode**: nonverbal, associative search and retrieval, running in the background and not under conscious control. It is why a forgotten name surfaces minutes after you stop trying.

Because R-mode cannot be forced, grinding harder on a stuck problem often fails. The move is to load the problem fully, then occupy L-mode with something routine (a walk, a shower, cooking, tidying) and let the background process work.

Agent playbook for a stuck developer:
1. Have them write down the problem, what they tried, and what they expected (this loads it properly).
2. Suggest a deliberate break of 15 to 30 minutes doing something mundane.
3. On return, ask what came to mind before resuming analysis.
4. If they are on a deadline, a smaller break (stand up, get water) still helps more than another hour of the same approach.

## Skill-stage models

Several models describe the same progression from rule following to intuition.

**Shu Ha Ri** (martial arts; Bruce Lee's phrasing is roughly: learn, follow, then transcend the principle) and **Imitate, Assimilate, Innovate** (jazz trumpeter Clark Terry):
| Stage | What the learner does | What helps |
|---|---|---|
| Shu / Imitate | Replicates the teacher exactly, little concern for theory | One trusted source, exact steps |
| Ha / Assimilate | Has the basics in muscle memory; adds theory, seeks other teachers | Multiple sources, explanations of why |
| Ri / Innovate | Learns from their own practice; forges their own path | Freedom, hard problems, peers |

**Dreyfus model** (five stages, progressive):
| Stage | Signature behaviour | Software example |
|---|---|---|
| Novice | Needs context-free recipes | Follows the Getting Started guide line by line |
| Advanced Beginner | Starts deviating from rules to see what happens | Tweaks tutorial code, changes configs |
| Competent | Can troubleshoot; diagnoses own mistakes from outcomes | Traces a failing request to a misconfigured bean or middleware |
| Proficient | Self-corrects without external feedback | Notices a design smell while writing it and rewrites |
| Expert | Works from intuition; struggles to explain how | Sketches the right architecture immediately; reasons are reconstructed afterward |

Key implications:
- Rules and recipes are essential to novices and stifling to experts. Telling a beginner to "just use your judgment" fails; forcing a checklist on an expert wastes their intuition.
- No amount of watching or reading replaces practice at any stage.
- Reaching expert takes a long time, which is why most people plateau at advanced beginner. Given how fast tools change, that is normal: a career has deep expertise in a few areas and advanced-beginner competence in many.

## Learning a framework: the typical arc

1. Start with the smallest possible example (hello world, the to-do app), not a complex system.
2. Copy code from tutorials; lean on search or a chatbot to decode errors.
3. Patterns emerge; you can locate a fault from the error message alone.
4. You discover the framework's boundaries and the parts you would redesign.
5. Near mastery you stop translating intent into framework idioms and simply express intent through it; you "see" the solution on reading the task.

## Agent playbook and pitfalls

- Diagnose stage before advising. Signals: does the person need exact steps, or do they push back on steps and ask why?
- For novices: give one path, exact commands, and a runnable result fast. Avoid presenting five alternatives.
- For competent and above: offer trade-offs and principles, let them choose.
- Pitfall: equating hours of video with skill. Always pair consumption with a build exercise.
- Pitfall: rereading as review. Replace with recall questions on a spaced schedule.
- Pitfall: treating forgetting as failure. It is expected; schedule for it.

## Glossary

- **Encoding**: the process of making information memorable by elaborating it and connecting it to meaning and context.
- **Spaced repetition**: reviewing at gradually lengthening intervals to interrupt the forgetting curve.
- **L-mode / R-mode**: shorthand for focused, linear analysis versus background, associative retrieval.
- **Dreyfus model**: five-stage skill model from Novice to Expert.
