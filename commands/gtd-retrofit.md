---
description: Retrofit the vault toward the canonical gws-gtd model; per-file confirmation required for moves.
agent: gtd-retrofit
subtask: true
---

Retrofit the current vault toward the canonical `gws-gtd` model.

Scope and notes: $ARGUMENTS

Follow `AGENTS.md` and `gws-gtd` in `project-retrofit` mode. Audit first (`vault-audit.md`), then execute migrations with per-file confirmation via AskUserQuestion.

Output per `project-retrofit.md § Output`:
- Counts per bucket.
- For each move/rename: source path, destination path, rationale.
- Link normalization actions.
- Google Docs matches: preserved, suggested, or left for user decision.
