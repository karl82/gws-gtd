# gtd

Single-skill GTD operating model for an Obsidian vault, integrated with Gmail and Google Calendar via the [`gws`](https://github.com/googleworkspace/cli) CLI.

## What this skill does

Runs GTD ceremonies (daily, weekly, monthly, organizing) inside an Obsidian vault. Processes Gmail into vault tasks. Mirrors dated tasks to a `GTD Signals` Google Calendar. Acts as a persistent assistant for "what should I work on?" queries between ceremonies.

## Files

- `SKILL.md` — entry point, when-to-use, procedure summary
- `reference.md` — full operating model (~640 lines, single file by design)
- `triage-policy.md` — email classification table + heuristics
- `commands.md` — `gws` Gmail/Calendar/People API mechanics
- `scripts/sync_signals.py` — calendar sync helper

## Permissions

Recommended minimum OAuth scopes:

- `https://www.googleapis.com/auth/gmail.modify` — read mail, apply/remove labels during classification
- `https://www.googleapis.com/auth/calendar.readonly` — attendee event review in daily intake
- `https://www.googleapis.com/auth/contacts.readonly` — People linking lookups

Optional scopes for active features:

- `https://www.googleapis.com/auth/calendar.events` — writing signal events to `GTD Signals` calendar
- `https://www.googleapis.com/auth/gmail.send` — sending replies via `gws`
- `https://www.googleapis.com/auth/gmail.settings.basic` — creating Gmail filters (e.g. for the `+gtd` capture alias)
- `https://www.googleapis.com/auth/contacts` — creating/updating Google Contacts

## Slash commands

- `/gtd` — main entry. Takes optional argument: `daily`, `weekly`, `monthly`, `organize`. Defaults to assistant mode.
- `/gtd-sweep` — narrow Gmail inbox junk-only sweep. Use via `/loop 2h /gtd-sweep` for ongoing maintenance.
- `/gtd-drain` — one-shot bulk drain for backlogged inboxes. Wraps `/gtd-sweep` in a ralph-loop.

## GTD Signals sync

Use the bundled script:

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/sync_signals.py"          # dry-run
python3 "${CLAUDE_SKILL_DIR}/scripts/sync_signals.py" --apply  # create/update/delete events
```

See `reference.md § Signal sync` for details.

## Cross-references

| Topic | File |
|-------|------|
| Vault structure, tag taxonomy, ceremonies, Gmail intake, calendar intake, signal sync, assistant mode, anti-rules | `reference.md` |
| Email classification table, heuristics, label contract | `triage-policy.md` |
| `gws` API gotchas | `commands.md` |
