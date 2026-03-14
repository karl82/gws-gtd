#!/usr/bin/env python3

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[4]
CALENDAR_SUMMARY = "GTD Signals"
MANAGED_BY = "gtd-signals-sync"
INCLUDE_PREFIXES = ("Projects/", "Areas/", "Journal/")
EXCLUDE_EXACT = {"Inbox.md"}
INBOX_TAG = "#inbox"
NEXT_TAG = "#next"
WAITING_TAG = "#waiting"
CALENDAR_SOURCE_TOKEN = "source:: calendar"
CALENDAR_EVENT_TOKEN = "event_id::"
TAG_PATTERN_CACHE: dict[str, re.Pattern[str]] = {}

TASK_LINE_RE = re.compile(r"^\s*-\s\[(?P<status>.)\]\s(?P<text>.+?)\s*$")
START_DATE_RE = re.compile(r"🛫\s*(\d{4}-\d{2}-\d{2})")
DUE_DATE_RE = re.compile(r"📅\s*(\d{4}-\d{2}-\d{2})")
TASK_ID_RE = re.compile(r"(?:\(|\[)task_id::\s*([^\])]+)")
INLINE_METADATA_RE = re.compile(r"\s*(?:\[[^\]]+::[^\]]*\]|\([^()]*::[^()]*\))")
DATE_TOKEN_RE = re.compile(r"\s*[➕🛫📅✅]\s*\d{4}-\d{2}-\d{2}")
SPACE_RE = re.compile(r"\s{2,}")
MARKDOWN_LINK_RE = re.compile(r"\[([^\]]+)\]\([^)]+\)")
WIKI_LINK_RE = re.compile(r"\[\[([^\]]+)\]\]")
URL_RE = re.compile(r"<?https?://[^>\s]+>?")
PHONE_RE = re.compile(r"(?:\+?\d[\d().\-\s]{6,}\d)")
REFERENCE_RE = re.compile(r"\b(?:order|invoice|ticket|ref(?:erence)?)\s*[:#-]?\s*([A-Za-z0-9][A-Za-z0-9\-_/]{2,})", re.IGNORECASE)
DONE_MARKER_RE = re.compile(r"^✅(?:\s+|)")

DROP_TAGS = {
    "admin",
    "blocked",
    "deep",
    "email",
    "home",
    "idea",
    "inbox",
    "next",
    "payment",
    "personal",
    "phone",
    "someday",
    "task",
    "waiting",
    "work",
}

COLOR_BY_SIGNAL = {
    "next": "10",
    "follow_up": "5",
}


@dataclass(frozen=True)
class Signal:
    signal_key: str
    vault_task_key: str
    signal_type: str
    title: str
    task_title: str
    task_path: str
    start_date: str
    end_date: str
    color_id: str


@dataclass(frozen=True)
class TaskRecord:
    path: str
    task_text: str
    task_title: str
    vault_task_key: str
    status: str
    line_number: int


def has_tag(task_text: str, tag: str) -> bool:
    pattern = TAG_PATTERN_CACHE.get(tag)
    if pattern is None:
        pattern = re.compile(rf"(^|\s){re.escape(tag)}(?=\s|$)")
        TAG_PATTERN_CACHE[tag] = pattern
    return pattern.search(task_text) is not None


def run_gws(args: list[str], *, params: dict[str, Any] | None = None, body: dict[str, Any] | None = None) -> Any:
    command = ["gws", *args]
    if params is not None:
        command.extend(["--params", json.dumps(params)])
    if body is not None:
        command.extend(["--json", json.dumps(body)])
    command.extend(["--format", "json"])

    result = subprocess.run(command, cwd=REPO_ROOT, check=True, capture_output=True, text=True)
    stdout = result.stdout.strip()
    if not stdout:
        return None
    return json.loads(stdout)


def normalize_title(task_text: str) -> str:
    def replace_wiki_link(match: re.Match[str]) -> str:
        body = match.group(1)
        if "|" in body:
            return body.split("|", 1)[1]
        return body.split("/")[-1]

    def replace_tag(match: re.Match[str]) -> str:
        prefix = match.group(1)
        tag = match.group(0).strip()[1:]
        if tag.lower() in DROP_TAGS:
            return prefix
        return f"{prefix}{tag}"

    text = INLINE_METADATA_RE.sub(" ", task_text)
    text = MARKDOWN_LINK_RE.sub(r"\1", text)
    text = WIKI_LINK_RE.sub(replace_wiki_link, text)
    text = URL_RE.sub(" ", text)
    text = DATE_TOKEN_RE.sub(" ", text)
    text = text.replace("#task", " ")
    text = re.sub(r"(^|\s)#\S+", replace_tag, text)
    text = SPACE_RE.sub(" ", text).strip()
    return text


