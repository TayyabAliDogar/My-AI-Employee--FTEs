#!/usr/bin/env python3
"""
Direct Email Sender - Sends emails directly via Gmail API
Bypasses MCP server requirement
"""

import os
import sys
import json
import base64
from pathlib import Path
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# Gmail API scope for sending
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def authenticate():
    """Authenticate with Gmail API"""
    # Look for credentials in email-sender directory
    token_path = Path(__file__).parent.parent / 'email-sender' / 'scripts' / 'gmail-sender-token.json'
    creds_path = Path(__file__).parent.parent / 'email-sender' / 'scripts' / 'credentials.json'

    creds = None

    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            # Save refreshed token
            with open(token_path, 'w') as token:
                token.write(creds.to_json())
        else:
            print(f"Error: Valid credentials not found at {token_path}")
            sys.exit(1)

    service = build('gmail', 'v1', credentials=creds)
    return service

def parse_draft(draft_path):
    """Parse draft markdown file"""
    with open(draft_path, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')
    data = {'to': '', 'subject': '', 'body': ''}

    in_body = False
    body_lines = []

    for line in lines:
        if line.startswith('**To:**'):
            data['to'] = line.replace('**To:**', '').strip()
        elif line.startswith('**Subject:**'):
            data['subject'] = line.replace('**Subject:**', '').strip()
        elif line.startswith('**Body:**'):
            in_body = True
            continue
        elif line.startswith('---') and in_body:
            break
        elif in_body:
            body_lines.append(line)

    data['body'] = '\n'.join(body_lines).strip()
    return data

def send_email(service, to, subject, body):
    """Send email via Gmail API"""
    message = MIMEText(body)
    message['to'] = to
    message['subject'] = subject

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

    try:
        result = service.users().messages().send(
            userId='me',
            body={'raw': raw}
        ).execute()
        return result
    except Exception as e:
        print(f"Error sending email: {e}")
        raise

def main():
    if len(sys.argv) < 2:
        print("Usage: python send-direct.py <draft_file.md>")
        sys.exit(1)

    draft_file = sys.argv[1]
    pending_path = Path(__file__).parent.parent.parent.parent / 'Vault' / 'Pending_Approval'
    draft_path = pending_path / draft_file

    if not draft_path.exists():
        print(f"Error: Draft file not found: {draft_path}")
        sys.exit(1)

    print(f"Sending: {draft_file}")

    # Parse draft
    data = parse_draft(draft_path)
    print(f"To: {data['to']}")
    print(f"Subject: {data['subject']}")

    # Authenticate
    service = authenticate()

    # Send email
    result = send_email(service, data['to'], data['subject'], data['body'])

    print(f"SUCCESS: Email sent successfully!")
    print(f"Message ID: {result.get('id', 'N/A')}")

    # Move to Done folder
    done_path = Path(__file__).parent.parent.parent.parent / 'Vault' / 'Done'
    done_path.mkdir(exist_ok=True)
    dest = done_path / f"SENT_{draft_file}"
    draft_path.rename(dest)
    print(f"SUCCESS: Moved to Done: SENT_{draft_file}")

if __name__ == '__main__':
    main()
