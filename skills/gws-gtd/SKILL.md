---
name: gws-gtd
description: Use when running GTD ceremonies (daily, weekly, monthly), processing Gmail inbox, organizing the vault, capturing calendar events, linking contacts, or syncing tasks to Google Calendar.
---

# gws-gtd

## Purpose

Unified skill for the opinionated `gws-gtd` workflow. Combines GTD vault conventions and Google Workspace operations into one integrated operating model.

- The vault is the task system of record.
- Gmail is the capture/intake layer.
- Calendar is a signal/review layer.

## Prerequisites

The `gws` binary must be on `PATH` and authenticated with the scopes needed for the requested Gmail, Calendar, or People operation.

Do not install or load separate generated `gws-*` skills for core GTD ceremonies. Use `references/command-reference.md` as the canonical Gmail, Calendar, People, and shared Google Workspace command surface.

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
   - `ad-hoc-maintenance` -> `references/daily-intake.md`, `references/weekly-reconcile.md`, `references/people-linking.md`, or `references/event-capture.md` depending on the surface involved
   - `assistant`          -> `references/assistant.md`
3. Always apply `references/conventions.md` and `references/email-triage-policy.md` as the fixed workflow contract.
4. Apply `references/canonical-vault.md` for vault structure and task syntax rules.
5. For Gmail, Calendar, People, and shared Google Workspace work, use `references/command-reference.md` first. Prefer the documented helper commands and API call patterns over ad-hoc `gws` invocations.

## Guardrails

- Apply `references/conventions.md` and `references/canonical-vault.md` as the fixed contract.
- Prefer minimal, reversible edits.
- Always pass `--format json` to every `gws` command so output is structured JSON, not a human-readable table.
- Always use `jq` to process JSON output from `gws` commands in Bash tool calls. Never use Python (`python3 -c`, inline scripts, etc.) for JSON parsing or field extraction.
- **Interactive decisions:** Always use the `AskUserQuestion` tool when the user must make a choice during any ceremony step. Never ask decisions as plain text. Include relevant clickable URLs (Gmail thread, calendar event, project note) in option descriptions.

## References

| Reference | Purpose |
|---|---|
| `references/conventions.md` | Fixed workflow conventions and label model |
| `references/email-triage-policy.md` | Gmail label meanings, classification defaults, heuristics |
| `references/canonical-vault.md` | Vault folder semantics, task syntax, link rules |
| `references/project-structure.md` | Project/design note layout and Google Docs metadata |
| `references/command-reference.md` | Canonical `gws` command surface for Gmail, Calendar, People, and shared rules |
| `references/daily.md` | Daily GTD ceremony |
| `references/weekly.md` | Weekly GTD review |
| `references/monthly.md` | Monthly GTD review |
| `references/organizing.md` | Vault organization and cleanup |
| `references/daily-intake.md` | Gmail and calendar intake during daily ceremony |
| `references/weekly-reconcile.md` | Gmail and calendar reconciliation during weekly review |
| `references/event-capture.md` | Event context capture procedure |
| `references/people-linking.md` | Google Contacts to People/ note linking |
| `references/signal-sync.md` | GTD Signals calendar sync procedure |
| `references/assistant.md` | Persistent GTD assistant warm-start and orchestration |

## Scripts

- `scripts/sync_gtd_signals.py` — syncs clarified dated tasks to the `GTD Signals` Google Calendar. See `references/signal-sync.md` for usage.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Parsing `gws` JSON output with Python | Use `jq` in Bash tool calls — never `python3 -c` |
| Asking decisions as plain text | Use `AskUserQuestion` with clickable URLs for every user choice |
| Running `gws` without `--format json` | Always pass `--format json` so output is structured |
| Calling generated `gws-*` skills for Gmail/Calendar | Use `references/command-reference.md`; it is the maintained command surface |
