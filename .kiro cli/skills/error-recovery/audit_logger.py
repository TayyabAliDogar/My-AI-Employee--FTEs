import os
import sys
import json
import traceback
from datetime import datetime
from pathlib import Path
from enum import Enum

class LogLevel(Enum):
    """Log severity levels"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class AuditLogger:
    """
    Comprehensive audit logging system for AI Employee

    Features:
    - Structured logging with severity levels
    - Automatic error recovery
    - Graceful degradation
    - Audit trail for all operations
    """

    def __init__(self, component_name, log_dir=None):
        """
        Initialize audit logger

        Args:
            component_name: Name of the component (e.g., 'instagram-watcher')
            log_dir: Directory for log files (default: Vault/Logs)
        """
        self.component_name = component_name

        if log_dir:
            self.log_dir = Path(log_dir)
        else:
            # Default to Vault/Logs
            vault_dir = Path(__file__).parent.parent.parent.parent / "Vault"
            self.log_dir = vault_dir / "Logs"

        self.log_dir.mkdir(parents=True, exist_ok=True)

        # Create component-specific log file
        self.log_file = self.log_dir / f"{component_name}-{datetime.now().strftime('%Y-%m-%d')}.log"

        # Create audit trail file
        self.audit_file = self.log_dir / f"audit-{datetime.now().strftime('%Y-%m')}.log"

        # Error recovery state
        self.error_count = 0
        self.max_errors = 10
        self.recovery_strategies = []

    def log(self, message, level=LogLevel.INFO, metadata=None):
        """
        Log a message with metadata

        Args:
            message: Log message
            level: Log severity level
            metadata: Additional context (dict)
        """
        timestamp = datetime.now().isoformat()

        log_entry = {
            'timestamp': timestamp,
            'component': self.component_name,
            'level': level.value,
            'message': message,
            'metadata': metadata or {}
        }

        # Format for file
        log_line = f"[{timestamp}] [{level.value}] [{self.component_name}] {message}"
        if metadata:
            log_line += f" | {json.dumps(metadata)}"

        # Write to log file
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_line + "\n")
        except Exception as e:
            print(f"Failed to write log: {e}")

        # Write to audit trail for important events
        if level in [LogLevel.WARNING, LogLevel.ERROR, LogLevel.CRITICAL]:
            try:
                with open(self.audit_file, 'a', encoding='utf-8') as f:
                    f.write(json.dumps(log_entry) + "\n")
            except Exception as e:
                print(f"Failed to write audit: {e}")

        # Print to console
        if level == LogLevel.ERROR or level == LogLevel.CRITICAL:
            print(f"❌ {log_line}")
        elif level == LogLevel.WARNING:
            print(f"⚠️  {log_line}")
        else:
            print(log_line)

    def debug(self, message, **metadata):
        """Log debug message"""
        self.log(message, LogLevel.DEBUG, metadata)

    def info(self, message, **metadata):
        """Log info message"""
        self.log(message, LogLevel.INFO, metadata)

    def warning(self, message, **metadata):
        """Log warning message"""
        self.log(message, LogLevel.WARNING, metadata)

    def error(self, message, **metadata):
        """Log error message"""
        self.error_count += 1
        self.log(message, LogLevel.ERROR, metadata)

    def critical(self, message, **metadata):
        """Log critical message"""
        self.error_count += 1
        self.log(message, LogLevel.CRITICAL, metadata)

    def log_exception(self, exception, context=None):
        """
        Log an exception with full traceback

        Args:
            exception: Exception object
            context: Additional context about where error occurred
        """
        tb = traceback.format_exc()

        metadata = {
            'exception_type': type(exception).__name__,
            'exception_message': str(exception),
            'traceback': tb,
            'context': context
        }

        self.error(f"Exception occurred: {exception}", **metadata)

    def should_continue(self):
        """
        Check if component should continue running

        Returns:
            bool: True if should continue, False if too many errors
        """
        if self.error_count >= self.max_errors:
            self.critical(f"Maximum error count ({self.max_errors}) reached. Stopping component.")
            return False
        return True

    def reset_error_count(self):
        """Reset error counter after successful operation"""
        if self.error_count > 0:
            self.info(f"Resetting error count (was {self.error_count})")
            self.error_count = 0

    def add_recovery_strategy(self, strategy_func, description):
        """
        Add an error recovery strategy

        Args:
            strategy_func: Function to call for recovery
            description: Description of the strategy
        """
        self.recovery_strategies.append({
            'func': strategy_func,
            'description': description
        })

    def attempt_recovery(self):
        """
        Attempt to recover from errors using registered strategies

        Returns:
            bool: True if recovery successful
        """
        self.warning("Attempting error recovery...")

        for strategy in self.recovery_strategies:
            try:
                self.info(f"Trying recovery strategy: {strategy['description']}")
                result = strategy['func']()

                if result:
                    self.info(f"Recovery successful: {strategy['description']}")
                    self.reset_error_count()
                    return True
                else:
                    self.warning(f"Recovery strategy failed: {strategy['description']}")

            except Exception as e:
                self.log_exception(e, f"Recovery strategy failed: {strategy['description']}")

        self.error("All recovery strategies failed")
        return False

class ErrorRecoveryMixin:
    """
    Mixin class to add error recovery capabilities to watchers

    Usage:
        class MyWatcher(ErrorRecoveryMixin):
            def __init__(self):
                self.setup_error_recovery('my-watcher')
    """

    def setup_error_recovery(self, component_name):
        """Initialize error recovery system"""
        self.logger = AuditLogger(component_name)

        # Add default recovery strategies
        self.logger.add_recovery_strategy(
            self._reconnect_strategy,
            "Reconnect to services"
        )

        self.logger.add_recovery_strategy(
            self._clear_cache_strategy,
            "Clear cache and retry"
        )

    def _reconnect_strategy(self):
        """Default reconnection strategy"""
        try:
            if hasattr(self, 'connect'):
                self.logger.info("Attempting to reconnect...")
                return self.connect()
            return False
        except Exception as e:
            self.logger.log_exception(e, "Reconnection failed")
            return False

    def _clear_cache_strategy(self):
        """Default cache clearing strategy"""
        try:
            if hasattr(self, 'clear_cache'):
                self.logger.info("Clearing cache...")
                self.clear_cache()
                return True
            return False
        except Exception as e:
            self.logger.log_exception(e, "Cache clearing failed")
            return False

    def safe_execute(self, func, *args, **kwargs):
        """
        Execute a function with error recovery

        Args:
            func: Function to execute
            *args, **kwargs: Arguments for the function

        Returns:
            Result of function or None if failed
        """
        try:
            result = func(*args, **kwargs)
            self.logger.reset_error_count()
            return result

        except Exception as e:
            self.logger.log_exception(e, f"Error in {func.__name__}")

            # Attempt recovery
            if self.logger.attempt_recovery():
                # Retry after successful recovery
                try:
                    return func(*args, **kwargs)
                except Exception as retry_error:
                    self.logger.log_exception(retry_error, f"Retry failed for {func.__name__}")

            return None

    def graceful_degradation(self, primary_func, fallback_func, *args, **kwargs):
        """
        Execute primary function with fallback

        Args:
            primary_func: Primary function to try
            fallback_func: Fallback function if primary fails
            *args, **kwargs: Arguments for functions

        Returns:
            Result from primary or fallback function
        """
        try:
            result = primary_func(*args, **kwargs)
            self.logger.info(f"Primary function succeeded: {primary_func.__name__}")
            return result

        except Exception as e:
            self.logger.warning(f"Primary function failed, using fallback: {primary_func.__name__}")
            self.logger.log_exception(e, f"Primary function error: {primary_func.__name__}")

            try:
                result = fallback_func(*args, **kwargs)
                self.logger.info(f"Fallback function succeeded: {fallback_func.__name__}")
                return result

            except Exception as fallback_error:
                self.logger.error(f"Fallback function also failed: {fallback_func.__name__}")
                self.logger.log_exception(fallback_error, f"Fallback error: {fallback_func.__name__}")
                return None

def create_audit_report(log_dir=None, days=7):
    """
    Generate audit report from logs

    Args:
        log_dir: Directory containing logs
        days: Number of days to include

    Returns:
        dict: Audit report
    """
    if log_dir:
        logs_path = Path(log_dir)
    else:
        vault_dir = Path(__file__).parent.parent.parent.parent / "Vault"
        logs_path = vault_dir / "Logs"

    if not logs_path.exists():
        return {'error': 'Log directory not found'}

    # Collect statistics
    stats = {
        'total_logs': 0,
        'by_level': {level.value: 0 for level in LogLevel},
        'by_component': {},
        'errors': [],
        'warnings': []
    }

    cutoff_date = datetime.now() - timedelta(days=days)

    # Parse audit logs
    for audit_file in logs_path.glob("audit-*.log"):
        try:
            with open(audit_file, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        entry = json.loads(line.strip())

                        # Check date
                        log_date = datetime.fromisoformat(entry['timestamp'])
                        if log_date < cutoff_date:
                            continue

                        stats['total_logs'] += 1

                        # Count by level
                        level = entry.get('level', 'INFO')
                        stats['by_level'][level] = stats['by_level'].get(level, 0) + 1

                        # Count by component
                        component = entry.get('component', 'unknown')
                        stats['by_component'][component] = stats['by_component'].get(component, 0) + 1

                        # Collect errors and warnings
                        if level == 'ERROR' or level == 'CRITICAL':
                            stats['errors'].append(entry)
                        elif level == 'WARNING':
                            stats['warnings'].append(entry)

                    except json.JSONDecodeError:
                        continue

        except Exception as e:
            print(f"Error reading {audit_file}: {e}")

    return stats

if __name__ == "__main__":
    # Test the audit logger
    logger = AuditLogger("test-component")

    logger.info("Starting test")
    logger.debug("Debug message", test_data="value")
    logger.warning("Warning message", issue="something")
    logger.error("Error message", error_code=500)

    try:
        raise ValueError("Test exception")
    except Exception as e:
        logger.log_exception(e, "Testing exception logging")

    print("\n" + "=" * 60)
    print("Audit Logger Test Complete")
    print(f"Log file: {logger.log_file}")
    print(f"Audit file: {logger.audit_file}")
    print("=" * 60)
