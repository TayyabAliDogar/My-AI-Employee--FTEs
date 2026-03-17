# Silver Tier - Gmail & LinkedIn Watchers - COMPLETE

## ✅ Status: Production Ready

Both Gmail and LinkedIn watchers are now complete and ready for use with your credentials.

---

## Quick Start

### 1. Install Dependencies (One-Time Setup)

```bash
cd "My-AI-Employee -FTEs/.kiro cli/skills"
python3 install-watchers.py
```

This will:
- Install all required Python packages
- Check for credentials.json
- Create Vault structure
- Test Gmail authentication
- Provide LinkedIn setup instructions

### 2. Start Gmail Watcher

```bash
cd gmail-watcher/scripts

# Continuous monitoring (recommended)
python3 gmail-watcher.py

# Single check (for testing)
python3 gmail-watcher.py --once
```

### 3. Start LinkedIn Watcher (Optional)

```bash
# Set credentials
export LINKEDIN_EMAIL="your-email@example.com"
export LINKEDIN_PASSWORD="your-password"

# Start Playwright server
cd browsing-with-playwright/scripts
bash start-server.sh

# Start watcher
cd ../../linkedin-automation/scripts
python3 linkedin-watcher.py
```

---

## What's Included

### Gmail Watcher ✓
- **File**: `gmail-watcher/scripts/gmail-watcher.py`
- **Features**:
  - OAuth 2.0 authentication with your credentials.json
  - Monitors inbox every 60 seconds (configurable)
  - Categorizes emails (urgent, client, invoice, etc.)
  - Determines priority (HIGH/MEDIUM)
  - Creates action files in Vault/Needs_Action/
  - Ignores newsletters and automated emails
  - Comprehensive logging
  - Production-ready error handling

### LinkedIn Watcher ✓
- **File**: `linkedin-automation/scripts/linkedin-watcher.py`
- **Features**:
  - Monitors LinkedIn messages and notifications
  - Uses Playwright MCP for browser automation
  - Checks every 5 minutes (configurable)
  - Creates action files for new items
  - Secure credential handling via environment variables
  - Production-ready error handling

### Configuration Files ✓
- `gmail-watcher/scripts/config.json` - Gmail settings
- `gmail-watcher/scripts/requirements.txt` - Python dependencies
- `linkedin-automation/scripts/linkedin-config.json` - LinkedIn settings

### Documentation ✓
- `WATCHERS_QUICK_START.md` - Comprehensive setup guide
- `install-watchers.py` - Automated installation script
- `test-setup.sh` - Gmail setup test script

---

## How It Works

### Gmail Watcher Flow

```
1. Authenticate with Gmail API (OAuth 2.0)
   ↓
2. Fetch unread emails from INBOX
   ↓
3. For each email:
   - Extract subject, sender, body
   - Categorize (urgent/client/invoice/general)
   - Determine priority (HIGH/MEDIUM)
   - Check if should ignore (newsletters, etc.)
   ↓
4. Create action file in Vault/Needs_Action/
   Format: EMAIL_Subject_2026-03-17_10-30-00.md
   ↓
5. Wait 60 seconds and repeat
```

### LinkedIn Watcher Flow

```
1. Connect to Playwright MCP server
   ↓
2. Login to LinkedIn
   ↓
3. Check messages and notifications
   ↓
4. For each new item:
   - Extract content
   - Create action file
   ↓
5. Wait 5 minutes and repeat
```

---

## Output Examples

### Gmail Action File

```markdown
# EMAIL: Client Request - Urgent Proposal

**From:** client@example.com
**Date:** Mon, 17 Mar 2026 10:30:00
**Category:** client
**Priority:** HIGH

## Email Content

Hi, I need the proposal for the new project by tomorrow...

## Suggested Actions

- [ ] Review email content
- [ ] Draft response
- [ ] Take appropriate action based on category

## Metadata

- Email ID: 18e4f2a3b9c1d5e7
- Labels: INBOX, UNREAD
- Thread ID: 18e4f2a3b9c1d5e7
- Processed: 2026-03-17 10:32:00
```

### LinkedIn Action File

