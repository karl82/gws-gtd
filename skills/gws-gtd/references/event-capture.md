## Event Capture Procedure

### Scope

- Capture event context through `gws` without turning calendar into a duplicate task system.
- Keep one-off event notes in Journal.
- For project-related events, link project and keep explicit traceability.

### Decision Rule

For each attendee event in the daily ask queue:

0. Present context first:
   - summary/title
   - when
   - short preview (first few lines from description/notes/location when present)
1. Pre-classify with recommendation and brief rationale:
   - `task`, `journal`, `project-note`, or `skip`
2. Is there an actionable next step?
   - Yes -> create canonical `#task` in Inbox or linked project note.
   - No -> create/append note context only.
3. Is this project-related?
   - Yes -> create project-linked event note and mention in daily journal.
   - No -> journal-only note entry.

### Storage Policy

- One-off event context: append to `Journal/YYYY-MM-DD.md`.
- Project-related context:
  - create `Resources/Events/YYYY/YYYY-MM-DD <event-title>.md`
  - include `[[Projects/...]]` link in the note
  - add journal mention linking to the event note and project

### Metadata

For event-linked task or note:

- `(source:: calendar)`
- `(calendar_id:: <id>)`
- `(event_id:: <id>)`
- `(web_link:: <url>)`

### Sync Caution

- Event description write-backs are optional and explicit.
- If writing back via API (`events.patch`), default to `sendUpdates: none` unless user asks otherwise.
