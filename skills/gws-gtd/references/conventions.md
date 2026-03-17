## Conventions

`gws-gtd` is an opinionated GTD-on-Google-Workspace workflow. These conventions are fixed package doctrine, not per-vault configuration.

### Canonical Task Syntax

- Task marker: `#task`
- Capture state: `#inbox`
- Action-now marker: `#next`
- Delegated/external dependency marker: `#waiting`
- Keep one canonical task line per commitment.
- Track lifecycle on that same line using `➕`, `🛫`, `✅`, and `📅`.

### Tag Taxonomy

Tags serve two purposes only: **GTD lifecycle state** and **execution context**. Area or domain ownership is expressed exclusively via `[[wikilinks]]`, never via tags.

| Tier | Tags | Meaning |
|---|---|---|
| **GTD state** | `#task`, `#inbox`, `#next`, `#waiting`, `#someday` | Lifecycle position of the action. `#inbox` = captured, not yet clarified (no wikilink). `#next` = currently actionable. `#waiting` = delegated or blocked on external party. `#someday` = incubated, not committed. |
| **Context / mode** | `#phone`, `#email`, `#errand`, `#internet`, `#deep`, `#buy`, `#idea`, `#payment` | How or where the action is performed |

**`#waiting` rule:** Use `#waiting` ONLY when the next step belongs to someone else — you delegated, sent a request, or are blocked on an external party. Never use `#waiting` for tasks where you are the next actor.

**Rules:**
- Domain/area tags (`#home`, `#admin`, `#work`, `#personal`, etc.) are not used. Ownership is declared by wikilink (`[[Areas/Home]]`, `[[Projects/...]]`) or by the file the task lives in.
- Context tags enable execution filtering (e.g. "all #phone calls", "all #errand tasks"). They do not imply ownership.
- A task with no context tag is valid — not every action needs a mode signal.
- Do not invent new domain tags. If a task needs an area owner, add the wikilink.

### Gmail Label Model

- Root label: `gtd`
- Intake gate: `gtd/import` → creates `#task #inbox` vault task
- Waiting gate: `gtd/waiting` → creates `#task #waiting` vault task
- Reference retention: `gtd/reference` → archive in Gmail, no vault task
- Post-import dedupe marker: `gtd/imported`

`gtd/review` is not used. Emails that can wait until weekly review are still imported via `gtd/import` — the vault `#inbox` queue is the single clarification queue for both urgent and deferred items.

### Calendar Model

- Signal calendar: `GTD Signals`
- `GTD Signals` is output-only.
- Mirror clarified dated `#next` tasks and dated `#waiting` follow-ups only.

### Journal vs Project Notes

**Journal** (`Journal/YYYY/MM/YYYY-MM-DD.md`) is the canonical place for timeline narrative — what happened, when, and why. Format: `# Daily - YYYY-MM-DD` with a `## Notes` section of plain linked bullet entries.

**Project and Area files** hold tasks, reference data, and stable context (tables, docs, links). They do not hold narrative timeline notes.

Rules:
- When something happens (decision made, action taken, reply sent, filing submitted), record it as a bullet in the daily journal with a `[[wikilink]]` to the relevant project or area.
- Do **not** append `📝 YYYY-MM-DD: ...` narrative sub-bullets under tasks in project files. The task line itself (with lifecycle emojis `➕ 🛫 ✅ 📅`) is the only thing that changes on the task.
- Exception: structured metadata that belongs to the task record itself (e.g. `(gmail_thread_id:: ...)`, `(web_link:: ...)`, checklist sub-items) may remain under the task line.

### Vault Model

- Canonical folders: `Projects/`, `Areas/`, `People/`, `Resources/`, `Archive/`, `Journal/`, `System/`
- `System/Templates/` and `System/Queries/` are runtime assets.
- Workflow doctrine lives in package skill references, not in `System/` config notes.
