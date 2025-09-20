#!/bin/bash

echo "==============================================="
echo "Markdown Converter - GUI Launcher"
echo "==============================================="

# ตรวจสอบว่ามี Python3 หรือไม่
if ! command -v python3 &> /dev/null; then
    echo "Error: Python3 is not installed"
    echo "Please install Python3 from your package manager"
    exit 1
fi

# ตรวจสอบว่ามีไฟล์ gui_app.py หรือไม่
if [ ! -f "gui_app.py" ]; then
    echo "Error: gui_app.py not found"
    echo "Please run this script from the export_markdown directory"
    exit 1
fi

# ตรวจสอบว่ามี virtual environment หรือไม่
if [ -d "markdown_converter_env" ]; then
    echo "Activating virtual environment..."
    source markdown_converter_env/bin/activate
    if [ $? -ne 0 ]; then
        echo "Warning: Failed to activate virtual environment"
        echo "Continuing with system Python..."
    fi
else
    echo "Warning: Virtual environment not found"
    echo "Please run ./setup_venv.sh first for better experience"
    echo "Continuing with system Python..."
fi

echo ""
echo "Starting Markdown Converter GUI..."
echo ""

# รัน GUI application
python3 gui_app.py

if [ $? -ne 0 ]; then
    echo ""
    echo "Error: Failed to start GUI application"
    echo "Please check if all dependencies are installed"
    echo "Run: pip3 install -r requirements.txt"
    read -p "Press Enter to continue..."
fi
