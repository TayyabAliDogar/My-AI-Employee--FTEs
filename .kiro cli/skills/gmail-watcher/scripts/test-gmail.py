#!/usr/bin/env python3
"""
Quick Test - Gmail Watcher
Tests Gmail authentication and fetches one email
"""

import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from gmail_watcher import GmailWatcher

    print("\n" + "="*60)
    print("  Gmail Watcher - Quick Test")
    print("="*60 + "\n")

    print("→ Initializing Gmail Watcher...")
    watcher = GmailWatcher()

    print("→ Authenticating with Gmail API...")
    print("  (This will open a browser window for OAuth consent)")
    watcher.authenticate()

    print("\n→ Fetching unread emails...")
    messages = watcher.get_unread_emails(max_results=1)

    if messages:
        print(f"✓ Found {len(messages)} unread email(s)")

        # Get details of first email
        email = watcher.get_email_details(messages[0]['id'])
        if email:
            print(f"\nSample Email:")
            print(f"  From: {email['sender']}")
            print(f"  Subject: {email['subject'][:50]}...")
            print(f"  Category: {watcher.categorize_email(email)}")
            print(f"  Priority: {watcher.determine_priority(email)}")
    else:
        print("✓ No unread emails found (inbox is clean!)")

    print("\n" + "="*60)
    print("✓ Gmail Watcher Test Complete!")
    print("="*60)
    print("\nYou can now run:")
    print("  python3 gmail-watcher.py          # Continuous monitoring")
    print("  python3 gmail-watcher.py --once   # Single check")
    print("\n")

except ImportError as e:
    print(f"\n✗ Import error: {e}")
    print("\nPlease ensure you're in the gmail-watcher/scripts directory")
    sys.exit(1)
except Exception as e:
    print(f"\n✗ Test failed: {e}")
    sys.exit(1)
