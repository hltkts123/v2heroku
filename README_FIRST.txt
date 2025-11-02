================================================================================
           CHAO MUNG DEN VOI STROKE ORDER DOWNLOADER
                    Tai Anh Thu Tu Net Chu Han
================================================================================

QUAN TRONG: PHIEN BAN NAY KHONG CO EMOJI!
------------------------------------------
Phien ban nay su dung 100% KY TU ASCII de tranh loi hien thi.
Giao dien van dep va ro rang, nhung khong co icon/emoji.

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
                            VE ICON/EMOJI
================================================================================

PHIEN BAN NAY: KHONG CO EMOJI
-----------------------------
- Su dung TEXT ASCII thuan tuy: [OK], [ERR], [INFO], [>], [+]
- Hien thi TOT tren MOI he thong
- KHONG con loi dau hoi (?) hay o vuong ([])

CAC KY HIU SU DUNG:
- [OK] - Thanh cong
- [ERR] - Loi
- [!] - Canh bao
- [INFO] - Thong tin
- [SUCCESS] - Hoan thanh
- [STATS] - Thong ke
- [+] - Chon
- [>] - Mo
- [X] - Huy
- >> << - Bat dau

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

stroke_order_downloader.py  ? File chinh (100% ASCII, khong emoji)
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

Q: Tai sao khong co emoji?
A: Vi nhieu he thong khong ho tro emoji trong Tkinter.
   Phien ban nay dung ASCII de chay tot tren MOI he thong!

Q: Lam sao de khong phai cai Python?
A: Build thanh file EXE:
   - Chay: build_exe.bat
   - File EXE se o trong thu muc "dist/"
   - Copy file EXE sang may khac duoc!

Q: Loi "pyinstaller is not recognized"?
A: Doc file HUONG_DAN_BUILD_EXE.md de biet cach sua!
   Hoac thu chay: python -m pip install pyinstaller

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
3. Click ">> BAT DAU TAI <<"
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

================================================================================
                           PHIEN BAN
================================================================================

Version: 2.2 (ASCII EDITION)
Update: 2025-11-02
Tinh nang:
  - Da luong (tai 10 anh song song) - NHANH GAP DOI!
  - Luu nho thu muc da chon
  - Mo thu muc truc tiep
  - Giao dien ASCII (khong emoji, khong loi)
  - Cross-platform (Windows/Mac/Linux)
  - Build EXE de dang

Thay doi phien ban nay:
  - XOA TAT CA emoji/icon
  - Su dung 100% ky tu ASCII
  - Khong con loi dau hoi (?) hay o vuong
  - Chay tot tren MOI Windows (7/8/10/11)

================================================================================

          CHUC BAN SU DUNG VUI VE VA HOC TOT TIENG TRUNG!

================================================================================
