# Email Triage Policy

The classification table for unlabeled Gmail. Used during Gmail intake (Step 1 of the daily ceremony, and during ad-hoc junk sweeps).

For the full Gmail intake procedure, see `reference.md § Gmail integration`.

## Classification defaults

Rows are evaluated top-to-bottom. First match wins.

**Match-first is the first rule.** Before anything else, check whether the email maps to an existing `#waiting` or `#next` task in the vault (by `gmail_thread_id`, sender + project, tracking number, order number, case ID). If it does, update the matching task and skip classification. See `reference.md § Step 1 — Classify`.

| Email type | Default action | Notes / exceptions |
|---|---|---|
| Matches existing `#waiting` task by `gmail_thread_id` | match existing | Append `📝 YYYY-MM-DD: <update>` to the task. Don't auto-mark `✅` even if the email reads like resolution — ask. |
| Matches existing task by tracking / order / case ID | match existing | USPS tracking, order number, ARAG case, Calendly event ID, etc. Update the task; archive the email. |
| Calendly / Cal.com / Authentisign confirmation for a meeting/signature already in the vault | match existing + archive | Never duplicate as a new import. If a `#waiting` task exists, update it with the confirmed date. |
| Auto-reply / out-of-office bounce (vacation responder, "automatická odpověď") | trash | No content; the original outbound is what matters. |
| Reaction-only message ([like], emoji-only react from corporate platforms like Outlook) | trash | No new content. If you're tracking the conversation, the underlying thread already covers it. |
| Already labeled `gtd/import` | task | Create or update a task in `Inbox.md`, even if phrased as a review. |
| Self-sent capture-alias message (`+gtd@`) | task | Plain capture in `Inbox.md`; no `source:: gmail` / `gmail_thread_id` / `subject::` / `web_link::` metadata. |
| Already labeled `gtd/waiting` | waiting task | Create or update the waiting task immediately. |
| Statement notice (no amount due) | trash | Override only when there is an amount due, a payment failure, or a real next step. |
| Shipping notification (FedEx, UPS, USPS, Amazon shipped) | trash | Informational only — package is either arriving or arrived. Exception: if there's a matching `#waiting` task for the tracking number, match and archive. |
| Order confirmation for something you ordered yourself | waiting task | `#waiting` for delivery, with order ID + expected date if known. Examples: Apple Store, Hovia, CVS. |
| Order or reshipment in progress (awaiting tracking, warehouse processing) | waiting task | Someone else's move — `#waiting`, not `#next`. |
| Venmo payment you sent | trash | Outgoing payment confirmation. |
| Completed Airbnb post-stay message (review request, etc.) | trash | No reference value after stay. |
| Subscription or service confirmation (Prime Video, streaming) | trash | Override on unexpected charge or cancellation. |
| Insurance or travel-plan upsell | trash | Marketing by default. |
| DocuSign / Authentisign / signature platform — "Please sign" | import | Task: `Sign <document> via <platform>`. Resolve in 5 min during daily if straightforward. |
| DocuSign / Authentisign — "Completed" | reference + archive | All parties have signed. If a `#waiting` task tracked it, update + match-existing; otherwise archive. |
| DocuSign / Authentisign — "Cancelled" or superseded | trash | Often happens when the sender corrects something. Trash unless it's the only artifact of an in-flight task. |
| Tax / CPA correspondence with explicit ask or deadline | import | Time-sensitive. Always import; don't archive on read. |
| IRS / tax authority payment or filing confirmation | reference + archive | Keep for records; no task unless follow-up is required. |
| Policy, booking, or plan document worth keeping | reference + archive | Searchable, out of inbox. |
| Flight, hotel, Airbnb, car rental, campsite booking confirmation | forward to `plans@tripit.com` + archive | Forward first, then archive (NOT trash — keep for disputes, taxes, records). TripIt parses and adds to itinerary. Never create a vault task. Execute silently — don't ask the user. |
| TripIt "check out your itinerary" notification | trash | TripIt's own auto-reply after parsing. No task, no archive. |
| Brokerage order fill or partial fill notification | trash | Execution notice only. Applies to all brokerages. |
| Appointment or reservation confirmation | calendar first | If already on calendar, archive. If not, create/update the calendar event then archive. Includes first-time confirmations (PSE energy assessment, dealer service, medical). See `reference.md § Appointment triage`. |
| Airline / transport check-in reminder | trash | Flight is on calendar; reminder is transient. |
| Card security or fraud alert | import | Task: `Review [issuer] card alert — [merchant] $[amount] and confirm or dispute`. Resolve in 5 min during daily. |
| Account security notification (password change, 2FA update, new login) | import | Task: `Confirm [issuer] account security change was intentional`. Resolve in 5 min. Applies to all issuers. **Match first**: if the security event was triggered by your own action recorded elsewhere (a 2FA setup task, a password rotation), match existing and archive. |
| General service / settings-change notification | trash | Override only if unexpected or security-related. |
| Datová schránka notification | trash | Czech govt data-mailbox delivery ping. The doc lives in the portal, not in Gmail. Open the portal to read; create a `#next` task only if a response is required. |
| Class action settlement / legal notice naming you or family | import | Decision needed: file claim or skip. Capture identifiers (class member ID, deadlines) in the task. |
| Recruiter first outreach with plausible opportunity | import | Review-style task in `Inbox.md`. Trash only when bulk mail to generic address with no specific role / company fit. |
| Recruiter follow-up after you've already replied | match existing | If you previously declined or matched against an existing `Areas/Career` task, do not import again. Reply per the task's intent or trash. |
| Clearly actionable message where you are the next actor | import | Task in `Inbox.md` for clarify. |
| Delegated thread where the next move belongs to someone else | waiting | `#waiting` task. |
| Ambiguous but potentially relevant informational mail | import | Default to import so it gets clarified rather than deferred in Gmail. |
| Pure noise, promotion, or accepted invitation notification | trash | Recommend unsubscribe when `List-Unsubscribe` header is present. |

