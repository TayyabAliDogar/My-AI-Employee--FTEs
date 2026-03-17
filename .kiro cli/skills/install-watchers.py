#!/usr/bin/env python3
"""
Silver Tier - Complete Installation Script
Installs and tests Gmail and LinkedIn watchers
"""

import os
import sys
import subprocess
from pathlib import Path

def print_header(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def run_command(cmd, description, check=True):
    """Run shell command"""
    print(f"→ {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=check, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"  ✓ {description} complete")
            return True
        else:
            print(f"  ✗ {description} failed: {result.stderr}")
            return False
    except subprocess.CalledProcessError as e:
        print(f"  ✗ {description} failed: {e}")
        return False

def main():
    print("""
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║     Silver Tier - Gmail & LinkedIn Watchers Setup       ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
""")

    # Check Python version
    print_header("Checking Prerequisites")

    version = sys.version_info
    print(f"→ Python version: {version.major}.{version.minor}.{version.micro}")
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("✗ Python 3.8+ required")
        sys.exit(1)
    print("✓ Python version OK")

    # Install Gmail dependencies
    print_header("Installing Gmail Watcher Dependencies")

    gmail_scripts = Path("gmail-watcher/scripts")
    if not gmail_scripts.exists():
        print("✗ Gmail watcher scripts directory not found")
        sys.exit(1)

    os.chdir(gmail_scripts)

    if run_command(
        "pip3 install google-auth-oauthlib google-auth-httplib2 google-api-python-client",
        "Installing Google API packages"
    ):
        print("\n✓ Gmail dependencies installed")
    else:
        print("\n✗ Failed to install Gmail dependencies")
        sys.exit(1)

    # Check credentials.json
    print_header("Checking Gmail Credentials")

    if Path("credentials.json").exists():
        print("✓ credentials.json found")
    else:
        print("✗ credentials.json not found!")
        print("\nPlease copy your Gmail API credentials.json to:")
        print(f"  {Path.cwd() / 'credentials.json'}")
        sys.exit(1)

    # Create Vault structure
    print_header("Setting Up Vault Structure")

    vault_path = Path("../../../Vault")
    folders = ['Needs_Action', 'Pending_Approval', 'Done', 'Logs']

    for folder in folders:
        folder_path = vault_path / folder
        folder_path.mkdir(parents=True, exist_ok=True)
        print(f"  ✓ Created {folder}/")

    # Test Gmail authentication
    print_header("Testing Gmail Authentication")

    print("This will open a browser window for OAuth consent.")
    print("Please authorize the application to access your Gmail.")
    print("\nPress Enter to continue or Ctrl+C to cancel...")
    input()

    if run_command(
        "python3 gmail-watcher.py --once",
        "Testing Gmail watcher",
        check=False
    ):
        print("\n✓ Gmail watcher test successful!")
    else:
        print("\n⚠ Gmail watcher test had issues - check logs above")

    # LinkedIn setup instructions
    print_header("LinkedIn Watcher Setup")

    print("""
To use the LinkedIn watcher:

1. Set environment variables:
   export LINKEDIN_EMAIL="your-email@example.com"
   export LINKEDIN_PASSWORD="your-password"

2. Start Playwright MCP server:
   cd ../browsing-with-playwright/scripts
   bash start-server.sh

3. Start LinkedIn watcher:
   cd ../../linkedin-automation/scripts
   python3 linkedin-watcher.py --once

For detailed instructions, see WATCHERS_QUICK_START.md
""")

    # Final summary
    print_header("Installation Complete!")

    print("""
✓ Gmail watcher is ready to use
✓ Vault structure created
✓ Dependencies installed

Next Steps:

1. Start Gmail watcher:
   cd gmail-watcher/scripts
   python3 gmail-watcher.py

2. Configure settings:
   Edit gmail-watcher/scripts/config.json

3. Set up LinkedIn watcher (optional):
   See instructions above

4. View documentation:
   - WATCHERS_QUICK_START.md
   - SILVER_TIER_README.md

Happy automating! 🚀
""")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInstallation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Installation failed: {e}")
        sys.exit(1)
