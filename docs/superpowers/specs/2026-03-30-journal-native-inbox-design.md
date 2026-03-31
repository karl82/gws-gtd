# Journal-Native Inbox Capture

## Problem

Journal entries and GTD tasks are disconnected. Events captured in journal notes spawn tasks that live elsewhere (Inbox.md, Projects/, Areas/), losing the timeline context of when and why they were captured. Tasks don't know their origin; journal entries don't know what they spawned.

## Design

### Capture Model

Three-tier capture based on source:

| Source | Landing zone | Rationale |
|--------|-------------|-----------|
| Gmail `gtd/import` | `Inbox.md` | Automated pipeline, no human context to preserve |
| Gmail `gtd/waiting` | `Inbox.md` | Same automated pipeline |
| Human capture during ceremony | Daily journal note | Event context co-located with spawned task |
| Calendar attendee events | Daily journal note | Timeline event that may spawn a task |
| Self-sent `+gtd` alias | `Inbox.md` | Mobile capture has no journal context yet |
| Mind sweep / ad-hoc capture | Daily journal note | Human-originated, timeline-relevant |

Journal notes can contain `#task #inbox` lines. These are real GTD tasks born from real events, not ceremony output.

### Inbox.md Role

`Inbox.md` becomes a pure transient staging area for Gmail imports. Nothing stays there after clarify. During clarify, tasks leave Inbox.md via one of two paths:

- Move to the destination project/area file (if it clearly belongs there)
- Move to the daily journal note with a `[[Projects/...]]` or `[[Areas/...]]` wikilink (gains timeline context)

### Clarify Flow

Depends on where the task lives:

**Journal-born tasks:** Remove `#inbox`, add `[[Projects/...]]` or `[[Areas/...]]` wikilink. Task stays in the journal file. No move needed — the wikilink connects it to the project, and queries find tasks by link, not by file path.

**Inbox.md tasks (Gmail imports):** Remove `#inbox`, then either move to a project/area file OR move to the daily journal note with a wikilink. Inbox.md empties after clarify.

**Optional move:** If a journal task turns out to be a major standalone action that belongs as a top-level item in a project file, the user can optionally move it. Default: stay in journal.

### Journal Hygiene

Updated rule: journal notes capture real-world timeline events, outcomes, and the tasks they spawn.

| Content | Example | Allowed? |
|---------|---------|----------|
| Task born from a real event | `- [ ] #task #inbox Draft migration plan [[Projects/Platform/Migration]]` | Yes |
| Narrative about what happened | "Had sync with Alex about timeline pressure" | Yes |
| Ceremony mechanics | "Classified 12 emails, imported 3, trashed 9" | No |
| Task-list snapshots | "Current #next tasks: ..." | No |

One canonical task line rule still holds. A task born in journal must not be duplicated into the project file. The wikilink is the connection.

### Queries and Templates

No changes needed. Existing queries work because:

- `task-list.js` queries vault-wide by tag, not by file location
- `project-linked-open.js` finds tasks by `[[Projects/...]]` wikilink
- `Task Query Config.md` does not exclude `Journal/`
- Orphan task detection correctly flags journal tasks without project/area links

## Files to Change

| File | Change |
|------|--------|
| `references/canonical-vault.md` — Folder Semantics | Update `Journal/` description to include tasks born from timeline events |
| `references/canonical-vault.md` — Inbox Rules | Clarify Inbox.md as transient staging for Gmail; tasks leave on clarify to project/area or journal |
| `references/conventions.md` — Journal Hygiene | Allow `#task` lines born from real events; keep prohibition on ceremony mechanics |
| `references/daily.md` — Decision Flow | Clarify guidance: journal-born tasks stay with wikilink; Inbox.md tasks move to project/area or journal |
| `references/daily-intake.md` — Step 3 | Inbox.md remains Gmail landing zone; clarify can move tasks to journal |
| `references/daily.md` — Daily Guardrails | Revise rules separating journal from tasks; tasks born from events belong in journal |
