# Email Triage Policy

This note is the canonical source for Gmail GTD label meaning and email classification rules across daily, weekly, monthly, and ad-hoc workflows.

Use heuristics to classify unlabeled email. Once a GTD label already exists, respect that label unless the thread is clearly mislabeled or already represented elsewhere.

## Label Contract

| Label | Meaning | Default handling |
|---|---|---|
| `gtd/import` | Explicit task-import gate | Create or update a canonical task now. Dedupe by `gmail_thread_id`. |
| `gtd/waiting` | Explicit waiting gate | Create or update a mandatory `#waiting` task now. |
| `gtd/review` | Deferred classification queue | Archive in Gmail, do not create a vault task yet, and sweep during weekly review or ad-hoc triage. |
| `gtd/reference` | Non-actionable but worth retaining | Archive in Gmail and keep no task. |
| `gtd/imported` | Already processed marker | Use for dedupe/post-import hygiene when available. |

Notes:

- `gtd/import` is stronger than heuristics. If a thread already has `gtd/import`, it should still create a task unless it is a duplicate or clearly mislabeled.
- `gtd/review` items should normally be archived, not left in Gmail inbox.
- `gtd/review` items should not create `Inbox.md` entries or `#inbox` tasks by default.
- If an email may need action before the next weekly review, prefer `gtd/import` over `gtd/review`.

## Recommended Capture Setup

- Gmail is the only mobile capture inbox.
- Recommended alias: `<your-address>+gtd@gmail.com`.
- Recommended filter: `to:<your-address>+gtd@gmail.com` -> apply `gtd/import`.

## Classification Defaults

| Email type | Default action | Notes / exceptions |
|---|---|---|
| Message already labeled `gtd/import` | task | Create or update a task even if the task is phrased as review. |
| Message already labeled `gtd/waiting` | waiting task | Create or update the waiting task immediately. |
| Statement notice | trash | Override only when there is an amount due, a problem, or a real next step. |
| Insurance or travel-plan upsell | trash | Treat as marketing by default. |
| Policy, booking, or plan document worth keeping | reference + archive | Keep searchable, out of inbox. |
| Confirmation already covered by an existing `#waiting` task | match existing | No duplicate task; clear from import flow. |
| Appointment or reservation confirmation | calendar first | If already on calendar, archive. If not, create/update calendar and archive. |
| Airline / transport check-in reminder | trash | Flight is already on calendar. Check-in reminders are transient; delete without action. |
| Card security or fraud alert | import | Create a quick-review task: `Review [issuer] card alert — [merchant] $[amount] and confirm or dispute`. Resolve ≤5 min during daily when context is available. |
| Account security notification (password change, 2FA update, new login) | import | Create a quick-confirmation task: `Confirm [issuer] account security change was intentional`. Resolve ≤5 min. Applies to all issuers and services (Fidelity, Google, banks, etc.). |
| General service / settings-change notification | trash | Informational only — no confirmation or action required. Override only if the change was unexpected or involves security. |
| Datová schránka notification | review + archive | Official Czech government data mailbox delivery notification. Archive the Gmail notification immediately and open the Datová schránka portal to review the document. Do not create a vault task from the email alone. |
| Recruiter outreach with plausible opportunity | review | Usually review and send a generic decline unless the opportunity is unusually compelling. |
| Clearly actionable message where you are the next actor | import | Create a task now. |
| Delegated thread where the next move belongs to someone else | waiting | Create or update a `#waiting` task. |
| Ambiguous but potentially relevant informational mail | review | Archive with `gtd/review` and revisit later. |
| Pure noise, promotion, or accepted invitation notification | trash | Recommend unsubscribe when appropriate. |

## Heuristics

Use these heuristics when deciding how unlabeled email should be labeled.

### Next-Actor Check

- If you must do the next step, prefer `gtd/import`.
- If someone else must do the next step, prefer `gtd/waiting`.
- If no action is needed now and it can safely wait until review, prefer `gtd/review`.

### Timing Check

- Ask: does this need attention before the next weekly review?
- If yes, prefer `gtd/import`.
- If no, `gtd/review` is acceptable.

### Existing-System Check

- If the thread already maps to an existing task by `gmail_thread_id`, update or match that task instead of creating a duplicate.
- If the thread is already represented by a `#waiting` task, match the existing task and clear the email from intake.
- If the thread is already represented on calendar, archive the email rather than creating a vault task.

### Retention Check

- Keep `gtd/reference` only when the message is realistically useful later for proof, policy details, travel, taxes, legal records, or similar reference.
- Do not keep generic notices that can be re-fetched or do not support a later decision.

### Card and Account Security Heuristic

- Any card-not-present alert, unusual merchant flag, or fraud alert from a card issuer → `gtd/import`. Create task: `Review [issuer] card alert — [merchant] $[amount] and confirm or dispute`. The ≤5 min rule applies: if the merchant is recognizable and the amount is expected, mark done immediately; if not, dispute.
- Any account security notification (password changed, 2FA modified, new device login, security setting updated) from any service (Fidelity, Google, bank, etc.) → `gtd/import`. Create task: `Confirm [issuer] account security change was intentional`. Resolve ≤5 min.
- General settings-change or preference-update notifications (mailing preferences, notification settings, non-security account updates) → `trash`. No action or confirmation required.

### Datová Schránka Heuristic

- Datová schránka (Czech government data mailbox) notifications in Gmail are delivery pings only — the document itself lives in the portal, not in Gmail.
- Archive the Gmail notification immediately with `gtd/review`.
- Open the Datová schránka portal to read the actual document.
- Only create a vault task if the document requires a response or action — in that case create a `#next` task with a `📅` deadline based on the document's response window.
- Do not create a task from the Gmail notification alone.

### Recruiter Heuristic

- Default recruiter outreach to `gtd/review` unless it is clearly time-sensitive or unusually strong on role fit, scope, compensation, company quality, location, or personal relevance.
- If a recruiter thread already has `gtd/import`, still create a task, but phrase it as a review task such as `Review recruiter outreach from <name>/<company> and send decline unless compelling`.

## Review Queue Rules

- `gtd/review` is a deferred-classification queue, not an execution queue.
- Weekly review should sweep:
  - `gtd/import`
  - `gtd/waiting`
  - `gtd/reference`
  - unlabeled inbox older than threshold
- Avoid leaving the same thread in `gtd/review` indefinitely.

## Billing and Time-Sensitive Mail

- A billing or statement email with an amount due, a payment failure, or a problem becomes `gtd/import`, not trash.
- A renewal notice tied to an active project becomes `gtd/import` when there is a real next step; otherwise use `gtd/reference` or trash based on retention value.
- Time-sensitive ambiguous mail should become `gtd/import` as a review-style task rather than `gtd/review`.

## Vault Hygiene

- Do not create `Inbox.md` entries for `gtd/review` items unless they have been promoted into actionable GTD capture.
- Keep Gmail cleanup and vault task creation aligned so the inbox state reflects actual review state.
