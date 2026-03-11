# gws-gtd

`gws-gtd` is an opinionated OpenPackage package for running a GTD vault with Google Workspace (`gws`), Google Docs review sync, and git/transcrypt support.

## What It Installs

- `gtd-getting-things-done` for GTD ceremonies
- `gws-gtd-operations` for Gmail, Calendar, People, and signal-sync workflows
- `gws-doc-review-sync` for Markdown-as-source Google Docs review
- `transcrypt-git-repo` for git encryption operations
- commands for vault analysis and retrofit
- vault runtime files under `System/`, including templates, queries, and email triage policy

## Package Layout

```text
skills/
  gtd-getting-things-done/
  gws-gtd-operations/
  gws-doc-review-sync/
  transcrypt-git-repo/
commands/
  analyze-vault.md
  retrofit-vault.md
root/
  System/
    GTD Config.md
    Email Triage Policy.md
    Templates/
    Queries/
AGENTS.md
openpackage.yml
```

## Opinionated Defaults

- canonical folders: `Projects/`, `Areas/`, `People/`, `Resources/`, `Archive/`, `Journal/`, `System/`
- canonical task syntax: `- [ ] #task ...`
- Gmail labels rooted under `gtd/`
- `GTD Signals` calendar for mirrored action/follow-up signals
- one canonical task line per commitment

## Install

Once the repo exists on GitHub, install with:

```bash
opkg install gh@karl82/gws-gtd
```

Then review the installed `AGENTS.md`, `System/GTD Config.md`, and `System/Email Triage Policy.md` in the target vault.

## Scope

This package is intentionally GTD/GWS-only. It excludes unrelated personal templates and helper views that are not part of the core workflow.
