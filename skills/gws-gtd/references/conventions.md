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
| **GTD state** | `#task`, `#inbox`, `#next`, `#waiting`, `#someday` | Lifecycle position of the action |
| **Context / mode** | `#phone`, `#email`, `#errand`, `#internet`, `#deep`, `#buy`, `#idea`, `#payment` | How or where the action is performed |

**Rules:**
- Domain/area tags (`#home`, `#admin`, `#work`, `#personal`, etc.) are not used. Ownership is declared by wikilink (`[[Areas/Home]]`, `[[Projects/...]]`) or by the file the task lives in.
- Context tags enable execution filtering (e.g. "all #phone calls", "all #errand tasks"). They do not imply ownership.
- A task with no context tag is valid — not every action needs a mode signal.
- Do not invent new domain tags. If a task needs an area owner, add the wikilink.

### Gmail Label Model

- Root label: `gtd`
- Intake gate: `gtd/import`
- Waiting gate: `gtd/waiting`
- Deferred review queue: `gtd/review`
- Reference retention: `gtd/reference`
- Post-import dedupe marker: `gtd/imported`

### Calendar Model

- Signal calendar: `GTD Signals`
- `GTD Signals` is output-only.
- Mirror clarified dated `#next` tasks and dated `#waiting` follow-ups only.

### Vault Model

- Canonical folders: `Projects/`, `Areas/`, `People/`, `Resources/`, `Archive/`, `Journal/`, `System/`
- `System/Templates/` and `System/Queries/` are runtime assets.
- Workflow doctrine lives in package skill references, not in `System/` config notes.
