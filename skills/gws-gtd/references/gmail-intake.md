# Gmail Intake

## Scope

- Extend the daily GTD ceremony with Gmail-only intake.
- Keep vault tasks as the only execution system.
- Treat Gmail as the only mobile capture inbox; do not import from Google Tasks.
- `GTD Signals` is output-only and must never be treated as capture.
- Use classify-then-import so the user reviews email quality before labels drive automation.
- Use `email-triage-policy.md` as the canonical source for label meanings, classification defaults, and heuristics.
- Use `gmail-commands.md` as the canonical Gmail `gws` execution reference.
- Calendar intake lives in `calendar-intake.md`. Appointment-triage lives in `appointment-triage.md`.

Default label mapping for this procedure:

- `ROOT_LABEL = "gtd"`
- `IMPORT_LABEL = "gtd/import"`
- `WAITING_LABEL = "gtd/waiting"`
- `REFERENCE_LABEL = "gtd/reference"`
- `IMPORTED_LABEL = "gtd/imported"` (required — see Step 0)

Capture alias filter setup: see `email-triage-policy.md § Recommended Capture Setup`.

## Step 0 — Label Bootstrap and Mapping

1. Verify label availability using `gws gmail users labels list` from `gmail-commands.md`.
2. `IMPORTED_LABEL` (`gtd/imported`) is required. If missing, create it before proceeding — do not skip. `IMPORTED_LABEL` enforces dedupe across ceremonies; without it, Step 4 cannot move imported threads out of the import queue and re-imports become possible.
3. If other mapped labels are missing, choose one per label:
   - Map to an existing mailbox label.
   - Create the missing structured `gtd` label.
4. When bootstrapping structured labels, create `ROOT_LABEL` first, then create child labels under it (`gtd/import`, `gtd/waiting`, `gtd/reference`, `gtd/imported`).
5. Persist the chosen mapping in ceremony context for this run.

## Step 1 — Classification Queue (Before Import)

1. Pull unlabeled inbox candidates:
   - `in:inbox -label:<IMPORT_LABEL> -label:<WAITING_LABEL> -label:<REFERENCE_LABEL> -label:<IMPORTED_LABEL>`
   - Omit any filter whose label is not configured.
   - Do NOT add time filters like `newer_than:2d` — process all inbox threads regardless of age.

   Efficient snippet retrieval: to get snippets for all candidate threads in one API call, use

   ```
   gws gmail users threads list --params '{"userId":"me","q":"<same query>","maxResults":500}' --format json
   ```

   This returns `id` + `snippet` for all threads. Join with `+triage` output on thread ID to get subject + sender + snippet together. Do NOT call `messages.list` (returns IDs only) or `messages.get` per-message (expensive). Only call `+read` or `messages.get format=metadata` when the snippet is insufficient for a decision.

2. For each candidate, always show sender, subject, and short preview (first few lines/snippet).

3. Use a Sonnet-class model for classification. Haiku-class models produce unreliable results for email triage (over-classify as import). Always classify with Sonnet.

   Propose one outcome and brief rationale per candidate, using the policy defaults and heuristics from `email-triage-policy.md`. Allowed outcomes in this procedure:
    - `IMPORT_LABEL`
    - `WAITING_LABEL`
    - `appointment` — service/reservation confirmation or reschedule. Follow `appointment-triage.md`.
    - `REFERENCE_LABEL`
    - `garbage` — move to TRASH/delete; recommend unsubscribe when available.

   Accepted calendar invitation notifications default to `garbage` unless they carry additional actionable context.

4. Execute the full-queue review using `## Bulk Review Pattern` below. Present GARBAGE FIRST, then actionables.

5. Apply confirmed labels at thread level in one batch operation.

6. Treat messages sent to the capture alias as pre-routed candidates for `IMPORT_LABEL` unless the content fits another policy outcome.

7. If the message is a self-sent capture to the `+gtd@gmail.com` alias, import it as a pure capture note by default: do not add `source:: gmail`, `gmail_thread_id`, `subject::`, or `web_link::` unless that email metadata is actually useful for later action.

8. Self-sent capture emails (`from:self`) already captured in the vault (in `Inbox.md`, a project/area file, or marked done) must be classified as `garbage` and trashed — never archived or kept in inbox.

### `#waiting` Tag Semantics

Use `#waiting` ONLY when the next step belongs to someone else (you delegated, you sent a request, you are blocked on an external party). Never use `#waiting` for tasks where you are the next actor. For the full tag taxonomy see `conventions.md § Tag Taxonomy`.

## Bulk Review Pattern

Use this pattern for every repetitive email-decision queue. GARBAGE-FIRST ordering reduces cognitive load before the actionable decisions.

1. Gather the whole candidate set in one call (`gws gmail users threads list --params '{"userId":"me","q":"<query>","maxResults":500}'`).
2. Classify the entire queue in one pass using Sonnet per `email-triage-policy.md § Classification Defaults`. Do NOT use Haiku for classification.
3. Group recommendations by outcome class.
4. Present the GARBAGE group first: one `AskUserQuestion` with per-category options (e.g. "Trash 12 shipping notices", "Trash 4 statements", "Override individually").
5. On confirm: execute one `messages.batchModify` with `addLabelIds:["TRASH"]` for the confirmed IDs.
6. THEN present the actionable/ambiguous group with sender, subject, preview. Collect decisions via `AskUserQuestion`.
7. Apply confirmed labels at thread level in one batch operation.

Garbage confirmation must complete BEFORE actionable items are presented. Do not mix them in one prompt.

## Backlog Drain

Use this procedure when the unlabeled inbox exceeds ~500 threads. Invoked via `/gtd-backlog-drain` (a ralph-loop wrapper). Single-phase: trash-only, iterated until the trash stream settles. Actionable review is deferred to the daily ceremony that follows.

