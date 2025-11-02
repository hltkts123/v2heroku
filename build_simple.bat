@echo off
echo.
echo ====================================
echo   BUILD EXE - PHIEN BAN DON GIAN
echo ====================================
echo.
echo Dang cai dat PyInstaller...
python -m pip install pyinstaller
echo.
echo Dang build file EXE...
python -m PyInstaller --onefile --windowed stroke_order_downloader.py
echo.
echo XONG! File EXE o trong thu muc: dist\
echo.
pause
