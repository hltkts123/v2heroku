# 📋 Hướng dẫn thiết kế UserForm cho PowerPoint Text Cleaner

## 🎨 THIẾT KẾ USERFORM

### 1️⃣ Tạo UserForm mới trong VBA Editor

1. Mở PowerPoint → Nhấn `Alt + F11` (mở VBA Editor)
2. Menu `Insert` → `UserForm`
3. Đặt tên form: `frmTextCleaner`

### 2️⃣ Thuộc tính của UserForm

```
Name: frmTextCleaner
Caption: Công cụ dọn dẹp Text
Width: 480
Height: 520
StartUpPosition: 1 - CenterOwner
ShowModal: True
Font: Segoe UI, 10
```

---

## 🧩 CÁC CONTROL CẦN THÊM

### ✅ GROUP 1: HEADER (Top)

**Label - lblTitle**
```
Name: lblTitle
Caption: CÔNG CỤ XÓA DÒNG TIẾNG ANH
Left: 20
Top: 10
Width: 420
Height: 25
Font: Segoe UI, 14, Bold
ForeColor: #0066CC
TextAlign: 2 - fmTextAlignCenter
```

**Label - lblDescription**
```
Name: lblDescription
Caption: Công cụ này sẽ xóa các dòng chỉ chứa ký tự ASCII...
Left: 20
Top: 40
Width: 420
Height: 40
Font: Segoe UI, 9
ForeColor: #666666
WordWrap: True
```

---

### ✅ GROUP 2: OPTIONS

**Frame - frameOptions**
```
Name: frameOptions
Caption: (empty)
Left: 20
Top: 90
Width: 420
Height: 80
```

**Label - lblOptions** (inside frameOptions)
```
Name: lblOptions
Caption: TÙY CHỌN XỬ LÝ:
Left: 10
Top: 5
Width: 150
Height: 18
Font: Segoe UI, 9, Bold
```

**CheckBox - chkPreview** (inside frameOptions)
```
Name: chkPreview
Caption: ✓ Xem trước kết quả (Preview)
Left: 15
Top: 25
Width: 200
Height: 18
Value: True
```

**CheckBox - chkBackup** (inside frameOptions)
```
Name: chkBackup
Caption: ✓ Tạo backup để có thể Undo
Left: 15
Top: 45
Width: 200
Height: 18
Value: True
```

**CheckBox - chkShowStats** (inside frameOptions)
```
Name: chkShowStats
Caption: ✓ Hiển thị thống kê chi tiết
Left: 220
Top: 25
Width: 180
Height: 18
Value: True
```

---

### ✅ GROUP 3: PROGRESS

**Frame - frameProgress** (container cho progress bar)
```
Name: frameProgress
Caption: (empty)
Left: 20
Top: 180
Width: 420
Height: 20
BorderStyle: 1 - fmBorderStyleSingle
BorderColor: #CCCCCC
SpecialEffect: 2 - fmSpecialEffectSunken
```

**Label - progressBar** (inside frameProgress - dùng làm progress bar)
```
Name: progressBar
Caption: (empty)
Left: 2
Top: 2
Width: 0  (sẽ thay đổi khi xử lý)
Height: 16
BackColor: #4CAF50
```

**Label - lblProgress**
```
Name: lblProgress
Caption: Trạng thái: Chưa xử lý
Left: 20
Top: 205
Width: 420
Height: 18
Font: Segoe UI, 9
ForeColor: #333333
```

---

### ✅ GROUP 4: PREVIEW AREA

**Label - lblPreviewTitle**
```
Name: lblPreviewTitle
Caption: === XEM TRƯỚC KẾT QUẢ ===
Left: 20
Top: 230
Width: 420
Height: 18
Font: Segoe UI, 9, Bold
Visible: False
```

**TextBox - txtPreview**
```
Name: txtPreview
Text: (empty)
Left: 20
Top: 250
Width: 420
Height: 120
MultiLine: True
ScrollBars: 2 - fmScrollBarsVertical
Locked: True
Font: Consolas, 9
BackColor: #F5F5F5
Visible: False
```

---

### ✅ GROUP 5: STATISTICS

**Label - lblStats**
```
Name: lblStats
Caption: (empty)
Left: 20
Top: 380
Width: 420
Height: 80
Font: Consolas, 9
ForeColor: #006600
```

---

### ✅ GROUP 6: BUTTONS (Bottom)

**CommandButton - btnProcess**
```
Name: btnProcess
Caption: ▶ Bắt đầu xử lý
Left: 20
Top: 470
Width: 120
Height: 30
Font: Segoe UI, 10, Bold
BackColor: #4CAF50
ForeColor: #FFFFFF
```

**CommandButton - btnUndo**
```
Name: btnUndo
Caption: ◀ Hoàn tác (Undo)
Left: 150
Top: 470
Width: 120
Height: 30
Font: Segoe UI, 10
Enabled: False
```

**CommandButton - btnHelp**
```
Name: btnHelp
Caption: ❓ Trợ giúp
Left: 280
Top: 470
Width: 80
Height: 30
Font: Segoe UI, 10
```

**CommandButton - btnClose**
```
Name: btnClose
Caption: ✖ Đóng
Left: 370
Top: 470
Width: 70
Height: 30
Font: Segoe UI, 10
```

---

