@echo off
REM PowerPoint Cleaner - Run Script (Windows)
REM Script chay ung dung tren Windows

echo Dang khoi dong PowerPoint Cleaner...
python ppt_cleaner.py

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Khong the chay ung dung!
    echo Vui long chay install.bat truoc.
    pause
)
