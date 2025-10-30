Option Explicit

' ===========================
' MODULE: modMain
' Mô tả: Module chính với UserForm - Xử lý Unicode tiếng Việt
' ===========================

' Cấu trúc lưu trữ hành động
Public Type ActionItem
    SlideIndex As Long
    ShapeIdPath As String
    OriginalText As String
    NewText As String
    DeleteShape As Boolean
    ShapeName As String
End Type

' Cấu trúc thống kê
Public Type Statistics
    TotalSlides As Long
    TotalShapes As Long
    ShapesModified As Long
    ShapesDeleted As Long
    LinesRemoved As Long
    LinesKept As Long
    ProcessingTime As Double
End Type

' Biến toàn cục
Public g_UndoActions() As ActionItem
Public g_UndoCount As Long
Public g_Stats As Statistics
Public g_PreviewActions() As ActionItem
Public g_PreviewCount As Long

' ===========================
' ENTRY POINT - Mở UserForm
' ===========================
Sub ShowTextCleanerForm()
    frmTextCleaner.Show
End Sub

' ===========================
' CORE PROCESSING FUNCTIONS
' ===========================

' Thu thập tất cả actions
Public Sub CollectAllActions(ByRef actions() As ActionItem, ByRef actionCount As Long)
    Dim sld As Slide
    Dim shp As Shape
    
    On Error Resume Next
    
    actionCount = 0
    ReDim actions(0 To 0)
    
    g_Stats.TotalSlides = ActivePresentation.Slides.Count
    g_Stats.TotalShapes = 0
    g_Stats.ShapesModified = 0
    g_Stats.ShapesDeleted = 0
    g_Stats.LinesRemoved = 0
    g_Stats.LinesKept = 0
    
    For Each sld In ActivePresentation.Slides
        For Each shp In sld.Shapes
            CollectActionsForShape sld.SlideIndex, shp, "", actions, actionCount
        Next shp
    Next sld
End Sub

' Thu thập action cho từng shape
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
    
    g_Stats.TotalShapes = g_Stats.TotalShapes + 1
    
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
    
    ' Lấy text với Unicode support
    rawText = GetShapeTextUnicode(shp)
    If Len(Trim(rawText)) = 0 Then Exit Sub
    
    ' Lọc text
    Dim linesRemoved As Long
    Dim linesKept As Long
    newText = FilterKeepNonAsciiLines(rawText, linesRemoved, linesKept)
    
    g_Stats.LinesRemoved = g_Stats.LinesRemoved + linesRemoved
    g_Stats.LinesKept = g_Stats.LinesKept + linesKept
    
    ' Thêm action nếu có thay đổi
    If Len(Trim(newText)) = 0 Then
        AddAction actions, actionCount, slideIndex, currentPath, shapeName, rawText, "", True
        g_Stats.ShapesDeleted = g_Stats.ShapesDeleted + 1
    ElseIf Not TextsAreEqual(rawText, newText) Then
        AddAction actions, actionCount, slideIndex, currentPath, shapeName, rawText, newText, False
        g_Stats.ShapesModified = g_Stats.ShapesModified + 1
    End If
End Sub

' Thêm action
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

' Thực hiện actions
Public Sub PerformActions(ByRef actions() As ActionItem, ByVal actionCount As Long)
    Dim i As Long
    Dim sld As Slide
    Dim targetShape As Shape
    
    On Error Resume Next
    Application.ScreenUpdating = False
    
    ' Backup cho undo
    g_UndoCount = actionCount
    ReDim g_UndoActions(0 To actionCount - 1)
    For i = 0 To actionCount - 1
        g_UndoActions(i) = actions(i)
    Next i
    
    ' Cập nhật text
    For i = 0 To actionCount - 1
        If Not actions(i).DeleteShape Then
            Set sld = ActivePresentation.Slides(actions(i).SlideIndex)
            Set targetShape = ResolveShapeByPath(sld, actions(i).ShapeIdPath)
            
            If Not targetShape Is Nothing Then
                SetShapeTextUnicode targetShape, actions(i).NewText
            End If
        End If
    Next i
    
    ' Xóa shapes
    For i = actionCount - 1 To 0 Step -1
        If actions(i).DeleteShape Then
            Set sld = ActivePresentation.Slides(actions(i).SlideIndex)
            Set targetShape = ResolveShapeByPath(sld, actions(i).ShapeIdPath)
            
            If Not targetShape Is Nothing Then
                targetShape.Delete
            End If
        End If
    Next i
    
    Application.ScreenUpdating = True
