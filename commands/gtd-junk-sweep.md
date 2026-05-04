---
description: Trash obvious Gmail junk per email-triage-policy; leaves ambiguous mail for the next daily ceremony.
agent: gtd-junk-sweep
subtask: true
---

Run a narrow Gmail inbox sweep — trash obvious garbage only.

Scope and notes: $ARGUMENTS

Follow `AGENTS.md` and `gws-gtd` in `gmail-intake` mode, Step 1 garbage-only classification. Delegate gws fetch + batch-trash calls to `gtd-gws-fetch` (Haiku). Confirm the trash batch via AskUserQuestion before mutating.

Do NOT create tasks, import, forward, unsubscribe, or classify ambiguous mail. Defer those for daily.

Typical invocation via loop: `/loop 2h /gtd-junk-sweep`.

Output: `{trashed: N, deferred_for_daily: N}` plus a one-line JSONL append to `System/.gtd-coach-state.jsonl`.
