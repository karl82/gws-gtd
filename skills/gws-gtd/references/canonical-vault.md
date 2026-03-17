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

- `Inbox.md` is a live query view of all `#task #inbox` items across the vault. It is not a capture file — tasks are never written directly into it.
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
- Canonical project notes live at `Projects/<Domain>/<Project>.md`.
- Deeper project artifacts may live under `Projects/<Domain>/<Project>/`.
- Project-owned design notes live under `Projects/<Domain>/<Project>/designs/`.
- Active project design notes should not live in a separate top-level `Designs/` folder in the canonical end state.

### Linking Rules

- Use full vault-relative links for canonical entities under `Projects/`, `Areas/`, and `People/`.
- Every active project task must include a full `[[Projects/<Domain>/<Project>]]` link.
- Every active area task must include a full `[[Areas/...]]` link.
- Design-specific tasks may include both the project link and the design link, but never the design link alone.
- Every design note must link back to its canonical project note using the full project path.

### Design Metadata Rules

- Design notes intended for review or export must keep `project`, `gdoc_id`, `gdoc_url`, and `gdoc_source_of_truth` in frontmatter.
- Shared Google Docs tab bundles use stable `gdoc_role` and `gdoc_tab_title` metadata.
- Exported Google Docs mirrors remain read-only in Markdown.

### Inbox Rules

- Inbox state is tag-driven through `#inbox`, not file-driven.
- `Inbox.md` is a live query view of all `#task #inbox` items across the entire vault — not a capture file.
- Clarify by removing `#inbox` and adding a `[[Projects/...]]` or `[[Areas/...]]` wikilink.
- Daily ceremony clarifies only urgent `#inbox` items. Weekly ceremony sweeps all remaining `#inbox` items.
- Inbox tasks should never remain completed.

### Task Placement Rules

- Tasks can be created anywhere: journal, project file, area file.
- The wikilink (`[[Projects/...]]` or `[[Areas/...]]`) is the ownership declaration — not the file the task lives in.
- Do not move tasks after creation. Leave them where they were born.
- Journal-born tasks with a wikilink are fully visible in project and area query views via `project-linked-open.js`.
- Tasks without a wikilink and outside `Projects/` or `Areas/` are orphans — surface in `orphan-open` preset and clarify during weekly ceremony.

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
- Do not rely on ambiguous short links for canonical entities.

### Areas and Archive

- Areas express ongoing responsibilities, not outcomes.
- Archive reduces active-surface clutter but preserves retrieval.
- Suggested default areas are `Home`, `Finances`, `Relationships`, and `Admin`.

### Taxes Convention

- Annual tax notes live in `Projects/Taxes/`.
- Parent action groups are `US`, `CZ`, and `Payments`.
- Parent items use canonical `#task` syntax.
- Child checklist items stay non-`#task`.
