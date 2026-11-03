#!/usr/bin/env python3
"""
CLI helper to email 3D CAD models (STEP/STL/GLB) and engineering drawings to contacts or aliases.

Usage:
    python3 scripts/send_cad_model_email.py <recipient_alias> <attachment_path1> [attachment_path2 ...]
"""

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
    if len(sys.argv) < 3 or sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0)

    recipient = sys.argv[1]
    attachments = [Path(p).resolve() for p in sys.argv[2:]]

    subject = "3D CAD Model: Partitioned Storage Frame (STEP & Drawing)"
    body = (
        "Hi Roland,\n\n"
        "Attached is the 3D CAD model in STEP format (desk_storage_frame.step) for the "
        "partitioned storage frame (1600 x 800 x 300 mm, 6 bays) reconstructed from "
        "the concept sketch.\n\n"
        "You can import the STEP file directly into Onshape (Insert / Import into document).\n\n"
        "The dimensioned ISO 2D engineering drawing PDF is also attached for reference.\n\n"
        "Best regards,\n"
        "Tom\n"
    )

    send_cad_email(
        to_aliases=[recipient],
        subject=subject,
        body=body,
        attachment_paths=attachments,
        log_summary="Sent 3D STEP model and 2D drawing to Roland for Onshape import",
    )


if __name__ == "__main__":
    main()
