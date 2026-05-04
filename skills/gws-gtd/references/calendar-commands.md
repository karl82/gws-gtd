# Calendar Commands

Patterns and gotchas for `gws calendar` API calls. Populate this file as Calendar mechanics are discovered during live sessions.

Always pass `--format json` and parse with `jq` in Bash. See `SKILL.md § Guardrails`.

## Agenda fetch

```bash
gws calendar +agenda --today --format json
gws calendar +agenda --tomorrow --format json
gws calendar +agenda --week --format json
```

Returns event list with `summary`, `when`, `attendees`, `description`, `location`, and `id`.

## Event creation

```bash
gws calendar +insert --summary "<title>" --start "<ISO>" --end "<ISO>" --location "<loc>" --format json
```

Used by `appointment-triage.md` when an appointment email has no matching calendar event.

## Event patch (reschedule)

```bash
gws calendar +patch --id "<event_id>" --start "<ISO>" --end "<ISO>" --format json
```

## GTD Signals calendar

`GTD Signals` is output-only. See `signal-sync.md` for the full sync algorithm, event shape, and the `scripts/sync_gtd_signals.py` helper.

## Auth and scope

Calendar operations require calendar scopes in the `gws` auth config. On `insufficientPermissions`, report the setup blocker and proceed without calendar operations.
