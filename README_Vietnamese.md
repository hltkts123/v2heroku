# 🇻🇳 Công cụ Xóa Dòng Tiếng Anh trong PowerPoint

## 📌 Giới thiệu

Đây là công cụ VBA mạnh mẽ giúp tự động xóa các dòng tiếng Anh (chỉ chứa ký tự ASCII) và giữ lại các dòng tiếng Việt (có ký tự Unicode) trong PowerPoint presentation.

### ✨ Tính năng nổi bật

- ✅ **UserForm giao diện đẹp** - Dễ sử dụng, không cần code
- ✅ **Hỗ trợ Unicode đầy đủ** - Hiển thị tiếng Việt hoàn hảo
- ✅ **Preview trước khi xử lý** - Xem trước kết quả
- ✅ **Undo/Backup** - Hoàn tác nếu cần
- ✅ **Thống kê chi tiết** - Báo cáo số liệu đầy đủ
- ✅ **Xử lý Group Shapes** - Hỗ trợ cả shapes trong group
- ✅ **Windows API** - Xử lý Unicode chuyên nghiệp

---

## 📦 Cấu trúc Files

```
📁 PowerPoint_TextCleaner/
├── 📄 PowerPoint_TextCleaner_UserForm.vba      [Module chính]
├── 📄 frmTextCleaner_Code.vba                   [UserForm code]
├── 📄 modUnicodeAPI.vba                         [Unicode API module]
├── 📄 PowerPoint_TextCleaner_Advanced.vba       [Version không UI]
├── 📄 USERFORM_DESIGN_GUIDE.md                  [Hướng dẫn thiết kế form]
└── 📄 README_Vietnamese.md                      [File này]
```

---

## 🚀 Cài đặt nhanh

### Bước 1: Mở VBA Editor

1. Mở PowerPoint
2. Nhấn `Alt + F11` để mở VBA Editor

### Bước 2: Import Modules

1. Menu `File` → `Import File...`
2. Import lần lượt:
   - `PowerPoint_TextCleaner_UserForm.vba` → Đặt tên module: `modMain`
   - `modUnicodeAPI.vba` → Giữ nguyên tên: `modUnicodeAPI`

### Bước 3: Tạo UserForm

1. Menu `Insert` → `UserForm`
2. Đặt tên: `frmTextCleaner`
3. Thiết kế form theo hướng dẫn trong file `USERFORM_DESIGN_GUIDE.md`
4. Paste code từ `frmTextCleaner_Code.vba` vào form

### Bước 4: Chạy thử

```vba
Sub Test()
    frmTextCleaner.Show
End Sub
```

Hoặc chạy macro: `ShowTextCleanerForm`

---

## 📖 Hướng dẫn sử dụng

### 🎯 Cách 1: Sử dụng UserForm (Khuyến nghị)

1. **Mở công cụ:**
   - Chạy macro `ShowTextCleanerForm`
   - Hoặc tạo button trên Ribbon gán vào macro này

2. **Chọn tùy chọn:**
   - ☑ **Preview**: Xem trước kết quả trước khi xử lý
   - ☑ **Backup**: Cho phép hoàn tác (Undo)
   - ☑ **Thống kê**: Hiển thị báo cáo chi tiết

3. **Thực hiện:**
   - Nhấn **"Bắt đầu xử lý"**
   - Nếu chọn Preview, xem kết quả và xác nhận
   - Chờ xử lý hoàn tất

4. **Hoàn tác (nếu cần):**
   - Nhấn **"Hoàn tác (Undo)"**

### 🎯 Cách 2: Chạy trực tiếp (Không UI)

```vba
' Version cơ bản
Sub XoaDongTiengAnh_Queued()
    ' Code trong file gốc
End Sub

' Version nâng cao
Sub XoaDongTiengAnh_Advanced()
    ' Code trong PowerPoint_TextCleaner_Advanced.vba
End Sub
```

---

## 🔧 Cấu hình nâng cao

### Thay đổi logic lọc

Mở module `modMain`, tìm function `ShouldKeepLine`:

```vba
Public Function ShouldKeepLine(ByVal line As String) As Boolean
    Dim ch As Long
    Dim charCode As Long
    
    ShouldKeepLine = False
    If Len(Trim(line)) = 0 Then Exit Function
    
    For ch = 1 To Len(line)
        charCode = AscW(Mid(line, ch, 1))
        
        ' TÙY CHỈNH ĐIỀU KIỆN Ở ĐÂY
        If charCode > 127 Or charCode < 0 Then
            ShouldKeepLine = True
            Exit Function
        End If
    Next ch
End Function
```

**Ví dụ tùy chỉnh:**

