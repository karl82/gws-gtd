Analyze the current vault against the canonical `gws-gtd` model.

Steps:

1. Inspect folder structure, task syntax, installed `System/` assets, and active GTD/GWS notes.
2. Report findings in three buckets:
   - `compatible`
   - `adaptable`
   - `conflicting`
3. Check for missing or divergent files under:
   - `System/Templates/`
   - `System/Queries/`
   - `System/Email Triage Policy.md`
   - `AGENTS.md`
4. Check whether open tasks use canonical `#task` syntax and whether inbox capture uses `#inbox`.
5. Check whether the vault uses the canonical folder model: `Projects/`, `Areas/`, `People/`, `Resources/`, `Archive/`, `Journal/`, `System/`.
6. Check whether project notes follow the canonical structure: `Projects/<Domain>/<Project>.md` plus optional `Projects/<Domain>/<Project>/` support folders.
7. Check whether active tasks use explicit full vault-relative links for canonical `Projects/` and `Areas/` notes.
8. Check whether design notes are colocated under project-owned `designs/` folders or are otherwise classifiable as `adaptable` or `needs-decision`.
9. Check whether design notes that participate in Google Docs review keep `project`, `gdoc_id`, `gdoc_url`, and `gdoc_source_of_truth` metadata, including tab metadata where relevant.
10. Check whether GWS-specific expectations are present:
   - label model rooted at `gtd`
   - Gmail-driven intake
   - optional `GTD Signals` calendar workflow
11. Produce a minimal retrofit plan.

Output:

- concise compatibility report
- missing files and mismatches
- recommended retrofit sequence
