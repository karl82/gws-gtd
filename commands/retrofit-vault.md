Retrofit an existing vault toward the canonical `gws-gtd` model.

Steps:

1. Run an analysis pass first.
2. Preserve existing vault content unless a move or rename is explicitly required.
3. Install missing package-owned files under `System/` and `AGENTS.md`.
4. Do not silently rewrite unrelated notes.
5. If task syntax or folder placement diverges, propose the migration first and apply only the agreed changes.
6. Keep one canonical task line per commitment; do not duplicate tasks during migration.
7. Preserve links and metadata when moving project, area, or people notes.
8. Reconcile project notes toward `Projects/<Domain>/<Project>.md` and add support folders only when needed.
9. Treat legacy top-level `Designs/` notes as `adaptable` by default; move project-owned designs under `Projects/<Domain>/<Project>/designs/` and reusable reference material to `Resources/`.
10. Normalize short links to full vault-relative links for canonical `Projects/`, `Areas/`, and `People/` notes.
11. During migration, try to match existing design notes to existing Google Docs or tabbed review bundles before proposing new docs.
12. If a Google Doc match is ambiguous, report the likely match and ask for the correct Google Doc URL or tab relationship.

Output:

- files installed
- files left untouched
- structural conflicts needing user decision
- exact next steps to finish alignment
