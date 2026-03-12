Verify vault project structure, canonical links, and design-to-Google-Docs alignment.

Steps:

1. Inspect `Projects/`, `Areas/`, `People/`, `Resources/`, and any legacy `Designs/` locations.
2. Check whether canonical project notes follow `Projects/<Domain>/<Project>.md`.
3. Check whether deeper project artifacts live under `Projects/<Domain>/<Project>/` and whether project-owned designs live under `Projects/<Domain>/<Project>/designs/`.
4. Audit active `#task` lines for explicit full vault-relative links to canonical project or area notes.
5. Audit design notes for required frontmatter:
   - `project`
   - `gdoc_id`
   - `gdoc_url`
   - `gdoc_source_of_truth`
6. If design notes appear to belong to a shared Google Doc review bundle, verify whether tab metadata is present and stable:
   - `gdoc_role`
   - `gdoc_tab_title`
7. Try to match legacy design notes to existing Google Docs from current metadata first, then from nearby project context; if the match is not safe, classify it as `needs-decision`.
8. Report findings in four buckets:
   - `compatible`
   - `adaptable`
   - `conflicting`
   - `needs-decision`
9. Produce a minimal reconciliation plan that prefers the idiomatic canonical layout over separate top-level `Designs/` directories.

Output:

- concise structure report
- canonical link violations
- design metadata or Google Docs mapping gaps
- exact retrofit sequence
