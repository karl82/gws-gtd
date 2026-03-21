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
  - Treat self-sent messages to the `+gtd@gmail.com` capture alias as plain capture notes by default, not as email references that must keep Gmail metadata on the task line.
  - Classify the full current unlabeled Gmail inbox in one pass by default, not in small batches.
  - Use recommendation-first bulk review: gather the whole current queue, bulk-group obvious garbage/reference classes where safe, show actionable/review-worthy items before obvious garbage, present one final compact classification review, and apply labels only after confirmation.
  - Always present email context for decisions: sender, subject, and a short preview (first few lines/snippet).
  - Import configured intake-label emails into canonical `#task #inbox` tasks in `Inbox.md` first.
  - Import configured waiting-label emails as mandatory `#waiting` tasks with references.
  - Treat `Inbox.md` as the mandatory landing zone for `gtd/import` captures so the user can apply the <=5-minute rule and clarify before filing elsewhere.
  - Treat `#inbox` as the cross-vault clarification state after import, but do not bypass `Inbox.md` during raw Gmail intake.
  - Clarify from `Inbox.md` by either completing the task via the <=5-minute rule or removing `#inbox` and moving/linking it into `Projects/`/`Areas/` only after the destination is explicit.
  - Review attendee-only calendar events in batches when possible.
  - Always present calendar context for decisions: summary plus a short preview (first few lines from description/notes/location when present).
  - Pre-classify each attendee event with recommendation (`task`, `journal`, `project-note`, `skip`) and rationale before asking.
- Focus on due, next, and waiting execution lists.
- Triage inbox only as needed; inbox zero is not required.
- Keep one canonical task line; track lifecycle on that line with `➕`, `🛫`, `✅`, `📅`.
- Use `#next` to mark the small set of currently actionable tasks; leave other open tasks active but off the main execution list.
- Use Tasks plugin dependency markers when useful: `🆔`, `⛔`, `[id:: ...]`, `[dependsOn:: ...]`.
- Apply the <=5-minute rule during clarify from `Inbox.md` when context/tools are available.
- Use the assistant proactively to analyze emails, attachments, and event details so review decisions can often be completed immediately.
- When a mail-driven task is completed and no immediate follow-up is expected, archive the thread from inbox.
- Treat `GTD Signals` as an output-only calendar layer for dated `#next` tasks and dated `#waiting` follow-ups only.
- Run as an interactive facilitation session.
- Prefer one compact final review for Gmail classification instead of repeated small-batch questions; show actionable choices first and obvious garbage last when possible; use one focused question only when something is truly ambiguous.
- In user-facing output, always identify tasks with recognizable context such as task text, sender, subject, person, or linked project/area; do not rely on bare file references or line numbers alone.
- Output decisions, blockers, and unresolved questions after each step.
