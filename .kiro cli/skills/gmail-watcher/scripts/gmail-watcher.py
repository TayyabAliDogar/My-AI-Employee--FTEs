#!/usr/bin/env python3
"""
Gmail Watcher - Production Ready
Monitors Gmail inbox and creates action items in Vault
"""

import os
import sys
import json
import time
import logging
import argparse
from datetime import datetime
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import base64

# Gmail API scope
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('gmail-watcher.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('GmailWatcher')

class GmailWatcher:
    def __init__(self, config_path='config.json', vault_path=None):
        self.config = self.load_config(config_path)
        self.service = None

        # Determine vault path
        if vault_path:
            self.vault_path = Path(vault_path)
        else:
            # Try to find Vault in parent directories
            current = Path.cwd()
            vault_found = False
            for _ in range(5):  # Search up to 5 levels
                potential_vault = current / 'Vault'
                if potential_vault.exists():
                    self.vault_path = potential_vault
                    vault_found = True
                    break
                current = current.parent

            if not vault_found:
                # Default to creating Vault in project root
                self.vault_path = Path('../../../Vault')

        self.needs_action_path = self.vault_path / 'Needs_Action'
        self.check_interval = self.config.get('check_interval', 60)
        self.processed_ids = set()

        # Ensure directories exist
        self.needs_action_path.mkdir(parents=True, exist_ok=True)
        logger.info(f"Vault path: {self.vault_path.absolute()}")
        logger.info(f"Output to: {self.needs_action_path.absolute()}")

    def load_config(self, config_path):
        """Load configuration from JSON file"""
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
                logger.info(f"Loaded config from {config_path}")
                return config
        except FileNotFoundError:
            logger.warning(f"Config file not found: {config_path}, using defaults")
            return {
                'check_interval': 60,
                'max_results': 10,
                'categories': {
                    'urgent': ['urgent', 'asap', 'important', 'critical'],
                    'client': ['client', 'customer', 'proposal'],
                    'invoice': ['invoice', 'payment', 'bill']
                },
                'priority_senders': [],
                'ignore_senders': ['noreply@', 'no-reply@', 'notifications@']
            }

    def authenticate(self):
        """Authenticate with Gmail API"""
        creds = None
        token_path = 'token.json'

        logger.info("Authenticating with Gmail API...")

        if os.path.exists(token_path):
            try:
                creds = Credentials.from_authorized_user_file(token_path, SCOPES)
                logger.info("Loaded existing credentials from token.json")
            except Exception as e:
                logger.error(f"Error loading token: {e}")
                creds = None

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    logger.info("Refreshing expired credentials...")
                    creds.refresh(Request())
                    logger.info("Credentials refreshed successfully")
                except Exception as e:
                    logger.error(f"Error refreshing credentials: {e}")
                    creds = None

            if not creds:
                if not os.path.exists('credentials.json'):
                    logger.error("credentials.json not found!")
                    logger.error("Please place your Gmail API credentials.json in this directory")
                    sys.exit(1)

                try:
                    logger.info("Starting OAuth flow...")
                    flow = InstalledAppFlow.from_client_secrets_file(
                        'credentials.json', SCOPES)
                    creds = flow.run_local_server(port=0)
                    logger.info("OAuth flow completed successfully")
                except Exception as e:
                    logger.error(f"OAuth flow failed: {e}")
                    sys.exit(1)

            # Save credentials
            try:
                with open(token_path, 'w') as token:
                    token.write(creds.to_json())
                logger.info("Credentials saved to token.json")
            except Exception as e:
                logger.error(f"Error saving token: {e}")

        try:
            self.service = build('gmail', 'v1', credentials=creds)
            logger.info("✓ Gmail API authenticated successfully")

            # Test the connection
            profile = self.service.users().getProfile(userId='me').execute()
            logger.info(f"✓ Connected to Gmail account: {profile.get('emailAddress')}")

        except Exception as e:
            logger.error(f"Error building Gmail service: {e}")
            sys.exit(1)

    def get_unread_emails(self, max_results=None):
        """Fetch unread emails from inbox"""
        if max_results is None:
            max_results = self.config.get('max_results', 10)

        try:
            results = self.service.users().messages().list(
                userId='me',
                labelIds=['INBOX', 'UNREAD'],
                maxResults=max_results
            ).execute()

            messages = results.get('messages', [])
            return messages
        except HttpError as error:
            logger.error(f"Error fetching emails: {error}")
            return []

    def get_email_details(self, msg_id):
        """Get full email details"""
        try:
            message = self.service.users().messages().get(
                userId='me',
                id=msg_id,
                format='full'
            ).execute()

            headers = message['payload']['headers']
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
            sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown')
            date = next((h['value'] for h in headers if h['name'] == 'Date'), '')

            # Get email body
            body = self.get_email_body(message['payload'])

            return {
                'id': msg_id,
                'subject': subject,
                'sender': sender,
                'date': date,
                'body': body,
                'thread_id': message['threadId'],
                'labels': message.get('labelIds', [])
            }
        except HttpError as error:
            logger.error(f"Error getting email details: {error}")
            return None

    def get_email_body(self, payload):
        """Extract email body from payload"""
        body = ""

        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    data = part['body'].get('data', '')
                    if data:
                        try:
                            body = base64.urlsafe_b64decode(data).decode('utf-8')
                            break
                        except:
                            pass
        else:
            data = payload['body'].get('data', '')
            if data:
                try:
                    body = base64.urlsafe_b64decode(data).decode('utf-8')
                except:
                    pass

        return body[:2000]  # Limit body length

    def categorize_email(self, email):
        """Categorize email based on content"""
        subject = email['subject'].lower()
        body = email['body'].lower()

        categories = self.config.get('categories', {})

        for category, keywords in categories.items():
            if any(keyword in subject or keyword in body for keyword in keywords):
                return category

        return 'general'

    def determine_priority(self, email):
        """Determine email priority"""
        subject = email['subject'].lower()
        sender = email['sender'].lower()

        urgent_keywords = ['urgent', 'asap', 'critical', 'important', 'emergency']
        if any(keyword in subject for keyword in urgent_keywords):
            return 'HIGH'

        priority_senders = self.config.get('priority_senders', [])
        if any(sender_domain.lower() in sender for sender_domain in priority_senders):
            return 'HIGH'

        return 'MEDIUM'

    def create_action_file(self, email):
        """Create action file in Needs_Action folder"""
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        safe_subject = "".join(c for c in email['subject'] if c.isalnum() or c in (' ', '-', '_')).strip()[:50]
        filename = f"EMAIL_{safe_subject}_{timestamp}.md"
        filepath = self.needs_action_path / filename

        category = self.categorize_email(email)
        priority = self.determine_priority(email)

        content = f"""# EMAIL: {email['subject']}

**From:** {email['sender']}
**Date:** {email['date']}
**Category:** {category}
**Priority:** {priority}

## Email Content

{email['body']}

## Suggested Actions

- [ ] Review email content
- [ ] Draft response
- [ ] Take appropriate action based on category

## Metadata

- Email ID: {email['id']}
- Labels: {', '.join(email['labels'])}
- Thread ID: {email['thread_id']}
- Processed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

*Auto-generated by Gmail Watcher*
*Silver Tier - AI Employee*
"""

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        logger.info(f"✓ Created action file: {filename}")
        return filepath

    def should_ignore_email(self, email):
        """Check if email should be ignored"""
        ignore_senders = self.config.get('ignore_senders', [
            'noreply@', 'no-reply@', 'notifications@', 'newsletter@'
        ])

        sender = email['sender'].lower()
        return any(ignore in sender for ignore in ignore_senders)

    def watch(self, once=False):
        """Main watch loop"""
        logger.info("="*60)
        logger.info("Gmail Watcher - Silver Tier")
        logger.info("="*60)
        logger.info(f"Monitoring Gmail inbox every {self.check_interval} seconds")
        logger.info(f"Output to: {self.needs_action_path}")
        logger.info("Press Ctrl+C to stop")
        logger.info("="*60)

        try:
            iteration = 0
            while True:
                iteration += 1
                logger.info(f"\n[Check #{iteration}] Fetching unread emails...")

                messages = self.get_unread_emails()

                if messages:
                    logger.info(f"✓ Found {len(messages)} unread email(s)")

                    for msg in messages:
                        msg_id = msg['id']

                        if msg_id in self.processed_ids:
                            logger.debug(f"Skipping already processed email: {msg_id}")
                            continue

                        email = self.get_email_details(msg_id)

                        if email:
                            if self.should_ignore_email(email):
                                logger.info(f"⊘ Ignoring email from: {email['sender']}")
                                self.processed_ids.add(msg_id)
                            else:
                                logger.info(f"→ Processing: {email['subject'][:50]}...")
                                self.create_action_file(email)
                                self.processed_ids.add(msg_id)
                else:
                    logger.info("No new unread emails")

                if once:
                    logger.info("Single check complete, exiting...")
                    break

                logger.info(f"Waiting {self.check_interval} seconds until next check...")
                time.sleep(self.check_interval)

        except KeyboardInterrupt:
            logger.info("\n✓ Gmail Watcher stopped by user")
        except Exception as e:
            logger.error(f"✗ Unexpected error: {e}", exc_info=True)

def main():
    parser = argparse.ArgumentParser(description='Gmail Watcher - Monitor Gmail inbox')
    parser.add_argument('--once', action='store_true', help='Check once and exit')
    parser.add_argument('--vault-path', help='Path to Vault directory')
    parser.add_argument('--config', default='config.json', help='Config file path')

    args = parser.parse_args()

    try:
        watcher = GmailWatcher(config_path=args.config, vault_path=args.vault_path)
        watcher.authenticate()
        watcher.watch(once=args.once)
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)

if __name__ == '__main__':
    main()
