---
description: Analyze the current vault against the canonical gws-gtd model (read-only audit).
agent: gtd-retrofit
subtask: true
---

Run a read-only audit of the vault against the canonical `gws-gtd` model.

Scope and notes: $ARGUMENTS

Follow `AGENTS.md` and `gws-gtd` in `vault-audit` mode. Read-only — do not move or rename files in this command. For retrofit execution, use `/gtd-retrofit`.

Output per `vault-audit.md § Output`:
- Counts per bucket (compatible, adaptable, conflicting, needs-decision).
- Missing files and mismatches.
- Recommended retrofit sequence.
- For each needs-decision item, surface via AskUserQuestion.
