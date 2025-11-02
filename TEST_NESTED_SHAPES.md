# KIỂM TRA TÍNH NĂNG XỬ LÝ NESTED SHAPES

## Cách test xử lý đệ quy

### 1. Tạo PowerPoint test

```
Slide 1:
├── TextBox 1: "Hello World" (Tiếng Anh - ngoài)
├── TextBox 2: "Xin chào" (Tiếng Việt - ngoài)
└── Group 1
    ├── TextBox 3: "English text" (Tiếng Anh - trong group)
    ├── TextBox 4: "Tiếng Việt" (Tiếng Việt - trong group)
    └── Group 1.1 (nested)
        ├── TextBox 5: "Nested English" (Tiếng Anh - nested)
        └── TextBox 6: "Nested Việt" (Tiếng Việt - nested)
```

### 2. Chạy tool với chế độ "Giữ tiếng Việt"

### 3. Kết quả mong đợi

**Version cũ (sai):**
- ❌ Xóa: TextBox 1 ✓
- ✅ Giữ: TextBox 2 ✓
- ⚠️ BỎ QUA: TextBox 3, 4, 5, 6 (không xử lý được)

**Version 3.0 (đúng):**
- ❌ Xóa: TextBox 1 (English - ngoài)
- ✅ Giữ: TextBox 2 (Việt - ngoài)
- ❌ Xóa: TextBox 3 (English - trong group)
- ✅ Giữ: TextBox 4 (Việt - trong group)
- ❌ Xóa: TextBox 5 (English - nested)
- ✅ Giữ: TextBox 6 (Việt - nested)

---

## Code để test

### Python test script

```python
from pptx import Presentation
from pptx.util import Inches

# Create test presentation
prs = Presentation()
slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank

# Add textboxes
left = Inches(1)
top = Inches(1)
width = Inches(3)
height = Inches(0.5)

# TextBox 1 - English (outside)
tb1 = slide.shapes.add_textbox(left, top, width, height)
tb1.text = "Hello World"

# TextBox 2 - Vietnamese (outside)
tb2 = slide.shapes.add_textbox(left, top + Inches(0.7), width, height)
tb2.text = "Xin chào"

# Create Group 1
# (PowerPoint groups must be created manually in PowerPoint)
# But you can verify the tool processes existing groups

prs.save('test_nested.pptx')
print("Test file created: test_nested.pptx")
print("Manually create groups in PowerPoint, then run the cleaner")
```

---

## So sánh kết quả

| Tình huống | Version cũ | Version 3.0 |
|-----------|------------|-------------|
| TextBox ngoài | ✅ Xử lý | ✅ Xử lý |
| TextBox trong Group | ❌ Bỏ qua | ✅ Xử lý |
| TextBox trong Nested Group | ❌ Bỏ qua | ✅ Xử lý |
| Group nhiều cấp | ❌ Bỏ qua | ✅ Xử lý |
| Hiệu suất | 50% | 100% |

---

## Debug mode

Để xem chi tiết quá trình xử lý, thêm print statements:

```python
def collect_text_changes(self, shapes, changes, level=0):
    indent = "  " * level
    for shape in shapes:
        try:
            if shape.shape_type == MSO_SHAPE_TYPE.GROUP:
                print(f"{indent}[GROUP] Processing group at level {level}")
                self.collect_text_changes(shape.shapes, changes, level+1)
                continue
            
            if self.has_text(shape):
                print(f"{indent}[TEXT] Found textbox: {shape.text[:20]}...")
                # ... rest of logic
        except Exception as e:
            print(f"{indent}[ERROR] {e}")
```

Output sẽ trông như:
```
[TEXT] Found textbox: Hello World...
[TEXT] Found textbox: Xin chào...
[GROUP] Processing group at level 0
  [TEXT] Found textbox: English text...
  [TEXT] Found textbox: Tiếng Việt...
  [GROUP] Processing group at level 1
    [TEXT] Found textbox: Nested English...
    [TEXT] Found textbox: Nested Việt...
```

---

## Lưu ý

1. PowerPoint groups phải được tạo trong PowerPoint (Ctrl+G)
2. python-pptx đọc groups nhưng không tạo được
3. Test file phải có group thật mới verify được tính năng
4. Kiểm tra Result Window để xem số lượng textbox đã xử lý

