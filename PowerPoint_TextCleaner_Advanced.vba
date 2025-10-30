Option Explicit

' ===========================
' MODULE: PowerPoint Text Cleaner - Advanced Version
' Mô tả: Xóa các dòng chỉ chứa ký tự ASCII, giữ lại dòng có Unicode (tiếng Việt)
' Phiên bản: 2.0 - Nâng cấp với nhiều tính năng mới
' ===========================

' Cấu trúc lưu trữ hành động
Private Type ActionItem
    SlideIndex As Long
    ShapeIdPath As String
    OriginalText As String      ' Backup text gốc để undo
    NewText As String
    DeleteShape As Boolean
    ShapeName As String         ' Tên shape để dễ debug
End Type

' Cấu trúc lưu trữ thống kê
Private Type Statistics
    TotalSlides As Long
    TotalShapes As Long
    ShapesModified As Long
    ShapesDeleted As Long
    LinesRemoved As Long
    LinesKept As Long
End Type

' Biến toàn cục cho undo
Private m_UndoActions() As ActionItem
Private m_UndoCount As Long
Private m_Stats As Statistics

' ===========================
' MAIN ENTRY POINT
' ===========================
Sub XoaDongTiengAnh_Advanced()
    Dim userChoice As VbMsgBoxResult
    Dim startTime As Double
    Dim elapsedTime As Double
    
    startTime = Timer
    
    ' Hỏi người dùng có muốn preview không
    userChoice = MsgBox("Bạn có muốn xem preview trước khi thực hiện không?" & vbCrLf & vbCrLf & _
                        "Yes = Xem preview" & vbCrLf & _
                        "No = Thực hiện ngay" & vbCrLf & _
                        "Cancel = Hủy", _
                        vbYesNoCancel + vbQuestion, "Tùy chọn xử lý")
    
    Select Case userChoice
        Case vbYes
            PreviewChanges
        Case vbNo
            ProcessPresentation isPreview:=False
        Case vbCancel
            Exit Sub
    End Select
    
    elapsedTime = Timer - startTime
    
    ' Hiển thị thống kê
    If Not userChoice = vbYes Then
        ShowStatistics elapsedTime
    End If
End Sub

' ===========================
' PREVIEW MODE
' ===========================
Private Sub PreviewChanges()
    Dim actions() As ActionItem
    Dim actionCount As Long
    Dim previewMsg As String
    Dim i As Long
    Dim userChoice As VbMsgBoxResult
    
    ' Thu thập actions
    actionCount = 0
    ReDim actions(0 To 0)
    
    CollectAllActions actions, actionCount
    
    If actionCount = 0 Then
        MsgBox "Không tìm thấy textbox nào cần xử lý.", vbInformation
        Exit Sub
    End If
    
    ' Tạo preview message (giới hạn 10 items đầu)
    previewMsg = "Tìm thấy " & actionCount & " thay đổi:" & vbCrLf & vbCrLf
    
    For i = 0 To IIf(actionCount > 10, 9, actionCount - 1)
        previewMsg = previewMsg & "Slide " & actions(i).SlideIndex & " - " & actions(i).ShapeName & ": "
        If actions(i).DeleteShape Then
            previewMsg = previewMsg & "[XÓA]" & vbCrLf
        Else
            previewMsg = previewMsg & "[CẬP NHẬT]" & vbCrLf
        End If
    Next i
    
    If actionCount > 10 Then
        previewMsg = previewMsg & vbCrLf & "... và " & (actionCount - 10) & " thay đổi khác." & vbCrLf
    End If
    
    previewMsg = previewMsg & vbCrLf & "Bạn có muốn tiếp tục?"
    
    userChoice = MsgBox(previewMsg, vbYesNo + vbQuestion, "Xác nhận xử lý")
    
    If userChoice = vbYes Then
        ProcessPresentation isPreview:=False
    End If
End Sub

' ===========================
' MAIN PROCESSING
' ===========================
Private Sub ProcessPresentation(Optional isPreview As Boolean = False)
    Dim actions() As ActionItem
    Dim actionCount As Long
    
    On Error GoTo ErrHandler
    
    ' Reset statistics
    ResetStatistics
    
    ' Khởi tạo progress (nếu không preview)
    If Not isPreview Then
        Application.ScreenUpdating = False
    End If
    
    ' Thu thập hành động
    actionCount = 0
    ReDim actions(0 To 0)
    CollectAllActions actions, actionCount
    
    If actionCount = 0 Then
        MsgBox "Không có textbox nào cần xử lý.", vbInformation
        GoTo ExitPoint
    End If
    
    ' Backup cho undo
    m_UndoCount = actionCount
    ReDim m_UndoActions(0 To actionCount - 1)
    Dim i As Long
    For i = 0 To actionCount - 1
        m_UndoActions(i) = actions(i)
    Next i
    
    ' Thực hiện các hành động
    If Not isPreview Then
        PerformActions actions, actionCount
    End If
    
