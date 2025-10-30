Option Explicit

' ===========================================================================================
' CÔNG CỤ XÓA DÒNG TIẾNG ANH - GIỮ LẠI DÒNG TIẾNG VIỆT
' 
' Cách sử dụng:
' 1. Mở PowerPoint → Alt+F11 (VBA Editor)
' 2. Insert → Module
' 3. Copy toàn bộ code này vào
' 4. Chạy macro: XoaDongTiengAnh
' ===========================================================================================

' Cấu trúc lưu hành động
Private Type ActionItem
    SlideIndex As Long
    ShapeIdPath As String
    OriginalText As String
    NewText As String
    DeleteShape As Boolean
End Type

' Biến toàn cục cho Undo
Private m_UndoActions() As ActionItem
Private m_UndoCount As Long

' ===========================================================================================
' MACRO CHÍNH - CHẠY MACRO NÀY
' ===========================================================================================
Sub XoaDongTiengAnh()
    Dim actions() As ActionItem
    Dim actionCount As Long
    Dim startTime As Double
    Dim msg As String
    Dim response As VbMsgBoxResult
    
    On Error GoTo ErrHandler
    
    ' Hỏi người dùng
    response = MsgBox("Công cụ này sẽ:" & vbCrLf & vbCrLf & _
                      "✓ XÓA các dòng chỉ chứa ký tự ASCII (tiếng Anh)" & vbCrLf & _
                      "✓ GIỮ LẠI các dòng có ký tự Unicode (tiếng Việt)" & vbCrLf & vbCrLf & _
                      "Bạn có muốn tiếp tục?", _
                      vbYesNo + vbQuestion, "Xác nhận")
    
    If response = vbNo Then Exit Sub
    
    startTime = Timer
    Application.ScreenUpdating = False
    
    ' Thu thập các thay đổi cần thực hiện
    actionCount = 0
    ReDim actions(0 To 0)
    CollectAllActions actions, actionCount
    
    If actionCount = 0 Then
        Application.ScreenUpdating = True
        MsgBox "Không tìm thấy textbox nào cần xử lý.", vbInformation
        Exit Sub
    End If
    
    ' Lưu backup cho Undo
    m_UndoCount = actionCount
    ReDim m_UndoActions(0 To actionCount - 1)
    Dim i As Long
    For i = 0 To actionCount - 1
        m_UndoActions(i) = actions(i)
    Next i
    
    ' Thực hiện xử lý
    PerformActions actions, actionCount
    
    Application.ScreenUpdating = True
    
    ' Thông báo kết quả
    Dim modified As Long, deleted As Long
    For i = 0 To actionCount - 1
        If actions(i).DeleteShape Then
            deleted = deleted + 1
        Else
            modified = modified + 1
        End If
    Next i
    
    msg = "HOÀN TẤT!" & vbCrLf & vbCrLf
    msg = msg & "✓ Textbox đã cập nhật: " & modified & vbCrLf
    msg = msg & "✓ Textbox đã xóa: " & deleted & vbCrLf
    msg = msg & "✓ Thời gian: " & Format(Timer - startTime, "0.00") & " giây" & vbCrLf & vbCrLf
    msg = msg & "Để hoàn tác, chạy macro: UndoXoaDongTiengAnh"
    
    MsgBox msg, vbInformation, "Thành công"
    Exit Sub
    
ErrHandler:
    Application.ScreenUpdating = True
    MsgBox "Lỗi: " & Err.Number & " - " & Err.Description, vbExclamation
End Sub

' ===========================================================================================
' MACRO HOÀN TÁC
' ===========================================================================================
Sub UndoXoaDongTiengAnh()
    Dim i As Long
    Dim sld As Slide
    Dim shp As Shape
    Dim restored As Long
    Dim response As VbMsgBoxResult
    
    On Error Resume Next
    
    If m_UndoCount = 0 Then
        MsgBox "Không có thao tác nào để hoàn tác.", vbInformation
        Exit Sub
    End If
    
    response = MsgBox("Bạn có chắc muốn hoàn tác " & m_UndoCount & " thay đổi?" & vbCrLf & vbCrLf & _
                      "Lưu ý: Không thể khôi phục các textbox đã bị xóa.", _
                      vbYesNo + vbQuestion, "Xác nhận Undo")
    
    If response = vbNo Then Exit Sub
    
    Application.ScreenUpdating = False
    
    ' Khôi phục text gốc
    For i = 0 To m_UndoCount - 1
        If Not m_UndoActions(i).DeleteShape Then
            Set sld = ActivePresentation.Slides(m_UndoActions(i).SlideIndex)
            Set shp = ResolveShapeByPath(sld, m_UndoActions(i).ShapeIdPath)
            
            If Not shp Is Nothing Then
                SetShapeText shp, m_UndoActions(i).OriginalText
                restored = restored + 1
            End If
        End If
    Next i
    
    Application.ScreenUpdating = True
    
    MsgBox "Đã khôi phục " & restored & " textbox.", vbInformation
    
    ' Xóa undo buffer
    m_UndoCount = 0
    Erase m_UndoActions
