# Quick Tasks (Inline Handlers)

Handle these requests inline in the assistant turn. Do not dispatch a ceremony sub-agent. Each handler is a micro-procedure that completes within the current turn.

Dispatch tree: match user intent against the table below top-to-bottom; first match wins. If no row matches, fall through to a ceremony (see `assistant.md § Ceremonies`).

## Inline intents

| Intent | Action |
|---|---|
| Capture / journal entry | Invoke the `journaling` skill. Append the captured item to today's daily note at `Journal/YYYY-MM-DD.md` (see `canonical-vault.md § Journal Paths`). For self-capture items that are tasks rather than log entries, route to `Inbox.md` for later clarify — see `canonical-vault.md § Inbox Rules`. Do not invent deadlines. |
| Next actions | Read `#task` lines from every file under `Areas/` and `Projects/`. Exclude tasks tagged `#waiting` or already completed. Rank by: (a) dated and due today or earlier, (b) tagged `#next`, (c) project most recently modified. Return the top 3 with the owning note path and one-line context. |
| Project status | Read the project note at its canonical path (see `canonical-vault.md § Canonical Project Model`). Summarize open `#task` lines, last journal link, and current stalled state using the thresholds in `conventions.md § Stalled Thresholds`. Return 2-4 sentences; do not rewrite the note. |
| Inbox triage | Walk items in `Inbox.md` one at a time. For each item, invoke `AskUserQuestion` with clarify options (next action / project / waiting / someday / trash). Apply the chosen option via a minimal edit. Stop when the user says stop or `Inbox.md` has zero `#inbox` items. |
| General GTD question | Answer using gws-gtd conventions. Cite the canonical reference file by name (e.g. `conventions.md § Tag Taxonomy`, `canonical-vault.md § Inbox Rules`). Do not restate the rule in full; link by name. |

## Guardrails

See `conventions.md § Interactive Decisions` and `conventions.md § Anti-Rules`.
