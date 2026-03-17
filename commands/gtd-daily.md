---
description: Run the daily GTD ceremony for this vault
agent: gtd-daily
subtask: true
---

Run the daily GTD ceremony for this repository.

Scope and notes: $ARGUMENTS

Requirements:
- Follow `AGENTS.md` and `gws-gtd` in `daily` plus `daily-intake` modes.
- Use `skills/gws-gtd/references/email-triage-policy.md` as the canonical source for Gmail label meaning, classification defaults, heuristics, and review-vs-import rules.
- Start with Google intake via `gws`:
  - Use Gmail as the only mobile capture channel; ignore Google Tasks.
  - Assume a single capture alias routes messages into `gtd/import`.
  - Classify recent unlabeled inbox emails with recommendation-first batch review; gather the batch first, show actionable/review-worthy items before obvious garbage, collect compact decisions, and apply labels only after confirmation.
  - Always present email context for decisions: sender, subject, and a short preview (first few lines/snippet).
  - Import configured intake-label emails into canonical `#task #inbox` tasks.
  - Import configured waiting-label emails as mandatory `#waiting` tasks with references.
  - Treat `gtd/review` as an archived deferred-review queue; do not create vault tasks from it unless promoted.
  - Treat `#inbox` as the cross-vault clarification queue (not only `Inbox.md`).
  - Clarify by removing `#inbox` and either moving to `Projects/`/`Areas/` or keeping in place with `[[Projects/...]]` / `[[Areas/...]]` link.
  - Review attendee-only calendar events in batches when possible.
  - Always present calendar context for decisions: summary plus a short preview (first few lines from description/notes/location when present).
  - Pre-classify each attendee event with recommendation (`task`, `journal`, `project-note`, `skip`) and rationale before asking.
- Focus on due, next, and waiting execution lists.
- Triage inbox only as needed; inbox zero is not required.
- Keep one canonical task line; track lifecycle on that line with `➕`, `🛫`, `✅`, `📅`.
- Use `#next` to mark the small set of currently actionable tasks; leave other open tasks active but off the main execution list.
- Use Tasks plugin dependency markers when useful: `🆔`, `⛔`, `[id:: ...]`, `[dependsOn:: ...]`.
- Apply the <=5-minute rule during clarify when context/tools are available.
- Use the assistant proactively to analyze emails, attachments, and event details so review decisions can often be completed immediately.
- When a mail-driven task is completed and no immediate follow-up is expected, archive the thread from inbox.
- Treat `GTD Signals` as an output-only calendar layer for dated `#next` tasks and dated `#waiting` follow-ups only.
- Run as an interactive facilitation session.
- Prefer compact batch questions for repetitive decisions; show actionable choices first and obvious garbage last when possible; use one focused question only when batching is not helpful.
- Output decisions, blockers, and unresolved questions after each step.
- At the end of the ceremony, run signal sync: dry-run `scripts/sync_gtd_signals.py`, show the diff (creates / updates / deletes), and apply after confirmation.