## 📦 IMPORT CODE VÀO FORM

### Bước 1: Copy code từ file

1. Mở file `PowerPoint_TextCleaner_UserForm.vba` → Copy toàn bộ code module chính
2. Trong VBA Editor: Menu `Insert` → `Module`
3. Đặt tên module: `modMain`
4. Paste code vào

### Bước 2: Import UserForm code

1. Mở file `frmTextCleaner_Code.vba` → Copy toàn bộ code
2. Double-click vào `frmTextCleaner` trong Project Explorer
3. Paste code vào cửa sổ code của form

---

## 🎨 MÀU SẮC KHUYẾN NGHỊ

```
Primary Color:   #0066CC (Xanh dương chủ đạo)
Success Color:   #4CAF50 (Xanh lá - thành công)
Warning Color:   #FF9800 (Cam - cảnh báo)
Error Color:     #F44336 (Đỏ - lỗi)
Text Primary:    #333333 (Chữ chính)
Text Secondary:  #666666 (Chữ phụ)
Background:      #FFFFFF (Nền trắng)
Border:          #CCCCCC (Viền xám nhạt)
```

---

## 🚀 CHẠY THỬ

### Cách 1: Từ VBA Editor
```vba
Sub Test()
    frmTextCleaner.Show
End Sub
```

### Cách 2: Tạo button trên Ribbon
1. Developer Tab → Controls → Insert Button
2. Gán macro: `ShowTextCleanerForm`

### Cách 3: Keyboard shortcut
1. Trong VBA: Tools → Macros
2. Chọn `ShowTextCleanerForm`
3. Options → Gán phím tắt (ví dụ: Ctrl+Shift+T)

---

## 🔧 TROUBLESHOOTING

### ❌ Lỗi: "Font không tồn tại"
**Giải pháp:** Đổi font sang `Arial` hoặc `Tahoma`

### ❌ Tiếng Việt bị lỗi font
**Giải pháp:** 
- Đảm bảo file PowerPoint được lưu với encoding UTF-8
- Sử dụng font hỗ trợ Unicode (Arial, Segoe UI, Times New Roman)

### ❌ Form bị lỗi khi mở
**Giải pháp:**
1. Kiểm tra tên controls có khớp với code không
2. Kiểm tra các module đã được import đầy đủ
3. Check `Tools` → `References` - bỏ check các library bị lỗi

### ❌ Preview không hiển thị
**Giải pháp:** 
- Kiểm tra `txtPreview.Visible = True` trong code
- Check height của form có đủ lớn không

---

## 📸 LAYOUT MINH HỌA

```
┌─────────────────────────────────────────────────┐
│          CÔNG CỤ XÓA DÒNG TIẾNG ANH            │
│  Công cụ này sẽ xóa các dòng chỉ chứa ASCII... │
├─────────────────────────────────────────────────┤
│ TÙY CHỌN XỬ LÝ:                                │
│ ☑ Xem trước kết quả      ☑ Hiển thị thống kê   │
│ ☑ Tạo backup để Undo                           │
├─────────────────────────────────────────────────┤
│ [███████░░░░░░░░░░░░░░░░░░] 30%               │
│ Trạng thái: Đang quét presentation...          │
├─────────────────────────────────────────────────┤
│ === XEM TRƯỚC KẾT QUẢ ===                      │
│ ┌─────────────────────────────────────────┐   │
│ │ [Slide 1] TextBox1: CẬP NHẬT            │   │
│ │   Trước: Hello World                    │   │
│ │   Sau:   Xin chào                       │   │
│ │ [Slide 2] TextBox2: XÓA                 │   │
│ └─────────────────────────────────────────┘   │
├─────────────────────────────────────────────────┤
│ === THỐNG KÊ XỬ LÝ ===                         │
│ Tổng số slide: 10                              │
│ Shape đã sửa: 15                               │
│ Dòng đã xóa: 45                                │
├─────────────────────────────────────────────────┤
│ [▶ Bắt đầu] [◀ Undo] [❓ Trợ giúp] [✖ Đóng]   │
└─────────────────────────────────────────────────┘
```

---

## 💡 MẸO NÂNG CAO

### 1. Thêm icon cho buttons
```vba
' Sử dụng Picture property của CommandButton
btnProcess.Picture = LoadPicture("C:\path\to\play.bmp")
btnProcess.PicturePosition = fmPicturePositionLeftCenter
```

### 2. Animation progress bar
```vba
' Trong code, update dần dần:
For i = 0 To 100 Step 5
    progressBar.Width = frameProgress.Width * i / 100
    DoEvents
    Sleep 50  ' Cần API Sleep
Next
```

### 3. Tooltip cho controls
```vba
' Sử dụng ControlTipText property
chkPreview.ControlTipText = "Hiển thị preview trước khi xử lý"
```

---

## 📞 HỖ TRỢ

Nếu gặp vấn đề, kiểm tra:
1. ✅ Tất cả tên controls khớp với code
2. ✅ Module `modMain` đã được import
3. ✅ UserForm code đã được paste vào form
4. ✅ References không bị lỗi (Tools → References)
5. ✅ Font hỗ trợ Unicode

---

**Phiên bản:** 2.0  
**Ngày cập nhật:** 2025-10-30  
**Tương thích:** PowerPoint 2010 trở lên
