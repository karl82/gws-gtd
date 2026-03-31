## Conventions

> **Scope:** Behavioral doctrine — HOW to operate within the vault. For the structural model (task syntax, folder semantics, project/linking rules), see `canonical-vault.md`.

`gws-gtd` is an opinionated GTD-on-Google-Workspace workflow. These conventions are fixed package doctrine, not per-vault configuration. Workflow doctrine lives in package skill references, not in `System/` config notes.

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
- Reference retention: `gtd/reference`
- Post-import dedupe marker: `gtd/imported`

### Calendar Model

- Signal calendar: `GTD Signals`
- `GTD Signals` is output-only.
- Mirror clarified dated `#next` tasks and dated `#waiting` follow-ups only.

### Journal Hygiene

- Journal notes capture real-world timeline events and outcomes, not GTD system maintenance.
- Do not write ceremony logs, inbox statistics, label routing, task creation counts, or completion banners into journal notes.
- Every journal entry should link to the relevant `[[Projects/...]]`, `[[Areas/...]]`, `[[People/...]]`, or canonical task.
- If nothing meaningful happened beyond review/maintenance, do not add a journal entry.

### User-Facing Context

- When summarizing work to the user, identify tasks and notes with enough context to be recognizable immediately.
- Do not use bare references like `Inbox.md:10` or "the item on line 10" as the main identifier.
- Pair any file reference with the task text, sender, subject, person, or linked project/area.
