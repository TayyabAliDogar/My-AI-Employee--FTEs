#!/bin/bash
# Setup script for Gmail Watcher

echo "=== Gmail Watcher Setup ==="
echo ""

# Check Python version
python3 --version || { echo "Error: Python 3 not found"; exit 1; }

# Install required packages
echo "Installing required Python packages..."
pip3 install google-auth-oauthlib google-auth-httplib2 google-api-python-client

# Check for credentials file
if [ ! -f "credentials.json" ]; then
    echo ""
    echo "⚠️  credentials.json not found!"
    echo ""
    echo "Please follow these steps:"
    echo "1. Go to https://console.cloud.google.com/"
    echo "2. Create a new project or select existing"
    echo "3. Enable Gmail API"
    echo "4. Create OAuth 2.0 credentials"
    echo "5. Download credentials and save as 'credentials.json' in this directory"
    echo ""
    exit 1
fi

# Run authentication
echo ""
echo "Starting authentication process..."
echo "A browser window will open for Google OAuth consent"
echo ""

python3 gmail-watcher.py --authenticate

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ Gmail Watcher setup complete!"
    echo ""
    echo "You can now run:"
    echo "  python3 gmail-watcher.py"
    echo ""
else
    echo ""
    echo "✗ Setup failed. Please check the error messages above."
    exit 1
fi
