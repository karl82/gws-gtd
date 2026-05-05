# Canonical Vault Model

> **Scope:** Structural model — WHAT the vault looks like. For behavioral doctrine (tags, labels, journal hygiene, anti-rules, interactive decisions), see `conventions.md`. For Gmail label mechanics and classification, see `email-triage-policy.md`. For migration and retrofit procedures, see `project-retrofit.md`.

## Task Syntax

- Globally tracked GTD actions use canonical syntax: `- [ ] #task ...`
- Plain checklists stay local and do not replace canonical GTD tasks.
- **One canonical task line per commitment.** Update lifecycle on the same line using `➕`, `🛫`, `✅`, and `📅`. Never duplicate a task across files to record state changes.
- Due dates use `📅 YYYY-MM-DD`.
- Optional task dependency markers:
  - `🆔 task-id`
  - `⛔ blocker-id`
  - `[id:: task-id]`
  - `[dependsOn:: blocker-id]`
- For GTD state and context tag meanings, see `conventions.md § Tag Taxonomy`.

## Folder Semantics

- `Inbox.md` — transient landing zone for Gmail imports. See `§ Inbox Rules` below.
- `Projects/` — finite outcomes.
- `Areas/` — ongoing responsibilities.
- `People/` — relationship notes and stable contact references.
- `Resources/` — reference-only material.
- `Archive/` — completed or inactive notes.
- `Journal/` — time-based notes, review artifacts, and tasks born from timeline events.
- `System/` (vault-root) — templates, queries, and workflow infrastructure installed from the `gws-gtd` package.

## Canonical Project Model

- Canonical project note path: `Projects/<Domain>/<Project>.md`
- Optional support folder for deeper artifacts: `Projects/<Domain>/<Project>/`
- Project-owned design notes live under `Projects/<Domain>/<Project>/designs/`
- Project-owned support notes may also include `decisions.md`, `notes.md`, and `diagrams/`
- Reusable, non-project-owned reference material belongs in `Resources/`
- Do not keep active project design notes in a separate top-level `Designs/` folder in the canonical end state. Legacy `Designs/` notes are reconciled per `project-retrofit.md`.
- Every active project has a measurable outcome AND at least one open linked `#task`. Plain checklist subtasks do not satisfy the open-task requirement.

## Linking Rules

- Use full vault-relative links for canonical entities under `Projects/`, `Areas/`, and `People/`.
- Prefer `[[Projects/Work/Billing Revamp]]` over `[[Billing Revamp]]`.
- Prefer `[[Areas/Home]]` over `[[Home]]`.
- Prefer `[[People/Jane Doe]]` over `[[Jane Doe]]` when linking to canonical people notes.
- Every active project task must include a full `[[Projects/<Domain>/<Project>]]` link.
- Every active area task must include a full `[[Areas/...]]` link.
- Design-specific tasks may include both the project link and the design link, but never the design link alone.
- Every design note must link back to its canonical project note using the full project path.

## Design Note Contract

Design notes intended for Google Docs review or export must carry frontmatter:

- `project: "[[Projects/<Domain>/<Project>]]"`
- `gdoc_id`
- `gdoc_url`
- `gdoc_source_of_truth: markdown|google-docs`

If multiple Markdown notes publish into one Google Doc with tabs, use:

- `gdoc_role: main|tab`
- `gdoc_tab_title`

If a design note is an exported mirror from Google Docs, treat Markdown as read-only and keep export metadata such as `gdoc_revision_id` and `gdoc_last_exported_at`.

## Inbox Rules

- Inbox state is tag-driven through `#inbox`, not file-driven.
- `Inbox.md` is the **required** transient staging area for Gmail imports. Tasks leave on clarify — either to a project/area file, or to the daily journal note with a wikilink.
- Journal-born `#inbox` tasks stay in the journal file. On clarify, remove `#inbox` and add the `[[Projects/...]]` or `[[Areas/...]]` wikilink.
- Inbox tasks must never remain marked completed.
- For clarify semantics and `#inbox` removal doctrine, see `conventions.md § Tag Taxonomy § #inbox semantics`.

## Orphan Tasks

An **orphan task** is an open `#task` that meets ALL of:

- Does not carry `#inbox`
- Has no `[[Projects/...]]` or `[[Areas/...]]` wikilink
- Does not live inside a `Projects/` or `Areas/` file

Tasks in `Journal/` or elsewhere that carry a valid wikilink are NOT orphans — do not flag or relocate them.

This definition is referenced from `weekly.md` (Integrity Checks) and `organizing.md`.

## Journal Paths

- Daily note: `Journal/YYYY-MM-DD.md`
- Weekly review note: `Journal/YYYY-WNN.md` (e.g. `Journal/2026-W15.md`)
- Monthly review note: `Journal/YYYY-MM.md` (e.g. `Journal/2026-04.md`)
- File clarified tasks in the daily note for the date the task was captured (`➕ YYYY-MM-DD`), not today's date.
- For journal entry hygiene, see `conventions.md § Journal Hygiene`.

## Someday/Maybe Rules

- `#someday` marks incubated items — not currently actionable but worth keeping.
- Someday items stay wherever filed (project, area, or standalone note).
- Weekly review includes a quick scan; monthly review does a deeper pass for promotion or deletion.

## Review Rules

- Weekly review uses `System/Templates/Weekly Review.md`.
- Monthly review uses `System/Templates/Monthly Review.md`.
- Shared task and review views live in `System/Queries/`.
- Central query exclusions live in `System/Queries/Task Query Config.md`.

## Areas and Archive

- Areas express ongoing responsibilities, not outcomes.
- Archive reduces active-surface clutter but preserves retrieval.
- Default baseline areas: `Areas/Home.md`, `Areas/Finances.md`, `Areas/Relationships.md`, `Areas/Admin.md`. Keep unless a split is justified.

## Taxes Convention

- Annual tax notes live in `Projects/Taxes/YYYY.md`.
- Required parent action groups: `US`, `CZ`, `Payments`.
- Parent items use canonical `#task` syntax.
- Child checklist items stay non-`#task`.
- Tag usage follows `conventions.md § Tag Taxonomy`; do not invent tax-specific tags.
- Template source: `System/Templates/Taxes Year.md`.
