---
name: gws-gtd
description: Use for the full opinionated gws-gtd workflow: GTD ceremonies, Google Workspace intake/sync, vault retrofit, and transcrypt operations.
compatibility: opencode
metadata:
  repository: gws-gtd
  domain: gws-gtd
---

## Purpose

Use this skill to operate an opinionated GTD vault with Google Workspace, Google Docs review sync, and git/transcrypt support.

The vault is the task system of record. Gmail is the capture/intake layer. Calendar is a signal/review layer. Git plus transcrypt protects the vault when it is synced through repositories.

## Supported Modes

- `analyze-vault`
- `retrofit-vault`
- `daily`
- `weekly`
- `monthly`
- `organizing`
- `daily-intake`
- `weekly-reconcile`
- `event-capture`
- `people-linking`
- `signal-sync`
- `ad-hoc-maintenance`
- `gdoc-bootstrap`
- `gdoc-publish`
- `gdoc-comment-intake`
- `gdoc-apply-feedback`
- `gdoc-reply-resolve`
- `gdoc-status`
- `transcrypt-bootstrap`
- `transcrypt-add-pattern`
- `transcrypt-clone-onboarding`
- `transcrypt-verify`
- `transcrypt-rekey`
- `transcrypt-troubleshoot`

## Router

1. Resolve the user intent.
2. Use the matching reference:
   - `analyze-vault` -> `references/analyze-vault.md`
   - `retrofit-vault` -> `references/retrofit-vault.md`
   - `daily` -> `references/gtd/daily.md`
   - `weekly` -> `references/gtd/weekly.md`
   - `monthly` -> `references/gtd/monthly.md`
   - `organizing` -> `references/gtd/organizing.md`
   - `daily-intake` -> `references/gws/daily-intake.md`
   - `weekly-reconcile` -> `references/gws/weekly-reconcile.md`
   - `event-capture` -> `references/gws/event-capture.md`
   - `people-linking` -> `references/gws/people-linking.md`
   - `signal-sync` -> `references/gws/signal-sync.md`
   - `ad-hoc-maintenance` -> `references/gws/command-reference.md`
   - `gdoc-bootstrap` -> `references/gdoc/bootstrap.md`
   - `gdoc-publish` -> `references/gdoc/publish.md`
   - `gdoc-comment-intake` -> `references/gdoc/comment-intake.md`
   - `gdoc-apply-feedback` -> `references/gdoc/apply-feedback.md`
   - `gdoc-reply-resolve` -> `references/gdoc/resolve.md`
   - `gdoc-status` -> `references/gdoc/status.md`
   - any transcrypt intent -> `references/transcrypt-overview.md`, `references/transcrypt/workflow.md`, `references/transcrypt/command-reference.md`, `references/transcrypt/troubleshooting.md`
3. Follow `references/gtd/canonical-vault.md` and installed runtime files under `System/` at all times.

## Runtime Contract

- `System/GTD Config.md`
- `System/Email Triage Policy.md`
- `System/Templates/`
- `System/Queries/`

## Google Docs Review Contract

- Markdown remains canonical.
- Google Docs is a review surface, not the source of truth.
- Reviewable Markdown notes use `gdoc_*` frontmatter linkage fields.
- Store the full Google Doc URL, not only the raw doc ID.
- If multiple `.md` files live in one directory, treat one file as the main note and publish sibling notes as Google Docs tabs in the same document.
- Apply accepted feedback in Markdown, then reply/resolve corresponding Google Docs comment threads.

## Guardrails

- Preserve canonical actionable syntax: `- [ ] #task ...`
- Keep one canonical task line per commitment.
- Treat inbox as tag-driven via `#inbox`.
- Do not invent deadlines.
- Do not auto-complete tasks unless the workflow explicitly reconciles from a managed external marker.
- Gmail is the only supported mobile capture inbox for this workflow.
- `GTD Signals` is output-only.
- Prefer minimal, reversible edits.
- Do not expose transcrypt passwords or commit plaintext secrets.

## Supporting References

- GTD model: `references/gtd/canonical-vault.md`
- GWS overview: `references/gws-overview.md`
- Google Docs review overview: `references/gdoc-overview.md`
- transcrypt overview: `references/transcrypt-overview.md`

## Output Contract

- State the mode used.
- Report concise decisions and mutations.
- Surface blockers and unresolved decisions.
- When moving text or tasks, include the full line or full text moved.
