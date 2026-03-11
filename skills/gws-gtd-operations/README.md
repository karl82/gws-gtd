# gws-gtd-operations

This skill integrates Google Workspace (`gws`) into the opinionated `gws-gtd` GTD workflow.

## Permissions

For the current workflow, your token is broader than necessary.

Recommended minimum scopes for ceremony use:

- `https://www.googleapis.com/auth/gmail.modify`
  - needed for reading mail and applying/removing labels during classification/import
- `https://www.googleapis.com/auth/calendar.readonly`
  - needed for attendee-event review in daily intake
- `https://www.googleapis.com/auth/contacts.readonly`
  - needed for People linking lookups against Google Contacts
- `https://www.googleapis.com/auth/gmail.send`
  - needed when sending or replying to emails via `gws`
- `https://www.googleapis.com/auth/contacts`
  - needed when creating or updating Google Contacts, not just reading them

Optional scopes (only if you enable those features):

- `https://www.googleapis.com/auth/calendar.events`
  - only if writing signal events or event notes back to calendar
- `https://www.googleapis.com/auth/gmail.settings.basic`
  - only if creating or updating Gmail filters such as the `+gtd` capture alias rule

Not needed for current ceremony flow:

- `https://www.googleapis.com/auth/tasks`
- Gmail send/compose/insert/settings scopes
- `https://www.googleapis.com/auth/cloud-platform`
- Docs/Drive write scopes

## Capture Model

- Use Gmail as the only mobile capture channel.
- GTD Gmail labels are structured under the parent label `gtd`.
- Recommended capture alias: `karel.rank+gtd@gmail.com`.
- Create a Gmail filter for `to:karel.rank+gtd@gmail.com` that applies `gtd/import`.
- Use `gtd/waiting` only for real waiting threads or messages that should become mandatory `#waiting` items.

## Replying to Existing Email Threads

- Reuse the existing Gmail thread whenever you reply to an existing conversation.
- Do not use `gws gmail +send` for replies; it is appropriate for new standalone outbound mail and may fork the conversation into a new thread.
- For replies, use raw Gmail send with:
  - the original `threadId`
  - `In-Reply-To` set to the original message `Message-ID`
  - `References` carrying the existing reference chain
- You can use the bundled `scripts/gmail_thread_reply.py` helper to build or send a correctly threaded reply.
- If you want normal reply-style context, pass `--quote` or `--quote-file` and optionally `--quote-header` so the outgoing message includes the original text as a quoted block.
- Do not use Google Tasks as a parallel capture or execution system.
- Use `references/command-reference.md` for one-off `gws` command lookup and mailbox-maintenance recipes.
- Daily intake should batch repetitive email and calendar decisions first, then apply the confirmed actions in one go.

## Calendar Signal Model

- `GTD Signals` is output-only and mirrors only clarified `#next` tasks plus dated `#waiting` follow-ups.
- Mirror only dated actions from trusted lists, not raw inbox capture.
- Waiting items should appear on `GTD Signals` only when they have a follow-up date.
- Non-waiting tasks must have `#next` to appear on `GTD Signals`.
- Do not mirror tasks that are already backed by a real calendar event (`source:: calendar`, `calendar_id::`, `event_id::`), because that creates duplicate calendar surfaces.

## Task Lifecycle Placement

- Use one canonical task record per commitment; do not duplicate tasks across notes.
- Capture state is `#inbox`, and it may appear in any note.
- Daily clarify processes all open `#task #inbox` lines across the vault.
- On clarification, remove `#inbox` and either:
  - move task to `Projects/`/`Areas/`, or
  - keep task in place with `[[Projects/...]]` or `[[Areas/...]]` link.
- Track lifecycle on the same task line (`➕`, `🛫`, `✅`, `📅`).
- When a task is blocked by another task in the vault, use Tasks dependency markers such as `🆔 blocker-id` and `⛔ blocker-id` (or Dataview `id` / `dependsOn`).
- Journal entries should be narrative context, not duplicate `#task` copies.
- Keep journal entries concise: if several same-day email/call steps belong to one project or person, collapse them into one useful narrative note unless step-by-step detail is needed for later reference. Preserve key pivots such as recommendations, decisions, handoffs, or changes in plan.

