# gws-gtd

Unified skill for the opinionated `gws-gtd` workflow. Integrates GTD vault conventions with Google Workspace (`gws`) into one operating model.

This skill is self-contained for core Gmail, Calendar, People, and shared Google Workspace operations. Use `references/gmail-commands.md`, `references/calendar-commands.md`, and `references/people-commands.md` for the canonical `gws` command surface instead of installing generated `gws-*` skills.

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
| Capture model | `references/conventions.md` (Gmail Label Model), `references/gmail-intake.md` |
| Calendar signal model | `references/conventions.md` (Calendar Model), `references/signal-sync.md` |
| Task lifecycle | `references/canonical-vault.md` (Task Syntax, Inbox Rules), `references/conventions.md` |
| People notes sync | `references/people-linking.md` |
| Label bootstrap | `references/gmail-intake.md` (Step 0), `references/email-triage-policy.md` |
| Gmail commands | `references/gmail-commands.md` |
| Calendar commands | `references/calendar-commands.md` |
| People commands | `references/people-commands.md` |

## GTD Signals Sync

Use the bundled script from the installed `gws-gtd` skill directory:

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/sync_gtd_signals.py"
python3 "${CLAUDE_SKILL_DIR}/scripts/sync_gtd_signals.py" --apply
```

- Dry run is the default.
- `--apply` creates, updates, and deletes managed events.

See `references/signal-sync.md` for full sync rules.

## Generated GWS Skills

Generated `gws-*` skills are no longer part of the normal `gws-gtd` setup. The maintained path is the command reference bundled with this skill.
