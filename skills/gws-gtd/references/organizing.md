# Organizing Procedure

## Scope

Classify, normalize, and clean up notes and tasks according to vault lifecycle rules.

## Core Rules

- `Projects/` = finite outcomes.
- `Areas/` = ongoing responsibilities.
- Use `#task` for globally tracked GTD actions; use plain `- [ ]` for project-local subtasks.
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
- Move project notes with no open `#task` AND mtime past the monthly archive threshold (see `conventions.md § Stalled Thresholds`) into `Archive/`.

## Taxes Convention

See `canonical-vault.md § Taxes Convention`.

## Output

- Moves or renames completed
- Integrity violations
- Minimal change plan
- Link normalization performed
- Google Docs matches preserved, suggested, or left for user decision
- For each move/rename, include the full task line or full text moved, plus source and destination paths.
