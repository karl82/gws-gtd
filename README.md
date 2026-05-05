# gtd

`gtd` is an opinionated Claude Code plugin for running [GTD](https://gettingthingsdone.com/) inside an [Obsidian](https://obsidian.md) vault, integrated with [Google Workspace](https://workspace.google.com) ([`gws`](https://github.com/googleworkspace/cli)). One skill, one agent, three commands.

## Requirements

- [Obsidian](https://obsidian.md) as the vault host
- Claude Code for AI-assisted GTD ceremonies
- [`gws` CLI](https://github.com/googleworkspace/cli), authenticated
- `jq`
- [`transcrypt`](https://github.com/elasticdog/transcrypt) for encrypted git repos (optional)
- The `ralph-loop` Claude Code plugin (only for `/gtd-drain`)

## What it installs

| Path | Purpose |
|---|---|
| `skills/gtd/` | Core GTD + Google Workspace skill |
| `skills/gws-doc-review-sync/` | Markdown-as-source Google Docs review sync (separate skill) |
| `skills/transcrypt-git-repo/` | Git encryption operations (separate skill) |
| `agents/gtd.md` | The single GTD agent |
| `commands/gtd.md` | Main slash command — ceremony or assistant |
| `commands/gtd-sweep.md` | Narrow Gmail junk-only sweep |
| `commands/gtd-drain.md` | Backlog drain via ralph-loop |
| `root/AGENTS.md` | Vault-root agent entrypoint |
| `root/System/Templates/` | Obsidian templates (Daily, Weekly Review, Monthly Review, Project Template, Person, Design Note, Recruiter Decline Email) |
| `root/System/Queries/` | Dataview JS queries for tasks, projects, journals, audits |

## Package layout

```text
skills/
  gtd/
    SKILL.md
    README.md
    reference.md
    triage-policy.md
    commands.md
    scripts/sync_signals.py
  gws-doc-review-sync/
  transcrypt-git-repo/
agents/
  gtd.md
commands/
  gtd.md
  gtd-sweep.md
  gtd-drain.md
root/                          ← placed at vault root on install
  AGENTS.md
  System/
    Templates/
    Queries/
openpackage.yml
```

## Opinionated defaults

- canonical folders: `Projects/`, `Areas/`, `People/`, `Resources/`, `Archive/`, `Journal/`, `System/`
- canonical task syntax: `- [ ] #task ...`
- Gmail labels rooted under `gtd/`
- `GTD Signals` calendar mirrors dated `#next` and dated `#waiting` follow-ups
- one canonical task line per commitment

## Claude plugin

This repository works as a Claude Code plugin because the repo root uses Claude's default component directories: `commands/`, `agents/`, and `skills/`.

Add the bundled marketplace and install:

```bash
claude plugin marketplace add https://github.com/karl82/gws-gtd
claude plugin install gtd@karl82-gtd
```

For local testing from a clone:

```bash
claude plugin marketplace add .
claude plugin install gtd@karl82-gtd
```

## Slash commands

- `/gtd` — main entry. Optional argument: `daily` / `weekly` / `monthly` / `organize`. Defaults to assistant mode.
- `/gtd-sweep` — narrow Gmail junk-only sweep. Use via `/loop 2h /gtd-sweep` for ongoing maintenance.
- `/gtd-drain` — one-shot bulk backlog drain. Wraps `/gtd-sweep` in a ralph-loop.

## Development

Edit the plugin source directly in this repository, then reinstall in Claude. The full operating model lives in `skills/gtd/reference.md` — one file, ~640 lines.

## Scope

This package is intentionally GTD/GWS-only. No unrelated personal templates or helper views.
