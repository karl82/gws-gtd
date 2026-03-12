---
name: gtd-getting-things-done
---

## Purpose

Use this skill to run GTD workflows in a vault that follows the canonical `gws-gtd` model.

## Supported Modes

- `daily`
- `weekly`
- `monthly`
- `organizing`
- `project-structure`

## Router

1. Resolve the ceremony intent.
2. Use the matching reference:
   - `daily` -> `references/daily.md`
   - `weekly` -> `references/weekly.md`
   - `monthly` -> `references/monthly.md`
   - `organizing` -> `references/organizing.md`
   - `project-structure` -> `references/project-structure.md`
3. Follow `references/canonical-vault.md` and installed runtime files under `System/` at all times.

## Runtime Contract

- `System/GTD Config.md`
- `System/Templates/`
- `System/Queries/`

## Guardrails

- Preserve canonical actionable syntax: `- [ ] #task ...`
- Keep one canonical task line per commitment.
- Treat inbox as tag-driven via `#inbox`.
- Use full vault-relative links for canonical entities under `Projects/`, `Areas/`, and `People/`.
- Do not invent deadlines.
- Do not auto-complete tasks.
- Prefer minimal, reversible edits.

## Supporting References

- Canonical vault rules: `references/canonical-vault.md`
