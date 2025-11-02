# H??NG D?N T?I V? C?I ??T

## ?? C?CH 1: T?i file ZIP (Khuy?n ngh? - D? nh?t)

### B??c 1: T?i file ZIP
Trong Cursor/VSCode, t?m file: **`PowerPoint_Cleaner_Tool.zip`**
- Click chu?t ph?i ? **Download**
- Ho?c k?o th? file ra Desktop

### B??c 2: Gi?i n?n
- Windows: Click chu?t ph?i file ZIP ? **Extract All...**
- Mac: Double-click file ZIP
- Linux: `unzip PowerPoint_Cleaner_Tool.zip`

### B??c 3: Ch?y
```bash
# Windows: Click ??p v?o
install.bat      # C?i ??t (ch? 1 l?n)
run.bat          # Ch?y app

# Mac/Linux: Trong Terminal
chmod +x install.sh run.sh
./install.sh     # C?i ??t (ch? 1 l?n)
./run.sh         # Ch?y app
```

---

## ?? C?CH 2: T?i t?ng file (N?u kh?ng c? file ZIP)

### Files c?n t?i:

#### ?? **B?T BU?C** (cho Python Tool):
1. **`ppt_cleaner.py`** - App ch?nh (2-in-1: X?a ?nh + L?c text)
2. **`requirements.txt`** - Danh s?ch th? vi?n
3. **`install.bat`** (Windows) ho?c **`install.sh`** (Mac/Linux)
4. **`run.bat`** (Windows) ho?c **`run.sh`** (Mac/Linux)

#### ?? **TU? CH?N**:
5. **`ppt_image_remover.py`** - App ??n gi?n (ch? x?a ?nh)
6. **`README_CLEANER.md`** - H??ng d?n chi ti?t
7. **`DeleteSpecificSizedImages_Upgraded.vba`** - Code VBA (n?u d?ng trong PowerPoint)
8. **`VBA_UPGRADE_NOTES.md`** - H??ng d?n VBA

### C?ch t?i t?ng file trong Cursor/VSCode:
1. M? Explorer (sidebar b?n tr?i)
2. Click chu?t ph?i v?o file
3. Ch?n **"Download..."**
4. Ch?n th? m?c l?u (khuy?n ngh?: t?o 1 folder m?i)

---

## ?? C?CH 3: Copy-Paste th? c?ng

### N?u kh?ng th? download:

**B??c 1:** T?o folder m?i tr?n m?y, v? d?: `C:\PowerPoint_Cleaner`

**B??c 2:** T?o file v? copy n?i dung:

#### File: `ppt_cleaner.py`
1. T?o file text m?i, ??t t?n `ppt_cleaner.py`
2. M? file `ppt_cleaner.py` trong Cursor
3. Ctrl+A (ch?n t?t c?) ? Ctrl+C (copy)
4. Paste v?o file m?i

#### File: `requirements.txt`
T?o file text, n?i dung:
```
python-pptx>=0.6.21
```

#### File: `install.bat` (Windows)
T?o file, n?i dung:
```bat
@echo off
echo Dang cai dat...
pip install python-pptx
echo Hoan tat!
pause
```

#### File: `run.bat` (Windows)
T?o file, n?i dung:
```bat
@echo off
python ppt_cleaner.py
pause
```

**B??c 3:** Ch?y `install.bat` r?i `run.bat`

---

## ?? SAU KHI T?I V? GI?I N?N

### ?? C?u tr?c th? m?c:
```
PowerPoint_Cleaner/
??? ppt_cleaner.py          ? App ch?nh (2-in-1)
??? ppt_image_remover.py    ? App ??n gi?n (ch? x?a ?nh)
??? requirements.txt        ? Th? vi?n c?n thi?t
??? install.bat             ? C?i ??t (Windows)
??? install.sh              ? C?i ??t (Mac/Linux)
??? run.bat                 ? Ch?y app (Windows)
??? run.sh                  ? Ch?y app (Mac/Linux)
??? README_CLEANER.md       ? H??ng d?n
??? DeleteSpecificSizedImages_Upgraded.vba  ? Code VBA (option)
```

### ?? C?i ??t l?n ??u:

