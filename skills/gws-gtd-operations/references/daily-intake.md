## Daily Intake Procedure

### Scope

- Extend the existing daily GTD ceremony with Google intake.
- Keep vault tasks as the only execution system.
- Intake should be selective and low-noise.
- Use classify-then-import flow so the user reviews email quality before labels drive automation.
- Treat Gmail as the only mobile capture inbox; do not import from Google Tasks.
- `GTD Signals` is output-only and must never be treated as capture.
- Use `System/Email Triage Policy.md` as the canonical source for label meanings, classification defaults, and heuristics.

Default label mapping for this procedure:

- `ROOT_LABEL = "gtd"`
- `IMPORT_LABEL = "gtd/import"`
- `WAITING_LABEL = "gtd/waiting"`
- `REVIEW_LABEL = "gtd/review"`
- `REFERENCE_LABEL = "gtd/reference"`
- `IMPORTED_LABEL = "gtd/imported"` (optional)

Recommended mobile capture filter:

- Gmail alias: `<your-address>+gtd@gmail.com`
- Filter: `to:<your-address>+gtd@gmail.com` -> apply `IMPORT_LABEL`

### Step 0 - Label Bootstrap and Mapping

1. Verify label availability with `gws gmail users labels list --params '{"userId":"me"}'`.
2. If mapped labels are missing, choose one:
   - map to existing mailbox labels
   - create missing structured `gtd` labels
3. Persist the chosen mapping in ceremony context for this run.
4. When bootstrapping structured labels, create `ROOT_LABEL` first, then create child labels under it (`gtd/import`, `gtd/waiting`, `gtd/review`, `gtd/reference`, `gtd/imported`).

### Step 1 - Classification Queue (Before Import)

1. Pull recent unlabeled inbox candidates (example):
   - `in:inbox newer_than:2d -label:<IMPORT_LABEL> -label:<WAITING_LABEL> -label:<REVIEW_LABEL> -label:<REFERENCE_LABEL> -label:<IMPORTED_LABEL>`
   - Omit any filter whose label is not configured.
2. For each candidate email, always show:
    - sender
    - subject
    - short preview (first few lines/snippet)
3. For each candidate email, propose one outcome and brief rationale using the policy defaults and heuristics from `System/Email Triage Policy.md`.
   Allowed outcomes in this procedure:
    - `IMPORT_LABEL`
    - `WAITING_LABEL`
    - `appointment` (service/reservation confirmation or reschedule — see Appointment Workflow below)
    - `REVIEW_LABEL`
    - `REFERENCE_LABEL`
    - `garbage` (move to TRASH/delete; recommend unsubscribe when available)
   Accepted calendar invitation notifications default to `garbage` unless they carry additional actionable context.

#### `#waiting` Tag Semantics

Use `#waiting` ONLY when the next step belongs to someone else (you delegated, you sent a request, you are blocked on an external party). Never use `#waiting` for tasks where you are the next actor.
4. Default to batch review for unlabeled email candidates:
    - gather the current candidate set first
    - split the batch into actionable-first vs obvious-garbage groups when possible
    - show the actionable/review-worthy items first so the user can focus on meaningful choices
    - group obvious `garbage` recommendations last and make them easy to approve in one shot
    - ask for compact replies such as `A1 i, A2 f` or `trash G1-G8`
    - wait to mutate labels until the batch decisions are confirmed
5. Apply confirmed labels at thread level in one batch operation when possible.
6. For confirmed message-level garbage decisions, prefer one `messages.batchModify` call with `addLabelIds:["TRASH"]` over many single-message trash calls.
7. Treat messages sent to the capture alias as pre-routed candidates for `IMPORT_LABEL` unless the content clearly belongs in another policy outcome.

### Step 2 - Gmail Intake Gates

1. Pull import candidates from Gmail label gate:
   - Query: `label:<IMPORT_LABEL> -label:<IMPORTED_LABEL>`
2. Pull waiting candidates:
   - Query: `label:<WAITING_LABEL>`
3. Pull via helper or resource methods:
   - `gws gmail +triage --query '<QUERY>' --format json`
   - or `gws gmail users threads list --params '{"userId":"me","q":"<QUERY>"}'`

### Step 3 - Convert to GTD Tasks

1. For import label: create canonical tasks with `#inbox` capture state.
2. Default destination is `Inbox.md`, but capture is allowed anywhere if the note context is intentional.
3. Clarification rule: remove `#inbox` only when destination is explicit (`Projects/`, `Areas/`, or line has `[[Projects/...]]` / `[[Areas/...]]` link).
4. For waiting label: always create or update a `#waiting` task with reference metadata.
5. Dedupe by `gmail_thread_id` so reruns are idempotent.
6. `REVIEW_LABEL` threads should usually be archived and should not create a vault task until they are promoted during weekly review or ad-hoc triage.
7. Do not assign `🛫` or `📅` during raw import unless the source message contains a true external commitment that the user confirms.
8. If created date is needed, use `➕ YYYY-MM-DD` on the same task line.
9. During clarify, if an imported action takes <=5 minutes and tools/context are available, execute it immediately.
10. Use the assistant to analyze message bodies and attachments during clarify so short review tasks can often be completed immediately instead of deferred.

Task pattern:

`- [ ] #task <action> #email #inbox [#waiting] (source:: gmail) (gmail_thread_id:: <id>) (subject:: <subject>) (web_link:: <url>)`

### Step 4 - Calendar Ask Queue (Attendees Only)

1. Pull upcoming events (today and tomorrow):
   - `gws calendar +agenda --days 2 --format json`
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
4. If a mail-driven task is completed and no immediate follow-up is expected, archive the Gmail thread by removing `INBOX`.
5. Keep completed threads in inbox only when an active near-term response loop still matters.

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
