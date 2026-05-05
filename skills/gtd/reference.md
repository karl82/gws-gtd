# GTD Reference

The complete operating model for running GTD inside an Obsidian vault, integrated with Gmail and Google Calendar via the `gws` CLI.

This is a single file by design. Search it with Cmd+F. Don't split it.

## Vault structure

The vault is the system of record. Everything else (Gmail, calendar) is a feeder or a signal.

### Folders

- `Inbox.md` — transient landing zone for raw Gmail imports and quick captures. Tasks leave on clarify.
- `Projects/` — finite outcomes with a defined end state. Folder layout: `Projects/<Domain>/<Project>.md`. Optional support folder: `Projects/<Domain>/<Project>/` for `notes.md`, `decisions.md`, `designs/`, `diagrams/`.
- `Areas/` — ongoing responsibilities. Default baseline: `Home.md`, `Finances.md`, `Relationships.md`, `Admin.md`. Add others when justified.
- `People/` — relationship notes and contact references.
- `Resources/` — reference material that isn't project-owned.
- `Archive/` — completed or inactive notes.
- `Journal/` — daily, weekly, monthly notes plus tasks born from real events.
- `System/` — Obsidian templates, Dataview queries, and runtime files (installed from this skill package).

### Task syntax

Globally tracked GTD actions: `- [ ] #task ...`

Plain `- [ ] ...` (no `#task`) stays local — for project-internal decomposition that doesn't need GTD tracking.

One canonical line per commitment. Update lifecycle on the same line:

- `➕ YYYY-MM-DD` — created date
- `🛫 YYYY-MM-DD` — start date
- `📅 YYYY-MM-DD` — due date
- `✅ YYYY-MM-DD` — completion date

Task dependency markers (optional, when one task can only start after another completes):

- `🆔 task-id` — assign an ID
- `⛔ blocker-id` — depends on this ID
- Or Dataview inline: `[id:: task-id]` and `[dependsOn:: blocker-id]`

### Linking

Use full vault-relative wikilinks for canonical entities:

- `[[Projects/Work/Billing Revamp]]` not `[[Billing Revamp]]`
- `[[Areas/Home]]` not `[[Home]]`
- `[[People/Jane Doe]]` not `[[Jane Doe]]`

Every active project task carries a `[[Projects/<Domain>/<Project>]]` link. Every active area task carries an `[[Areas/...]]` link. Design notes link back to their canonical project.

## Tag taxonomy

Tags serve two purposes only: GTD lifecycle state and execution context. Ownership is expressed by wikilink, never by tag.

### State tags

