## Canonical Vault Model

> **Scope:** Structural model — WHAT the vault looks like. For behavioral doctrine (tag taxonomy, label semantics, journal hygiene, calendar rules), see `conventions.md`.

### Task Syntax

- Globally tracked GTD actions use canonical syntax: `- [ ] #task ...`
- Plain checklists stay local and should not replace canonical GTD tasks.
- GTD state tags: `#inbox` (capture), `#next` (action-now), `#waiting` (delegated/external dependency), `#someday`.
- Keep one canonical task line per commitment.
- Track lifecycle on that same line using `➕`, `🛫`, `✅`, and `📅`.
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
- Clarify by removing `#inbox` and moving the task to the right project/area or linking it there.
- Inbox tasks should never remain completed.
- `#someday` items are incubated, not actionable. They stay wherever filed (project, area, or standalone) and are reviewed periodically for promotion or deletion.

### Review Rules

- Weekly review uses `System/Templates/Weekly Review.md`.
- Monthly review uses `System/Templates/Monthly Review.md`.
- Shared task and review views live in `System/Queries/`.
- Central query exclusions live in `System/Queries/Task Query Config.md`.

### Journal Rules

- See `conventions.md` — Journal Hygiene.

### Calendar and GWS Rules

- The vault is the task system of record.
- Gmail is the capture/intake mailbox.
- For calendar and GTD Signals behavioral rules, see `conventions.md` — Calendar Model.

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
