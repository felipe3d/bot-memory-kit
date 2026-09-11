---
name: bot-memory-kit
description: "Use when the user explicitly asks to set up bots and memory with the Bot Memory Kit. Conducts an interview, plans bot architecture, and deploys with approval gates. Does NOT trigger on casual mentions of memory or bots."
version: 0.1.0
author: fac
license: MIT
metadata:
  hermes:
    tags: [memory, bots, profiles, setup, planning]
    related_skills: [hermes-agent, hermes-memory-systems, hermes-profile-management]
---

# Bot Memory Kit

Kit replicável para descobrir necessidades, planejar e implantar bots e memória no Hermes Agent.

## When to Use

- User says "iniciar bot-memory-kit", "retomar bot-memory-kit", or "consultar bot-memory-kit"
- User explicitly asks to set up the Bot Memory Kit
- User wants to plan and deploy Hermes bots with isolated memory, skills, and secrets

## When NOT to Use

- Casual mentions of "memory", "bots", or "profiles" without the explicit trigger
- General questions about how Hermes memory works
- Routine profile management without the kit workflow

## Explicit Triggers

The kit only starts when the user says one of:
- **"iniciar bot-memory-kit"** — start a new deployment from scratch
- **"retomar bot-memory-kit"** — resume an interrupted deployment
- **"consultar bot-memory-kit"** — check status of a deployment

Any other mention of memory, bots, or profiles does NOT start the kit. Respond normally.

## Workflow

```
INTENT → INTERVIEW → SCOPE_APPROVED → CONSENT_PER_HOST → DISCOVERY
  → SELECTION → ARCHITECTURE → PLAN_READY
  → WAITING_IMPLEMENTATION_APPROVAL → APPLY → VERIFY → COMPLETE
```

### Phase: INTERVIEW

Conduct an adaptive interview about the user's work, personal life, hobbies, routines, information sources, privacy, and autonomy. Save progress to `checkpoint.json` in the workspace directory after every question and answer.

**Rules:**
1. Ask ONE question at a time. Wait for the answer before proceeding.
2. After each answer, save the question, answer, and current state to `checkpoint.json`.
3. Skip questions already answered when resuming.
4. Never persist secrets, credentials, or sensitive values — only references.
5. The interview covers 5 blocks (see `templates/interview.md`):
   - Block 1: Life and responsibilities
   - Block 2: Routines and difficulties
   - Block 3: Information and tools
   - Block 4: Autonomy, audience, and privacy
   - Block 5: Desired experience
6. After the last question, synthesize a diagnosis and transition to SCOPE_APPROVED.

### Phase: MODEL_GATE

Before any phase that modifies the environment (APPLY), check the active model:
- Read `model.default` from config.
- If the model is a Flash variant or otherwise below the recommended tier for APPLY, warn the user.
- Recommend alternatives (see `references/selection-and-safety.md`).
- Never proceed to APPLY without explicit human approval of the diffs.

## Checkpoint

The checkpoint file (`checkpoint.json` in the workspace) is the source of truth for resumption. It must survive session interruption and allow continuing without the chat transcript.

Fields: `schema_version`, `kit_version`, `run_id`, `phase`, `host_id`, `profile_id`, `workspace`, `session_id`, `approved_scope`, `selected_items`, `completed_steps`, `blocked_reason`, `next_step`, `current_query`, `current_response`, `interview_answers`, `updated_at`.

## References

- `references/consent-and-discovery.md` — multi-host consent protocol
- `references/selection-and-safety.md` — skill/tool/MCP selection and safety
- `references/memory-migration.md` — memory audit and migration
- `references/secrets-and-privileges.md` — secrets and sudo
- `references/canonical-knowledge.md` — Obsidian vault topology
- `references/resume-protocol.md` — checkpoint and resumption