This vault uses the `gtd` package as its opinionated GTD + Google Workspace operating model.

Source of truth:

- Unified workflow skill lives in `skills/gtd/`.
- Google Docs review-sync skill lives in `skills/gws-doc-review-sync/`.
- transcrypt utility skill lives in `skills/transcrypt-git-repo/`.
- The single GTD agent lives in `agents/gtd.md`.
- Slash commands live in `commands/` (`gtd`, `gtd-sweep`, `gtd-drain`).
- Vault runtime files live in `System/`.

Core runtime assets:

- `System/Templates/` — Daily, Weekly Review, Monthly Review, Project Template, Person, Design Note, Recruiter Decline Email
- `System/Queries/` — Dataview queries for tasks, projects, journals
- `System/.gtd-state.jsonl` — append-only sweep/drain event log (created on first sweep)

Local vault notes should keep only vault-specific overrides or migration notes. Do not redefine GTD rules here when the package already defines them in `skills/gtd/reference.md`.
