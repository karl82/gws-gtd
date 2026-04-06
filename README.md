# gws-gtd

`gws-gtd` is an opinionated Claude Code plugin for running [GTD](https://gettingthingsdone.com/) inside an [Obsidian](https://obsidian.md) vault, integrated with [Google Workspace](https://workspace.google.com) ([`gws`](https://github.com/googleworkspace/cli)). It bundles skills, agents, commands, templates, and Dataview queries into a single installable unit.

## Requirements

- [Obsidian](https://obsidian.md) as the vault host
- Claude Code for AI-assisted GTD ceremonies
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

## Claude Plugin

This repository also works as a Claude Code plugin because the repo root already uses Claude's default component directories: `commands/`, `agents/`, and `skills/`.

Add the bundled marketplace and install `gws-gtd` from it:

```bash
claude plugin marketplace add https://github.com/karl82/gws-gtd
claude plugin install gws-gtd@karl82-gtd
```

For local testing from a clone of this repo:

```bash
claude plugin marketplace add .
claude plugin install gws-gtd@karl82-gtd
```

## Development

Edit the plugin source directly in this repository, then reinstall or update it in Claude from the local checkout or marketplace source as needed.

## Scope

This package is intentionally GTD/GWS-only. It excludes unrelated personal templates and helper views that are not part of the core workflow.
