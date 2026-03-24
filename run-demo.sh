#!/bin/bash
# ============================================================================
# AI EMPLOYEE - MASTER DEMO LAUNCHER (Linux/Mac)
# For 3-minute technical demonstration video
# ============================================================================

echo ""
echo "================================================================================"
echo "   AI EMPLOYEE - MASTER DEMO LAUNCHER"
echo "   Bronze → Silver → Gold Tier Demonstration"
echo "================================================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed"
    echo "Please install Python 3.8+ from python.org"
    exit 1
fi

echo "[INFO] Python detected: $(python3 --version)"
echo ""

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "[WARNING] .env file not found"
    echo "Please ensure your credentials are configured"
    echo ""
fi

# Install/check dependencies
echo "[INFO] Checking dependencies..."
pip3 install -q requests python-dotenv 2>/dev/null || {
    echo "[WARNING] Could not install dependencies"
    echo "Please run: pip3 install requests python-dotenv"
    echo ""
}

echo "[INFO] Starting Master Demo..."
echo ""
echo "================================================================================"
echo ""

# Run the demo
python3 demo-master.py

echo ""
echo "================================================================================"
echo "   Demo Complete"
echo "================================================================================"
echo ""