def derive_task_key(path: str, task_text: str, task_title: str) -> str:
    explicit_id = TASK_ID_RE.search(task_text)
    if explicit_id:
        return explicit_id.group(1).strip()
    digest = hashlib.sha1(f"{path}|{task_title}".encode("utf-8")).hexdigest()
    return digest[:16]


def iter_task_records(include_completed: bool = False) -> list[TaskRecord]:
    tasks: list[TaskRecord] = []
    for note in sorted(REPO_ROOT.rglob("*.md")):
        relative = note.relative_to(REPO_ROOT).as_posix()
        if relative in EXCLUDE_EXACT:
            continue
        if not relative.startswith(INCLUDE_PREFIXES):
            continue
        content = note.read_text(encoding="utf-8")
        for line_number, line in enumerate(content.splitlines(), start=1):
            match = TASK_LINE_RE.match(line)
            if not match:
                continue
            status = match.group("status")
            if status != " " and not (include_completed and status.lower() == "x"):
                continue
            task_text = match.group("text").strip()
            if not has_tag(task_text, "#task"):
                continue
            if status == " " and has_tag(task_text, INBOX_TAG):
                continue
            task_title = normalize_title(task_text)
            if not task_title:
                continue
            tasks.append(
                TaskRecord(
                    path=relative,
                    task_text=task_text,
                    task_title=task_title,
                    vault_task_key=derive_task_key(relative, task_text, task_title),
                    status=status,
                    line_number=line_number,
                )
            )
    return tasks


def extract_mobile_details(task_text: str) -> list[str]:
    details: list[str] = []
    seen: set[str] = set()

    for pattern in (URL_RE, PHONE_RE):
        for match in pattern.finditer(task_text):
            value = match.group(0).strip("<>")
            if value and value not in seen:
                seen.add(value)
                details.append(value)

    for match in REFERENCE_RE.finditer(task_text):
        value = match.group(1).strip()
        label = f"ref: {value}"
        if value and label not in seen:
            seen.add(label)
            details.append(label)

    return details


def build_event_description(signal: Signal, task_text: str) -> str:
    lines = [f"Task: {signal.task_title}", f"Source: {signal.task_path}"]
    details = extract_mobile_details(task_text)
    if details:
        lines.append("")
        lines.append("Details:")
        lines.extend(f"- {detail}" for detail in details)
    return "\n".join(lines)


def mark_task_complete(vault_task_key: str, apply: bool) -> tuple[str, str]:
    matches = [record for record in iter_task_records(include_completed=True) if record.vault_task_key == vault_task_key]
    if not matches:
        return ("missing", "")
    if len(matches) > 1:
        paths = ", ".join(f"{record.path}:{record.line_number}" for record in matches)
        return ("ambiguous", paths)

    record = matches[0]
    location = f"{record.path}:{record.line_number}"
    if record.status.lower() == "x":
        return ("already_completed", location)

    if not apply:
        return ("completed", location)

    note_path = REPO_ROOT / record.path
    lines = note_path.read_text(encoding="utf-8").splitlines(keepends=True)
    index = record.line_number - 1
    if index >= len(lines):
        return ("missing", location)

    line = lines[index]
    marker = "- [ ]"
    marker_index = line.find(marker)
    if marker_index == -1:
        return ("missing", location)
    lines[index] = f"{line[:marker_index]}- [x]{line[marker_index + len(marker):]}"
    note_path.write_text("".join(lines), encoding="utf-8")
    return ("completed", location)


def build_signals() -> dict[str, Signal]:
    signals: dict[str, Signal] = {}
    today = datetime.now().date().isoformat()
    for record in iter_task_records():
        path = record.path
        task_text = record.task_text
        task_title = record.task_title

        start_match = START_DATE_RE.search(task_text)
        due_match = DUE_DATE_RE.search(task_text)
        start_date = start_match.group(1) if start_match else None
        due_date = due_match.group(1) if due_match else None
        is_waiting = has_tag(task_text, WAITING_TAG)
        is_next = has_tag(task_text, NEXT_TAG)
        is_calendar_backed = CALENDAR_SOURCE_TOKEN in task_text or CALENDAR_EVENT_TOKEN in task_text
        vault_task_key = record.vault_task_key

        if is_calendar_backed:
            continue

        def add_signal(signal_type: str, start: str, end: str, prefix: str) -> None:
            signal_key = f"{vault_task_key}:{signal_type}"
            signals[signal_key] = Signal(
                signal_key=signal_key,
                vault_task_key=vault_task_key,
                signal_type=signal_type,
                title=f"{prefix}: {task_title}",
                task_title=task_title,
                task_path=path,
                start_date=start,
                end_date=end,
                color_id=COLOR_BY_SIGNAL[signal_type],
            )

        if is_waiting:
            if due_date:
                add_signal("follow_up", due_date, due_date, "FOLLOW UP")
            continue

        if not is_next:
            continue

        signal_start = start_date or due_date or today
        signal_end = due_date or start_date or today
        if signal_start > signal_end:
            signal_start, signal_end = signal_end, signal_start
        add_signal("next", signal_start, signal_end, "NEXT")

    return signals


