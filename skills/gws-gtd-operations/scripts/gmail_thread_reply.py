#!/usr/bin/env python3

import argparse
import base64
import json
import subprocess
import sys
from email.message import EmailMessage
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build or send a Gmail reply that stays on an existing thread.",
    )
    parser.add_argument("--thread-id", required=True, help="Existing Gmail thread id")
    parser.add_argument("--to", required=True, help="Recipient email address")
    parser.add_argument("--subject", required=True, help="Reply subject")
    body = parser.add_mutually_exclusive_group(required=True)
    body.add_argument("--body", help="Plain-text body")
    body.add_argument("--body-file", help="Path to plain-text body file")
    parser.add_argument(
        "--quote",
        help="Optional plain-text content to append as a quoted block",
    )
    parser.add_argument(
        "--quote-file",
        help="Path to plain-text content to append as a quoted block",
    )
    parser.add_argument(
        "--quote-header",
        help="Optional header line placed before the quoted block",
    )
    parser.add_argument("--in-reply-to", required=True, help="Message-ID being replied to")
    parser.add_argument(
        "--references",
        action="append",
        default=[],
        help="Reference Message-ID header value; repeat to add multiple values",
    )
    parser.add_argument(
        "--send",
        action="store_true",
        help="Send via gws instead of printing the Gmail API payload",
    )
    return parser.parse_args()


def build_body(args: argparse.Namespace) -> str:
    if args.body is not None:
        body = args.body
    else:
        body = Path(args.body_file).read_text(encoding="utf-8")

    quote = None
    if args.quote is not None:
        quote = args.quote
    elif args.quote_file is not None:
        quote = Path(args.quote_file).read_text(encoding="utf-8")

    if quote is None:
        return body

    quoted_lines = "\n".join(f"> {line}" if line else ">" for line in quote.splitlines())
    parts = [body.rstrip()]
    if args.quote_header:
        parts.append(args.quote_header.rstrip())
    parts.append(quoted_lines)
    return "\n\n".join(part for part in parts if part)


def build_payload(args: argparse.Namespace) -> dict:
    msg = EmailMessage()
    msg["To"] = args.to
    msg["Subject"] = args.subject
    msg["In-Reply-To"] = args.in_reply_to

    refs = list(args.references)
    if args.in_reply_to not in refs:
        refs.append(args.in_reply_to)
    msg["References"] = " ".join(refs)
    msg.set_content(build_body(args))

    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode("ascii")
    return {"threadId": args.thread_id, "raw": raw}


def main() -> int:
    args = parse_args()
    payload = build_payload(args)

    if not args.send:
        json.dump(payload, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
        return 0

    proc = subprocess.run(
        [
            "gws",
            "gmail",
            "users",
            "messages",
            "send",
            "--params",
            '{"userId":"me"}',
            "--json",
            json.dumps(payload, ensure_ascii=False),
        ],
        check=False,
    )
    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
