# CẬP NHẬT v3.2 - KHẮC PHỤC LỌC TEXT & LAYOUT

## 🎯 CÁC VẤN ĐỀ ĐÃ KHẮC PHỤC

### 1. **Logic lọc text CHÍNH XÁC hơn**

#### ❌ **Vấn đề cũ:**
- Code xóa nhầm tiếng Trung, tiếng Nhật, hoặc các ký tự đặc biệt
- Không giữ định dạng của các ngôn ngữ Unicode khác tiếng Việt

#### ✅ **Đã sửa:**
```python
def delete_english_lines(text):
    """XOA CHI dong tieng Anh (pure ASCII)
       GIU tat ca dong co Unicode (Viet, Trung, Nhat, Han, Emoji...)
    """
    lines = text.split('\n')
    result = []
    
    for line in lines:
        # Dong rong -> giu lai
        if not line.strip():
            result.append(line)
            continue
        
        # Dong co it nhat 1 ky tu Unicode (ord > 127) -> GIU
        if any(ord(char) > 127 for char in line):
            result.append(line)
        # Dong PURE ASCII (chi a-z, A-Z, 0-9, punctuation) -> XOA
    
    return '\n'.join(result)
```

**Logic mới:**
- ✅ Dòng có ít nhất 1 ký tự Unicode (>127) → **GIỮ LẠI**
  - Tiếng Việt: á, é, ô, ơ, ư, đ...
  - Tiếng Trung: 中文, 汉字...
  - Tiếng Nhật: ひらがな, カタカナ, 漢字...
  - Tiếng Hàn: 한글...
  - Emoji: 😀, ✓, ★...
- ❌ Dòng PURE ASCII (0-127) → **XÓA**
  - Tiếng Anh: "Hello World", "Made in USA"...
  - Số và dấu câu đơn: "123", "Test"...

---

### 2. **Layout tối ưu - KHÔNG CẦN SCROLLBAR**

#### ❌ **Vấn đề cũ:**
- Cửa sổ quá cao → Cần scrollbar
- Nút "Xử lý file" bị che khuất
- Tabs tràn ra ngoài

#### ✅ **Đã sửa:**

**Kích thước mới:**
| Tool | Kích thước | Tối thiểu |
|------|-----------|-----------|
| Single file | 900x720 | 850x680 |
| Batch | 950x750 | 900x720 |

**Layout tối ưu:**
```
┌─────────────────────────────────┐
│ Header (60px, compact)          │
├─────────────────────────────────┤
│ 1. Chon file (compact)          │
│ 2. Chuc nang (compact)          │
│ [Tab: Xoa anh] [Tab: Loc text] │ ← Vừa vặn
│   Nội dung tab...               │
│ Tuy chon + Tien trinh (1 row)  │ ← Gộp lại
│ [▶ XU LY FILE] (luon hien thi) │ ← Nút lớn
└─────────────────────────────────┘
  Status bar (compact)
```

**Cải tiến:**
- ✅ **KHÔNG cần scrollbar** - Tất cả hiển thị vừa vặn
- ✅ Font nhỏ hơn (8-10px) → Tiết kiệm không gian
- ✅ Padding/margin giảm → Compact hơn
- ✅ Options + Progress cùng 1 hàng → Tiết kiệm 50px
- ✅ Tabs gọn gàng, nội dung vừa đủ
- ✅ Nút "Xử lý file" LUÔN hiển thị ở dưới

---

### 3. **Xóa textbox rỗng**

#### ✅ **Tính năng:**
- Sau khi lọc text, nếu textbox trống → Tự động XÓA textbox
- Có checkbox để bật/tắt tính năng này
- Giúp presentation gọn gàng, không có textbox thừa

---

## 📋 CHẾ ĐỘ LỌC TEXT MỚI

### **Mode 1: Xóa tiếng Anh - Giữ Việt/Trung/Nhật/Hàn** (Mặc định)

**Input:**
```
Hello World
Xin chào
中文测试
こんにちは
안녕하세요
Test 123
Tiếng Việt có dấu
```

