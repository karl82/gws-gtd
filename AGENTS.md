This vault uses the `gws-gtd` package as its opinionated GTD + Google Workspace operating model.

Source of truth:

- GTD ceremony skill lives in `skills/gtd-getting-things-done/`.
- Google Workspace operations skill lives in `skills/gws-gtd-operations/`.
- Google Docs review-sync skill lives in `skills/gws-doc-review-sync/`.
- transcrypt utility skill lives in `skills/transcrypt-git-repo/`.
- Analyze and retrofit commands live in `commands/`.
- Vault runtime files live in `System/`.

Core runtime files:

- `System/GTD Config.md`
- `System/Email Triage Policy.md`
- `System/Templates/`
- `System/Queries/`

Local vault notes should keep only truly local overrides or migration notes. Do not redefine GTD or GWS workflow rules here when the package already defines them.
