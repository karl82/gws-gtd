# People Commands

Patterns and gotchas for `gws people` API calls. Populate this file as People mechanics are discovered during live sessions.

Always pass `--format json` and parse with `jq` in Bash. See `SKILL.md § Guardrails`.

## Contact lookup

```bash
gws people people searchContacts --params '{"query":"<name-or-email>","readMask":"names,emailAddresses,phoneNumbers"}' --format json
```

Exact-match lookup by email or name. Used by `people-linking.md`.

## Directory search

```bash
gws people people searchDirectoryPeople --params '{"query":"<q>","sources":["DIRECTORY_SOURCE_TYPE_DOMAIN_PROFILE"],"readMask":"names,emailAddresses"}' --format json
```

## Other contacts

```bash
gws people otherContacts search --params '{"query":"<q>","readMask":"names,emailAddresses"}' --format json
```

## Auth and scope

People operations require contacts scopes in the `gws` auth config. On `insufficientPermissions`, report the setup blocker and proceed without people operations.
