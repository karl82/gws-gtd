This vault uses the `gws-gtd` package as its opinionated GTD + Google Workspace operating model.

Source of truth:

- Unified workflow skill lives in `skills/gws-gtd/`.
- Google Docs review-sync skill lives in `skills/gws-doc-review-sync/`.
- transcrypt utility skill lives in `skills/transcrypt-git-repo/`.
- GTD ceremony agents live in `agents/`.
- Analyze and retrofit commands live in `commands/`.
- Vault runtime files live in `System/`.

Core runtime assets:

- `System/Templates/`
- `System/Queries/`

Local vault notes should keep only truly local overrides or migration notes. Do not redefine GTD or GWS workflow rules here when the package already defines them.
