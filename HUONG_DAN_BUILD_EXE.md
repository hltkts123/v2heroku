# H??NG D?N BUILD FILE EXE

## ?? M?C ??CH

Build Python tool th?nh file **EXE** ??:
- ? Ch?y KH?NG C?N c?i Python
- ? D? ph?n ph?i cho ng??i d?ng
- ? Double-click l? ch?y
- ? C? icon ??p, chuy?n nghi?p

---

## ?? Y?U C?U

### Windows:
- Python 3.6+ ?? c?i ??t
- pip ?? c?i ??t

### Mac/Linux:
- Python 3.6+ ?? c?i ??t
- pip3 ?? c?i ??t

**L?u ?:** Ch? c?n Python ?? BUILD, ng??i d?ng cu?i KH?NG c?n Python!

---

## ?? C?CH BUILD

### **C?CH 1: T? ??ng (Khuy?n ngh?)**

#### Windows:
```bash
# Double click file:
build_all_exe.bat

# Ho?c ch?y t? Command Prompt:
build_all_exe.bat
```

#### Mac/Linux:
```bash
# M? Terminal, cd v?o folder, ch?y:
chmod +x build_all_exe.sh
./build_all_exe.sh
```

**Script s?:**
1. ? Ki?m tra Python
2. ? C?i PyInstaller
3. ? T?o icon t? ??ng
4. ? Build 3 file EXE
   - ToolLauncher.exe
   - PowerPointCleanerBatch.exe
   - StrokeOrderDownloader.exe

---

### **C?CH 2: Th? c?ng**

#### B??c 1: C?i PyInstaller
```bash
pip install pyinstaller pillow
```

#### B??c 2: T?o icon
```bash
python create_icon.py
```

#### B??c 3: Build EXE

**Launcher:**
```bash
python -m PyInstaller --noconfirm --clean \
    --name "ToolLauncher" \
    --onefile \
    --windowed \
    --icon="icon.ico" \
    launcher.py
```

**PowerPoint Cleaner Batch:**
```bash
python -m PyInstaller --noconfirm --clean \
    --name "PowerPointCleanerBatch" \
    --onefile \
    --windowed \
    --icon="icon.ico" \
    --hidden-import=pptx \
    --hidden-import=pptx.util \
    ppt_cleaner_batch.py
```

**Stroke Order Downloader:**
```bash
python -m PyInstaller --noconfirm --clean \
    --name "StrokeOrderDownloader" \
    --onefile \
    --windowed \
    --icon="icon.ico" \
    --hidden-import=requests \
    --hidden-import=bs4 \
    stroke_order_downloader.py
```

---

## ?? K?T QU?

Sau khi build, file EXE n?m trong folder **`dist`**:

```
dist/
??? ToolLauncher.exe          (~20 MB)
??? PowerPointCleanerBatch.exe (~18 MB)
??? StrokeOrderDownloader.exe (~19 MB)
```

**Ph?n ph?i:**
- Ch? c?n copy 3 file EXE n?y
- Ng??i d?ng double-click ?? ch?y
- KH?NG C?N Python!

---

## ?? T?Y CH?NH BUILD

### Build kh?ng c? console window:
```bash
--windowed
```

### Build v?i console (?? debug):
```bash
--console
```

### Build nhi?u files (nhanh h?n):
```bash
--onedir
```

### Build 1 file EXE (g?n h?n):
```bash
--onefile
```

### Th?m data files:
```bash
--add-data "data.txt;."
```

---

## ?? T?I ?U

### Gi?m k?ch th??c EXE:
```bash
# D?ng UPX compression
pip install upx-windows
pyinstaller --upx-dir="path/to/upx" ...

# Lo?i b? modules kh?ng c?n
--exclude-module matplotlib
--exclude-module numpy
```

### T?ng t?c ?? kh?i ??ng:
```bash
# D?ng onedir thay v? onefile
--onedir

# Disable collect submodules
--no-collect-submodules
```

---

## ?? T?O ICON

### T? ??ng (Khuy?n ngh?):
```bash
python create_icon.py
```

### Th? c?ng:
1. T?o ?nh PNG 256x256
2. D?ng online converter: https://icoconvert.com/
3. L?u th?nh `icon.ico`
4. ??t c?ng folder v?i script

---

## ?? TROUBLESHOOTING

### L?i: "ModuleNotFoundError"
```bash
# Th?m hidden imports
--hidden-import=t?n_module
```

### L?i: "Failed to execute script"
```bash
# Build v?i console ?? xem l?i
pyinstaller --console ...
```

### L?i: "Permission denied"
```bash
# T?t antivirus t?m th?i
# X?a folder build, dist
# Build l?i
```

### EXE qu? l?n
```bash
# D?ng virtual environment
python -m venv venv
venv\Scripts\activate
pip install python-pptx pyinstaller
# Build trong venv (ch? c? dependencies c?n thi?t)
```

---

## ?? SCRIPT T? ??NG FIX L?I

N?u g?p l?i "pyinstaller not recognized":

```bash
# Windows:
fix_and_build.bat

# Script s?:
# 1. Upgrade pip
# 2. C?i PyInstaller
# 3. Verify installation
# 4. Build t?t c? EXE
```

---

## ?? SO S?NH BUILD OPTIONS

| Option | K?ch th??c | T?c ?? kh?i ??ng | Ph?n ph?i |
|--------|------------|------------------|-----------|
| `--onefile` | Nh? g?n (1 file) | Ch?m h?n | ? D? |
| `--onedir` | L?n h?n (folder) | Nhanh h?n | Kh? h?n |

**Khuy?n ngh?:** D?ng `--onefile` cho end-user

---

## ?? T?I LI?U LI?N QUAN

- `KHAC_PHUC_LOI_BUILD.md` - Kh?c ph?c l?i build
- `HUONG_DAN_SUA_LOI_PYINSTALLER.txt` - Fix l?i PyInstaller
- `fix_and_build.bat` - Script t? ??ng

---

## ?? TIPS

? **Build trong virtual environment** - EXE nh? h?n  
? **Test EXE tr?n m?y s?ch** - ??m b?o kh?ng thi?u dependencies  
? **T?o installer** - D?ng Inno Setup ho?c NSIS  
? **K? s? EXE** - Tr?nh c?nh b?o c?a Windows Defender

---

**Version:** 4.1  
**Tools:** 3 EXE  
**Platform:** Windows (ch?nh), macOS, Linux  
**Build time:** ~3-5 ph?t
