---
name: orchestrator
description: |
  Email orchestration workflow that analyzes incoming emails, generates professional
  draft responses using Amazon PPC expertise, and manages approval workflow before sending.
  Integrates with Gmail MCP server for automated email sending.
---

# Orchestrator - Email Response Automation

Intelligent email analysis and response generation system with human-in-the-loop approval.

## Overview

The Orchestrator analyzes emails in `Vault/Needs_Action`, determines which require responses, generates professional draft replies using your Amazon PPC expertise profile, and saves them to `Vault/Pending_Approval` for your review before sending.

## Features

✅ **Intelligent Email Analysis**
- Categorizes emails by type (client, urgent, invoice, general)
- Filters out automated notifications (Indeed alerts, newsletters, etc.)
- Identifies client inquiries and high-priority messages
- Extracts key information from email content

✅ **Expert Draft Generation**
- Uses Amazon PPC expertise profile ($2M+ managed ad spend)
- Professional, data-driven tone
- Customized responses based on inquiry type
- Includes clear next steps and call-to-action

✅ **Approval Workflow**
- All drafts require manual approval before sending
- Clear approval instructions in each draft
- Easy approve/reject commands
- Audit logging of all sent emails

✅ **Gmail MCP Integration**
- Sends approved emails via Gmail API
- Tracks message IDs and send status
- Comprehensive error handling
- Rate limiting and security features

## Quick Start

### 1. Create Test Emails (Optional)

```bash
cd ".kiro cli/skills/orchestrator"
node create-test-emails.js
```

This creates 3 sample client inquiry emails in `Vault/Needs_Action/`.

### 2. Run Orchestrator

```bash
node orchestrator.js
```

This will:
- Analyze all emails in `Vault/Needs_Action/`
- Generate draft responses for client inquiries
- Save drafts to `Vault/Pending_Approval/`
- Skip automated notifications

### 3. Review Drafts

```bash
cd "../../../Vault/Pending_Approval"
cat DRAFT_*.md
```

Review the generated draft responses.

### 4. Approve and Send

```bash
cd ".kiro cli/skills/orchestrator"
node approve-and-send.js "DRAFT_filename.md"
```

Or tell Claude:
```
Approve and send DRAFT_Client_PPC_Consultation_Request_2026-03-17.md
```

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Email Orchestration Flow                  │
└─────────────────────────────────────────────────────────────┘

1. Gmail Watcher
   ↓
   Saves emails to: Vault/Needs_Action/

2. Orchestrator (orchestrator.js)
   ↓
   Analyzes emails:
   - Client inquiries → Generate draft
   - Urgent messages → Generate draft
   - Automated alerts → Skip
   ↓
   Saves drafts to: Vault/Pending_Approval/

3. Human Review
   ↓
   Reviews draft content
   Decides: Approve or Reject

4. Approve & Send (approve-and-send.js)
   ↓
   Sends via Gmail MCP Server
   ↓
   Logs to: Vault/Logs/email-sends.log
   Moves to: Vault/Done/SENT_*.md
```

## Configuration

### Expertise Profile

Edit `orchestrator.js` to customize your expertise profile:

```javascript
expertise: {
    name: 'Amazon PPC Expert',
    specialties: [
        'Amazon PPC campaign optimization',
        'ACOS and TACOS analysis',
        'Bid management strategies',
        // Add your specialties
    ],
    experience: '$2M+ in managed ad spend',
    tone: 'professional, confident, data-driven'
}
```

### Response Categories

Configure which email categories trigger responses:

```javascript
responseCategories: ['client', 'urgent', 'invoice']
```

### Ignore Senders

Add senders to automatically skip:

```javascript
ignoreSenders: [
    'noreply@',
    'alert@indeed.com',
    'notifications@',
    // Add more
]
```

## Email Analysis Logic

### Response Criteria

The orchestrator generates a draft if:

1. **Client Inquiry Detected**
   - Keywords: proposal, quote, consultation, help with, ppc, acos, tacos, campaign
   - Category: client
   - Action: Generate expert consultation response

2. **High Priority Email**
   - Priority: HIGH
   - Not from ignored sender
   - Action: Generate acknowledgment response

3. **Urgent Category**
   - Category: urgent
   - Action: Generate immediate response

### Skip Criteria

Emails are skipped if:
- From automated notification senders (Indeed, newsletters, etc.)
- Category not in response list
- No client inquiry keywords detected
- Already processed

## Draft Response Templates

### Client Inquiry Response

Professional response highlighting:
- Amazon PPC expertise and credentials
- Specific services offered (ACOS/TACOS optimization, bid management, etc.)
- Clear next steps (consultation call)
- Contact information and availability

### High Priority Response

Quick acknowledgment:
- Confirms receipt
- Promises detailed response within 24 hours
- Professional tone

### Urgent Response

Immediate attention:
- Acknowledges urgency
- Provides timeline for resolution
- Offers direct contact if needed

## Approval Workflow

### Draft Format

Each draft includes:

```markdown
# EMAIL DRAFT - PENDING APPROVAL

**Status:** 🟡 PENDING APPROVAL
**Created:** [timestamp]
**Original Email:** [filename]

---

## Draft Email

**To:** recipient@example.com
**Subject:** Re: [original subject]

**Body:**
[Generated response]

---

## Analysis

**Response Type:** client_inquiry
**Reason:** Client inquiry detected
**Requires Approval:** Yes (external communication)

---

## Approval Instructions

