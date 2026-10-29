# Building a Learning Habit and Cadence

Covers "The Learning Habit", the technology merry-go-round sidebar, "Learning Through AI", "Practice Grace", "Wrapping Up", "Putting It into Practice" and "Additional Resources".

## Contents
- Core stance
- Learning depth levels
- Cadence across the year
- Protecting the time
- Learning out loud
- Learning with AI
- Grace and sustainability
- Practice plan
- Worked example
- Further reading

## Core stance

Expertise takes years, technology moves faster, and learning time is scarce. The goal is not to master everything but to spend limited hours well. Keep a written list of topics for the next few months, ranked, and expect it to change as interests shift. Constant reinvention is energizing but tiring; one author's early manager left engineering for management partly to step off the endless cycle of new languages, frameworks and datastores. Acknowledge that cost openly when coaching someone.

## Learning depth levels

Christopher Judd's Learning Depth Strategy assigns effort per topic instead of treating every topic the same:

| Level | Typical activities | Use when |
|---|---|---|
| Survey | Podcasts, user group or conference sessions, keynotes, release notes | You want awareness of what exists |
| Shallow dive | Short videos, blog posts, articles, tutorials | You may use it soon or need to talk about it |
| Deep dive | Live workshops or courses, books | It is central to your work or a strong interest |
| Ultra deep dive | Presenting on it, leading a workshop or class | You want mastery or to become the go-to person |

Decision rule: most topics should stay at survey. Promote a topic only when there is a concrete need or durable interest. Teaching is the deepest level because explaining exposes gaps.

## Cadence across the year

Learning has to be continuous because memory decays (see how-learning-works.md for spacing). A balanced yearly mix:

- **Weekly**: a podcast episode, one or two videos, one or two articles.
- **Monthly**: a technical or business book, a meetup or user group, an online course.
- **Yearly**: a conference, a new programming language, a side project, a certification, a talk you give.

Many small regular sessions are more sustainable, and stick better, than a single weekend marathon.

## Protecting the time

- Put recurring learning blocks on the calendar. Meetings will sometimes overwrite them; reschedule rather than drop. You are the only reliable guardian of this time.
- Pick a slot that is quiet for you (Friday afternoons are often calm, but a Tuesday morning or Thursday lunch may suit better).
- Some people map a year of topics on a kanban board or seed calendar reminders. Experiment; the format matters less than having dedicated blocks.
- **Morning coffee**: spend the first 15 to 30 minutes of the workday on learning (news, a podcast, a tutorial, an early-release book) before incidents and meetings consume the day. On chaotic days it guarantees at least one productive outcome.

## Learning out loud

- Share progress publicly (social posts, a blog, short videos). A supportive community often forms around it.
- Document what you figured out. Engineers regularly search a question and land on their own forgotten write-up.
- Pair or form a small study group on a shared project; even one extra reviewer helps.
- Host the project in a public repository or open-source it to invite comments.
- Live streaming is intimidating but brings advice from people who hit the same walls, and the reassurance that you are not learning alone.

## Learning with AI

Chatbots accelerate study: they explain an unfamiliar class or API, summarize a reference model (for example the OSI layers), and propose tailored learning paths in conversational form. Guardrails:

- Treat answers as a starting point; confirm against official docs or source code, because models hallucinate.
- Ask for explanations at your Dreyfus stage ("explain as to a beginner", or "assume I know X; compare to Y").
- Use AI to generate recall questions for spaced review, then answer them without AI.
- AI cannot substitute for hands-on practice; always follow an explanation with an exercise.

Example prompt pattern (original):
```
I know <familiar tech>. Explain <new concept> by contrast with it.
Then give me 5 recall questions and one 30-minute exercise.
Cite the official documentation sections I should verify against.
```

## Grace and sustainability

- Keeping up is a real part of the job, but the industry is too broad to cover; trying to do so leads to burnout.
- Learning should be enjoyable. Never trade sleep, mental health or physical health for it.
- Waiting until the last responsible moment is valid. Hype cycles resolve; many hot tools are abandoned within months. If something proves durable, you can pick it up later at no penalty.

## Practice plan

An agent can turn the chapter's closing advice into this loop:

1. **Find a vehicle.** Build a small personal app that scratches a real itch (a collection tracker, a stats app for a kid's team). No itch? Offer help to a school or nonprofit; they often allow wide freedom in technology choice.
2. **Pick a topic that energizes you.** Scan what the field is excited about; if none of it appeals, choose something that does.
3. **Immerse.** Follow practitioners, subscribe to podcasts, newsletters and streams, find a local user group, a focused conference or a virtual event.
4. **Produce working code** over days or weeks. It can be inelegant and skip edge cases; it only has to prove the technology. There is no shortcut that loads knowledge directly.
5. **Teach it** to colleagues, a user group or a conference.
6. **Reassess every month or two.** Still excited? Continue. If not, switch. Returning to an earlier topic later is cheap; prior knowledge carries over and expands.

## Worked example

A backend developer wants to stay current while shipping features.
- List (next 3 months): event streaming (deep dive, team need), Rust (shallow dive, curiosity), WebAssembly (survey).
- Calendar: 20 minutes each morning; Thursday lunch for a course module.
- Weekly: one streaming podcast, one article on Rust.
- Monthly: one chapter-a-week book on streaming with two colleagues; one meetup.
- Project: a small consumer that ingests home sensor data, in a public repo with a short write-up per milestone.
- Review: spaced recall of ten core streaming concepts using the skill's script.
- Month-two check: Rust interest fading, swap it for observability tooling; WebAssembly stays at survey.

## Further reading

- "Thinking Architecturally" (Schutta)
- The Pragmatic Programmer (Hunt, Thomas)
- The Passionate Programmer (Fowler)
- Thoughtworks Technology Radar
- The First 20 Hours (Kaufman)
- Pragmatic Thinking and Learning (Hunt)
