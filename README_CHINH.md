# PowerPoint Cleaner v4.1 - C?ng c? d?n d?p PowerPoint

**?ng d?ng Python v?i giao di?n ??p - Kh?ng c?n m? PowerPoint!**

## ?? T?nh n?ng

### ??? X?a h?nh ?nh
- X?a h?nh theo k?ch th??c c? th?
- 4 ch? ??: AND, OR, Width only, Height only
- T?y ch?nh dung sai

### ?? L?c text  
- **Gi? ti?ng Vi?t/Trung - X?a ti?ng Anh** (khuy?n ngh?)
- Gi? ti?ng Anh - X?a ti?ng Vi?t
- X?a t?t c? text
- Pattern t?y ch?nh (regex)
- **GI? NGUY?N FORMAT** (font, size, color, bold, italic...)

### ?? T?nh n?ng kh?c
- ? Preview tr??c khi x? l?
- ? T? ??ng backup file g?c
- ? Batch processing (nhi?u file)
- ? Progress tracking real-time
- ? Cross-platform (Windows/Mac/Linux)

### ?? Stroke Order Downloader
- ? T?i ?nh th? t? n?t ch? H?n
- ? T? strokeorder.info
- ? Download song song (10 threads)
- ? L?u GIF

## ?? C?ch t?i v?

### File c?n t?i:
**`PowerPoint_Cleaner_v4.1_OPTIMIZED.zip`** (35 KB)

### Trong Cursor/VSCode:
1. T?m file `PowerPoint_Cleaner_v4.1_OPTIMIZED.zip` trong Explorer
2. Click chu?t ph?i ? **Download**
3. Ch?n n?i l?u (Desktop / Documents)
4. Gi?i n?n file ZIP

## ?? C?i ??t & Ch?y

### Windows (2 b??c):

```bash
1. Gi?i n?n file ZIP

2. Double-click: install_full.bat
   (C?i ??t - ch? l?m 1 l?n)

3. Double-click: run_launcher.bat
   (Ch?y launcher)
```

### Mac/Linux:

```bash
1. Gi?i n?n file ZIP

2. Terminal:
   chmod +x install_full.sh run_launcher.sh
   ./install_full.sh
   (C?i ??t - ch? l?m 1 l?n)

3. Ch?y:
   ./run_launcher.sh
```

## ?? Y?u c?u h? th?ng

- **Python 3.6+** (t?i t? python.org)
  - ?? **Quan tr?ng:** Tick "Add Python to PATH" khi c?i
- Th? vi?n `python-pptx`, `requests`, `beautifulsoup4` (t? ??ng c?i b?ng script)

## ?? H??ng d?n s? d?ng

### V? d? 1: X?a h?nh 1.6x1.6 inch

1. Ch?y launcher
2. Ch?n "PowerPoint Cleaner"
3. Th?m file PowerPoint
4. Tab **"X?a h?nh ?nh"**
5. Width: `1.6`, Height: `1.6`
6. Ch? ??: **AND**
7. Click "X? l? t?t c? files"
8. Xong!

### V? d? 2: Gi? ti?ng Vi?t/Trung, x?a ti?ng Anh

**Tr??c:**
```
???? Product Introduction
(STXihei 54pt Red Bold) (Times 20pt)
```

**Sau:**
```
????
(STXihei 54pt Red Bold) ? FORMAT GI? NGUY?N!
```

**C?ch l?m:**
1. Ch?y launcher
2. Ch?n "PowerPoint Cleaner"
3. Th?m file PowerPoint
4. Tab **"L?c text"**
5. Ch?n: **"X?a ti?ng Anh - Gi? Vi?t/Trung"**
6. Click "X? l? t?t c? files"
7. Xong!

### V? d? 3: T?i ?nh ch? H?n

1. Ch?y launcher
2. Ch?n "Stroke Order Downloader"
3. Nh?p: `????`
4. Ch?n folder l?u
5. Click "B?t ??u t?i"
6. Xong! ? 4 file GIF (?.gif, ?.gif, ?.gif, ?.gif)

