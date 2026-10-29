# Use-Case Patterns: Where Foundation Models Earn Their Keep

Covers the chapter's survey of applications: how to categorize use cases, how to judge whether a task is a good AI candidate, enterprise risk preferences, and the eight recurring categories with what each reveals about AI's strengths and limits. Use it when brainstorming, prioritizing a backlog of ideas, or sanity-checking whether an idea matches a proven pattern.

## Contents
- Ways to slice the use-case space
- The exposure lens
- Enterprise risk preference: internal and close-ended first
- The eight categories at a glance
- Coding
- Image and video production
- Writing
- Education
- Conversational bots
- Information aggregation
- Data organization
- Workflow automation and agents
- Candidate screening checklist
- Worked examples
- Pitfalls

## Ways to slice the use-case space

No taxonomy is canonical; pick the one that fits the audience. Common alternatives: by function (customer experience, employee productivity, process optimization), by activity (programming, data analysis, research, support, design, art, copy), and by value captured (cost reduction, efficiency, growth, faster innovation, plus business continuity, the "adopt or die" bucket cited by 7% of about 2,500 executives in a 2023 survey). The book's eight product categories suit engineering and product design.

They come from interviews with about 50 companies, 100+ case studies, and 205 open source apps with at least 500 GitHub stars. Apps often span several categories (a companion bot that also aggregates news; a tool that extracts PDF fields and answers questions about the PDF). Low open source counts for education, writing and data organization reflect closed enterprise builds, not low demand.

## The exposure lens

A 2023 study defined a task as exposed when AI (or software built on it) can cut its completion time by at least 50%; an occupation's exposure is its share of exposed tasks. Near-fully exposed: interpreters and translators, tax preparers, web designers, writers, mathematicians, quantitative analysts. Unexposed: cooks, stonemasons, athletes.

Use it by decomposing a workflow into tasks and asking of each "could a model halve the time?". The study also ranks industries, useful when judging whether AI is an existential threat to a business.

## Enterprise risk preference: internal and close-ended first

Two observed tendencies:

1. **Internal before external.** Companies deploy internal tools (knowledge management) faster than customer-facing ones (support chatbots). Internal deployment builds team expertise while limiting exposure to privacy breaches, compliance problems and public catastrophic failures.
2. **Close-ended before open-ended.** Even though the models are open-ended, many shipped apps are classification-style. Fixed outputs are easier to evaluate, so risk is easier to quantify.

Recommendation pattern: for a risk-averse organization, sequence work as internal plus close-ended, then internal plus open-ended, then external.

## The eight categories at a glance

| Category | Consumer flavor | Enterprise flavor | Why AI fits |
|---|---|---|---|
| Coding | General coding help | Coding | Strong model skill; builders are coders |
| Image and video | Photo and video editing, design | Presentations, ad generation | Probabilistic variety is a feature |
| Writing | Email, social posts, blogs | Copywriting, SEO, reports, memos, design docs | High volume, tedious, mistakes are cheap |
| Education | Tutoring, essay grading | Onboarding, upskilling | Personalization at scale |
| Conversational bots | General chat, companions | Support, product copilots | Fast responses, guidance through hard tasks |
| Information aggregation | Summaries, talk-to-your-docs | Summaries, market research | Distillation is a core strength |
| Data organization | Image search, personal memory | Knowledge management, document processing | Turns unstructured into searchable |
| Workflow automation | Travel and event planning | Data extraction, entry, annotation, lead generation | End goal of automation; needs tools |

## Coding

- Most popular use case in surveys: models are good at code, and early AI engineers were coders. A code completion product passed $100M ARR about two years after launch.
- Specialized sub-tasks: pulling structured fields out of PDFs and web pages, natural language to SQL or dataframe code, screenshot or sketch to front-end code, cross-language or cross-framework migration, documentation, tests, commit messages.
- Measured gains (McKinsey): about 2x on documentation, 25 to 50% on generation and refactoring, little on highly complex tasks. Tool builders report front-end benefits more than back-end.
- Implication: teams do more with fewer engineers, and outsourcing (simpler, non-core work) is especially exposed. Evidence supports task-level augmentation that varies by complexity, not wholesale replacement either way.

## Image and video production

- Probabilistic generation suits creative work; leading startups scaled revenue very fast (one image generator near $200M ARR at about 18 months).
- Norms shift quickly: AI profile photos went from banned on a major platform (2019) to a built-in feature in many apps (2023).
- Ads and marketing adopted early because marketing budgets are large (around 11% of company budgets). Patterns: generate assets, draft for human experts, mass-produce A/B variants, localize by season or region.

