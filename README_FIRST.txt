================================================================================
           CHAO MUNG DEN VOI STROKE ORDER DOWNLOADER
                    Tai Anh Thu Tu Net Chu Han
                     + GEMINI AI OCR (MOI!)
================================================================================

TINH NANG MOI: NHAN DANG CHU HAN TU ANH BANG AI!
-------------------------------------------------
Ban co the CHUP ANH chu Han, AI se tu dong nhan dang va tai stroke!
KHONG CAN GO CHU thu cong nua!

BUOC 1: CAI DAT PYTHON (neu chua co)
----------------------------------------
- Tai Python tai: https://www.python.org/downloads/
- Phien ban toi thieu: Python 3.7+
- KHI CAI DAT: Nho TICK vao "Add Python to PATH" <<<< QUAN TRONG!

BUOC 2: CAI DAT THU VIEN
----------------------------------------
Mo Command Prompt (Windows) hoac Terminal (Mac/Linux) tai thu muc nay:

    pip install -r requirements.txt

LUU Y: Lan nay co them thu vien Gemini AI va Pillow!

BUOC 3: LAY GEMINI API KEY (MIEN PHI!)
----------------------------------------
1. Truy cap: https://aistudio.google.com/app/apikey
2. Dang nhap Google
3. Click "Create API Key"
4. Copy API key

Chi mat 1 phut! API key MIEN PHI va KHONG HET HAN!

BUOC 4: CHAY UNG DUNG
----------------------------------------
    python stroke_order_downloader.py

BUOC 5: SU DUNG GEMINI AI
----------------------------------------
1. Dan API key vao o "Gemini API Key", click "Luu"
2. Click "[+] Chon Anh Chua Chu Han"
3. Chon anh co chu Han (chup man hinh, anh sach, anh chup, v.v.)
4. Click "[AI] Nhan Dang Chu Han"
5. Doi 2-5 giay
6. Chu Han se TU DONG dien vao!
7. Click "Bat dau tai" de tai stroke!

XONG! Nhanh va de dang!

================================================================================
                          TINH NANG CHINH
================================================================================

? GEMINI AI OCR - Nhan dang chu Han tu anh (MOI!)
  - Tu dong nhan dang chu Han
  - Khong can go chu
  - Nhanh 2-5 giay
  - Chinh xac cao
  - Mien phi (Google Gemini API)

? TAI STROKE NHANH
  - 10 anh song song
  - Nhanh gap doi
  - Luu nho thu muc

? GIAO DIEN DEP
  - De su dung
  - Hien thi ro rang
  - 100% ASCII (khong loi)

================================================================================
                            VE ICON/EMOJI
================================================================================

PHIEN BAN NAY: KHONG CO EMOJI
-----------------------------
- Su dung TEXT ASCII thuan tuy: [OK], [ERR], [INFO], [AI]
- Hien thi TOT tren MOI he thong
- KHONG con loi dau hoi (?) hay o vuong ([])

CAC KY HIU SU DUNG:
- [OK] - Thanh cong
- [ERR] - Loi
- [!] - Canh bao
- [INFO] - Thong tin
- [AI] - Gemini AI
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

stroke_order_downloader.py  ? File chinh (CO GEMINI AI!)
requirements.txt            ? Thu vien (co them Gemini AI)
HUONG_DAN_GEMINI_AI.md      ? Huong dan chi tiet ve AI (DOC DAU TIEN!)
README_STROKE_ORDER.md      ? Huong dan tong quan
HUONG_DAN.md                ? Huong dan chi tiet
HUONG_DAN_BUILD_EXE.md      ? Huong dan build EXE
build_exe.bat              ? Build EXE tu dong
build_simple.bat           ? Build EXE don gian

================================================================================
                            CAU HOI THUONG GAP
================================================================================

Q: Gemini AI co mien phi khong?
A: CO! Hoan toan MIEN PHI! Gioi han 1500 request/ngay (qua du dung!)

Q: Tai sao phai dung AI?
A: De KHONG PHAI GO CHU thu cong! Chi can chup anh, AI tu dong nhan dang!

Q: Loai anh nao duoc ho tro?
A: Tat ca! Anh chup man hinh, anh sach, anh chup tu dien thoai, v.v.

Q: AI co chinh xac khong?
A: RAT chinh xac! Gemini la AI manh cua Google.

Q: Co can internet khong?
A: CAN! De goi Gemini API.

Q: API key co an toan khong?
A: AN TOAN! Chi luu tren may ban, khong gui di dau.

Q: Tai sao khong co emoji?
A: Vi nhieu he thong khong ho tro emoji trong Tkinter.
   Phien ban nay dung ASCII de chay tot tren MOI he thong!

Q: Ung dung luu anh o dau?
A: Mac dinh:
   - Windows: C:\Users\<ten-ban>\Stroke_images\
   - Mac/Linux: ~/Stroke_images/
   Ban co the chon thu muc khac!

Q: Tai duoc bao nhieu anh cung luc?
A: 10 anh song song! Rat nhanh!

================================================================================
                        CACH SU DUNG NHANH
================================================================================

CACH 1: Dung AI (KHUY?N NGHI - NHANH NHAT!)
--------------------------------------------
1. Mo ung dung
2. Dan Gemini API key, click Luu
3. Click "Chon Anh Chua Chu Han"
4. Chon anh (chup man hinh, anh sach, v.v.)
5. Click "Nhan Dang Chu Han"
6. Click "Bat dau tai"
7. XONG!

CACH 2: Go thu cong (cach cu)
------------------------------
1. Mo ung dung
2. Go chu Han vao o input: ????
3. Click "Bat dau tai"
4. XONG!

================================================================================
                        HO TRO & BUG REPORT
================================================================================

Neu gap loi, hay doc file tuong ung:
- Loi Gemini AI ? HUONG_DAN_GEMINI_AI.md (DOC NAY TRUOC!)
- Loi build EXE ? HUONG_DAN_BUILD_EXE.md
- Loi chay ung dung ? HUONG_DAN.md

Cac van de thuong gap:
- "ModuleNotFoundError" ? pip install -r requirements.txt
- "API key invalid" ? Kiem tra lai API key
- "Khong tim thay chu Han" ? Thu anh ro hon
- "pyinstaller not recognized" ? Doc HUONG_DAN_BUILD_EXE.md

================================================================================
                           PHIEN BAN
================================================================================

Version: 3.0 (GEMINI AI EDITION)
Update: 2025-11-02

Tinh nang:
  - GEMINI AI OCR - Nhan dang chu Han tu anh (MOI!)
  - Tai 10 anh song song (nhanh gap doi)
  - Luu nho thu muc va API key
  - Mo thu muc truc tiep
  - Giao dien ASCII (khong loi, khong emoji)
  - Cross-platform (Windows/Mac/Linux)
  - Build EXE de dang

Thay doi phien ban nay:
  - THEM tinh nang Gemini AI OCR
  - Tu dong nhan dang chu Han tu anh
  - Preview anh truoc khi xu ly
  - Luu API key tu dong
  - Giao dien lon hon de chua AI features
  - Them huong dan chi tiet ve AI

================================================================================

    TINH NANG AI TOAN TAP - KY NGUYEN MOI CUA HIEU QUA!

          CHUC BAN SU DUNG VUI VE VA HOC TOT TIENG TRUNG!

================================================================================
