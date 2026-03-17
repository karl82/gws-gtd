## Organizing Procedure

### Scope

Classify, normalize, and clean up notes and tasks according to vault lifecycle rules.

### Core Rules

- `Projects/` = finite outcomes.
- `Areas/` = ongoing responsibilities.
- Use `#task` for globally tracked GTD actions; use plain `- [ ]` for project-local subtasks.
- Tasks can live in journal, project, or area files. The `[[Projects/...]]` or `[[Areas/...]]` wikilink is the ownership declaration — not the file location. Do not relocate tasks that already have a valid wikilink.
- Canonical project notes live at `Projects/<Domain>/<Project>.md`.
- Add `Projects/<Domain>/<Project>/` only when the project needs deeper artifacts.
- Keep project-owned designs under `Projects/<Domain>/<Project>/designs/`.
- Normalize project, area, and people links to full vault-relative links.
- Keep baseline areas unless split is justified:
  - `Areas/Home.md`
  - `Areas/Finances.md`
  - `Areas/Relationships.md`
  - `Areas/Admin.md`
- Keep reference-only material in `Resources/`.
- Treat legacy top-level `Designs/` notes as adaptable and reconcile them toward the owning project or `Resources/`.
- Move finished or inactive project notes into `Archive/` when appropriate.

### Taxes Convention

- Annual notes live in `Projects/Taxes/Taxes YYYY.md`.
- Required parent groups: `US`, `CZ`, `Payments`.
- Keep tax tags minimal:
  - `#payment` for payment items.
  - `#waiting` only when blocked externally.
- Template source: `System/Templates/Taxes Year.md`.

### Organizing Output

- Moves or renames completed
- Integrity violations
- Minimal change plan
- Link normalization performed
- Google Docs matches preserved, suggested, or left for user decision
- For each move/rename, include the full task line or full text moved, plus source and destination paths.
