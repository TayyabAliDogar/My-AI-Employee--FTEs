---
name: gmail-watcher
description: |
  Monitor Gmail inbox for new emails and create action items in Obsidian vault.
  Automatically detects important emails, categorizes them, and triggers AI processing.
  Use when you need to automate email monitoring and response workflows.
---

# Gmail Watcher

Monitors Gmail inbox and creates actionable tasks in the Obsidian vault.

## Prerequisites

1. Gmail API credentials (OAuth 2.0)
2. Python 3.8+ with required packages
3. Obsidian vault with proper folder structure

## Setup

### 1. Enable Gmail API

```bash
# Install required packages
pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client

# Run setup script to authenticate
python3 scripts/setup-gmail.py
```

This will:
- Open browser for Google OAuth consent
- Save credentials to `scripts/token.json`
- Test connection to Gmail API

### 2. Configure Watcher

Edit `scripts/config.json`:

```json
{
  "vault_path": "../../Vault",
  "check_interval": 60,
  "categories": {
    "urgent": ["urgent", "asap", "important"],
    "client": ["client", "customer", "proposal"],
    "invoice": ["invoice", "payment", "bill"],
    "meeting": ["meeting", "schedule", "calendar"]
  }
}
```

## Running the Watcher

### Start Monitoring

```bash
# Using helper script (recommended)
bash scripts/start-watcher.sh

# Or manually
python3 scripts/gmail-watcher.py
```

### Stop Monitoring

```bash
# Using helper script
bash scripts/stop-watcher.sh

# Or manually
pkill -f "gmail-watcher.py"
```

## How It Works

1. **Poll Gmail**: Checks for unread emails every 60 seconds (configurable)
2. **Categorize**: Analyzes subject and sender to determine priority
3. **Create Action**: Generates markdown file in `Vault/Needs_Action/`
4. **Mark Read**: Optionally marks email as read after processing

## Action File Format

```markdown
# EMAIL: [Subject]

**From:** sender@example.com
**Date:** 2026-03-17 10:30:00
**Category:** client
**Priority:** high

## Email Content

[Email body text]

## Suggested Actions

- [ ] Review client request
- [ ] Draft response
- [ ] Schedule follow-up

## Metadata

- Email ID: 18e4f2a3b9c1d5e7
- Labels: INBOX, UNREAD
- Thread ID: 18e4f2a3b9c1d5e7
```

## Configuration Options

| Option | Default | Description |
|--------|---------|-------------|
| check_interval | 60 | Seconds between Gmail checks |
| max_results | 10 | Max emails to fetch per check |
| mark_as_read | false | Auto-mark processed emails as read |
| filter_labels | ["INBOX"] | Only process emails with these labels |

## Filtering Rules

Create custom filters in `scripts/filters.json`:

```json
{
  "ignore_senders": [
    "noreply@",
    "no-reply@",
    "notifications@"
  ],
  "priority_senders": [
    "client@company.com",
    "boss@company.com"
  ],
  "keywords": {
    "urgent": ["urgent", "asap", "critical"],
    "ignore": ["newsletter", "unsubscribe"]
  }
}
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Authentication failed | Re-run `python3 scripts/setup-gmail.py` |
| No emails detected | Check filter_labels in config.json |
| Permission denied | Ensure Gmail API scope includes gmail.readonly |
| Rate limit exceeded | Increase check_interval to 120+ seconds |

## Security Notes

- `token.json` contains OAuth credentials - keep it secure
- Never commit `token.json` to version control
- Use read-only Gmail scope unless sending emails
- Credentials expire after 7 days of inactivity

## Integration with Claude Code

The watcher creates action files that Claude Code can process:

```bash
# Claude Code will automatically detect new files in Needs_Action/
# and process them according to PLAN.md
```

## Verification

Run: `python3 scripts/verify.py`

Expected: `✓ Gmail API connected, X unread emails found`
