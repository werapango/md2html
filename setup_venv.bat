@echo off
echo ===============================================
echo Markdown Converter - Virtual Environment Setup
echo ===============================================

REM ตรวจสอบว่ามี Python หรือไม่
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

REM ตรวจสอบว่ามีไฟล์ requirements.txt หรือไม่
if not exist "requirements.txt" (
    echo Error: requirements.txt not found
    echo Please run this script from the export_markdown directory
    pause
    exit /b 1
)

echo Creating virtual environment for Markdown Converter...
echo.

REM สร้าง virtual environment
python -m venv markdown_converter_env
if errorlevel 1 (
    echo Error: Failed to create virtual environment
    pause
    exit /b 1
)

echo Virtual environment created successfully!
echo.

REM เปิดใช้งาน virtual environment
echo Activating virtual environment...
call markdown_converter_env\Scripts\activate.bat
if errorlevel 1 (
    echo Error: Failed to activate virtual environment
    pause
    exit /b 1
)

echo Virtual environment activated!
echo.

REM อัปเกรด pip
echo Upgrading pip...
python -m pip install --upgrade pip
if errorlevel 1 (
    echo Warning: Failed to upgrade pip, continuing...
)

echo.

REM ติดตั้ง dependencies ที่จำเป็นเท่านั้น
echo Installing required Python dependencies...
echo.

echo Installing markdown...
pip install markdown
if errorlevel 1 (
    echo Error: Failed to install markdown - this is required!
    pause
    exit /b 1
) else (
    echo markdown installed successfully!
)

echo Installing pygments...
pip install pygments
if errorlevel 1 (
    echo Error: Failed to install pygments - this is required!
    pause
    exit /b 1
) else (
    echo pygments installed successfully!
)

echo Installing pymdown-extensions (optional)...
pip install pymdown-extensions
if errorlevel 1 (
    echo Warning: Failed to install pymdown-extensions
    echo This is optional, continuing...
) else (
    echo pymdown-extensions installed successfully!
)

echo Installing tkinter (GUI support)...
python -c "import tkinter; print('tkinter is available')" 2>nul || echo "Warning: tkinter not available"
if errorlevel 1 (
    echo Warning: tkinter may not be installed properly
    echo Please reinstall Python with tkinter support
) else (
    echo tkinter is working correctly!
)

echo.
echo Checking installation...
python -c "import markdown; print('✓ markdown: OK')" 2>nul || echo "✗ markdown: FAILED"
python -c "import pygments; print('✓ pygments: OK')" 2>nul || echo "✗ pygments: FAILED"
python -c "import pymdownx; print('✓ pymdown-extensions: OK')" 2>nul || echo "✗ pymdown-extensions: FAILED (optional)"
python -c "import tkinter; print('✓ tkinter: OK')" 2>nul || echo "✗ tkinter: FAILED"

echo.
echo ===============================================
echo Setup completed successfully!
echo ===============================================
echo.
echo Virtual environment: markdown_converter_env
echo.
echo To use the converter:
echo 1. Activate the environment: markdown_converter_env\Scripts\activate.bat
echo 2. Run the converter: python main.py [options]
echo 3. Deactivate when done: deactivate
echo.
echo To test the setup:
echo   python main.py --help
echo   python gui_app.py
echo.
echo ===============================================
pause
