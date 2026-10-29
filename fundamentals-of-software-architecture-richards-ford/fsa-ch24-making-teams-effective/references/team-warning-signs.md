# Team Warning Signs: When a Team Is Too Big

Bigger teams need more architect involvement, but past some point size itself makes the team less effective. The chapter gives three observable signals that a team has grown too large. An effective architect watches for them as part of keeping the team healthy, not just technically on track.

## 1. Process loss

Origin: Fred Brooks, *The Mythical Man-Month*. Adding people to a project tends to lengthen it (Brooks's Law). A team's potential productivity is the combined effort of all members; actual productivity always falls short of it. The gap is process loss.

Observable symptoms:
- Frequent merge conflicts, a sign that people are editing the same code and stepping on each other.
- Work items blocked on other people's in-progress changes.
- Coordination meetings growing faster than delivered output.

Response playbook:
1. Look for natural parallelism: separate services, modules, or areas of the application that people can own independently.
2. When a project manager proposes adding someone, first ask: is there a distinct workstream this person can own?
3. If there is, carve it out before they arrive.
4. If there is not, tell the project manager explicitly that the addition is likely to slow the team down.

Context number (standard formula, not from this chapter): a team of n people has n(n-1)/2 pairwise communication channels, so going from 6 to 12 people raises channels from 15 to 66. `scripts/involvement_score.py --team-size N` prints this count.

## 2. Pluralistic ignorance

Definition: each person privately rejects an idea but goes along with it publicly, assuming everyone else sees something they are missing. The fable of the emperor's new clothes is the classic illustration.

Invented example: a team converges on a shared database between two services for convenience. One developer knows the two services have different data retention obligations, which makes sharing a compliance problem, but stays quiet because everyone else seems sure. In a group of four they would likely have raised it; in a group of fifteen they did not. Larger groups make people less willing to challenge the room.

Response playbook (the architect as facilitator):
- In meetings, watch faces and body language for masked doubt.
- Invite the likely skeptic by name to give their view of the proposal.
- Back them up for speaking, even if their objection turns out to be wrong. The goal is a room where dissent feels safe, not winning the specific point.
- Agent addition: suggest lightweight anonymous or written-first input (for example, everyone writes concerns before discussion) when the group is large.

## 3. Diffusion of responsibility

Definition: as a group grows, each member assumes someone else is handling a problem, so nobody does. The roadside analogy: a stranded driver on a quiet rural road will likely get help from the first passerby; on a crowded city highway, thousands may drive past, each assuming help is already coming.

Observable symptoms:
- Confusion about who owns what.
- Tasks, bugs, follow-ups or alerts falling through the cracks.
- "I thought you were doing that" in retrospectives.

Response: treat these as evidence that the team is too large; split ownership more explicitly or split the team. Clear single-owner assignment for each area is the immediate mitigation.

## Using the three signals together

| Signal | What to observe | Primary fix |
|---|---|---|
| Process loss | Merge conflicts, collisions, coordination overhead | Create parallel workstreams; resist additions without one |
| Pluralistic ignorance | Silent agreement, hidden skepticism | Facilitate dissent; protect people who speak up |
| Diffusion of responsibility | Dropped work, unclear ownership | Explicit owners; smaller teams |

Two or more signals at once is a strong case for splitting the team. Any of them also feeds back into the involvement score: a struggling large team warrants more architect presence.
