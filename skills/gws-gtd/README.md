# gws-gtd

Unified skill for the opinionated `gws-gtd` workflow. Integrates GTD vault conventions with Google Workspace (`gws`) into one operating model.

This skill assumes the upstream Google Workspace native skills are installed in the workspace and used directly for Gmail, Calendar, People, and shared operations.

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

## Install Upstream GWS Skills

Use the bundled installer when you want GTD-relevant Google Workspace skills from `googleworkspace/cli` in a consumer workspace such as `~/src/cml`:

```bash
bash <installed-gws-gtd-skill-dir>/scripts/install_gws_skills.sh
```

Defaults:

- workspace: `~/src/cml`
- source: `https://github.com/googleworkspace/cli`
- obsidian MCP: install a local Claude `obsidian` MCP entry if missing
- agents: `claude-code`
- skills: the built-in GTD-oriented Google Workspace bundle defined in `scripts/install_gws_skills.sh`

Useful variants:

```bash
bash <installed-gws-gtd-skill-dir>/scripts/install_gws_skills.sh --dry-run
bash <installed-gws-gtd-skill-dir>/scripts/install_gws_skills.sh --list
bash <installed-gws-gtd-skill-dir>/scripts/install_gws_skills.sh --skip-obsidian-mcp
bash <installed-gws-gtd-skill-dir>/scripts/install_gws_skills.sh --workspace ~/src/cml --skill gws-drive
```

Project installs land in Claude's local skill directory:

- Claude: `.claude/skills/`

After installation, use the upstream native skills directly from Claude rather than invoking raw `gws` CLI commands from this skill.
