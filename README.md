# gws-gtd

`gws-gtd` is an opinionated [OpenPackage](https://github.com/anomalyco/openpackage) package for running [GTD](https://gettingthingsdone.com/) inside an [Obsidian](https://obsidian.md) vault, integrated with [Google Workspace](https://workspace.google.com) (`gws`). It bundles skills, agents, commands, templates, and Dataview queries into a single installable unit.

## Requirements

- [Obsidian](https://obsidian.md) as the vault host
- [OpenCode](https://opencode.ai) / Claude Code for AI-assisted GTD ceremonies
- [`opkg`](https://github.com/anomalyco/openpackage) CLI for install/save
- [`transcrypt`](https://github.com/elasticdog/transcrypt) for encrypted git repos (optional)

## What It Installs

| Path | Purpose |
|---|---|
| `skills/gws-gtd/` | Core GTD + Google Workspace workflow guidance |
| `skills/gws-doc-review-sync/` | Markdown-as-source Google Docs review sync |
| `skills/transcrypt-git-repo/` | Git encryption operations via transcrypt |
| `agents/` | GTD ceremony agents (daily, weekly, monthly, organizing) |
| `commands/` | Slash commands for ceremonies and vault maintenance |
| `root/AGENTS.md` | Vault-root agent entrypoint |
| `root/System/Templates/` | Obsidian templates (Daily, Weekly, Monthly, Project, Person, …) |
| `root/System/Queries/` | Dataview JS queries for tasks, projects, journals, audits |

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
  gtd-daily.md
  gtd-weekly.md
  gtd-monthly.md
  gtd-cleanup.md
  analyze-vault.md
  retrofit-vault.md
  verify-project-structure.md
root/                          ← placed at vault root on install
  AGENTS.md
  System/
    Templates/
      Daily.md
      Weekly Review.md
      Monthly Review.md
      Project Template.md
      Person.md
      Design Note.md
      Recruiter Decline Email.md
    Queries/
      task-list.js
      daily-due.js
      weekly-due.js
      monthly-due.js
      project-linked-open.js
      project-linked-done.js
      project-structure-audit.js
      area-linked-open.js
      person-interactions.js
      journal-weekly.js
      journal-monthly.js
      project-designs.js
      Task Query Config.md
openpackage.yml
```

## Opinionated Defaults

- canonical folders: `Projects/`, `Areas/`, `People/`, `Resources/`, `Archive/`, `Journal/`, `System/`
- canonical task syntax: `- [ ] #task ...`
- Gmail labels rooted under `gtd/`
- `GTD Signals` calendar for mirrored action/follow-up signals
- one canonical task line per commitment

## Install

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