Each loop iteration:

1. Consult `§ Backlog Drain Exit Conditions` below. If any condition is met, emit `<promise>TRASH_DRAINED</promise>` and write `{"kind":"loop-exit","command":"gtd-backlog-drain","reason":"<name>","ts":"<ISO>"}` to `System/.gtd-coach-state.jsonl`.
2. Otherwise, run one `/gtd-junk-sweep` pass. The sweep handles its own `AskUserQuestion` confirmation, its own batch-trash mutation, and its own `kind:"junk-sweep"` JSONL event append.
3. Ralph-loop re-enters and the cycle repeats.

The junk-sweep agent's narrow scope (see `agents/gtd-junk-sweep.md`) is unchanged. The backlog drain is a loop wrapper around repeated invocations, not a widening of sweep behavior.

After the loop exits, prompt the user to run `/gtd-daily` to review the deferred actionable mail. Do not auto-invoke.

### Backlog Drain Exit Conditions

Evaluate at the start of each loop iteration by reading the last 10 lines of `System/.gtd-coach-state.jsonl`. First match wins.

1. **Zero candidates.** Candidate query (`in:inbox -label:gtd/import -label:gtd/waiting -label:gtd/reference -label:gtd/imported`) with `maxResults:1` returns zero threads.
2. **Trash stream settled.** Last 2 `kind:"junk-sweep"` events both have `trashed:0` AND `deferred > 0`. No more junk to drain; remaining mail is actionable.
3. **User disengagement.** Last 3 `kind:"junk-sweep"` events all have `trashed:0` AND `deferred:0`. User has been skipping every batch.
4. **Sweep cap reached.** Sum of `trashed` across today's `kind:"junk-sweep"` events exceeds 800. Stop for review.
5. **Stale loop.** Last `kind:"junk-sweep"` event is older than 5 minutes of wall-clock (user walked away).

On exit, emit `<promise>TRASH_DRAINED</promise>` and the `loop-exit` event.

## Step 2 — Gmail Intake Gates

1. Pull import candidates from Gmail label gate:
   - Query: `label:<IMPORT_LABEL> -label:<IMPORTED_LABEL>`
2. Pull waiting candidates:
   - Query: `label:<WAITING_LABEL>`
3. Pull candidates through the Gmail commands in `gmail-commands.md`.

## Step 3 — Convert to GTD Tasks

1. For `IMPORT_LABEL`: create canonical tasks with `#inbox` capture state in `Inbox.md`. See `canonical-vault.md § Inbox Rules` for the full lifecycle.
2. For `WAITING_LABEL`: always create or update a `#waiting` task with reference metadata.
3. Dedupe by `gmail_thread_id` for normal email-driven imports. For self-sent capture-alias notes, prefer dedupe by task text/content and avoid forcing Gmail metadata onto the task line.
4. Ambiguous but potentially important mail becomes `IMPORT_LABEL` so it is clarified in `Inbox.md`, not deferred into a separate Gmail review queue.
5. Do not assign `🛫` or `📅` during raw import unless the source message contains an external commitment that the user confirms.
6. If created date is needed, use `➕ YYYY-MM-DD` on the same task line.
7. During clarify from `Inbox.md`, if an imported action takes <=5 minutes AND context+tools are available, execute it immediately.
8. Use the assistant to analyze message bodies and attachments during clarify so short review tasks can be completed immediately instead of deferred.

Task patterns:

`- [ ] #task <action> #email #inbox [#waiting] (source:: gmail) (gmail_thread_id:: <id>) (subject:: <subject>) (web_link:: <url>)`

Self-capture pattern:

`- [ ] #task <action> #inbox`

## Step 4 — Post-Import Hygiene

1. If import succeeded, move the Gmail thread from the import queue to `IMPORTED_LABEL` (`IMPORTED_LABEL` is required per Step 0).
2. For `garbage` decisions, move the thread to `TRASH` after user confirmation.
3. If `List-Unsubscribe` is present, recommend unsubscribe as a follow-up and confirm via `AskUserQuestion` before executing any unsubscribe action.

## Step 5 — Lifecycle Logging

1. Keep one canonical task line for lifecycle updates (`➕`, `🛫`, `✅`, `📅`). See `canonical-vault.md § Task Syntax`.
2. Do not duplicate completed tasks into Journal as additional `#task` entries.
3. If timeline context is useful, add narrative journal notes with backlinks, not duplicate tasks.
4. Follow `conventions.md § Journal Hygiene`: do not record trash counts, label moves, import counts, queue-cleanup stats, or similar ceremony output in the daily note.
5. Only journal mail-driven real-world outcomes — a reply sent, a dispute filed, a booking changed, a purchase completed.
6. Every journal entry created from intake work must link to the relevant `[[Projects/...]]`, `[[Areas/...]]`, `[[People/...]]`, or canonical task.
7. If a mail-driven task is completed and no immediate follow-up is expected, archive the Gmail thread by removing `INBOX`.
8. Keep completed threads in inbox only when an active near-term response loop still matters.

## Waiting Follow-Up Signals

- `#waiting` tasks stay on the waiting list by default.
- Only create a calendar follow-up signal when a waiting task has an explicit follow-up date.
- Use the calendar as a reminder layer for follow-up, not as a waiting inventory.
- For the full signal contract (which tasks produce signals and how), see `signal-sync.md § Signal Rules`.

## Auth and Scope Check

- If a Gmail call fails with auth/scope error, stop intake and report the exact blocker.

## Output

- Count of emails classified with user confirmation.
- Count of imported actionable emails.
- Count of mandatory waiting tasks created/updated.
- Any unresolved clarifications.
- Keep this output in the ceremony/session response only; do not copy it into the journal.
