# HUONG DAN SU DUNG CHI TIET

## Tai sao khong thay icon/emoji?

**GIAI THICH:**
- Tkinter (thu vien GUI cua Python) **KHONG HO TRO TOT** emoji tren nhieu he thong
- Windows cu (7, 8), mot so Linux distribution khong hien thi duoc emoji
- Font he thong phai ho tro Unicode emoji (chi co Windows 10+, macOS moi day du)

**GIAI PHAP:**
- Phien ban hien tai da **THAY EMOJI BANG TEXT** de hoat dong tren MOI he thong
- Vi du: `??` ? `>>`, `??` ? `[+]`, `?` ? `[OK]`

## Cach chay ung dung

### Cach 1: Chay truc tiep bang Python

```bash
# Buoc 1: Cai dat thu vien
pip install -r requirements.txt

# Buoc 2: Chay ung dung
python stroke_order_downloader.py
```

### Cach 2: Build thanh file EXE (Windows)

**Tai sao can build EXE?**
- Khong can cai Python
- Chia se de dang cho nguoi khac
- Chay nhanh hon

**Cach build:**

```bash
# Cach 1: Dung file .bat co san
build_exe.bat

# Cach 2: Chay lenh thu cong
pip install pyinstaller
pyinstaller --onefile --windowed --name "StrokeOrderDownloader" stroke_order_downloader.py
```

File EXE se o: `dist\StrokeOrderDownloader.exe`

### Cach 3: Build tren Linux/macOS

```bash
# Cho quyen thuc thi
chmod +x build_exe.sh

# Chay build
./build_exe.sh
```

File se o: `dist/StrokeOrderDownloader`

## Cac tinh nang chinh

### 1. Nhap ky tu tieng Trung
- Nhap truc tiep: `????`
- Nhap cach dau phay: `?,?,?,?`
- Nhap cach khoang trang: `? ? ? ?`

### 2. Chon thu muc
- Click `[+] Chon Thu Muc` de chon noi luu anh
- Thu muc se duoc **LUU NHO** cho lan sau

### 3. Mo thu muc
- Click `[>] Mo Thu Muc` de mo folder trong File Explorer
- Xem ngay cac anh da tai

### 4. Tai anh
- Click `>> BAT DAU TAI <<` hoac nhan `Enter`
- Xem tien trinh trong thanh Progress Bar
- Ket qua hien thi day du o khung ben duoi

### 5. Huy bo
- Trong qua trinh tai, click `[X] HUY BO` de dung

## Cau hinh duoc luu o dau?

File: `~/.stroke_order_config.json`

**Windows:** `C:\Users\<ten-ban>\.stroke_order_config.json`
**Linux/macOS:** `/home/<ten-ban>/.stroke_order_config.json`

Noi dung:
```json
{
  "last_folder": "/duong/dan/thu/muc/cuoi/cung"
}
```

## Khac phuc loi thuong gap

### Loi: "ModuleNotFoundError: No module named 'requests'"
**Giai phap:**
```bash
pip install -r requirements.txt
```

### Loi: "Khong the mo thu muc"
**Giai phap:**
- Kiem tra thu muc co ton tai
- Kiem tra quyen truy cap
- Thu tao thu muc moi

### Loi: "Timeout" khi tai anh
**Giai phap:**
- Kiem tra ket noi internet
- Thu giam so luong ky tu tai cung luc
- Website strokeorder.info co the bi cham hoac loi

### Loi: Build EXE that bai
**Giai phap:**
```bash
# Cai dat lai PyInstaller
pip uninstall pyinstaller
pip install pyinstaller

# Thu build lai voi lenh day du
pyinstaller --onefile --windowed --hidden-import=requests --hidden-import=bs4 stroke_order_downloader.py
```

## He thong da test

- ? Windows 10/11
- ? Windows 7/8 (khong co emoji nhung van chay tot)
- ? Ubuntu 20.04+
- ? macOS 11+

## Lien he & Bao loi

Neu gap loi, hay ghi ro:
1. He dieu hanh (Windows/Linux/macOS)
2. Phien ban Python (`python --version`)
3. Thong bao loi cu the
4. Cac buoc da lam truoc khi gap loi
