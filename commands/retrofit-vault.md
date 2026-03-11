Retrofit an existing vault toward the canonical `gws-gtd` model.

Steps:

1. Run an analysis pass first.
2. Preserve existing vault content unless a move or rename is explicitly required.
3. Install missing package-owned files under `System/` and `AGENTS.md`.
4. Do not silently rewrite unrelated notes.
5. If task syntax or folder placement diverges, propose the migration first and apply only the agreed changes.
6. Keep one canonical task line per commitment; do not duplicate tasks during migration.
7. Preserve links and metadata when moving project, area, or people notes.

Output:

- files installed
- files left untouched
- structural conflicts needing user decision
- exact next steps to finish alignment
