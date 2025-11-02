@echo off
REM PowerPoint Image Remover - Run Script (Windows)
REM Script chay ung dung tren Windows

echo Dang khoi dong PowerPoint Image Remover...
python ppt_image_remover.py

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Khong the chay ung dung!
    echo Vui long chay install.bat truoc.
    pause
)
