# HUONG DAN BUILD FILE EXE

## Van de ban gap

**Loi:** `'pyinstaller' is not recognized as an internal or external command`

**Nguyen nhan:** 
- PyInstaller chua duoc cai dat
- Hoac Python khong co trong PATH cua Windows

---

## GIAI PHAP 1: Su dung file build_exe.bat moi (KHUYEN NGHI)

File build_exe.bat da duoc cap nhat de tu dong xu ly moi thu!

**Cach chay:**
1. Mo Command Prompt (cmd)
2. Di chuyen den thu muc chua code:
   ```
   cd duong\dan\den\thu\muc
   ```
3. Chay file bat:
   ```
   build_exe.bat
   ```

File bat moi se:
- ? Kiem tra Python da cai chua
- ? Tu dong cai PyInstaller
- ? Cai cac thu vien can thiet
- ? Build file EXE
- ? Tu dong mo thu muc chua file EXE

---

## GIAI PHAP 2: Cai dat thu cong tung buoc

### Buoc 1: Kiem tra Python
```bash
python --version
```

Neu khong co Python, tai tai: https://www.python.org/downloads/

**LUU Y:** Khi cai Python, phai TICK vao "Add Python to PATH"

### Buoc 2: Cai dat pip (neu chua co)
```bash
python -m ensurepip --upgrade
```

### Buoc 3: Nang cap pip
```bash
python -m pip install --upgrade pip
```

### Buoc 4: Cai dat PyInstaller
```bash
python -m pip install pyinstaller
```

### Buoc 5: Cai dat cac thu vien khac
```bash
python -m pip install -r requirements.txt
```

### Buoc 6: Build file EXE
```bash
python -m PyInstaller --onefile --windowed --name "StrokeOrderDownloader" stroke_order_downloader.py
```

### Buoc 7: Tim file EXE
File EXE se nam trong thu muc:
```
dist\StrokeOrderDownloader.exe
```

---

## GIAI PHAP 3: Su dung lenh ngan gon

Neu da cai PyInstaller thanh cong, co the dung lenh ngan:

```bash
pyinstaller --onefile --windowed stroke_order_downloader.py
```

---

## Khac phuc loi thuong gap

### Loi 1: "python is not recognized"
**Nguyen nhan:** Python khong co trong PATH

**Giai phap:**
1. Go cai Python
2. Cai lai, nho TICK "Add Python to PATH"
3. Khoi dong lai Command Prompt

### Loi 2: "pip is not recognized"
**Giai phap:**
```bash
python -m ensurepip
python -m pip install --upgrade pip
```

### Loi 3: PyInstaller cai that bai
**Giai phap:**
```bash
# Thu cai truc tiep bang Python
python -m pip install --user pyinstaller

# Neu van loi, thu version cu hon
python -m pip install pyinstaller==5.13.0
```

### Loi 4: Build thanh cong nhung khong tim thay file EXE
**Giai phap:**
1. Kiem tra thu muc `dist/` trong thu muc hien tai
2. Tim file ten: `StrokeOrderDownloader.exe` hoac `stroke_order_downloader.exe`
3. Neu khong co, kiem tra xem co loi trong qua trinh build khong

### Loi 5: File EXE chay bi loi
**Giai phap:** Build lai voi cac option day du:
```bash
python -m PyInstaller --onefile --windowed ^
    --hidden-import=requests ^
    --hidden-import=bs4 ^
    --hidden-import=tkinter ^
    --name "StrokeOrderDownloader" ^
    stroke_order_downloader.py
```

---

## Cach kiem tra PyInstaller da cai chua

Chay lenh:
```bash
python -m PyInstaller --version
```

Neu hien version (vi du: 6.3.0) tuc la da cai thanh cong!

---

## Test file EXE sau khi build

1. Di vao thu muc `dist/`
2. Double-click file `StrokeOrderDownloader.exe`
3. Ung dung se mo ra (khong can Python nua!)

---

## Luu y quan trong

### Emoji/Icon co hien thi khong?
- **Windows 10+:** C?, hien thi tot
- **Windows 7/8:** KHONG, hien thi la o vuong
- Neu muon chay tot tren Windows cu, su dung phien ban khong emoji

### Kich thuoc file EXE
- File EXE se khoang 15-20 MB
- Lon vi chua tat ca thu vien Python ben trong

### Chia se file EXE
- Co the copy file EXE sang may khac
- May khac KHONG CAN cai Python
- Nhung van can Windows de chay

---

## Video demo (cac buoc lam)

1. Mo Command Prompt (Win + R, go `cmd`, Enter)
2. Di chuyen den thu muc code:
   ```
   cd Desktop\StrokeOrderDownloader
   ```
3. Chay build:
   ```
   build_exe.bat
   ```
4. Doi build xong (khoang 1-2 phut)
5. File EXE se o: `dist\StrokeOrderDownloader.exe`
6. Double-click de chay!

---

## Neu van gap loi

Hay cung cap thong tin sau:
1. Version Windows (Win 7/8/10/11?)
2. Version Python (`python --version`)
3. Noi dung loi cu the (chup anh man hinh)
4. Thu muc hien tai (`cd` trong cmd)

---

## Khong muon build EXE?

Co the chay truc tiep bang Python:
```bash
python stroke_order_downloader.py
```

Nhanh hon va khong can build!
