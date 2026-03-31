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

## Cross-References

| Topic | Reference |
|-------|-----------|
| Capture model | `references/conventions.md` (Gmail Label Model), `references/daily-intake.md` |
| Calendar signal model | `references/conventions.md` (Calendar Model), `references/signal-sync.md` |
| Task lifecycle | `references/canonical-vault.md` (Task Syntax, Inbox Rules), `references/conventions.md` |
| People notes sync | `references/people-linking.md` |
| Label bootstrap | `references/daily-intake.md` (Step 0), `references/email-triage-policy.md` |

## GTD Signals Sync

Use the bundled script from the installed `gws-gtd` skill directory:

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/sync_gtd_signals.py"
python3 "${CLAUDE_SKILL_DIR}/scripts/sync_gtd_signals.py" --apply
```

- Dry run is the default.
- `--apply` creates, updates, and deletes managed events.

See `references/signal-sync.md` for full sync rules.

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
