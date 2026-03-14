# gws-gtd

`gws-gtd` is an opinionated OpenPackage package for running GTD on Google Workspace (`gws`), with Google Docs review sync and git/transcrypt support.

## What It Installs

- `gws-gtd` for the integrated GTD + Google Workspace workflow
- `gws-doc-review-sync` for Markdown-as-source Google Docs review
- `transcrypt-git-repo` for git encryption operations
- GTD ceremony agents under `agents/`
- commands for vault analysis and retrofit
- vault runtime assets under `System/`, including templates and queries

## Package Layout

```text
skills/
  gws-gtd/
  gws-doc-review-sync/
  transcrypt-git-repo/
agents/
  gtd-daily.md
  gtd-weekly.md
  gtd-monthly.md
  gtd-organizing.md
commands/
  analyze-vault.md
  retrofit-vault.md
root/
  AGENTS.md
  System/
    Templates/
    Queries/
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

Then review the installed `AGENTS.md`, `.opencode/skills/gws-gtd/references/conventions.md`, and `.opencode/skills/gws-gtd/references/email-triage-policy.md` in the target vault.

## Maintenance Workflow

Preferred default: edit package-managed files in a consumer vault, then save them back to the package.

From the vault root:

```bash
opkg save gws-gtd
```

Then review and commit in `gws-gtd`, and reinstall where needed.

Detailed guidance lives in `CONTRIBUTING.md`.

## Scope

This package is intentionally GTD/GWS-only. It excludes unrelated personal templates and helper views that are not part of the core workflow.
