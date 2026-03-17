---
name: approval-workflow
description: |
  Human-in-the-loop approval system for sensitive AI actions. Manages approval requests,
  tracks decisions, and enforces approval policies. Use when AI needs to perform actions
  that require human oversight (emails, financial transactions, social posts).
---

# Approval Workflow

Human-in-the-loop approval system for sensitive AI actions.

## Overview

The approval workflow ensures that sensitive actions (external communications, financial transactions, legal documents) require explicit human approval before execution.

## How It Works

1. **Action Request**: AI identifies action requiring approval
2. **Create Request**: Saves approval request to `Vault/Pending_Approval/`
3. **Human Review**: User reviews request in Obsidian
4. **Decision**: User approves or rejects
5. **Execution**: If approved, AI executes action
6. **Logging**: Decision and outcome logged

## Quick Reference

### Check Pending Approvals

```bash
# List all pending approvals
python3 scripts/list-approvals.py --vault-path "../../Vault"

# Check specific approval
python3 scripts/check-approval.py --file "APPROVAL_EMAIL_2026-03-17.md"
```

### Approve/Reject Actions

```bash
# Approve action
python3 scripts/approve.py --file "Vault/Pending_Approval/APPROVAL_EMAIL_2026-03-17.md"

# Reject action
python3 scripts/reject.py --file "Vault/Pending_Approval/APPROVAL_EMAIL_2026-03-17.md" --reason "Incorrect recipient"

# Approve with modifications
python3 scripts/approve.py --file "APPROVAL_EMAIL_2026-03-17.md" --modify
```

## Approval Request Format

### Email Approval Request

```markdown
# APPROVAL REQUEST: Send Email

**Type:** Email Communication
**Priority:** HIGH
**Created:** 2026-03-17 10:30:00
**Requires Approval By:** 2026-03-17 18:00:00

## Action Details

**To:** client@example.com
**CC:** manager@company.com
**Subject:** Re: Project Proposal

**Body:**
Hi John,

Thank you for your interest in our services. I've reviewed your requirements and prepared a proposal.

[Proposal details]

Please let me know if you have any questions.

Best regards,
AI Employee

## Risk Assessment

- **External Communication:** Yes
- **Contains Sensitive Info:** No
- **Financial Impact:** None
- **Legal Implications:** None

## Approval Decision

**Status:** PENDING

[ ] APPROVE - Send email as drafted
[ ] APPROVE WITH CHANGES - Modify before sending
[ ] REJECT - Do not send

**Approved By:** _____________
**Date:** _____________
**Notes:** _____________

---

*To approve: Change status to APPROVED and add your name*
*To reject: Change status to REJECTED and add reason*
