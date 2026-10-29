# Team Topologies and Moving On to Specific Styles

Covers the chapter's team-type section (from Skelton and Pais, *Team Topologies*, 2019) and its closing guidance on learning styles by their sweet spots.

## The four team types and what they mean for architecture

| Team type | Purpose | Architectural implication |
|---|---|---|
| Stream-aligned | Owns one flow of work tied to a business domain or capability (a product, service, or feature set) and aims to deliver value as fast as possible. | Wants domain-partitioned boundaries it can change and deploy without waiting on others. Every other team type exists to remove its friction. |
| Enabling | Fills a capability gap: research, learning, and specialist knowledge that matters but is not urgent. Collaborative and proactive. | Helps stream teams adopt new practices (for example, observability or contract testing) without owning their code. |
| Complicated-subsystem | Holds deep expertise in a hard, specialized part of the system and helps stream teams use it. | Justifies a separate component with a stable, narrow interface so stream teams carry less cognitive load. |
| Platform | Offers internal services and building blocks as a self-service product (Evan Bottcher's framing) so delivery teams move faster with less coordination. | Owns cross-cutting infrastructure and governance (quality, security) exposed through self-service APIs; must avoid becoming a ticket queue. |

## How to apply

- Start from the stream-aligned teams and their domains; the top-level partitioning should let each one change its area independently. This is the Inverse Conway Maneuver in practice.
- When a technical concern keeps blocking several stream teams, decide whether it is a platform capability (self-service, broadly used), a complicated subsystem (narrow, deep expertise), or a temporary skills gap (enabling team).
- Distributed styles raise platform demands sharply: deployment automation, observability, and security per endpoint usually need a platform team, or stream teams absorb that load themselves.
- When evaluating any style in later chapters, ask which team types it favors and what it demands from the platform.

## Learning styles by sweet spot

Trade-off analysis requires knowing several styles first. Each style is strongest for a particular set of architecture characteristics; learning the philosophy behind each tells the architect where it fits best, or where it is the least bad option. Agent rule: never recommend a style without naming the characteristics it serves well and the ones it sacrifices for this specific problem.

## Review questions (original)

1. Which stream-aligned teams exist or are planned, and does each map to one top-level component?
2. Which shared concerns currently block more than one stream team, and which team type should own each?
3. Does the proposed style need platform capabilities the organization does not yet have?
4. Which characteristics drive this system, and which candidate styles have those as strengths?
