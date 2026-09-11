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

### Phase: APPLY (after explicit "aprovo")

Apply the approved items from `selected_items`, step by step:

1. **Lock**: create `bmk.lock` in the workspace (refuse if another run is active).
2. **Backup**: copy destination state (`memories/`, configs) before touching anything; record backup path in checkpoint.
3. **Create profiles**: `hermes profile create <name> --no-skills` — **the `--no-skills` flag is MANDATORY on every profile the kit creates** (positive selection only; creating without it seeds the full bundled catalog, which violates acceptance criterion #4). Never use `--clone`/`--clone-all`. Install each approved skill individually afterwards.
4. **Idempotency check per step**: before each action, verify the destination already exists. If it does, record the step as done and continue — never blindly re-create.
5. **Write atomically**: persist intent to checkpoint BEFORE the action; record verified result AFTER.
6. **Inventory comparison**: after all steps, compare final inventory against `selected_items`. Divergence = verification failure.
7. **No secrets**: creation steps never carry credential values.

Then VERIFY: run the acceptance tests (see `templates/acceptance-tests.md`). Only after verification report the bot as ready.

### Phase: VERIFY

Run the acceptance checklist from the plan on the real destination. Each test result goes to `verification_results` in the checkpoint. Any failure → `BLOCKED` with the reason. Success requires all tests passing on the **actual** destination/surface — a plausible output is not a test.

## Checkpoint

The checkpoint file (`checkpoint.json` in the workspace) is the source of truth for resumption. It must survive session interruption and allow continuing without the chat transcript.

**Path is MANDATORY: `<HERMES_HOME>/bmk-backups/checkpoint.json`** (resolved from the `HERMES_HOME` env var at run time). The skill directory and container-ephemeral paths (`/opt/data`, `/tmp`) are FORBIDDEN — they vanish between runs and the checkpoint is then lost (observed in sandbox test 2026-09-11: durable backup stayed empty because the skill wrote to `/opt/data`). Every checkpoint write goes to this path; the durable copy is written on every phase transition, not only at the end.

Fields: `schema_version`, `kit_version`, `run_id`, `phase`, `host_id`, `profile_id`, `workspace`, `session_id`, `approved_scope`, `selected_items`, `completed_steps`, `blocked_reason`, `next_step`, `current_query`, `current_response`, `interview_answers`, `updated_at`.

## References

- `references/consent-and-discovery.md` — multi-host consent protocol
- `references/selection-and-safety.md` — skill/tool/MCP selection and safety
- `references/memory-migration.md` — memory audit and migration
- `references/secrets-and-privileges.md` — secrets and sudo
- `references/canonical-knowledge.md` — Obsidian vault topology
- `references/resume-protocol.md` — checkpoint and resumption