## ?? C?u tr?c file trong ZIP

```
PowerPoint_Cleaner_v4.1_OPTIMIZED.zip
??? launcher.py                    ? Launcher ch?nh
??? ppt_cleaner_batch.py          ? PowerPoint Cleaner
??? stroke_order_downloader.py    ? Stroke Order
??? requirements_full.txt           Th? vi?n c?n thi?t
??? install_full.bat/sh             Script c?i ??t
??? run_launcher.bat/sh             Script ch?y launcher
??? build_all_exe.bat               Build th?nh EXE
??? docs/
    ??? README_INTEGRATED.md      ? H??ng d?n ??y ??
    ??? START_HERE_v4.1.txt       ? Quick start
    ??? CAP_NHAT_v4.1.md            Changelog
    ??? ...
```

## ?? X? l? l?i th??ng g?p

### "python is not recognized"
**Nguy?n nh?n:** Ch?a c?i Python ho?c ch?a add v?o PATH

**Gi?i ph?p:**
1. T?i Python t? python.org
2. C?i l?i, **nh? tick "Add Python to PATH"**
3. Restart Command Prompt

### "No module named 'pptx'"
**Nguy?n nh?n:** Ch?a c?i th? vi?n

**Gi?i ph?p:**
```bash
pip install python-pptx requests beautifulsoup4
```

### "Permission denied"
**Nguy?n nh?n:** File PowerPoint ?ang m?

**Gi?i ph?p:**
- ??ng PowerPoint
- ??ng c? Preview/File Explorer n?u ?ang xem file

### File ZIP kh?ng gi?i n?n ???c
**Gi?i ph?p:**
- T?i l?i file ZIP
- D?ng WinRAR ho?c 7-Zip

## ?? T?i li?u chi ti?t

Trong file ZIP c? c?c file h??ng d?n ??y ??:

- **`START_HERE_v4.1.txt`** - H??ng d?n nhanh (m? b?ng Notepad)
- **`README_INTEGRATED.md`** - H??ng d?n ??y ?? t?ch h?p
- **`CAP_NHAT_v4.1.md`** - Changelog v4.1
- **`HUONG_DAN_TICH_HOP.md`** - Chi ti?t t?ch h?p
- **`HUONG_DAN_BUILD_EXE.md`** - H??ng d?n build EXE

## ?? Tips

? **Lu?n b?t "T? ??ng backup"** - An to?n tuy?t ??i
? **Preview tr??c** - Ki?m tra k? tr??c khi x?a
? **Test v?i file nh?** - Th? nghi?m tr??c khi x? l? file l?n
? **??ng PowerPoint** - Tr?nh l?i Permission denied

## ?? So s?nh Single vs Batch

| T?nh n?ng | Single (?? b?) | Batch v4.1 |
|-----------|-----------------|------------|
| X? l? 1 file | ? | ? |
| X? l? nhi?u file | ? | ? |
| Progress tracking | C? b?n | ? Chi ti?t |
| T?c ?? | Ch?m | ? Nhanh |

? **Batch mode c? th? l?m m?i th?!**

## ?? T?ng k?t - 3 b??c duy nh?t

```
1. T?i ZIP ? Gi?i n?n
2. Ch?y install_full (1 l?n)
3. Ch?y run_launcher (m?i l?n d?ng)
```

**??n gi?n v?y th?i!** ??

---

## ?? H? tr?

**Python:** https://www.python.org/downloads/  
**Library:** https://python-pptx.readthedocs.io/  
**Regex:** https://regex101.com/
**Stroke Order:** http://www.strokeorder.info/

---

**Version:** 4.1  
**Date:** 2025-11-02  
**Platform:** Windows / Mac / Linux  
**Tools:** 2 (PowerPoint Cleaner + Stroke Order)  
**License:** Free to use
