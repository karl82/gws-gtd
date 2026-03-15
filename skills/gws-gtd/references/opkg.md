## Skill Package Lifecycle (opkg)

This skill is managed as an `opkg` package. Use these commands when making or receiving changes.

### Propagate local edits back to the package source

After editing any file under `.opencode/skills/gws-gtd/`:

```
opkg save gws-gtd
```

This writes changes back to the mutable source at the path defined in `.openpackage/openpackage.yml` (default: `/Users/karl/src/gws-gtd`). Commit and push from that repo to publish upstream.

### Pull upstream changes into the workspace

```
opkg install gws-gtd
```

Run this after pulling changes in the source repo to sync them into the vault workspace.

### Check installed packages

```
opkg list
```
