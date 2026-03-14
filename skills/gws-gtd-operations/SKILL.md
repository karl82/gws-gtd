---
name: gws-gtd-operations
---

## Purpose

Legacy split skill retained during transition to the unified `gws-gtd` skill.

Prefer `skills/gws-gtd/SKILL.md` for new work.

The vault is the task system of record. Gmail is the capture/intake layer. Calendar is a signal/review layer.

## Supported Modes

- `daily-intake`
- `weekly-reconcile`
- `event-capture`
- `people-linking`
- `signal-sync`
- `ad-hoc-maintenance`

## Router

1. Resolve the user intent.
2. Use the matching reference:
   - `daily-intake` -> `references/daily-intake.md`
   - `weekly-reconcile` -> `references/weekly-reconcile.md`
   - `event-capture` -> `references/event-capture.md`
   - `people-linking` -> `references/people-linking.md`
   - `signal-sync` -> `references/signal-sync.md`
   - `ad-hoc-maintenance` -> `references/command-reference.md`
3. Follow `../gws-gtd/references/conventions.md` and `../gws-gtd/references/email-triage-policy.md` first.

## Guardrails

- Gmail is the only supported mobile capture inbox for this workflow.
- `GTD Signals` is output-only.
- Do not use Google Tasks as a parallel capture system.
- Keep one canonical task line per commitment.
- Prefer batch-first review before applying repetitive Gmail or Calendar actions.
- For reviewed message-level Gmail cleanup, prefer one `messages.batchModify` call with `addLabelIds:["TRASH"]` over many `messages.trash` calls.

## Supporting Files

- Overview: `README.md`
- Helpers:
  - `scripts/gmail_thread_reply.py`
  - `scripts/sync_gtd_signals.py`
