#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DOC_ID_RE = re.compile(r"/document/d/([a-zA-Z0-9_-]+)")
DATA_URI_RE = re.compile(r"^(\[[^\]]+\]:)\s*<data:[^>]+>$")
TABLE_ROW_RE = re.compile(r"^\*\*(.+\|.+)\*\*\s*$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Export a Google Doc to one Markdown file with provenance metadata.",
    )
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--doc-id", help="Google Doc file ID")
    source.add_argument("--doc-url", help="Google Doc URL")
    parser.add_argument("--output", required=True, help="Output .md path or directory")
    parser.add_argument("--force", action="store_true", help="Overwrite existing output file")
    parser.add_argument("--stdout-manifest", action="store_true", help="Print export manifest JSON")
    return parser.parse_args()


def extract_doc_id(args: argparse.Namespace) -> str:
    if args.doc_id:
        return args.doc_id
    match = DOC_ID_RE.search(args.doc_url)
    if not match:
        raise SystemExit("Could not extract a Google Doc ID from --doc-url")
    return match.group(1)


def run_gws_json(command: list[str], *, params: dict[str, Any] | None = None) -> Any:
    full_command = ["gws", *command]
    if params is not None:
        full_command.extend(["--params", json.dumps(params, ensure_ascii=True)])
    full_command.extend(["--format", "json"])
    proc = subprocess.run(full_command, capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        sys.stderr.write(proc.stderr)
        raise SystemExit(proc.returncode)
    stdout = proc.stdout.strip()
    return json.loads(stdout) if stdout else None


def export_markdown_via_drive(doc_id: str) -> str:
    with tempfile.TemporaryDirectory() as tempdir:
        proc = subprocess.run(
            [
                "gws",
                "drive",
                "files",
                "export",
                "--params",
                json.dumps({"fileId": doc_id, "mimeType": "text/markdown"}, ensure_ascii=True),
            ],
            cwd=tempdir,
            capture_output=True,
            text=True,
            check=False,
        )
        if proc.returncode != 0:
            sys.stderr.write(proc.stderr)
            raise SystemExit(proc.returncode)
        output_file = Path(tempdir) / "download.bin"
        if not output_file.exists():
            raise SystemExit("Drive export did not produce download.bin")
        return output_file.read_text(encoding="utf-8")


def convert_bold_pipe_rows_to_tables(lines: list[str]) -> list[str]:
    converted: list[str] = []
    i = 0
    while i < len(lines):
        match = TABLE_ROW_RE.match(lines[i].strip())
        if not match:
            converted.append(lines[i])
            i += 1
            continue

        run: list[str] = []
        while i < len(lines):
            current = TABLE_ROW_RE.match(lines[i].strip())
            if not current:
                break
            run.append(current.group(1).strip())
            i += 1

        if len(run) < 2:
            converted.extend(f"**{row}**" for row in run)
            continue

        rows = [[cell.strip() for cell in row.split("|")] for row in run]
        width = max(len(row) for row in rows)
        rows = [row + [""] * (width - len(row)) for row in rows]
        converted.append("| " + " | ".join(rows[0]) + " |")
        converted.append("| " + " | ".join(["---"] * width) + " |")
        for row in rows[1:]:
            converted.append("| " + " | ".join(row) + " |")
    return converted


def postprocess_markdown(text: str) -> str:
    lines = convert_bold_pipe_rows_to_tables(text.splitlines())
    cleaned: list[str] = []
    for line in lines:
        match = DATA_URI_RE.match(line.strip())
        if match:
            cleaned.append(f"{match.group(1)} <embedded-image-omitted>")
        else:
            cleaned.append(line)
    return "\n".join(cleaned).rstrip() + "\n"


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def resolve_output_path(output: Path) -> Path:
    output = output.expanduser()
    if output.suffix.lower() == ".md":
        return output
    return output / "main.md"


def escape_frontmatter_value(value: str) -> str:
    return value.replace('"', '\\"')


def compose_frontmatter(metadata: dict[str, str]) -> str:
    lines = ["---"]
    for key, value in metadata.items():
        lines.append(f'{key}: "{escape_frontmatter_value(value)}"')
    lines.append("---")
    return "\n".join(lines) + "\n\n"


def main() -> int:
    args = parse_args()
    doc_id = extract_doc_id(args)
    drive_meta = run_gws_json(
        ["drive", "files", "get"],
        params={"fileId": doc_id, "fields": "id,name,modifiedTime,webViewLink,mimeType"},
    )
    doc_meta = run_gws_json(["docs", "documents", "get"], params={"documentId": doc_id})
    output_path = resolve_output_path(Path(args.output))
    if output_path.exists() and not args.force:
        raise SystemExit(f"Refusing to overwrite existing file without --force: {output_path}")

    markdown = postprocess_markdown(export_markdown_via_drive(doc_id))
    exported_at = now_iso()
    gdoc_url = drive_meta.get("webViewLink") or args.doc_url or f"https://docs.google.com/document/d/{doc_id}/edit"
    title = drive_meta.get("name") or doc_meta.get("title") or "Untitled Document"
    revision_id = doc_meta.get("revisionId", "")

    frontmatter = compose_frontmatter(
        {
            "gdoc_id": doc_id,
            "gdoc_url": gdoc_url,
            "gdoc_source_of_truth": "google-docs",
            "gdoc_title": title,
            "gdoc_revision_id": revision_id,
            "gdoc_last_exported_at": exported_at,
        }
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(frontmatter + markdown, encoding="utf-8")

    if args.stdout_manifest:
        json.dump(
            {
                "gdoc_id": doc_id,
                "gdoc_url": gdoc_url,
                "gdoc_title": title,
                "gdoc_revision_id": revision_id,
                "gdoc_last_exported_at": exported_at,
                "output": str(output_path),
            },
            sys.stdout,
            ensure_ascii=True,
            indent=2,
        )
        sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
