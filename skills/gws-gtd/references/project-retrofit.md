# Project Retrofit

> **Scope:** Migration and retrofit procedures for moving legacy vault structure toward the canonical model. For the canonical project layout, linking rules, and design-note frontmatter contract, see `canonical-vault.md`.

## Idiomatic Obsidian Bias

- Use a normal project note at `Projects/<Domain>/<Project>.md`; do not require `index.md`.
- Keep small projects lightweight as one note until deeper artifacts are needed.
- Add the sibling support folder only when the project grows beyond one note.
- Preserve natural note titles during migration.

## Migration and Retrofit Principles

- Treat legacy top-level `Designs/` notes as `adaptable` by default.
- Reconcile project-owned design notes into `Projects/<Domain>/<Project>/designs/`.
- Move reusable or shared reference design material into `Resources/`.
- If ownership is ambiguous, classify as `needs-decision` rather than guessing.
- Normalize short links to full vault-relative canonical links during retrofit.
- Preserve note content, metadata, and review history while reconciling structure.

## Google Docs Matching During Migration

- Match design notes to existing Google Docs before proposing new review surfaces.
- Use existing frontmatter first: `gdoc_id`, `gdoc_url`, `gdoc_role`, `gdoc_tab_title`.
- If metadata is missing, infer from nearby project context or sibling design bundles.
- If several design notes belong to one reviewed package, prefer one shared `gdoc_id` and `gdoc_url` with tab metadata.
- If the match is not safe, ask for the Google Doc URL or specific tab relationship via `AskUserQuestion`.
- Suggest name-based matches, but do not auto-assign without confirmation.

## Verification Expectations

Use Dataview or dedicated audit commands as the compliance layer. Native Obsidian backlinks or outgoing-links panes are browsing aids, not enforcement.

Verify during retrofit:

- Canonical project paths match `Projects/<Domain>/<Project>.md`.
- Explicit full links on active tasks.
- Design note placement under project-owned folders.
- Required design frontmatter (per `canonical-vault.md § Design Note Contract`).
- Project-to-design backlinks.
- Google Docs `gdoc_id` or `gdoc_tab_title` consistency.

## Output Buckets

Every retrofit audit classifies candidates into one of:

- `compatible` — already canonical.
- `adaptable` — can be reconciled cleanly.
- `conflicting` — violates canonical invariants.
- `needs-decision` — requires explicit ownership or mapping choice.

## Output

- Counts per bucket.
- For each `adaptable`/`conflicting` item: source path, target path, rationale.
- For each `needs-decision` item: the specific question for the user, surfaced via `AskUserQuestion`.
- Link-normalization actions.
- Google Docs matches: preserved, suggested, or left for user decision.
