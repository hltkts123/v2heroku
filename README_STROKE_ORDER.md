# Stroke Order Downloader - Tai Anh Thu Tu Net Chu Han

## Tinh nang moi (phien ban 2.0)

### ? Cai tien so voi phien ban cu:

1. **Da luong (Multi-threading)**
   - Tai nhieu anh song song (toi da 5 anh cung luc)
   - UI khong bi dong bang trong khi tai
   - Toc do tai nhanh hon dang ke

2. **Thanh tien trinh (Progress Bar)**
   - Hien thi tien do tai anh
   - Cho biet so luong anh da xu ly

3. **To chuc code tot hon**
   - Su dung OOP voi classes ro rang
   - Type hints cho Python hien dai
   - De bao tri va mo rong

4. **Cross-platform**
   - Hoat dong tot tren Windows, macOS, va Linux
   - Thu muc mac dinh tu dong dieu chinh theo he dieu hanh

5. **Tinh nang moi**
   - Nut **Huy** de dung qua trinh tai
   - Nut **Mo thu muc** de mo folder chua anh
   - **Luu nho thu muc** da chon trong lan su dung gan nhat
   - Loai bo ky tu trung lap tu dong
   - Thong ke ket qua (thanh cong/that bai)
   - Mau sac phan biet cac loai thong bao

6. **UI hien dai hon**
   - Su dung icon/emoji dep mat
   - Su dung ttk widgets (giao dien dep hon)
   - Scrollbar cho khu vuc ket qua
   - Layout duoc to chuc tot hon
   - Ho tro phim Enter de bat dau tai

7. **Error Handling tot hon**
   - Xu ly loi chi tiet va ro rang
   - Session management cho requests
   - Timeout handling

## Cai dat

```bash
pip install -r requirements.txt
```

## Su dung

```bash
python stroke_order_downloader.py
```

### Huong dan:

1. Nhap cac ky tu tieng Trung vao o nhap lieu
2. (Tuy chon) Chon thu muc luu anh khac bang nut **?? Chon**
3. (Tuy chon) Mo thu muc hien tai bang nut **??? Mo**
4. Nhan **?? Bat dau tai** hoac phim Enter
5. Xem ket qua trong khung ben duoi

### Vi du input:

- `????` - Cac ky tu lien nhau
- `?,?,?,?` - Cach nhau bang dau phay
- `? ? ? ?` - Cach nhau bang khoang trang
- `??,??` - Ket hop

## Thu muc mac dinh

- **Windows**: `C:\Users\<username>\Stroke_images`
- **macOS/Linux**: `~/Stroke_images`

## Luu nho cau hinh

Ung dung tu dong luu thu muc ban chon vao file config:
- File config: `~/.stroke_order_config.json`
- Lan sau mo lai, ung dung se tu dong su dung thu muc da chon truoc do
- Neu thu muc khong con ton tai, se quay ve thu muc mac dinh

## Yeu cau he thong

- Python 3.7+
- Ket noi internet
- Tkinter (thuong di kem voi Python)

## Icon va ky hieu

- ? - Thanh cong
- ? - Loi
- ?? - Canh bao
- ?? - Thong tin
- ?? - Thu muc
- ?? - Bat dau
- ?? - Huy
- ?? - Tam dung
- ?? - Hoan thanh
- ?? - Thong ke
- ? - Dang xu ly
- ??? - Mo thu muc
- ?? - Chon thu muc
