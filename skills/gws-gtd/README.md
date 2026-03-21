# gws-gtd

Unified skill for the opinionated `gws-gtd` workflow. Integrates GTD vault conventions with Google Workspace (`gws`) into one operating model.

## Permissions

Recommended minimum OAuth scopes for ceremony use:

- `https://www.googleapis.com/auth/gmail.modify` — read mail, apply/remove labels during classification and import
- `https://www.googleapis.com/auth/calendar.readonly` — attendee-event review in daily intake
- `https://www.googleapis.com/auth/contacts.readonly` — People linking lookups against Google Contacts
- `https://www.googleapis.com/auth/gmail.send` — sending or replying to emails via `gws`

Optional scopes (only if you enable those features):

- `https://www.googleapis.com/auth/calendar.events` — writing signal events or event notes back to calendar
- `https://www.googleapis.com/auth/gmail.settings.basic` — creating or updating Gmail filters such as the `+gtd` capture alias rule
- `https://www.googleapis.com/auth/contacts` — creating or updating Google Contacts (not just reading)

Not needed for GTD ceremonies:

- `https://www.googleapis.com/auth/tasks`
- `https://www.googleapis.com/auth/cloud-platform`
- Docs/Drive write scopes (required by `gws-doc-review-sync`, not by core ceremonies)

## Capture Model

- Gmail is the only mobile capture channel.
- GTD Gmail labels are structured under the parent label `gtd`.
- Recommended capture alias: `<your-address>+gtd@gmail.com`.
- Create a Gmail filter for `to:<your-address>+gtd@gmail.com` that applies `gtd/import`.
- Use `gtd/waiting` only for real waiting threads or messages that should become mandatory `#waiting` items.

## Calendar Signal Model

- `GTD Signals` is output-only and mirrors only clarified `#next` tasks plus dated `#waiting` follow-ups.
- Mirror only dated actions from trusted lists, not raw inbox capture.
- Waiting items appear on `GTD Signals` only when they have a follow-up date.
- Non-waiting tasks must have `#next` to appear on `GTD Signals`.
- Do not mirror tasks already backed by a real calendar event (`source:: calendar`, `calendar_id::`, `event_id::`).

## Task Lifecycle Placement

- One canonical task record per commitment; no duplicate tasks across notes.
- Capture state is `#inbox` and may appear in any note.
- Daily clarify processes all open `#task #inbox` lines across the vault.
- On clarification, remove `#inbox` and either move the task to `Projects/`/`Areas/` or keep it in place with `[[Projects/...]]` or `[[Areas/...]]` link.
- Track lifecycle on the same task line (`➕`, `🛫`, `✅`, `📅`).
- When a task is blocked by another task, use Tasks dependency markers: `🆔 blocker-id` and `⛔ blocker-id` (or Dataview `id` / `dependsOn`).
- Journal entries should be narrative context, not duplicate `#task` copies.

## People Notes Sync Rule

- Google Contacts is the source of truth for contact details.
- Preserve only stable references in `People/` notes:
  - frontmatter: `google_contact_id`, `last_contact_sync`
  - note body: `Contact: [Google Contact](...)`
- Do not copy email addresses or phone numbers from Google Contacts into `People/` notes.

## GTD Signals Sync

Use the bundled script from the installed `gws-gtd` skill directory:

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/sync_gtd_signals.py"
python3 "${CLAUDE_SKILL_DIR}/scripts/sync_gtd_signals.py" --apply
```

- Dry run is the default.
- `--apply` creates, updates, and deletes managed events.

See `references/signal-sync.md` for full sync rules.

## GTD Label Bootstrap

Canonical label meaning and triage rules live in `references/email-triage-policy.md`.

Create the parent label first, then child labels:

```
gtd
gtd/import
gtd/waiting
gtd/reference
gtd/imported
```

Apply the same parent-first order on any Google account that uses this workflow.

## Re-auth with Least Privilege

```bash
gws auth logout
gws auth login --scopes "https://www.googleapis.com/auth/gmail.modify,https://www.googleapis.com/auth/gmail.send,https://www.googleapis.com/auth/calendar.readonly,https://www.googleapis.com/auth/contacts.readonly"
gws auth status
```

To preserve a broad existing scope set and add contacts read access:

```bash
gws auth logout
gws auth login --scopes "email,openid,https://www.googleapis.com/auth/calendar,https://www.googleapis.com/auth/cloud-platform,https://www.googleapis.com/auth/contacts.readonly,https://www.googleapis.com/auth/gmail.compose,https://www.googleapis.com/auth/gmail.insert,https://www.googleapis.com/auth/gmail.labels,https://www.googleapis.com/auth/gmail.modify,https://www.googleapis.com/auth/gmail.readonly,https://www.googleapis.com/auth/gmail.send,https://www.googleapis.com/auth/gmail.settings.basic,https://www.googleapis.com/auth/gmail.settings.sharing,https://www.googleapis.com/auth/tasks,https://www.googleapis.com/auth/userinfo.email"
gws auth status
```

## Verification Checks

```bash
gws auth status
gws gmail +triage --max 5 --query 'label:gtd/import -label:gtd/imported'
gws gmail +triage --max 5 --query 'label:gtd/waiting'
gws calendar +agenda --days 2 --format table
gws people people connections list --params '{"resourceName":"people/me","personFields":"names,emailAddresses","pageSize":10}'
```

## Ad-Hoc Maintenance

- Prefer read-only inspection first: `+triage`, `threads.list`, `threads.get`, `messages.get`.
- Prefer reversible cleanup next: `threads.modify`, `threads.trash`, or `messages.batchModify` with `TRASH` for reviewed sets.
- When an email-driven task is done and no follow-up is expected, archive by removing `INBOX` from the thread.
- For command recipes (cleaning old promotions, archiving stale notifications, checking unsubscribe headers), see `references/command-reference.md`.
