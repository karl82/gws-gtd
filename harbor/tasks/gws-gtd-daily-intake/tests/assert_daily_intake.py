#!/usr/bin/env python3

from __future__ import annotations

import json
import pathlib
import sys


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read_text(path: pathlib.Path) -> str:
    return path.read_text(encoding="utf-8")


def main() -> int:
    workspace = pathlib.Path(sys.argv[1]).resolve()
    inbox = read_text(workspace / "Inbox.md")
    journal = read_text(workspace / "Journal" / "2026-04-04.md")
    mock_log = workspace / ".gws-mock-log.jsonl"

    require("- [ ] #task Send Alpha draft to Alice #email #inbox (source:: gmail) (gmail_thread_id:: thread-action-1) (subject:: Need draft for Friday review) (web_link:: https://mail.google.com/mail/u/0/#inbox/thread-action-1)" in inbox, "missing imported actionable task")
    require("- [ ] #task Follow up on revised contract from vendor #email #inbox #waiting (source:: gmail) (gmail_thread_id:: thread-waiting-1) (subject:: We will send the revised contract next week) (web_link:: https://mail.google.com/mail/u/0/#inbox/thread-waiting-1)" in inbox, "missing waiting task")
    require("- [ ] #task buy shoe polish #inbox" in inbox, "missing self-capture task")
    require("thread-capture-1" not in inbox, "self-capture task should stay minimal")
    require("20% off office chairs" not in inbox, "garbage email should not be imported")
    require("[[Projects/Alpha]]" in journal, "journal should link back to Alpha project")
    require("Alpha design review" in journal, "journal should capture event context")
    require("follow up with plumber" in inbox.lower(), "calendar follow-up task missing")

    require(mock_log.exists(), "mock gws log missing")
    entries = [json.loads(line) for line in mock_log.read_text(encoding="utf-8").splitlines() if line.strip()]
    argv_sequences = [entry["argv"] for entry in entries]
    require(any(argv[:4] == ["gmail", "users", "labels", "list"] for argv in argv_sequences), "expected labels list call")
    require(any(argv[:2] == ["gmail", "+triage"] for argv in argv_sequences), "expected gmail triage call")
    require(any(argv[:2] == ["calendar", "+agenda"] for argv in argv_sequences), "expected calendar agenda call")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