```markdown
# LINKEDIN MESSAGE: New Connection Request

**Type:** MESSAGE
**Date:** 2026-03-17 10:35:00
**Priority:** MEDIUM

## Content

John Smith wants to connect with you...

## Suggested Actions

- [ ] Review message
- [ ] Take appropriate action
- [ ] Respond if needed
```

---

## Configuration

### Gmail Watcher (`config.json`)

```json
{
  "check_interval": 60,
  "max_results": 10,
  "categories": {
    "urgent": ["urgent", "asap", "important", "critical"],
    "client": ["client", "customer", "proposal", "quote"],
    "invoice": ["invoice", "payment", "bill", "receipt"]
  },
  "priority_senders": [
    "@important-client.com",
    "boss@company.com"
  ],
  "ignore_senders": [
    "noreply@",
    "no-reply@",
    "notifications@",
    "newsletter@"
  ]
}
```

### LinkedIn Watcher (`linkedin-config.json`)

```json
{
  "check_interval": 300,
  "monitor_messages": true,
  "monitor_notifications": true
}
```

---

## Running in Production

### Background Mode (Linux/Mac)

```bash
# Gmail Watcher
cd gmail-watcher/scripts
nohup python3 gmail-watcher.py > gmail-watcher.log 2>&1 &

# LinkedIn Watcher
cd linkedin-automation/scripts
nohup python3 linkedin-watcher.py > linkedin-watcher.log 2>&1 &
```

### Scheduled Execution (Cron)

Add to crontab:

```cron
# Check Gmail every 5 minutes
*/5 * * * * cd /path/to/gmail-watcher/scripts && python3 gmail-watcher.py --once

# Check LinkedIn every 10 minutes
*/10 * * * * cd /path/to/linkedin-automation/scripts && python3 linkedin-watcher.py --once
```

---

## Logs

Both watchers create detailed logs:

- `gmail-watcher/scripts/gmail-watcher.log`
- `linkedin-automation/scripts/linkedin-watcher.log`

View logs in real-time:
```bash
tail -f gmail-watcher.log
```

---

## Troubleshooting

### Gmail Watcher

| Issue | Solution |
|-------|----------|
| "Module 'google' not found" | Run: `pip3 install -r requirements.txt` |
| "credentials.json not found" | Copy credentials.json to gmail-watcher/scripts/ |
| "Authentication failed" | Delete token.json and re-authenticate |
| "No emails found" | Check Gmail has unread emails in INBOX |

### LinkedIn Watcher

| Issue | Solution |
|-------|----------|
| "Playwright server not running" | Start: `bash start-server.sh` |
| "Login failed" | Check LINKEDIN_EMAIL and LINKEDIN_PASSWORD |
| "MCP timeout" | Restart Playwright server |

---

## Security

- ✓ **credentials.json** - OAuth client secrets (keep secure, never commit)
- ✓ **token.json** - Access tokens (auto-generated, never commit)
- ✓ **LinkedIn credentials** - Environment variables only
- ✓ **All data** - Stored locally in Vault (no cloud storage)

---

## Integration with AI Employee

Both watchers integrate seamlessly with your AI Employee workflow:

```
Gmail/LinkedIn Watcher
    ↓
Creates action files in Vault/Needs_Action/
    ↓
Plan Creator (every 30 min)
    ↓
Generates PLAN.md
    ↓
Claude Code executes plan
    ↓
Results in Vault/Done/
```

---

## Next Steps

1. ✅ **Test Gmail watcher** - Run with `--once` flag
2. ✅ **Verify action files** - Check Vault/Needs_Action/
3. ✅ **Configure categories** - Edit config.json
4. ⏭️ **Set up Plan Creator** - Automate task processing
5. ⏭️ **Add scheduling** - Use cron or task-scheduler skill

---

## Support

- **Quick Start**: `WATCHERS_QUICK_START.md`
- **Gmail Watcher**: `gmail-watcher/SKILL.md`
- **LinkedIn Automation**: `linkedin-automation/SKILL.md`
- **Silver Tier Guide**: `SILVER_TIER_README.md`

---

**Your Silver Tier watchers are complete and ready!** 🎉

Start monitoring Gmail and LinkedIn to automate your business communications.

Run: `python3 install-watchers.py` to begin.