#### **Windows:**
1. C?i Python t? [python.org](https://www.python.org/downloads/)
   - **QUAN TR?NG:** Tick v?o "Add Python to PATH"
2. Double-click `install.bat`
3. ??i c?i ??t xong

#### **Mac:**
```bash
# C?i Homebrew (n?u ch?a c?)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# C?i Python
brew install python3

# C?i th? vi?n
chmod +x install.sh
./install.sh
```

#### **Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-tk
chmod +x install.sh
./install.sh
```

### ?? Ch?y ?ng d?ng:

#### **Windows:**
```bash
# C?ch 1: Double-click
run.bat

# C?ch 2: Command Prompt
python ppt_cleaner.py
```

#### **Mac/Linux:**
```bash
# C?ch 1:
./run.sh

# C?ch 2: Terminal
python3 ppt_cleaner.py
```

---

## ? KI?M TRA C?I ??T

### Test Python:
```bash
# Windows
python --version

# Mac/Linux
python3 --version
```

K?t qu?: `Python 3.x.x` (x >= 7)

### Test th? vi?n:
```bash
# Windows
python -c "import pptx; print('OK')"

# Mac/Linux
python3 -c "import pptx; print('OK')"
```

K?t qu?: `OK`

N?u l?i ? Ch?y l?i `install.bat` ho?c `install.sh`

---

## ?? S? D?NG NHANH

### App Python (Khuy?n ngh?):

1. **Ch?y:** `run.bat` (Windows) ho?c `./run.sh` (Mac/Linux)

2. **Giao di?n hi?n ra:**
   ```
   ???????????????????????????????
   ?  PowerPoint Cleaner         ?
   ?  [??? X?a ?nh] [?? L?c text]?
   ???????????????????????????????
   ```

3. **S? d?ng:**
   - Ch?n file .pptx
   - Ch?n tab: X?a ?nh HO?C L?c text
   - C?u h?nh
   - Preview (xem tr??c)
   - X? l? file
   - Xong!

### Code VBA (Trong PowerPoint):

1. M? file `.vba` b?ng Notepad
2. M? PowerPoint ? Alt+F11 (VBA Editor)
3. Insert ? Module
4. Copy to?n b? code VBA v?o
5. Alt+F8 ? Ch?n macro ? Run

---

## ?? X? L? L?I TH??NG G?P

### ? "python is not recognized"
**Nguy?n nh?n:** Python ch?a c?i ho?c ch?a th?m v?o PATH

**Gi?i ph?p:**
1. G? Python (n?u ?? c?i)
2. T?i l?i t? python.org
3. **Tick v?o "Add Python to PATH"** ? QUAN TR?NG
4. C?i ??t l?i

### ? "No module named 'pptx'"
**Nguy?n nh?n:** Ch?a c?i th? vi?n

**Gi?i ph?p:**
```bash
pip install python-pptx
```

### ? File ZIP kh?ng gi?i n?n ???c
**Nguy?n nh?n:** File b? l?i khi t?i

**Gi?i ph?p:**
- T?i l?i file ZIP
- Ho?c t?i t?ng file ri?ng l? (C?ch 2)

### ? App kh?ng ch?y tr?n Mac
**Nguy?n nh?n:** Thi?u quy?n th?c thi

**Gi?i ph?p:**
```bash
chmod +x install.sh run.sh
./install.sh
./run.sh
```

### ? "Permission denied" khi x? l? file
**Nguy?n nh?n:** File PowerPoint ?ang m?

**Gi?i ph?p:**
- ??ng PowerPoint
- ??ng c? Preview/Explorer n?u ?ang xem file

---

## ?? H? TR?

### Checklist tr??c khi b?o l?i:
- [ ] ?? c?i Python? (`python --version`)
- [ ] ?? c?i th? vi?n? (`pip list | grep pptx`)
- [ ] File .pptx hay .ppt? (Ch? h? tr? .pptx)
- [ ] ?? ??ng PowerPoint?
- [ ] ?? th? file kh?c?

### Files c?n thi?t t?i thi?u:
N?u ch? mu?n app Python ??n gi?n nh?t:
1. `ppt_cleaner.py` (ho?c `ppt_image_remover.py`)
2. Python 3.7+
3. Th? vi?n: `pip install python-pptx`

Ch? 3 th? tr?n l? ??!

---

## ?? BONUS: Build file .EXE (Windows)

N?u mu?n t?o file .exe ch?y ??c l?p (kh?ng c?n Python):

```bash
# C?i PyInstaller
pip install pyinstaller

# Build
pyinstaller --onefile --windowed --name "PowerPoint_Cleaner" ppt_cleaner.py

# File .exe s? ? trong th? m?c dist/
```

File .exe c? th? copy sang m?y kh?c ch?y lu?n, kh?ng c?n c?i Python!

---

## ?? LINK H?U ?CH

- **Python:** https://www.python.org/downloads/
- **python-pptx docs:** https://python-pptx.readthedocs.io/
- **Regex tester:** https://regex101.com/
- **Homebrew (Mac):** https://brew.sh/

---

## ?? T?M T?T - B??C ??N GI?N NH?T

### 3 B??C DUY NH?T:

1. **T?i file ZIP** ? Gi?i n?n
2. **Ch?y `install.bat`** (ho?c `install.sh`)
3. **Ch?y `run.bat`** (ho?c `run.sh`)

### XONG! ??

App s? m? ra, b?n ch?n file PowerPoint v? x? l?!

---

**C?n h? tr? th?m?** H?y ki?m tra:
- `README_CLEANER.md` - H??ng d?n chi ti?t
- `README_TOOL.md` - H??ng d?n app x?a ?nh
- `VBA_UPGRADE_NOTES.md` - H??ng d?n VBA
