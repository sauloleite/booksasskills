# Memory Systems for RAG and Agents

## Contents
- Why memory matters for RAG and agents
- The three memory mechanisms
- Placement rule: frequency of use
- Benefits of an external memory system
- Memory management vs memory retrieval
- Context budget split and overflow
- Eviction and compression strategies
- Handling contradictions
- Design playbook
- Worked example: a coaching assistant

## Why memory matters for RAG and agents

Memory is any mechanism that lets a model keep and reuse information. RAG depends on it for augmented context that can grow over turns as more is retrieved. Agents must keep far more: their instructions and examples, the tools on offer, the current plan, every tool result, and their own reflections. Both regularly exceed the context limit, which is why the chapter ends with memory. Any application that must retain information benefits, not just these two.

## The three memory mechanisms

| Mechanism | Where it lives | Persistence | Access | How it changes |
|---|---|---|---|---|
| Internal knowledge | Model weights | Permanent until the model is retrained or finetuned | Available in every query | Only by updating the model |
| Short-term memory | The context window (e.g. earlier messages of this conversation) | Does not persist across tasks or queries | Fast | Limited by maximum context length |
| Long-term memory | External stores reached through retrieval (as in RAG) | Persists across tasks | Requires a retrieval step | Can be edited or deleted without touching the model |

## Placement rule: frequency of use

Decide where a piece of information lives by how often it is needed:
- Needed for essentially every task: bake into internal knowledge via training or finetuning.
- Rarely needed: long-term memory.
- Immediately relevant to the current task: short-term memory (context).

## Benefits of an external memory system

1. **In-session overflow**: excess from long tasks goes to long-term storage.
2. **Cross-session persistence**: an assistant that forgets history and preferences is tiresome; remembered history enables personalization.
3. **Consistency**: recalling earlier answers to subjective questions (rate this pitch 1 to 10) keeps later answers calibrated.
4. **Structural integrity**: text context flattens structure, and a table fed line by line may not be read as a table. Store structured objects as such: a spreadsheet of leads, a queue of pending actions.

## Memory management vs memory retrieval

A memory system does two things:
- **Memory management**: deciding what goes into short-term vs long-term memory (add and delete operations).
- **Memory retrieval**: fetching task-relevant items from long-term memory. This is essentially RAG retrieval against an external store, so all retrieval guidance (lexical, semantic, hybrid, reranking) applies.

Deletion is often unnecessary for long-term memory because external storage is cheap and expandable. Short-term memory is bounded by context length, so it always needs an add/remove policy.

## Context budget split and overflow

Per query, the model's context holds both short-term memory and items retrieved from long-term memory. So the short-term capacity is whatever is left after reserving room for retrieved memory.

- Example from the chapter: reserve 30% of the context for retrieved long-term items, leaving at most 70% for short-term memory.
- When short-term usage hits its threshold, move the overflow into long-term memory.
- Arithmetic (own example): a 128k-token window, 8k reserved for system prompt and tools, 25% of the remaining 120k (30k) reserved for retrieval, leaves 90k for conversation history; once history crosses 90k, archive the oldest or least important turns into the long-term store.

## Eviction and compression strategies

Memory management borrows from decades of data-system practice. Options, roughly from simple to sophisticated:

1. **FIFO**: the oldest items leave first. API providers may drop the beginning of long conversations; frameworks such as LangChain can keep only the last N messages or N tokens.
   - Hidden assumption: early messages matter least. Often false, since opening turns frequently state the conversation's purpose (though with human small talk, openers may be mere pleasantries).
2. **Summarization**: language is redundant, so compression shrinks memory a lot. Summarize with the same or another model and add **named-entity tracking**; this goes a long way.
3. **Summary plus recovered details** (Bae et al., 2022): build new memory by joining the summary with key facts the summary dropped. A classifier looks at each sentence of the old memory and each sentence of the summary and decides whether to keep one, both or neither.
4. **Reflection-based updates** (Liu et al., 2023): after every action, the agent reflects on the newly generated information and decides whether to *insert* it, *merge* it with existing memory, or *replace* something, especially stale information it contradicts.

Not recommended without instrumentation: **usage-based eviction** (least frequently used). It requires knowing when the model actually used a memory item, which is hard to observe.

## Handling contradictions

Three policies, pick per use case:
- Keep the newest item.
- Ask a model to judge which to keep.
- Keep both. Contradictions can confuse an agent, but they can also offer multiple perspectives when that is valuable (for example differing expert opinions).

Rule of thumb: for facts that genuinely change over time (address, plan tier, preferences), newest wins; for opinions or disputed claims, keeping both with provenance may be better.

## Design playbook

1. Place information by frequency of need (weights, long-term, short-term).
2. Budget the context: fixed reserve for instructions and tools, a share for retrieved memory, the rest for short-term.
3. Pin goal-defining messages so eviction never removes them.
4. Evict by summarization plus entity tracking; add reflection-based insert/merge/replace for long-running agents.
5. Keep structured state in structured stores; define a contradiction policy; evaluate memory retrieval like RAG.

## Worked example: a coaching assistant

Invented: a fitness coaching app with weekly check-ins. The coaching method is finetuned in (needed every time); injuries, goals and progress live as structured long-term records plus session summaries; this week's chat is short-term, with 20% of context reserved for retrieved records. An entity tracker keeps injuries, dates and numbers verbatim through summarization. "Running 3x per week" (March) vs "stopped running" (May): newest wins for the current routine, both kept for trends. FIFO would have dropped an opening message about a knee injury and produced an unsafe plan; pinning constraint messages prevents it.
