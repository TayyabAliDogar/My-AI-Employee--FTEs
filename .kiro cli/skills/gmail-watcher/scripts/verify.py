#!/usr/bin/env python3
"""
Verify Gmail Watcher setup
"""

import os
import sys
from pathlib import Path

def check_file(filepath, description):
    """Check if file exists"""
    if Path(filepath).exists():
        print(f"✓ {description}")
        return True
    else:
        print(f"✗ {description} - NOT FOUND")
        return False

def check_gmail_api():
    """Check Gmail API connection"""
    try:
        from google.oauth2.credentials import Credentials
        from googleapiclient.discovery import build

        if not os.path.exists('token.json'):
            print("✗ Gmail API - Not authenticated (run setup-gmail.sh)")
            return False

        creds = Credentials.from_authorized_user_file('token.json')
        service = build('gmail', 'v1', credentials=creds)

        # Test API call
        results = service.users().messages().list(userId='me', maxResults=1).execute()

        print("✓ Gmail API - Connected")
        return True

    except Exception as e:
        print(f"✗ Gmail API - Error: {e}")
        return False

def main():
    print("\n=== Gmail Watcher Verification ===\n")

    checks = [
        check_file('gmail-watcher.py', 'Gmail watcher script'),
        check_file('config.json', 'Configuration file'),
        check_file('../../Vault', 'Vault directory'),
        check_gmail_api()
    ]

    print("\n" + "="*40)

    if all(checks):
        print("✓ All checks passed - Gmail Watcher ready!")
        sys.exit(0)
    else:
        print("✗ Some checks failed - Please fix issues above")
        sys.exit(1)

if __name__ == '__main__':
    main()
