# Contributing

## Preferred Workflow

The default maintenance workflow for `gws-gtd` is:

1. edit package-managed files in a consumer vault
2. save them back to the package with `opkg save`
3. review and commit changes in `gws-gtd`
4. reinstall the package into other vaults with `opkg install`

This keeps the package aligned with real day-to-day usage.

## Package-Owned vs Vault-Owned Files

Treat these as package-owned and eligible for `opkg save`:

- `.opencode/skills/`
- `.opencode/commands/`
- `.opencode/agents/`
- package-installed runtime files in `System/`

Treat these as vault-owned and do not sync them back into the package unless you are intentionally extracting a reusable pattern:

- `Projects/`
- `Areas/`
- `People/`
- `Journal/`
- `Resources/`
- active tasks and working notes

## Default Loop

From the vault root:

```bash
opkg save gws-gtd
```

or, if needed:

```bash
opkg save /Users/karl/src/gws-gtd
```

Then in the package repo:

```bash
git status
git diff
git add .
git commit -m "..."
```

To propagate updates back into a vault:

```bash
opkg install /Users/karl/src/gws-gtd --cwd /path/to/vault --platforms opencode --force
```

For Claude Code:

```bash
opkg install /Users/karl/src/gws-gtd --cwd /path/to/vault --platforms claude --force
```

## Notes

- `AGENTS.md` in a vault should stay slim and local.
- Workflow logic belongs in package skills, commands, agents, and package-owned runtime files.
- Source-first editing in `gws-gtd` is still fine, but vault-first is the preferred default.