def ensure_calendar(apply: bool) -> dict[str, Any]:
    calendar_list = run_gws(["calendar", "calendarList", "list"])
    for item in calendar_list.get("items", []):
        if item.get("summary") == CALENDAR_SUMMARY:
            return item

    primary = next((item for item in calendar_list.get("items", []) if item.get("primary")), None)
    body = {
        "summary": CALENDAR_SUMMARY,
        "description": "Dedicated all-day task signal calendar mirrored from GTD tasks",
        "timeZone": primary.get("timeZone", "UTC") if primary else "UTC",
    }
    if not apply:
        return {"summary": CALENDAR_SUMMARY, "timeZone": body["timeZone"], "_dry_run_create": True}
    return run_gws(["calendar", "calendars", "insert"], body=body)


def load_managed_events(calendar_id: str) -> dict[str, dict[str, Any]]:
    response = run_gws(
        ["calendar", "events", "list"],
        params={
            "calendarId": calendar_id,
            "singleEvents": True,
            "showDeleted": False,
            "maxResults": 2500,
        },
    )
    events_by_key: dict[str, dict[str, Any]] = {}
    for item in response.get("items", []):
        private = (((item.get("extendedProperties") or {}).get("private")) or {})
        signal_type = private.get("signal_type")
        if not signal_type:
            continue
        if private.get("managed_by") == MANAGED_BY:
            key = f"{private.get('vault_task_key')}:{signal_type}"
            events_by_key[key] = item
            continue

        legacy_path = private.get("task_path")
        legacy_title = private.get("task_line")
        if legacy_path and legacy_title:
            legacy_task_key = hashlib.sha1(f"{legacy_path}|{legacy_title}".encode("utf-8")).hexdigest()[:16]
            key = f"{legacy_task_key}:{signal_type}"
            events_by_key[key] = item
    return events_by_key


def event_body(signal: Signal) -> dict[str, Any]:
    exclusive_end = (date.fromisoformat(signal.end_date) + timedelta(days=1)).isoformat()
    task_record = next((record for record in iter_task_records() if record.vault_task_key == signal.vault_task_key), None)
    description = f"Source: {signal.task_path}"
    if task_record is not None:
        description = build_event_description(signal, task_record.task_text)
    return {
        "summary": signal.title,
        "description": description,
        "start": {"date": signal.start_date},
        "end": {"date": exclusive_end},
        "transparency": "transparent",
        "visibility": "private",
        "colorId": signal.color_id,
        "extendedProperties": {
            "private": {
                "managed_by": MANAGED_BY,
                "vault_task_key": signal.vault_task_key,
                "signal_type": signal.signal_type,
                "task_path": signal.task_path,
                "task_line": signal.task_title,
                "start_date": signal.start_date,
                "end_date": signal.end_date,
            }
        },
    }


def event_matches(signal: Signal, event: dict[str, Any]) -> bool:
    private = (((event.get("extendedProperties") or {}).get("private")) or {})
    summary = event.get("summary") or ""
    if DONE_MARKER_RE.match(summary):
        return True
    task_record = next((record for record in iter_task_records() if record.vault_task_key == signal.vault_task_key), None)
    expected_description = f"Source: {signal.task_path}"
    if task_record is not None:
        expected_description = build_event_description(signal, task_record.task_text)
    return (
        summary == signal.title
        and event.get("description") == expected_description
        and (event.get("start") or {}).get("date") == signal.start_date
        and (event.get("end") or {}).get("date") == (date.fromisoformat(signal.end_date) + timedelta(days=1)).isoformat()
        and event.get("colorId") == signal.color_id
        and event.get("transparency") == "transparent"
        and event.get("visibility") == "private"
        and private.get("managed_by") == MANAGED_BY
        and private.get("vault_task_key") == signal.vault_task_key
        and private.get("signal_type") == signal.signal_type
        and private.get("task_path") == signal.task_path
        and private.get("task_line") == signal.task_title
        and private.get("start_date") == signal.start_date
        and private.get("end_date") == signal.end_date
    )


def signal_date_label(signal: Signal) -> str:
    if signal.start_date == signal.end_date:
        return signal.start_date
    return f"{signal.start_date} -> {signal.end_date}"


