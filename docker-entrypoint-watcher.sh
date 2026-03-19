#!/bin/bash
set -e

echo "Starting ${WATCHER_TYPE} watcher..."

case "${WATCHER_TYPE}" in
  gmail)
    cd /app/watcher/scripts
    python gmail-watcher.py
    ;;
  instagram)
    cd /app/watcher/scripts
    python instagram-watcher.py
    ;;
  facebook)
    cd /app/watcher/scripts
    python facebook-watcher.py
    ;;
  twitter)
    cd /app/watcher/scripts
    python twitter-watcher.py
    ;;
  linkedin)
    cd /app/watcher/scripts
    python linkedin-watcher.py
    ;;
  *)
    echo "Unknown watcher type: ${WATCHER_TYPE}"
    exit 1
    ;;
esac
