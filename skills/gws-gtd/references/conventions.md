# Conventions

> **Scope:** Behavioral doctrine — HOW to operate within the vault. For the structural model (task syntax, folder semantics, project/linking rules), see `canonical-vault.md`. For Gmail label mechanics, see `email-triage-policy.md`.

`gws-gtd` is an opinionated GTD-on-Google-Workspace workflow. These conventions are fixed package doctrine, not per-vault configuration. Workflow doctrine lives in package skill references, not in `System/` config notes.

## Tag Taxonomy

Tags serve two purposes only: **GTD lifecycle state** and **execution context**. Area or domain ownership is expressed exclusively via `[[wikilinks]]`, never via tags.

| Tier | Tags | Meaning |
|---|---|---|
| **GTD state** | `#task`, `#inbox`, `#next`, `#waiting`, `#someday` | Lifecycle position of the action |
| **Context / mode** | `#phone`, `#email`, `#errand`, `#internet`, `#deep`, `#buy`, `#idea`, `#payment` | How or where the action is performed |

**Rules:**

- Domain/area tags (`#home`, `#admin`, `#work`, `#personal`, etc.) are not used. Ownership is declared by wikilink (`[[Areas/Home]]`, `[[Projects/...]]`) or by the file the task lives in.
- Context tags enable execution filtering. They do not imply ownership.
- A task with no context tag is valid — not every action needs a mode signal.
- Do not invent new domain tags. If a task needs an area owner, add the wikilink.

### `#waiting` semantics

Use `#waiting` when the next step belongs to someone else: you delegated, you sent a request, you are blocked on an external party. Never use `#waiting` for tasks where you are the next actor.

### `#inbox` semantics

`#inbox` marks captures that have not been clarified. Clarify by:

1. Removing `#inbox`.
2. Adding a `[[Projects/...]]` or `[[Areas/...]]` wikilink.
3. Moving the task to its owning file, or leaving it in the journal with the wikilink if it belongs to a real-world timeline event.

Inbox tasks must never remain marked completed — either clarify and move, or delete.

## Gmail Label Model

For the full Gmail label contract, classification defaults, and heuristics, see `email-triage-policy.md`. Quick map:

- Root label: `gtd`
- Intake gate: `gtd/import` (aliased `IMPORT_LABEL`)
- Waiting gate: `gtd/waiting` (aliased `WAITING_LABEL`)
- Reference retention: `gtd/reference` (aliased `REFERENCE_LABEL`)
- Post-import dedupe marker: `gtd/imported` (aliased `IMPORTED_LABEL`)

## Calendar Model

- Signal calendar: `GTD Signals`
- `GTD Signals` is output-only — never a capture surface.
- Mirror clarified dated `#next` tasks and dated `#waiting` follow-ups only. See `signal-sync.md` for the full signal contract.

## Journal Hygiene

- Journal notes capture real-world timeline events, outcomes, and the tasks they spawn.
- `#task #inbox` lines born from real events belong in the daily journal note alongside narrative context.
- Do not write ceremony mechanics into journal notes: no inbox counts, classification summaries, label routing, task-list snapshots, or completion banners.
- Every journal entry and journal-born task must link to the relevant `[[Projects/...]]`, `[[Areas/...]]`, `[[People/...]]`, or canonical task.
- If no real-world timeline event, outcome, or named commitment occurred beyond review/maintenance, do not add a journal entry.

## Stalled Thresholds

- **14 days** without modification → warm-start flag ("stalled project"). Surfaces in assistant warm-start and in daily/weekly signals.
- **30 days** without modification → monthly review archive candidate. Surfaces in monthly portfolio audit.
- Both thresholds apply to top-level project notes in `Projects/<Domain>/*.md`.

## Anti-Rules

These apply to every ceremony, every agent, every command. Named here so other files reference by pointer instead of re-listing.

- Do not invent deadlines.
- Do not auto-complete tasks.
- Do not archive automatically.
- Do not create hidden states outside the canonical model.
- Do not convert reference notes into GTD tasks without `#task`.
- Do not rely on ambiguous short links for canonical entities.
- Do not duplicate completed tasks into the journal as additional `#task` entries.
- Do not persist ceremony mechanics to the journal (counts, label moves, import tallies, completion banners).

## User-Facing Context

- When summarizing work to the user, identify tasks and notes with enough context to be recognizable immediately.
- Do not use bare references like `Inbox.md:10` or "the item on line 10" as the main identifier.
- Pair any file reference with the task text, sender, subject, person, or linked project/area.

## Interactive Decisions

- Every user decision during a ceremony must be surfaced via the `AskUserQuestion` tool. Never ask decisions as plain text.
- Include clickable URLs (Gmail thread, calendar event, vault note path) in option descriptions.
- Exceptions: see `email-triage-policy.md § TripIt Import` for the documented silent-execution case. All other decisions go through `AskUserQuestion`.
