---
name: task-scheduler
description: |
  Schedule automated tasks using cron (Linux/Mac) or Task Scheduler (Windows).
  Enables periodic execution of watchers, plan generation, and AI processing.
  Use when you need to run AI Employee tasks on a schedule (hourly, daily, weekly).
---

# Task Scheduler

Automated scheduling for AI Employee tasks using cron or Windows Task Scheduler.

## Overview

The Task Scheduler enables autonomous operation by running tasks on a schedule:
- Watchers check for new emails/messages every N minutes
- Plan Creator generates execution plans periodically
- Claude Code processes plans automatically
- Dashboard updates on schedule

## Platform Support

- **Linux/Mac**: Uses cron
- **Windows**: Uses Task Scheduler
- **Cross-platform**: Python-based scheduler included

## Quick Reference

### Setup Scheduled Tasks

```bash
# Linux/Mac: Install cron jobs
bash scripts/install-cron.sh

# Windows: Install scheduled tasks
powershell scripts/install-tasks.ps1

# Cross-platform: Use Python scheduler
python3 scripts/scheduler.py --config scheduler-config.json
```

### View Scheduled Tasks

```bash
# Linux/Mac
crontab -l

# Windows
schtasks /query /fo LIST /v

# Python scheduler
python3 scripts/scheduler.py --list
```

## Cron Setup (Linux/Mac)

### Install Cron Jobs

```bash
# Run installation script
bash scripts/install-cron.sh

# Or manually edit crontab
crontab -e
```

### Example Crontab

```cron
# AI Employee Scheduled Tasks

# Check Gmail every 5 minutes
*/5 * * * * cd /path/to/skills/gmail-watcher && python3 scripts/gmail-watcher.py --once

# Check WhatsApp every 10 minutes
*/10 * * * * cd /path/to/skills/whatsapp-watcher && python3 scripts/whatsapp-watcher.py --once

# Generate plan every 30 minutes
*/30 * * * * cd /path/to/skills/plan-creator && python3 scripts/create-plan.py

# Execute plan every hour
0 * * * * cd /path/to/vault && claude-code "Execute PLAN.md if exists"

# Post to LinkedIn daily at 9 AM
0 9 * * 1-5 cd /path/to/skills/linkedin-automation && python3 scripts/linkedin-post.py --auto

# Weekly business review every Monday at 8 AM
0 8 * * 1 cd /path/to/vault && claude-code "Generate weekly business review"

# Update dashboard every 15 minutes
*/15 * * * * cd /path/to/vault && python3 scripts/update-dashboard.py
```

## Windows Task Scheduler

### Install Tasks (PowerShell)

```powershell
# Run as Administrator
.\scripts\install-tasks.ps1

# Or create individual task
schtasks /create /tn "AI Employee - Gmail Watcher" /tr "python C:\path\to\gmail-watcher.py" /sc minute /mo 5
```

### Example Tasks

```xml
<!-- Gmail Watcher - Every 5 minutes -->
<Task>
  <Triggers>
    <TimeTrigger>
      <Repetition>
        <Interval>PT5M</Interval>
      </Repetition>
    </TimeTrigger>
  </Triggers>
  <Actions>
    <Exec>
      <Command>python</Command>
      <Arguments>C:\path\to\gmail-watcher.py --once</Arguments>
    </Exec>
  </Actions>
</Task>
```

## Python Scheduler (Cross-Platform)

### Configuration

Create `scripts/scheduler-config.json`:

```json
{
  "tasks": [
    {
      "name": "gmail-watcher",
      "command": "python3 ../gmail-watcher/scripts/gmail-watcher.py --once",
      "schedule": "*/5 * * * *",
      "enabled": true
    },
    {
      "name": "whatsapp-watcher",
      "command": "python3 ../whatsapp-watcher/scripts/whatsapp-watcher.py --once",
      "schedule": "*/10 * * * *",
      "enabled": true
    },
    {
      "name": "plan-creator",
      "command": "python3 ../plan-creator/scripts/create-plan.py",
      "schedule": "*/30 * * * *",
      "enabled": true
    },
    {
      "name": "linkedin-post",
      "command": "python3 ../linkedin-automation/scripts/linkedin-post.py --auto",
      "schedule": "0 9 * * 1-5",
      "enabled": true
    }
  ],
  "timezone": "America/New_York",
  "log_file": "../../Vault/Logs/scheduler.log"
}
```

### Run Scheduler

```bash
# Start scheduler daemon
python3 scripts/scheduler.py --daemon

# Run in foreground (for testing)
python3 scripts/scheduler.py

# Stop scheduler
python3 scripts/scheduler.py --stop
```

## Schedule Patterns

### Cron Syntax

