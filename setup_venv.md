# Virtual Environment Setup for Markdown Converter

## การสร้าง Virtual Environment

### Windows:

```batch
@echo off
echo Creating virtual environment for Markdown Converter...

REM สร้าง virtual environment
python -m venv markdown_converter_env

REM เปิดใช้งาน virtual environment
call markdown_converter_env\Scripts\activate.bat

REM อัปเกรด pip
python -m pip install --upgrade pip

REM ติดตั้ง dependencies
pip install -r requirements.txt

echo.
echo Virtual environment created successfully!
echo.
echo To activate the environment, run:
echo   markdown_converter_env\Scripts\activate.bat
echo.
echo To deactivate, run:
echo   deactivate
echo.
pause
```

### Linux/macOS:

```bash
#!/bin/bash
echo "Creating virtual environment for Markdown Converter..."

# สร้าง virtual environment
python3 -m venv markdown_converter_env

# เปิดใช้งาน virtual environment
source markdown_converter_env/bin/activate

# อัปเกรด pip
python -m pip install --upgrade pip

# ติดตั้ง dependencies
pip install -r requirements.txt

echo ""
echo "Virtual environment created successfully!"
echo ""
echo "To activate the environment, run:"
echo "  source markdown_converter_env/bin/activate"
echo ""
echo "To deactivate, run:"
echo "  deactivate"
```

## การใช้งาน Virtual Environment

### เปิดใช้งาน (Windows):

```batch
markdown_converter_env\Scripts\activate.bat
```

### เปิดใช้งาน (Linux/macOS):

```bash
source markdown_converter_env/bin/activate
```

### ปิดใช้งาน:

```bash
deactivate
```

## การติดตั้ง Dependencies ใน Virtual Environment

```bash
# เปิดใช้งาน virtual environment ก่อน
# แล้วรัน:
pip install -r requirements.txt
```

## การทดสอบใน Virtual Environment

```bash
# เปิดใช้งาน virtual environment
# แล้วรัน:
python test_converter.py
```

## การสร้าง requirements.txt ใหม่

```bash
# เปิดใช้งาน virtual environment
# แล้วรัน:
pip freeze > requirements.txt
```

## การลบ Virtual Environment

```bash
# Windows
rmdir /s markdown_converter_env

# Linux/macOS
rm -rf markdown_converter_env
```
