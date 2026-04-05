## Daily Intake Procedure

### Scope

- Extend the existing daily GTD ceremony with Google intake.
- Keep vault tasks as the only execution system.
- Intake should be selective and low-noise.
- Use classify-then-import flow so the user reviews email quality before labels drive automation.
- Treat Gmail as the only mobile capture inbox; do not import from Google Tasks.
- `GTD Signals` is output-only and must never be treated as capture.
- Use `skills/gws-gtd/references/email-triage-policy.md` as the canonical source for label meanings, classification defaults, and heuristics.
- Use the installed upstream `gws-gmail*`, `gws-calendar*`, `gws-people`, and `gws-shared` skills for execution.

Default label mapping for this procedure:

- `ROOT_LABEL = "gtd"`
- `IMPORT_LABEL = "gtd/import"`
- `WAITING_LABEL = "gtd/waiting"`
- `REFERENCE_LABEL = "gtd/reference"`
- `IMPORTED_LABEL = "gtd/imported"` (optional)

Recommended mobile capture filter:

- Gmail alias: `<your-address>+gtd@gmail.com`
- Filter: `to:<your-address>+gtd@gmail.com` -> apply `IMPORT_LABEL`

### Step 0 - Label Bootstrap and Mapping

1. Verify label availability using the installed Gmail skills.
2. If mapped labels are missing, choose one:
   - map to existing mailbox labels
   - create missing structured `gtd` labels
3. Persist the chosen mapping in ceremony context for this run.
4. When bootstrapping structured labels, create `ROOT_LABEL` first, then create child labels under it (`gtd/import`, `gtd/waiting`, `gtd/reference`, `gtd/imported`).

### Step 1 - Classification Queue (Before Import)

1. Pull recent unlabeled inbox candidates (example):
   - `in:inbox newer_than:2d -label:<IMPORT_LABEL> -label:<WAITING_LABEL> -label:<REFERENCE_LABEL> -label:<IMPORTED_LABEL>`
   - Omit any filter whose label is not configured.
2. For each candidate email, always show:
    - sender
    - subject
    - short preview (first few lines/snippet)
3. For each candidate email, propose one outcome and brief rationale using the policy defaults and heuristics from `skills/gws-gtd/references/email-triage-policy.md`.
   Allowed outcomes in this procedure:
    - `IMPORT_LABEL`
    - `WAITING_LABEL`
    - `appointment` (service/reservation confirmation or reschedule — see Appointment Workflow below)
    - `REFERENCE_LABEL`
    - `garbage` (move to TRASH/delete; recommend unsubscribe when available)
   Accepted calendar invitation notifications default to `garbage` unless they carry additional actionable context.

#### `#waiting` Tag Semantics

Use `#waiting` ONLY when the next step belongs to someone else (you delegated, you sent a request, you are blocked on an external party). Never use `#waiting` for tasks where you are the next actor.
4. Default to full-queue bulk review for unlabeled email candidates:
    - gather the whole current candidate set first
    - classify the entire queue in one pass when practical, rather than using repeated micro-batches
    - split the review into actionable-first vs obvious-garbage groups when possible
    - group obvious `garbage` and `reference` recommendations so they can be approved in one shot
    - present one compact final review summary for the whole queue, plus any ambiguous/high-signal items with sender, subject, and preview
    - ask for one final confirmation or compact overrides before mutating labels
5. Apply confirmed labels at thread level in one batch operation when possible.
6. For confirmed message-level garbage decisions, prefer one `messages.batchModify` call with `addLabelIds:["TRASH"]` over many single-message trash calls.
7. Treat messages sent to the capture alias as pre-routed candidates for `IMPORT_LABEL` unless the content clearly belongs in another policy outcome.
8. If the message is a self-sent capture to the `+gtd@gmail.com` alias, import it as a pure capture note by default: do not add `source:: gmail`, `gmail_thread_id`, `subject::`, or `web_link::` unless that email metadata is actually useful for later action.

### Step 2 - Gmail Intake Gates

1. Pull import candidates from Gmail label gate:
   - Query: `label:<IMPORT_LABEL> -label:<IMPORTED_LABEL>`
2. Pull waiting candidates:
   - Query: `label:<WAITING_LABEL>`
3. Pull candidates through the installed Gmail skills.

### Step 3 - Convert to GTD Tasks

