@echo off
echo ===============================================
echo Markdown Converter GUI
echo ===============================================
echo.

REM ตรวจสอบว่ามี Python หรือไม่
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed!
    echo Please install Python from https://python.org
    echo.
    pause
    exit /b 1
)

echo ✓ Python is installed
python --version

REM ตรวจสอบว่ามีไฟล์ gui_app.py หรือไม่
if not exist "gui_app.py" (
    echo Error: gui_app.py not found
    echo Please run this script from the export_markdown directory
    echo.
    pause
    exit /b 1
)

REM ตรวจสอบว่ามีไฟล์ main.py หรือไม่
if not exist "main.py" (
    echo Error: main.py not found
    echo Please run this script from the export_markdown directory
    echo.
    pause
    exit /b 1
)

echo ✓ Required files found

REM ตรวจสอบ dependencies
echo.
echo Checking dependencies...
python -c "import tkinter; print('✓ tkinter: OK')" 2>nul || echo "✗ tkinter: FAILED"
python -c "import markdown; print('✓ markdown: OK')" 2>nul || echo "✗ markdown: FAILED"

echo.
echo Starting GUI application...
echo.

REM รัน GUI application
python gui_app.py

if errorlevel 1 (
    echo.
    echo Error: Failed to start GUI application
    echo Please check if all dependencies are installed
    echo Run: pip install -r requirements.txt
    echo.
    pause
)