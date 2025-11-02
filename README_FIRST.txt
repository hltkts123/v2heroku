================================================================================
           CHAO MUNG DEN VOI STROKE ORDER DOWNLOADER
                    Tai Anh Thu Tu Net Chu Han
================================================================================

BUOC 1: CAI DAT PYTHON (neu chua co)
----------------------------------------
- Tai Python tai: https://www.python.org/downloads/
- Phien ban toi thieu: Python 3.7+
- KHI CAI DAT: Nho TICK vao "Add Python to PATH"

BUOC 2: CAI DAT THU VIEN
----------------------------------------
Mo Command Prompt (Windows) hoac Terminal (Mac/Linux) tai thu muc nay:

    pip install -r requirements.txt

BUOC 3: CHAY UNG DUNG
----------------------------------------
    python stroke_order_downloader.py

XONG! Giao dien se mo ra ngay!

================================================================================
                            CAC FILE TRONG ZIP
================================================================================

stroke_order_downloader.py  ? File chinh cua ung dung
requirements.txt            ? Danh sach thu vien can cai
README_STROKE_ORDER.md      ? Huong dan tong quan
HUONG_DAN.md                ? Huong dan chi tiet day du
GIAO_DIEN.txt              ? Mo ta giao dien ung dung
build_exe.bat              ? Build file EXE tren Windows
build_exe.sh               ? Build tren Linux/macOS

================================================================================
                            CAU HOI THUONG GAP
================================================================================

Q: Lam sao de khong phai cai Python?
A: Build thanh file EXE:
   - Windows: Chay file "build_exe.bat"
   - Mac/Linux: Chay "chmod +x build_exe.sh" sau do "./build_exe.sh"
   - File EXE se o trong thu muc "dist/"

Q: Tai sao khong thay icon emoji?
A: Day la thiet ke co y de chay tot tren moi he thong!
   Tkinter khong ho tro emoji tot tren Windows cu va Linux.
   Giao dien su dung text ASCII de dam bao hoat dong 100%.

Q: Ung dung luu anh o dau?
A: Mac dinh:
   - Windows: C:\Users\<ten-ban>\Stroke_images\
   - Mac/Linux: ~/Stroke_images/
   Ban co the chon thu muc khac trong ung dung!

Q: Anh nao duoc tai?
A: Anh GIF dong hien thi thu tu net viet chu Han
   Tu website: strokeorder.info

Q: Thu muc da chon co duoc luu khong?
A: CO! Ung dung tu dong nho thu muc ban chon lan truoc.
   File config: ~/.stroke_order_config.json

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

Neu gap loi, hay doc file HUONG_DAN.md de biet cach khac phuc!

Cac van de thuong gap:
- "ModuleNotFoundError" ? Chay: pip install -r requirements.txt
- "Timeout" ? Kiem tra internet
- Build EXE loi ? Xem chi tiet trong HUONG_DAN.md

================================================================================
                           PHIEN BAN
================================================================================

Version: 2.0
Update: 2025-11-02
Tinh nang:
  - Da luong (tai 10 anh song song)
  - Luu nho thu muc
  - Mo thu muc truc tiep
  - Giao dien hien dai
  - Cross-platform

================================================================================

          CHUC BAN SU DUNG VUI VE VA HOC TOT TIENG TRUNG!

================================================================================
