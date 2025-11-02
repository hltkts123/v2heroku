================================================================================
           CHAO MUNG DEN VOI STROKE ORDER DOWNLOADER
                    Tai Anh Thu Tu Net Chu Han
================================================================================

BUOC 1: CAI DAT PYTHON (neu chua co)
----------------------------------------
- Tai Python tai: https://www.python.org/downloads/
- Phien ban toi thieu: Python 3.7+
- KHI CAI DAT: Nho TICK vao "Add Python to PATH" <<<< QUAN TRONG!

BUOC 2: CAI DAT THU VIEN
----------------------------------------
Mo Command Prompt (Windows) hoac Terminal (Mac/Linux) tai thu muc nay:

    pip install -r requirements.txt

BUOC 3: CHAY UNG DUNG
----------------------------------------
    python stroke_order_downloader.py

XONG! Giao dien se mo ra ngay!

================================================================================
                            VE EMOJI/ICON
================================================================================

Ung dung su dung EMOJI de dep mat hon:
  ?? ?? ?? ?? ?? ? ? ?? ?? v.v.

HIEN THI TOT TREN:
  ? Windows 10 va cao hon
  ? macOS (tat ca phien ban)
  ? Linux voi font Unicode day du

KHONG HIEN THI TOT TREN:
  ? Windows 7, 8, 8.1 (se hien thi o vuong)

Neu Windows cu, emoji se hien thi la cac o vuong [] nhung UNG DUNG VAN
CHAY TOT VA DAY DU CHUC NANG!

================================================================================
                            BUILD THANH FILE EXE
================================================================================

CO 3 CACH BUILD:

CACH 1: Tu dong (khuyen nghi)
-----------------------------
    build_exe.bat

CACH 2: Don gian
-----------------------------
    build_simple.bat

CACH 3: Thu cong
-----------------------------
    python -m pip install pyinstaller
    python -m PyInstaller --onefile --windowed stroke_order_downloader.py

FILE EXE SE NAM TRONG THU MUC: dist\StrokeOrderDownloader.exe

NEU GAP LOI BUILD:
-> Doc file: HUONG_DAN_BUILD_EXE.md

================================================================================
                            CAC FILE TRONG ZIP
================================================================================

stroke_order_downloader.py  ? File chinh cua ung dung (CO EMOJI)
requirements.txt            ? Danh sach thu vien can cai
README_STROKE_ORDER.md      ? Huong dan tong quan
HUONG_DAN.md                ? Huong dan chi tiet day du
HUONG_DAN_BUILD_EXE.md      ? Huong dan build EXE chi tiet
GIAO_DIEN.txt              ? Mo ta giao dien ung dung
build_exe.bat              ? Build EXE (tu dong, khuyen nghi)
build_simple.bat           ? Build EXE (don gian)
build_exe.sh               ? Build tren Linux/macOS

================================================================================
                            CAU HOI THUONG GAP
================================================================================

Q: Lam sao de khong phai cai Python?
A: Build thanh file EXE:
   - Chay: build_exe.bat
   - File EXE se o trong thu muc "dist/"
   - Copy file EXE sang may khac duoc!

Q: Loi "pyinstaller is not recognized"?
A: Doc file HUONG_DAN_BUILD_EXE.md de biet cach sua!
   Hoac thu chay: python -m pip install pyinstaller

Q: Tai sao emoji hien thi la o vuong?
A: Ban dang dung Windows 7/8. Emoji chi hien thi tot tren Windows 10+.
   Ung dung van chay binh thuong, chi la khong dep thoi!

Q: Ung dung luu anh o dau?
A: Mac dinh:
   - Windows: C:\Users\<ten-ban>\Stroke_images\
   - Mac/Linux: ~/Stroke_images/
   Ban co the chon thu muc khac trong ung dung!

Q: Thu muc da chon co duoc luu khong?
A: CO! Ung dung tu dong nho thu muc ban chon lan truoc.
   File config: ~/.stroke_order_config.json

Q: Tai duoc bao nhieu anh cung luc?
A: 10 anh song song! Rat nhanh!

================================================================================
                        CACH SU DUNG NHANH
================================================================================

1. Mo ung dung
2. Nhap chu Han vao o input (vi du: ????)
3. Click "?? Bat dau tai"
4. Xem anh trong thu muc Stroke_images!

DON GIAN VAY THOI!

================================================================================
                        HO TRO & BUG REPORT
================================================================================

Neu gap loi, hay doc file tuong ung:
- Loi build EXE ? HUONG_DAN_BUILD_EXE.md
- Loi chay ung dung ? HUONG_DAN.md
- Khong hieu giao dien ? GIAO_DIEN.txt

Cac van de thuong gap:
- "ModuleNotFoundError" ? Chay: pip install -r requirements.txt
- "pyinstaller not recognized" ? Doc HUONG_DAN_BUILD_EXE.md
- "Timeout" ? Kiem tra internet
- Emoji la o vuong ? Binh thuong tren Windows cu!

================================================================================
                           PHIEN BAN
================================================================================

Version: 2.1
Update: 2025-11-02
Tinh nang:
  - Da luong (tai 10 anh song song) - NHANH GAP DOI!
  - Luu nho thu muc da chon
  - Mo thu muc truc tiep
  - Giao dien hien dai voi emoji
  - Cross-platform (Windows/Mac/Linux)
  - Build EXE de dang

Thay doi moi nhat:
  - Tang toc do tai len 10 anh song song (tu 5)
  - Sua file build_exe.bat de xu ly loi tot hon
  - Them huong dan build EXE chi tiet
  - Giu nguyen emoji (dep tren Windows 10+)

================================================================================

          CHUC BAN SU DUNG VUI VE VA HOC TOT TIENG TRUNG!

================================================================================
