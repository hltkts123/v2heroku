@echo off
echo ========================================
echo Build Stroke Order Downloader to EXE
echo ========================================
echo.

echo [1/3] Cai dat PyInstaller...
pip install pyinstaller

echo.
echo [2/3] Build file EXE...
pyinstaller --onefile --windowed --name "StrokeOrderDownloader" --icon=NONE stroke_order_downloader.py

echo.
echo [3/3] Hoan thanh!
echo File EXE da duoc tao trong thu muc: dist\StrokeOrderDownloader.exe
echo.

pause
