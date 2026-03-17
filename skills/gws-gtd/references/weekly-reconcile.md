## Weekly Reconcile Procedure

### Prerequisites

Run the daily intake ceremony (`references/daily-intake.md`) before starting the weekly reconcile. The vault must be current before reconciliation begins.

### Scope

- Extend weekly review with Google inbox safety nets.
- Ensure no important email/calendar input remains outside GTD control.
- Sweep all unclarified `#inbox` tasks in the vault.
- Use `skills/gws-gtd/references/email-triage-policy.md` as the canonical source for label meaning and promotion rules.

### Step 1 - Sweep Unclarified `#inbox` Tasks (mandatory)

The vault `#inbox` queue is the single clarification queue for all imported emails — both urgent items handled during daily ceremonies and deferred review-style tasks. Weekly review must clarify all remaining `#inbox` items before Get Clear is complete.

Query vault-wide for open `#task #inbox` items:
- Items without a `[[Projects/...]]` or `[[Areas/...]]` wikilink need a destination decision.

For each unclarified `#inbox` task decide:
- **Clarify** — add wikilink, remove `#inbox`, add `#next` or `#waiting` as appropriate
- **Trash** — task is no longer relevant; delete it and archive the source Gmail thread

Also surface unlabeled inbox threads older than 7 days (missed by daily processing):

- `in:inbox older_than:7d -label:<IMPORT_LABEL> -label:<IMPORTED_LABEL> -label:<WAITING_LABEL> -label:<REFERENCE_LABEL>`

For each stale thread decide: import as `#task #inbox`, move to `gtd/reference`, or trash.

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

- Surface non-`#inbox` open tasks that have no `[[Projects/...]]` or `[[Areas/...]]` wikilink AND do not live inside a `Projects/` or `Areas/` file. Tasks in `Journal/` or elsewhere that carry a valid wikilink are clean — do not flag or relocate them.
- Keep one canonical task line per commitment; do not duplicate tasks between Journal and project/area notes.

### Weekly Output

- Count of clarified `#inbox` tasks and stale unlabeled emails processed
- Waiting loop risks and owner/follow-up decision points
- Calendar load risks for the next 7 days
- Hybrid inbox/orphan integrity actions performed
