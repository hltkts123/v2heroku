@echo off
REM PowerPoint Image Remover - Installation Script (Windows)
REM Script cai dat tu dong cho Windows

echo ========================================
echo PowerPoint Image Remover - Cai dat
echo ========================================
echo.

REM Check Python
echo [1/3] Kiem tra Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Khong tim thay Python!
    echo Vui long tai va cai dat Python tu: https://www.python.org/downloads/
    echo Nho TICK vao "Add Python to PATH" khi cai dat!
    pause
    exit /b 1
)

python --version
echo Python da duoc cai dat!
echo.

REM Check pip
echo [2/3] Kiem tra pip...
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Khong tim thay pip!
    echo Pip nen duoc cai dat cung Python.
    pause
    exit /b 1
)

echo pip da san sang!
echo.

REM Install dependencies
echo [3/3] Cai dat thu vien python-pptx...
pip install python-pptx
if %errorlevel% neq 0 (
    echo [ERROR] Khong the cai dat python-pptx!
    pause
    exit /b 1
)

echo.
echo ========================================
echo Cai dat thanh cong!
echo ========================================
echo.
echo De chay ung dung, su dung file run.bat
echo Hoac chay lenh: python ppt_image_remover.py
echo.

pause
