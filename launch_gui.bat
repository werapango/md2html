@echo off
echo ===============================================
echo Markdown Converter GUI - Shortcut Launcher
echo ===============================================
echo.

REM เปลี่ยนไปยังโฟลเดอร์ของโปรแกรม
cd /d "%~dp0"

REM ตรวจสอบว่ามี Python หรือไม่
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed!
    echo Please install Python from https://python.org
    echo.
    pause
    exit /b 1
)

REM ตรวจสอบไฟล์ที่จำเป็น
if not exist "gui_app.py" (
    echo Error: gui_app.py not found
    echo Please run this shortcut from the correct directory
    echo.
    pause
    exit /b 1
)

REM ตรวจสอบ dependencies
python -c "import tkinter; print('✓ tkinter: OK')" 2>nul || (
    echo Error: tkinter not available
    echo Please reinstall Python with tkinter support
    echo.
    pause
    exit /b 1
)

python -c "import markdown; print('✓ markdown: OK')" 2>nul || (
    echo Error: markdown not installed
    echo Installing markdown...
    pip install markdown pygments
    if errorlevel 1 (
        echo Failed to install dependencies
        echo Please run: pip install markdown pygments
        echo.
        pause
        exit /b 1
    )
)

echo ✓ All dependencies ready
echo.
echo Starting Markdown Converter GUI...
echo.

REM รัน GUI application
python gui_app.py

REM ถ้าเกิดข้อผิดพลาด
if errorlevel 1 (
    echo.
    echo Error: Failed to start GUI application
    echo Please check the error messages above
    echo.
    pause
)
