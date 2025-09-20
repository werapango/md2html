@echo off
echo ===============================================
echo Markdown Converter - Windows Batch Script
echo ===============================================

REM ตรวจสอบว่ามี Python หรือไม่
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

REM ตรวจสอบว่ามีไฟล์ main.py หรือไม่
if not exist "main.py" (
    echo Error: main.py not found
    echo Please run this script from the export_markdown directory
    pause
    exit /b 1
)

REM ติดตั้ง dependencies
echo Installing Python dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo Dependencies installed successfully!
echo.

REM แสดงเมนู
:menu
echo ===============================================
echo Markdown Converter Menu
echo ===============================================
echo 1. Convert to HTML
echo 2. Convert to PDF
echo 3. Convert to Word
echo 4. Convert to All Formats
echo 5. Test Converter
echo 6. Exit
echo ===============================================
set /p choice="Enter your choice (1-6): "

if "%choice%"=="1" goto convert_html
if "%choice%"=="2" goto convert_pdf
if "%choice%"=="3" goto convert_word
if "%choice%"=="4" goto convert_all
if "%choice%"=="5" goto test_converter
if "%choice%"=="6" goto exit
goto menu

:convert_html
set /p input_file="Enter input Markdown file path: "
set /p output_file="Enter output HTML file path (or press Enter for auto): "
if "%output_file%"=="" (
    python main.py "%input_file%" --format html
) else (
    python main.py "%input_file%" --format html --output "%output_file%"
)
goto menu

:convert_pdf
set /p input_file="Enter input Markdown file path: "
set /p output_file="Enter output PDF file path (or press Enter for auto): "
if "%output_file%"=="" (
    python main.py "%input_file%" --format pdf
) else (
    python main.py "%input_file%" --format pdf --output "%output_file%"
)
goto menu

:convert_word
set /p input_file="Enter input Markdown file path: "
set /p output_file="Enter output Word file path (or press Enter for auto): "
if "%output_file%"=="" (
    python main.py "%input_file%" --format word
) else (
    python main.py "%input_file%" --format word --output "%output_file%"
)
goto menu

:convert_all
set /p input_file="Enter input Markdown file path: "
set /p output_dir="Enter output directory (or press Enter for ./output/): "
if "%output_dir%"=="" (
    python main.py "%input_file%" --format all --output-dir "./output/"
) else (
    python main.py "%input_file%" --format all --output-dir "%output_dir%"
)
goto menu

:test_converter
echo Running converter test...
python test_converter.py
goto menu

:exit
echo Thank you for using Markdown Converter!
pause
