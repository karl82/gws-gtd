## Weekly Reconcile Procedure

### Scope

- Extend weekly review with Google inbox safety nets.
- Ensure no important email/calendar input remains outside GTD control.
- Respect strict weekly gate: `#inbox` Zero in vault before exiting Get Clear.
- Use `skills/gws-gtd/references/email-triage-policy.md` as the canonical source for label meaning and promotion rules.
- Use the installed upstream `gws-gmail*` and `gws-calendar*` skills for review queries.

### Step 1 - Review Gmail Intake Safety Nets

Review unresolved queues:

- unlabeled inbox older than 7 days, excluding known GTD labels
- `label:<IMPORT_LABEL> -label:<IMPORTED_LABEL>` for captures that still need clarification

Suggested queries:

- `label:<IMPORT_LABEL> -label:<IMPORTED_LABEL>`
- `in:inbox older_than:7d -label:<IMPORT_LABEL> -label:<IMPORTED_LABEL> -label:<WAITING_LABEL> -label:<REFERENCE_LABEL>`

If your mailbox uses a different label taxonomy, replace the label filters with your mapped equivalents.

For each stale intake candidate, decide whether it should move to `IMPORT_LABEL`, `WAITING_LABEL`, `REFERENCE_LABEL`, or trash. Use `IMPORT_LABEL` for anything that still needs an `Inbox.md` clarify step.

### Step 2 - Reconcile Waiting Dependencies

- List open GTD tasks containing `#waiting` and `source:: gmail`.
- Surface items with no progress signals and no due date.
- Confirm that only dated waiting items are being mirrored to `GTD Signals` as follow-up reminders.
- Keep or re-sequence; do not auto-complete.

### Step 3 - Calendar Pressure Check

- Pull weekly agenda through the installed calendar skills.
- Compare meeting load with due-date clusters in vault.
- Flag overloaded days and suggest redistribution candidates.

### Step 4 - Integrity Checks for Hybrid Inbox Model

- Review `#inbox` items across the whole vault and enforce `#inbox` zero by end of Get Clear.
- Surface non-`#inbox` open tasks that have no `[[Projects/...]]` or `[[Areas/...]]` wikilink AND do not live inside a `Projects/` or `Areas/` file. Tasks in `Journal/` or elsewhere that carry a valid wikilink are clean — do not flag or relocate them.
- Keep one canonical task line per commitment; do not duplicate tasks between Journal and project/area notes.

### Weekly Output

- Count of reviewed deferred/unlabeled emails
- Waiting loop risks and owner/follow-up decision points
- Calendar load risks for the next 7 days
- Hybrid inbox/orphan integrity actions performed
