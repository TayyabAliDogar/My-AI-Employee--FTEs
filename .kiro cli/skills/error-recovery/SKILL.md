# Error Recovery & Audit Logging

## Overview
Comprehensive error recovery and audit logging system for the AI Employee. Provides graceful degradation, automatic recovery, and complete audit trails.

## Features
- ✅ Structured logging with severity levels
- ✅ Automatic error recovery strategies
- ✅ Graceful degradation with fallbacks
- ✅ Complete audit trail
- ✅ Error count tracking
- ✅ Recovery attempt logging
- ✅ Exception tracking with full tracebacks
- ✅ Component-specific logging
- ✅ Monthly audit reports

## Installation

### Prerequisites
```bash
pip install python-dotenv
```

## Usage

### Basic Logging
```python
from audit_logger import AuditLogger, LogLevel

logger = AuditLogger("my-component")

logger.info("Operation started")
logger.warning("Potential issue detected")
logger.error("Operation failed")
logger.critical("System failure")
```

### Exception Logging
```python
try:
    risky_operation()
except Exception as e:
    logger.log_exception(e, "Context about the operation")
```

### Error Recovery Mixin
```python
from audit_logger import ErrorRecoveryMixin

class MyWatcher(ErrorRecoveryMixin):
    def __init__(self):
        self.setup_error_recovery('my-watcher')

    def fetch_data(self):
        # Automatically handles errors and recovery
        return self.safe_execute(self._fetch_data_internal)

    def _fetch_data_internal(self):
        # Your actual implementation
        pass
```

### Graceful Degradation
```python
class MyService(ErrorRecoveryMixin):
    def get_data(self):
        # Try primary API, fallback to cache
        return self.graceful_degradation(
            self.fetch_from_api,
            self.fetch_from_cache
        )
```

## Log Levels

- **DEBUG**: Detailed diagnostic information
- **INFO**: General informational messages
- **WARNING**: Warning messages for potential issues
- **ERROR**: Error messages for failures
- **CRITICAL**: Critical failures requiring immediate attention

## Log Files

### Component Logs
Location: `Vault/Logs/{component}-{date}.log`

Format:
```
[2026-03-19T12:30:00] [INFO] [instagram-watcher] Fetching messages...
[2026-03-19T12:30:05] [ERROR] [instagram-watcher] API request failed | {"error_code": 429}
```

### Audit Trail
Location: `Vault/Logs/audit-{month}.log`

Format: JSON lines
```json
{
  "timestamp": "2026-03-19T12:30:00",
  "component": "instagram-watcher",
  "level": "ERROR",
  "message": "API request failed",
  "metadata": {"error_code": 429}
}
```

## Error Recovery Strategies

### Default Strategies

1. **Reconnect Strategy**
   - Attempts to reconnect to services
   - Useful for network failures
   - Automatically retries connection

2. **Clear Cache Strategy**
   - Clears cached data
   - Forces fresh data fetch
   - Resolves stale data issues

### Custom Strategies

```python
logger = AuditLogger("my-component")

def custom_recovery():
    # Your recovery logic
    return True  # Return True if successful

logger.add_recovery_strategy(
    custom_recovery,
    "Custom recovery description"
)
```

## Error Count Tracking

The system tracks consecutive errors:
- Maximum errors: 10 (configurable)
- Auto-reset on successful operation
- Stops component if max errors reached

```python
if not logger.should_continue():
    # Too many errors, stop component
    sys.exit(1)
```

## Audit Reports

Generate audit reports from logs:

```python
from audit_logger import create_audit_report

report = create_audit_report(days=7)

print(f"Total logs: {report['total_logs']}")
print(f"Errors: {report['by_level']['ERROR']}")
print(f"Warnings: {report['by_level']['WARNING']}")
```

## Integration Examples

### Instagram Watcher with Error Recovery

```python
from audit_logger import ErrorRecoveryMixin

class InstagramWatcher(ErrorRecoveryMixin):
    def __init__(self):
        self.setup_error_recovery('instagram-watcher')

        # Add custom recovery
        self.logger.add_recovery_strategy(
            self.refresh_token,
            "Refresh Instagram access token"
        )

    def watch(self):
        while self.logger.should_continue():
            # Safe execution with auto-recovery
            messages = self.safe_execute(self.fetch_messages)

            if messages:
                self.process_messages(messages)

            time.sleep(300)
```

### Odoo MCP with Graceful Degradation

```python
class OdooMCPServer(ErrorRecoveryMixin):
    def __init__(self):
        self.setup_error_recovery('odoo-mcp')

    def get_revenue(self):
        # Try live data, fallback to cached
        return self.graceful_degradation(
            self.fetch_live_revenue,
            self.fetch_cached_revenue
        )
```

## Best Practices

1. **Log at Appropriate Levels**
   - Use DEBUG for detailed diagnostics
   - Use INFO for normal operations
   - Use WARNING for potential issues
   - Use ERROR for failures
   - Use CRITICAL for system failures

2. **Include Context**
   - Add metadata to log entries
   - Include relevant IDs and values
   - Provide context for debugging

3. **Handle Exceptions Properly**
   - Always log exceptions with context
   - Use log_exception() for full tracebacks
   - Don't swallow exceptions silently

4. **Implement Recovery Strategies**
   - Add component-specific recovery
   - Test recovery strategies
   - Log recovery attempts

5. **Monitor Error Counts**
   - Check should_continue() regularly
   - Stop components gracefully
   - Alert on high error rates

## Monitoring

### Check Recent Errors
```bash
# View recent errors
tail -f Vault/Logs/instagram-watcher-2026-03-19.log | grep ERROR

# Count errors by component
grep ERROR Vault/Logs/*.log | cut -d: -f1 | sort | uniq -c
```

### Audit Report
```bash
python -c "from audit_logger import create_audit_report; import json; print(json.dumps(create_audit_report(days=7), indent=2))"
```

## Gold Tier Requirement

This skill is CRITICAL for Gold Tier:
- ✅ Error recovery (required)
- ✅ Graceful degradation (required)
- ✅ Comprehensive audit logging (required)
- ✅ Production-ready reliability

## Troubleshooting

### Logs Not Being Created
- Check Vault/Logs directory exists
- Verify write permissions
- Check disk space

### Recovery Not Working
- Verify recovery strategies are registered
- Check recovery function returns boolean
- Review error logs for details

### High Error Counts
- Review audit trail for patterns
- Check external service status
- Verify credentials and configuration

---

*Part of Gold Tier AI Employee Implementation*
*Production-Ready Error Handling & Audit System*
*Built with Claude Code - March 2026*
