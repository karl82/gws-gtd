---
name: gtd
description: Run GTD inside an Obsidian vault, integrated with Gmail and Google Calendar via the gws CLI. Use for daily / weekly / monthly review ceremonies, processing the Gmail inbox into vault tasks, capturing calendar events, syncing dated tasks to a GTD Signals calendar, and answering questions about the vault state. Loaded for any vault using these conventions.
---

# GTD

Run GTD inside an Obsidian vault, integrated with Gmail and Google Calendar.

## When to use

The user invokes a slash command (`/gtd`, `/gtd-sweep`, `/gtd-drain`) or asks about:

- Daily, weekly, monthly, or organizing review
- Inbox triage / Gmail processing
- Capturing a task or calendar event
- "What should I work on?" / next-action queries
- Project status, stalled projects
- Syncing tasks to the calendar

## Procedure

1. **Read `reference.md` end-to-end before any action.** This is a hard preflight gate. Do not infer rules from vault contents — the vault may carry legacy patterns that violate current rules. Skipping this step is the most common cause of avoidable mistakes.
2. **Read `commands.md` once at session start** for `gws` API mechanics. Don't `--help` per command.
3. Read `triage-policy.md` when classifying email.
4. Determine which ceremony the user wants from the slash command argument or natural language. Default to assistant mode if nothing is specified.
5. Follow the matching section of `reference.md`.

## Files

- `reference.md` — vault structure, ceremonies, Gmail/calendar integration, anti-rules. The full operating model.
- `triage-policy.md` — email classification table and heuristics. Frequently tuned.
- `commands.md` — `gws` API mechanics for Gmail, Calendar, People.
- `scripts/sync_signals.py` — the GTD Signals calendar sync helper.

## Prerequisites

- `gws` binary on PATH, authenticated. Recommended scopes: `gmail.modify`, `calendar.readonly`, `contacts.readonly`. Plus `gmail.send` for replies, `calendar.events` for writing signal events.
- `jq` for JSON parsing.
- Obsidian vault following the canonical structure (see `reference.md § Vault structure`).
- For backlog drain: the `ralph-loop` plugin.

## Guardrails

- Pass `--format json` to every `gws` command.
- Use `jq` for JSON extraction. Never `python3 -c`.
- Every user decision goes through `AskUserQuestion`.
- See `reference.md § Anti-rules` for behavioral rules that apply across all ceremonies.

## Common mistakes

| Mistake | Fix |
|---|---|
| Skipping `reference.md` and inferring rules from the vault | Read it end-to-end before the first action. |
| Treating new emails as standalone captures | Match by `gmail_thread_id` / sender / order ID against existing `#waiting` and `#next` tasks first. See `reference.md § Step 1 — Classify`. |
| Replying to your own sent message via `+reply` | Reply goes to yourself. Find last message **from the other party** in the thread. See `commands.md § +reply`. |
| Marking `✅` when user reports completion in chat | Capture as a `📝` note; ask before marking complete. Anti-rule: don't auto-complete. |
| Adding inline `#task` to a project file | Tasks live in journal daily notes; project files surface via dataviewjs. |
| Putting completed `[x]` lines in `Inbox.md` | Inbox is unclarified-only. Move to journal/project on clarify, delete on completion. |
| Parsing `gws` JSON with Python | Use `jq` in Bash. |
| Plain-text decisions | Always `AskUserQuestion`. |
| `gws ... | jq` parse errors | Redirect stderr: `gws ... 2>/dev/null | jq ...`. |
| `gws` without `--format json` | Always pass it. |
| `messages.batchModify` with thread IDs | Requires message IDs. See `commands.md`. |
| `threads.modify` with labels in `--params` | Labels go in `--json`, not `--params`. See `commands.md`. |
