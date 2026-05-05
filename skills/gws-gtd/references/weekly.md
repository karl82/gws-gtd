# Weekly Review

## Scope

- Run the weekly GTD review cycle against `canonical-vault.md` structure and `System/Templates/Weekly Review.md`.
- Extend the vault sweep with Google inbox safety nets so no Gmail or Calendar input remains outside GTD control.
- Enforce `#inbox` zero as a strict exit gate for Get Clear.
- Cross-reference `canonical-vault.md` for structural rules and `System/Templates/Weekly Review.md` for the agenda sections.

## Template Incorporation

- Use a review note path that matches `^Journal(?:/.+)?/\d{4}-W\d{2}\.md$`.
- If the weekly note does not exist, create it at a matching path so Templater applies `System/Templates/Weekly Review.md`.
- Use the template sections as the interactive agenda.

## Steps

1. Get Clear
   - Run a mind sweep — capture anything untracked as `#task #inbox` before processing:
     - Open browser tabs, recent meeting notes, physical inboxes.
     - Open commitments to others (promises, delegations, replies owed).
     - Upcoming events or deadlines not yet reflected in tasks.
     - People to follow up with.
     - Ideas, projects, or improvements currently in mind.
   - Drive `#inbox` to zero as a strict gate. Clarify each ambiguous capture into an explicit outcome plus either a `#task` next action or a plain local checklist step.
   - If `#inbox` is not zero at the end of this step, stop and report: `Get Clear incomplete (#inbox not zero)`.
2. Get Current
   - Review overdue and next-7-day due tasks.
   - Review `#waiting` items (full reconciliation handled in the Waiting Reconciliation section below).
   - Review possible next-step candidates and promote at most five to `#next`.
   - Surface stalled projects: open projects past the warm-start threshold (see `conventions.md § Stalled Thresholds`) OR with no open linked `#task`.
3. Get Creative
   - Review journal patterns from the week: recurring blockers, energy dips, repeated themes.
   - Scan `#someday` items; promote items with a concrete next action to active `#task`, or delete items stale >90 days with no supporting notes.
   - Recommend top 3 outcomes for next week, each expressible as a single verb phrase.
4. Gmail Reconcile
   - Run the unresolved-intake queries from `gmail-intake.md § Waiting Follow-Up Signals` and the queue queries defined there; label mechanics live in `email-triage-policy.md § Label Contract`.
   - Target queues:
     - Captures still needing clarification: `label:<IMPORT_LABEL> -label:<IMPORTED_LABEL>`.
     - Stale unlabeled inbox: `in:inbox older_than:7d -label:<IMPORT_LABEL> -label:<IMPORTED_LABEL> -label:<WAITING_LABEL> -label:<REFERENCE_LABEL>`.
   - For each stale intake candidate decide `IMPORT_LABEL`, `WAITING_LABEL`, `REFERENCE_LABEL`, or trash per `email-triage-policy.md § Classification Defaults`. Use `IMPORT_LABEL` for anything that still needs an `Inbox.md` clarify step.
5. Calendar Pressure Check
   - Pull the weekly agenda with `gws calendar +agenda --week --format json`.
   - Compare meeting load with due-date clusters in the vault.
   - Flag overloaded days and list redistribution candidates (tasks, meetings, or commitments movable to lower-load days).
6. Integrity Checks
   - Confirm `#inbox` zero was reached in Step 1; if any `#inbox` regressed during review, re-drain before exit.
   - Surface orphan tasks per `canonical-vault.md § Orphan Tasks`.
   - Keep one canonical task line per commitment per `canonical-vault.md § Task Syntax`; do not duplicate tasks between Journal and project/area notes.

## Waiting Reconciliation

- List open tasks containing `#waiting` with `source:: gmail`.
- Surface items with no progress signals and no due date; decide per item: keep, re-sequence, escalate to owner, or drop.
- Confirm that dated `#next` and dated `#waiting` tasks are the only ones mirrored into `GTD Signals` per `signal-sync.md § Signal Rules`.
- Do not auto-complete waiting tasks — see `conventions.md § Anti-Rules`.

## Guardrails

See `conventions.md § Anti-Rules`. Additionally: Analytical assistant, not decision-maker. Keep recommendations tied to due dates, explicit priority markers, and project value. Exclude plain checklist items from global task counts.

## Output

- Weekly health snapshot.
- Stalled or stale exceptions.
- Proposed top 3 outcomes.
- Count of reviewed deferred/unlabeled emails.
- Waiting loop risks and owner/follow-up decision points.
- Calendar load risks for the next 7 days.
- Hybrid inbox/orphan integrity actions performed.
