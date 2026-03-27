# Email Triage Policy

This note is the canonical source for Gmail GTD label meaning and email classification rules across daily, weekly, monthly, and ad-hoc workflows.

Use heuristics to classify unlabeled email. Once a GTD label already exists, respect that label unless the thread is clearly mislabeled or already represented elsewhere.

## Label Contract

| Label | Meaning | Default handling |
|---|---|---|
| `gtd/import` | Explicit task-import gate | Create or update a canonical `#task #inbox` in `Inbox.md` now. For ordinary email, dedupe by `gmail_thread_id`; for self-sent capture-alias notes, keep it as a plain capture without forced Gmail metadata. |
| `gtd/waiting` | Explicit waiting gate | Create or update a mandatory `#waiting` task now. |
| `gtd/reference` | Non-actionable but worth retaining | Archive in Gmail and keep no task. |
| `gtd/imported` | Already processed marker | Use for dedupe/post-import hygiene when available. |

Notes:

- `gtd/import` is stronger than heuristics. If a thread already has `gtd/import`, it should still create a task in `Inbox.md` unless it is a duplicate or clearly mislabeled.
- If an email is ambiguous but plausibly important, prefer `gtd/import` so it is clarified in `Inbox.md` instead of being deferred in Gmail.
- Self-sent messages to the `+gtd@gmail.com` capture alias are capture notes first, not reference emails. Import them as plain `#task #inbox` lines unless the Gmail metadata is genuinely useful.

## Recommended Capture Setup

- Gmail is the only mobile capture inbox.
- Recommended alias: `<your-address>+gtd@gmail.com`.
- Recommended filter: `to:<your-address>+gtd@gmail.com` -> apply `gtd/import`.

## Classification Defaults

| Email type | Default action | Notes / exceptions |
|---|---|---|
| Message already labeled `gtd/import` | task | Create or update a task even if the task is phrased as review. |
| Self-sent capture alias message | task | Import as a plain capture in `Inbox.md`; do not force `source:: gmail`, `gmail_thread_id`, `subject::`, or `web_link::`. |
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
| Recruiter outreach with plausible opportunity | import | Create a review-style task in `Inbox.md` unless it is clearly noise. |
| Clearly actionable message where you are the next actor | import | Create a task now. |
| Delegated thread where the next move belongs to someone else | waiting | Create or update a `#waiting` task. |
| Ambiguous but potentially relevant informational mail | import | Create a review-style task in `Inbox.md` so it gets clarified instead of deferred in Gmail. |
| Pure noise, promotion, or accepted invitation notification | trash | Recommend unsubscribe when appropriate. |

## Heuristics

Use these heuristics when deciding how unlabeled email should be labeled.

### Next-Actor Check

- If you must do the next step, prefer `gtd/import`.
- If someone else must do the next step, prefer `gtd/waiting`.
- If no action is needed now, prefer `gtd/reference` or trash instead of a separate Gmail review queue.

### Timing Check

- Ask: does this need attention before the next weekly review?
- If yes, prefer `gtd/import`.
- If no, prefer `gtd/reference` or trash unless you still need an `Inbox.md` clarify step.

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
- Archive the Gmail notification immediately, then open the Datova schranka portal to review the actual document.
- Open the Datová schránka portal to read the actual document.
- Only create a vault task if the document requires a response or action — in that case create a `#next` task with a `📅` deadline based on the document's response window.
- Do not create a task from the Gmail notification alone.

### Recruiter Heuristic

- Default recruiter outreach to `gtd/import` as a review-style task unless it is clearly noise or an immediate trash candidate.
- If a recruiter thread already has `gtd/import`, still create a task, but phrase it as a review task such as `Review recruiter outreach from <name>/<company> and send decline unless compelling`.

### LinkedIn InMail Detection

Recruiter emails that arrived as LinkedIn InMail notifications **cannot be replied to via `gws gmail +reply`** — replies must go through LinkedIn messaging.

Identify LinkedIn InMail notifications by checking the thread headers (`gws gmail users threads get`):
- `Delivered-To` ends in `+linkedin@gmail.com`, OR
- `Return-Path` contains `@bounce.linkedin.com`

Subject patterns are a weaker signal but often correlate: `"Message replied: ..."` prefix, or heavy emoji subjects like `"💬 ... 💬"`.

**Reply channel when Claude in Chrome is available:**
1. Navigate to `https://www.linkedin.com/messaging/`
2. Search for the contact by name in the messages search box (press Enter)
3. Click their thread — the URL becomes the canonical `sent_reply::` link
4. Inject message text via `javascript_tool` into `.msg-form__contenteditable` using `document.execCommand('insertText', false, text)`
5. Click Send via `find` → `computer left_click`

Log the LinkedIn thread URL as `(sent_reply:: https://www.linkedin.com/messaging/thread/...)` in the vault, same as Gmail sent links.

## Review Queue Rules

- Weekly review should sweep:
  - `gtd/import`
  - `gtd/waiting`
  - `gtd/reference`
  - unlabeled inbox older than threshold

## Billing and Time-Sensitive Mail

- A billing or statement email with an amount due, a payment failure, or a problem becomes `gtd/import`, not trash.
- A renewal notice tied to an active project becomes `gtd/import` when there is a real next step; otherwise use `gtd/reference` or trash based on retention value.
- Time-sensitive ambiguous mail should become `gtd/import` as a review-style task.

## Vault Hygiene

- Create `Inbox.md` entries for `gtd/import` items first; do not file raw Gmail imports directly into `Projects/` or `Areas/` before clarification.
- Do not use a separate Gmail review label as a holding queue; either import to `Inbox.md`, retain as `gtd/reference`, or trash.
- Keep Gmail cleanup and vault task creation aligned so the inbox state reflects actual review state.
