# Calendar Intake

## Scope

- Review upcoming Google Calendar events (today and tomorrow) that have attendees, and decide per event whether they need a GTD artifact.
- Calendar-only. Gmail intake lives in `gmail-intake.md`. Appointment-triage (service/reservation confirmations) lives in `appointment-triage.md`.
- Do not import non-attendee events (solo focus blocks, habits). Those have no GTD decision to make.
- Per-event capture mechanics (how to write the event note, where to file it, what to link) live in `event-capture.md`. This file owns the queue; `event-capture.md` owns the per-event decision.

## Step 1 — Calendar Ask Queue (Attendees Only)

1. Pull upcoming events with `gws calendar +agenda --today --format json` and `gws calendar +agenda --tomorrow --format json`.
2. Keep only events with attendees.
3. For each event, always show:
   - summary/title
   - when
   - short preview (first few lines from description/notes/location when present)
4. Pre-classify each event with recommendation and brief rationale:
   - `task` — explicit actionable follow-up needed.
   - `journal` — context only, no immediate action.
   - `project-note` — project-related context to preserve.
   - `skip` — no GTD value.
5. Review the full batch using the junk-first pattern from `gmail-intake.md § Bulk Review Pattern`:
   - Present all `skip` recommendations first; confirm in one `AskUserQuestion`.
   - Then present all non-`skip` candidates with sender, summary, preview; collect decisions via `AskUserQuestion`.
   - Apply event-note/task actions in one batch per `event-capture.md`.

## Auth and Scope Check

- Calendar ask queue requires calendar scopes. On `insufficientPermissions`, report the setup blocker and continue the daily ceremony without calendar intake.

## Output

- Calendar decisions taken and deferred.
- Any unresolved clarifications.
- Keep this output in the ceremony/session response only; do not copy it into the journal (see `conventions.md § Journal Hygiene`).