## People Notes Sync Rule

- Google Contacts is the source of truth for contact details.
- Preserve only stable references in `People/` notes:
  - frontmatter: `google_contact_id`, `last_contact_sync`
  - note body: `Contact: [Google Contact](...)`
- Do not copy email addresses or phone numbers from Google Contacts into `People/` notes, because they will drift out of sync.

## GTD Signals Sync

Use the bundled skill script:

Run the bundled `scripts/sync_gtd_signals.py` helper from the installed `gws-gtd-operations` skill directory. On Claude Code the common form is:

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/sync_gtd_signals.py"
python3 "${CLAUDE_SKILL_DIR}/scripts/sync_gtd_signals.py" --apply
```

- Dry run is the default.
- `--apply` creates, updates, and deletes managed events.

## Re-auth with least privilege

```bash
gws auth logout
gws auth login --scopes "https://www.googleapis.com/auth/gmail.modify,https://www.googleapis.com/auth/gmail.send,https://www.googleapis.com/auth/calendar.readonly,https://www.googleapis.com/auth/contacts.readonly"
gws auth status
```

## Add Contacts Read Only To Existing Broad Scope Set

If you want to preserve the current broad scope set and only add Google Contacts read access, use:

```bash
gws auth logout
gws auth login --scopes "email,openid,https://www.googleapis.com/auth/calendar,https://www.googleapis.com/auth/cloud-platform,https://www.googleapis.com/auth/contacts.readonly,https://www.googleapis.com/auth/gmail.compose,https://www.googleapis.com/auth/gmail.insert,https://www.googleapis.com/auth/gmail.labels,https://www.googleapis.com/auth/gmail.modify,https://www.googleapis.com/auth/gmail.readonly,https://www.googleapis.com/auth/gmail.send,https://www.googleapis.com/auth/gmail.settings.basic,https://www.googleapis.com/auth/gmail.settings.sharing,https://www.googleapis.com/auth/tasks,https://www.googleapis.com/auth/userinfo.email"
gws auth status
```

If you also manage the Gmail capture filter or apply `GTD Signals` writes directly, add the needed optional scopes:

```bash
gws auth login --scopes "https://www.googleapis.com/auth/gmail.modify,https://www.googleapis.com/auth/gmail.send,https://www.googleapis.com/auth/gmail.settings.basic,https://www.googleapis.com/auth/calendar.events,https://www.googleapis.com/auth/contacts.readonly"
```

## Verification checks

```bash
gws gmail +triage --max 5 --query 'label:gtd/import -label:gtd/imported'
gws gmail +triage --max 5 --query 'label:gtd/waiting'
gws calendar +agenda --days 2 --format table
gws people people connections list --params '{"resourceName":"people/me","personFields":"names,emailAddresses","pageSize":10}'
```

## Ad-hoc maintenance

- Prefer read-only inspection first: `+triage`, `threads.list`, `threads.get`, `messages.get`.
- Prefer reversible cleanup next: `threads.modify` or `threads.trash`.
- When an email-driven task is done and no immediate follow-up is expected, archive by removing `INBOX` from the thread.
- Accepted calendar invitation notification emails should be trashed by default unless they add actionable context beyond the calendar event itself.
- Use permanent delete only when explicitly requested.
- For examples such as cleaning old promotional email, archiving stale notifications, or checking unsubscribe headers, see `references/command-reference.md`.

## GTD Label Bootstrap

- Canonical label meaning and triage rules live in `System/Email Triage Policy.md`.
- Create the parent label `gtd` first.
- Then create child labels under it:
  - `gtd/import`
  - `gtd/waiting`
  - `gtd/review`
  - `gtd/reference`
  - `gtd/imported`
- Apply the same parent-first rule on any other Google account that uses this workflow.