ExitPoint:
    Application.ScreenUpdating = True
    Exit Sub
    
ErrHandler:
    Application.ScreenUpdating = True
    MsgBox "Lỗi: " & Err.Number & " - " & Err.Description, vbExclamation
    Resume ExitPoint
End Sub

' ===========================
' COLLECT ACTIONS
' ===========================
Private Sub CollectAllActions(ByRef actions() As ActionItem, ByRef actionCount As Long)
    Dim sld As Slide
    Dim shp As Shape
    Dim slideCount As Long
    
    slideCount = ActivePresentation.Slides.Count
    m_Stats.TotalSlides = slideCount
    
    For Each sld In ActivePresentation.Slides
        For Each shp In sld.Shapes
            CollectActionsForShape sld.SlideIndex, shp, "", actions, actionCount
        Next shp
    Next sld
End Sub

Private Sub CollectActionsForShape(ByVal slideIndex As Long, _
                                    ByRef shp As Shape, _
                                    ByVal pathSoFar As String, _
                                    ByRef actions() As ActionItem, _
                                    ByRef actionCount As Long)
    Dim currentPath As String
    Dim rawText As String
    Dim newText As String
    Dim shapeName As String
    
    On Error Resume Next
    If shp Is Nothing Then Exit Sub
    
    ' Đếm shape
    m_Stats.TotalShapes = m_Stats.TotalShapes + 1
    
    ' Tạo path và lấy tên shape
    If pathSoFar = "" Then
        currentPath = CStr(shp.Id)
    Else
        currentPath = pathSoFar & "/" & CStr(shp.Id)
    End If
    
    shapeName = shp.Name
    If Len(shapeName) = 0 Then shapeName = "Shape" & shp.Id
    
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
    
    ' Lọc text
    Dim linesRemoved As Long
    Dim linesKept As Long
    newText = FilterKeepNonAsciiLines(rawText, linesRemoved, linesKept)
    
    ' Cập nhật thống kê
    m_Stats.LinesRemoved = m_Stats.LinesRemoved + linesRemoved
    m_Stats.LinesKept = m_Stats.LinesKept + linesKept
    
    ' Thêm action nếu có thay đổi
    If Len(Trim(newText)) = 0 Then
        ' Xóa shape
        AddAction actions, actionCount, slideIndex, currentPath, shapeName, rawText, "", True
        m_Stats.ShapesDeleted = m_Stats.ShapesDeleted + 1
    ElseIf Not TextsAreEqual(rawText, newText) Then
        ' Cập nhật text
        AddAction actions, actionCount, slideIndex, currentPath, shapeName, rawText, newText, False
        m_Stats.ShapesModified = m_Stats.ShapesModified + 1
    End If
End Sub

' Helper: Thêm action vào mảng
Private Sub AddAction(ByRef actions() As ActionItem, _
                      ByRef actionCount As Long, _
                      ByVal slideIndex As Long, _
                      ByVal path As String, _
                      ByVal shapeName As String, _
                      ByVal originalText As String, _
                      ByVal newText As String, _
                      ByVal deleteShape As Boolean)
    actionCount = actionCount + 1
    ReDim Preserve actions(0 To actionCount - 1)
    
    With actions(actionCount - 1)
        .SlideIndex = slideIndex
        .ShapeIdPath = path
        .ShapeName = shapeName
        .OriginalText = originalText
        .NewText = newText
        .DeleteShape = deleteShape
    End With
End Sub

