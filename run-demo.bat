@echo off
REM ============================================================================
REM AI EMPLOYEE - MASTER DEMO LAUNCHER
REM For 3-minute technical demonstration video
REM ============================================================================

echo.
echo ================================================================================
echo    AI EMPLOYEE - MASTER DEMO LAUNCHER
echo    Bronze → Silver → Gold Tier Demonstration
echo ================================================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8+ from python.org
    pause
    exit /b 1
)

echo [INFO] Python detected
echo.

REM Check if .env file exists
if not exist ".env" (
    echo [WARNING] .env file not found
    echo Please ensure your credentials are configured
    echo.
)

REM Install/check dependencies
echo [INFO] Checking dependencies...
pip install -q requests python-dotenv 2>nul
if errorlevel 1 (
    echo [WARNING] Could not install dependencies
    echo Please run: pip install requests python-dotenv
    echo.
)

echo [INFO] Starting Master Demo...
echo.
echo ================================================================================
echo.

REM Run the demo
python demo-master.py

echo.
echo ================================================================================
echo    Demo Complete
echo ================================================================================
echo.
pause
