#!/usr/bin/env bash
# Re-authenticate the gws CLI for the gws-gtd skill.
# Requests the OAuth scopes listed in skills/gtd/README.md (required + optional).
# Opens a browser for the OAuth2 flow, then verifies the new token with `gws auth status`.

set -euo pipefail

GWS="${GWS:-/opt/homebrew/bin/gws}"

SCOPES="https://www.googleapis.com/auth/gmail.modify,\
https://www.googleapis.com/auth/calendar.readonly,\
https://www.googleapis.com/auth/contacts.readonly,\
https://www.googleapis.com/auth/calendar.events,\
https://www.googleapis.com/auth/gmail.send,\
https://www.googleapis.com/auth/gmail.settings.basic,\
https://www.googleapis.com/auth/contacts"

echo "=========================================="
echo " gws-gtd auth refresh"
echo "=========================================="
echo "Re-authenticating the gws CLI for the GTD skill."
echo "A browser window will open for the Google OAuth2 flow."
echo
echo "Scopes requested:"
echo "$SCOPES" | tr ',' '\n' | sed 's/^/  - /'
echo

"$GWS" auth login --scopes "$SCOPES"

echo
echo "=========================================="
echo " Verifying new credentials"
echo "=========================================="

STATUS_JSON="$("$GWS" auth status 2>/dev/null || true)"

if command -v jq >/dev/null 2>&1; then
    TOKEN_VALID="$(echo "$STATUS_JSON" | jq -r '.token_valid // false')"
    HAS_REFRESH="$(echo "$STATUS_JSON" | jq -r '.has_refresh_token // false')"
    AUTH_METHOD="$(echo "$STATUS_JSON" | jq -r '.auth_method // "unknown"')"
    PROJECT_ID="$(echo "$STATUS_JSON" | jq -r '.project_id // "unknown"')"

    echo "auth_method:       $AUTH_METHOD"
    echo "project_id:        $PROJECT_ID"
    echo "token_valid:       $TOKEN_VALID"
    echo "has_refresh_token: $HAS_REFRESH"
    echo

    if [ "$TOKEN_VALID" = "true" ]; then
        echo "✓ gws auth refresh succeeded."
        exit 0
    else
        echo "✗ Token is not valid. Full status:"
        echo "$STATUS_JSON"
        exit 1
    fi
else
    echo "(jq not installed — printing raw status)"
    echo "$STATUS_JSON"
fi