End Sub

' ===========================================================================================
' HÀM XỬ LÝ NỘI BỘ
' ===========================================================================================

' Thu thập tất cả các actions
Private Sub CollectAllActions(ByRef actions() As ActionItem, ByRef actionCount As Long)
    Dim sld As Slide
    Dim shp As Shape
    
    For Each sld In ActivePresentation.Slides
        For Each shp In sld.Shapes
            CollectActionsForShape sld.SlideIndex, shp, "", actions, actionCount
        Next shp
    Next sld
End Sub

' Thu thập action cho từng shape (hỗ trợ group)
Private Sub CollectActionsForShape(ByVal slideIndex As Long, _
                                    ByRef shp As Shape, _
                                    ByVal pathSoFar As String, _
                                    ByRef actions() As ActionItem, _
                                    ByRef actionCount As Long)
    Dim currentPath As String
    Dim rawText As String
    Dim newText As String
    
    On Error Resume Next
    If shp Is Nothing Then Exit Sub
    
    ' Tạo path cho shape
    If pathSoFar = "" Then
        currentPath = CStr(shp.Id)
    Else
        currentPath = pathSoFar & "/" & CStr(shp.Id)
    End If
    
    ' Xử lý group
    If shp.Type = msoGroup Then
        Dim gi As Shape
        For Each gi In shp.GroupItems
            CollectActionsForShape slideIndex, gi, currentPath, actions, actionCount
        Next gi
        Exit Sub
    End If
    
    ' Lấy text
    rawText = GetShapeText(shp)
    If Len(Trim(rawText)) = 0 Then Exit Sub
    
    ' Lọc: giữ dòng có ký tự Unicode, xóa dòng chỉ ASCII
    newText = FilterKeepUnicodeLines(rawText)
    
    ' Thêm action nếu có thay đổi
    If Len(Trim(newText)) = 0 Then
        ' Xóa shape vì rỗng
        AddAction actions, actionCount, slideIndex, currentPath, rawText, "", True
    ElseIf Not TextsEqual(rawText, newText) Then
        ' Cập nhật text
        AddAction actions, actionCount, slideIndex, currentPath, rawText, newText, False
    End If
End Sub

' Thêm action vào mảng
Private Sub AddAction(ByRef actions() As ActionItem, _
                      ByRef actionCount As Long, _
                      ByVal slideIndex As Long, _
                      ByVal path As String, _
                      ByVal originalText As String, _
                      ByVal newText As String, _
                      ByVal deleteShape As Boolean)
    actionCount = actionCount + 1
    ReDim Preserve actions(0 To actionCount - 1)
    
    With actions(actionCount - 1)
        .SlideIndex = slideIndex
        .ShapeIdPath = path
        .OriginalText = originalText
        .NewText = newText
        .DeleteShape = deleteShape
    End With
End Sub

' Thực hiện các actions
Private Sub PerformActions(ByRef actions() As ActionItem, ByVal actionCount As Long)
    Dim i As Long
    Dim sld As Slide
    Dim shp As Shape
    
    On Error Resume Next
    
    ' Cập nhật text trước
    For i = 0 To actionCount - 1
        If Not actions(i).DeleteShape Then
            Set sld = ActivePresentation.Slides(actions(i).SlideIndex)
            Set shp = ResolveShapeByPath(sld, actions(i).ShapeIdPath)
            
            If Not shp Is Nothing Then
                SetShapeText shp, actions(i).NewText
            End If
        End If
    Next i
    
    ' Xóa shapes sau (ngược từ cuối)
    For i = actionCount - 1 To 0 Step -1
        If actions(i).DeleteShape Then
            Set sld = ActivePresentation.Slides(actions(i).SlideIndex)
            Set shp = ResolveShapeByPath(sld, actions(i).ShapeIdPath)
            
            If Not shp Is Nothing Then
                shp.Delete
            End If
        End If
    Next i
