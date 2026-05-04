# Daily Procedure

> **Scope:** Daily GTD ceremony. Invokes `gmail-intake.md`, `calendar-intake.md`, and `appointment-triage.md` as the Gmail and Calendar surfaces. For structural rules see `canonical-vault.md`; for behavioral doctrine see `conventions.md`; for label mechanics see `email-triage-policy.md`.

## Scope

- Run daily execution from trusted lists: due, next actions, waiting, and active projects.
- Triage `#inbox` queue across the vault only when it is needed for the day's work. Inbox zero is not a daily gate.
- Use bulk handling for repetitive review queues per `gmail-intake.md § Bulk Review Pattern` — garbage-first for email batches.

## Decision Flow

1. What is it?
2. Is it actionable?
   - No → trash, reference, or incubate (`#someday`).
   - Yes → define the next physical action.
3. If multi-step, create or update a project with measurable outcome and at least one open `#task`.
4. For the next action:
   - Use the assistant to analyze emails, attachments, event details, and context before deciding.
   - Promote to `#task` when the action should be globally tracked; keep project-local decomposition as plain checklist items.
   - Do immediately if all three hold: the action takes ≤ 5 minutes, required context is available, and required tools are available.
   - Delegate and mark `#waiting` per `conventions.md § Tag Taxonomy § #waiting semantics`.
   - Defer into the correct project, area, or keep in the daily journal with a wikilink.

## Context-Based Execution (Optional)

After reviewing due/next/waiting lists, group `#next` tasks by context tag for batch execution when the task list has ≥ 3 tasks per context:

1. Filter `#next` tasks by current context (e.g., all `#phone` calls, all `#email` replies, all `#errand` tasks).
2. Execute the batch, then switch context.
3. Skip this step when the task list has fewer than 3 tasks in any context.

## GTD Signals Pre-Check

At the start of each daily ceremony, after loading the calendar agenda, check for stale GTD Signals events whose corresponding vault tasks are already complete. Delegate the diff to `gtd-signal-diff` (Haiku), then offer to delete stale signals via `AskUserQuestion` before proceeding to the main ceremony.

## Daily Guardrails

- Do not require inbox zero in daily mode.
- Keep `#inbox` tasks free of completed items (see `canonical-vault.md § Inbox Rules`).
- Use `#next` to mark the small set of tasks that are actionable now. Other open commitments stay untagged.
- When one task can start only after another task completes, use Tasks dependency markers (`🆔`, `⛔`, or Dataview `id` / `dependsOn`).
- Keep minor implementation subtasks as plain checklist items unless they need independent GTD tracking.
- Tasks born from real events (meetings, calls, decisions) belong in the daily journal note with a `[[Projects/...]]` or `[[Areas/...]]` wikilink.
- When timeline context matters but no new task is needed, record a plain linked narrative entry in the journal.
- Every journal entry links to a `[[Projects/...]]`, `[[Areas/...]]`, `[[People/...]]`, or canonical task.
- Keep due dates for hard commitments only.
- Keep context tags sparse and execution-focused.
- For full journal hygiene, see `conventions.md § Journal Hygiene`.
- For anti-rules (no auto-complete, no invented deadlines, no ceremony mechanics in journals), see `conventions.md § Anti-Rules`.

## Termination Gates

The daily ceremony exits only when ALL of the following are true. Re-evaluate at the end of each pass.

1. **Classification queue empty.** Re-run the `gmail-intake.md` Step 1 query; zero threads returned.
2. **Import/Waiting drained.** Re-run `gmail-intake.md` Step 2 queries; zero unprocessed threads on either label.
3. **Calendar ask queue reviewed.** Every attendee event from `calendar-intake.md` has a recorded decision (`task | journal | project-note | skip`).
4. **User confirms end.** Present a final `AskUserQuestion` with residual unresolved items, deferred clarifications, and per-destination counts. Accept only an explicit "end ceremony" answer.

If gate 1 or 2 reopens mid-run because new mail arrived, report "new candidates detected, N items" and ask whether to process now or defer.

On exit, append `{"kind":"ceremony","name":"daily","ts":"<ISO>","outcome":"complete","residual":[...]}` to `root/System/.gtd-coach-state.jsonl` so the coach persona has handoff context.

## Output

- Decisions made (counts by destination).
- Items requiring user decision.
- Risks or blockers (`#waiting`, `#blocked`).
- Keep this output in the ceremony/session response, not in the journal.
