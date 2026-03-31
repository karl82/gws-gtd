## Daily Procedure

### Scope

- Run daily execution from trusted lists: due, next actions, waiting, and active projects.
- Triage `#inbox` queue across the vault only as needed; inbox zero is not required in the daily ceremony.
- Prefer batch handling for repetitive review queues so decisions are gathered first and mutations happen after confirmation; within each batch, present meaningful/actionable choices before obvious garbage when possible.

### Decision Flow

1. What is it?
2. Is it actionable?
   - No -> trash, reference, or incubate (`#someday`).
   - Yes -> define next physical action.
3. If multi-step, create or update a project with measurable outcome and at least one open `#task`.
4. For the next action:
    - Use the assistant proactively to analyze emails, attachments, event details, and context so the user can make faster GTD decisions.
    - Promote to `#task` only when the action should be globally tracked; keep project-local decomposition as plain checklist items.
    - Do immediately if truly <=5 minutes and context/tools are available.
    - Delegate and mark `#waiting`.
    - Defer into the correct project, area, or keep in the daily journal with a wikilink.

### Context-Based Execution (Optional)

After reviewing due/next/waiting lists, optionally group `#next` tasks by context tag for batch execution:

1. Filter `#next` tasks by current context (e.g., all `#phone` calls, all `#email` replies, all `#errand` tasks).
2. Execute the batch, then switch context.
3. Skip this step when the task list is short or context variety is low.

### Daily Guardrails

- Do not require inbox zero in daily mode.
- Keep `#inbox` tasks free of completed items.
- Use `#inbox` as capture state across the vault; remove `#inbox` when clarified.
- Keep one canonical task line; update lifecycle on the same line (`➕`, `🛫`, `✅`, `📅`) instead of creating duplicates.
- Use `#next` to distinguish the small set of tasks that are truly actionable now from the larger pool of open commitments.
- When one task can only start after another task completes, use Tasks dependency markers (`🆔`, `⛔`, or Dataview `id` / `dependsOn`) instead of only describing the dependency in prose.
- Keep minor implementation subtasks as plain checklist items unless they need independent GTD tracking.
- Tasks born from real events (meetings, calls, decisions) belong in the daily journal note with a `[[Projects/...]]` or `[[Areas/...]]` wikilink.
- When timeline context matters but no new task is needed, record a plain linked narrative entry in the journal.
- Do not persist ceremony mechanics to the journal: no inbox counts, no email classification summaries, no import/waiting counts, no task-list snapshots, and no "daily review completed" markers.
- Journal entries are only for real-world timeline events or outcomes with later narrative value.
- Every journal entry should link to the relevant `[[Projects/...]]`, `[[Areas/...]]`, `[[People/...]]`, or canonical task.
- If the ceremony produced no meaningful real-world event, leave the journal untouched.
- In user-facing ceremony output, always identify tasks by recognizable context (task text, linked project/area/person, sender, or subject). Do not rely on bare file paths or line numbers as the primary identifier.
- Keep due dates for hard commitments only.
- Keep context tags sparse and execution-focused.

### Daily Output

- Decisions made (counts by destination)
- Items requiring user decision
- Risks or blockers (`#waiting`, `#blocked`)
- Keep this output in the ceremony/session response, not in the journal.
