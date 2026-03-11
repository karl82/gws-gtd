## Canonical Vault Model

### Task Syntax

- Globally tracked GTD actions use canonical syntax: `- [ ] #task ...`
- Plain checklists stay local and should not replace canonical GTD tasks.
- Due dates use `📅 YYYY-MM-DD`.
- Optional task dependency markers are supported:
  - `🆔 task-id`
  - `⛔ blocker-id`
  - `[id:: task-id]`
  - `[dependsOn:: blocker-id]`

### Folder Semantics

- `Inbox.md` is an optional capture surface.
- `Projects/` are finite outcomes.
- `Areas/` are ongoing responsibilities.
- `People/` stores relationship notes and stable contact references.
- `Resources/` is reference-only.
- `Archive/` is for completed or inactive notes.
- `Journal/` stores time-based notes and review artifacts.
- `System/` stores templates, queries, and workflow infrastructure.

### Project Rules

- Every active project should define a measurable outcome.
- Every active project should have at least one open linked `#task`.
- Plain subtasks do not satisfy the open-task requirement.

### Inbox Rules

- Inbox state is tag-driven through `#inbox`, not file-driven.
- Clarify by removing `#inbox` and moving the task to the right project/area or linking it there.
- Inbox tasks should never remain completed.

### Review Rules

- Weekly review uses `System/Templates/Weekly Review.md`.
- Monthly review uses `System/Templates/Monthly Review.md`.
- Shared task and review views live in `System/Queries/`.
- Central query exclusions live in `System/Queries/Task Query Config.md`.

### Calendar and GWS Rules

- The vault is the task system of record.
- Gmail is the capture/intake mailbox.
- `GTD Signals` is output-only and mirrors only qualified tasks.
- Waiting items should appear on calendar only when follow-up is dated.

### Anti-Rules

- Do not invent deadlines.
- Do not auto-complete tasks.
- Do not create hidden states outside the canonical model.
- Do not convert reference notes into GTD tasks without `#task`.

### Areas and Archive

- Areas express ongoing responsibilities, not outcomes.
- Archive reduces active-surface clutter but preserves retrieval.
- Suggested default areas are `Home`, `Finances`, `Relationships`, and `Admin`.

### Taxes Convention

- Annual tax notes live in `Projects/Taxes/`.
- Parent action groups are `US`, `CZ`, and `Payments`.
- Parent items use canonical `#task` syntax.
- Child checklist items stay non-`#task`.
