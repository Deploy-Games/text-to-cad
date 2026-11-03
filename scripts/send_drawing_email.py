#!/usr/bin/env python3
"""
CLI helper to email engineering drawing PDFs to contacts or aliases.
Usage:
    python3 scripts/send_drawing_email.py <recipient_alias_or_email> <pdf_path> [subject] [message]

Examples:
    python3 scripts/send_drawing_email.py serverOwner drawings/bracket_drawing.pdf
    python3 scripts/send_drawing_email.py roland drawings/bracket_drawing.pdf "Updated Bracket Drawing" "Here is the drawing per our discussion."
"""

import sys
from pathlib import Path

# Add homeserver root to sys.path so we can import email_client
HOMESERVER_ROOT = Path("/home/tom/homeserver")
if str(HOMESERVER_ROOT) not in sys.path:
    sys.path.insert(0, str(HOMESERVER_ROOT))

try:
    from scripts.email_client import send_email
except ImportError as err:
    print(f"Error importing email_client: {err}", file=sys.stderr)
    sys.exit(1)


def main():
    if len(sys.argv) < 3 or sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0)

    recipient = sys.argv[1]
    pdf_path = Path(sys.argv[2]).resolve()

    if not pdf_path.exists():
        print(f"Error: File not found at {pdf_path}", file=sys.stderr)
        sys.exit(1)

    part_name = pdf_path.stem.replace("_drawing", "").replace("_", " ").title()
    subject = sys.argv[3] if len(sys.argv) > 3 else f"Engineering Drawing: {part_name}"
    body = sys.argv[4] if len(sys.argv) > 4 else f"Attached is the professional engineering drawing for {part_name}."

    print(f"Sending email to '{recipient}' with attachment: {pdf_path.name}...")
    send_email(
        to_aliases=[recipient],
        subject=subject,
        body=body,
        attachment_path=str(pdf_path),
        logSummary=f"Sent {pdf_path.name} to {recipient}",
    )
    print("Email sent successfully!")


if __name__ == "__main__":
    main()
