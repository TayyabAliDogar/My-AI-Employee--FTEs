---
name: plan-creator
description: |
  Creates strategic PLAN.md files for Claude Code to execute. Analyzes tasks in Needs_Action
  folder and generates step-by-step execution plans with priorities, dependencies, and
  approval requirements. Use when you need Claude to autonomously process multiple tasks.
---

# Plan Creator

Generates execution plans for autonomous task processing by Claude Code.

## Overview

The Plan Creator analyzes pending tasks and creates structured PLAN.md files that guide Claude Code through multi-step workflows with proper prioritization and human oversight.

## How It Works

1. **Scan**: Reads all files in `Vault/Needs_Action/`
2. **Analyze**: Categorizes tasks by type, priority, and complexity
3. **Plan**: Creates execution strategy with dependencies
4. **Output**: Generates PLAN.md with clear instructions

## Quick Reference

### Generate Plan

```bash
# Analyze and create plan
python3 scripts/create-plan.py --vault-path "../../Vault"

# With specific focus
python3 scripts/create-plan.py --focus "urgent" --vault-path "../../Vault"

# Dry run (preview only)
python3 scripts/create-plan.py --dry-run
```

### Plan Structure

```markdown
# EXECUTION PLAN

**Generated:** 2026-03-17 10:30:00
**Tasks:** 5
**Estimated Time:** 15 minutes

## Priority Queue

### HIGH PRIORITY (Execute First)
1. EMAIL_Client_Request_Urgent
2. DOCUMENT_Invoice_Review

### MEDIUM PRIORITY
3. EMAIL_Meeting_Confirmation
4. DOCUMENT_Contract_Draft

### LOW PRIORITY (If Time Permits)
5. EMAIL_Newsletter_Response

## Execution Strategy

### Task 1: Client Request (HIGH)
- **File:** EMAIL_Client_Request_Urgent_2026-03-17.md
- **Action:** Draft response email
- **Approval:** Required before sending
- **Dependencies:** None
- **Estimated Time:** 5 minutes

### Task 2: Invoice Review (HIGH)
- **File:** DOCUMENT_Invoice_Review_2026-03-17.md
- **Action:** Verify calculations, flag discrepancies
- **Approval:** Required for amounts > $1000
- **Dependencies:** None
- **Estimated Time:** 3 minutes

## Approval Requirements

- Task 1: Human approval required before sending email
- Task 2: Human approval required for financial transaction

## Success Criteria

- All HIGH priority tasks completed
- Approval requests created for sensitive actions
- All outputs saved to appropriate folders
- Dashboard updated with results
```

## Configuration

Edit `scripts/plan-config.json`:

```json
{
  "vault_path": "../../Vault",
  "max_tasks_per_plan": 10,
  "priority_rules": {
    "urgent_keywords": ["urgent", "asap", "critical"],
    "high_value_threshold": 1000,
    "client_priority": true
  },
  "approval_rules": {
    "financial_threshold": 500,
    "external_communication": true,
    "legal_documents": true
  }
}
```

## Task Categorization

### Automatic Priority Assignment

| Category | Priority | Criteria |
|----------|----------|----------|
| Client Email | HIGH | From client or contains "urgent" |
| Financial | HIGH | Amount > $1000 or invoice/payment |
| Legal | HIGH | Contract, agreement, compliance |
| Internal | MEDIUM | Team communication, updates |
| Administrative | LOW | Filing, organization, routine |

### Approval Requirements

| Task Type | Approval Needed | Reason |
|-----------|----------------|---------|
| Send Email | Yes | External communication |
| Financial Transaction | Yes | Money involved |
| Legal Document | Yes | Legal implications |
| Social Media Post | Yes | Public visibility |
| Internal Note | No | Low risk |

## Integration with Claude Code

### Workflow

1. **Watcher** detects new files → `Needs_Action/`
2. **Plan Creator** analyzes tasks → generates `PLAN.md`
3. **Claude Code** reads `PLAN.md` → executes tasks
4. **Approval Workflow** handles sensitive actions
5. **Dashboard** updates with results

### Triggering Claude Code

```bash
# Manual trigger
claude-code "Execute the plan in Vault/Needs_Action/PLAN.md"

# Automated trigger (via cron)
*/30 * * * * cd /path/to/vault && claude-code "Check for PLAN.md and execute"
```

## Plan Templates

### Simple Task Plan
```markdown
# EXECUTION PLAN

## Task 1: [Task Name]
- Read file
- Analyze content
- Take action
- Save result
```

### Complex Multi-Step Plan
```markdown
# EXECUTION PLAN

## Phase 1: Analysis
- Task 1: Review documents
- Task 2: Extract key information

## Phase 2: Action
- Task 3: Draft responses
- Task 4: Create summaries

## Phase 3: Approval
- Task 5: Submit for human review
```

## Advanced Features

### Dependency Management

```python
# Tasks with dependencies
Task 2 depends on Task 1 completion
Task 3 depends on Task 1 AND Task 2
```

### Conditional Execution

```python
# Execute only if condition met
IF invoice_amount > 1000 THEN require_approval
IF sender == "client@company.com" THEN priority = HIGH
```

### Error Handling

```python
# Fallback strategies
IF task_fails THEN save_to_pending AND notify_human
IF approval_timeout THEN escalate_to_manager
```

## Monitoring

### Plan Execution Logs

```bash
# View execution history
cat Vault/Logs/plan-execution.log

# Check success rate
python3 scripts/plan-stats.py
```

### Metrics Tracked

- Plans generated per day
- Tasks completed vs pending
- Average execution time
- Approval response time
- Success/failure rate

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No plan generated | Check if Needs_Action folder has files |
| Tasks not prioritized | Review priority_rules in config |
| Missing dependencies | Ensure all referenced files exist |
| Approval not triggered | Check approval_rules configuration |

## Best Practices

1. **Keep Plans Focused**: Max 10 tasks per plan
2. **Clear Instructions**: Each task should be unambiguous
3. **Proper Prioritization**: HIGH tasks should truly be urgent
4. **Approval Gates**: Always require approval for sensitive actions
5. **Update Dashboard**: Reflect plan status in Dashboard.md

## Verification

Run: `python3 scripts/verify-plan.py`

Expected: `✓ Plan creator ready, X tasks pending`
