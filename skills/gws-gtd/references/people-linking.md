## People Linking Procedure

### Scope

- Link Google Contacts and meeting/email participants to `People/` notes.
- Prefer deterministic matching and avoid noisy false positives.
- Use the installed `gws-people` skill for contact pulls and lookups.

### Contact Pull

Use the installed `gws-people` skill.

### Matching Strategy

1. Primary key: exact email match.
2. Secondary key: normalized full name.
3. If ambiguous, do not auto-link; return to user for decision.

### People Note Fields

Recommended structure in `People/Name.md`:

- Frontmatter:
  - `google_contact_id`
  - `last_contact_sync`
- Relationship section:
  - `Contact: [Google Contact](...)`

The clickable Google Contact link is required in the note body alongside `google_contact_id`.

Do not copy contact details such as email addresses or phone numbers into People notes from Google Contacts. Treat Google Contacts as the source of truth and store only the stable Google reference needed for linking.

### Link Injection

- When importing Gmail or calendar items, append `[[People/Name]]` only on high-confidence match.
- Keep links in task or note text, not hidden-only metadata.

### Integrity Rules

- Never create tasks from contact data alone.
- Never mutate unrelated People notes.
- Keep unresolved matches in a short review list.