**Output:**
```
Xin chào
中文测试
こんにちは
안녕하세요
Tiếng Việt có dấu
```

**Giải thích:**
- ❌ Xóa: "Hello World" (pure English)
- ❌ Xóa: "Test 123" (pure ASCII)
- ✅ Giữ: Tất cả dòng có Unicode

---

### **Mode 2: Chỉ giữ tiếng Anh**

**Input:**
```
Hello World
Xin chào
中文测试
Test 123
```

**Output:**
```
Hello World
Test 123
```

---

### **Mode 3: Xóa tất cả text**

**Input:** (bất kỳ)

**Output:** (rỗng, textbox bị xóa nếu bật option)

---

## 🔧 CHI TIẾT KỸ THUẬT

### Thuật toán phát hiện tiếng Anh

```python
def is_pure_english(line):
    """Kiểm tra dòng có phải PURE ASCII (tiếng Anh) không"""
    if not line.strip():
        return False
    
    # Nếu có BẤT KỲ ký tự nào > 127 → KHÔNG phải pure English
    return all(ord(char) <= 127 for char in line)
```

**Ví dụ:**
- `"Hello World"` → ord('H')=72, ord('o')=111... → Tất cả ≤127 → **Pure English** → Xóa
- `"Xin chào"` → ord('à')=224 → >127 → **NOT Pure English** → Giữ
- `"中文"` → ord('中')=20013 → >127 → **NOT Pure English** → Giữ

### Bảng mã Unicode

| Loại | Range | Ví dụ |
|------|-------|-------|
| ASCII | 0-127 | a-z, A-Z, 0-9 |
| Latin Extended | 128-255 | á, é, ô, đ |
| CJK (Trung/Nhật) | 0x4E00-0x9FFF | 中文, 漢字 |
| Hangul (Hàn) | 0xAC00-0xD7AF | 한글 |
| Emoji | 0x1F600+ | 😀, 🎉 |

---

## 📊 SO SÁNH TRƯỚC/SAU

### Trường hợp 1: Textbox hỗn hợp

**Before:**
```
Welcome to our company
Công ty XYZ
中国分公司
Contact: info@example.com
```

**After (Mode: Xóa tiếng Anh):**
```
Công ty XYZ
中国分公司
```

**Giải thích:**
- ❌ Xóa "Welcome..." (pure English)
- ✅ Giữ "Công ty XYZ" (có Unicode: ô, y with hook)
- ✅ Giữ "中国分公司" (Chinese)
- ❌ Xóa "Contact:..." (pure ASCII)

---

### Trường hợp 2: Textbox trong Group

**Slide structure:**
```
Slide
└─ Group 1
   ├─ TextBox A: "Product Name" (English)
   ├─ TextBox B: "Tên sản phẩm" (Vietnamese)
   └─ TextBox C: "产品名称" (Chinese)
```

**After processing:**
```
Slide
└─ Group 1
   ├─ TextBox B: "Tên sản phẩm"
   └─ TextBox C: "产品名称"
```

**Kết quả:**
- ❌ TextBox A bị xóa (empty → deleted if option checked)
- ✅ TextBox B giữ nguyên
- ✅ TextBox C giữ nguyên

---

## 🎯 DEMO THỰC TẾ

### Case 1: Presentation đa ngôn ngữ

**Tình huống:**
- Slide có text tiếng Anh, Việt, Trung
- Chỉ muốn xóa tiếng Anh, giữ Việt + Trung

**Cấu hình:**
```
Mode: "CHI loc text"
Chế độ: "Xóa tiếng Anh - Giữ Việt/Trung/Nhật/Hàn"
☑ Xóa textbox rỗng sau khi lọc
```

**Kết quả:**
- ✅ Xóa sạch tất cả dòng tiếng Anh
- ✅ Giữ nguyên tiếng Việt
- ✅ Giữ nguyên tiếng Trung
- ✅ Xóa textbox nếu rỗng

---

### Case 2: Chỉ giữ tiếng Anh (dịch ngược)

**Tình huống:**
- Có presentation song ngữ Việt-Anh
- Chỉ muốn giữ phiên bản tiếng Anh