' ===========================
' PERFORM ACTIONS
' ===========================
Private Sub PerformActions(ByRef actions() As ActionItem, ByVal actionCount As Long)
    Dim i As Long
    Dim sld As Slide
    Dim targetShape As Shape
    Dim successCount As Long
    
    On Error Resume Next
    
    ' Cập nhật text trước
    For i = 0 To actionCount - 1
        If Not actions(i).DeleteShape Then
            Set sld = ActivePresentation.Slides(actions(i).SlideIndex)
            Set targetShape = ResolveShapeByPath(sld, actions(i).ShapeIdPath)
            
            If Not targetShape Is Nothing Then
                If SetShapeText(targetShape, actions(i).NewText) Then
                    successCount = successCount + 1
                End If
            End If
        End If
    Next i
    
    ' Xóa shapes sau (ngược từ cuối lên)
    For i = actionCount - 1 To 0 Step -1
        If actions(i).DeleteShape Then
            Set sld = ActivePresentation.Slides(actions(i).SlideIndex)
            Set targetShape = ResolveShapeByPath(sld, actions(i).ShapeIdPath)
            
            If Not targetShape Is Nothing Then
                targetShape.Delete
                successCount = successCount + 1
            End If
        End If
    Next i
    
    On Error GoTo 0
End Sub

' ===========================
' UNDO FUNCTIONALITY
' ===========================
Sub UndoLastCleanup()
    Dim i As Long
    Dim sld As Slide
    Dim targetShape As Shape
    Dim restoredCount As Long
    
    On Error Resume Next
    
    If m_UndoCount = 0 Then
        MsgBox "Không có thao tác nào để hoàn tác.", vbInformation
        Exit Sub
    End If
    
    Dim userChoice As VbMsgBoxResult
    userChoice = MsgBox("Bạn có chắc muốn hoàn tác " & m_UndoCount & " thay đổi?", _
                        vbYesNo + vbQuestion, "Xác nhận Undo")
    
    If userChoice = vbNo Then Exit Sub
    
    Application.ScreenUpdating = False
    
    ' Khôi phục text cho các shapes đã cập nhật
    For i = 0 To m_UndoCount - 1
        If Not m_UndoActions(i).DeleteShape Then
            Set sld = ActivePresentation.Slides(m_UndoActions(i).SlideIndex)
            Set targetShape = ResolveShapeByPath(sld, m_UndoActions(i).ShapeIdPath)
            
            If Not targetShape Is Nothing Then
                If SetShapeText(targetShape, m_UndoActions(i).OriginalText) Then
                    restoredCount = restoredCount + 1
                End If
            End If
        End If
    Next i
    
    Application.ScreenUpdating = True
    
    ' Lưu ý: Không thể khôi phục shapes đã xóa (cần phức tạp hơn)
    MsgBox "Đã khôi phục " & restoredCount & " textbox." & vbCrLf & _
           "Lưu ý: Không thể khôi phục các shape đã bị xóa.", vbInformation
    
    ' Clear undo buffer
    m_UndoCount = 0
    Erase m_UndoActions
End Sub

' ===========================
' HELPER FUNCTIONS
' ===========================

' Lấy text từ shape (an toàn)
Private Function GetShapeText(ByRef shp As Shape) As String
    Dim txt As String
    
    On Error Resume Next
    txt = ""
    
    ' Thử TextFrame trước
    If shp.HasTextFrame Then
        If shp.TextFrame.HasText Then
            txt = shp.TextFrame.TextRange.Text
        End If
    End If
    
    ' Fallback TextFrame2
    If Len(Trim(txt)) = 0 Then
        Err.Clear
        txt = shp.TextFrame2.TextRange.Text
    End If
    
    On Error GoTo 0
    GetShapeText = txt
End Function

' Set text cho shape (an toàn)
Private Function SetShapeText(ByRef shp As Shape, ByVal txt As String) As Boolean
    On Error Resume Next
    
    SetShapeText = False
    
    If shp.HasTextFrame Then
        shp.TextFrame.TextRange.Text = txt
        SetShapeText = (Err.Number = 0)
    Else
        shp.TextFrame2.TextRange.Text = txt
        SetShapeText = (Err.Number = 0)
    End If
    
    On Error GoTo 0
End Function

' Lọc dòng - Nâng cấp với thống kê
Private Function FilterKeepNonAsciiLines(ByVal txt As String, _
                                         ByRef linesRemoved As Long, _
                                         ByRef linesKept As Long) As String
    Dim normalized As String
    Dim lines() As String
    Dim ln As Long
    Dim outLines() As String
    Dim outCount As Long
    
    normalized = NormalizeLineEnds(txt)
    lines = Split(normalized, vbLf)
    
    ReDim outLines(0 To UBound(lines))
    outCount = 0
    linesRemoved = 0
    linesKept = 0
    
    For ln = LBound(lines) To UBound(lines)
        If ShouldKeepLine(lines(ln)) Then
            outLines(outCount) = lines(ln)
            outCount = outCount + 1
            linesKept = linesKept + 1
        Else
            If Len(Trim(lines(ln))) > 0 Then
                linesRemoved = linesRemoved + 1
            End If
        End If
    Next ln
    
    ' Join lines
    If outCount > 0 Then
        ReDim Preserve outLines(0 To outCount - 1)
        FilterKeepNonAsciiLines = Join(outLines, vbCrLf)
    Else
        FilterKeepNonAsciiLines = ""
    End If
