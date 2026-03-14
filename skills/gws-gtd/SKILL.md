---
name: gws-gtd
---

## Purpose

Use this skill for the opinionated `gws-gtd` workflow.

This package treats GTD conventions and Google Workspace operations as one integrated operating model. The vault is the task system of record. Gmail is the capture/intake layer. Calendar is a signal/review layer.

## Canonical References

- Conventions: `references/conventions.md`
- Email triage policy: `references/email-triage-policy.md`
- Templates: `System/Templates/`
- Queries: `System/Queries/`

## Supported Modes

- `daily`
- `weekly`
- `monthly`
- `organizing`
- `daily-intake`
- `weekly-reconcile`
- `event-capture`
- `people-linking`
- `signal-sync`
- `ad-hoc-maintenance`

## Router

1. Resolve the user intent.
2. Use the matching reference:
   - `daily` -> `../gtd-getting-things-done/references/daily.md`
   - `weekly` -> `../gtd-getting-things-done/references/weekly.md`
   - `monthly` -> `../gtd-getting-things-done/references/monthly.md`
   - `organizing` -> `../gtd-getting-things-done/references/organizing.md`
   - `daily-intake` -> `../gws-gtd-operations/references/daily-intake.md`
   - `weekly-reconcile` -> `../gws-gtd-operations/references/weekly-reconcile.md`
   - `event-capture` -> `../gws-gtd-operations/references/event-capture.md`
   - `people-linking` -> `../gws-gtd-operations/references/people-linking.md`
   - `signal-sync` -> `../gws-gtd-operations/references/signal-sync.md`
   - `ad-hoc-maintenance` -> `../gws-gtd-operations/references/command-reference.md`
3. Apply `references/conventions.md` and `references/email-triage-policy.md` as the fixed workflow contract.

## Guardrails

- Preserve canonical actionable syntax: `- [ ] #task ...`
- Keep one canonical task line per commitment.
- Treat `#inbox` as queue state across the vault.
- Treat `GTD Signals` as output-only.
- Gmail is the only supported mobile capture inbox.
- Do not use Google Tasks as a parallel capture system.
- Do not invent deadlines.
- Do not auto-complete tasks.
- Prefer minimal, reversible edits.
