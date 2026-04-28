#!/usr/bin/env bash

set -euo pipefail

task_root="$(cd "$(dirname "$0")/.." && pwd)"
repo_root="$(cd "$task_root/../../.." && pwd)"
workspace_dir="${1:-/tmp/gws-gtd-daily-intake-workspace}"

rm -rf "$workspace_dir"
mkdir -p "$workspace_dir"
cp -R "$task_root/environment/vault-template/." "$workspace_dir/"

export PATH="$task_root/environment/bin:$PATH"
export GWS_FIXTURES_DIR="$task_root/environment/fixtures"
export GWS_MOCK_LOG="$workspace_dir/.gws-mock-log.jsonl"

opkg install "$repo_root" --cwd "$workspace_dir" --platforms claude --force
bash "$repo_root/skills/gws-gtd/scripts/install_gws_skills.sh" --workspace "$workspace_dir"

printf 'workspace_dir=%s\n' "$workspace_dir"
printf 'repo_root=%s\n' "$repo_root"
