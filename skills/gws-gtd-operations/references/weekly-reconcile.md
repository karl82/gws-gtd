## Weekly Reconcile Procedure

### Scope

- Extend weekly review with Google inbox safety nets.
- Ensure no important email/calendar input remains outside GTD control.
- Respect strict weekly gate: `#inbox` Zero in vault before exiting Get Clear.
- Use `System/Email Triage Policy.md` as the canonical source for label meaning and promotion rules.

### Step 1 - Review Deferred Gmail Intake

Review unresolved queues:

- archived `label:<REVIEW_LABEL>` threads
- unlabeled inbox older than 7 days, excluding known GTD labels

Suggested queries:

- `label:<REVIEW_LABEL>`
- `in:inbox older_than:7d -label:<IMPORT_LABEL> -label:<IMPORTED_LABEL> -label:<WAITING_LABEL> -label:<REFERENCE_LABEL> -label:<REVIEW_LABEL>`

If your mailbox uses a different label taxonomy, replace the label filters with your mapped equivalents.

For each `REVIEW_LABEL` thread, decide whether it should move to `IMPORT_LABEL`, `WAITING_LABEL`, `REFERENCE_LABEL`, or trash. Do not create vault tasks directly from `REVIEW_LABEL` unless the review decision promotes the thread into action.

### Step 2 - Reconcile Waiting Dependencies

- List open GTD tasks containing `#waiting` and `source:: gmail`.
- Surface items with no progress signals and no due date.
- Confirm that only dated waiting items are being mirrored to `GTD Signals` as follow-up reminders.
- Keep or re-sequence; do not auto-complete.

### Step 3 - Calendar Pressure Check

- Pull weekly agenda: `gws calendar +agenda --week --format json`
- Compare meeting load with due-date clusters in vault.
- Flag overloaded days and suggest redistribution candidates.

### Step 4 - Integrity Checks for Hybrid Inbox Model

- Review `#inbox` items across the whole vault and enforce `#inbox` zero by end of Get Clear.
- Surface non-`#inbox` open tasks outside `Projects/` and `Areas/` that lack `[[Projects/...]]` or `[[Areas/...]]` links.
- Keep one canonical task line per commitment; do not duplicate tasks between Journal and project/area notes.

### Weekly Output

- Count of reviewed deferred/unlabeled emails
- Waiting loop risks and owner/follow-up decision points
- Calendar load risks for the next 7 days
- Hybrid inbox/orphan integrity actions performed
