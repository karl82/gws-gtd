# Vault Audit

> **Scope:** Audit an Obsidian vault against the canonical `gws-gtd` model. Emits a compatibility report with retrofit recommendations. Read-only by default; mutations belong to `project-retrofit.md`. For the canonical structure, see `canonical-vault.md`. For behavioral doctrine, see `conventions.md`.

## Audit Steps

1. Inspect folder structure, task syntax, installed runtime assets, and active GTD/GWS notes.
2. Check installed package files:
   - `skills/gws-gtd/SKILL.md`
   - `skills/gws-gtd/references/conventions.md`
   - `skills/gws-gtd/references/canonical-vault.md`
   - `skills/gws-gtd/references/email-triage-policy.md`
   - `System/Templates/`
   - `System/Queries/`
   - `AGENTS.md` (vault root)
3. Verify canonical folder model is present: `Projects/`, `Areas/`, `People/`, `Resources/`, `Archive/`, `Journal/`, `System/`.
4. Audit task syntax per `canonical-vault.md § Task Syntax`:
   - Open tasks use `- [ ] #task ...`.
   - Inbox captures use `#inbox` per `canonical-vault.md § Inbox Rules`.
   - One canonical line per commitment (see `canonical-vault.md § Task Syntax`).
5. Audit project structure per `canonical-vault.md § Canonical Project Model`:
   - Project notes live at `Projects/<Domain>/<Project>.md`.
   - Deeper artifacts under `Projects/<Domain>/<Project>/`.
   - Project-owned designs under `Projects/<Domain>/<Project>/designs/`.
6. Audit linking per `canonical-vault.md § Linking Rules`:
   - Active project tasks carry full `[[Projects/<Domain>/<Project>]]` link.
   - Active area tasks carry full `[[Areas/...]]` link.
   - Design notes link back to their canonical project.
7. Audit design notes per `canonical-vault.md § Design Note Contract`:
   - Required frontmatter: `project`, `gdoc_id`, `gdoc_url`, `gdoc_source_of_truth`.
   - Tab metadata: `gdoc_role`, `gdoc_tab_title` when notes share a Google Doc bundle.
8. Audit orphan tasks per `canonical-vault.md § Orphan Tasks` — tasks without wikilinks that do not live in canonical folders.
9. Audit Google Docs matching for design notes:
   - Match from existing frontmatter first.
   - Infer from nearby project context when metadata is missing.
   - If ownership is ambiguous, classify as `needs-decision`.
10. Verify GWS expectations:
    - Label model rooted at `gtd` (see `email-triage-policy.md § Label Contract`).
    - Gmail-driven intake via `gmail-intake.md`.
    - `GTD Signals` calendar (optional; see `signal-sync.md`).

## Output Buckets

Every audited item is classified into one of:

- `compatible` — already canonical, no action.
- `adaptable` — can be reconciled cleanly, retrofit plan proposed.
- `conflicting` — violates canonical invariants, requires decision.
- `needs-decision` — requires explicit ownership or mapping choice from the user.

## Retrofit Plan

Produce a minimal retrofit sequence that:

- Prefers the idiomatic canonical layout over separate top-level `Designs/` directories.
- Preserves note content, metadata, and review history.
- Normalizes short links to full vault-relative canonical links.
- Surfaces each `needs-decision` item as an explicit question via `AskUserQuestion` (do not guess).

For the retrofit execution procedure, see `project-retrofit.md`.

## Output

- Counts per bucket.
- Concise compatibility report: missing files, canonical link violations, design metadata gaps.
- Recommended retrofit sequence (file moves, link normalizations, frontmatter fills).
- Google Docs matches: preserved, suggested, or left for user decision.
- For each `needs-decision` item: the specific question for the user.
