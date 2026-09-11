# AgentLibrarian

AgentLibrarian is a universal retrieval and reuse agent for AI systems.

Its purpose is simple:

> AgentVallet remembers what happened. AgentLibrarian decides what past knowledge is useful now.

AgentLibrarian does **not** execute the main business task. It understands the incoming task, searches AgentVallet, ranks relevant memories and skills, resolves conflicts, compresses context, and returns a small universal Agent Knowledge Packet (AKP) that any working agent can consume.

## Core flow

```text
User / Manager Agent
        |
        v
AgentLibrarian
        |
        +--> Understand task
        +--> Build search queries
        +--> Search AgentVallet
        +--> Rank candidates
        +--> Apply trust + conflict rules
        +--> Compress context
        v
Agent Knowledge Packet (AKP)
        |
        v
Hermes / Codex / Claude / Prime / Exo / Any Agent
```

## First-principles MVP

The first version only needs to do six things:

1. Understand a task.
2. Search AgentVallet.
3. Retrieve relevant skills, rules, corrections, validations and prior work.
4. Rank the candidates.
5. Build a minimal context package.
6. Return it to the working agent.

## Trust order

```text
Human Approved
> Validated Skill
> Repeated Successful Pattern
> Single Successful Run
> Raw Observation
> LLM Suggestion
```

## Universal Agent Knowledge Packet

```json
{
  "task": {},
  "recommended_skill": {},
  "rules": [],
  "corrections": [],
  "known_failures": [],
  "required_tools": [],
  "validation": [],
  "confidence": 0,
  "source_ids": []
}
```

## Design rules

- AgentVallet remains the single source of truth.
- AgentLibrarian must not create a second memory system.
- Retrieval should be hybrid: metadata + keyword + semantic + trust filtering.
- Raw logs should not be sent to a model by default.
- Deterministic code should handle trust, status, version and approval rules.
- LLMs should be used only where interpretation or semantic understanding is useful.
- If there is no reliable match, return `NO_RELIABLE_MATCH` instead of guessing.
- Any model or agent should be replaceable without changing stored experience.

## Repository layout

```text
src/agent_librarian/
  core/
  retrieval/
  ranking/
  context/
  adapters/
  schemas/
  api/

tests/
docs/
examples/
```

## Development milestones

### Milestone A — Retrieve
Task -> AgentVallet search -> top relevant results.

### Milestone B — Rank
Add trust, similarity, recency, validation and compatibility scoring.

### Milestone C — Package
Return a compact Agent Knowledge Packet instead of raw history.

### Milestone D — Universal
Prove the same packet can be consumed by at least two different working agents.

## Success metrics

- Top-1 retrieval accuracy
- Correction recall
- Context/token reduction
- Task success improvement
- Repeat-error reduction
- Skill reuse rate

## Phase 1 relationship

```text
AgentVallet
= RECORD + STORE + LEARN

AgentLibrarian
= SEARCH + RANK + SELECT + PACKAGE

Working Agent
= EXECUTE
```

This repository is the second half of the universal Knowledge & Skills layer.