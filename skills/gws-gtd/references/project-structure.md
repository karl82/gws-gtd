## Project Structure Principles

### Scope

Define the canonical project and design note layout for `gws-gtd`, including strict link rules, Google Docs review metadata, and migration guidance for existing vaults.

### Canonical Project Model

- Canonical project note path: `Projects/<Domain>/<Project>.md`
- Optional support folder for deeper project material: `Projects/<Domain>/<Project>/`
- Project-owned design notes live under `Projects/<Domain>/<Project>/designs/`
- Project-owned support notes may also include `decisions.md`, `notes.md`, and `diagrams/`
- Do not keep active project design notes in a separate top-level `Designs/` folder in the canonical end state
- Reusable, non-project-owned architecture or reference material belongs in `Resources/`

### Link Principles

- Full vault-relative links are required for canonical entities
- Canonical entities are `Projects/`, `Areas/`, `People/`, and project-owned design notes
- Prefer `[[Projects/Work/Billing Revamp]]` over `[[Billing Revamp]]`
- Prefer `[[Areas/Home]]` over `[[Home]]`
- Prefer `[[People/Jane Doe]]` over `[[Jane Doe]]` when linking to canonical people notes
- Every active project task must include a full project link
- Every active area task must include a full area link
- Design-specific tasks may include both the project link and the design link, but never the design link alone

### Design Note Contract

- Every design note must link back to its canonical project note using the full project path
- Design notes intended for Google Docs review or export must carry frontmatter:
  - `project: "[[Projects/<Domain>/<Project>]]"`
  - `gdoc_id`
  - `gdoc_url`
  - `gdoc_source_of_truth: markdown|google-docs`
- If multiple Markdown notes publish into one Google Doc with tabs, use:
  - `gdoc_role: main|tab`
  - `gdoc_tab_title`
- If a design note is an exported mirror from Google Docs, treat Markdown as read-only and keep export metadata such as `gdoc_revision_id` and `gdoc_last_exported_at`

### Idiomatic Obsidian Bias

- Use a normal project note at `Projects/<Domain>/<Project>.md`; do not require `index.md`
- Keep small projects lightweight as one note until deeper artifacts are needed
- Add the sibling support folder only when the project grows beyond one note
- Preserve natural note titles during migration whenever possible

### Migration and Retrofit Principles

- Treat legacy top-level `Designs/` notes as `adaptable` by default
- Reconcile project-owned design notes into `Projects/<Domain>/<Project>/designs/`
- Move reusable or shared reference design material into `Resources/`
- If ownership is ambiguous, classify as `needs-decision` rather than guessing
- Normalize short links to full vault-relative canonical links during retrofit
- Preserve note content, metadata, and review history while reconciling structure

### Google Docs Matching During Migration

- Try to match design notes to existing Google Docs before proposing new review surfaces
- Use existing frontmatter first: `gdoc_id`, `gdoc_url`, `gdoc_role`, `gdoc_tab_title`
- If metadata is missing, infer cautiously from nearby project context or sibling design bundles
- If several design notes belong to one reviewed package, prefer one shared `gdoc_id` and `gdoc_url` with tab metadata
- If the match is not safe, ask for the Google Doc URL or specific tab relationship
- Suggest likely name-based matches, but do not auto-assign them without confirmation

### Verification Expectations

- Use Dataview or dedicated audit commands as the compliance layer
- Native Obsidian backlinks or outgoing-links panes are browsing aids, not enforcement
- Verify:
  - canonical project paths
  - explicit full links on active tasks
  - design note placement under project-owned folders
  - required design frontmatter
  - project-to-design backlinks
  - Google Docs doc or tab metadata consistency

### Expected Output

- `compatible`: already canonical
- `adaptable`: can be reconciled cleanly
- `conflicting`: violates canonical invariants
- `needs-decision`: requires explicit ownership or mapping choice
