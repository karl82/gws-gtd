# Email Triage Policy

The classification table for unlabeled Gmail. Used during Gmail intake (Step 1 of the daily ceremony, and during ad-hoc junk sweeps).

For the full Gmail intake procedure, see `reference.md § Gmail integration`.

## Classification defaults

Rows are evaluated top-to-bottom. First match wins.

**Match-first is the first rule.** Before anything else, check whether the email maps to an existing `#waiting` or `#next` task in the vault (by `gmail_thread_id`, sender + project, tracking number, order number, case ID). If it does, update the matching task and skip classification. See `reference.md § Step 1 — Classify`.

**Pattern ledger is the second rule.** After match-first, consult the pattern ledger (see `reference.md § Pattern ledger`) keyed on `(from, pattern)`. If the (sender, pattern) pair has count ≥ 3 with consistent class and zero user overrides, classify silently with that class. Items without ledger history fall through to the table below.

Each row carries a stable `pattern` slug (first column). When the LLM matches a candidate to a row, it must emit `(class, pattern)` so the ledger can learn per (sender, pattern) — not per sender alone. This matters because the same sender (Apple, DocuSign, your bank) emits multiple patterns with different correct classes.

| Pattern | Email type | Default action | Notes / exceptions |
|---|---|---|---|
| `match-thread-id` | Matches existing `#waiting` task by `gmail_thread_id` | match existing | Append `📝 YYYY-MM-DD: <update>` to the task. Don't auto-mark `✅` even if the email reads like resolution — ask. Excluded from ledger writes. |
| `match-by-id` | Matches existing task by tracking / order / case ID | match existing | USPS tracking, order number, ARAG case, Calendly event ID, etc. Update the task; archive the email. Excluded from ledger writes. |
| `match-calendly` | Calendly / Cal.com / Authentisign confirmation for a meeting/signature already in the vault | match existing + archive | Never duplicate as a new import. If a `#waiting` task exists, update it with the confirmed date. Excluded from ledger writes. |
| `auto-reply` | Auto-reply / out-of-office bounce (vacation responder, "automatická odpověď") | trash | No content; the original outbound is what matters. |
| `reaction-only` | Reaction-only message ([like], emoji-only react from corporate platforms like Outlook) | trash | No new content. If you're tracking the conversation, the underlying thread already covers it. |
| `label-import` | Already labeled `gtd/import` | task | Create or update a task in `Inbox.md`, even if phrased as a review. Excluded from ledger writes (label-driven, not pattern-driven). |
| `self-capture` | Self-sent capture-alias message (`+gtd@`) | task | Plain capture in `Inbox.md`; no `source:: gmail` / `gmail_thread_id` / `subject::` / `web_link::` metadata. Excluded from ledger writes. |
| `label-waiting` | Already labeled `gtd/waiting` | waiting task | Create or update the waiting task immediately. Excluded from ledger writes. |
| `statement-notice` | Statement notice (no amount due) | trash | Override only when there is an amount due, a payment failure, or a real next step. |
| `shipping-notification` | Shipping notification (FedEx, UPS, USPS, Amazon shipped) | trash | Informational only — package is either arriving or arrived. Exception: if there's a matching `#waiting` task for the tracking number, match and archive. |
| `order-confirmation` | Order confirmation for something you ordered yourself | waiting task | `#waiting` for delivery, with order ID + expected date if known. Examples: Apple Store, Hovia, CVS. |
| `order-in-progress` | Order or reshipment in progress (awaiting tracking, warehouse processing) | waiting task | Someone else's move — `#waiting`, not `#next`. |
| `venmo-sent` | Venmo payment you sent | trash | Outgoing payment confirmation. |
| `airbnb-poststay` | Completed Airbnb post-stay message (review request, etc.) | trash | No reference value after stay. |
| `subscription-confirmation` | Subscription or service confirmation (Prime Video, streaming) | trash | Override on unexpected charge or cancellation. |
| `subscription-renewal` | Subscription renewal upcoming notice ("will renew soon") | import if decision pending, else trash | Import when you haven't decided whether to keep or cancel. Trash when the subscription is intentional and no decision is needed. Mixed-class — never promoted. |
| `insurance-upsell` | Insurance or travel-plan upsell | trash | Marketing by default. |
| `signing-request-pending` | DocuSign / Authentisign / signature platform — "Please sign" | import | Task: `Sign <document> via <platform>`. Resolve in 5 min during daily if straightforward. |
| `signing-request-completed` | DocuSign / Authentisign — "Completed" | reference + archive | All parties have signed. If a `#waiting` task tracked it, update + match-existing; otherwise archive. |
| `signing-request-cancelled` | DocuSign / Authentisign — "Cancelled" or superseded | trash | Often happens when the sender corrects something. Trash unless it's the only artifact of an in-flight task. |
| `tax-cpa-correspondence` | Tax / CPA correspondence with explicit ask or deadline | import | Time-sensitive. Always import; don't archive on read. Content varies — never promoted. |
| `irs-tax-confirmation` | IRS / tax authority payment or filing confirmation | reference + archive | Keep for records; no task unless follow-up is required. |
| `policy-or-plan-doc` | Policy, booking, or plan document worth keeping | reference + archive | Searchable, out of inbox. Content varies — never promoted. |
| `tripit-forward` | Flight, hotel, Airbnb, car rental, campsite booking confirmation | forward to `plans@tripit.com` + archive | Forward first, then archive (NOT trash — keep for disputes, taxes, records). TripIt parses and adds to itinerary. Never create a vault task. Execute silently — don't ask the user. Special action — never promoted. |
| `tripit-itinerary-notification` | TripIt "check out your itinerary" notification | trash | TripIt's own auto-reply after parsing. No task, no archive. |
| `brokerage-fill` | Brokerage order fill or partial fill notification | trash | Execution notice only. Applies to all brokerages. |
| `appointment-confirmation` | Appointment or reservation confirmation | calendar first | If already on calendar, archive. If not, create/update the calendar event then archive. Includes first-time confirmations (PSE energy assessment, dealer service, medical). See `reference.md § Appointment triage`. Calendar action — never promoted. |
| `airline-checkin-reminder` | Airline / transport check-in reminder | trash | Flight is on calendar; reminder is transient. |
| `card-security-alert` | Card security or fraud alert | import or trash | If the merchant is recognizable and the amount is expected (e.g. Uber Eats charge matching a same-day Uber Eats receipt), trash silently — no task, no ask. Only import when the merchant or amount is genuinely unfamiliar. Task if imported: `Review [issuer] card alert — [merchant] $[amount] and confirm or dispute`. Mixed-class — never promoted. |
| `account-security-notification` | Account security notification (password change, 2FA update, new login) | import or trash | Import only when the change is unexpected. If the email itself says "if you did this, disregard" and you recognize the action, trash silently. Task if imported: `Confirm [issuer] account security change was intentional`. **Match first**: if triggered by your own recorded action, match existing and archive. Mixed-class — never promoted. |
| `family-account-security-alert` | Google/Apple/platform security alert for an account where the owner is recovery contact (not their own account, e.g. family member's account) | trash | Not actionable by the owner — the account holder must act. |
| `general-service-notification` | General service / settings-change notification | trash | Override only if unexpected or security-related. Sender-driven, not subject-driven — ledger-only, never promoted. |
| `datova-schranka-notification` | Datová schránka notification | trash | Czech govt data-mailbox delivery ping. The doc lives in the portal, not in Gmail. Open the portal to read; create a `#next` task only if a response is required. |
| `school-portal-notification` | School parent/communication system notification (Bakaláři, Komens, iParent, etc.) | trash | Delivery ping only — the actual message lives in the school portal. Open the portal to read; create a `#next` task only if a response or action is required. Sender-driven — ledger-only, never promoted. |
| `recall-notice` | Product safety recall notice (CPSC, manufacturer) | reference + archive | Archive as `gtd/reference`. Create a `#next` task only if a replacement or remediation action is required (e.g. mandatory stop-use, return label, repair appointment). Content varies — never promoted. |
| `class-action-notice` | Class action settlement / legal notice naming you or family | import | Decision needed: file claim or skip. Capture identifiers (class member ID, deadlines) in the task. Content varies — never promoted. |
| `recruiter-first-outreach` | Recruiter first outreach with plausible opportunity | import | Review-style task in `Inbox.md`. Trash only when bulk mail to generic address with no specific role / company fit. Content varies — never promoted. |
| `recruiter-followup` | Recruiter follow-up after you've already replied | match existing | If you previously declined or matched against an existing `Areas/Career` task, do not import again. Reply per the task's intent or trash. |
| `actionable-next-actor` | Clearly actionable message where you are the next actor | import | Task in `Inbox.md` for clarify. Generic — never promoted. |
| `delegated-thread` | Delegated thread where the next move belongs to someone else | waiting | `#waiting` task. Generic — never promoted. |
| `ambiguous-informational` | Ambiguous but potentially relevant informational mail | import | Default to import so it gets clarified rather than deferred in Gmail. Generic — never promoted. |
| `noise-promo` | Pure noise, promotion, or accepted invitation notification | trash | Recommend unsubscribe when `List-Unsubscribe` header is present. Sender-driven — ledger-only, never promoted (subjects are too varied for a safe filter). |

## Heuristics

Use these when no row in the table fits.

### Importance order — surface high-signal items first

Before presenting any batch to the user, sort by impact:
1. **Security / financial alerts** with unrecognized merchants or unexpected amounts
2. **Signing deadlines** or time-sensitive decisions (DocuSign, mortgage, legal)
3. **Service appointments** or pickups happening today or tomorrow
4. **Project-relevant updates** (replies from counterparties, document delivery)
5. **Routine garbage** — present last as a bulk confirm

Don't bury a signing deadline behind 18 newsletters.

### Archive vs. trash

`gtd/reference` is for things you may need to look up later (policy docs, travel confirmations, tax records). Everything else is trash. Default to trash for:
- Payment confirmations for transactions you initiated (Venmo sent, Zelle sent, card receipts)
- Auto-replies and out-of-office bounces
- Routine deposit / statement / score-change notifications
- Delivery notifications once the item has arrived or been actioned
- Security notifications you recognize and have resolved

When in doubt: if you'd never search for this email again, trash it.

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

### People/ record creation

- Only create a `People/` file for contacts with an ongoing relationship relevant to a project or area.
- Do NOT create `People/` records for recruiters, one-off contacts, or low-stakes interactions.

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

## Filter keywords

Patterns listed here are eligible for Gmail filter promotion (see `reference.md § Pattern ledger § Step 5`). Patterns NOT in this table are auto-classified by the ledger but never promoted — either because the class varies with content (`card-security-alert`), the action is special (`tripit-forward` forwards before archive), or the subject space is too varied for a safe filter (`noise-promo`).

A promoted filter always combines `from:<sender>` AND the subject keywords below, so promoting one pattern from a sender never affects other patterns from the same sender.

| Pattern | Subject keywords (Gmail filter syntax) |
|---|---|
| `auto-reply` | `subject:("Out of Office" OR "Auto-Reply" OR "automatická odpověď" OR "Automatic reply")` |
| `statement-notice` | `subject:(statement OR "monthly statement" OR "is available" OR "is ready")` |
| `shipping-notification` | `subject:(shipped OR delivered OR "out for delivery" OR "on its way" OR "has shipped")` |
| `venmo-sent` | `subject:("you paid" OR "you completed your payment" OR "payment to")` |
| `airbnb-poststay` | `subject:("how was your stay" OR "review your stay" OR "share your experience")` |
| `subscription-confirmation` | `subject:(receipt OR "your subscription" OR "is confirmed" OR "thanks for your purchase")` |
| `insurance-upsell` | `subject:("trip protection" OR "travel insurance" OR "protect your" OR "insurance offer")` |
| `signing-request-completed` | `subject:("Completed:" OR "All parties have signed" OR "Completed by")` |
| `signing-request-cancelled` | `subject:(Cancelled OR Voided OR "has been voided" OR "envelope canceled")` |
| `irs-tax-confirmation` | `subject:("payment received" OR "filing accepted" OR "confirmation number")` |
| `tripit-itinerary-notification` | `subject:("Your TripIt" OR "check out your itinerary" OR "trip on TripIt")` |
| `brokerage-fill` | `subject:(filled OR "partial fill" OR "trade execution" OR "order executed")` |
| `airline-checkin-reminder` | `subject:("check in" OR "check-in" OR "ready for check-in" OR "time to check in")` |
| `family-account-security-alert` | `subject:("security alert" OR "new sign-in" OR "new device")` |
| `datova-schranka-notification` | `subject:("Doručena datová zpráva" OR "datová schránka" OR "datová zpráva")` |
