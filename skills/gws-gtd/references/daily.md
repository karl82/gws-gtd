## Daily Procedure

### Scope

- Run daily execution from trusted lists: due, next actions, waiting, and active projects.
- Triage `#inbox` queue only for urgent items identified during intake — items that need action before the next weekly review. Leave all other `#inbox` items for the weekly ceremony sweep. Inbox zero is not a daily goal.
- Prefer batch handling for repetitive review queues so decisions are gathered first and mutations happen after confirmation; within each batch, present meaningful/actionable choices before obvious garbage when possible.

### Decision Flow

1. What is it?
2. Is it actionable?
   - No -> trash, reference, or incubate.
   - Yes -> define next physical action.
3. If multi-step, create or update a project with measurable outcome and at least one open `#task`.
4. For the next action:
    - Use the assistant proactively to analyze emails, attachments, event details, and context so the user can make faster GTD decisions.
    - Promote to `#task` only when the action should be globally tracked; keep project-local decomposition as plain checklist items.
    - Do immediately if truly <=5 minutes and context/tools are available.
    - Delegate and mark `#waiting`.
    - Defer into the correct project or area.

### Daily Guardrails

- Do not require inbox zero in daily mode. Only clarify `#inbox` items that are urgent or time-sensitive. All other `#inbox` items are swept during the weekly ceremony.
- Keep `#inbox` tasks free of completed items.
- Use `#inbox` as capture state across the vault; remove `#inbox` when clarified.
- Keep one canonical task line; update lifecycle on the same line (`➕`, `🛫`, `✅`, `📅`) instead of creating duplicates.
- Use `#next` to distinguish the small set of tasks that are truly actionable now from the larger pool of open commitments.
- When one task can only start after another task completes, use Tasks dependency markers (`🆔`, `⛔`, or Dataview `id` / `dependsOn`) instead of only describing the dependency in prose.
- Keep minor implementation subtasks as plain checklist items unless they need independent GTD tracking.
- When the timeline matters (reply sent, work started, important decision made), record that in the daily journal note as a plain linked note entry, not as a second task and **not** as a `📝` sub-bullet under the task. Use `System/Templates/Daily.md` as the required format: heading `# Daily - YYYY-MM-DD` with a `## Notes` section containing plain linked bullet entries pointing to the relevant `[[Projects/...]]` or `[[Areas/...]]`.
- Keep due dates for hard commitments only.
- Keep context tags sparse and execution-focused.

### Daily Output

- Decisions made (counts by destination)
- Items requiring user decision
- Risks or blockers (`#waiting`, `#blocked`)