[Commands to approve or reject]
```

### Approval Commands

**Option 1: Command Line**
```bash
node approve-and-send.js "DRAFT_filename.md"
```

**Option 2: Tell Claude**
```
Approve and send DRAFT_Client_Request_2026-03-17.md
```

**Option 3: Reject**
```bash
mv "Vault/Pending_Approval/DRAFT_*.md" "Vault/Done/REJECTED_DRAFT_*.md"
```

## Gmail MCP Server Integration

### Prerequisites

1. Gmail MCP server running on port 8809
2. Gmail API credentials configured
3. OAuth token with send permissions

### Start MCP Server

```bash
cd ".kiro cli/skills/email-sender/scripts"
bash start-email-server.sh
```

### Verify Server

```bash
curl http://localhost:8809/health
```

Expected: `{"status": "ok", "service": "gmail-mcp-server"}`

### Send Email via MCP

The `approve-and-send.js` script automatically:
1. Reads draft from Pending_Approval
2. Extracts To, Subject, Body
3. Sends POST request to MCP server
4. Logs response and message ID
5. Moves draft to Done folder

## Logging

### Email Send Log

Location: `Vault/Logs/email-sends.log`

Format:
```
2026-03-17T10:30:00Z | SENT | to:client@example.com | subject:Re: Consultation | msg_id:18e4f2a3b9c1d5e7
```

### JSON Log

Location: `Vault/Logs/email-sends.json`

Contains detailed send information:
```json
{
  "timestamp": "2026-03-17T10:30:00Z",
  "draft_file": "DRAFT_Client_Request.md",
  "to": "client@example.com",
  "subject": "Re: Consultation Request",
  "status": "sent",
  "message_id": "18e4f2a3b9c1d5e7",
  "error": null
}
```

## Security Features

### Approval Requirements

- **All external emails require approval** - No automatic sending
- **Human-in-the-loop** - You review every draft before sending
- **Audit trail** - All sends logged with timestamps and message IDs

### Rate Limiting

- Managed by Gmail MCP server
- Default: 100 emails/day, 10 emails/hour
- Prevents accidental bulk sending

### Sender Filtering

- Ignores automated notifications
- Prevents responses to no-reply addresses
- Configurable ignore list

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No drafts created | Check if emails match response criteria |
| MCP server connection failed | Start server: `bash start-email-server.sh` |
| Draft parsing error | Verify draft file format is correct |
| Send failed | Check Gmail API credentials and token |
| Duplicate drafts | Orchestrator creates one draft per email |

## Example Workflow

### Complete End-to-End Example

```bash
# 1. Create test emails
cd ".kiro cli/skills/orchestrator"
node create-test-emails.js

# Output:
# ✓ Created: EMAIL_Client_PPC_Consultation_Request_2026-03-17_TEST.md
# ✓ Created: EMAIL_Urgent_Campaign_Help_Needed_2026-03-17_TEST.md
# ✓ Created: EMAIL_Product_Launch_Strategy_Inquiry_2026-03-17_TEST.md

# 2. Run orchestrator
node orchestrator.js

# Output:
# Found 3 email(s) to analyze
# [Processing] EMAIL_Client_PPC_Consultation_Request_2026-03-17_TEST.md
#   ✓ Response needed: Client inquiry detected
#   ✓ Draft created: DRAFT_Client_PPC_Consultation_Request_2026-03-17.md
# ...
# Drafts created: 3

# 3. Review draft
cat "../../../Vault/Pending_Approval/DRAFT_Client_PPC_Consultation_Request_2026-03-17.md"

# 4. Approve and send
node approve-and-send.js "DRAFT_Client_PPC_Consultation_Request_2026-03-17.md"

# Output:
# ✓ Email sent successfully!
# Message ID: 18e4f2a3b9c1d5e7
# ✓ Moved to Done: SENT_DRAFT_Client_PPC_Consultation_Request_2026-03-17.md
```

## Integration with Other Skills

### Gmail Watcher
- Monitors inbox every 60 seconds
- Creates email files in Needs_Action
- Orchestrator processes these automatically

### Email Sender MCP
- Provides Gmail API integration
- Handles authentication and sending
- Returns message IDs for tracking

### Approval Workflow
- Human review before sending
- Risk assessment for external communications
- Audit logging

## Customization

### Custom Response Templates

Edit `orchestrator.js` to add custom templates:

```javascript
generateCustomResponse() {
    return `Your custom template here...`;
}
```

### Custom Analysis Rules

Add custom email analysis logic:

```javascript
shouldRespond() {
    // Your custom logic
    if (this.emailData.body.includes('custom keyword')) {
        return { respond: true, reason: 'Custom rule matched' };
    }
}
```

### Custom Expertise Profile

Update the expertise section to match your business:

```javascript
expertise: {
    name: 'Your Name',
    specialties: ['Your', 'Specialties'],
    experience: 'Your experience',
    tone: 'your preferred tone'
}
```

## Best Practices

1. **Review Every Draft** - Always review before approving
2. **Customize Templates** - Adjust response templates to match your voice
3. **Monitor Logs** - Check email-sends.log regularly
4. **Test First** - Use create-test-emails.js to test workflow
5. **Keep MCP Running** - Ensure Gmail MCP server is always available

## Verification

Run orchestrator on test emails:

```bash
node create-test-emails.js && node orchestrator.js
```

Expected output:
```
✓ Test emails created successfully!
Found 3 email(s) to analyze
Drafts created: 3
```

## Files Created

- `orchestrator.js` - Main orchestration engine
- `approve-and-send.js` - Email sending script
- `create-test-emails.js` - Test email generator
- `SKILL.md` - This documentation

## Next Steps

1. Run orchestrator on your real emails
2. Review and customize response templates
3. Set up Gmail MCP server for sending
4. Configure your expertise profile
5. Test the complete workflow with test emails

---

*Orchestrator - Silver Tier AI Employee*
*Intelligent Email Response Automation*
