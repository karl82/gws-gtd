## Conventions

`gws-gtd` is an opinionated GTD-on-Google-Workspace workflow. These conventions are fixed package doctrine, not per-vault configuration.

### Canonical Task Syntax

- Task marker: `#task`
- Capture state: `#inbox`
- Action-now marker: `#next`
- Delegated/external dependency marker: `#waiting`
- Keep one canonical task line per commitment.
- Track lifecycle on that same line using `➕`, `🛫`, `✅`, and `📅`.

### Gmail Label Model

- Root label: `gtd`
- Intake gate: `gtd/import`
- Waiting gate: `gtd/waiting`
- Deferred review queue: `gtd/review`
- Reference retention: `gtd/reference`
- Post-import dedupe marker: `gtd/imported`

### Calendar Model

- Signal calendar: `GTD Signals`
- `GTD Signals` is output-only.
- Mirror clarified dated `#next` tasks and dated `#waiting` follow-ups only.

### Vault Model

- Canonical folders: `Projects/`, `Areas/`, `People/`, `Resources/`, `Archive/`, `Journal/`, `System/`
- `System/Templates/` and `System/Queries/` are runtime assets.
- Workflow doctrine lives in package skill references, not in `System/` config notes.