## Heuristics

Use these when no row in the table fits.

### Next-actor check

- If you must do the next step → `gtd/import`.
- If someone else must do the next step → `gtd/waiting`.
- If no action is needed → `gtd/reference` or trash.

### Timing check

- Does this need attention before the next weekly review? → `gtd/import`.
- If no → `gtd/reference` or trash.

### Existing-system check

- Already mapped to a vault task by `gmail_thread_id` → update or match the existing task.
- Already represented by a `#waiting` task → match existing, clear from intake.
- Already represented on calendar → archive, don't create vault task.

### Retention check

- Keep `gtd/reference` only when the message is useful later for proof, policy, travel, taxes, or legal.
- Don't keep generic notices that can be re-fetched or don't support a later decision.

### LinkedIn InMail detection

InMail bounces from LinkedIn cannot be replied to via `gws gmail +reply`. Detect via thread headers (`gws gmail users threads get`):

- `Delivered-To` ends in `+linkedin@gmail.com`, OR
- `Return-Path` contains `@bounce.linkedin.com`

Subject patterns are weaker but correlate: `Message replied: ...` prefix, heavy emoji subjects.

For the LinkedIn reply procedure, see `reference.md § LinkedIn InMail detection`.

## Label contract

| Label | Symbolic alias | Meaning |
|---|---|---|
| `gtd/import` | `IMPORT_LABEL` | Explicit task-import gate. Becomes a `#task #inbox` in `Inbox.md`. |
| `gtd/waiting` | `WAITING_LABEL` | Explicit waiting gate. Becomes a `#waiting` task. |
| `gtd/reference` | `REFERENCE_LABEL` | Non-actionable but worth retaining. Archive in Gmail; keep no task. |
| `gtd/imported` | `IMPORTED_LABEL` | Post-import dedupe marker (recommended; without it, dedup falls back to `gmail_thread_id` only). |

`gtd/import` is stronger than heuristics — if a thread already has it, create a task even if the task is phrased as review. Exception: duplicate by `gmail_thread_id`, or genuinely mislabeled (the label doesn't match the rule that applies).

For ambiguous mail that's plausibly important, prefer `gtd/import` over `gtd/reference` so it gets clarified in `Inbox.md` rather than deferred in Gmail.

For `garbage` decisions where `List-Unsubscribe` header is present, recommend unsubscribe as a follow-up after the trash batch is confirmed. Ask before executing the unsubscribe.
