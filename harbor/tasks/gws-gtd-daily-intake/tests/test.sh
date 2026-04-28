#!/usr/bin/env bash

set -euo pipefail

workspace_dir="${1:-${WORKSPACE_DIR:-/tmp/gws-gtd-daily-intake-workspace}}"
script_dir="$(cd "$(dirname "$0")" && pwd)"

python3 "$script_dir/assert_daily_intake.py" "$workspace_dir"