## Writing

- Writing is frequent, tedious and error-tolerant: users simply ignore bad suggestions.
- Controlled evidence: in an MIT experiment with 453 professionals, those given ChatGPT finished about 40% faster with about 18% higher quality, the skill gap narrowed, and treated participants were 2x as likely to use it at work two weeks later (1.6x after two months).
- Consumer patterns: tone repair, bullets to prose, essays, genre fiction, reader-adaptive stories, children's stories built around words the child struggles with. Writing assistants finetune for fluency, coherence and clarity.
- Enterprise: sales and marketing copy, performance reviews, cold outreach, product descriptions, CRM-integrated content.
- SEO is a particular strength (web training data is full of SEO text), which also feeds junk content farms: a 2023 audit found ads from 141 major brands on AI junk sites, one publishing about 1,200 articles a day. Factor abuse into design.

## Education

- Students rely heavily on chat assistants; large school districts banned ChatGPT and reversed within months.
- Better framing is personalization: textbook summaries, per-student lesson plans, materials adapted to format and interests. A Duolingo study found lesson personalization benefits most of four course-creation stages; role-play suits language practice.
- Other patterns: quiz generation and grading, debate partners, student and teacher assistants, finding errors in AI-written essays.
- Disruption is real: a homework-help company's stock fell from about $28 to $2 between late 2022 and late 2024. The upside: AI as a tutor to bootstrap any skill.

## Conversational bots

- Versatile: lookup, explanation, brainstorming, companionship (which grew remarkably fast), persona emulation, even simulated societies for research.
- Enterprise: support bots cut cost and response time; product copilots guide users through insurance claims, taxes or policy lookups.
- Beyond text: voice assistants (incumbents moved slowly, plausibly due to higher quality and compliance bars) and 3D characters, including smart game NPCs that replace scripted dialogue.

## Information aggregation

- Mainstream: in a 2023 survey, 74% of generative AI users used it to distill and summarize.
- Consumer: talk-to-your-docs over contracts, disclosures and papers; research summaries.
- Enterprise: less middle-management relay. One company's most popular internal prompt template condensed meetings, email and chat into facts, open questions and action items that flowed into a tracker with owners. Also prospect and competitor research.

## Data organization

- Data volume (photos, logs, contracts, PDFs) keeps growing and is mostly unstructured or semistructured; value depends on searchability.
- Patterns: generate captions for images and video, match text queries to visuals, generate an image when none matches, write analysis code, find outliers, forecast.
- Enterprise extraction: simple (credit cards, licenses, receipts, tickets, contact details in email signatures) to complex (contracts, reports, charts). The intelligent document processing market was projected near $12.8B by 2030 at about 33% annual growth.

## Workflow automation and agents

- The end goal is automating as much as possible. Consumer: booking, refunds, trip planning, form filling. Enterprise: lead management, invoicing, reimbursements, request handling, data entry.
- Data synthesis is a notable pattern: models generate or label data that improves models, with humans in the loop to refine labels.
- Many tasks require external tools and permissions (search, phone, calendar). Systems that plan and call tools are agents. Interest is intense and partly justified by the potential productivity gains; design for permissions and tool access from the start.

## Candidate screening checklist

- [ ] Which categories does it touch, and does a model halve the time of most underlying tasks?
- [ ] How tolerant are users of mistakes?
- [ ] Internal or external, close-ended or open-ended, and what risk follows?
- [ ] Does published evidence show gains for this task type at this complexity?
- [ ] Does it need tools and permissions?
- [ ] What is the abuse potential, and could others' use of AI here disrupt your own business?

## Worked examples

**Ranking three ideas for an insurer.** (a) Internal claims-note summarizer: aggregation, internal, error-tolerant since adjusters review; start here. (b) Field extraction from claim forms: close-ended and measurable; second. (c) Customer-facing claims copilot: external and open-ended; schedule after (a) and (b) have built evaluation muscle.

**Coding assistant scope.** Target documentation and refactoring first (largest measured gains), keep humans on intricate cross-service changes, and expect better results on UI code than core back-end logic.

## Pitfalls

- Reading open source popularity as market demand.
- Choosing an external, open-ended first project in a risk-averse company.
- Assuming coding gains are uniform across task difficulty.
- Ignoring that your own business may be the one disrupted.
- Building tool-using automation without a permission model, or optimizing purely for content volume.
