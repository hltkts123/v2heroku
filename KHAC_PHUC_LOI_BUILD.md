# KH?C PH?C L?I BUILD EXE

## ?? C?C L?I TH??NG G?P

### 1. **L?i: "ModuleNotFoundError: No module named 'pptx'"**

**Nguy?n nh?n:** Thi?u th? vi?n python-pptx

**Kh?c ph?c:**
```bash
# C?i ??t t?t c? dependencies tr??c
pip install python-pptx pillow pyinstaller

# Sau ?? build l?i
pyinstaller --noconfirm --clean \
    --hidden-import=pptx \
    --hidden-import=pptx.util \
    --hidden-import=PIL \
    --name "PowerPointCleaner" \
    --onefile \
    --windowed \
    ppt_cleaner.py
```

---

### 2. **L?i: "Unable to find 'icon.ico'"**

**Nguy?n nh?n:** File icon ch?a ???c t?o

**Kh?c ph?c:**
```bash
# Option 1: T?o icon tr??c
pip install pillow
python create_icon.py

# Option 2: Build kh?ng c?n icon
pyinstaller --noconfirm --clean \
    --name "PowerPointCleaner" \
    --onefile \
    --windowed \
    ppt_cleaner.py

# Option 3: D?ng icon Windows m?c ??nh
pyinstaller --noconfirm --clean \
    --name "PowerPointCleaner" \
    --onefile \
    --windowed \
    --icon=NONE \
    ppt_cleaner.py
```

---

### 3. **L?i: "PyInstaller not found"**

**Kh?c ph?c:**
```bash
# C?i ??t PyInstaller
pip install --upgrade pyinstaller

# Ki?m tra ?? c?i ch?a
pyinstaller --version

# N?u v?n l?i, d?ng python -m
python -m PyInstaller --version
```

---

### 4. **L?i: "Failed to execute script pyi_rth_pkgres"**

**Nguy?n nh?n:** Xung ??t dependencies

**Kh?c ph?c:**
```bash
# X?a cache PyInstaller
rd /s /q build dist *.spec

# Rebuild v?i clean
pyinstaller --noconfirm --clean \
    --onefile \
    --windowed \
    ppt_cleaner.py
```

---

### 5. **L?i: "PermissionError: [WinError 5] Access is denied"**

**Nguy?n nh?n:** Antivirus ?ang qu?t ho?c file ?ang m?

**Kh?c ph?c:**
```bash
# 1. T?t antivirus t?m th?i
# 2. ??ng t?t c? file EXE ?ang ch?y
# 3. X?a folder build, dist
rd /s /q build dist

# 4. Build l?i
pyinstaller --noconfirm --clean ppt_cleaner.py
```

---

### 6. **L?i: "RecursionError: maximum recursion depth exceeded"**

**Kh?c ph?c:**
```bash
# T?ng recursion limit
pyinstaller --noconfirm --clean \
    --recursion-limit=5000 \
    --onefile \
    --windowed \
    ppt_cleaner.py
```

---

## ??? BUILD SCRIPT T??NG TH?CH T?T H?N

T?o file `build_simple.bat`:

```batch
@echo off
echo Building PowerPoint Cleaner...

REM Install dependencies
pip install python-pptx pillow pyinstaller

REM Clean old build
if exist build rd /s /q build
if exist dist rd /s /q dist
del *.spec

REM Build WITHOUT icon (safer)
pyinstaller ^
    --noconfirm ^
    --clean ^
    --name "PowerPointCleaner" ^
    --onefile ^
    --windowed ^
    --hidden-import=pptx ^
    --hidden-import=pptx.util ^
    --hidden-import=PIL ^
    ppt_cleaner.py

REM Build batch version
pyinstaller ^
    --noconfirm ^
    --clean ^
    --name "PowerPointCleanerBatch" ^
    --onefile ^
    --windowed ^
    --hidden-import=pptx ^
    --hidden-import=pptx.util ^
    --hidden-import=PIL ^
    ppt_cleaner_batch.py

echo Done! Check 'dist' folder
pause
```

