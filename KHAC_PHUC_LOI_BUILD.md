# KH?C PH?C L?I BUILD EXE

## ?? C?C L?I TH??NG G?P

### 1. **L?i: "ModuleNotFoundError: No module named 'pptx'"**

**Nguy?n nh?n:** Thi?u th? vi?n python-pptx

**Kh?c ph?c:**
```bash
# C?i ??t t?t c? dependencies tr??c
pip install python-pptx pillow pyinstaller

# Sau ?? build l?i v?i hidden imports
python -m PyInstaller --noconfirm --clean \
    --hidden-import=pptx \
    --hidden-import=pptx.util \
    --hidden-import=PIL \
    --name "PowerPointCleanerBatch" \
    --onefile \
    --windowed \
    ppt_cleaner_batch.py
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
python -m PyInstaller --noconfirm --clean \
    --name "PowerPointCleanerBatch" \
    --onefile \
    --windowed \
    ppt_cleaner_batch.py

# Option 3: D?ng icon Windows m?c ??nh
python -m PyInstaller --noconfirm --clean \
    --name "PowerPointCleanerBatch" \
    --onefile \
    --windowed \
    --icon=NONE \
    ppt_cleaner_batch.py
```

---

### 3. **L?i: "PyInstaller not found" ho?c "pyinstaller is not recognized"**

**Kh?c ph?c:**
```bash
# Option 1: C?i ??t PyInstaller
python -m pip install --upgrade pyinstaller

# Option 2: Ki?m tra ?? c?i ch?a
python -m pip list | findstr pyinstaller

# Option 3: D?ng python -m (LU?N HO?T ??NG)
python -m PyInstaller --version

# Option 4: Ch?y script t? ??ng s?a l?i
fix_and_build.bat
```

**Xem th?m:** `HUONG_DAN_SUA_LOI_PYINSTALLER.txt`

---

### 4. **L?i: "Failed to execute script pyi_rth_pkgres"**

**Nguy?n nh?n:** Xung ??t dependencies

**Kh?c ph?c:**
```bash
# X?a cache PyInstaller
rd /s /q build dist *.spec

# Rebuild v?i clean
python -m PyInstaller --noconfirm --clean \
    --onefile \
    --windowed \
    ppt_cleaner_batch.py
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
python -m PyInstaller --clean ppt_cleaner_batch.py
```

---

### 6. **L?i: "RecursionError: maximum recursion depth exceeded"**

**Nguy?n nh?n:** Code c? ?? quy s?u

**Kh?c ph?c:**
```bash
# T?ng gi?i h?n recursion
python -m PyInstaller \
    --recursion-limit=5000 \
    --onefile \
    --windowed \
    ppt_cleaner_batch.py
```

---

### 7. **L?i: EXE ch?y r?i t?t ngay**

**Nguy?n nh?n:** L?i runtime kh?ng hi?n th?

**Kh?c ph?c:**
```bash
# Build v?i console ?? xem l?i
python -m PyInstaller \
    --noconfirm \
    --clean \
    --onefile \
    --console \
    ppt_cleaner_batch.py

# Ch?y EXE t? Command Prompt ?? xem l?i
dist\PowerPointCleanerBatch.exe
```

---

### 8. **L?i: "ImportError: DLL load failed"**

**Nguy?n nh?n:** Thi?u Visual C++ Redistributable

**Kh?c ph?c:**
```bash
# C?i Visual C++ Redistributable:
# https://aka.ms/vs/17/release/vc_redist.x64.exe

# Ho?c build v?i --hidden-import
python -m PyInstaller \
    --hidden-import=win32api \
    --hidden-import=win32con \
    ppt_cleaner_batch.py
```

---

### 9. **L?i: File EXE qu? l?n (>50MB)**

**Nguy?n nh?n:** Bao g?m nhi?u dependencies kh?ng c?n

**Kh?c ph?c:**
```bash
# 1. D?ng virtual environment s?ch
python -m venv venv_build
venv_build\Scripts\activate

# 2. Ch? c?i dependencies c?n thi?t
pip install python-pptx pyinstaller

# 3. Build trong venv
python -m PyInstaller --onefile ppt_cleaner_batch.py

# 4. Lo?i b? modules kh?ng c?n
python -m PyInstaller \
    --exclude-module=matplotlib \
    --exclude-module=numpy \
    --onefile \
    ppt_cleaner_batch.py
```

---

### 10. **L?i: "WARNING: lib not found"**

**Nguy?n nh?n:** C?nh b?o, kh?ng ?nh h??ng nghi?m tr?ng

**Kh?c ph?c:**
```bash
# C? th? ignore ho?c th?m path
python -m PyInstaller \
    --paths="C:\path\to\libs" \
    ppt_cleaner_batch.py
```

---

## ?? SCRIPT T? ??NG S?A T?T C? L?I

### Windows:

```bash
# Ch?y script t? ??ng s?a l?i
fix_and_build.bat
```

**Script s?:**
1. ? Upgrade pip
2. ? C?i PyInstaller
3. ? Verify installation  
4. ? Clean old builds
5. ? Build t?t c? EXE v?i ??y ?? imports
6. ? T?o icon t? ??ng

---

## ?? CHECKLIST TR??C KHI BUILD

- [ ] Python 3.6+ ?? c?i
- [ ] pip ?? c?i v? update
- [ ] T?t c? dependencies ?? c?i (`requirements_full.txt`)
- [ ] PyInstaller ?? c?i
- [ ] ?? test code ch?y OK
- [ ] ?? x?a folder build, dist c?
- [ ] Antivirus t?m t?t

---

## ?? DEBUG BUILD L?I

### B??c 1: Build v?i console
```bash
python -m PyInstaller --console ppt_cleaner_batch.py
```

### B??c 2: Ch?y v? ??c l?i
```bash
dist\PowerPointCleanerBatch.exe
```

### B??c 3: Google l?i c? th?
- T?m tr?n Stack Overflow
- Xem docs PyInstaller

### B??c 4: Th?m hidden imports
```bash
python -m PyInstaller \
    --hidden-import=module_bi_loi \
    ppt_cleaner_batch.py
```

---

## ?? TIPS TR?NH L?I

? **Lu?n d?ng `python -m PyInstaller`** thay v? `pyinstaller`  
? **Build trong virtual environment** ?? tr?nh conflict  
? **Test tr?n m?y s?ch** kh?ng c? Python  
? **??c warning** khi build ?? bi?t thi?u g?  
? **D?ng `--clean`** m?i l?n build

---

## ?? T?I LI?U LI?N QUAN

- `HUONG_DAN_BUILD_EXE.md` - H??ng d?n build chi ti?t
- `HUONG_DAN_SUA_LOI_PYINSTALLER.txt` - Fix l?i c? th?
- `fix_and_build.bat` - Script t? ??ng

---

## ?? V?N KH?NG GI?I QUY?T ???C?

1. **Xem log chi ti?t:**
   ```bash
   python -m PyInstaller --log-level=DEBUG ppt_cleaner_batch.py
   ```

2. **Rebuild t? ??u:**
   ```bash
   rd /s /q build dist __pycache__ *.spec
   python -m pip uninstall pyinstaller
   python -m pip install pyinstaller
   python -m PyInstaller --clean ppt_cleaner_batch.py
   ```

3. **D?ng script t? ??ng:**
   ```bash
   fix_and_build.bat
   ```

---

**Version:** 4.1  
**Platform:** Windows (ch?nh)  
**Last updated:** 2025-11-02
