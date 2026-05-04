---
name: gws-gtd
description: Use when running GTD ceremonies (daily, weekly, monthly, organizing), processing Gmail inbox, syncing the GTD Signals calendar, auditing or retrofitting a vault, operating the persistent assistant and coach, or invoking the 2h Gmail junk sweep.
---

# gws-gtd

## Purpose

Unified skill for the opinionated `gws-gtd` workflow. Combines GTD vault conventions and Google Workspace operations into one integrated operating model.

- The vault is the task system of record.
- Gmail is the capture/intake layer.
- Calendar is a signal/review layer.

## Prerequisites

The `gws` binary must be on `PATH` and authenticated with the scopes needed for the requested Gmail, Calendar, or People operation.

Do not install or load separate generated `gws-*` skills for core GTD ceremonies. Use the three `*-commands.md` references as the canonical `gws` command surface.

## Router

1. Resolve the user intent.
2. Route to the matching reference:

   | Intent | Reference |
   |---|---|
   | `daily` | `references/daily.md` |
   | `weekly` | `references/weekly.md` |
   | `monthly` | `references/monthly.md` |
   | `organizing` | `references/organizing.md` |
   | `gmail-intake` | `references/gmail-intake.md` |
   | `calendar-intake` | `references/calendar-intake.md` |
   | `appointment-triage` | `references/appointment-triage.md` |
   | `event-capture` | `references/event-capture.md` |
   | `people-linking` | `references/people-linking.md` |
   | `signal-sync` | `references/signal-sync.md` |
   | `project-retrofit` | `references/project-retrofit.md` |
   | `vault-audit` | `references/vault-audit.md` |
   | `assistant` | `references/assistant.md` |
   | `quick-tasks` | `references/quick-tasks.md` |
   | `coach` | `references/coach.md` |

3. Always-applied references (load unconditionally at ceremony start):
   - `references/conventions.md`
   - `references/canonical-vault.md`
   - `references/email-triage-policy.md`
   - `references/gmail-commands.md` (Gmail ops)
   - `references/calendar-commands.md` (Calendar ops)
   - `references/people-commands.md` (People ops)

## Guardrails

- Apply `references/conventions.md` and `references/canonical-vault.md` as the fixed contract.
- Prefer minimal, reversible edits.
- Always pass `--format json` to every `gws` command so output is structured JSON, not a human-readable table.
- Always use `jq` to process JSON output from `gws` commands in Bash tool calls. Never use Python (`python3 -c`, inline scripts, etc.) for JSON parsing or field extraction.
- **Interactive decisions:** Always use `AskUserQuestion` for user choices. See `conventions.md § Interactive Decisions`.

### Model Routing (skill-scoped override of the global Haiku ban)

The global rule "ALWAYS use opus / NEVER use haiku" applies to judgment and classification work. Within this skill it is explicitly overridden for three mechanical subagents that perform deterministic, no-judgment operations:

- `gtd-gws-fetch` — mechanical gws Gmail/Calendar/People fetches and pre-decided label mutations.
- `gtd-vault-scan` — vault counts, orphan detection, stalled-project mtime scans.
- `gtd-signal-diff` — `scripts/sync_gtd_signals.py --dry-run` wrapper.

These must be dispatched with `model: "haiku"`. All other subagent dispatches — including `gtd-daily`, `gtd-weekly`, `gtd-monthly`, `gtd-organizing`, `gtd-signals`, `gtd-retrofit`, `gtd-junk-sweep`, `gtd-assistant`, and any email-triage or GTD-clarify call — continue to use `opus` per the global rule.

**Guardrails for Haiku calls:**

- Structured JSON input, not free-form instructions.
- Documented output schema per op. Callers validate via `jq -e` or regex before acting.
- On validation failure: escalate the same op to self (Opus/Sonnet). Never retry Haiku.
- No free-form commentary in Haiku output — envelope only.
- No query-derived mutations. `batch_modify` and `threads_modify` require pre-resolved `ids`.
- **Do not use Haiku for email classification.** See `gmail-intake.md § Bulk Review Pattern`.

## References

| Reference | Purpose |
|---|---|
| `references/conventions.md` | Behavioral doctrine — anti-rules, journal hygiene, tag taxonomy, interactive decisions, stalled thresholds |
| `references/canonical-vault.md` | Structural model — task syntax, folder semantics, project model, linking, orphan tasks, journal paths |
| `references/email-triage-policy.md` | Gmail label contract, classification defaults, heuristics, capture setup |
| `references/gmail-commands.md` | Gmail `gws` API mechanics |
| `references/calendar-commands.md` | Calendar `gws` API mechanics |
| `references/people-commands.md` | People `gws` API mechanics |
| `references/daily.md` | Daily ceremony |
| `references/weekly.md` | Weekly review (absorbs former weekly-reconcile) |
| `references/monthly.md` | Monthly review |
| `references/organizing.md` | Organizing procedure |
| `references/gmail-intake.md` | Gmail classification, import, hygiene — used by daily and weekly |
| `references/calendar-intake.md` | Calendar ask queue — delegates to event-capture |
| `references/appointment-triage.md` | Appointment sub-procedure |
| `references/event-capture.md` | Per-event capture decision |
| `references/people-linking.md` | Google Contacts to People/ note linking |
| `references/signal-sync.md` | GTD Signals calendar sync procedure |
| `references/project-retrofit.md` | Vault migration and Google-Docs matching |
| `references/vault-audit.md` | Vault audit procedure |
| `references/assistant.md` | Persistent assistant warm-start + menu |
| `references/quick-tasks.md` | Inline quick-task handlers |
| `references/coach.md` | Proactive ambient coach — rhythm, nudges, JSONL state |
| `references/opkg.md` | Package lifecycle (opkg save/install/list) |

## Scripts

- `scripts/sync_gtd_signals.py` — syncs clarified dated tasks to the `GTD Signals` Google Calendar. See `signal-sync.md`.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Parsing `gws` JSON output with Python | Use `jq` in Bash tool calls — never `python3 -c` |
| Asking decisions as plain text | Use `AskUserQuestion` with clickable URLs for every user choice |
| Running `gws` without `--format json` | Always pass `--format json` so output is structured |
| Calling generated `gws-*` skills for Gmail/Calendar | Use `gmail-commands.md`, `calendar-commands.md`, `people-commands.md` |
| Using Haiku for email classification | Only `gtd-gws-fetch`, `gtd-vault-scan`, `gtd-signal-diff` are Haiku. Classification stays on Sonnet+ |
