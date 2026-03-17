---
name: email-sender
description: |
  Send emails via Gmail API with MCP server integration. Handles email composition,
  sending, and tracking. Requires human approval for external communications.
  Use when Claude needs to send emails as part of automated workflows.
---

# Email Sender

MCP server for sending emails through Gmail API with approval workflow.

## Prerequisites

1. Gmail API credentials (OAuth 2.0)
2. Python 3.8+ with required packages
3. MCP server framework

## Setup

### 1. Install Dependencies

```bash
pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client mcp
```

### 2. Enable Gmail API

```bash
# Run setup to get credentials
python3 scripts/setup-gmail-sender.py
```

This will:
- Enable Gmail API with send permissions
- Create OAuth credentials
- Save to `scripts/gmail-sender-token.json`

### 3. Start MCP Server

```bash
# Using helper script (recommended)
bash scripts/start-email-server.sh

# Or manually
python3 scripts/email-mcp-server.py --port 8809
```

## Quick Reference

### Send Email via MCP

```bash
# Send simple email
python3 scripts/mcp-client.py call -u http://localhost:8809 -t send_email \
  -p '{"to": "recipient@example.com", "subject": "Test", "body": "Hello!"}'

# Send with CC and attachments
python3 scripts/mcp-client.py call -u http://localhost:8809 -t send_email \
  -p '{"to": "recipient@example.com", "cc": "cc@example.com", "subject": "Report", "body": "See attached", "attachments": ["/path/to/file.pdf"]}'

# Send HTML email
python3 scripts/mcp-client.py call -u http://localhost:8809 -t send_email \
  -p '{"to": "recipient@example.com", "subject": "Newsletter", "body": "<h1>Hello</h1><p>Content</p>", "html": true}'
```

### Draft Email (No Send)

```bash
# Create draft for review
python3 scripts/mcp-client.py call -u http://localhost:8809 -t create_draft \
  -p '{"to": "recipient@example.com", "subject": "Draft", "body": "Review this"}'
```

## MCP Server Tools

### send_email

Send an email through Gmail.

**Parameters:**
- `to` (required): Recipient email address
- `subject` (required): Email subject
- `body` (required): Email body (plain text or HTML)
- `cc` (optional): CC recipients (comma-separated)
- `bcc` (optional): BCC recipients (comma-separated)
- `attachments` (optional): Array of file paths
- `html` (optional): Boolean, true if body is HTML

**Returns:**
```json
{
  "message_id": "18e4f2a3b9c1d5e7",
  "status": "sent",
  "timestamp": "2026-03-17T10:30:00Z"
}
```

### create_draft

Create email draft without sending.

**Parameters:** Same as send_email

**Returns:**
```json
{
  "draft_id": "r-1234567890",
  "status": "draft",
  "preview_url": "https://mail.google.com/mail/u/0/#drafts/r-1234567890"
}
```

### get_sent_emails

Retrieve recently sent emails.

**Parameters:**
- `limit` (optional): Max emails to return (default: 10)
- `since` (optional): ISO timestamp to filter from

**Returns:**
```json
{
  "emails": [
    {
      "id": "18e4f2a3b9c1d5e7",
      "to": "recipient@example.com",
      "subject": "Test",
      "sent_at": "2026-03-17T10:30:00Z"
    }
  ]
}
```

## Integration with Approval Workflow

### Workflow

1. **Draft Creation**: Claude creates email draft
2. **Save for Approval**: Draft saved to `Vault/Pending_Approval/`
3. **Human Review**: User reviews and approves
4. **Send**: Approved email sent via MCP server
5. **Logging**: Email logged to `Vault/Done/`

### Example: Automated Email Response

```python
# 1. Claude analyzes incoming email
# 2. Generates response draft
# 3. Saves to Pending_Approval/EMAIL_DRAFT_*.md
# 4. User approves
# 5. Script sends via MCP server

python3 scripts/send-approved-email.py --draft-file "Vault/Pending_Approval/EMAIL_DRAFT_2026-03-17.md"
```

## Email Templates

### Client Response Template

```markdown
# EMAIL DRAFT

**To:** client@example.com
**Subject:** Re: Your Request

**Body:**

Hi [Client Name],

Thank you for reaching out. I've reviewed your request and here's what I can do:

[Response content]

Please let me know if you have any questions.

Best regards,
[Your Name]

---

**Approval Status:** PENDING
**Created:** 2026-03-17 10:30:00
**Requires Approval:** Yes (external communication)
```

## Configuration

Edit `scripts/email-config.json`:

```json
{
  "smtp_settings": {
    "use_gmail_api": true,
    "from_name": "Your Name",
    "from_email": "you@example.com"
  },
  "approval_rules": {
    "require_approval_for_external": true,
    "auto_approve_internal": false,
    "max_recipients": 10
  },
  "templates": {
    "signature": "\n\nBest regards,\nYour Name\nYour Company",
    "footer": "\n\n---\nThis email was sent via AI Employee"
  }
}
```

## Security Features

### Approval Requirements

All emails require approval by default:
- External recipients: Always require approval
- Internal recipients: Configurable
- Bulk emails (>5 recipients): Always require approval
- Emails with attachments: Always require approval

### Rate Limiting

- Max 100 emails per day
- Max 10 emails per hour
- Cooldown period between sends

### Audit Logging

All sent emails are logged:
```
2026-03-17 10:30:00 | SENT | to:client@example.com | subject:Response | approved_by:user
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Authentication failed | Re-run setup-gmail-sender.py |
| Permission denied | Ensure Gmail API scope includes gmail.send |
| Rate limit exceeded | Wait 1 hour or increase quota |
| Attachment too large | Gmail limit is 25MB, compress files |
| MCP server not responding | Restart: bash scripts/restart-email-server.sh |

## Server Management

### Start Server

```bash
bash scripts/start-email-server.sh
```

### Stop Server

```bash
bash scripts/stop-email-server.sh
```

### Check Status

```bash
python3 scripts/verify-email-server.py
```

Expected: `✓ Email MCP server running on port 8809`

## Integration with Claude Code

Claude Code can use this skill to send emails:

```bash
# Claude detects email draft in Pending_Approval
# User approves
# Claude calls email-sender skill to send
```

## Best Practices

1. **Always Draft First**: Never send without creating draft
2. **Require Approval**: External emails must be approved
3. **Use Templates**: Maintain consistent formatting
4. **Log Everything**: Keep audit trail of all sends
5. **Test Recipients**: Use test email for development

## Verification

Run: `python3 scripts/verify.py`

Expected: `✓ Email MCP server ready, Gmail API connected`
