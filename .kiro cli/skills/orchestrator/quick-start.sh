#!/bin/bash
# Quick Start - Orchestration Workflow
# Run this script to process emails and generate draft responses

echo "═══════════════════════════════════════════════════════"
echo "  Email Orchestration - Quick Start"
echo "═══════════════════════════════════════════════════════"
echo ""

# Navigate to orchestrator directory
cd "$(dirname "$0")"

echo "Step 1: Running Orchestrator..."
echo "Analyzing emails in Vault/Needs_Action/"
echo ""

node orchestrator.js

echo ""
echo "═══════════════════════════════════════════════════════"
echo "  Next Steps"
echo "═══════════════════════════════════════════════════════"
echo ""
echo "1. Review drafts:"
echo "   cd ../../../Vault/Pending_Approval"
echo "   ls -la DRAFT_*.md"
echo ""
echo "2. Read a draft:"
echo "   cat DRAFT_[filename].md"
echo ""
echo "3. Approve and send (via Claude):"
echo "   Tell Claude: 'Approve and send DRAFT_[filename].md'"
echo ""
echo "4. Or approve via command line:"
echo "   node approve-and-send.js \"DRAFT_[filename].md\""
echo ""
echo "═══════════════════════════════════════════════════════"
