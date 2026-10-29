# Technical Breadth, Learning Habits and the Personal Radar

## Contents

- Depth versus breadth
- The knowledge pyramid
- Two dysfunctions and the Frozen Caveman antipattern
- The 20-minute rule
- Building a personal technology radar
- Glossary
- Review questions (original)

## Depth versus breadth

Developers succeed through depth: deep command of a language, framework, platform or product. Architects succeed through breadth: shallow but wide awareness of many options. The reason is the job itself. An architect matches capabilities to technical constraints, so knowing that several viable solutions exist for a problem beats being an expert in only one. Many people moving from developer to architect find this shift uncomfortable because it asks them to let hard-won expertise shrink.

## The knowledge pyramid

Picture all technical knowledge as a pyramid in three bands:

1. **Known (top, smallest).** Tools and technologies you use daily and are good at. Small because no one can master everything. This is your depth, and it decays: expertise left untouched for a year or two goes stale, so keeping it costs ongoing time.
2. **Known unknowns (middle, larger).** Things you have heard of and could describe but cannot use proficiently (for example, knowing a language is a Lisp dialect without being able to write it).
3. **Unknown unknowns (bottom, largest).** Technologies that might perfectly solve your problem if only you knew they existed.

Career moves:

- Promote items from unknown unknowns to known unknowns (awareness).
- When a need arises, promote from known unknowns to known (expertise).

For an architect, the top and middle bands matter most, and breadth is measured by how far the middle band reaches into the bottom one. The healthy architect profile is a wider middle and a somewhat narrower top, keeping a few areas of depth (often the enjoyable ones) and letting others fade on purpose.

## Two dysfunctions and the Frozen Caveman antipattern

**Dysfunction 1: chasing expertise everywhere.** The architect tries to stay expert in many areas, achieves it in none, and burns out.

**Dysfunction 2: stale expertise.** Outdated knowledge feels current. Common when founding developers rise into leadership and keep deciding with criteria from years ago.

**Frozen Caveman antipattern.** An antipattern looks sensible at first and then causes trouble. Here, an architect who was burned once by a rare failure raises that same fear against every new design. In the chapter's anecdote, client architects kept asking about losing connectivity to one country's stores after a single freak outage years earlier, even though recurrence was very unlikely.

How an agent should respond when it sees this pattern:

- Acknowledge the past incident; do not dismiss it.
- Separate real risk from perceived risk: estimate likelihood and impact with current data.
- Ask whether the concern maps to a business driver today.
- If the risk is real but rare, propose a proportionate mitigation rather than reshaping the whole architecture around it.

## The 20-minute rule

Spend at least 20 minutes every day learning something new or going deeper on a topic. Good sources include the Thoughtworks Technology Radar, InfoQ and DZone Refcardz; looking up unfamiliar buzzwords is a cheap way to turn unknown unknowns into known unknowns.

Timing matters. Lunch and evening slots tend to fail (lunch turns into catch-up work; evenings fill with family and social life). The authors recommend the first thing in the morning, with a coffee or tea, before opening email, because once email starts the day is effectively taken over.

Agent guidance: when someone asks how to keep up, propose a concrete daily morning slot, a short rotating source list, and a way to log what moved between pyramid bands.

## Building a personal technology radar

**Why.** Technologists who invest heavily in one technology live in a self-reinforcing bubble where everyone shares the same enthusiasm, outside criticism rarely gets in, and collapse comes without warning (the chapter's example: a DOS-era development platform whose market vanished abruptly when Windows took over). A radar is a living document for weighing the risks and rewards of current and emerging technologies so that does not happen to you.

**Origin.** Thoughtworks' Technology Advisory Board, a group of senior technologists advising the CTO, publishes a Technology Radar twice a year. Many organizations and individuals copied the idea.

**Quadrants** (Thoughtworks layout): tools; languages and frameworks; techniques (processes, engineering practices, advice); platforms (databases, cloud vendors, operating systems). You may relabel quadrants for personal use.

**Rings, outer to inner, with personal meanings:**

| Ring | Organizational meaning (paraphrased) | Personal use |
|---|---|---|
| Hold | Do not start new work with it; existing use is fine | Things to avoid, including low-value habits (for example, time sunk in gossip forums) |
| Assess | Worth exploring via spikes, research, talks | Promising items you have heard about but not yet checked; staging area for research |
| Trial | Worth pursuing; pilot a low-risk project | Active hands-on experiments, deep enough to use in trade-off analysis |
| Adopt | Recommended for broad use | What excites you most and your proven go-to solutions |

**Portfolio thinking.** Treat skills like an investment portfolio and diversify. Hold some widely demanded, stable skills and track their demand; place a few speculative bets (the chapter mentions generative AI and embedded IoT as examples). Weigh opposing criteria such as a large job market for established tech versus more interesting but scarcer roles. Avoid letting your employer's current stack or fashion choose your portfolio for you.

**The exercise matters more than the picture.** The real value is the scheduled thinking and the conversations the radar triggers. For visualization, Thoughtworks offers Build Your Own Radar, which renders a radar from a spreadsheet.

### Minimal radar entry format (original)

```yaml
- name: vector-database-x
  quadrant: platforms
  ring: assess
  why: candidate for semantic search; heard strong reports
  next_step: spike against current search index, 2 hours
  reviewed: 2026-10
```

Review the radar on a fixed cadence (for example quarterly) and move items between rings with a one-line reason.

## Glossary

- **Technical depth:** how much you know about one topic.
- **Technical breadth:** how many topics you know enough about to recognize as options.
- **Blip:** one item plotted on a radar.
- **Memetic bubble:** an echo chamber around one technology that filters out honest outside assessment.

## Review questions (original)

1. Which two items in your current stack would you move to Hold, and what replaces them?
2. Name a problem you solved last quarter; list three alternatives you did not consider at the time.
3. Which of your expert areas would you deliberately let fade to gain breadth?
4. What recurring fear in your team's design reviews might be a Frozen Caveman concern?
