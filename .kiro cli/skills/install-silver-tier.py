#!/usr/bin/env python3
"""
Silver Tier Installation Script
"""

import os
import sys
import subprocess
from pathlib import Path

def print_header(text):
    """Print section header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def run_command(cmd, description):
    """Run shell command"""
    print(f"→ {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"  ✓ {description} complete")
        return True
    except subprocess.CalledProcessError as e:
        print(f"  ✗ {description} failed: {e}")
        return False

def check_prerequisites():
    """Check system prerequisites"""
    print_header("Checking Prerequisites")

    checks = []

    # Python version
    print("→ Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"  ✓ Python {version.major}.{version.minor}.{version.micro}")
        checks.append(True)
    else:
        print(f"  ✗ Python 3.8+ required (found {version.major}.{version.minor})")
        checks.append(False)

    # pip
    print("→ Checking pip...")
    try:
        subprocess.run(['pip3', '--version'], check=True, capture_output=True)
        print("  ✓ pip available")
        checks.append(True)
    except:
        print("  ✗ pip not found")
        checks.append(False)

    # Node.js (for Playwright)
    print("→ Checking Node.js...")
    try:
        result = subprocess.run(['node', '--version'], check=True, capture_output=True, text=True)
        print(f"  ✓ Node.js {result.stdout.strip()}")
        checks.append(True)
    except:
        print("  ✗ Node.js not found (required for Playwright)")
        checks.append(False)

    return all(checks)

def install_python_packages():
    """Install required Python packages"""
    print_header("Installing Python Packages")

    packages = [
        'google-auth-oauthlib',
        'google-auth-httplib2',
        'google-api-python-client',
        'croniter'
    ]

    for package in packages:
        run_command(f'pip3 install {package}', f'Installing {package}')

def setup_vault_structure():
    """Create vault folder structure"""
    print_header("Setting Up Vault Structure")

    vault_path = Path('../../Vault')
    folders = [
        'Needs_Action',
        'Pending_Approval',
        'Done',
        'Logs'
    ]

    for folder in folders:
        folder_path = vault_path / folder
        folder_path.mkdir(parents=True, exist_ok=True)
        print(f"  ✓ Created {folder}/")

def create_config_files():
    """Create default configuration files"""
    print_header("Creating Configuration Files")

    configs = [
        ('gmail-watcher/scripts/config.json', 'Gmail Watcher config'),
        ('whatsapp-watcher/scripts/whatsapp-config.json', 'WhatsApp Watcher config'),
        ('plan-creator/scripts/plan-config.json', 'Plan Creator config'),
        ('linkedin-automation/scripts/linkedin-config.json', 'LinkedIn config'),
        ('email-sender/scripts/email-config.json', 'Email Sender config'),
        ('task-scheduler/scripts/scheduler-config.json', 'Scheduler config')
    ]

    for config_path, description in configs:
        if Path(config_path).exists():
            print(f"  ✓ {description} exists")
        else:
            print(f"  ⚠ {description} not found - using defaults")

def make_scripts_executable():
    """Make shell scripts executable"""
    print_header("Making Scripts Executable")

    script_patterns = [
        '**/*.sh'
    ]

    for pattern in script_patterns:
        for script in Path('.').glob(pattern):
            os.chmod(script, 0o755)
            print(f"  ✓ {script}")

def print_next_steps():
    """Print next steps for user"""
    print_header("Installation Complete!")

    print("""
Next Steps:

1. Setup Gmail API:
   cd gmail-watcher/scripts
   bash setup-gmail.sh

2. Setup WhatsApp (optional):
   cd whatsapp-watcher/scripts
   python3 whatsapp-watcher.py --authenticate

3. Start Email MCP Server:
   cd email-sender/scripts
   bash start-email-server.sh

4. Configure Scheduler:
   cd task-scheduler/scripts
   # Edit scheduler-config.json
   python3 scheduler.py

5. Test the system:
   # Place a test file in Vault/Needs_Action/
   cd plan-creator/scripts
   python3 create-plan.py

For detailed documentation, see:
- SILVER_TIER_README.md
- Individual SKILL.md files in each skill directory

Happy automating! 🚀
""")

def main():
    print("""
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║        Silver Tier Installation Script                  ║
║        AI Employee - Functional Assistant                ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
""")

    if not check_prerequisites():
        print("\n✗ Prerequisites check failed. Please install missing components.")
        sys.exit(1)

    install_python_packages()
    setup_vault_structure()
    create_config_files()
    make_scripts_executable()
    print_next_steps()

if __name__ == '__main__':
    main()
