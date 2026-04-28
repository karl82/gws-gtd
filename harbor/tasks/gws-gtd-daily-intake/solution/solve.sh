#!/usr/bin/env bash

set -euo pipefail

workspace_dir="${1:-${WORKSPACE_DIR:-/tmp/gws-gtd-daily-intake-workspace}}"

export PATH="$(cd "$(dirname "$0")/.." && pwd)/environment/bin:$PATH"
export GWS_FIXTURES_DIR="$(cd "$(dirname "$0")/.." && pwd)/environment/fixtures"
export GWS_MOCK_LOG="$workspace_dir/.gws-mock-log.jsonl"

gws gmail users labels list >/dev/null
gws gmail +triage --query "label:gtd/import -label:gtd/imported" --format json >/dev/null
gws gmail +triage --query "label:gtd/waiting" --format json >/dev/null
gws calendar +agenda --days 2 --format json >/dev/null

cat >"$workspace_dir/Inbox.md" <<'EOF'
# Inbox

- [ ] #task Send Alpha draft to Alice #email #inbox (source:: gmail) (gmail_thread_id:: thread-action-1) (subject:: Need draft for Friday review) (web_link:: https://mail.google.com/mail/u/0/#inbox/thread-action-1)
- [ ] #task Follow up on revised contract from vendor #email #inbox #waiting (source:: gmail) (gmail_thread_id:: thread-waiting-1) (subject:: We will send the revised contract next week) (web_link:: https://mail.google.com/mail/u/0/#inbox/thread-waiting-1)
- [ ] #task buy shoe polish #inbox
- [ ] #task Follow up with plumber about sink repair #inbox [[Areas/Personal]]
EOF

cat >"$workspace_dir/Journal/2026-04-04.md" <<'EOF'
# 2026-04-04

- Reviewed [[Projects/Alpha]] during Alpha design review and confirmed the Friday draft still needs to be sent.
EOF
