#!/bin/bash
# Start Gmail Watcher in background

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check if already running
if pgrep -f "gmail-watcher.py" > /dev/null; then
    echo "Gmail Watcher is already running"
    exit 1
fi

# Start watcher in background
nohup python3 gmail-watcher.py > ../../Vault/Logs/gmail-watcher.log 2>&1 &

PID=$!
echo "Gmail Watcher started (PID: $PID)"
echo "Logs: ../../Vault/Logs/gmail-watcher.log"