1. For import label: create canonical tasks with `#inbox` capture state in `Inbox.md`.
2. `Inbox.md` is the transient landing zone for raw Gmail imports. Tasks leave on clarify — to a project/area file or the daily journal note.
3. Clarification rule: remove `#inbox` only after clarifying. Tasks leave `Inbox.md` on clarify — either move to a project/area file, or move to the daily journal note with a `[[Projects/...]]` or `[[Areas/...]]` wikilink.
4. For waiting label: always create or update a `#waiting` task with reference metadata.
5. Dedupe by `gmail_thread_id` for normal email-driven imports. For self-sent capture-alias notes, prefer dedupe by task text/content and avoid forcing Gmail metadata onto the task line.
6. Ambiguous but potentially important mail should usually become `IMPORT_LABEL` so it is clarified in `Inbox.md`, not deferred into a separate Gmail review queue.
7. Do not assign `🛫` or `📅` during raw import unless the source message contains a true external commitment that the user confirms.
8. If created date is needed, use `➕ YYYY-MM-DD` on the same task line.
9. During clarify from `Inbox.md`, if an imported action takes <=5 minutes and tools/context are available, execute it immediately.
10. Use the assistant to analyze message bodies and attachments during clarify so short review tasks can often be completed immediately instead of deferred.

Task patterns:

`- [ ] #task <action> #email #inbox [#waiting] (source:: gmail) (gmail_thread_id:: <id>) (subject:: <subject>) (web_link:: <url>)`

Self-capture pattern:

`- [ ] #task <action> #inbox`

### Step 4 - Calendar Ask Queue (Attendees Only)

1. Pull upcoming events (today and tomorrow) through the installed calendar skills.
2. Keep only events with attendees.
3. For each event, always show:
   - summary/title
   - when
   - short preview (first few lines from description/notes/location when present)
4. Pre-classify each event with recommendation and brief rationale:
   - `task` (explicit actionable follow-up needed)
   - `journal` (context only, no immediate action)
   - `project-note` (project-related context to preserve)
   - `skip` (no GTD value)
5. Default to batch review for attendee events too:
    - present all candidate events together with recommendation and rationale
    - collect compact user decisions for the whole batch
    - then apply event-note/task actions in one go

### Appointment Workflow

Apply this when an email is a service/reservation/appointment confirmation or reschedule notification.

1. Search Google Calendar for an existing event matching the appointment (search by venue name, service type, or date range).
2. If an existing event is found:
   - Compare the email's date/time against the calendar event.
   - If they match: archive the email, no task needed.
   - If they differ (reschedule): patch the calendar event with the new date/time, then archive the email.
3. If no existing event is found:
   - Create a calendar event with the appointment date/time, summary, and location from the email.
   - Archive the email after creation.
4. Never create a vault `#task` for an appointment that is already reflected (or can be reflected) in the calendar.

### Step 5 - Post-Import Hygiene

- If import succeeded and `IMPORTED_LABEL` exists, move Gmail item from import queue to `IMPORTED_LABEL`.
- If `IMPORTED_LABEL` does not exist, rely on thread-id dedupe and leave labels unchanged.
- For `garbage` decisions, move the thread to `TRASH` after user confirmation.
- If `List-Unsubscribe` is present, recommend unsubscribe as a follow-up and ask before executing any unsubscribe action.

### Step 6 - Lifecycle Logging

1. Keep one canonical task line for lifecycle updates (`➕`, `🛫`, `✅`, `📅`).
2. Do not duplicate completed tasks into Journal as additional `#task` entries.
3. If timeline context is useful, add narrative journal notes with backlinks, not duplicate tasks.
4. Never journal email triage mechanics: do not record trash counts, label moves, import counts, queue-cleanup stats, or similar ceremony output in the daily note.
5. Only journal mail-driven real-world outcomes, such as a reply sent, a dispute filed, a booking changed, or a purchase completed.
6. Every journal entry created from intake work must link to the relevant `[[Projects/...]]`, `[[Areas/...]]`, `[[People/...]]`, or canonical task.
7. If a mail-driven task is completed and no immediate follow-up is expected, archive the Gmail thread by removing `INBOX`.
8. Keep completed threads in inbox only when an active near-term response loop still matters.

### Waiting Follow-Up Signals

- `#waiting` tasks stay on the waiting list by default.
- Only create a calendar follow-up signal when a waiting task has an explicit follow-up date.
- Use the calendar as a reminder layer for follow-up, not as a waiting inventory.

### Auth and Scope Check

- If Gmail call fails with auth/scope error, stop intake and report exact blocker.
- Calendar ask queue requires calendar scopes. On `insufficientPermissions`, report setup blocker and continue daily ceremony without calendar import.

### Daily Output

- Count of emails classified with user confirmation
- Count of imported actionable emails
- Count of mandatory waiting tasks created/updated
- Calendar decisions taken and deferred
- Any unresolved clarifications
- Keep this output in the ceremony/session response only; do not copy it into the journal.
