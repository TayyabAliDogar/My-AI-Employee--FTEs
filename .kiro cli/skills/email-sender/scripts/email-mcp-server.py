#!/usr/bin/env python3
"""
Email MCP Server - Sends emails via Gmail API
"""

import os
import json
import base64
import logging
from datetime import datetime
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Gmail API scope for sending
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('EmailMCPServer')

class EmailSender:
    def __init__(self):
        self.service = None
        self.authenticate()

    def authenticate(self):
        """Authenticate with Gmail API"""
        creds = None
        token_path = 'gmail-sender-token.json'

        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(token_path, SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)

            with open(token_path, 'w') as token:
                token.write(creds.to_json())

        self.service = build('gmail', 'v1', credentials=creds)
        logger.info("Gmail API authenticated successfully")

    def create_message(self, to, subject, body, cc=None, bcc=None, html=False, attachments=None):
        """Create email message"""
        if html or attachments:
            message = MIMEMultipart()
        else:
            message = MIMEText(body)
            message['to'] = to
            message['subject'] = subject
            return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

        message['to'] = to
        message['subject'] = subject

        if cc:
            message['cc'] = cc
        if bcc:
            message['bcc'] = bcc

        # Add body
        if html:
            message.attach(MIMEText(body, 'html'))
        else:
            message.attach(MIMEText(body, 'plain'))

        # Add attachments
        if attachments:
            for filepath in attachments:
                if os.path.exists(filepath):
                    with open(filepath, 'rb') as f:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(f.read())
                        encoders.encode_base64(part)
                        part.add_header(
                            'Content-Disposition',
                            f'attachment; filename={os.path.basename(filepath)}'
                        )
                        message.attach(part)

        return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

    def send_email(self, to, subject, body, cc=None, bcc=None, html=False, attachments=None):
        """Send email via Gmail API"""
        try:
            message = self.create_message(to, subject, body, cc, bcc, html, attachments)

            result = self.service.users().messages().send(
                userId='me',
                body=message
            ).execute()

            logger.info(f"Email sent successfully to {to}")

            return {
                'message_id': result['id'],
                'status': 'sent',
                'timestamp': datetime.now().isoformat()
            }

        except HttpError as error:
            logger.error(f"Error sending email: {error}")
            raise

    def create_draft(self, to, subject, body, cc=None, bcc=None, html=False, attachments=None):
        """Create email draft"""
        try:
            message = self.create_message(to, subject, body, cc, bcc, html, attachments)

            draft = self.service.users().drafts().create(
                userId='me',
                body={'message': message}
            ).execute()

            logger.info(f"Draft created for {to}")

            return {
                'draft_id': draft['id'],
                'status': 'draft',
                'preview_url': f"https://mail.google.com/mail/u/0/#drafts/{draft['id']}"
            }

        except HttpError as error:
            logger.error(f"Error creating draft: {error}")
            raise

    def get_sent_emails(self, limit=10, since=None):
        """Get recently sent emails"""
        try:
            query = 'in:sent'
            if since:
                query += f' after:{since}'

            results = self.service.users().messages().list(
                userId='me',
                q=query,
                maxResults=limit
            ).execute()

            messages = results.get('messages', [])
            emails = []

            for msg in messages:
                message = self.service.users().messages().get(
                    userId='me',
                    id=msg['id'],
                    format='metadata'
                ).execute()

                headers = message['payload']['headers']
                to = next((h['value'] for h in headers if h['name'] == 'To'), '')
                subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '')
                date = next((h['value'] for h in headers if h['name'] == 'Date'), '')

                emails.append({
                    'id': msg['id'],
                    'to': to,
                    'subject': subject,
                    'sent_at': date
                })

            return {'emails': emails}

        except HttpError as error:
            logger.error(f"Error fetching sent emails: {error}")
            raise

def handle_mcp_request(tool, params):
    """Handle MCP tool requests"""
    sender = EmailSender()

    if tool == 'send_email':
        return sender.send_email(
            to=params['to'],
            subject=params['subject'],
            body=params['body'],
            cc=params.get('cc'),
            bcc=params.get('bcc'),
            html=params.get('html', False),
            attachments=params.get('attachments')
        )

    elif tool == 'create_draft':
        return sender.create_draft(
            to=params['to'],
            subject=params['subject'],
            body=params['body'],
            cc=params.get('cc'),
            bcc=params.get('bcc'),
            html=params.get('html', False),
            attachments=params.get('attachments')
        )

    elif tool == 'get_sent_emails':
        return sender.get_sent_emails(
            limit=params.get('limit', 10),
            since=params.get('since')
        )

    else:
        raise ValueError(f"Unknown tool: {tool}")

def main():
    """Main MCP server loop"""
    import argparse
    from http.server import HTTPServer, BaseHTTPRequestHandler

    parser = argparse.ArgumentParser(description='Email MCP Server')
    parser.add_argument('--port', type=int, default=8809, help='Server port')
    args = parser.parse_args()

    class MCPHandler(BaseHTTPRequestHandler):
        def do_POST(self):
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            request = json.loads(post_data)

            try:
                result = handle_mcp_request(request['tool'], request['params'])
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(result).encode())
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode())

    server = HTTPServer(('localhost', args.port), MCPHandler)
    logger.info(f"Email MCP Server running on port {args.port}")
    server.serve_forever()

if __name__ == '__main__':
    main()
