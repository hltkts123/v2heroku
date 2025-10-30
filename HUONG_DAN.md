# 📝 HƯỚNG DẪN SỬ DỤNG

## ⚡ Cài đặt (3 bước đơn giản)

### Bước 1: Mở VBA Editor
- Mở PowerPoint
- Nhấn `Alt + F11`

### Bước 2: Tạo Module mới
- Menu `Insert` → `Module`

### Bước 3: Copy code
- Mở file `XoaDongTiengAnh.vba`
- Copy toàn bộ code
- Paste vào cửa sổ Module vừa tạo

---

## 🚀 Sử dụng

### Chạy macro:
1. Trong VBA Editor: Nhấn `F5` hoặc
2. PowerPoint: `View` → `Macros` → Chọn `XoaDongTiengAnh` → `Run`

### Hoàn tác (Undo):
- Chạy macro: `UndoXoaDongTiengAnh`

---

## ✅ Công cụ sẽ làm gì?

- ✓ **Giữ lại**: Dòng có ký tự tiếng Việt (á, à, ả, ã, ạ, đ, ơ, ư, v.v.)
- ✗ **Xóa**: Dòng chỉ có tiếng Anh (a-z, A-Z, số, dấu câu cơ bản)
- ✗ **Xóa luôn textbox** nếu rỗng sau khi lọc

---

## ⚠️ Lưu ý

1. **Luôn backup file** trước khi chạy
2. **Test trên file copy** trước
3. Undo chỉ khôi phục text, **không khôi phục textbox đã xóa**

---

## 🎯 Ví dụ

**Trước khi xử lý:**
```
Hello World
Xin chào Việt Nam
Good morning
Chúc buổi tối tốt lành
123 Main Street
```

**Sau khi xử lý:**
```
Xin chào Việt Nam
Chúc buổi tối tốt lành
```

---

**Chúc bạn sử dụng hiệu quả! 🎉**