```
* * * * *
│ │ │ │ │
│ │ │ │ └─── Day of week (0-7, Sun=0 or 7)
│ │ │ └───── Month (1-12)
│ │ └─────── Day of month (1-31)
│ └───────── Hour (0-23)
└─────────── Minute (0-59)
```

### Common Patterns

| Pattern | Description |
|---------|-------------|
| `*/5 * * * *` | Every 5 minutes |
| `0 * * * *` | Every hour |
| `0 9 * * *` | Daily at 9 AM |
| `0 9 * * 1-5` | Weekdays at 9 AM |
| `0 0 * * 0` | Weekly on Sunday midnight |
| `0 0 1 * *` | Monthly on 1st at midnight |

## Recommended Schedules

### Silver Tier Setup

```bash
# Watchers (frequent checks)
*/5 * * * *   - Gmail Watcher
*/10 * * * *  - WhatsApp Watcher

# Processing (moderate frequency)
*/30 * * * *  - Plan Creator
0 * * * *     - Execute Plans

# Content (daily)
0 9 * * 1-5   - LinkedIn Post

# Reporting (weekly)
0 8 * * 1     - Weekly Review

# Maintenance (daily)
0 0 * * *     - Cleanup old logs
```

## Task Management

### Enable/Disable Tasks

```bash
# Disable task
python3 scripts/scheduler.py --disable gmail-watcher

# Enable task
python3 scripts/scheduler.py --enable gmail-watcher

# Pause all tasks
python3 scripts/scheduler.py --pause-all
```

### Monitor Task Execution

```bash
# View logs
tail -f ../../Vault/Logs/scheduler.log

# Check last run times
python3 scripts/scheduler.py --status

# View task history
python3 scripts/scheduler.py --history gmail-watcher
```

## Error Handling

### Retry Logic

```json
{
  "retry_on_failure": true,
  "max_retries": 3,
  "retry_delay": 300
}
```

### Notifications

```json
{
  "notify_on_failure": true,
  "notification_methods": ["email", "log"],
  "alert_email": "admin@example.com"
}
```

## Integration with AI Employee

### Autonomous Workflow

```
1. [Every 5 min]  Gmail Watcher → Detects new emails
2. [Every 10 min] WhatsApp Watcher → Detects messages
3. [Every 30 min] Plan Creator → Generates PLAN.md
4. [Every hour]   Claude Code → Executes PLAN.md
5. [Every 15 min] Dashboard → Updates status
```

### Manual Override

```bash
# Force immediate execution
python3 scripts/scheduler.py --run-now plan-creator

# Skip next scheduled run
python3 scripts/scheduler.py --skip-next gmail-watcher
```

## Advanced Features

### Conditional Execution

```json
{
  "name": "urgent-check",
  "command": "python3 check-urgent.py",
  "schedule": "*/5 * * * *",
  "condition": "file_exists('../../Vault/Needs_Action/URGENT_*')"
}
```

### Chained Tasks

```json
{
  "name": "process-and-notify",
  "tasks": [
    "create-plan",
    "execute-plan",
    "update-dashboard",
    "send-summary"
  ],
  "schedule": "0 * * * *"
}
```

### Resource Limits

```json
{
  "max_concurrent_tasks": 3,
  "timeout_seconds": 300,
  "cpu_limit_percent": 50
}
```

## Monitoring & Logging

### Log Format

```
2026-03-17 10:30:00 | INFO | gmail-watcher | Started
2026-03-17 10:30:05 | INFO | gmail-watcher | Found 3 new emails
2026-03-17 10:30:10 | SUCCESS | gmail-watcher | Completed in 10s
```

### Metrics Tracked

- Task execution count
- Success/failure rate
- Average execution time
- Last run timestamp
- Next scheduled run

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Task not running | Check cron service: `systemctl status cron` |
| Permission denied | Ensure scripts are executable: `chmod +x` |
| Path not found | Use absolute paths in cron jobs |
| Task runs twice | Check for duplicate cron entries |
| Logs not created | Ensure log directory exists and is writable |

## Best Practices

1. **Use Absolute Paths**: Always use full paths in scheduled commands
2. **Log Everything**: Enable logging for all scheduled tasks
3. **Test First**: Run tasks manually before scheduling
4. **Monitor Regularly**: Check logs and task status daily
5. **Graceful Degradation**: Handle failures without breaking workflow
6. **Resource Awareness**: Don't schedule too many concurrent tasks

## Security Considerations

- Run tasks with minimum required permissions
- Secure credential files (chmod 600)
- Use environment variables for secrets
- Audit scheduled tasks regularly
- Monitor for unauthorized task additions

## Verification

Run: `python3 scripts/verify-scheduler.py`

Expected: `✓ Scheduler active, X tasks scheduled, next run in Y minutes`
