# gws-gtd Overhaul — Consolidated Design

**Status:** Draft, pending user approval
**Branch:** `refactor/gws-gtd-overhaul`
**Date:** 2026-05-03
**Scope:** Foundation cleanup + 5 user-reported issues, as one coordinated change.

## Why this document exists

Five user-reported issues triggered a brainstorm; during exploration, audits surfaced ~180 latent problems in the existing skill surface (contradictions, duplication, vague phrasing, stale paths, misrouted commands). Fixing the 5 issues on top of the existing mess would compound drift. This spec integrates both: first clean the foundation, then ship the 5 features.

## Outcomes

1. **One-job-per-file layout.** Every reference file has one clear purpose. Every agent has a reference counterpart. Every command has an agent binding.
2. **Single source of truth for every rule.** Gmail label model, tag taxonomy, anti-rules, journal hygiene, inbox lifecycle, orphan-task definition, `#waiting` semantics — each defined once, referenced elsewhere.
3. **Zero hedge words.** No "truly," "meaningful," "when appropriate," "as needed," "clearly." Every rule specifies the deterministic criterion.
4. **Ceremonies terminate explicitly.** Four-gate exit for daily. Residual state handed off via JSONL.
5. **Junk presented first.** Garbage-batch-then-actionables in all bulk-review flows.
6. **Cost-aware model routing.** Mechanical gws/vault ops delegated to Haiku subagents; judgment stays on Sonnet/Opus. Skill-scoped override of the global Haiku ban, narrowly documented.
7. **Two-hour junk sweep** via `/loop 2h /gtd-junk-sweep` as an in-session automation.
8. **Proactive coach persona** — ambient nudges with bounded vocabulary and daily rhythm.

## Non-goals

- No changes to `gws-doc-review-sync/`, `transcrypt-git-repo/`, `journaling/` skills.
- No vault-content migration (only skill-package changes).
- No changes to Obsidian templates, Dataview queries, or vault runtime assets beyond the new `.gtd-coach-state.jsonl` file.
- No weakening of the global CLAUDE.md Haiku ban — only a narrow skill-scoped exception.

---

## Part I — Target file layout

### Reference files (after changes)

```
skills/gws-gtd/
├── SKILL.md                             # router + guardrails + always-applied list
├── README.md                            # install/permissions; links to SKILL.md
├── references/
│   ├── conventions.md                   # behavioral doctrine (sole owner)
│   ├── canonical-vault.md               # structural model only
│   ├── email-triage-policy.md           # Gmail label contract + classification
│   ├── gmail-commands.md                # Gmail gws API mechanics (renamed)
│   ├── calendar-commands.md             # NEW — Calendar gws mechanics
│   ├── people-commands.md               # NEW — People gws mechanics
│   ├── daily.md                         # daily ceremony (thin orchestrator)
│   ├── weekly.md                        # weekly (absorbs reconcile)
│   ├── monthly.md                       # monthly
│   ├── organizing.md                    # organizing procedure only
│   ├── gmail-intake.md                  # NEW — split from daily-intake
│   ├── calendar-intake.md               # NEW — split from daily-intake
│   ├── appointment-triage.md            # NEW — split from daily-intake
│   ├── event-capture.md                 # per-event capture decision
│   ├── people-linking.md                # contact → People/ note linking
│   ├── signal-sync.md                   # sole owner of GTD Signals rules
│   ├── project-retrofit.md              # renamed from project-structure.md
│   ├── vault-audit.md                   # NEW — merged from analyze + verify
│   ├── assistant.md                     # persona + warm-start + menu only
│   ├── quick-tasks.md                   # NEW — split from assistant.md
│   ├── coach.md                         # NEW — proactive coach rhythm & nudges
│   └── opkg.md                          # package lifecycle, linked from README
agents/
├── gtd-daily.md                         # edit: termination gates + delegation
├── gtd-weekly.md                        # edit: drop weekly-reconcile mode
├── gtd-monthly.md                       # edit: minor alignment
├── gtd-organizing.md                    # edit: minor termination gate
├── gtd-assistant.md                     # NEW — top-level persona
├── gtd-signals.md                       # NEW — signal-sync persona
├── gtd-retrofit.md                      # NEW — audit + retrofit persona
├── gtd-junk-sweep.md                    # NEW — 2h sweep agent (Sonnet)
├── gtd-gws-fetch.md                     # NEW — Haiku mechanical gws
├── gtd-vault-scan.md                    # NEW — Haiku mechanical vault ops
└── gtd-signal-diff.md                   # NEW — Haiku signal-sync dry-run
commands/
├── gtd-daily.md
├── gtd-weekly.md
├── gtd-monthly.md
├── gtd-organize.md                      # renamed from gtd-cleanup.md
├── gtd-signals-sync.md                  # rewired to gtd-signals agent
├── gtd-analyze.md                       # renamed from analyze-vault.md
├── gtd-retrofit.md                      # renamed from retrofit-vault.md
├── gtd-verify-projects.md               # renamed from verify-project-structure.md
├── gtd-junk-sweep.md                    # NEW — 2h sweep wrapper
└── gtd-assistant.md                     # NEW (optional)
root/
├── AGENTS.md                            # one-line edit: mention coach state file
└── System/
    └── .gtd-coach-state.jsonl           # runtime artifact, created on first write
```

