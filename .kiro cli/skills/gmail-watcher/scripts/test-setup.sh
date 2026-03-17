#!/bin/bash
# Test Gmail Watcher Setup

echo "==================================="
echo "Gmail Watcher - Setup Test"
echo "==================================="
echo ""

# Check Python
echo "→ Checking Python..."
python3 --version || { echo "✗ Python 3 not found"; exit 1; }
echo "✓ Python available"
echo ""

# Check credentials.json
echo "→ Checking credentials.json..."
if [ -f "credentials.json" ]; then
    echo "✓ credentials.json found"
else
    echo "✗ credentials.json not found!"
    echo "Please copy your Gmail API credentials to this directory"
    exit 1
fi
echo ""

# Check required packages
echo "→ Checking required Python packages..."
python3 -c "import google.auth" 2>/dev/null || { echo "✗ google-auth not installed"; echo "Run: pip3 install google-auth-oauthlib google-auth-httplib2 google-api-python-client"; exit 1; }
echo "✓ Required packages installed"
echo ""

# Check Vault directory
echo "→ Checking Vault directory..."
if [ -d "../../../Vault" ]; then
    echo "✓ Vault directory found"
else
    echo "⚠ Vault directory not found at ../../../Vault"
    echo "Creating Vault structure..."
    mkdir -p "../../../Vault/Needs_Action"
    mkdir -p "../../../Vault/Pending_Approval"
    mkdir -p "../../../Vault/Done"
    mkdir -p "../../../Vault/Logs"
    echo "✓ Vault structure created"
fi
echo ""

# Test authentication
echo "→ Testing Gmail authentication..."
echo "This will open a browser window for OAuth consent"
echo "Press Enter to continue or Ctrl+C to cancel..."
read

python3 gmail-watcher.py --once

if [ $? -eq 0 ]; then
    echo ""
    echo "==================================="
    echo "✓ Gmail Watcher Setup Complete!"
    echo "==================================="
    echo ""
    echo "You can now run:"
    echo "  python3 gmail-watcher.py          # Continuous monitoring"
    echo "  python3 gmail-watcher.py --once   # Single check"
    echo ""
else
    echo ""
    echo "✗ Setup failed. Please check the errors above."
    exit 1
fi