```vba
' Giữ dòng có ít nhất 2 ký tự Unicode
Public Function ShouldKeepLine(ByVal line As String) As Boolean
    Dim unicodeCount As Long
    unicodeCount = CountUnicodeChars(line)
    ShouldKeepLine = (unicodeCount >= 2)
End Function

' Giữ dòng có ký tự tiếng Việt cụ thể
Public Function ShouldKeepLine(ByVal line As String) As Boolean
    ShouldKeepLine = HasVietnameseText(line)
End Function
```

### Thêm xử lý đặc biệt

Trong `CollectActionsForShape`, thêm điều kiện:

```vba
' Bỏ qua shapes có tên cụ thể
If InStr(1, shapeName, "KeepThis", vbTextCompare) > 0 Then
    Exit Sub
End If

' Chỉ xử lý TextBox
If shp.Type <> msoTextBox Then
    Exit Sub
End If
```

---

## 🧪 Testing & Debug

### Test Unicode API

```vba
Sub TestUnicode()
    modUnicodeAPI.TestUnicodeAPI
End Sub
```

### Debug encoding issues

```vba
Sub DebugText()
    Dim testText As String
    testText = "Xin chào Việt Nam! Hello World"
    
    Call modUnicodeAPI.ShowEncodingInfo(testText)
End Sub
```

### Kiểm tra shape text

```vba
Sub InspectShape()
    Dim shp As Shape
    Set shp = ActiveWindow.Selection.ShapeRange(1)
    
    Debug.Print "Text: " & GetShapeTextUnicode(shp)
    Debug.Print "Has Unicode: " & HasUnicodeChars(GetShapeTextUnicode(shp))
    Debug.Print "Vietnamese chars: " & CountVietnameseChars(GetShapeTextUnicode(shp))
End Sub
```

---

## 🎨 Tùy chỉnh giao diện UserForm

### Thay đổi màu sắc

Mở `frmTextCleaner` trong Design Mode:

```vba
' Thay đổi màu button
btnProcess.BackColor = RGB(76, 175, 80)  ' Xanh lá
btnUndo.BackColor = RGB(255, 152, 0)     ' Cam
btnClose.BackColor = RGB(244, 67, 54)     ' Đỏ

' Thay đổi màu progress bar
progressBar.BackColor = RGB(33, 150, 243) ' Xanh dương
```

### Thêm logo/hình ảnh

```vba
' Thêm Image control
' Trong UserForm_Initialize:
imgLogo.Picture = LoadPicture("C:\path\to\logo.png")
imgLogo.PictureSizeMode = fmPictureSizeModeZoom
```

### Resize động

```vba
Private Sub chkPreview_Click()
    If chkPreview.Value Then
        Me.Height = 550  ' Cao hơn để hiện preview
    Else
        Me.Height = 400  ' Nhỏ gọn
    End If
End Sub
```

---

## 📊 Giải thích các thống kê

| Thống kê | Ý nghĩa |
|----------|---------|
| **Tổng số slide** | Số slide trong presentation |
| **Tổng số shape** | Tổng số shapes đã quét (bao gồm cả trong groups) |
| **Shape đã sửa** | Số textbox đã cập nhật nội dung |
| **Shape đã xóa** | Số textbox bị xóa hoàn toàn (vì rỗng sau lọc) |
| **Dòng đã xóa** | Tổng số dòng tiếng Anh bị xóa |
| **Dòng đã giữ** | Tổng số dòng tiếng Việt được giữ lại |
| **Thời gian** | Thời gian xử lý (giây hoặc ms) |

---

## ⚠️ Lưu ý quan trọng

### ✅ Những gì công cụ LÀM

- ✓ Xóa dòng chỉ có ký tự ASCII (a-z, A-Z, 0-9, dấu câu cơ bản)
- ✓ Giữ dòng có ký tự Unicode (ả, ế, ồ, ư, đ, v.v.)
- ✓ Xử lý shapes trong groups
- ✓ Backup cho Undo
- ✓ Thống kê chi tiết

### ❌ Những gì công cụ KHÔNG làm

- ✗ Không khôi phục shapes đã bị xóa (chỉ khôi phục text)
- ✗ Không xử lý hình ảnh, charts, tables
- ✗ Không thay đổi formatting (font, size, color)
- ✗ Không tự động lưu file (bạn phải Save thủ công)

### 🔒 An toàn

- **Luôn backup file** trước khi chạy công cụ
- **Test trên file copy** trước khi dùng trên file chính
- **Bật tùy chọn Preview** để kiểm tra trước
- **Bật tùy chọn Backup** để có thể Undo

---

## 🐛 Troubleshooting

### ❌ Lỗi: "User-defined type not defined"

**Nguyên nhân:** Thiếu module hoặc Type definition

**Giải pháp:**
1. Kiểm tra đã import đủ 2 modules (`modMain` và `modUnicodeAPI`)
2. Đảm bảo `ActionItem` và `Statistics` được khai báo ở đầu `modMain`

### ❌ Lỗi: "Object doesn't support this property or method"

**Nguyên nhân:** Office version không tương thích

