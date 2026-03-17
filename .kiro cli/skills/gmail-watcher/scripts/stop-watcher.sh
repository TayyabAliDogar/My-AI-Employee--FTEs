#!/bin/bash
# Stop Gmail Watcher

if pgrep -f "gmail-watcher.py" > /dev/null; then
    pkill -f "gmail-watcher.py"
    echo "✓ Gmail Watcher stopped"
else
    echo "Gmail Watcher is not running"
fi
