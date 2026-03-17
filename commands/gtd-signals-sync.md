---
description: Sync clarified dated vault tasks to the GTD Signals Google Calendar
agent: gtd-daily
subtask: true
---

Sync the `GTD Signals` Google Calendar from the vault.

Scope and notes: $ARGUMENTS

Requirements:
- Load the `gws-gtd` skill and use the `signal-sync` mode (`references/signal-sync.md`).
- Run the bundled `scripts/sync_gtd_signals.py` helper:
  - Dry-run first: `python3 "${CLAUDE_SKILL_DIR}/scripts/sync_gtd_signals.py"`
  - Show a concise diff (creates / updates / deletes) and ask for confirmation.
  - Apply after confirmation: `python3 "${CLAUDE_SKILL_DIR}/scripts/sync_gtd_signals.py" --apply`
- Source open `#next` and dated `#waiting` tasks from `Projects/` and `Areas/` only.
- Exclude `#inbox` tasks, completed tasks, `Archive/`, `Resources/`, and `System/`.
- Reconcile any mobile `✅` completions back to the vault before pushing changes.
- Report: counts of created / updated / deleted signals and any reconciled completions.