def sync_signals(apply: bool) -> int:
    calendar = ensure_calendar(apply)
    calendar_id = calendar.get("id")

    if not calendar_id:
        desired = build_signals()
        print(f"Would create calendar: {CALENDAR_SUMMARY}")
        print(f"Desired signals: {len(desired)}")
        return 0

    existing = load_managed_events(calendar_id)
    completions: list[dict[str, Any]] = []
    active_existing: dict[str, dict[str, Any]] = {}
    for signal_key, event in existing.items():
        summary = event.get("summary") or ""
        if DONE_MARKER_RE.match(summary):
            completions.append(event)
            continue
        active_existing[signal_key] = event

    completed_deletes: list[dict[str, Any]] = []
    completed_task_keys: set[str] = set()
    for event in completions:
        private = (((event.get("extendedProperties") or {}).get("private")) or {})
        vault_task_key = private.get("vault_task_key", "")
        status, detail = mark_task_complete(vault_task_key, apply)
        summary = event.get("summary") or "(untitled)"
        if not apply:
            if status == "completed":
                print(f"COMPLETE {summary} -> {detail}")
                completed_deletes.append(event)
                completed_task_keys.add(vault_task_key)
            elif status == "already_completed":
                print(f"ALREADY COMPLETE {summary} -> {detail}")
                completed_deletes.append(event)
                completed_task_keys.add(vault_task_key)
            elif status == "ambiguous":
                print(f"WARN ambiguous completed event {summary} -> {detail}")
            else:
                print(f"WARN missing vault task for completed event {summary}")
        else:
            if status in {"completed", "already_completed"}:
                completed_deletes.append(event)
                completed_task_keys.add(vault_task_key)
                if status == "completed":
                    print(f"Completed {detail}")
                else:
                    print(f"Already completed {detail}")
            elif status == "ambiguous":
                print(f"Warn: ambiguous completed event {summary} -> {detail}")
            else:
                print(f"Warn: missing vault task for completed event {summary}")

    desired = build_signals()
    if completed_task_keys:
        desired = {
            signal_key: signal
            for signal_key, signal in desired.items()
            if signal.vault_task_key not in completed_task_keys
        }

    creates: list[Signal] = []
    updates: list[tuple[Signal, dict[str, Any]]] = []
    deletes: list[dict[str, Any]] = []

    for signal_key, signal in desired.items():
        current = active_existing.get(signal_key)
        if current is None:
            creates.append(signal)
        elif not event_matches(signal, current):
            updates.append((signal, current))

    for signal_key, event in active_existing.items():
        if signal_key not in desired:
            deletes.append(event)

    deletes.extend(completed_deletes)

    if not apply:
        for signal in creates:
            print(f"CREATE {signal.title} [{signal_date_label(signal)}] ({signal.task_path})")
        for signal, event in updates:
            current_start = (event.get("start") or {}).get("date")
            current_end_raw = (event.get("end") or {}).get("date")
            current_end = None
            if current_end_raw:
                current_end = (date.fromisoformat(current_end_raw) - timedelta(days=1)).isoformat()
            current_label = current_start if not current_end or current_start == current_end else f"{current_start} -> {current_end}"
            print(f"UPDATE {event.get('summary')} [{current_label}] -> {signal.title} [{signal_date_label(signal)}]")
        for event in deletes:
            current_start = (event.get("start") or {}).get("date")
            current_end_raw = (event.get("end") or {}).get("date")
            current_end = None
            if current_end_raw:
                current_end = (date.fromisoformat(current_end_raw) - timedelta(days=1)).isoformat()
            current_label = current_start if not current_end or current_start == current_end else f"{current_start} -> {current_end}"
            print(f"DELETE {event.get('summary')} [{current_label}]")
        if not creates and not updates and not deletes and not completions:
            print("No changes.")
        return 0

    for signal in creates:
        run_gws(
            ["calendar", "events", "insert"],
            params={"calendarId": calendar_id, "sendUpdates": "none"},
            body=event_body(signal),
        )
        print(f"Created {signal.title} [{signal_date_label(signal)}]")

    for signal, event in updates:
        run_gws(
            ["calendar", "events", "patch"],
            params={"calendarId": calendar_id, "eventId": event["id"], "sendUpdates": "none"},
            body=event_body(signal),
        )
        print(f"Updated {signal.title} [{signal_date_label(signal)}]")

    for event in deletes:
        run_gws(
            ["calendar", "events", "delete"],
            params={"calendarId": calendar_id, "eventId": event["id"], "sendUpdates": "none"},
        )
        print(f"Deleted {event.get('summary')}")

    if not creates and not updates and not deletes and not completions:
        print("No changes.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync clarified dated GTD tasks into the GTD Signals calendar.")
    parser.add_argument("--apply", action="store_true", help="Apply changes. Without this flag, the script performs a dry run.")
    args = parser.parse_args()

    try:
        return sync_signals(apply=args.apply)
    except subprocess.CalledProcessError as exc:
        stderr = exc.stderr.strip() if exc.stderr else str(exc)
        print(stderr, file=sys.stderr)
        return exc.returncode or 1


if __name__ == "__main__":
    raise SystemExit(main())
