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
build_exe.bat

# Ho?c ch?y t? Command Prompt:
build_exe.bat
```

#### Mac/Linux:
```bash
# M? Terminal, cd v?o folder, ch?y:
chmod +x build_exe.sh
./build_exe.sh
```

**Script s?:**
1. ? Ki?m tra Python
2. ? C?i PyInstaller
3. ? T?o icon t? ??ng
4. ? Build 2 file EXE

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

**Single file mode:**
```bash
pyinstaller --noconfirm --clean ^
    --name "PowerPointCleaner" ^
    --onefile ^
    --windowed ^
    --icon="icon.ico" ^
    ppt_cleaner.py
```

**Batch mode:**
```bash
pyinstaller --noconfirm --clean ^
    --name "PowerPointCleanerBatch" ^
    --onefile ^
    --windowed ^
    --icon="icon.ico" ^
    ppt_cleaner_batch.py
```

---

## ?? K?T QU?

Sau khi build, file EXE n?m trong folder **`dist`**:

```
dist/
??? PowerPointCleaner.exe          (~15-20 MB)
??? PowerPointCleanerBatch.exe     (~15-20 MB)
```

**??c ?i?m:**
- ? Ch?y ??c l?p, KH?NG C?N Python
- ? C? icon ??p
- ? Double-click l? ch?y
- ? K?ch th??c ~15-20MB (bao g?m Python runtime)

---

## ?? ICON

### Icon t? ??ng t?o:

```
???????????????????
?  [PP] PowerPoint? ? Orange bar
?                 ?
?      [?]        ? ? Green checkmark
?     Clean       ?
???????????????????
```

**??c ?i?m:**
- M?u cam gi?ng PowerPoint
- Checkmark xanh l? = "Clean"
- Professional design

### T? t?o icon ri?ng:

1. T?o ?nh PNG 256x256
2. Convert sang ICO:
   - Online: https://convertio.co/png-ico/
   - Ho?c d?ng Photoshop/GIMP
3. ??t t?n: `icon.ico`
4. Ch?y build script

---

## ?? PH?N PH?I

### Cho ng??i d?ng cu?i:

**G?i file EXE k?m h??ng d?n:**
```
PowerPointCleaner.exe          - X? l? 1 file
PowerPointCleanerBatch.exe     - X? l? nhi?u file
QUICK_START.txt                - H??ng d?n ng?n
```

**Ng??i d?ng ch? c?n:**
1. Download file EXE
2. Double-click ?? ch?y
3. KH?NG C?N c?i Python!

---

## ?? T?Y CH?NH BUILD

### Gi?m k?ch th??c file:

```bash
# Build v?i n?n UPX
pyinstaller --noconfirm --clean \
    --onefile \
    --windowed \
    --upx-dir=/path/to/upx \
    ppt_cleaner.py
```

### Build v?i console (debug):

```bash
# B? --windowed ?? th?y console output
pyinstaller --noconfirm --clean \
    --onefile \
    --console \
    --icon="icon.ico" \
    ppt_cleaner.py
```

### Build th?nh folder (nhanh h?n):

```bash
# B? --onefile
pyinstaller --noconfirm --clean \
    --windowed \
    --icon="icon.ico" \
    ppt_cleaner.py
```

? K?t qu?: Folder ch?a EXE + DLL files

---

## ?? TROUBLESHOOTING

### **L?i: "PyInstaller not found"**

**Gi?i ph?p:**
```bash
pip install --upgrade pyinstaller
```

### **L?i: "Failed to execute script"**

**Nguy?n nh?n:** Thi?u dependencies

**Gi?i ph?p:**
```bash
# Th?m hidden imports
pyinstaller --hidden-import=pptx \
    --hidden-import=PIL \
    ppt_cleaner.py
```

### **Icon kh?ng hi?n th?**

**Ki?m tra:**
```bash
# File icon.ico c? t?n t?i kh?ng?
dir icon.ico

