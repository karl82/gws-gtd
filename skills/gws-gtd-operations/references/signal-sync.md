## Signal Sync Procedure

### Scope

- Mirror clarified dated GTD tasks into the `GTD Signals` Google calendar.
- Keep the vault as the only task system of record.
- Delete calendar signals when a task is completed, deleted, or no longer has the qualifying date.

### Source Rules

- Include open canonical `#task` items from:
  - `Projects/`
  - `Areas/`
  - `Journal/`
- Exclude:
  - any task containing `#inbox`
  - `Archive/`
  - `Resources/`
  - `System/`
  - completed tasks

### Signal Rules

- `#next` task -> one `NEXT: ...` signal
- If task has both `🛫 YYYY-MM-DD` and `📅 YYYY-MM-DD`, the signal spans from `🛫` to `📅`
- If task has only one of those dates, the signal collapses to that single date
- If task has neither `🛫` nor `📅`, the signal defaults to today
- `#waiting` task with `📅 YYYY-MM-DD` -> `FOLLOW UP: ...`
- `#waiting` task without a follow-up date -> no calendar signal
- Non-`#next`, non-`#waiting` tasks never appear on `GTD Signals`

### Event Rules

- Calendar: `GTD Signals`
- Event type: all-day
- Transparency: `transparent`
- Visibility: `private`
- Description: execution packet with source path plus any mobile-useful details available from the task text, such as URLs, phone numbers, and reference numbers
- Managed event metadata lives in `extendedProperties.private`
- Mobile completion marker: event summary must start with `✅`, with or without following whitespace

### Sync Behavior

1. Load desired signals from the vault.
2. Load managed events from `GTD Signals`.
3. Detect managed events whose summary starts with `✅ `.
4. Mark the matching vault task complete using the managed task id.
5. Delete successfully reconciled completed events from the calendar.
6. Create missing events.
7. Update changed events.
8. Delete orphaned events.

### Bundled Script

- Run the bundled `scripts/sync_gtd_signals.py` helper from the installed `gws-gtd-operations` skill directory.
- Claude Code example:
  - `python3 "${CLAUDE_SKILL_DIR}/scripts/sync_gtd_signals.py"`
- Claude Code apply example:
  - `python3 "${CLAUDE_SKILL_DIR}/scripts/sync_gtd_signals.py" --apply`