End Function

' Kiểm tra có nên giữ dòng không (có Unicode char)
Private Function ShouldKeepLine(ByVal line As String) As Boolean
    Dim ch As Long
    Dim charCode As Long
    
    ShouldKeepLine = False
    
    If Len(Trim(line)) = 0 Then Exit Function
    
    For ch = 1 To Len(line)
        charCode = AscW(Mid(line, ch, 1))
        
        ' Kiểm tra Unicode (>127) hoặc các ký tự đặc biệt tiếng Việt
        If charCode > 127 Or charCode < 0 Then
            ShouldKeepLine = True
            Exit Function
        End If
    Next ch
End Function

' So sánh 2 text (ignore whitespace differences)
Private Function TextsAreEqual(ByVal txt1 As String, ByVal txt2 As String) As Boolean
    TextsAreEqual = (StrComp(Trim(NormalizeLineEnds(txt1)), _
                             Trim(NormalizeLineEnds(txt2)), _
                             vbTextCompare) = 0)
End Function

' Chuẩn hóa line endings
Private Function NormalizeLineEnds(ByVal s As String) As String
    s = Replace(s, vbCrLf, vbLf)
    s = Replace(s, vbCr, vbLf)
    NormalizeLineEnds = s
End Function

' Resolve shape by path
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
    
    ' Nếu chỉ có 1 part
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

' ===========================
' STATISTICS & REPORTING
' ===========================
Private Sub ResetStatistics()
    With m_Stats
        .TotalSlides = 0
        .TotalShapes = 0
        .ShapesModified = 0
        .ShapesDeleted = 0
        .LinesRemoved = 0
        .LinesKept = 0
    End With
End Sub

Private Sub ShowStatistics(ByVal elapsedTime As Double)
    Dim msg As String
    
    msg = "=== KẾT QUẢ XỬ LÝ ===" & vbCrLf & vbCrLf
    msg = msg & "Tổng số slide: " & m_Stats.TotalSlides & vbCrLf
    msg = msg & "Tổng số shape: " & m_Stats.TotalShapes & vbCrLf
    msg = msg & "Shape đã cập nhật: " & m_Stats.ShapesModified & vbCrLf
    msg = msg & "Shape đã xóa: " & m_Stats.ShapesDeleted & vbCrLf
    msg = msg & vbCrLf
    msg = msg & "Dòng đã xóa: " & m_Stats.LinesRemoved & vbCrLf
    msg = msg & "Dòng đã giữ: " & m_Stats.LinesKept & vbCrLf
    msg = msg & vbCrLf
    msg = msg & "Thời gian: " & Format(elapsedTime, "0.00") & " giây" & vbCrLf
    msg = msg & vbCrLf
    msg = msg & "Sử dụng 'UndoLastCleanup' để hoàn tác nếu cần."
    
    MsgBox msg, vbInformation, "Hoàn tất"
End Sub

' ===========================
' EXPORT LOG (BONUS FEATURE)
' ===========================
Sub ExportProcessingLog()
    Dim msg As String
    
    msg = "Tính năng này sẽ xuất log chi tiết ra file text." & vbCrLf & _
          "Hiện chưa được implement trong phiên bản này." & vbCrLf & vbCrLf & _
          "Bạn có thể mở rộng thêm bằng cách lưu m_UndoActions ra file."
    
    MsgBox msg, vbInformation
End Sub

' ===========================
' BATCH PROCESSING WITH OPTIONS
' ===========================
Sub ProcessWithOptions()
    Dim keepEmptyShapes As Boolean
    Dim minUnicodeChars As Long
    Dim userInput As String
    
    ' Có thể thêm dialog form để người dùng chọn options
    userInput = InputBox("Số ký tự Unicode tối thiểu để giữ dòng (mặc định 1):", "Tùy chọn", "1")
    
    If IsNumeric(userInput) Then
        minUnicodeChars = CLng(userInput)
        ' TODO: Implement logic với minUnicodeChars
    End If
    
    MsgBox "Tính năng này có thể được mở rộng thêm theo nhu cầu.", vbInformation
End Sub
