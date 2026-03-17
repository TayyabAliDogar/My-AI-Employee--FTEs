#!/usr/bin/env python3
"""
Task Scheduler - Cross-platform task scheduling
"""

import os
import json
import time
import logging
import subprocess
from datetime import datetime
from pathlib import Path
from croniter import croniter

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('TaskScheduler')

class TaskScheduler:
    def __init__(self, config_path='scheduler-config.json'):
        self.config = self.load_config(config_path)
        self.tasks = self.config.get('tasks', [])
        self.running = False

    def load_config(self, config_path):
        """Load configuration"""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"Config file not found: {config_path}")
            return {'tasks': []}

    def get_next_run_time(self, cron_expression):
        """Calculate next run time from cron expression"""
        try:
            cron = croniter(cron_expression, datetime.now())
            return cron.get_next(datetime)
        except Exception as e:
            logger.error(f"Invalid cron expression: {cron_expression} - {e}")
            return None

    def should_run_task(self, task):
        """Check if task should run now"""
        if not task.get('enabled', True):
            return False

        cron_expression = task.get('schedule')
        if not cron_expression:
            return False

        try:
            cron = croniter(cron_expression, datetime.now())
            # Check if current time matches schedule (within 1 minute)
            next_run = cron.get_prev(datetime)
            time_diff = (datetime.now() - next_run).total_seconds()

            return 0 <= time_diff < 60

        except Exception as e:
            logger.error(f"Error checking schedule for {task['name']}: {e}")
            return False

    def run_task(self, task):
        """Execute a task"""
        task_name = task.get('name', 'Unknown')
        command = task.get('command')

        if not command:
            logger.error(f"No command specified for task: {task_name}")
            return False

        logger.info(f"Running task: {task_name}")
        start_time = time.time()

        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=task.get('timeout', 300)
            )

            duration = time.time() - start_time

            if result.returncode == 0:
                logger.info(f"✓ Task completed: {task_name} ({duration:.1f}s)")
                return True
            else:
                logger.error(f"✗ Task failed: {task_name} - {result.stderr}")
                return False

        except subprocess.TimeoutExpired:
            logger.error(f"✗ Task timeout: {task_name}")
            return False
        except Exception as e:
            logger.error(f"✗ Task error: {task_name} - {e}")
            return False

    def list_tasks(self):
        """List all scheduled tasks"""
        print("\nScheduled Tasks:\n")

        for task in self.tasks:
            name = task.get('name', 'Unknown')
            schedule = task.get('schedule', 'N/A')
            enabled = task.get('enabled', True)
            status = "✓ Enabled" if enabled else "✗ Disabled"

            next_run = self.get_next_run_time(schedule) if enabled else None
            next_run_str = next_run.strftime('%Y-%m-%d %H:%M:%S') if next_run else 'N/A'

            print(f"- {name}")
            print(f"  Schedule: {schedule}")
            print(f"  Status: {status}")
            print(f"  Next Run: {next_run_str}")
            print()

    def run_scheduler(self):
        """Main scheduler loop"""
        logger.info("Task Scheduler started")
        logger.info(f"Monitoring {len(self.tasks)} task(s)")

        self.running = True

        try:
            while self.running:
                for task in self.tasks:
                    if self.should_run_task(task):
                        self.run_task(task)

                # Check every minute
                time.sleep(60)

        except KeyboardInterrupt:
            logger.info("Scheduler stopped by user")
            self.running = False

def main():
    import argparse

    parser = argparse.ArgumentParser(description='Task Scheduler')
    parser.add_argument('--config', default='scheduler-config.json', help='Config file path')
    parser.add_argument('--list', action='store_true', help='List scheduled tasks')
    parser.add_argument('--daemon', action='store_true', help='Run as daemon')

    args = parser.parse_args()

    scheduler = TaskScheduler(config_path=args.config)

    if args.list:
        scheduler.list_tasks()
    else:
        scheduler.run_scheduler()

if __name__ == '__main__':
    main()
