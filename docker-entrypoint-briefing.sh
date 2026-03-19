#!/bin/bash
set -e

echo "Setting up CEO Briefing Generator..."
echo "Schedule: ${SCHEDULE}"

# Create cron job
echo "${SCHEDULE} cd /app/briefing/scripts && python ceo-briefing-generator.py >> /app/Vault/Logs/ceo-briefing-cron.log 2>&1" > /etc/cron.d/ceo-briefing

# Give execution rights
chmod 0644 /etc/cron.d/ceo-briefing

# Apply cron job
crontab /etc/cron.d/ceo-briefing

# Create log file
touch /app/Vault/Logs/ceo-briefing-cron.log

echo "CEO Briefing Generator configured"
echo "Starting cron daemon..."

# Start cron in foreground
cron -f
