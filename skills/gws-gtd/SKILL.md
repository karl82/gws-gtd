---
name: gws-gtd
---

## Purpose

Unified skill for the opinionated `gws-gtd` workflow. Combines GTD vault conventions and Google Workspace operations into one integrated operating model.

- The vault is the task system of record.
- Gmail is the capture/intake layer.
- Calendar is a signal/review layer.

## Prerequisites

The `gws` CLI must be installed and authenticated before running any ceremony:

```
gws auth status
```

Upstream `gws` AI agent skills (`gws-gmail`, `gws-calendar`, `gws-people`, etc.) are available separately via:

```
npx skills add https://github.com/googleworkspace/cli
```

These are optional supplements. The `references/command-reference.md` in this skill covers all `gws` commands needed for GTD ceremonies.

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
   - `daily`              -> `references/daily.md`
   - `weekly`             -> `references/weekly.md`
   - `monthly`            -> `references/monthly.md`
   - `organizing`         -> `references/organizing.md`
   - `daily-intake`       -> `references/daily-intake.md`
   - `weekly-reconcile`   -> `references/weekly-reconcile.md`
   - `event-capture`      -> `references/event-capture.md`
   - `people-linking`     -> `references/people-linking.md`
   - `signal-sync`        -> `references/signal-sync.md`
   - `ad-hoc-maintenance` -> `references/command-reference.md`
3. Always apply `references/conventions.md` and `references/email-triage-policy.md` as the fixed workflow contract.
4. Apply `references/canonical-vault.md` for vault structure and task syntax rules.

## Guardrails

- Apply `references/conventions.md` and `references/canonical-vault.md` as the fixed contract.
- Prefer minimal, reversible edits.

## References

| Reference | Purpose |
|---|---|
| `references/conventions.md` | Fixed workflow conventions and label model |
| `references/email-triage-policy.md` | Gmail label meanings, classification defaults, heuristics |
| `references/canonical-vault.md` | Vault folder semantics, task syntax, link rules |
| `references/project-structure.md` | Project/design note layout and Google Docs metadata |
| `references/daily.md` | Daily GTD ceremony |
| `references/weekly.md` | Weekly GTD review |
| `references/monthly.md` | Monthly GTD review |
| `references/organizing.md` | Vault organization and cleanup |
| `references/daily-intake.md` | Gmail and calendar intake during daily ceremony |
| `references/weekly-reconcile.md` | Gmail and calendar reconciliation during weekly review |
| `references/event-capture.md` | Event context capture procedure |
| `references/people-linking.md` | Google Contacts to People/ note linking |
| `references/signal-sync.md` | GTD Signals calendar sync procedure |
| `references/command-reference.md` | Full `gws` command reference for GTD ceremonies |

## Scripts

- `scripts/sync_gtd_signals.py` — syncs clarified dated tasks to the `GTD Signals` Google Calendar. See `references/signal-sync.md` for usage.
