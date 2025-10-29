@echo off
REM Lustify Bot Startup Script for Windows

echo ==================================
echo 🔥 Lustify Bot Startup
echo ==================================
echo.

REM Check if .env exists
if not exist .env (
    echo ⚠️  Warning: .env file not found!
    echo Creating .env from .env.example...
    copy .env.example .env
    echo.
    echo Please edit .env and add your Venice AI API key
    echo Then run this script again.
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist venv (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo 📥 Installing dependencies...
pip install -q -r requirements.txt

echo.
echo ✅ Setup complete!
echo.
echo 🚀 Starting Lustify Bot...
echo.

REM Run the application
python app.py

pause