# C? th? d?ng icon kh?c
pyinstaller --icon="path/to/your/icon.ico" ppt_cleaner.py
```

### **File EXE qu? l?n**

**Gi?i ph?p:**
1. D?ng UPX ?? n?n
2. Build th?nh folder thay v? onefile
3. X?a c?c imports kh?ng c?n thi?t

### **Antivirus b?o virus**

**L? do:** EXE ???c pack b?i PyInstaller c? th? b? false positive

**Gi?i ph?p:**
1. Submit file l?n VirusTotal ?? ki?m tra
2. Add exception trong antivirus
3. Sign code v?i certificate (n?u ph?n ph?i r?ng)

---

## ?? SO S?NH

| ??c ?i?m | Python Script | EXE File |
|----------|--------------|----------|
| **Y?u c?u Python** | C? | KH?NG |
| **K?ch th??c** | ~50 KB | ~15-20 MB |
| **Ch?y** | `python script.py` | Double-click |
| **Ph?n ph?i** | Ph?c t?p | D? d?ng |
| **Icon** | Kh?ng | C? |
| **Startup** | Nhanh | Ch?m h?n ~2s |

---

## ? CHECKLIST

### Tr??c khi ph?n ph?i:

- [ ] Build th?nh c?ng c? 2 file EXE
- [ ] Test EXE tr?n m?y KH?NG c?i Python
- [ ] Icon hi?n th? ??ng
- [ ] T?t c? t?nh n?ng ho?t ??ng
- [ ] File backup ???c t?o t? ??ng
- [ ] K?t qu? hi?n th? ??ng
- [ ] Kh?ng c? l?i console
- [ ] K?ch th??c file h?p l?

### G?i ph?n ph?i:

- [ ] PowerPointCleaner.exe
- [ ] PowerPointCleanerBatch.exe  
- [ ] QUICK_START.txt
- [ ] README_CHINH.md (optional)
- [ ] Sample files (optional)

---

## ?? BUILD INSTALLER (N?ng cao)

### S? d?ng Inno Setup (Windows):

1. Download Inno Setup: https://jrsoftware.org/isinfo.php
2. T?o file script `.iss`:

```iss
[Setup]
AppName=PowerPoint Cleaner
AppVersion=3.3.1
DefaultDirName={autopf}\PowerPointCleaner
DefaultGroupName=PowerPoint Cleaner
OutputDir=installer
OutputBaseFilename=PowerPointCleaner_Setup

[Files]
Source: "dist\PowerPointCleaner.exe"; DestDir: "{app}"
Source: "dist\PowerPointCleanerBatch.exe"; DestDir: "{app}"
Source: "README_CHINH.md"; DestDir: "{app}"

[Icons]
Name: "{group}\PowerPoint Cleaner"; Filename: "{app}\PowerPointCleaner.exe"
Name: "{group}\PowerPoint Cleaner Batch"; Filename: "{app}\PowerPointCleanerBatch.exe"
Name: "{commondesktop}\PowerPoint Cleaner"; Filename: "{app}\PowerPointCleaner.exe"
```

3. Compile script ? T?o file `Setup.exe`

---

## ?? GHI CH?

### PyInstaller options:

| Option | ? ngh?a |
|--------|---------|
| `--onefile` | G?p th?nh 1 file EXE |
| `--windowed` | Kh?ng hi?n console |
| `--icon` | ??t icon |
| `--name` | T?n file EXE |
| `--add-data` | Th?m file data |
| `--hidden-import` | Import ?n |
| `--clean` | X?a cache tr??c build |
| `--noconfirm` | Kh?ng h?i confirm |

### Build time:

- **L?n ??u:** 3-5 ph?t (download dependencies)
- **L?n sau:** 30-60 gi?y (s? d?ng cache)

---

## ?? H? TR?

**N?u g?p v?n ??:**

1. Xem log build: `build.log`
2. Ch?y EXE t? console ?? xem l?i
3. Google error message + "PyInstaller"
4. Ki?m tra PyInstaller docs: https://pyinstaller.org/

**Common issues:**
- Hidden imports thi?u
- Icon path sai
- DLL conflicts
- Antivirus blocking

---

**Version:** 3.3.1
**Build tool:** PyInstaller 5.0+
**Platform:** Windows, macOS, Linux
