#!/usr/bin/env bash

set -euo pipefail

workspace_dir="${GWS_GTD_WORKSPACE_DIR:-$HOME/src/cml}"
source_ref="${GWS_GTD_GWS_SKILLS_SOURCE:-https://github.com/googleworkspace/cli}"
dry_run=0
list_only=0

agents=(
  "claude-code"
  "codex"
  "opencode"
)

skills=(
  "gws-gmail"
  "gws-gmail-read"
  "gws-gmail-send"
  "gws-gmail-reply"
  "gws-gmail-reply-all"
  "gws-gmail-forward"
  "gws-gmail-triage"
  "gws-gmail-watch"
  "gws-calendar"
  "gws-calendar-agenda"
  "gws-calendar-insert"
  "gws-people"
  "gws-shared"
  "gws-workflow-email-to-task"
)

usage() {
  cat <<'EOF'
Usage: install_gws_skills.sh [options]

Install GTD-relevant Google Workspace skills into a workspace such as ~/src/cml.

Defaults:
  workspace: ~/src/cml
  source:    https://github.com/googleworkspace/cli
  agents:    claude-code, codex, opencode
  skills:    built-in GTD skill bundle from this script

Options:
  --workspace DIR   Target workspace root.
  --source REF      GitHub repo, git URL, or local path accepted by `npx skills add`.
  --skill NAME      Add an extra skill to install. May be repeated.
  --agent NAME      Override default agents. May be repeated.
  --list            List available skills and exit.
  --dry-run         Print the command without running it.
  --help            Show this help.

Notes:
  - Claude project skills install into .claude/skills/
  - Codex and OpenCode project skills install into .agents/skills/
EOF

  printf '\nDefault skills:\n'
  printf '  %s\n' "${skills[@]}"
}

require_cmd() {
  if ! command -v "$1" >/dev/null 2>&1; then
    printf 'Missing required command: %s\n' "$1" >&2
    exit 1
  fi
}

if [[ $# -gt 0 ]]; then
  custom_agents=0
else
  custom_agents=0
fi

while [[ $# -gt 0 ]]; do
  case "$1" in
    --workspace)
      workspace_dir="$2"
      shift 2
      ;;
    --source)
      source_ref="$2"
      shift 2
      ;;
    --skill)
      skills+=("$2")
      shift 2
      ;;
    --agent)
      if [[ $custom_agents -eq 0 ]]; then
        agents=()
        custom_agents=1
      fi
      agents+=("$2")
      shift 2
      ;;
    --list)
      list_only=1
      shift
      ;;
    --dry-run)
      dry_run=1
      shift
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      printf 'Unknown argument: %s\n\n' "$1" >&2
      usage >&2
      exit 1
      ;;
  esac
done

require_cmd "npx"

if [[ ! -d "$workspace_dir" ]]; then
  printf 'Workspace directory does not exist: %s\n' "$workspace_dir" >&2
  exit 1
fi

cmd=(npx skills add "$source_ref" --yes)

for agent in "${agents[@]}"; do
  cmd+=(--agent "$agent")
done

if [[ $list_only -eq 1 ]]; then
  cmd+=(--list)
else
  for skill in "${skills[@]}"; do
    cmd+=(--skill "$skill")
  done
fi

printf 'Workspace: %s\n' "$workspace_dir"
printf 'Source: %s\n' "$source_ref"
printf 'Agents: %s\n' "${agents[*]}"

if [[ $list_only -eq 1 ]]; then
  printf 'Mode: list\n'
else
  printf 'Skills: %s\n' "${skills[*]}"
fi

printf 'Command: (cd %q &&' "$workspace_dir"
printf ' %q' "${cmd[@]}"
printf ')\n'

if [[ $dry_run -eq 1 ]]; then
  exit 0
fi

(
  cd "$workspace_dir"
  "${cmd[@]}"
)
