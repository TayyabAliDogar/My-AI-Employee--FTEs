#!/usr/bin/env python3
"""
Quick Start Script for Silver Tier
"""

import os
import sys
import subprocess
from pathlib import Path

def print_banner():
    print("""
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║           Silver Tier - Quick Start Guide               ║
║           AI Employee - Functional Assistant             ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
""")

def print_step(number, title):
    print(f"\n{'='*60}")
    print(f"  STEP {number}: {title}")
    print('='*60)

def run_command(cmd, description):
    print(f"\n→ {description}")
    print(f"  Command: {cmd}")
    response = input("  Run this command? (y/n): ")

    if response.lower() == 'y':
        try:
            subprocess.run(cmd, shell=True, check=True)
            print("  ✓ Success")
            return True
        except subprocess.CalledProcessError as e:
            print(f"  ✗ Failed: {e}")
            return False
    else:
        print("  ⊘ Skipped")
        return False

def main():
    print_banner()

    print("""
This script will guide you through setting up Silver Tier skills.

You can skip any step if you've already completed it or want to do it manually.
""")

    input("Press Enter to continue...")

    # Step 1: Check Prerequisites
    print_step(1, "Check Prerequisites")
    print("""
Required:
- Python 3.8+
- pip3
- Node.js (for Playwright)
- Gmail API credentials (credentials.json)
""")

    response = input("\nDo you have all prerequisites? (y/n): ")
    if response.lower() != 'y':
        print("\nPlease install prerequisites first:")
        print("- Python: https://python.org")
        print("- Node.js: https://nodejs.org")
        print("- Gmail API: https://console.cloud.google.com")
        sys.exit(1)

    # Step 2: Install Python Packages
    print_step(2, "Install Python Packages")
    run_command(
        'pip3 install google-auth-oauthlib google-auth-httplib2 google-api-python-client croniter',
        'Installing required Python packages'
    )

    # Step 3: Setup Vault Structure
    print_step(3, "Setup Vault Structure")
    vault_path = Path('../../Vault')
    folders = ['Needs_Action', 'Pending_Approval', 'Done', 'Logs']

    for folder in folders:
        folder_path = vault_path / folder
        folder_path.mkdir(parents=True, exist_ok=True)
        print(f"  ✓ Created {folder}/")

    # Step 4: Setup Gmail
    print_step(4, "Setup Gmail Watcher")
    print("\nThis will authenticate with Gmail API.")
    print("Make sure you have credentials.json in gmail-watcher/scripts/")

    if run_command(
        'cd gmail-watcher/scripts && bash setup-gmail.sh',
        'Setting up Gmail authentication'
    ):
        print("\n  ✓ Gmail setup complete")

    # Step 5: Start Playwright
    print_step(5, "Start Playwright MCP Server")
    print("\nPlaywright is required for WhatsApp and LinkedIn automation.")

    run_command(
        'cd browsing-with-playwright/scripts && bash start-server.sh',
        'Starting Playwright MCP server'
    )

    # Step 6: Start Email Server
    print_step(6, "Start Email MCP Server")
    print("\nEmail server enables sending emails via Gmail API.")

    run_command(
        'cd email-sender/scripts && bash start-email-server.sh',
        'Starting Email MCP server'
    )

    # Step 7: Configure Scheduler
    print_step(7, "Configure Task Scheduler")
    print("\nThe scheduler automates periodic tasks.")
    print("You can edit scheduler-config.json to customize schedules.")

    response = input("\nStart scheduler now? (y/n): ")
    if response.lower() == 'y':
        run_command(
            'cd task-scheduler/scripts && python3 scheduler.py &',
            'Starting task scheduler'
        )

    # Step 8: Test System
    print_step(8, "Test the System")
    print("""
To test the system:

1. Create a test file in Vault/Needs_Action/
   Example: echo "Test task" > ../../Vault/Needs_Action/test.txt

2. Generate a plan:
   cd plan-creator/scripts && python3 create-plan.py

3. Check PLAN.md was created:
   cat ../../Vault/Needs_Action/PLAN.md

4. Execute with Claude Code:
   claude-code "Execute the plan in Vault/Needs_Action/PLAN.md"
""")

    # Final Summary
    print("\n" + "="*60)
    print("  SETUP COMPLETE!")
    print("="*60)

    print("""
Your Silver Tier AI Employee is ready!

Running Services:
- Playwright MCP Server (port 8808)
- Email MCP Server (port 8809)
- Task Scheduler (background)

Next Steps:
1. Review SILVER_TIER_README.md for detailed documentation
2. Customize configuration files for your needs
3. Test each skill individually
4. Setup automated schedules
5. Monitor Vault/Logs/ for system activity

For help:
- Documentation: SILVER_TIER_README.md
- Structure: SILVER_TIER_STRUCTURE.md
- Individual skills: Each SKILL.md file

Happy automating! 🚀
""")

if __name__ == '__main__':
    main()
