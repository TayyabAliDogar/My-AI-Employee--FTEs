#!/bin/bash
# Stop Email MCP Server

PORT=8809

if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
    PID=$(lsof -Pi :$PORT -sTCP:LISTEN -t)
    kill $PID
    echo "✓ Email MCP Server stopped (PID: $PID)"
else
    echo "Email MCP Server is not running"
fi
