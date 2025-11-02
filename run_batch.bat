@echo off
REM PowerPoint Cleaner Batch - Run Script (Windows)

echo Dang khoi dong PowerPoint Cleaner (Batch Mode)...
python ppt_cleaner_batch.py

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Khong the chay ung dung!
    pause
)
