## Weekly Reconcile Procedure

### Prerequisites

Run the daily intake ceremony (`references/daily-intake.md`) before starting the weekly reconcile. The vault must be current before reconciliation begins.

### Scope

- Extend weekly review with Google inbox safety nets.
- Ensure no important email/calendar input remains outside GTD control.
- Respect strict weekly gate: `#inbox` Zero in vault before exiting Get Clear.
- Use `skills/gws-gtd/references/email-triage-policy.md` as the canonical source for label meaning and promotion rules.

### Step 1 - Drain `gtd/review` Queue (mandatory)

The `gtd/review` label is the weekly deferred queue. Emails are placed here during daily processing specifically to avoid daily distraction — they must be resolved at the weekly review, not before. This queue **must reach zero** before Get Clear is complete.

Suggested query: `label:<REVIEW_LABEL>`

For each thread decide:
- **Promote to `gtd/import`** — becomes a vault task via normal intake
- **Move to `gtd/waiting`** — delegated, tracking externally
- **Move to `gtd/reference`** — no action needed, keep for reference
- **Trash** — no action, no reference value

Do not create vault tasks directly from `REVIEW_LABEL` — promote to `IMPORT_LABEL` first and let the intake flow handle task creation.

Also surface unlabeled inbox threads older than 7 days (missed by daily processing):

- `in:inbox older_than:7d -label:<IMPORT_LABEL> -label:<IMPORTED_LABEL> -label:<WAITING_LABEL> -label:<REFERENCE_LABEL> -label:<REVIEW_LABEL>`

If your mailbox uses a different label taxonomy, replace the label filters with your mapped equivalents.

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
- Surface non-`#inbox` open tasks that have no `[[Projects/...]]` or `[[Areas/...]]` wikilink AND do not live inside a `Projects/` or `Areas/` file. Tasks in `Journal/` or elsewhere that carry a valid wikilink are clean — do not flag or relocate them.
- Keep one canonical task line per commitment; do not duplicate tasks between Journal and project/area notes.

### Weekly Output

- Count of reviewed deferred/unlabeled emails
- Waiting loop risks and owner/follow-up decision points
- Calendar load risks for the next 7 days
- Hybrid inbox/orphan integrity actions performed
