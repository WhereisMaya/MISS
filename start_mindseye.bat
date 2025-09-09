@echo off
echo 🧠 Mindseye Evidence Compiler - Windows Startup
echo ================================================

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.7 or higher from https://python.org
    pause
    exit /b 1
)

REM Run the startup script
python start_mindseye.py

pause
