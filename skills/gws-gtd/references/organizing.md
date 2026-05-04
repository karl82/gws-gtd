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
- Move project notes with no open `#task` and no mtime update in 30+ days into `Archive/`.

## Taxes Convention

- Annual notes live in `Projects/Taxes/YYYY.md`.
- Required parent groups: `US`, `CZ`, `Payments`.
- Keep tax tags minimal:
  - `#payment` for payment items.
  - `#waiting` only when blocked externally.
- Template source: `System/Templates/Taxes Year.md`.

## Organizing Output

- Moves or renames completed
- Integrity violations
- Minimal change plan
- Link normalization performed
- Google Docs matches preserved, suggested, or left for user decision
- For each move/rename, include the full task line or full text moved, plus source and destination paths.
