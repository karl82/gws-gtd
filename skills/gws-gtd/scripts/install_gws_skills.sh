#!/usr/bin/env bash

set -euo pipefail

workspace_dir="${GWS_GTD_WORKSPACE_DIR:-$HOME/src/cml}"
source_ref="${GWS_GTD_GWS_SKILLS_SOURCE:-https://github.com/googleworkspace/cli}"
obsidian_mcp_package="${GWS_GTD_OBSIDIAN_MCP_PACKAGE:-@mauricio.wolff/mcp-obsidian@latest}"
obsidian_mcp_name="${GWS_GTD_OBSIDIAN_MCP_NAME:-obsidian}"
dry_run=0
list_only=0
skip_obsidian_mcp=0

agents=(
  "claude-code"
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
  obsidian:  install local MCP entry for Obsidian if missing
  agents:    claude-code
  skills:    built-in GTD skill bundle from this script

Options:
  --workspace DIR   Target workspace root.
  --source REF      GitHub repo, git URL, or local path accepted by `npx skills add`.
  --obsidian-mcp-package REF
                    npm package for the Obsidian MCP server.
  --skip-obsidian-mcp
                    Skip installing the local Obsidian MCP entry.
  --skill NAME      Add an extra skill to install. May be repeated.
  --agent NAME      Override default agents. May be repeated.
  --list            List available skills and exit.
  --dry-run         Print the command without running it.
  --help            Show this help.

Notes:
  - Claude project skills install into .claude/skills/
  - Claude MCP installs at local scope for the target workspace
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

has_agent() {
  local needle="$1"
  local agent

  for agent in "${agents[@]}"; do
    if [[ "$agent" == "$needle" ]]; then
      return 0
    fi
  done

  return 1
}

print_step() {
  printf '\n==> %s\n' "$1"
}

ensure_claude_obsidian_mcp() {
  local json_payload

  if ! has_agent "claude-code"; then
    return 0
  fi

  json_payload="$(python3 - "$obsidian_mcp_package" "$workspace_dir" <<'PY'
import json
import sys

package_name, workspace = sys.argv[1], sys.argv[2]
print(json.dumps({
    "type": "stdio",
    "command": "npx",
    "args": ["-y", package_name, workspace],
}))
PY
)"

  if [[ $dry_run -eq 1 ]]; then
    printf 'Command: (cd %q && claude mcp add-json %q --scope local %q)\n' \
      "$workspace_dir" "$obsidian_mcp_name" "$json_payload"
    return 0
  fi

  if ! command -v claude >/dev/null 2>&1; then
    printf 'Skipping Claude MCP install because `claude` is not available.\n'
    return 0
  fi

  if (
    cd "$workspace_dir"
    claude mcp get "$obsidian_mcp_name" >/dev/null 2>&1
  ); then
    printf 'Claude MCP `%s` already configured.\n' "$obsidian_mcp_name"
    return 0
  fi

  printf 'Claude MCP `%s` missing; installing local entry.\n' "$obsidian_mcp_name"

  (
    cd "$workspace_dir"
    claude mcp add-json "$obsidian_mcp_name" --scope local "$json_payload"
  )
}

ensure_obsidian_mcp() {
  if [[ $skip_obsidian_mcp -eq 1 ]]; then
    printf 'Skipping Obsidian MCP bootstrap.\n'
    return 0
  fi

  print_step "Ensuring Obsidian MCP"
  ensure_claude_obsidian_mcp
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
    --obsidian-mcp-package)
      obsidian_mcp_package="$2"
      shift 2
      ;;
    --skip-obsidian-mcp)
      skip_obsidian_mcp=1
      shift
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
printf 'Obsidian MCP package: %s\n' "$obsidian_mcp_package"
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
  if [[ $list_only -eq 0 ]]; then
    ensure_obsidian_mcp
  fi
  exit 0
fi

(
  cd "$workspace_dir"
  "${cmd[@]}"
)

if [[ $list_only -eq 0 ]]; then
  ensure_obsidian_mcp
fi
