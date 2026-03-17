#!/bin/bash
# Start Email MCP Server

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

PORT=8809

# Check if already running
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "Email MCP Server is already running on port $PORT"
    exit 1
fi

# Start server in background
nohup python3 email-mcp-server.py --port $PORT > ../../Vault/Logs/email-server.log 2>&1 &

PID=$!
echo "Email MCP Server started (PID: $PID)"
echo "Port: $PORT"
echo "Logs: ../../Vault/Logs/email-server.log"

# Wait a moment and verify it started
sleep 2

if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "✓ Server is running"
else
    echo "✗ Server failed to start - check logs"
    exit 1
fi
