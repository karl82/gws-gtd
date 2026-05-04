This vault uses the `gws-gtd` package as its opinionated GTD + Google Workspace operating model.

Source of truth:

- Unified workflow skill lives in `skills/gws-gtd/`.
- Google Docs review-sync skill lives in `skills/gws-doc-review-sync/`.
- transcrypt utility skill lives in `skills/transcrypt-git-repo/`.
- GTD ceremony and support agents live in `agents/` (11 agents: daily, weekly, monthly, organizing, assistant, signals, retrofit, junk-sweep, and three Haiku mechanical agents: gws-fetch, vault-scan, signal-diff).
- Slash commands live in `commands/`.
- Vault runtime files live in `System/`.

Core runtime assets:

- `System/Templates/`
- `System/Queries/`
- `System/.gtd-coach-state.jsonl` — append-only event log used by the coach persona (mechanics-only, never journaled). Fallback: vault-root `.gtd-coach-state.jsonl` if `System/` is absent.

Local vault notes should keep only vault-specific overrides or migration notes. Do not redefine GTD or GWS workflow rules here when the package already defines them.
