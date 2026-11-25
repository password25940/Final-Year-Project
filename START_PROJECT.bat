@echo off
title Student Feedback Analytics System
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo Creating Python environment...
    py -m venv .venv
    if errorlevel 1 (
        echo Python 3.10 or newer is required.
        pause
        exit /b 1
    )
)

echo Installing required packages...
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 (
    echo Package installation failed.
    pause
    exit /b 1
)

echo Preparing demo database...
".venv\Scripts\python.exe" seed.py
if errorlevel 1 (
    pause
    exit /b 1
)

echo.
echo Open http://127.0.0.1:5000 in your browser.
echo Admin login: admin@example.com / admin123
echo Press Ctrl+C to stop the server.
echo.
".venv\Scripts\python.exe" app.py
pause