End Sub

' Undo
Public Sub PerformUndo()
    Dim i As Long
    Dim sld As Slide
    Dim targetShape As Shape
    
    On Error Resume Next
    Application.ScreenUpdating = False
    
    For i = 0 To g_UndoCount - 1
        If Not g_UndoActions(i).DeleteShape Then
            Set sld = ActivePresentation.Slides(g_UndoActions(i).SlideIndex)
            Set targetShape = ResolveShapeByPath(sld, g_UndoActions(i).ShapeIdPath)
            
            If Not targetShape Is Nothing Then
                SetShapeTextUnicode targetShape, g_UndoActions(i).OriginalText
            End If
        End If
    Next i
    
    Application.ScreenUpdating = True
    
    g_UndoCount = 0
    Erase g_UndoActions
End Sub

' ===========================
' UNICODE TEXT FUNCTIONS
' ===========================

' Lấy text với Unicode support
Public Function GetShapeTextUnicode(ByRef shp As Shape) As String
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
    GetShapeTextUnicode = txt
End Function

' Set text với Unicode support
Public Sub SetShapeTextUnicode(ByRef shp As Shape, ByVal txt As String)
    On Error Resume Next
    
    If shp.HasTextFrame Then
        shp.TextFrame.TextRange.Text = txt
    Else
        shp.TextFrame2.TextRange.Text = txt
    End If
    
    On Error GoTo 0
End Sub

' Lọc giữ dòng có Unicode
Public Function FilterKeepNonAsciiLines(ByVal txt As String, _
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
    
    If outCount > 0 Then
        ReDim Preserve outLines(0 To outCount - 1)
        FilterKeepNonAsciiLines = Join(outLines, vbCrLf)
    Else
        FilterKeepNonAsciiLines = ""
    End If
End Function

' Kiểm tra có giữ dòng không
Public Function ShouldKeepLine(ByVal line As String) As Boolean
    Dim ch As Long
    Dim charCode As Long
    
    ShouldKeepLine = False
    
    If Len(Trim(line)) = 0 Then Exit Function
    
    For ch = 1 To Len(line)
        charCode = AscW(Mid(line, ch, 1))
        
        ' Unicode characters hoặc negative codes (tiếng Việt có dấu)
        If charCode > 127 Or charCode < 0 Then
            ShouldKeepLine = True
            Exit Function
        End If
    Next ch
End Function

' ===========================
' HELPER FUNCTIONS
' ===========================

Public Function TextsAreEqual(ByVal txt1 As String, ByVal txt2 As String) As Boolean
    TextsAreEqual = (StrComp(Trim(NormalizeLineEnds(txt1)), _
                             Trim(NormalizeLineEnds(txt2)), _
                             vbTextCompare) = 0)
End Function

Public Function NormalizeLineEnds(ByVal s As String) As String
    s = Replace(s, vbCrLf, vbLf)
    s = Replace(s, vbCr, vbLf)
    NormalizeLineEnds = s
End Function

Public Function ResolveShapeByPath(ByRef sld As Slide, ByVal path As String) As Shape
    Dim parts() As String
    Dim curShape As Shape
    Dim curItem As Shape
    Dim i As Long
    Dim gi As Shape
    
    On Error Resume Next
    Set ResolveShapeByPath = Nothing
    
    If Len(Trim(path)) = 0 Then Exit Function
    
    parts = Split(path, "/")
    
    For Each curShape In sld.Shapes
        If CStr(curShape.Id) = parts(0) Then Exit For
    Next curShape
    
    If curShape Is Nothing Then Exit Function
    
    If UBound(parts) = 0 Then
        Set ResolveShapeByPath = curShape
        Exit Function
    End If
    
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

' Format số với dấu phẩy ngăn cách
Public Function FormatNumber(ByVal num As Long) As String
    FormatNumber = Format(num, "#,##0")
End Function

' Format thời gian
Public Function FormatTime(ByVal seconds As Double) As String
    If seconds < 1 Then
        FormatTime = Format(seconds * 1000, "0") & " ms"
    Else
        FormatTime = Format(seconds, "0.00") & " giây"
    End If
End Function
