# Stroke Order Downloader - Tai Anh Thu Tu Net Chu Han

## Tinh nang moi

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
   - Loai bo ky tu trung lap tu dong
   - Thong ke ket qua (thanh cong/that bai)
   - Mau sac phan biet cac loai thong bao

6. **UI hien dai hon**
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
2. (Tuy chon) Chon thu muc luu anh khac
3. Nhan "Bat dau tai" hoac phim Enter
4. Xem ket qua trong khung ben duoi

### Vi du input:

- `????` - Cac ky tu lien nhau
- `?,?,?,?` - Cach nhau bang dau phay
- `? ? ? ?` - Cach nhau bang khoang trang
- `??,??` - Ket hop

## Thu muc mac dinh

- **Windows**: `C:\Users\<username>\Stroke_images`
- **macOS/Linux**: `~/Stroke_images`

## Yeu cau he thong

- Python 3.7+
- Ket noi internet
- Tkinter (thuong di kem voi Python)