---

## ?? DEBUG MODE

?? xem l?i chi ti?t h?n:

```bash
# Build v?i console (kh?ng d?ng --windowed)
pyinstaller --noconfirm --clean \
    --name "PowerPointCleaner_Debug" \
    --onefile \
    --console \
    ppt_cleaner.py

# Ch?y file EXE t? command prompt ?? xem l?i
dist\PowerPointCleaner_Debug.exe
```

---

## ?? CHECKLIST TR??C KHI BUILD

- [ ] Python ?? c?i (3.6+)
- [ ] pip ?? c?i
- [ ] ?? c?i: `pip install python-pptx pillow pyinstaller`
- [ ] Antivirus t?t t?m th?i
- [ ] Kh?ng c? file EXE n?o ?ang ch?y
- [ ] Folder build, dist ?? x?a
- [ ] File .py kh?ng c? l?i syntax

---

## ?? N?U V?N L?I

### **C?ch 1: Build ??n gi?n nh?t**

```bash
# Ch? c?n l?nh t?i thi?u
pyinstaller --onefile --windowed ppt_cleaner.py
```

Kh?ng c? icon, kh?ng c? g? fancy, nh?ng ch?c ch?n ch?y ???c.

---

### **C?ch 2: D?ng spec file**

T?o file `ppt_cleaner.spec`:

```python
# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['ppt_cleaner.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['pptx', 'pptx.util', 'PIL'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='PowerPointCleaner',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
```

Sau ?? build:
```bash
pyinstaller ppt_cleaner.spec
```

---

### **C?ch 3: Kh?ng d?ng PyInstaller**

D?ng **auto-py-to-exe** (GUI cho PyInstaller):

```bash
pip install auto-py-to-exe
auto-py-to-exe
```

M? GUI, ch?n file, click Build!

---

## ?? M? T? L?I C?A B?N

**?? t?i gi?p ch?nh x?c h?n, vui l?ng:**

1. **Copy text l?i** (thay v? screenshot)
2. **Ho?c m? t?:**
   - L?i xu?t hi?n ? b??c n?o?
   - Th?ng b?o l?i l? g??
   - ?? c?i PyInstaller ch?a?
   - Python version?

**V? d?:**
```
L?i xu?t hi?n khi ch?y: build_exe.bat
Th?ng b?o: "ModuleNotFoundError: No module named 'pptx'"
Python: 3.9
```

---

## ?? GI?I PH?P T?M TH?I

N?u kh?ng build ???c EXE, ng??i d?ng v?n c? th? d?ng Python script:

```bash
# C?i dependencies
pip install python-pptx pillow

# Ch?y tr?c ti?p
python ppt_cleaner.py
```

Ho?c t?o shortcut v?i file `.bat`:

```batch
@echo off
python ppt_cleaner.py
```

??t t?n: `Run_PowerPointCleaner.bat`

---

## ?? TOOLS H? TR?

### **1. Nuitka** (alternative to PyInstaller)

```bash
pip install nuitka
python -m nuitka --onefile --windows-disable-console ppt_cleaner.py
```

### **2. cx_Freeze**

```bash
pip install cx_Freeze
cxfreeze ppt_cleaner.py --target-dir dist
```

### **3. py2exe** (Windows only)

```bash
pip install py2exe
python setup.py py2exe
```

---

## ? H?I NHANH

**Q: Build m?t bao l?u?**
A: 3-5 ph?t l?n ??u, 30-60 gi?y l?n sau

**Q: C?n bao nhi?u dung l??ng?**
A: ~500MB cho cache PyInstaller, EXE final ~15-20MB

**Q: C? th? build tr?n Mac/Linux kh?ng?**
A: C?, nh?ng ch? t?o ???c EXE cho platform ??

**Q: Antivirus c? ch?n kh?ng?**
A: C? th? false positive, add exception

---

**Copy l?i c?a b?n cho t?i ?? gi?p c? th? h?n!**
