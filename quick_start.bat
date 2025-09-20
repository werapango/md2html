@echo off
echo ===============================================
echo Markdown Converter - Quick Start Guide
echo ===============================================

REM เปลี่ยนไปยังโฟลเดอร์ export_markdown
cd /d "%~dp0"
echo Current directory: %CD%
echo.

echo Welcome to Markdown Converter!
echo This tool converts Markdown files with Mermaid diagrams to HTML, PDF, and Word.
echo.

echo ===============================================
echo Quick Setup (Choose one option)
echo ===============================================
echo.
echo 1. Full Setup (Recommended)
echo    - Creates virtual environment
echo    - Installs all dependencies
echo    - Sets up Mermaid support
echo    - Installs wkhtmltopdf for image generation
echo.
echo 2. Basic Setup
echo    - Installs core dependencies only
echo    - Mermaid diagrams will show as interactive HTML
echo.
echo 3. Test Current Installation
echo    - Tests what's already installed
echo    - Shows available features
echo.
echo 4. Launch GUI (if already set up)
echo    - Starts the graphical interface
echo.
echo 5. Create Test Files
echo    - Creates sample HTML with Mermaid diagrams
echo.
echo 6. Exit
echo.

:menu
set /p choice="Enter your choice (1-6): "

if "%choice%"=="1" goto full_setup
if "%choice%"=="2" goto basic_setup
if "%choice%"=="3" goto test_installation
if "%choice%"=="4" goto launch_gui
if "%choice%"=="5" goto create_test
if "%choice%"=="6" goto exit
echo Invalid choice. Please try again.
goto menu

:full_setup
echo.
echo ===============================================
echo Running Full Setup...
echo ===============================================
echo.
echo Step 1: Setting up virtual environment...
call setup_venv.bat
if errorlevel 1 (
    echo Setup failed. Please check the error messages above.
    pause
    goto menu
)

echo.
echo Step 2: Installing wkhtmltopdf for Mermaid image generation...
call install_wkhtmltopdf.bat
if errorlevel 1 (
    echo wkhtmltopdf installation failed, but you can still use HTML format.
)

echo.
echo Step 3: Testing installation...
call test_all.bat
if errorlevel 1 (
    echo Some tests failed, but basic functionality should work.
)

echo.
echo ===============================================
echo Full Setup Complete!
echo ===============================================
echo.
echo You can now:
echo - Launch GUI: run_gui.bat
echo - Test Mermaid: start mermaid_test.html
echo - Convert files: python main.py input.md --format html --output output.html
echo.
pause
goto menu

:basic_setup
echo.
echo ===============================================
echo Running Basic Setup...
echo ===============================================
echo.
echo Installing core dependencies...
python -m pip install markdown requests Pillow mermaid-py
if errorlevel 1 (
    echo Basic setup failed. Please check the error messages above.
    pause
    goto menu
)

echo.
echo Basic setup complete!
echo Mermaid diagrams will display as interactive HTML.
echo.
pause
goto menu

:test_installation
echo.
echo ===============================================
echo Testing Current Installation...
echo ===============================================
echo.
call test_all.bat
echo.
pause
goto menu

:launch_gui
echo.
echo ===============================================
echo Launching GUI Application...
echo ===============================================
echo.
call run_gui.bat
echo.
pause
goto menu

:create_test
echo.
echo ===============================================
echo Creating Test Files...
echo ===============================================
echo.
python create_mermaid_test.py
if errorlevel 1 (
    echo Failed to create test files.
) else (
    echo Test files created successfully!
    echo Opening test file in browser...
    start mermaid_test.html
)
echo.
pause
goto menu

:exit
echo.
echo Thank you for using Markdown Converter!
echo.
echo For help and documentation:
echo - README.md - Basic usage guide
echo - MERMAID_PY_GUIDE.md - Mermaid-py usage guide
echo - WKHTMLTOPDF_TROUBLESHOOTING.md - PDF troubleshooting
echo - PDF_TROUBLESHOOTING.md - PDF generation guide
echo.
pause
exit /b 0