**Cấu hình:**
```
Mode: "CHI loc text"
Chế độ: "Chi giu tieng Anh"
☑ Xóa textbox rỗng
```

**Kết quả:**
- ✅ Giữ tất cả dòng tiếng Anh
- ❌ Xóa tất cả dòng tiếng Việt/Trung/Nhật...

---

## ✅ KIỂM TRA

### Test 1: Mở tool
1. Chạy `run.bat` hoặc `run_batch.bat`
2. **Kiểm tra:** Tất cả nội dung hiển thị vừa vặn?
3. **Kiểm tra:** Thấy nút "▶ XU LY FILE" ở dưới?
4. **Kết quả:** ✅ KHÔNG cần cuộn, tất cả hiển thị

### Test 2: Xóa tiếng Anh
1. Tạo file test với text:
   ```
   Hello
   Xin chào
   中文
   ```
2. Chọn mode "Xóa tiếng Anh"
3. Xử lý
4. **Kết quả:** Chỉ còn "Xin chào" và "中文"

### Test 3: Textbox trong group
1. Tạo group chứa textbox tiếng Anh
2. Xử lý với mode "Xóa tiếng Anh"
3. **Kết quả:** Textbox trong group cũng bị xử lý

---

## 📦 CÀI ĐẶT

**File:** `PowerPoint_Cleaner_v3.2_FINAL.zip`

**Nội dung:**
- ✅ `ppt_cleaner.py` (v3.2)
- ✅ `ppt_cleaner_batch.py` (v3.2)
- ✅ `CAP_NHAT_v3.2.md` ← File này
- ✅ Các file khác giữ nguyên

**Cài đặt:**
```bash
# Windows
1. Giải nén ZIP
2. Double click: install.bat
3. Double click: run.bat hoặc run_batch.bat

# Mac/Linux
1. Giải nén ZIP
2. Terminal: bash install.sh
3. Terminal: bash run.sh hoặc bash run_batch.sh
```

---

## ❓ FAQ

**Q: Tại sao tiếng Trung/Nhật bị xóa ở version cũ?**
A: Version cũ có bug logic. Version 3.2 đã sửa: Chỉ xóa dòng PURE ASCII (tiếng Anh).

**Q: Emoji có bị xóa không?**
A: KHÔNG. Emoji là Unicode (>127) nên được giữ lại khi chọn mode "Xóa tiếng Anh".

**Q: Số và ký tự đặc biệt (123, @#$) có bị xóa không?**
A: Có, nếu dòng CHỈ chứa ASCII. Ví dụ: "123" sẽ bị xóa, nhưng "Số 123" (có Unicode) sẽ được giữ.

**Q: Có thể xóa chọn lọc tiếng Trung mà giữ tiếng Việt không?**
A: Chưa hỗ trợ. Version hiện tại chỉ phân biệt ASCII vs Unicode.

**Q: Layout có responsive không khi resize cửa sổ?**
A: Có. Cửa sổ có thể resize, nội dung tự động điều chỉnh. Không còn scrollbar.

---

## 📝 CHANGELOG v3.2

```
[2025-11-02] Version 3.2 - Bug Fixes & Layout Optimization

  🐛 FIX: Logic lọc text bị xóa nhầm tiếng Trung/Nhật/Hàn
  🐛 FIX: Không giữ định dạng của các ngôn ngữ Unicode
  ✨ NEW: Xóa CHÍNH XÁC chỉ dòng pure ASCII (tiếng Anh)
  ✨ NEW: Giữ TẤT CẢ dòng có Unicode (Việt/Trung/Nhật/Hàn/Emoji)
  ⚡ IMPROVE: Layout compact, KHÔNG cần scrollbar
  ⚡ IMPROVE: Kích thước 900x720 (single), 950x750 (batch)
  ⚡ IMPROVE: Tabs và nút luôn hiển thị vừa vặn
  📖 DOCS: Thêm giải thích chi tiết về thuật toán lọc
```

---

**Version:** 3.2
**Ngày:** 2025-11-02
**Tương thích:** Windows, macOS, Linux
**Yêu cầu:** Python 3.6+, python-pptx