### Files removed (by rename or merge)

- `skills/gws-gtd/references/daily-intake.md` → split into `gmail-intake.md`, `calendar-intake.md`, `appointment-triage.md`
- `skills/gws-gtd/references/weekly-reconcile.md` → absorbed into `weekly.md`
- `skills/gws-gtd/references/project-structure.md` → renamed to `project-retrofit.md`, 3 sections moved to `canonical-vault.md`
- `skills/gws-gtd/references/command-reference.md` → renamed to `gmail-commands.md`
- `commands/gtd-cleanup.md` → renamed to `gtd-organize.md`
- `commands/analyze-vault.md` → renamed to `gtd-analyze.md`
- `commands/retrofit-vault.md` → renamed to `gtd-retrofit.md`
- `commands/verify-project-structure.md` → renamed to `gtd-verify-projects.md`

### File-ownership matrix (single source of truth per rule)

| Rule / concept                      | Canonical location                               | Referenced from (no re-definition)                               |
| ----------------------------------- | ------------------------------------------------ | ----------------------------------------------------------------- |
| Tag taxonomy (#task, #inbox, …)     | `conventions.md § Tag Taxonomy`                  | `canonical-vault.md`, `daily.md`, `weekly.md`                     |
| Gmail label model                   | `email-triage-policy.md § Label Contract`        | `conventions.md`, `gmail-intake.md`, `weekly.md`                  |
| Journal hygiene                     | `conventions.md § Journal Hygiene`               | `daily.md`, `weekly.md`, `monthly.md`, `gmail-intake.md`          |
| Inbox.md lifecycle                  | `canonical-vault.md § Inbox Rules`               | `daily.md`, `gmail-intake.md`                                     |
| Orphan-task definition              | `canonical-vault.md § Orphan Tasks`              | `weekly.md`, `organizing.md`                                      |
| `#waiting` semantics                | `conventions.md § Tag Taxonomy`                  | `daily.md`, `gmail-intake.md`, `email-triage-policy.md`           |
| Anti-rules (no auto-complete, …)    | `conventions.md § Anti-Rules`                    | All 7 agents; `assistant.md`                                      |
| One-canonical-task-line rule        | `canonical-vault.md § Task Syntax`               | `daily.md`, `gmail-intake.md`                                     |
| Bulk review pattern (junk-first)    | `gmail-intake.md § Bulk Review Pattern`          | `daily.md`, `calendar-intake.md`, `weekly.md`                     |
| Dedupe rules                        | `gmail-intake.md § Dedupe`                       | `weekly.md`                                                       |
| Canonical project path              | `canonical-vault.md § Project Rules`             | `organizing.md`, `project-retrofit.md`                            |
| Taxes convention                    | `canonical-vault.md § Taxes`                     | `organizing.md`                                                   |
| Daily note path                     | `canonical-vault.md § Journal Paths`             | `assistant.md`, `daily.md`                                        |
| Weekly/monthly note paths           | `canonical-vault.md § Journal Paths`             | `weekly.md`, `monthly.md`                                         |
| Stalled threshold                   | `conventions.md § Stalled Thresholds`            | `assistant.md`, `weekly.md`, `monthly.md`                         |
| Vault status snapshot spec          | `assistant.md § Warm-Start`                      | `coach.md`                                                        |
| Signal rules (when a signal exists) | `signal-sync.md § Signal Rules`                  | `daily.md`, `gmail-intake.md`, `weekly.md`                        |
| Capture alias setup                 | `email-triage-policy.md § Capture Setup`         | `gmail-intake.md`                                                 |
| Model routing override              | `SKILL.md § Model Routing`                       | `gtd-gws-fetch`, `gtd-vault-scan`, `gtd-signal-diff` agents       |
| Coach state file                    | `coach.md § State File`                          | `gtd-junk-sweep`, `assistant.md`, `root/AGENTS.md`                |

---

## Part II — Router

New `SKILL.md` router replaces the current 13 intents:

```
daily              -> references/daily.md
weekly             -> references/weekly.md
monthly            -> references/monthly.md
organizing         -> references/organizing.md
gmail-intake       -> references/gmail-intake.md
calendar-intake    -> references/calendar-intake.md
appointment-triage -> references/appointment-triage.md
event-capture      -> references/event-capture.md
people-linking     -> references/people-linking.md
signal-sync        -> references/signal-sync.md
project-retrofit   -> references/project-retrofit.md
vault-audit        -> references/vault-audit.md
assistant          -> references/assistant.md
quick-tasks        -> references/quick-tasks.md
coach              -> references/coach.md
junk-sweep         -> references/gmail-intake.md § Garbage-Only Sweep (new subsection)
```

Always-applied references (load unconditionally at ceremony start):

```
- conventions.md
- canonical-vault.md
- email-triage-policy.md
- gmail-commands.md, calendar-commands.md, people-commands.md (as needed)
```

---

## Part III — Foundational cleanup (Lens A + B + D-P0)

### Contradictions resolved

| # | Contradiction                                       | Resolution                                                                                      |
| - | --------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| 1 | Actionable-first vs junk-first ordering             | Junk-first wins. Update `daily.md:7`, `daily-intake.md:70`, `agents/gtd-daily.md:20`            |
| 2 | Daily note path: `Journal/YYYY-MM-DD.md` vs nested  | Canonical: `Journal/YYYY-MM-DD.md` (flat). Defined in `canonical-vault.md § Journal Paths`      |
| 3 | Weekly/monthly path: flat vs regex                  | Canonical: regex form (`^Journal(?:/.+)?/\d{4}-W\d{2}\.md$` and `\d{4}-\d{2}`)                  |
| 4 | Stalled threshold 14 vs 30 days                     | 14 days = warm-start flag; 30 days = monthly archive candidate. Both, named separately          |
| 5 | Top-level `Designs/` end state                      | `Designs/` is adaptable — agents should reconcile to owning project. `project-retrofit.md` owns |
| 6 | Signal mirroring scope (dated `#next` only)         | Canonical: dated `#next` + dated `#waiting`. `signal-sync.md` is sole owner                     |
| 7 | `skills/` vs `.opencode/skills/` paths              | `skills/` wins. Fix `opkg.md`, `commands/analyze-vault.md` path references                      |
| 8 | Taxes tags vs tag taxonomy                          | Taxes uses the standard taxonomy; no special tags. Remove divergent Taxes tag list              |
| 9 | Inbox.md "optional" vs "Gmail-only"                 | `Inbox.md` is the **required** transient landing zone for all Gmail imports                     |
| 10| Self-alias: Inbox.md vs journal                     | Self-alias always goes to `Inbox.md` for clarify; journal only after clarify                    |
| 11| Monthly agent mode list                             | Add `signal-sync` to monthly if wanted; otherwise leave narrow. Defer                           |
| 12| "uses template" vs "templater instantiates"         | Standardize on "Templater applies `<template>`"                                                 |
| 13| Assistant dispatch-only vs inline triage            | Assistant dispatches ceremonies; `quick-tasks.md` owns inline handling                          |

### Redundancies collapsed (Lens D P0 + P1)

- **Gmail label model** — one table in `email-triage-policy.md`. `conventions.md` and `gmail-intake.md` cross-reference.
- **Anti-rules** (don't invent deadlines, don't auto-complete) — one block in `conventions.md § Anti-Rules`. 7 agent files each cite it; duplicate bullets removed.
- **One canonical task line** rule — named rule in `canonical-vault.md § Task Syntax`. Other files reference by name.
- **Bulk review pattern** — one named sub-procedure in `gmail-intake.md`. Callers reference it.
- **Orphan-task definition** — one rule in `canonical-vault.md`. `weekly.md` and `organizing.md` cite by name.
- **`Inbox.md` lifecycle** — one canonical block in `canonical-vault.md § Inbox Rules`.
- **Journal hygiene** — one block in `conventions.md § Journal Hygiene`.
- **Taxes convention** — one block in `canonical-vault.md § Taxes`.

### Stale / broken references fixed

- `opkg.md` — rewrite to reference `skills/gws-gtd/` (not `.opencode/skills/`). Add pointer from `README.md`.
- `commands/analyze-vault.md` (now `gtd-analyze.md`) — fix `.opencode/...` paths to `skills/gws-gtd/...`.
- `Taxes Year.md` template missing — remove references to it, or create the template. Defer to follow-up (not blocking this spec).
- `journaling` skill cross-reference — declare in `SKILL.md § References` as an external dependency.
- `assistant` mode now has an agent (`gtd-assistant.md`) — mismatch resolved.
- `signal-sync` mode now has an agent (`gtd-signals.md`) — mismatch resolved.
- `ad-hoc-maintenance` intent dissolved — absorbed by `gmail-intake` / `calendar-intake` / `appointment-triage`.

### Scope splits

1. **`daily-intake.md` → 3 files.**
   - `gmail-intake.md`: Steps 0/1/2/3/5/6, waiting-follow-up signals, Gmail auth. Invoked by daily AND weekly.
   - `calendar-intake.md`: Step 4 ask queue; delegates per-event to `event-capture.md`.
   - `appointment-triage.md`: Appointment sub-procedure (service/reservation confirmations).

2. **`assistant.md` → 2 files.**
   - `assistant.md`: persona + warm-start + menu + dispatch table.
   - `quick-tasks.md`: inline quick-task handlers (capture, next-actions, project status, inbox triage).

3. **`command-reference.md` → 3 files.**
   - `gmail-commands.md` (rename current, keep Gmail content).
   - `calendar-commands.md` (new stub, fill as calendar mechanics land).
   - `people-commands.md` (new stub, fill as People mechanics land).

### Scope merges

1. **`weekly.md` + `weekly-reconcile.md` → `weekly.md`.**
   New structure: Get Clear, Get Current, Get Creative, Gmail Reconcile, Calendar Pressure, Integrity Checks. Drop `weekly-reconcile` agent mode from `gtd-weekly.md`.

2. **`project-structure.md` redistribution.**
   - Structural doctrine → `canonical-vault.md` (Canonical Project Model, Link Principles, Design Note Contract).
   - Behavioral doctrine → `conventions.md` (any cross-cutting rules).
   - Migration/retrofit-only content → new `project-retrofit.md`.

3. **`analyze-vault.md` + `verify-project-structure.md` → `vault-audit.md` + two command aliases.**
   Two commands point at the same procedure with mode flags.

### New agents

All four existing agents get minor edits. Seven new agents:

| Agent               | Model  | Purpose                                           |
| ------------------- | ------ | ------------------------------------------------- |
| `gtd-assistant.md`  | Opus   | Top-level persona, warm-start, menu, coach router |
| `gtd-signals.md`    | Sonnet | Signal-sync ceremony (dry-run → confirm → apply)  |
| `gtd-retrofit.md`   | Opus   | Vault audit + retrofit procedure                  |
| `gtd-junk-sweep.md` | Sonnet | 2h inbox garbage-only sweep                       |
| `gtd-gws-fetch.md`  | Haiku  | Mechanical gws Gmail/Calendar/People fetches      |
| `gtd-vault-scan.md` | Haiku  | Mechanical vault counts, orphan scans, mtime ops  |
| `gtd-signal-diff.md`| Haiku  | `sync_gtd_signals.py --dry-run` wrapper           |

### Command layer changes

| Current                             | New                          | Change                            |
| ----------------------------------- | ---------------------------- | --------------------------------- |
| `gtd-cleanup.md`                    | `gtd-organize.md`            | Rename for consistency            |
| `gtd-signals-sync.md`               | `gtd-signals-sync.md`        | Rewire `agent: gtd-signals`       |
| `analyze-vault.md`                  | `gtd-analyze.md`             | Rename + fix stale `.opencode/`   |
| `retrofit-vault.md`                 | `gtd-retrofit.md`            | Rename                            |
| `verify-project-structure.md`       | `gtd-verify-projects.md`     | Rename                            |
| —                                   | `gtd-junk-sweep.md`          | New                               |
| —                                   | `gtd-assistant.md`           | New (optional)                    |

---

## Part IV — Language pass (Lens C)

### Banned vocabulary

In every reference and agent file, replace or eliminate:

| Banned phrase          | Replacement                                                                 |
| ---------------------- | --------------------------------------------------------------------------- |
| "truly <=5 minutes"    | "<=5 minutes AND context+tools available"                                   |
| "meaningful"           | Named criterion (e.g. "has ≥1 open `#task` AND ≥1 journal link in 14 days") |
| "when appropriate"     | Remove or specify the signal                                                |
| "as needed"            | Remove or specify the trigger condition                                     |
| "clearly actionable"   | "the user is the next actor AND action is expressible as one verb phrase"   |
| "high-signal" / "noise"| Reference `email-triage-policy.md § Heuristics` — do not hedge              |
| "prefer X"             | "Use X. Exception: <named case>."                                           |
| "usually" / "generally"| Imperative + named exception                                                |

### Cross-file style standards

- **Heading at file top:** every reference starts with `# <Title>`. `email-triage-policy.md` already does; others use `##` — promote all.
- **Scope as bullet list** in every reference with a Scope section (not prose).
- **Output section heading:** uniform `## Output` (not `### Daily Output`, `### Weekly Output`, etc., within their files — these can be `## Output` consistently).
- **Imperative voice:** "Classify the thread" not "The thread should be classified."
- **`AskUserQuestion` wording:** every "ask the user" / "confirm with user" replaced with explicit "via `AskUserQuestion`" or "without `AskUserQuestion` — execute silently" so the channel is never ambiguous.
- **Table precedence:** every overlapping-row table states "Evaluate top-to-bottom; first match wins" or declares non-overlap explicitly. Applies to `email-triage-policy.md § Classification Defaults` and `signal-sync.md § Signal Rules`.
- **Symbolic vs literal labels:** always define the mapping once per file; never use `IMPORT_LABEL` without a visible mapping in the same file.

### Per-file priority (critical files first)

| File                       | Findings | Priority  |
| -------------------------- | -------- | --------- |
| `daily.md`                 | 12       | Critical  |
| `gmail-intake.md` (new)    | 11 in.   | Critical  |
| `email-triage-policy.md`   | 8        | Critical  |
| `assistant.md`             | 7        | High      |
| `weekly.md`                | 3        | High      |
| Others                     | ≤3 each  | Medium    |

Cross-file style pass applied uniformly.

---

## Part V — The five user-reported issues

### Issue 1: Ceremony never finishes (compounding: no stop / context / re-loops)

Four-gate termination added to `daily.md`:

1. **Classification queue empty** — Step 1 query returns zero threads on re-run.
2. **Import/Waiting queues drained** — Step 2 queries return zero unprocessed.
3. **Calendar ask queue reviewed** — every attendee event has a decision.
4. **User confirms end** — `AskUserQuestion` with residual state; accept only explicit "end ceremony."

**Context management:** when classification candidate set exceeds 25 threads, `gtd-daily` agent delegates Step 1 classification via a single Task tool call returning compact `{thread_id, outcome, rationale}` tuples. Checkpoint after each of Steps 1/2/4.

**Dedupe hardening:**
- `IMPORTED_LABEL` becomes **required** (Step 0 blocker if missing).
- In-run processed set keyed by `thread_id` (and `SHA1(task_text)` for self-capture).
- Self-capture tasks carry `(capture_hash:: <sha1>)` metadata — blocks re-import.

### Issue 2: Process junk first

Invert three ordering instructions:

- `daily.md:7` — "garbage FIRST for bulk confirmation, then actionable/ambiguous"
- `gmail-intake.md` Bulk Review Pattern — "garbage-first presentation"
- `agents/gtd-daily.md:20` — "GARBAGE FIRST (bulk-approve obvious trash), actionable/ambiguous after"

The bulk-review sub-procedure in `gmail-intake.md` defines: (a) classify whole queue; (b) present garbage batch; (c) confirm + execute trash; (d) present actionable batch; (e) confirm + execute labels. Garbage confirmation must complete before actionables are presented.

### Issue 3: Haiku for mechanical gws + vault scans

**Three new Haiku subagents** (`gtd-gws-fetch`, `gtd-vault-scan`, `gtd-signal-diff`) handle:

- `gws gmail users labels list` / threads list / +triage fetches
- `gws calendar +agenda` fetches
- `gws people ...` exact-match lookups
- Batch label mutations with pre-resolved IDs
- Vault scans (inbox counts, orphan detection, stalled-project mtimes)
- Signal-sync dry-run diff

**NOT Haiku:** email classification (keep existing `daily-intake.md` warning), GTD clarify, project-vs-area decisions, stalled-project interpretation, ambiguous people-link resolution, appointment triage.

**Global Haiku ban reconciliation:** skill-scoped override in `SKILL.md § Guardrails`:

> **Model routing (skill-scoped override of the global Haiku ban).** The global rule "ALWAYS use opus / NEVER use haiku" applies to judgment and classification work. Within this skill it is explicitly overridden for three mechanical subagents: `gtd-gws-fetch`, `gtd-vault-scan`, `gtd-signal-diff`. These must be dispatched with `model: "haiku"`. All other subagent dispatches — including `gtd-daily`, `gtd-weekly`, `gtd-monthly`, `gtd-organizing`, `gtd-signals`, `gtd-retrofit`, `gtd-junk-sweep`, `gtd-assistant`, and any email-triage or GTD-clarify call — continue to use `opus` per the global rule. Haiku output failing validation escalates to `opus` — never retry Haiku.

**Guardrails for Haiku calls:**
- Structured JSON input (not free-form).
- Documented output schema (envelope: `{"ok": true, "data": ...}`).
- Caller validates via `jq -e` or regex before acting.
- On validation fail: escalate same op to self (Opus/Sonnet); no Haiku retry.
- No free-form commentary — envelope only.
- No query-derived mutations; only pre-resolved id lists.

### Issue 4: 2h junk sweep via `/loop`

**New slash command** `commands/gtd-junk-sweep.md` wraps the new `gtd-junk-sweep` agent. User invokes `/loop 2h /gtd-junk-sweep` once per session.

**`gtd-junk-sweep` agent scope (Sonnet, narrow):**
- Pull `in:inbox -label:gtd/* -label:gtd/imported` candidates via `gtd-gws-fetch`.
- Classify per `email-triage-policy.md` into `garbage` or `defer` only.
- `AskUserQuestion` with one grouped option per trash category plus "Skip" and "Override individually."
- On confirm: one `messages.batchModify` with `addLabelIds:["TRASH"]` via `gtd-gws-fetch`.
- Append result to `System/.gtd-coach-state.jsonl` as `{kind:"junk-sweep", ts, trashed, deferred, categories}`.

**Sweep invariants:**
- Never import, label, classify ambiguous mail, create tasks, forward, or unsubscribe.
- Empty candidate set → silent return; log `trashed:0`.
- Auth/scope error → log `kind:"junk-sweep", trashed:0, error:...` and stop.
- Never invoke other ceremony agents.

**Integration with daily:** `gmail-intake.md` adds a "Step 1b — Prior Junk-Sweep Awareness": if JSONL contains a `junk-sweep` entry newer than last daily, subtract its trashed IDs from candidate set before classification.

### Issue 5: Proactive coach persona

**New `references/coach.md`** owns coach doctrine. **`assistant.md`** keeps only warm-start + menu; coach runs every turn after warm-start.

**State file:** `System/.gtd-coach-state.jsonl` — append-only JSONL, one event per line. Event kinds: `session-start`, `junk-sweep`, `ceremony`, `nudge`.

**Daily rhythm** (local wall-clock + elapsed-since triggers):

| Window (local)  | Trigger                                                           | Nudge label                    |
| --------------- | ----------------------------------------------------------------- | ------------------------------ |
| 06:00–10:30     | First turn AND no `ceremony/daily` today                          | `morning-ceremony-prompt`      |
| 10:30–14:00     | Loop inactive AND inbox candidates ≥ 20                           | `midday-start-sweep-loop`      |
| 14:00–17:30     | Stalled project (>14d) AND not nudged this session                | `stalled-project:<name>`       |
| 17:30–22:00     | No `ceremony/daily` today AND Inbox.md has ≥10 `#inbox`           | `evening-wrap-up`              |
| Any             | Last 3 completions all `#deep` AND >2h wall-clock deep-work       | `context-switch:deep-to-errand`|
| Any             | Sweep `trashed > 0`                                               | `ambient-sweep-complete`       |

**Nudge invariants:**
- ≤1 nudge per assistant turn; always final line; prefix `·`.
- ≤4 total nudges per calendar day.
- Before emitting: check JSONL for same-label nudge today; skip if present.
- After emitting: append `kind:"nudge", label, ts` to JSONL.
- Suppressed while ceremony agents are active.
- Only labels in the above table may be emitted — no free-style nudges.
- Silent-by-default — emitting nothing is valid.

**Handoff from ceremonies:** `gtd-daily` agent writes a `kind:"ceremony", name:"daily", ts, outcome, residual:[...]` event to the JSONL on exit. Coach reads residual list as context for subsequent nudges. No separate handoff mechanism.

**Vault fallback:** JSONL lives at `System/.gtd-coach-state.jsonl`. If `System/` is absent (retrofit vaults), fall back to vault-root `.gtd-coach-state.jsonl`. One line in `coach.md` documents this.

**Loop-armed detection:** no API to query it. Show "Re-arm 2h junk-sweep loop" button unconditionally in warm-start menu; the `loop` skill handles idempotency or warns on double-arm.

---

## Part VI — Implementation sequencing

Because all changes land in one branch, but some edits depend on others, implementation follows this order. Each step commits separately for review.

### Step 1 — Foundation files (behavioral doctrine)
1. Expand `conventions.md` — absorb Anti-Rules, Journal Hygiene, Inbox Rules, Tag Taxonomy (enriched), Stalled Thresholds.
2. Trim `canonical-vault.md` — keep structural only; move behavioral to `conventions.md`; absorb Canonical Project Model from `project-structure.md`; add Orphan Tasks named rule.
3. Enrich `email-triage-policy.md` — sole Gmail label model with symbolic aliases; precedence note on Classification Defaults; sole Capture Setup.

### Step 2 — Split files
4. Create `gmail-intake.md`, `calendar-intake.md`, `appointment-triage.md`; delete `daily-intake.md`.
5. Create `quick-tasks.md`; trim `assistant.md` to persona + warm-start + menu.
6. Rename `command-reference.md` → `gmail-commands.md`; create stub `calendar-commands.md` and `people-commands.md`.
7. Rename `project-structure.md` → `project-retrofit.md`; redistribute content as above.

### Step 3 — Merge files
8. Absorb `weekly-reconcile.md` into `weekly.md`; delete `weekly-reconcile.md`.
9. Create `vault-audit.md` from union of `commands/analyze-vault.md` + `commands/verify-project-structure.md`.

### Step 4 — New references
10. Create `coach.md`.

### Step 5 — Agent layer
11. Create `gtd-assistant.md`, `gtd-signals.md`, `gtd-retrofit.md`.
12. Create Haiku subagents: `gtd-gws-fetch.md`, `gtd-vault-scan.md`, `gtd-signal-diff.md`.
13. Create `gtd-junk-sweep.md`.
14. Edit existing agents: termination gates, delegation, junk-first ordering, strip duplicate anti-rules (now cross-ref only).

### Step 6 — Command layer
15. Rename `gtd-cleanup.md` → `gtd-organize.md`; `analyze-vault.md` → `gtd-analyze.md`; `retrofit-vault.md` → `gtd-retrofit.md`; `verify-project-structure.md` → `gtd-verify-projects.md`.
16. Rewire `gtd-signals-sync.md` to `agent: gtd-signals`.
17. Create `gtd-junk-sweep.md`, `gtd-assistant.md` commands.
18. Fix stale `.opencode/` paths.

### Step 7 — SKILL.md + root
19. Rewrite `SKILL.md` router and References table.
20. Add Model Routing guardrail block.
21. Update `root/AGENTS.md` to mention `.gtd-coach-state.jsonl`.
22. Update `README.md` for new layout; fix cross-references.

### Step 8 — Language pass
23. Walk every reference and agent. Ban hedge vocabulary. Apply style standards. Uniform headings and Output sections.

### Step 9 — Verification
24. Every file reference in every file resolves to an existing file.
25. Every agent has a reference counterpart; every command has an agent binding.
26. No rule appears verbatim in two places; every non-owning location references by name.
27. Router intents map 1:1 to reference files.
28. `grep` confirms no banned hedge words remain in priority files.

---

## Part VII — Risks and rollback

### Risks

1. **Big-bang refactor on live skill.** The branch is isolated, but once merged, existing sessions reading the old paths may break. Mitigation: land on `refactor/gws-gtd-overhaul`; exercise manually in a test vault before merging.
2. **Haiku subagents untested in production.** Haiku's behavior on structured JSON ops is known but gws JSON schemas are specific. Mitigation: caller-side validation; escalate to Opus on schema mismatch; monitor first week.
3. **Coach nudges annoying in practice.** Silent-by-default + 4/day cap mitigates. If still intrusive, add `/gtd-coach off` command in a follow-up.
4. **Global Haiku ban override normalizes Haiku use.** Mitigation: override is enumerated to three specific agents; all other dispatches remain Opus.
5. **Package consumers using the current layout break on update.** `gws-gtd` is a personal package; single user. Low impact.

### Rollback

Branch-level revert. Every step commits independently, so partial rollback is possible. If Steps 1–3 (foundation) are fine but Steps 11–13 (new agents) misbehave, revert only the agent commits.

---

## Part VIII — Open questions still deferred

1. **Weekly/monthly Haiku routing.** Spec limits mechanical delegation to daily-path ceremonies for scope control. Widen to weekly/monthly in a follow-up if daily-path works.
2. **`Taxes Year.md` template.** Missing from vault; referenced by `canonical-vault.md`. Either create the template or remove the reference. Not blocking this spec.
3. **Coach off-switch.** Not included; add if nudges prove intrusive.
4. **Commands for new agents.** `gtd-assistant.md` command is optional; added if you want the assistant persona as an explicit invocation vs just the default behavior.

---

## Approval required

This spec touches ~30 files in one branch, with renames, deletes, and new files. Before implementation:

1. Approve the target layout in Part I.
2. Approve the router changes in Part II.
3. Approve the file-ownership matrix — this is the hardest thing to change later.
4. Approve the 5-issue design decisions in Part V (JSONL handoff, Sonnet+Haiku split for sweep, override option (a), wall-clock fallback, always-show re-arm button).
5. Approve the implementation sequencing in Part VI.

Once approved, the next step is invoking `writing-plans` to generate a step-by-step implementation plan, then executing it on this branch.