**Giải pháp:**
```vba
' Thay đổi API declarations thành 32-bit nếu dùng Office cũ
' Xóa "PtrSafe" và đổi "LongPtr" thành "Long"
```

### ❌ Tiếng Việt hiển thị "??????" hoặc "□□□"

**Nguyên nhân:** Font không hỗ trợ Unicode

**Giải pháp:**
1. Đổi font UserForm sang `Arial` hoặc `Segoe UI`
2. Kiểm tra PowerPoint file encoding
3. Chạy `TestUnicodeAPI` để debug

### ❌ Lỗi: "Run-time error '424': Object required"

**Nguyên nhân:** Thiếu UserForm hoặc tên sai

**Giải pháp:**
1. Kiểm tra tên UserForm phải là `frmTextCleaner`
2. Đảm bảo đã paste code vào form
3. Check tên controls khớp với code

### ❌ Preview không hiển thị

**Nguyên nhân:** Controls bị ẩn hoặc vị trí sai

**Giải pháp:**
```vba
' Trong UserForm_Initialize, thêm:
txtPreview.Visible = False
lblPreviewTitle.Visible = False

' Trong ShowPreview, set:
txtPreview.Visible = True
lblPreviewTitle.Visible = True
```

### ❌ Undo không hoạt động

**Nguyên nhân:** 
- Shapes đã bị xóa không thể khôi phục
- Không bật option Backup

**Giải pháp:**
- Undo chỉ khôi phục text, không khôi phục shapes đã xóa
- Luôn bật checkbox "Tạo backup để Undo"
- Backup file trước khi xử lý

---

## 🔬 Advanced Usage

### Export log ra file

```vba
Sub ExportLog()
    Dim fso As Object
    Dim file As Object
    Dim logPath As String
    Dim logContent As String
    
    Set fso = CreateObject("Scripting.FileSystemObject")
    logPath = Environ("USERPROFILE") & "\Desktop\TextCleaner_Log.txt"
    
    logContent = "=== TEXT CLEANER LOG ===" & vbCrLf
    logContent = logContent & "Date: " & Now & vbCrLf & vbCrLf
    logContent = logContent & "Slides: " & g_Stats.TotalSlides & vbCrLf
    logContent = logContent & "Shapes Modified: " & g_Stats.ShapesModified & vbCrLf
    logContent = logContent & "Shapes Deleted: " & g_Stats.ShapesDeleted & vbCrLf
    
    Set file = fso.CreateTextFile(logPath, True, True)
    file.Write logContent
    file.Close
    
    MsgBox "Log saved to: " & logPath, vbInformation
End Sub
```

### Batch processing nhiều files

```vba
Sub ProcessMultipleFiles()
    Dim fso As Object
    Dim folder As Object
    Dim file As Object
    Dim ppt As Object
    Dim folderPath As String
    
    Set fso = CreateObject("Scripting.FileSystemObject")
    Set ppt = CreateObject("PowerPoint.Application")
    
    folderPath = "C:\Path\To\Presentations\"
    Set folder = fso.GetFolder(folderPath)
    
    For Each file In folder.Files
        If LCase(fso.GetExtensionName(file.Name)) = "pptx" Then
            Dim pres As Presentation
            Set pres = ppt.Presentations.Open(file.Path)
            
            ' Process
            ' ... (code xử lý)
            
            pres.Save
            pres.Close
        End If
    Next file
    
    ppt.Quit
    MsgBox "Batch processing complete!", vbInformation
End Sub
```

---

## 📞 Hỗ trợ & Đóng góp

### Báo lỗi

Nếu gặp lỗi, vui lòng cung cấp:
1. Phiên bản Office/PowerPoint
2. Thông báo lỗi chi tiết
3. Steps để reproduce lỗi
4. Screenshot (nếu có)

### Đề xuất tính năng

Bạn có thể đề xuất:
- Thêm tùy chọn lọc mới
- Cải thiện giao diện
- Thêm shortcuts/hotkeys
- Export/Import settings

---

## 📝 Changelog

### Version 2.0 (2025-10-30)
- ✅ Thêm UserForm giao diện
- ✅ Hỗ trợ Unicode API đầy đủ
- ✅ Thêm Preview mode
- ✅ Thêm Undo functionality
- ✅ Thêm thống kê chi tiết
- ✅ Cải thiện error handling

### Version 1.0 (Initial)
- ✅ Chức năng cơ bản xóa dòng ASCII
- ✅ Hỗ trợ group shapes
- ✅ Queue-based processing

---

## 📄 License

MIT License - Sử dụng tự do cho mục đích cá nhân và thương mại.

---

## 🙏 Credits

Phát triển bởi: AI Assistant (Claude)  
Ngôn ngữ: VBA (Visual Basic for Applications)  
Platform: Microsoft PowerPoint 2010+

---

**Chúc bạn sử dụng hiệu quả! 🎉**