- `#task` — globally tracked GTD action
- `#inbox` — captured but not clarified
- `#next` — actionable now (sparse — only the small set you'll actually do)
- `#waiting` — delegated or blocked on someone else
- `#someday` — incubated, not currently actionable

### Context tags

- `#phone`, `#email`, `#errand`, `#internet`, `#deep`, `#buy`, `#idea`, `#payment`

A task without a context tag is fine. Don't invent domain tags (`#home`, `#work`) — use wikilinks.

### `#waiting` rule

Use `#waiting` only when someone else owes you the next move. Never use it for tasks where you are the next actor.

### `#inbox` clarify rule

To clarify an inbox task: remove `#inbox`, add a `[[Projects/...]]` or `[[Areas/...]]` wikilink, move it to its owning file (or leave it in the journal if it's tied to a real event). An `#inbox` task that's marked complete is a bug — clarify and move, or delete.

## Inbox.md vs Journal-born tasks

`Inbox.md` is for raw Gmail imports only. Tasks leave on clarify.

Tasks born from real events (meetings, calls, decisions you made) belong in the daily journal note for that day, with a wikilink to the relevant project or area. They don't go through `Inbox.md`.

## Stalled-project thresholds

- **14 days** without modification → flagged in warm-start as stalled
- **30 days** without modification → monthly review archive candidate

Both apply to top-level project notes (`Projects/<Domain>/*.md`).

## Project structure

Canonical project note: `Projects/<Domain>/<Project>.md` with a measurable outcome and at least one open `#task`. Plain checklist subtasks don't satisfy the open-task requirement.

Add the sibling folder `Projects/<Domain>/<Project>/` only when the project grows beyond one note (designs, decisions, notes, diagrams).

Project-owned design notes live under `Projects/<Domain>/<Project>/designs/`. Never use a separate top-level `Designs/` folder for active work — that's legacy structure.

Reusable, non-project-owned reference material goes in `Resources/`.

### Google Docs review metadata

Design notes intended for Google Docs review or export carry frontmatter:

- `project: "[[Projects/<Domain>/<Project>]]"`
- `gdoc_id`
- `gdoc_url`
- `gdoc_source_of_truth: markdown|google-docs`

Multi-tab bundles (multiple Markdown notes publishing into one Google Doc) add:

- `gdoc_role: main|tab`
- `gdoc_tab_title`

If a design note is an exported mirror from Google Docs, treat the Markdown as read-only and keep `gdoc_revision_id` and `gdoc_last_exported_at`.

## Taxes

Annual tax notes: `Projects/Taxes/YYYY.md`.

Required parent action groups: `US`, `CZ`, `Payments`. Use canonical `#task` syntax for parents; child checklist items stay non-`#task`.

Tag usage follows the standard taxonomy — no tax-specific tags.

Template: `System/Templates/Taxes Year.md`.

## Gmail integration

### Label model

- Root label: `gtd`
- `gtd/import` — explicit task-import gate
- `gtd/waiting` — explicit waiting gate
- `gtd/reference` — non-actionable but worth retaining
- `gtd/imported` — post-import dedupe marker (recommended; without it, dedup falls back to `gmail_thread_id` only)

### Capture alias

Set up the mobile capture path:

- Alias: `<your-address>+gtd@gmail.com`
- Gmail filter: `to:<your-address>+gtd@gmail.com` → apply `gtd/import`

Send yourself emails to that address (often from your phone) and they show up as imports the next time you process your inbox.

### Gmail intake procedure

Run as part of daily ceremony or on demand.

#### Step 0 — Label bootstrap

Verify `gtd`, `gtd/import`, `gtd/waiting`, `gtd/reference`, and `gtd/imported` exist. Create any missing labels under the `gtd` root before proceeding. Use `gws gmail users labels list` to check.

#### Step 1 — Classify

Pull unlabeled inbox candidates:

```
in:inbox -label:gtd/import -label:gtd/waiting -label:gtd/reference -label:gtd/imported
```

For efficient retrieval across all candidate threads in one call:

```bash
gws gmail +triage --query 'in:inbox -label:gtd/import -label:gtd/waiting -label:gtd/reference -label:gtd/imported' --max 100 --format json \
  | jq '[.messages[] | {id, from, subject, date}]'
```

This returns structured `id` + `from` + `subject` + `date` for all threads. Pipe through `jq` for filtering and classification. Don't call `messages.list` (IDs only) or `messages.get` per-message (expensive). Reach for `+read` only when subject+sender isn't enough to decide.

To get message IDs for `messages.batchModify` after classifying thread IDs:

```bash
gws gmail users threads get --params '{"userId":"me","id":"<thread_id>","format":"minimal"}' \
  | jq '[.messages[].id]'
```

For each candidate, show sender + subject + snippet preview. Classify into one of:

- `gtd/import` — task in `Inbox.md` for clarify
- `gtd/waiting` — waiting task with reference metadata
- `appointment` — service/reservation confirmation; see Calendar integration § Appointment triage
- `gtd/reference` — keep, archive
- `garbage` — trash, recommend unsubscribe if `List-Unsubscribe` header present

Use `triage-policy.md` for classification defaults and heuristics.

**Garbage first.** Within a batch, present the obvious-trash group first for one bulk confirmation. Apply trash. Then present actionable / ambiguous items for individual review. This keeps the actionable set small and reduces decision fatigue.

#### Step 2 — Apply labels

Apply confirmed labels at thread level via `messages.batchModify` or `threads.modify`. See `commands.md` for API gotchas.

For confirmed garbage, prefer one `messages.batchModify` with `addLabelIds:["TRASH"]` over many single trash calls.

#### Step 3 — Convert to vault tasks

For each `gtd/import` thread, create or update a task in `Inbox.md`:

```
- [ ] #task <action> #email #inbox (source:: gmail) (gmail_thread_id:: <id>) (subject:: <subject>) (web_link:: <url>)
```

For self-sent capture-alias messages (from yourself, to `+gtd`), import as a plain capture without forced Gmail metadata:

```
- [ ] #task <action> #inbox
```

Don't add `source:: gmail` / `gmail_thread_id` / `subject::` / `web_link::` to self-capture notes — they're capture notes, not email threads.

For each `gtd/waiting` thread, create or update a `#waiting` task with reference metadata. Dedupe by `gmail_thread_id`.

#### Step 4 — Dedupe and post-import hygiene

Dedupe by `gmail_thread_id` for normal email-driven imports. For self-capture notes, dedupe by task text/content.

If `gtd/imported` exists, move the thread there after successful import. Otherwise rely on thread-id dedupe.

For confirmed reference items, archive (remove `INBOX` label) — the `gtd/reference` label is enough; no need to keep in inbox.

#### Self-capture trash rule

Self-sent capture emails (from:self) that are already captured in the vault — meaning the equivalent task is already in `Inbox.md`, a project/area file, or marked done — must be classified as `garbage` and trashed. Don't archive, don't keep in inbox, don't import a duplicate.

#### TripIt forwarding rule

Booking confirmations (flight, hotel, Airbnb, car rental, campsite/park reservations) are forwarded to `plans@tripit.com` and then archived. TripIt parses them automatically and builds the itinerary. Never create a vault task for a TripIt-managed booking. Execute silently — don't ask the user.

The follow-up "check out your itinerary" notification from TripIt is trashed immediately.

#### Card / account security heuristic

Card-not-present alerts, unusual merchant flags, fraud alerts → `gtd/import`. Task: `Review [issuer] card alert — [merchant] $[amount] and confirm or dispute`. The 5-min rule applies: if the merchant is recognizable and the amount is expected, mark done immediately; else dispute.

Account security notifications (password change, 2FA modified, new device login) → `gtd/import`. Task: `Confirm [issuer] account security change was intentional`. Resolve in 5 min if you recognize it; else investigate.

General settings-change or preference-update notifications (mailing prefs, notification settings, non-security account changes) → trash.

#### LinkedIn InMail detection

Recruiter emails arriving as LinkedIn InMail bounces cannot be replied to via `gws gmail +reply` — replies must go through LinkedIn messaging.

Identify InMail by checking thread headers (`gws gmail users threads get`):

- `Delivered-To` ends in `+linkedin@gmail.com`, OR
- `Return-Path` contains `@bounce.linkedin.com`

Subject patterns are a weaker signal but often correlate: `Message replied: ...` prefix, or heavy emoji subjects like `💬 ... 💬`.

Reply channel via Claude in Chrome (when available):

1. Navigate to `https://www.linkedin.com/messaging/`.
2. Search for the contact by name in the messages search box (press Enter).
3. Click their thread — the URL becomes the canonical `sent_reply::` link.
4. Inject message text via `javascript_tool` into `.msg-form__contenteditable` using `document.execCommand('insertText', false, text)`.
5. Click Send.

Log the LinkedIn thread URL as `(sent_reply:: https://www.linkedin.com/messaging/thread/...)` in the vault, same as Gmail sent links.

#### Datová schránka rule

Czech government data-mailbox notifications (Datová schránka) are delivery pings only — the actual document lives in the Datová schránka portal, not in Gmail.

- Archive the Gmail notification immediately (`gtd/reference`, then archive).
- Open the Datová schránka portal to read the document.
- Create a vault task only if the document requires a response — use `#next` with a `📅` deadline based on the response window.
- Never create a vault task from the notification email alone.

## Calendar integration

### Calendar model

The vault is the task system of record. Calendar is for events and signals only — not for capturing tasks.

- Personal calendars hold real events.
- A separate calendar named `GTD Signals` is output-only — used to mirror dated `#next` and dated `#waiting` follow-ups so they show up alongside real events. See § Signal sync below.

### Calendar intake (ask queue)

Run as part of daily ceremony.

1. Pull upcoming events with attendees:
   ```
   gws calendar +agenda --today --format json
   gws calendar +agenda --tomorrow --format json
   ```
2. Filter to events with attendees.
3. For each event, show summary + when + preview from description / notes / location.
4. For each event, decide:
   - `task` — explicit follow-up needed (e.g. send a doc, schedule next sync). Create `#task` in the daily journal note with project link.
   - `journal` — context worth keeping (decisions made, themes). Add narrative entry to journal note with project link.
   - `project-note` — project-related context that should live in the project note rather than journal. Add to project file.
   - `skip` — no GTD value.

Default to batch review when 5+ events: present them all together with recommendation + rationale, collect compact decisions, then apply event-note / task actions in one go.

### Appointment triage

For service/reservation/appointment confirmation or reschedule emails (classified `appointment` in Step 1):

1. Search Google Calendar for an existing event matching the appointment (by venue name, service type, or date range).
2. If an existing event matches:
   - If the email's date/time matches the calendar event: archive the email, no task needed.
   - If they differ (reschedule): patch the calendar event (`gws calendar +patch`) with the new date/time, then archive the email.
3. If no existing event is found:
   - Create a calendar event with `gws calendar +insert` using the date/time, summary, and location from the email.
   - Archive the email after creation.

Never create a vault `#task` for an appointment that is already (or can be) reflected on the calendar.

## Signal sync

The `GTD Signals` Google Calendar mirrors dated tasks so they appear alongside real events.

### What gets mirrored

- Dated `#next` tasks (have a `📅 YYYY-MM-DD`)
- Dated `#waiting` tasks (the date is the follow-up reminder)

`#someday` items are never mirrored. Undated tasks are never mirrored.

### Event shape

- Calendar: `GTD Signals`
- Title: the task text without the date marker
- Date: from `📅 YYYY-MM-DD`, all-day event
- `extendedProperties.private.gtd_task_id` = stable hash of `(file path, task text)` so the script can match vault → calendar without ambiguity
- `extendedProperties.private.gtd_source_file` = vault-relative path

### Sync algorithm

Run via `scripts/sync_signals.py`:

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/sync_signals.py"          # dry-run, default
python3 "${CLAUDE_SKILL_DIR}/scripts/sync_signals.py" --apply  # create/update/delete
```

The script:

1. Scans the vault for dated `#next` and dated `#waiting` tasks.
2. Lists `GTD Signals` events with `gtd_task_id` set.
3. Diffs: creates events for new tasks, updates events whose date changed, deletes events whose tasks are completed or removed.
4. Dry-run prints the diff. `--apply` mutates the calendar.

### Pre-check during daily

At the start of each daily ceremony, after loading the calendar agenda, check for stale `GTD Signals` events whose corresponding vault tasks are already complete or removed. Offer to delete them via `AskUserQuestion`.

## Event capture

For ad-hoc calendar events you want to record beyond the calendar itself (decisions, action items from a meeting):

- If the event spawned tasks, write them as `#task #inbox` in the daily journal note with `[[Projects/...]]` or `[[Areas/...]]` wikilinks. Don't create a separate event note.
- If the event is project-significant (a decision, a milestone, a stakeholder commitment), append a narrative entry to the project note with the date and a brief description.
- If the event is just context (a meeting happened, here's what was discussed), keep a brief journal entry. Don't pad it.
- One-off events that aren't tied to a project go in `Resources/` only if they have lasting reference value. Otherwise: journal.

## People linking

Link Google Contacts and meeting/email participants to `People/` notes when the relationship is worth tracking.

### Match strategy

1. Primary key: exact email match.
2. Secondary key: normalized full name (lowercase, trimmed).
3. Ambiguous matches → don't auto-link; ask the user via `AskUserQuestion`.

### People note structure

`People/<Name>.md` with frontmatter:

- `google_contact_id` — stable Google reference (the only contact data stored in the vault)
- `last_contact_sync`

Body section:

- `Contact: [Google Contact](<contact_url>)` — clickable link

Don't copy email addresses, phone numbers, or other contact details from Google Contacts. Treat Google Contacts as the source of truth and store only the reference. The clickable link gets you to the live contact data.

### Link injection

When importing Gmail or calendar items, append `[[People/<Name>]]` only when the match is high-confidence (exact email or name match). Keep the wikilink in the task or journal text — not hidden-only metadata.

Never create a vault task from contact data alone. Never mutate unrelated People notes.

## Ceremonies

### Daily

Quick. Drives execution from trusted lists. Inbox zero is NOT a daily gate.

#### Steps

1. **Calendar agenda check.** Pull today and tomorrow. Note timing of events with attendees.
2. **GTD Signals pre-check.** Look for stale signals (events for completed vault tasks). Offer to delete via `AskUserQuestion`.
3. **Gmail intake.** Run the Gmail intake procedure above. Garbage-first. Stop when the unlabeled inbox is empty OR when the user says enough.
4. **Calendar intake.** Run the calendar ask-queue for events with attendees.
5. **Due / next / waiting review.** Read tasks across `Areas/` and `Projects/`. Surface:
   - Tasks with `📅` due today or earlier
   - `#next` queue
   - `#waiting` items (just review; full reconcile is weekly)
6. **Optional context batching.** If `#next` has 3+ tasks in a single context (e.g. all `#phone`), batch them.
7. **End.** Ask the user if anything else is needed; otherwise summarize and stop.

#### Decision flow for any captured item

1. What is it?
2. Is it actionable?
   - No → trash, reference (archive), or `#someday`.
   - Yes → define the next physical action.
3. If multi-step, create or update a project with a measurable outcome and at least one open `#task`.
4. For the next action:
   - Do immediately if it takes 5 min and the context+tools are available.
   - Delegate and mark `#waiting`.
   - Defer into the correct project, area, or daily journal with a wikilink.

#### Daily output

- Counts by destination (trashed, imported, waiting created, calendar decisions)
- Items requiring user decision
- Risks or blockers (`#waiting`, `#blocked`)

Don't journal these counts. Output goes in the session response only.

### Weekly

Strict. Mind sweep, full review, top-3 commitments. Inbox zero IS a weekly gate.

#### Steps

1. **Get Clear** (strict gate)
   - Mind sweep: capture anything untracked as `#task #inbox` before processing — open browser tabs, recent meeting notes, physical inboxes, open commitments to others, upcoming events, people to follow up with, ideas.
   - Run inbox zero across the vault: clarify every `#inbox` task. Stop and report `Get Clear incomplete` if the queue isn't zero.
2. **Get Current**
   - Review overdue and next-7-day due tasks.
   - Review `#waiting` items in detail (longer than the daily glance).
   - Review next-step candidates and promote a small set to `#next`.
   - Surface stalled projects (>14 days unmodified or no open linked task).
   - Surface orphan tasks: open `#task` with no `[[Projects/...]]` or `[[Areas/...]]` wikilink AND not inside a `Projects/` or `Areas/` file. Tasks in `Journal/` with a valid wikilink are NOT orphans.
3. **Get Creative**
   - Review journal patterns from the week.
   - Scan `#someday` items for ones to promote or delete.
   - Recommend top 3 outcomes for next week.
4. **Gmail safety net**
   - Sweep `gtd/import` items that haven't been clarified.
   - Sweep `in:inbox older_than:7d` minus GTD labels — old unprocessed mail.
   - Reconcile `#waiting + source:: gmail` tasks: any with no progress signal and no due date?
5. **Calendar pressure**
   - Pull `gws calendar +agenda --week`.
   - Compare meeting load with due-date clusters in the vault. Flag overloaded days.

Use `System/Templates/Weekly Review.md` for the note format. Path: `Journal/YYYY-WNN.md` (e.g. `Journal/2026-W18.md`).

#### Weekly output

- Weekly health snapshot
- Stalled / stale exceptions
- Orphan task list
- Proposed top 3 outcomes

### Monthly

Reflective. Portfolio audit, capacity, commitments.

#### Steps

1. **Portfolio audit.** Confirm each active project has a measurable outcome and at least one open `#task`.
2. **Area balance.** Surface neglected or overloaded areas.
3. **Stalled / stale detection.**
   - Projects inactive >30 days (archive candidates).
   - Open tasks stale >30 days without due dates.
4. **Pattern and capacity analysis.** Review journal signals, recurring blockers, due-date clustering.
5. **Someday review.** Review all `#someday` items: promote, delete, or leave incubated. Deeper than the weekly quick scan.
6. **Next-month commitments.** Recommend top commitments and elimination candidates.

Use `System/Templates/Monthly Review.md`. Path: `Journal/YYYY-MM.md`.

#### Monthly output

- Portfolio exceptions
- Capacity and risk summary
- Proposed commitments for next month

#### Monthly anti-rules

- Don't auto-archive.
- Don't assume calendar availability.

### Organizing

Ad-hoc cleanup ceremony. Run when the vault feels cluttered.

#### Steps

1. **Folder check.** Confirm the canonical folders exist: `Projects/`, `Areas/`, `People/`, `Resources/`, `Archive/`, `Journal/`, `System/`.
2. **Project structure check.** Confirm projects live at `Projects/<Domain>/<Project>.md`. Move any deeper artifacts into the project's sibling folder. Move project-owned designs into `Projects/<Domain>/<Project>/designs/`.
3. **Link normalization.** Find short links to canonical entities (`[[Billing]]` instead of `[[Projects/Work/Billing]]`) and propose normalizations via `AskUserQuestion`. One per file, with confirmation.
4. **Archive sweep.** Move project notes that have no open `#task` AND mtime older than 30 days into `Archive/`.
5. **Legacy reconciliation.** Notes in a top-level `Designs/` folder are legacy — reconcile them into project-owned `designs/` folders or `Resources/` per ambiguity. If ownership is unclear, mark `needs-decision` and ask.

Per-move confirmation. Never batch moves without asking.

#### Organizing output

- Moves and renames performed
- Link normalizations applied
- `needs-decision` items left for the user
- Anything unresolved

## Junk sweep

A narrow, repeated lightweight version of Gmail intake Step 1 — garbage-only. Used for ongoing maintenance between daily ceremonies.

### Procedure

1. Pull the unlabeled inbox candidate set via `gws gmail +triage --query '...' --format json | jq '[.messages[] | {id, from, subject}]'`.
2. Classify only into `garbage` or `defer`. Don't make import / waiting / reference decisions — those go to daily.
3. Present the trash batch via one `AskUserQuestion` with per-category options (`Trash 12 shipping`, `Trash 4 statements`, `Skip`, `Override individually`).
4. On confirm, collect message IDs via `threads get --format minimal`, then execute one `messages.batchModify` with `addLabelIds:["TRASH"]`.
5. Output: `{trashed: N, deferred_for_daily: N}`.

### Invariants

- Garbage-only. Never apply `gtd/*` labels, never create vault tasks, never forward, never unsubscribe.
- Empty candidate set → silent return.
- Auth/scope error → report blocker, stop.

### Recurring invocation

For ongoing maintenance, run on a 2h interval while the assistant session is alive:

```
/loop 2h /gtd-sweep
```

The loop runs only while a Claude session is open. It's not a system-level cron.

## Backlog drain

A one-shot bulk cleanup for backlogged inboxes (>500 unlabeled threads). Iterates the junk sweep until trash settles. NOT for ongoing maintenance.

### Procedure

Wraps `/gtd-sweep` in a ralph-loop. Each iteration runs one sweep, then re-evaluates exit conditions.

```
/ralph-loop "Read last 10 lines of System/.gtd-state.jsonl. If any backlog drain exit condition is met, emit <promise>TRASH_DRAINED</promise>. Otherwise run one /gtd-sweep pass." --completion-promise TRASH_DRAINED --max-iterations 50
```

After exit, prompt the user to run a daily ceremony to review the deferred actionable mail.

### Exit conditions

Evaluate at the start of each iteration. First match wins.

1. **Zero candidates.** Unlabeled-inbox query returns zero threads.
2. **Trash stream settled.** Last 2 sweep events both have `trashed:0` AND `deferred > 0`. No more junk; remaining mail is actionable.
3. **User disengagement.** Last 3 sweeps all have `trashed:0` AND `deferred:0`. User has been skipping every batch.
4. **Sweep cap reached.** Sum of `trashed` across today's sweeps exceeds 800.
5. **Stale loop.** Last sweep event older than 5 minutes wall-clock.

### State file

Optional: `System/.gtd-state.jsonl` (append-only JSONL). Each sweep writes one line:

```jsonl
{"kind":"sweep","ts":"<ISO>","trashed":N,"deferred":N,"categories":{...}}
```

The backlog drain reads recent lines to evaluate exit conditions. Unused otherwise.

## Assistant mode

The default behavior when invoked without a specific ceremony — for example via `/gtd` with no argument, or when the assistant is running between ceremonies.

### Warm-start

On the first user message of a session, before responding:

1. Count `#inbox` items in `Inbox.md` that lack `✅`.
2. Read today's `Journal/YYYY-MM-DD.md` — note what's already logged.
3. Scan `Areas/` and top-level `Projects/` for `#task` due today or earlier.
4. Scan top-level `Projects/` mtimes — flag any not modified in 14+ days as stalled.

Output:

```
Inbox: N items
Due today: N tasks  (or "none")
Stalled: ProjectName, ProjectName  (or "none")

What would you like to do?
  [daily]  [weekly]  [monthly]  [organize]
  [capture]  [next actions]  [ask anything]
```

Don't repeat the warm-start on subsequent messages in the same session.

### Inline quick tasks

Handle these inline — don't dispatch a sub-agent:

- **Capture / journal entry** — append to today's journal note. For task captures, route to `Inbox.md` for clarify. Don't invent deadlines.
- **Next actions** — read `#task` lines from `Areas/` and `Projects/`, exclude `#waiting` and completed. Rank by (a) due today or earlier, (b) `#next`, (c) project most-recently-modified. Return top 3 with the owning note path and one-line context.
- **Project status** — read the project note. Summarize open `#task` lines, last journal link, current stalled state. 2–4 sentences. Don't rewrite the note.
- **Inbox triage** — walk `Inbox.md` items one at a time via `AskUserQuestion` (next action / project / waiting / someday / trash). Stop when the user says stop or `#inbox` is zero.
- **General GTD question** — answer using this reference. Cite section names; don't restate the rule in full.

### Ceremony dispatch

When the user asks for a ceremony, run the corresponding section above.

## Anti-rules

These apply to every ceremony, every command, every interaction.

- Don't invent deadlines. If the user hasn't given you a date, the task has no `📅`.
- Don't auto-complete tasks. The user marks `✅`.
- Don't auto-archive. The user moves things to `Archive/` (organizing ceremony surfaces candidates).
- Don't create hidden states outside the canonical model.
- Don't convert reference notes into GTD tasks without `#task`.
- Don't rely on ambiguous short wikilinks for canonical entities.
- Don't duplicate completed tasks into the journal as additional `#task` entries.

## Journal hygiene

The daily journal is for real-world timeline events and outcomes — not ceremony mechanics.

- `#task #inbox` lines born from real events go in the daily journal alongside narrative context.
- Don't write ceremony mechanics into the journal: no inbox counts, no classification summaries, no label routing tallies, no task-list snapshots, no completion banners.
- Every journal entry and journal-born task links to a `[[Projects/...]]`, `[[Areas/...]]`, `[[People/...]]`, or canonical task.
- If nothing real happened beyond review/maintenance, leave the journal alone.

Daily note path: `Journal/YYYY-MM-DD.md`.
Weekly review note path: `Journal/YYYY-WNN.md`.
Monthly review note path: `Journal/YYYY-MM.md`.

## Interaction rules

- Every user decision goes through `AskUserQuestion`. Don't ask in plain text.
- Include clickable URLs in option descriptions when available — Gmail thread URL, calendar event URL, vault note path.
- Identify tasks and notes by recognizable context — task text, sender + subject, person, linked project. Don't refer to `Inbox.md:10` without context.
- Pass `--format json` to every `gws` command. Use `jq` to extract fields. Don't shell out to `python3 -c` for JSON parsing.
- Prefer minimal, reversible vault edits. When in doubt, ask.

For Gmail, Calendar, and People `gws` API gotchas, see `commands.md`.
For email classification table and heuristics, see `triage-policy.md`.
