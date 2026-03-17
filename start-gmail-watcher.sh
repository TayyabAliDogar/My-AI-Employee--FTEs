#!/bin/bash
# SILVER TIER - START YOUR AI EMPLOYEE
# Run this script to start monitoring Gmail

echo "╔══════════════════════════════════════════════════════════╗"
echo "║                                                          ║"
echo "║     SILVER TIER - START YOUR AI EMPLOYEE                 ║"
echo "║                                                          ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Navigate to Gmail watcher
cd "My-AI-Employee -FTEs/.kiro cli/skills/gmail-watcher/scripts" || {
    echo "✗ Error: Could not find Gmail watcher directory"
    exit 1
}

echo "Current directory: $(pwd)"
echo ""

# Check files
echo "Checking installation..."
echo ""

if [ -f "gmail-watcher.py" ]; then
    echo "✓ Gmail watcher script found"
else
    echo "✗ Gmail watcher script not found"
    exit 1
fi

if [ -f "credentials.json" ]; then
    echo "✓ credentials.json found"
else
    echo "✗ credentials.json not found"
    exit 1
fi

if [ -f "config.json" ]; then
    echo "✓ config.json found"
else
    echo "✗ config.json not found"
    exit 1
fi

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "  Starting Gmail Watcher"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "This will:"
echo "  1. Authenticate with Gmail (opens browser)"
echo "  2. Fetch unread emails"
echo "  3. Create action files in Vault/Needs_Action/"
echo "  4. Monitor continuously (press Ctrl+C to stop)"
echo ""
echo "Press Enter to start or Ctrl+C to cancel..."
read

# Start Gmail watcher
python3 gmail-watcher.py

echo ""
echo "Gmail watcher stopped."
echo ""
