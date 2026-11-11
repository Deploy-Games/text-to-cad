#!/usr/bin/env python3
"""
CLI helper to email 3D CAD models (STEP/STL/GLB/FeatureScript) and engineering drawings to contacts or aliases.

Usage:
    python3 scripts/send_cad_model_email.py <recipient_alias> <attachment_path1> [attachment_path2 ...]
    python3 scripts/send_cad_model_email.py --to <recipient_alias> --subject <subject> --body <body> <attachments...>
"""

import argparse
import os
import smtplib
import sys
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

HOMESERVER_ROOT = Path("/home/tom/homeserver")
if str(HOMESERVER_ROOT) not in sys.path:
    sys.path.insert(0, str(HOMESERVER_ROOT))

try:
    from scripts.email_client import (
        _GMX_ADDRESS,
        _SMTP_HOST,
        _SMTP_PORT,
        _load_password,
        _log_sent_email,
        _resolve_aliases,
    )
except ImportError as err:
    print(f"Error importing email_client: {err}", file=sys.stderr)
    sys.exit(1)


def send_cad_email(
    to_aliases: list[str],
    subject: str,
    body: str,
    attachment_paths: list[str | Path],
    log_summary: str = "3D CAD model delivery",
):
    recipients = _resolve_aliases(to_aliases)
    password = _load_password()

    msg = MIMEMultipart()
    msg["From"] = _GMX_ADDRESS
    msg["To"] = ", ".join(recipients)
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain", "utf-8"))

    attached_names = []
    for att in attachment_paths:
        p = Path(att).resolve()
        if not p.exists():
            raise FileNotFoundError(f"Attachment not found: {p}")
        with open(p, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f'attachment; filename="{p.name}"')
        msg.attach(part)
        attached_names.append(str(p))

    with smtplib.SMTP(_SMTP_HOST, _SMTP_PORT) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login(_GMX_ADDRESS, password)
        smtp.sendmail(_GMX_ADDRESS, recipients, msg.as_string())

    _log_sent_email(
        to_aliases=to_aliases,
        recipients=recipients,
        subject=subject,
        log_summary=log_summary,
        attachment_path=", ".join(attached_names),
    )
    print(f"[send_cad_email] Sent '{subject}' to {recipients} with attachments: {[Path(a).name for a in attached_names]}")


def main():
    parser = argparse.ArgumentParser(description="Send CAD models and drawings via email.")
    parser.add_argument("recipient", help="Recipient alias (e.g. roland, serverOwner)")
    parser.add_argument("attachments", nargs="+", help="Paths to attachments")
    parser.add_argument("--subject", default=None, help="Optional email subject")
    parser.add_argument("--body", default=None, help="Optional email body")

    args = parser.parse_args()

    attachments = [Path(p).resolve() for p in args.attachments]

    subject = args.subject or "3D CAD Model & Onshape Feature Tree: Desk Storage Frame"
    body = args.body or (
        "Hi,\n\n"
        "Here are the CAD model files and Onshape Feature Tree files for the partitioned desk storage frame "
        "(1600 x 800 x 300 mm, 6 partitioned bays):\n\n"
        "Attached Files:\n"
        "1. desk_storage_frame.fs (Onshape FeatureScript - creates a fully parametric feature in Onshape's Feature Tree)\n"
        "2. desk_storage_frame.step (Standard 3D STEP solid for universal CAD import)\n"
        "3. desk_storage_frame_drawing.pdf (Dimensioned ISO engineering drawing)\n\n"
        "How to use FeatureScript in Onshape:\n"
        "1. In your Onshape document, click the '+' icon at the bottom-left and select 'Create Feature Studio'.\n"
        "2. Paste the contents of 'desk_storage_frame.fs' into the Feature Studio and click 'Commit'.\n"
        "3. Switch back to your Part Studio. A new 'Desk Storage Frame' button will appear in the toolbar.\n"
        "4. Click it to insert the feature directly into your Feature Tree with full parametric controls (Length, Depth, Height, Wall Thickness)!\n\n"
        "Best regards,\n"
        "Tom\n"
    )

    send_cad_email(
        to_aliases=[args.recipient],
        subject=subject,
        body=body,
        attachment_paths=attachments,
        log_summary=f"Sent Onshape FeatureScript and STEP model to {args.recipient}",
    )


if __name__ == "__main__":
    main()
