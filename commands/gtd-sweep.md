---
description: Narrow Gmail inbox junk-only sweep. Trashes obvious garbage; defers everything actionable to the daily ceremony.
agent: gtd
subtask: true
---

Run a Gmail inbox junk-only sweep.

Scope and notes: $ARGUMENTS

Follow `reference.md § Junk sweep`. Garbage-only — don't apply `gtd/*` labels, don't create vault tasks, don't forward, don't unsubscribe. Defer ambiguous mail for the next daily ceremony.

For ongoing maintenance, invoke via `/loop 2h /gtd-sweep`.

Output: `{trashed: N, deferred_for_daily: N}`.