End Sub

' Lấy text từ shape
Private Function GetShapeText(ByRef shp As Shape) As String
    Dim txt As String
    
    On Error Resume Next
    txt = ""
    
    If shp.HasTextFrame Then
        If shp.TextFrame.HasText Then
            txt = shp.TextFrame.TextRange.Text
        End If
    End If
    
    If Len(Trim(txt)) = 0 Then
        Err.Clear
        txt = shp.TextFrame2.TextRange.Text
    End If
    
    On Error GoTo 0
    GetShapeText = txt
End Function

' Set text cho shape
Private Sub SetShapeText(ByRef shp As Shape, ByVal txt As String)
    On Error Resume Next
    
    If shp.HasTextFrame Then
        shp.TextFrame.TextRange.Text = txt
    Else
        shp.TextFrame2.TextRange.Text = txt
    End If
    
    On Error GoTo 0
End Sub

' Lọc giữ lại dòng có Unicode (tiếng Việt)
Private Function FilterKeepUnicodeLines(ByVal txt As String) As String
    Dim normalized As String
    Dim lines() As String
    Dim i As Long
    Dim result As String
    
    ' Chuẩn hóa line breaks
    normalized = Replace(txt, vbCrLf, vbLf)
    normalized = Replace(normalized, vbCr, vbLf)
    
    lines = Split(normalized, vbLf)
    result = ""
    
    For i = LBound(lines) To UBound(lines)
        ' Giữ dòng nếu có ít nhất 1 ký tự Unicode
        If HasUnicodeChar(lines(i)) Then
            If result = "" Then
                result = lines(i)
            Else
                result = result & vbCrLf & lines(i)
            End If
        End If
    Next i
    
    FilterKeepUnicodeLines = result
End Function

' Kiểm tra dòng có ký tự Unicode không
Private Function HasUnicodeChar(ByVal line As String) As Boolean
    Dim i As Long
    Dim charCode As Long
    
    HasUnicodeChar = False
    
    If Len(Trim(line)) = 0 Then Exit Function
    
    For i = 1 To Len(line)
        charCode = AscW(Mid(line, i, 1))
        
        ' Ký tự Unicode (>127) hoặc negative (tiếng Việt có dấu)
        If charCode > 127 Or charCode < 0 Then
            HasUnicodeChar = True
            Exit Function
        End If
    Next i
End Function

' So sánh 2 text
Private Function TextsEqual(ByVal txt1 As String, ByVal txt2 As String) As Boolean
    Dim norm1 As String, norm2 As String
    
    norm1 = Replace(txt1, vbCrLf, vbLf)
    norm1 = Replace(norm1, vbCr, vbLf)
    
    norm2 = Replace(txt2, vbCrLf, vbLf)
    norm2 = Replace(norm2, vbCr, vbLf)
    
    TextsEqual = (StrComp(Trim(norm1), Trim(norm2), vbTextCompare) = 0)
End Function

' Tìm shape theo path
Private Function ResolveShapeByPath(ByRef sld As Slide, ByVal path As String) As Shape
    Dim parts() As String
    Dim curShape As Shape
    Dim curItem As Shape
    Dim i As Long
    Dim gi As Shape
    
    On Error Resume Next
    Set ResolveShapeByPath = Nothing
    
    If Len(Trim(path)) = 0 Then Exit Function
    
    parts = Split(path, "/")
    
    ' Tìm shape root
    For Each curShape In sld.Shapes
        If CStr(curShape.Id) = parts(0) Then Exit For
    Next curShape
    
    If curShape Is Nothing Then Exit Function
    
    ' Nếu chỉ 1 part
    If UBound(parts) = 0 Then
        Set ResolveShapeByPath = curShape
        Exit Function
    End If
    
    ' Duyệt group items
    For i = 1 To UBound(parts)
        Set curItem = Nothing
        
        If curShape.Type = msoGroup Then
            For Each gi In curShape.GroupItems
                If CStr(gi.Id) = parts(i) Then
                    Set curItem = gi
                    Exit For
                End If
            Next gi
        End If
        
        If curItem Is Nothing Then
            Set ResolveShapeByPath = Nothing
            Exit Function
        End If
        
        Set curShape = curItem
    Next i
    
    Set ResolveShapeByPath = curShape
End Function
