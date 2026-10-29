# Trends and Prerequisites for Choosing a Style

Two concerns come before any style comparison: understanding why the industry's preferred styles keep moving, and confirming you know enough about the situation to choose at all.

## Why architecture "fashion" moves

Popular styles change for identifiable reasons. When someone proposes a style because "everyone is doing it", trace which driver produced the trend and whether that driver applies to the current system.

| Driver | What it means | Question to ask |
|---|---|---|
| Lessons from earlier systems | New styles are usually reactions to the pain of previous ones (for example, the industry swung away from architectures built around maximal code reuse once the coupling cost became obvious). | Which past pain does this style fix, and do we actually have that pain? |
| Ecosystem churn | Tools and platforms appear and fade unpredictably; today's standard orchestration platform may be displaced by something not yet written. | Are we coupling the design to a tool, or to a durable idea? |
| New capabilities | Sometimes a capability changes the paradigm rather than swapping a tool (containerization reshaped deployment, tooling and practice). Even a small feature that lines up exactly with your goals can be decisive. | Does a new capability remove a constraint that previously ruled a style out? |
| Accelerating change | Each new tool spawns new practices, which spawn new designs; generative AI is a current example of fast, hard-to-predict shift. | How reversible is the decision if the landscape moves again in two years? |
| Domain change | Businesses evolve, merge and split, so the problem itself shifts. | Is the domain stable enough to justify a rigid structure? |
| Technology change | Organizations adopt technology that has clear financial upside. | Is there a bottom-line reason, or only enthusiasm? |
| External factors | Forces outside engineering, such as a sharp licensing price increase, can force migration even when the team is content. | Which vendors or contracts could force our hand? |

Guidance: stay current on trends so following or ignoring them is a conscious choice. An organization can lag or lead fashion; what matters is that each exception is reasoned.

## Prerequisite knowledge before choosing

An architect designs two things at once: the domain as specified, and the structural support that lets the system succeed (expressed as architecture characteristics). Do not pick a style until each factor below is understood well enough. When acting as an agent, treat any unknown factor as an explicit assumption in the output.

### 1. The domain
- You need broad understanding, not expert depth. Focus on aspects that drive operational characteristics (peak loads, timing, failure impact).
- Fill gaps with business analysts or subject matter experts.
- Probe: what business events cause load spikes? Which workflows are long-running or multi-step?

### 2. Structural architecture characteristics
- Run an architecture characteristics analysis; it is the core input to style selection.
- Generic styles can serve nearly any domain. What really distinguishes them is how well each supports particular characteristics, which is why style comparisons are framed by characteristics rather than by business area.
- Exception: domains with unusual operational demands (an auction site needing huge bursts of scale) do constrain the style directly.
- Probe: which characteristics differ between parts of the system?

### 3. Data architecture
- Collaborate with data specialists on schemas and stores.
- Watch especially for an existing or legacy data architecture the new system must integrate with; it can constrain partitioning and service boundaries.
- Probe: is there a shared database we cannot split? Who owns which data today?

### 4. Cloud deployment
- On-prem and cloud designs involve different trade-offs.
- Know data volume and how much data will move between zones or services, because data transfer can be a major cost.
- Capabilities that once needed rare skills (high elasticity on-prem) are now cloud configuration settings; re-check old assumptions about what is "hard".
- Probe: what are storage and egress costs at expected volume?

### 5. Organizational factors
- Cost of a specific cloud vendor can rule out an otherwise ideal design.
- Expected mergers and acquisitions favor open standards and integration-oriented architectures.
- Probe: what business events in the next few years could reshape the system's boundaries?

### 6. Process, teams and operations
- Consider the development process, whether architects and operations actually collaborate, and how QA works.
- Styles that rely on mature engineering practice (microservices depends heavily on Agile engineering, automation and DevOps maturity) will struggle where that maturity is missing.
- Probe: how often do teams deploy today? Is testing automated? Who runs production?

## Readiness checklist

- [ ] Major domain workflows and their operational stresses are known.
- [ ] Characteristics analysis exists, with variance across parts flagged.
- [ ] Existing data stores and integration constraints are listed.
- [ ] Deployment target and data movement costs are estimated.
- [ ] Budget, vendor, and M&A considerations are captured.
- [ ] Team and process maturity is honestly assessed.

If more than one box is empty, report that the choice is provisional and list what would firm it up.
