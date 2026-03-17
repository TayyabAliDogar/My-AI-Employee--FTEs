# Silver Tier - Gmail & LinkedIn Watchers - Quick Start

## Overview

This guide will help you set up and run the Gmail and LinkedIn watchers for your AI Employee.

## Prerequisites

1. **Python 3.8+** installed
2. **Gmail API credentials** (credentials.json) - ✓ You have this
3. **Playwright MCP server** (for LinkedIn) - from Bronze tier
4. **LinkedIn account** credentials

## Setup Gmail Watcher

### 1. Install Required Packages

```bash
pip3 install google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

### 2. Run Setup Test

```bash
cd "My-AI-Employee -FTEs/.kiro cli/skills/gmail-watcher/scripts"
bash test-setup.sh
```

This will:
- Check all prerequisites
- Authenticate with Gmail API (opens browser)
- Create token.json for future use
- Test fetching emails

### 3. Start Gmail Watcher

```bash
# Continuous monitoring (checks every 60 seconds)
python3 gmail-watcher.py

# Single check and exit
python3 gmail-watcher.py --once

# Custom vault path
python3 gmail-watcher.py --vault-path "/path/to/Vault"
```

## Setup LinkedIn Watcher

### 1. Set LinkedIn Credentials

```bash
# Linux/Mac
export LINKEDIN_EMAIL="your-email@example.com"
export LINKEDIN_PASSWORD="your-password"

# Windows PowerShell
$env:LINKEDIN_EMAIL="your-email@example.com"
$env:LINKEDIN_PASSWORD="your-password"
```

### 2. Start Playwright Server

```bash
cd "../browsing-with-playwright/scripts"
bash start-server.sh
```

### 3. Start LinkedIn Watcher

```bash
cd "../../linkedin-automation/scripts"

# Continuous monitoring (checks every 5 minutes)
python3 linkedin-watcher.py

# Single check and exit
python3 linkedin-watcher.py --once
```

## Configuration

### Gmail Watcher Config

Edit `gmail-watcher/scripts/config.json`:

```json
{
  "check_interval": 60,
  "max_results": 10,
  "categories": {
    "urgent": ["urgent", "asap", "important"],
    "client": ["client", "customer", "proposal"],
    "invoice": ["invoice", "payment", "bill"]
  },
  "priority_senders": [
    "@important-client.com",
    "boss@company.com"
  ],
  "ignore_senders": [
    "noreply@",
    "no-reply@",
    "notifications@"
  ]
}
```

### LinkedIn Watcher Config

Edit `linkedin-automation/scripts/linkedin-config.json`:

```json
{
  "check_interval": 300,
  "monitor_messages": true,
  "monitor_notifications": true
}
```

## How It Works

### Gmail Watcher

1. **Authenticates** with Gmail API using OAuth 2.0
2. **Fetches** unread emails from INBOX
3. **Categorizes** emails (urgent, client, invoice, etc.)
4. **Determines priority** (HIGH/MEDIUM)
5. **Creates action files** in `Vault/Needs_Action/`
6. **Ignores** newsletters and automated emails

### LinkedIn Watcher

1. **Connects** to Playwright MCP server
2. **Logs in** to LinkedIn
3. **Checks** messages and notifications
4. **Creates action files** for new items
5. **Monitors** continuously

## Output Files

Both watchers create markdown files in `Vault/Needs_Action/`:

### Gmail Example
```
EMAIL_Client_Request_2026-03-17_10-30-00.md
```

### LinkedIn Example
```
LINKEDIN_MESSAGE_2026-03-17_10-35-00.md
```

## Running in Background

### Linux/Mac

```bash
# Gmail Watcher
nohup python3 gmail-watcher.py > gmail-watcher.log 2>&1 &

# LinkedIn Watcher
nohup python3 linkedin-watcher.py > linkedin-watcher.log 2>&1 &
```

### Windows

```powershell
# Gmail Watcher
Start-Process python3 -ArgumentList "gmail-watcher.py" -WindowStyle Hidden

# LinkedIn Watcher
Start-Process python3 -ArgumentList "linkedin-watcher.py" -WindowStyle Hidden
```

## Stopping Watchers

```bash
# Find process
ps aux | grep watcher

# Kill process
kill <PID>

# Or use pkill
pkill -f gmail-watcher
pkill -f linkedin-watcher
```

## Troubleshooting

### Gmail Watcher

| Issue | Solution |
|-------|----------|
| "credentials.json not found" | Copy credentials.json to gmail-watcher/scripts/ |
| "Authentication failed" | Delete token.json and re-authenticate |
| "No emails found" | Check Gmail inbox has unread emails |
| "Permission denied" | Ensure Gmail API scope includes gmail.readonly |

### LinkedIn Watcher

| Issue | Solution |
|-------|----------|
| "Playwright server not running" | Start with: bash start-server.sh |
| "Login failed" | Check LINKEDIN_EMAIL and LINKEDIN_PASSWORD |
| "MCP call timeout" | Restart Playwright server |
| "No items found" | Check LinkedIn account has messages/notifications |

## Logs

Both watchers create log files:
- `gmail-watcher.log` - Gmail watcher activity
- `linkedin-watcher.log` - LinkedIn watcher activity

View logs:
```bash
tail -f gmail-watcher.log
tail -f linkedin-watcher.log
```

## Next Steps

1. **Test both watchers** with single check mode
2. **Verify action files** created in Vault/Needs_Action/
3. **Configure categories** and priorities
4. **Set up scheduling** (see task-scheduler skill)
5. **Integrate with Plan Creator** for automated processing

## Automated Scheduling

Add to crontab (Linux/Mac):

```cron
# Check Gmail every 5 minutes
*/5 * * * * cd /path/to/gmail-watcher/scripts && python3 gmail-watcher.py --once

# Check LinkedIn every 10 minutes
*/10 * * * * cd /path/to/linkedin-automation/scripts && python3 linkedin-watcher.py --once
```

## Security Notes

- **credentials.json** contains OAuth client secrets - keep secure
- **token.json** contains access tokens - never commit to git
- **LinkedIn credentials** should be in environment variables, not config files
- All data stored locally in Vault - no cloud storage

## Support

- Gmail Watcher: See `gmail-watcher/SKILL.md`
- LinkedIn Automation: See `linkedin-automation/SKILL.md`
- General: See `SILVER_TIER_README.md`

---

**Your Silver Tier watchers are ready!** 🎉

Start monitoring Gmail and LinkedIn to automate your business communications.
