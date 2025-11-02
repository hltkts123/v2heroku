@echo off
chcp 65001 >nul
echo ========================================
echo Build Stroke Order Downloader to EXE
echo ========================================
echo.

echo [1/4] Kiem tra Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [LOI] Python chua duoc cai dat!
    echo Vui long tai Python tai: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)
echo [OK] Python da duoc cai dat
echo.

echo [2/4] Cai dat PyInstaller...
python -m pip install --upgrade pip
python -m pip install pyinstaller
if errorlevel 1 (
    echo [LOI] Khong the cai dat PyInstaller!
    echo Thu chay lenh: pip install pyinstaller
    echo.
    pause
    exit /b 1
)
echo [OK] PyInstaller da duoc cai dat
echo.

echo [3/4] Cai dat cac thu vien can thiet...
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo [CANH BAO] Mot so thu vien co the khong cai duoc
)
echo.

echo [4/4] Build file EXE...
python -m PyInstaller --onefile --windowed --name "StrokeOrderDownloader" --icon=NONE stroke_order_downloader.py
if errorlevel 1 (
    echo [LOI] Build that bai!
    echo.
    pause
    exit /b 1
)
echo.

echo ========================================
echo           BUILD THANH CONG!
echo ========================================
echo.
echo File EXE da duoc tao tai:
echo %CD%\dist\StrokeOrderDownloader.exe
echo.
echo Ban co the chay file EXE ma khong can Python!
echo.

if exist "dist\StrokeOrderDownloader.exe" (
    echo [OK] File EXE ton tai va san sang su dung!
    explorer /select,"dist\StrokeOrderDownloader.exe"
) else (
    echo [LOI] File EXE khong ton tai!
)
echo.

pause
